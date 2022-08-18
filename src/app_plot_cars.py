import numpy as np

from app_collection_plot import get_node_coordinates


def get_cars_xy(G, s):

    edge = G.get_edge_data(s.from_node_id, s.to_node_id)

    if edge is None:
        return [], []
    else:
        x, y = get_node_coordinates(edge, G, s)

        edge_length = G[s.from_node_id][s.to_node_id][0]['length']
        scale = np.linspace(0, edge_length, len(x))
        cars_x = np.interp(s.car_offsets, scale, x)
        cars_y = np.interp(s.car_offsets, scale, y)

        return cars_x, cars_y


def plot_cars(G, segments, ax):
    xp = []
    yp = []

    for s in segments:
        x, y = get_cars_xy(G, s)
        xp.extend(x)
        yp.extend(y)

    ax.scatter(xp, yp)

