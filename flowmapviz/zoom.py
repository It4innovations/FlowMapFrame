import networkx as nx
import osmnx as ox

from enum import Enum, unique
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


@unique
class ZoomLevel(Enum):
    LEVEL_ONE = 320_000
    LEVEL_TWO = 161_000
    LEVEL_THREE = 40_000
    LEVEL_FOUR = 0


def get_zoom_level(ax) -> ZoomLevel:
    lims = ax.get_xlim()
    lims = lims[1] - lims[0]
    window_size = ax.get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted()).size
    ratio = lims / window_size[0]
    ratio = ratio * 111 * 39370.0787
    for zoom_level in ZoomLevel:
        if ratio > zoom_level.value:
            return zoom_level


def get_highway_types(zoom_level: ZoomLevel):
    if zoom_level == ZoomLevel.LEVEL_ONE:
        return ['motorway', 'motorway_link',
                'primary', 'primary_link']
    if zoom_level == ZoomLevel.LEVEL_TWO:
        return ['motorway', 'motorway_link',
                'primary', 'primary_link',
                'secondary', 'secondary_link']
    if zoom_level == ZoomLevel.LEVEL_THREE:
        return ['motorway', 'motorway_link',
                'primary', 'primary_link',
                'secondary', 'secondary_link'
                'tertiary', 'tertiary_link']
    if zoom_level == ZoomLevel.LEVEL_FOUR:
        return ['motorway', 'motorway_link',
                'primary', 'primary_link',
                'secondary', 'secondary_link'
                'tertiary', 'tertiary_link'
                'unclassified', 'residential']
    return []


def plot_graph_with_zoom(g: nx.MultiDiGraph,
                         ax: Axes,
                         color_primary="dimgray",
                         color_hidden="darkgray"):
    if ax is None:
        ax = plt.gca()

    lines = ax.collections
    if not lines:
        _, ax = ox.plot_graph(g, ax=ax, node_size=0, show=False)

    lines = ax.collections
    if not lines:
        return ax

    zoom_level = get_zoom_level(ax)

    if not zoom_level:
        ax.collections[0].set_color(color_primary)
        return ax

    ec = []
    for u, v, k, d in g.edges(keys=True, data=True):
        if d['highway'] in get_highway_types(zoom_level):
            ec.append(color_primary)
        else:
            ec.append(color_hidden)

    ax.collections[0].set_color(ec)
    return ax
