import logging

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection

from enum import Enum, unique

from .preprocessing import get_width_polygon, plot_polygon_patch


@unique
class WidthStyle(Enum):
    BOXED = 1
    CALLIGRAPHY = 2
    EQUIDISTANT = 3


def plot_routes(G, segments, ax,
                min_density=1, max_density=10,
                min_width_density=10, max_width_density=50,
                width_modifier=1,
                width_style: WidthStyle = WidthStyle.BOXED,
                round_edges=True):
    lines = []
    color_scalars = []
    polygons = []
    false_segments = 0
    if isinstance(segments, pd.Series):
        segments = pd.DataFrame([segments])

    for _, s in segments.iterrows():
        lines_new, color_scalars_new, polygons_new = plot_route(G, s, ax, min_width_density, max_width_density,
                                                                width_modifier=width_modifier,
                                                                width_style=width_style, round_edges=round_edges)
        if lines_new is None:
            false_segments += 1
        else:
            lines.append(lines_new)
            color_scalars.append(color_scalars_new)
            polygons.extend(polygons_new)

    logging.error(f"False segments: {false_segments} from {segments.shape}")

    if not lines:
        return

    # plotting of gradient lines
    lines = np.vstack(lines)
    color_scalars = np.hstack(color_scalars)
    norm = plt.Normalize(min_density, max_density)

    coll = LineCollection(lines, cmap='autumn_r', norm=norm)

    # width in collection
    if width_style == WidthStyle.BOXED:
        line_widths = np.interp(color_scalars, [min_width_density, max_width_density], [2, 2 + width_modifier])
        coll.set_linewidth(line_widths)
        if round_edges:
            coll.set_capstyle('round')

    coll.set_array(color_scalars)
    ax.add_collection(coll, autolim=False)

    if polygons:
        polygons = plot_polygon_patch(ax, polygons)

    return coll, polygons


def plot_route(G, segment, ax,
               min_width_density, max_width_density,
               width_modifier,
               width_style: WidthStyle,
               round_edges=True,
               **pg_kwargs):
    edge = G.get_edge_data(segment['node_from'], segment['node_to'])
    if edge is None:
        return None, None, None
    else:
        x, y = get_node_coordinates(edge, G, segment)

        # color gradient
        density_from = segment['count_from']
        density_to = segment['count_to']

        line = reshape(x, y)
        color_scalar = np.linspace(density_from, density_to, len(x) - 1)
        polygons = []

        # width as filling
        if width_style == WidthStyle.CALLIGRAPHY:
            polygons = get_width_polygon(ax, x, y, density_from, density_to, min_width_density, max_width_density,
                                         width_modifier, equidistant=False, round_edges=round_edges)

        elif width_style == WidthStyle.EQUIDISTANT:
            polygons = get_width_polygon(ax, x, y, density_from, density_to, min_width_density, max_width_density,
                                         width_modifier, equidistant=True, round_edges=round_edges)

        return line, color_scalar, polygons


def get_node_coordinates(edge, G, s):
    x = []
    y = []

    data = min(edge.values(), key=lambda d: d["length"])
    if "geometry" in data:
        xs, ys = data["geometry"].xy
        x.extend(xs)
        y.extend(ys)
    else:
        x.extend((G.nodes[s['node_from']]["x"], G.nodes[s['node_to']]["x"]))
        y.extend((G.nodes[s['node_from']]["y"], G.nodes[s['node_to']]["y"]))

    return x, y


def reshape(x, y):
    """
    Transforms x and y coords lists into list of lines (defined by START and END point)
    """
    points = np.vstack([x, y]).T.reshape(-1, 1, 2)
    points = np.concatenate([points[:-1], points[1:]], axis=1)
    return points
