from __future__ import annotations

import logging
import networkx as nx
import numpy as np

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
    uses matplotlib.fill_between / matplotlib.fill_betweenx
    """
    EQUIDISTANT = 3
    """
    uses matplotlib.PatchCollection
    """


def plot_routes(g: nx.MultiDiGraph,
                ax: Axes,
                nodes_from: list[int],
                nodes_to: list[int],
                densities: list[int] | list[list[int]],
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
    :param ax: layer for adding plotted shapes
    :param nodes_from: OSM id defining starting nodes of segments
    :param nodes_to: OSM id defining ending nodes of segments
    :param densities: list of lists defining number of cars for each part of the segment
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
    if not (len(nodes_from) == len(nodes_to) and len(nodes_to) == len(densities)):
        logging.error(f"Nodes_from, nodes_to and densities does not have the same length")

    for node_from, node_to, density in zip(nodes_from, nodes_to, densities):
        if type(density) is int:
            density = [density]

        lines_new, color_scalars_new, polygons_new = plot_route(g, node_from, node_to, density, ax,
                                                                min_width_density, max_width_density,
                                                                width_modifier=width_modifier,
                                                                width_style=width_style, round_edges=round_edges)
        if lines_new is None:
            false_segments += 1
        else:
            lines.append(lines_new)
            color_scalars.append(color_scalars_new)
            polygons.extend(polygons_new)

    if false_segments:
        logging.info(f"False segments: {false_segments} from {len(nodes_from)}")

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
               node_from: int,
               node_to: int,
               densities: list[int],
               ax: Axes,
               min_width_density: int,
               max_width_density: int,
               width_modifier: float,
               width_style: WidthStyle,
               round_edges: bool = True,
               **pg_kwargs):

    x, y = get_node_coordinates(g, node_from, node_to)
    if not x or not y:
        return None, None, None

    # edit length of densities to match length of x
    a = np.arange(len(x))
    density_index = np.interp(a, [0, len(x)], [0, len(densities)])
    point_densities = np.interp(density_index, np.arange(len(densities)), densities)

    # color gradient
    line = reshape(x, y)
    density_index = np.interp(np.arange(len(line)), [0, len(line)], [0, len(densities)])
    color_scalar = np.interp(density_index, np.arange(len(densities)), densities)

    # width as filling
    polygons = []
    if width_style == WidthStyle.CALLIGRAPHY:
        polygons = get_width_polygon(ax, x, y, point_densities, min_width_density, max_width_density,
                                     width_modifier, equidistant=False, round_edges=round_edges)

    elif width_style == WidthStyle.EQUIDISTANT:
        polygons = get_width_polygon(ax, x, y, point_densities, min_width_density, max_width_density,
                                     width_modifier, equidistant=True, round_edges=round_edges)

    return line, color_scalar, polygons


def get_node_coordinates(g, node_from, node_to):
    x = []
    y = []
    edge = g.get_edge_data(node_from, node_to)
    if edge is None:
        edge = g.get_edge_data(node_to, node_from)
        if edge is None:
            return x, y

    data = min(edge.values(), key=lambda d: d["length"])
    if "geometry" in data:
        xs, ys = data["geometry"].xy
        x.extend(xs)
        y.extend(ys)
    else:
        x.extend((g.nodes[node_from]["x"], g.nodes[node_to]["x"]))
        y.extend((g.nodes[node_from]["y"], g.nodes[node_to]["y"]))

    return x, y


def reshape(x, y):
    """
    Transforms x and y coords lists into list of lines (defined by START and END point)
    """
    points = np.vstack([x, y]).T.reshape(-1, 1, 2)
    points = np.concatenate([points[:-1], points[1:]], axis=1)
    return points
