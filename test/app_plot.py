import numpy
import osmnx as ox
import numpy as np


def plot_line(ax, x, y, width_from_m, width_to_m):

    if abs(x[0] - x[-1]) > abs(y[0] - y[-1]):
        d = np.linspace(width_from_m / 10000, width_to_m / 10000, len(y))
        y1 = np.add(y, d)
        y2 = np.subtract(y, d)

        ax.fill_between(x, y1, y2, alpha=.5, linewidth=0)
    else:
        d = numpy.linspace(width_from_m / 10000, width_to_m / 10000, len(x))
        x1 = np.add(x, d)
        x2 = np.subtract(x, d)

        ax.fill_betweenx(y=y, x1=x1, x2=x2, alpha=.5, linewidth=0)



def get_node_density(segments):
    node_densities = {}
    for segment in segments:
        if segment.from_node_id in node_densities:
            node_densities[segment.from_node_id] += segment.vehicle_count
        else:
            node_densities[segment.from_node_id] = segment.vehicle_count

    print(node_densities)
    return node_densities


def plot_graph_route(
        G,
        segments,
        route_alpha=0.5,
        ax=None,
        **pg_kwargs,
):
    if ax is None:
        override = {"show", "save", "close"}
        kwargs = {k: v for k, v in pg_kwargs.items() if k not in override}
        fig, ax = ox.plot_graph(G, show=False, save=False, close=False, **kwargs)
    else:
        fig = ax.figure

    # Add node densities
    node_densities = get_node_density(segments)

    for segment in segments:
        x = []
        y = []
        u = segment.from_node_id
        v = segment.to_node_id

        edge = G.get_edge_data(u, v)
        if edge is None:
            print("Edge not found")
        else:
            data = min(edge.values(), key=lambda d: d["length"])
            if "geometry" in data:
                xs, ys = data["geometry"].xy
                x.extend(xs)
                y.extend(ys)
            else:
                x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
                y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))

            _ = ax.plot(x, y, lw=2, alpha=route_alpha, markersize=0)
            min_width = 6
            width_from = min_width*node_densities[u] if u in node_densities else 0
            width_to = min_width*node_densities[v] if v in node_densities else 0

            plot_line(ax, x, y, width_from, width_to)

    return
