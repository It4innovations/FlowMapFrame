import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from app_plot import get_density, plot_route_width


# TRANSFORMS X AND Y COORDS LISTS INTO LIST OF LINES (DEFINED BY START AND END POINT)
from app_plot_width import plot_line_width_equidistant


def reshape(x, y):
    points = np.vstack([x, y]).T.reshape(-1, 1, 2)
    points = np.concatenate([points[:-1], points[1:]], axis=1)
    return points


def node_ids(G, ax):
    for node in (335776496, 31969990):
        x = G.nodes[node]["x"]
        y = G.nodes[node]["y"]
        ax.text(x, y, node)


def get_node_coordinates(edge, G, s):
    x = []
    y = []

    data = min(edge.values(), key=lambda d: d["length"])
    if "geometry" in data:
        xs, ys = data["geometry"].xy
        x.extend(xs)
        y.extend(ys)
    else:
        x.extend((G.nodes[s.from_node_id]["x"], G.nodes[s.to_node_id]["x"]))
        y.extend((G.nodes[s.from_node_id]["y"], G.nodes[s.to_node_id]["y"]))

    return x, y


# MAIN PLOT FUNCTION
def plot_routes(G, segments, ax,
                min_density=1, max_density=10,
                min_width_density=10, max_width_density=50,
                width_modifier=1,
                width_style=1,
                **pg_kwargs):

    # Count node densities
    node_densities = get_density(segments, G)

    lines = []
    color_scalars = []

    for s in segments:
        edge = G.get_edge_data(s.from_node_id, s.to_node_id)
        if edge is not None:
            x, y = get_node_coordinates(edge, G, s)

            # line collection
            line = reshape(x, y)
            lines.append(line)

            # color gradient
            density_from = node_densities[s.from_node_id]['density'] if s.from_node_id in node_densities else 0
            density_to = node_densities[s.to_node_id]['density'] if s.to_node_id in node_densities else 0

            color_scalar = np.linspace(density_from, density_to, len(x) - 1)
            color_scalars.append(color_scalar)

            # width as filling
            if width_style == 2:
                plot_route_width(ax, x, y, density_from, density_to,
                                 min_width_density, max_width_density, width_modifier, equidistant=False)
            if width_style == 3:
                plot_route_width(ax, x, y, density_from, density_to,
                                 min_width_density, max_width_density, width_modifier, equidistant=True)

    print('lines:', len(lines))
    if len(lines) <= 0:
        return

    # plotting of gradient lines
    lines = np.vstack(lines)
    color_scalars = np.hstack(color_scalars)
    norm = plt.Normalize(min_density, max_density)

    coll = LineCollection(lines, cmap='autumn_r', norm=norm)

    # width in collection
    if width_style == 1:
        line_widths = np.interp(color_scalars, [min_width_density, max_width_density], [2, width_modifier])
        coll.set_linewidth(line_widths)

    coll.set_array(color_scalars)
    ax.add_collection(coll)
