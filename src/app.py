import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib import animation

from datetime import datetime
from time import time
from ax_settings import Ax_settings
from base_graph import get_route_network, get_route_network_small, get_route_network_simple
from collection_plot import plot_routes
from plot_cars import plot_cars


def animate(g, times, ax, ax_settings, timestamp_from):
    def step(i):
        print(i)
        segments = times.loc[timestamp_from + i]

        ax.clear()
        ax_settings.apply(ax)
        ax.axis('off')

        plot_routes(g, segments, ax=ax)

    return step


def main():
    start = datetime.now()
    g = get_route_network()

    # PREPROCESSED DATA
    times_df = pd.read_pickle("../data/data.pkl")
    timestamp_from = times_df.index.min()
    times_len = times_df.index.max() - timestamp_from
    print(times_len)
    print(times_df.to_string(index=True, max_rows=100))

    f, ax_map = plt.subplots()
    fig, ax_map = ox.plot_graph(g, ax=ax_map, show=False, node_size=0)
    ax_density = ax_map.twinx()
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())

    anim = animation.FuncAnimation(plt.gcf(), animate(g, times_df,
                                                      ax_settings=ax_map_settings, ax=ax_density,
                                                      timestamp_from=timestamp_from),
                                   interval=150, frames=times_len, repeat=False)

    timestamp = round(time() * 1000)
    anim.save("../images/" + str(timestamp) + "-rt.mp4", writer="ffmpeg")

    finish = datetime.now()
    print(finish - start)


if __name__ == "__main__":
    main()
