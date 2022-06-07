import pprint

import matplotlib.pyplot as plt
import numpy as np
import osmnx as ox

from matplotlib.widgets import Button

from app_io import load_input
from ax_settings import Ax_settings
from app_plot import plot_graph_route, plot_segment_line, plot_segment_edge


def get_route_network():
    cz010 = ox.geocode_to_gdf({"country": "Czech Republic", "county": "Hlavní město Praha"})
    return ox.graph_from_polygon(cz010.geometry[0], network_type="drive", retain_all=True, clean_periphery=False,
                                 custom_filter='["highway"~"motorway|trunk|primary|secondary"]')


def plot_timestamp_test(time, g, ax):
    if time == 0:
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
        return plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
    if time == 1:
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
        plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
        return plot_segment_edge(g,  29166269, 8811408, ax, 50, 30)
    if time == 2:
        plot_segment_edge(g, 1835840419, 409801399, ax, 1, 50)
        plot_segment_edge(g, 409801399, 29166269, ax, 50, 50)
        plot_segment_edge(g, 29166269, 8811408, ax, 50, 30)
        plot_segment_edge(g, 8811408, 8811405, ax, 30, 30)
        return plot_segment_edge(g, 8811405, 1262229633, ax, 30, 1)


class FrameSwitch:
    def __init__(self, g, ax, ax_settings, times=None):
        self.i = 0
        self.g = g
        self.ax_settings = ax_settings
        self.ax = ax
        self.times = times

    def plot(self):
        print(self.i)
        self.ax.clear()
        self.ax_settings.apply(self.ax)
        self.ax.axis('off')

        if self.times is not None:
            self.check_bounds()
            print(self.times[self.i])
            segments = self.times[self.i]
            _ = plot_graph_route(self.g, segments, ax=self.ax, show=False, close=False, node_size=1)  # ax2 plot
        else:
            plot_timestamp_test(self.i, self.g, self.ax)
        plt.show()

    def check_bounds(self):
        if self.i < 0:
            self.i = 0
        elif self.i >= len(self.times):
            self.i = len(self.times) - 1

    def next(self, event):
        self.i = self.i + 1
        self.plot()

    def prev(self, event):
        self.i = self.i - 1
        self.plot()


def with_buttons():
    g = get_route_network()
    # times = load_input("../data/gv-osm_nodes_id.pickle")
    times = None

    # twin axes
    f, ax_map = plt.subplots()
    _, ax_map = ox.plot_graph(g, ax=ax_map, node_size=0, show=False)
    ax_density = ax_map.twinx()
    ax_density.axis('off')
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())
    ax_map_settings.apply(ax_density)

    # add buttons
    callback = FrameSwitch(g, ax_density, ax_map_settings, times)

    axprev = plt.axes([0.7, 0.005, 0.1, 0.075])
    axnext = plt.axes([0.81, 0.005, 0.1, 0.075])
    bnext = Button(axnext, 'Next')
    bnext.on_clicked(callback.next)
    bprev = Button(axprev, 'Previous')
    bprev.on_clicked(callback.prev)

    plt.show()


if __name__ == "__main__":
    with_buttons()
