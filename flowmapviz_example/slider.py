import os

import matplotlib.pyplot as plt
import pandas as pd
import osmnx as ox
import click
import importlib.resources as pkg_resources

from flowmapviz import map_distance_to_point_units
from matplotlib import rcParams, animation
from matplotlib.widgets import Slider
from datetime import datetime
from time import time

from flowmapviz.plot import plot_routes, WidthStyle
from flowmapviz.zoom import plot_graph_with_zoom, get_zoom_level

from .ax_settings import twin_axes, Ax_settings

rcParams['keymap.back'].remove('left')
rcParams['keymap.forward'].remove('right')
rcParams['keymap.home'].remove('r')


def create_sliders(max_time, max_width, width_init):
    plt.subplots_adjust(bottom=0.1)
    time_slider_ax = plt.axes([0.2, 0.06, 0.65, 0.03])
    width_slider_ax = plt.axes([0.2, 0.03, 0.65, 0.03])
    time_slider = Slider(ax=time_slider_ax, label='Time [s]', valmin=0, valmax=max_time, valstep=1)
    width_slider = Slider(ax=width_slider_ax, label='Width', valmin=2, valmax=max_width, valstep=1, valinit=width_init)
    return time_slider, width_slider


def get_max(times_dic):
    max_count = 0
    for key, time_data in times_dic.items():
        for segment in time_data:
            if type(segment) == tuple:
                segment_max = max(segment[2])
            else:
                segment_max = max(segment['counts'])
            max_count = max(segment_max, max_count)
    return max_count


def display_help():
    text = pkg_resources.read_text(__package__, 'README.md')
    print('\n' + '-' * 80)
    print(text)
    print('\n' + '-' * 80)


@click.command()
@click.argument('map-file', type=click.Path(exists=True))
@click.argument('segments-file', type=click.Path(exists=True))
@click.option('--width-in-map-distance', is_flag=True, default=False, help='if set, width is in map distance, otherwise'
                                                                           'in points')
def main(map_file, segments_file, width_in_map_distance, width_style="EQUIDISTANT", width_modif=10):
    print('Loading data.')
    # read data saved from FlowMapVideo repository
    times_dic = pd.read_pickle(segments_file)

    # load graph
    g = ox.load_graphml(map_file)

    # create slider window
    _ = SliderWindow(g, times_dic, width_style, width_modif, width_in_map_distance)


class SliderWindow:
    def __init__(self, g, times_dic, width_style, width_modif, width_in_map_distance):
        self.times_dic = times_dic
        self.keys = list(sorted(self.times_dic.keys()))

        self.max_count = get_max(self.times_dic)
        print('Max number of cars: ', self.max_count)

        self.g = g
        self.width_style = WidthStyle[width_style]
        self.round_edges = False
        self.roadtypes_by_zoom = False
        self.video_mode = False
        self.width_in_map_distance = width_in_map_distance

        f, self.ax_density, self.ax_map = twin_axes(self.g)
        self.last_zoom_level = get_zoom_level(self.ax_density)

        # add sliders
        self.time_slider, self.width_slider = create_sliders(len(self.keys), 100, width_modif)

        f.canvas.mpl_connect('key_press_event', self.on_press)
        self.time_slider.on_changed(self.update)
        self.width_slider.on_changed(self.width_update)
        self.ax_map.callbacks.connect('xlim_changed', self.on_lim_changed)
        self.ax_map.callbacks.connect('ylim_changed', self.on_lim_changed)

        display_help()
        plt.show()

    def on_lim_changed(self, ax):
        new_zoom_level = get_zoom_level(ax)
        if new_zoom_level != self.last_zoom_level:
            print("set: ", new_zoom_level)
            plot_graph_with_zoom(self.g, self.ax_map)
            self.last_zoom_level = new_zoom_level
            if self.roadtypes_by_zoom:
                self.update()

    def on_press(self, event):
        if event.key == 'right':
            self.time_slider.set_val(self.time_slider.val + 1)
        elif event.key == 'left':
            self.time_slider.set_val(self.time_slider.val - 1)
        elif event.key == 'up':
            self.width_slider.set_val(self.width_slider.val + 1)
        elif event.key == 'down':
            self.width_slider.set_val(self.width_slider.val - 1)
        elif event.key.isnumeric():
            self.width_style = WidthStyle(int(event.key) % 4)
            self.update()
        elif event.key == 'r':
            self.round_edges = not self.round_edges
            self.update()
        elif event.key == 'z':
            self.roadtypes_by_zoom = not self.roadtypes_by_zoom
            self.update()
        elif event.key == 'm':
            self.time_slider.set_val(len(self.keys) // 2)
        elif event.key == 'v':
            print('Video export')
            self.video_mode = True

            anim = animation.FuncAnimation(plt.gcf(), self.animate(), interval=1000, frames=20, repeat=False)

            timestamp = round(time() * 1000)
            anim.save(os.path.join(str(timestamp) + "-rt.gif"), writer="ffmpeg")

            print('DONE')
            self.video_mode = False

    def update(self, val=None):
        if val is None:
            val = self.time_slider.val

        settings = Ax_settings(ylim=self.ax_density.get_ylim(), aspect=self.ax_density.get_aspect())
        self.ax_density.clear()
        settings.apply(self.ax_density)
        self.ax_density.axis('off')

        if val < 0:
            return

        segments = self.times_dic[self.keys[val]]
        nodes_from = [s['node_from'] for s in segments]
        nodes_to = [s['node_to'] for s in segments]
        densities = [s['counts'] for s in segments]

        start = datetime.now()

        # MAIN PLOT FUNCTION
        width = self.width_slider.val
        if self.width_in_map_distance:
            width, _ = map_distance_to_point_units(width / 1000, self.ax_density)

        line_col, poly_col = plot_routes(self.g,
                                         ax=self.ax_density,
                                         nodes_from=nodes_from,
                                         nodes_to=nodes_to,
                                         densities=densities,
                                         min_density=2, max_density=10,
                                         min_width_density=10, max_width_density=self.max_count,
                                         width_modifier=width,
                                         width_style=self.width_style,
                                         round_edges=self.round_edges,
                                         roadtypes_by_zoom=self.roadtypes_by_zoom)

        if not self.video_mode:
            plt.gcf().canvas.draw_idle()

        finish = datetime.now()
        print(val, finish - start)

    def width_update(self, val):
        if self.time_slider.val > -1:
            self.update()

    def animate(self):
        def step(i):
            self.update(self.time_slider.val + i)
            # self.time_slider.set_val(self.time_slider.val + 1)

        return step


if __name__ == "__main__":
    main()
