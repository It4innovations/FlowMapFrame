import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib import animation

from app_io import load_input
from datetime import datetime
from time import time
from ax_settings import Ax_settings


def anim(g, times, ax, ax_settings):

    def step(i):
        print(i)
        segments = times[i]

        ax.clear()
        ax_settings.apply(ax)
        ax_density.axis('off')

        plot_graph_route(g, segments, ax=ax, show=False, close=False, node_size=0)  # ax2 plot

    return step


if __name__ == "__main__":
    start = datetime.now()
    g = get_route_network()
    # times = load_input("../data/gv_325630_records.parquet")
    # times = load_input("../data/gv-osm_nodes_id.pickle")
    times = pd.read_pickle("../data/times.pickle")

    f, ax_map = plt.subplots()
    fig, ax_map = ox.plot_graph(g, ax=ax_map, show=False, node_size=0)
    ax_density = ax_map.twinx()
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())

    anim = animation.FuncAnimation(plt.gcf(), anim(g, times, ax_settings=ax_map_settings, ax=ax_density),
                                   interval=150, frames=1000, repeat=False)

    timestamp = round(time() * 1000)
    anim.save("images/" + str(timestamp) + "-rt.mp4", writer="ffmpeg")
    finish = datetime.now()
    print(finish - start)
