import logging

import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import LineCollection

from enum import Enum, unique

from .preprocessing import get_width_polygon, plot_polygon_patch


@unique
class WidthStyle(Enum):
    BOXED = 1
    """
    uses matplotlib.LineCollection
    """
    CALLIGRAPHY = 2
    """
    uses matplotlib.fill_between / matplotlib.fill_betweex
    """
    EQUIDISTANT = 3
    """
    uses matplotlib.PatchCollection
    """


def plot_routes(g: nx.MultiDiGraph,
                segments: pd.DataFrame,
                ax: Axes,
                min_density: int = 1, max_density: int = 10,
                min_width_density: int = 10, max_width_density: int = 50,
                width_modifier: float = 1,
                width_style: WidthStyle = WidthStyle.BOXED,
                round_edges: bool = True,
                plot: bool = True,
                **pg_kwargs):
    """
    Plotting of segments into ax with their density represented by color and width
    :param g: Graph representation of base layer map
    :param segments: Dataframe of segments represented by columns: 'node_from', 'node_to', 'count_from', 'count_to
    :param ax: layer for adding plotted shapes
    :param min_density: density defining color gradient scope
    :param max_density: density defining color gradient scope
    :param min_width_density: density defining width change scope
    :param max_width_density: density defining width change scope
    :param width_modifier: width of the line with max_width_density
    :param width_style: style of the width representation
    :param round_edges: if True plot circles at the end of wide segments for smoother connection
    :return: LineCollection of color segments, PatchCollection of width representation
    :param plot: if True add collections to Ax
    """
    lines = []
    color_scalars = []
    polygons = []
    false_segments = 0
    if isinstance(segments, pd.Series):
        segments = pd.DataFrame([segments])

    for _, s in segments.iterrows():
        lines_new, color_scalars_new, polygons_new = plot_route(g, s, ax, min_width_density, max_width_density,
                                                                width_modifier=width_modifier,
                                                                width_style=width_style, round_edges=round_edges)
        if lines_new is None:
            false_segments += 1
        else:
            lines.append(lines_new)
            color_scalars.append(color_scalars_new)
            polygons.extend(polygons_new)

    logging.info(f"False segments: {false_segments} from {segments.shape}")

    if not lines:
        return None, None

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
    if plot:
        ax.add_collection(coll, autolim=False)

    if polygons and plot:
        polygons = plot_polygon_patch(ax, polygons)

    return coll, polygons


def plot_route(g: nx.MultiDiGraph,
               segment: pd.Series,
               ax: Axes,
               min_width_density: int,
               max_width_density: int,
               width_modifier: float,
               width_style: WidthStyle,
               round_edges: bool = True,
               **pg_kwargs):
    edge = g.get_edge_data(segment['node_from'], segment['node_to'])
    if edge is None:
        return None, None, None
    else:
        x, y = get_node_coordinates(edge, g, segment)

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


def get_node_coordinates(edge, g, s):
    x = []
    y = []

    data = min(edge.values(), key=lambda d: d["length"])
    if "geometry" in data:
        xs, ys = data["geometry"].xy
        x.extend(xs)
        y.extend(ys)
    else:
        x.extend((g.nodes[s['node_from']]["x"], g.nodes[s['node_to']]["x"]))
        y.extend((g.nodes[s['node_from']]["y"], g.nodes[s['node_to']]["y"]))

    return x, y


def reshape(x, y):
    """
    Transforms x and y coords lists into list of lines (defined by START and END point)
    """
    points = np.vstack([x, y]).T.reshape(-1, 1, 2)
    points = np.concatenate([points[:-1], points[1:]], axis=1)
    return points
