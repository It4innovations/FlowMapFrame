import numpy as np
import pandas as pd

from collection_plot import get_node_coordinates


def get_cars_xy(G, s):

    edge = G.get_edge_data(s['node_from'], s['node_to'])

    if edge is None:
        return [], []
    else:
        x, y = get_node_coordinates(edge, G, s)

        edge_length = G[s['node_from']][s['node_to']][0]['length']
        scale = np.linspace(0, edge_length, len(x))
        cars_x = np.interp(s['start_offset_m'], scale, x)
        cars_y = np.interp(s['start_offset_m'], scale, y)

        return cars_x, cars_y


def plot_cars(G, segments, ax):
    xp = []
    yp = []

    if isinstance(segments, pd.Series):
        x, y = get_cars_xy(G, segments)
    else:
        for _, s in segments.iterrows():
            x, y = get_cars_xy(G, s)
            xp.extend(x)
            yp.extend(y)

    ax.scatter(xp, yp)

