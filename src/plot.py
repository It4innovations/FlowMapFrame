import numpy
import osmnx as ox
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection


# PLOTS LINE WITH AROUND LINES ABOVE MIN_WIDTH_DENSITY


def plot_route_width(ax, x, y,
                     density_from, density_to,
                     min_width_density, max_width_density,
                     width_modifier=2,
                     equidistant=False
                     ):

    width_from, width_to = np.interp([density_from, density_to],
                                     [min_width_density, max_width_density], [0, 10 * width_modifier])

    if max(width_from, width_to) > 0:
        plot_segment_line_width(ax, x, y, width_from, width_to)


# COLORED SPACE EITHER HORIZONTALLY OR VERTICALLY AROUND LINES
def plot_segment_line_width(ax, x, y, width_from_m, width_to_m):
    if abs(x[0] - x[-1]) > abs(y[0] - y[-1]):
        d = np.linspace(width_from_m / 10000, width_to_m / 10000, len(y))
        y1 = np.add(y, d)
        y2 = np.subtract(y, d)

        ax.fill_between(x, y1, y2, alpha=1, linewidth=0, color='red')
    else:
        d = np.linspace(width_from_m / 10000, width_to_m / 10000, len(x))
        x1 = np.add(x, d)
        x2 = np.subtract(x, d)

        ax.fill_betweenx(y=y, x1=x1, x2=x2, alpha=1, linewidth=0, color='red')


# COUNT CAR DENSITY FOR NODE (WILL MOVE OUTSIDE OF PLOTTING FUNCTIONS)
def get_density(segments, G=None):
    densities = {}

    def _add_density(node, count, node2='density'):
        if node in densities:
            densities[node][node2] += count
        else:
            densities[node] = {node2: count}

    if G is None:
        for segment in segments:
            _add_density(segment.from_node_id, segment.vehicle_count)
    else:
        for segment in segments:

            if G.has_edge(segment.from_node_id, segment.to_node_id):
                edge_length = G[segment.from_node_id][segment.to_node_id][0]['length']

                for offset in segment.car_offsets:
                    if offset < edge_length/2:
                        _add_density(segment.from_node_id, 1)
                    else:
                        _add_density(segment.to_node_id, 1)
    return densities


# PLOTS COLOR GRADIENT ON ONE EDGE
def plot_segment_line_color(x, y, density_from, density_to, min_density, max_density, lw=2):
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    norm = plt.Normalize(min_density, max_density)
    lc = LineCollection(segments, cmap='autumn_r', norm=norm)
    # Set the values used for colormapping
    density_array = np.linspace(density_from, density_to, len(x))
    lc.set_array(density_array)
    lc.set_linewidth(lw)
    return lc


# PLOTS ONE EDGE OF GRAPH
def plot_segment_edge(G, u, v, ax, density_from, density_to,
                      min_color_density=1, max_color_density=10,
                      min_width_density=10, max_width_density=50
):
    x = []
    y = []

    edge = G.get_edge_data(u, v)
    if edge is not None:
        data = min(edge.values(), key=lambda d: d["length"])
        if "geometry" in data:
            xs, ys = data["geometry"].xy
            x.extend(xs)
            y.extend(ys)
        else:
            x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
            y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))

        # simple line
        # _ = ax.plot(x, y, lw=2, alpha=0.5, markersize=0, color='red')

        # colored line
        lc = plot_segment_line_color(x, y, density_from, density_to, min_density=min_color_density, max_density=max_color_density)
        ax.add_collection(lc, autolim=False)

        # line with width if density above min_width_density
        plot_route_width(ax, x, y, density_from, density_to, min_width_density, max_width_density)


# MAIN PLOT FUNCTION
def plot_segments(G, segments, ax=None, **pg_kwargs):
    if ax is None:
        override = {"show", "save", "close"}
        kwargs = {k: v for k, v in pg_kwargs.items() if k not in override}
        fig, ax = ox.plot_graph(G, show=False, save=False, close=False, **kwargs)
    else:
        fig = ax.figure

    # Count node densities
    node_densities = get_density(segments, G)

    for segment in segments:
        if segment.from_node_id not in G:
            # print(f"Node {segment.from_node_id} is None")
            continue

        if segment.to_node_id not in G:
            # print(f"Node {segment.to_node_id} is None")
            continue

        # route = [segment.from_node_id, segment.to_node_id]
        route = ox.shortest_path(G, segment.from_node_id, segment.to_node_id)
        for u, v in zip(route[:-1], route[1:]):
            density_from = node_densities[u]['density'] if u in node_densities else 0
            density_to = node_densities[v]['density'] if v in node_densities else 0
            plot_segment_edge(G, u, v, ax, density_from, density_to)
