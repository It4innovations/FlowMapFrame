import matplotlib.pyplot as plt
import numpy as np
from math import pi
from matplotlib import animation
from datetime import datetime

import osmnx as ox
import networkx as nx


def get_route_network():
    cz010 = ox.geocode_to_gdf({"country": "Czech Republic", "county": "Hlavní město Praha"})
    return ox.graph_from_polygon(cz010.geometry[0], network_type="drive", retain_all=True, clean_periphery=False,
                                 custom_filter='["highway"~"motorway|trunk|primary|secondary"]')


def bell(x, max):
    mean = np.mean(x)
    std = np.std(x)
    y_out = max / (std * np.sqrt(2 * np.pi)) * np.exp(- (x - mean) ** 2 / (2 * std ** 2))
    return y_out


def test_line1(ax, start=0, end=10):
    step = abs(start - end) / 500
    x = np.arange(start, end, step)
    y = x
    y1 = y + bell(x, 5)
    y2 = y - bell(x, 5)

    ax.fill_between(x, y1, y2, alpha=.5, linewidth=0)
    ax.plot(x, y, linewidth=2)

    x = np.arange(end, 2 * end, step)
    y = end - (x - end) / 4
    y1 = y + bell(x, 7)
    y2 = y - bell(x, 7)

    ax.fill_between(x, y1, y2, alpha=.5, linewidth=0)
    ax.plot(x, y, linewidth=2)

    plt.show()


def test_line2(ax, x, y, width_from, width_to):
    d = np.linspace(width_from / 10000, width_to / 10000, len(y))
    y1 = np.add(y, d)
    y2 = np.subtract(y, d)

    ax.fill_between(x, y1, y2, alpha=.5, linewidth=0)
    ax.plot(x, y, linewidth=2)


def plot_route(G, u, v, ax, width_from, width_to):
    x = []
    y = []

    edge = G.get_edge_data(u, v)
    if edge is None:
        print("Help")
    else:
        data = min(edge.values(), key=lambda d: d["length"])
        if "geometry" in data:
            xs, ys = data["geometry"].xy
            x.extend(xs)
            y.extend(ys)
        else:
            x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
            y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))
        test_line2(ax, x, y, width_from, width_to)


def node_ids(G, ax):
    for node in (8811408, 8811405, 29166269, 409801399, 1835840419):
        x = G.nodes[node]["x"]
        y = G.nodes[node]["y"]
        ax.text(x, y, node)


if __name__ == "__main__":
    g = get_route_network()
    print([n for n in g.neighbors(8811408)])

    ax = plt.gca()
    ax.clear()
    _, ax = ox.plot_graph(g, ax=ax, node_size=1, show=False)

    node_ids(g, ax)
    plot_route(g, 409801399, 1835840419, ax, 50, 1)
    plot_route(g, 29166269, 409801399, ax, 50, 1)
    plot_route(g, 8811408, 29166269, ax, 1, 50)

    plt.show()
