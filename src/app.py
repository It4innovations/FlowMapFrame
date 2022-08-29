import click
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


def animate(g, times, ax, ax_settings, timestamp_from, max_count, width_modif, width_style):
    def step(i):
        print(i)
        segments = times.loc[timestamp_from + i]

        ax.clear()
        ax_settings.apply(ax)
        ax.axis('off')

        plot_routes(g, segments, ax=ax,
                    min_density=1, max_density=10,
                    min_width_density=10, max_width_density=max_count,
                    width_modifier=width_modif,
                    width_style=width_style
                    )

    return step


@click.command()
@click.option('--map-file', default="../data/map.graphml",
              help='GRAPHML file with map.')
@click.option('--segments-file', default="../data/data.pkl", help='File with preprocessed data into segments datafame.')
@click.option('--frames-start', default=0, help="Number of frames to skip before plotting.")
@click.option('--frames-len', default=None, type=int, help="Number of frames to plot.")
@click.option('--width-style', default='boxed',
              help="Style of the line for wide segments. [boxed/caligraphy]")
@click.option('--width-modif', default=10, type=click.IntRange(2, 200, clamp=True), show_default=True,
              help="Adjust width.")
@click.option('--save-path', default="", help='Path to the folder for the output video.')
def main(map_file, segments_file, frames_start, frames_len, width_style, width_modif, save_path):
    start = datetime.now()
    g = get_route_network(map_file)

    # PREPROCESSED DATA
    times_df = pd.read_pickle(segments_file)

    timestamp_from = times_df.index.min() + frames_start
    times_len = times_df.index.max() - timestamp_from
    times_len = min(frames_len, times_len) if frames_len else times_len
    max_count = times_df['vehicle_count'].max()

    print(times_len)
    print(times_df.to_string(index=True, max_rows=100))

    f, ax_map = plt.subplots()
    fig, ax_map = ox.plot_graph(g, ax=ax_map, show=False, node_size=0)
    ax_density = ax_map.twinx()
    ax_map_settings = Ax_settings(ylim=ax_map.get_ylim(), aspect=ax_map.get_aspect())

    anim = animation.FuncAnimation(plt.gcf(), animate(g, times_df,
                                                      ax_settings=ax_map_settings, ax=ax_density,
                                                      timestamp_from=timestamp_from,
                                                      max_count=max_count,
                                                      width_modif=width_modif,
                                                      width_style=width_style),
                                   interval=150, frames=times_len, repeat=False)

    timestamp = round(time() * 1000)

    if save_path != '' or save_path[-1] != '/':
        save_path = save_path + '/'
    anim.save(save_path + str(timestamp) + "-rt.mp4", writer="ffmpeg")

    finish = datetime.now()
    print(finish - start)


if __name__ == "__main__":
    main()