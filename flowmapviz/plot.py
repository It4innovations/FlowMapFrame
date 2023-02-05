import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from .plot_width import get_polygon_from_equidistant


def plot_patch(ax, patches):
    p = PatchCollection(patches)
    p.set_facecolor("red")
    ax.add_collection(p, autolim=False)
    return p


def create_circle_endings(ax, x, y, width_from, width_to):
    patches = [Circle((x[0], y[0]), width_from), Circle((x[-1], y[-1]), width_to)]
    # plot_patch(ax, patches)
    return patches


def plot_route_width(ax, x, y,
                     density_from, density_to,
                     min_width_density, max_width_density,
                     width_modifier=2,
                     equidistant=False,
                     round_edges=True,
                     ):
    """
    Plot line width around line with any density above MIN_WIDTH_DENSITY

    :param list x: 1D array of horizontal coordinates of the route
    :param list y: 1D array of vertical coordinates of the route
    :param int width_modifier: width of the line with max_width_density (in lat degrees / 1 000)
    """

    width_from, width_to = np.interp([density_from, density_to],
                                     [min_width_density, max_width_density], [0, width_modifier])

    polygons = []
    width_from, width_to = width_from / 1000, width_to / 1000

    if max(width_from, width_to) > 0:

        if round_edges:
            polygons.extend(add_circle_endings(ax, x, y, width_from, width_to))

        if equidistant:
            patch = get_polygon_from_equidistant(ax, x, y, width_from, width_to)
            polygons.append(patch)
        else:
            patch = plot_segment_line_width(ax, x, y, width_from, width_to)

    return polygons


def plot_segment_line_width(ax, x, y, width_from, width_to):
    """
    Plot coloured line width around line either horizontally or vertically
    """
    if abs(x[0] - x[-1]) > abs(y[0] - y[-1]):
        d = np.linspace(width_from, width_to, len(y))
        y1 = np.add(y, d)
        y2 = np.subtract(y, d)

        patch = ax.fill_between(x, y1, y2, alpha=1, linewidth=0, color='red')
    else:
        d = np.linspace(width_from, width_to, len(x))
        x1 = np.add(x, d)
        x2 = np.subtract(x, d)

        patch = ax.fill_betweenx(y=y, x1=x1, x2=x2, alpha=1, linewidth=0, color='red')

    return patch
