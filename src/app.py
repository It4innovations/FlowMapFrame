from os import path

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


def get_witdh_style(style):
    return {
        'boxed': 1, 'b': 1, '1': 1,
        'caligraphy': 2, 'c': 2, '2': 2,
        'equidistant': 3, 'e': 3, '3': 3,
    }.get(style, 1)


@click.command()
@click.argument('map-file', type=click.Path(exists=True))
@click.argument('segments-file', type=click.Path(exists=True))
@click.option('--frames-start', default=0, help="Number of frames to skip before plotting.")
@click.option('--frames-len', type=int, help="Number of frames to plot.")
@click.option('--width-style', default='boxed',
              help="Style of the line for wide segments. [boxed|caligraphy|equidistant]")
@click.option('--width-modif', default=10, type=click.IntRange(2, 200, clamp=True), show_default=True,
              help="Adjust width.")
@click.option('--save-path', default="", help='Path to the folder for the output video.')
def main(map_file, segments_file, frames_start, frames_len, width_style, width_modif, save_path):
    """Create a video of the traffic situation.

    | MAP_FILE is graphml file with map of the plotted area.
    | SEGMENTS_FILE is pickle file with preprocessed traffic data
    """
    start = datetime.now()
    print(start)
    g = get_route_network(map_file)

    width_style = get_witdh_style(width_style)

    # PREPROCESSED DATA
    times_df = pd.read_pickle(segments_file)

    timestamp_from = times_df.index.min() + frames_start
    times_len = times_df.index.max() - timestamp_from
    times_len = min(frames_len, times_len) if frames_len else times_len
    max_count = times_df['vehicle_count'].max()

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

    anim.save(path.join(save_path, str(timestamp) + "-rt.mp4"), writer="ffmpeg")

    finish = datetime.now()
    print(finish - start)


if __name__ == "__main__":
    main()
