import osmnx as ox
import networkx as nx
import matplotlib.pyplot as plt

from matplotlib import animation
from app_io import load_input
from scale import get_scale
from app_plot import plot_graph_route
from datetime import datetime
from ax_settings import Ax_settings


def get_route_network():
    cz010 = ox.geocode_to_gdf({"country": "Czech Republic", "county": "Hlavní město Praha"})
    return ox.graph_from_polygon(cz010.geometry[0], network_type="drive", retain_all=True, clean_periphery=False,
                                 custom_filter='["highway"~"motorway|trunk|primary|secondary"]')


def anim(g, times, ax, ax_settings):
    lines = None

    def step(i):
        nonlocal lines
        print(i)
        segments = times[i]

        ax.clear()
        ax_settings.apply(ax)
        lines = plot_graph_route(g, segments, ax=ax, show=False, close=False, node_size=0)  # ax2 plot

    return step


if __name__ == "__main__":
    start = datetime.now()
    g = get_route_network()
    data_start = datetime.now()
    times = load_input("../data/gv-osm_nodes_id.pickle")

    f, ax_map = plt.subplots()
    fig, ax_map = ox.plot_graph(g, ax=ax_map, show=False, node_size=0)
    ax_density = ax_map.twinx()
    ax_density.axis('off')
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())
    anim = animation.FuncAnimation(plt.gcf(), anim(g, times, ax_settings=ax_map_settings, ax=ax_density),
                                   interval=150, frames=len(times), repeat=False)

    plt.show()
    #anim.save("route_test.mp4", writer="ffmpeg")
    finish = datetime.now()
    print(finish - start)
