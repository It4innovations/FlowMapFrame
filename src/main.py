import logging
import pprint

import matplotlib.pyplot as plt
import pandas as pd
import click

from matplotlib.widgets import Slider
from datetime import datetime

from ax_settings import twin_axes

from collection_plot import plot_routes
from base_graph import get_route_network_small, get_route_network_simple, get_route_network
from app import get_witdh_style


def create_sliders(max_time, max_width, width_init):
    plt.subplots_adjust(bottom=0.1)
    time_slider_ax = plt.axes([0.2, 0.06, 0.65, 0.03])
    width_slider_ax = plt.axes([0.2, 0.03, 0.65, 0.03])
    time_slider = Slider(ax=time_slider_ax, label='Time [s]', valmin=0, valmax=max_time, valstep=1)
    width_slider = Slider(ax=width_slider_ax, label='Width', valmin=2, valmax=max_width, valstep=1, valinit=width_init)
    return time_slider, width_slider


@click.command()
@click.argument('map-file', type=click.Path(exists=True))
@click.argument('segments-file', type=click.Path(exists=True))
@click.option('--width-style', default='boxed',
              help="Style of the line for wide segments. [boxed|caligraphy]")
@click.option('--width-modif', default=10, type=click.IntRange(2, 200, clamp=True), show_default=True,
              help="Adjust width.")
def with_slider(map_file, segments_file, width_style, width_modif):
    g = get_route_network(map_file)

    times_df = pd.read_pickle(segments_file)
    f, ax_density, ax_map_settings = twin_axes(g)

    # get max car count
    max_count = times_df['vehicle_count'].max()

    # add slider
    timestamp_from = times_df.index.min()
    times_len = times_df.index.max() - timestamp_from

    time_slider, width_slider = create_sliders(times_len, 100, width_modif)

    width_style = get_witdh_style(width_style)

    def on_press(event):
        nonlocal width_style

        if event.key == 'right':
            time_slider.set_val(time_slider.val + 1)
        elif event.key == 'left':
            time_slider.set_val(time_slider.val - 1)
        elif event.key == 'up':
            width_slider.set_val(width_slider.val + 1)
        elif event.key == 'down':
            width_slider.set_val(width_slider.val - 1)
        elif event.key.isnumeric():
            width_style = int(event.key) % 4
            update()

    f.canvas.mpl_connect('key_press_event', on_press)

    def width_update(val):
        if time_slider.val > -1:
            update()

    def update(val=None):
        if val is None:
            val = time_slider.val

        start = datetime.now()
        # clear ax and copy base map
        ax_density.clear()

        ax_map_settings.apply(ax_density)
        ax_density.axis('off')

        segments = times_df.loc[timestamp_from + val]

        # MAIN PLOT FUNCTION
        width = width_slider.val
        _ = plot_routes(g, segments, ax=ax_density,
                        max_width_density=max_count,
                        width_modifier=width, width_style=width_style)

        f.canvas.draw_idle()

        finish = datetime.now()
        print(finish - start)

    time_slider.on_changed(update)
    width_slider.on_changed(width_update)
    plt.show()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    with_slider()
