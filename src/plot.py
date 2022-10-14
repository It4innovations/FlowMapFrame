import numpy as np

from src.plot_width import plot_line_width_equidistant


def plot_route_width(ax, x, y,
                     density_from, density_to,
                     min_width_density, max_width_density,
                     width_modifier=2,
                     equidistant=False
                     ):
    """
    Plot line width around line with any density above MIN_WIDTH_DENSITY

    :param list x: 1D array of horizontal coordinates of the route
    :param list y: 1D array of vertical coordinates of the route
    :param int width_modifier: width of the line with max_width_density (in meters * 10)
    """

    width_from, width_to = np.interp([density_from, density_to],
                                     [min_width_density, max_width_density], [0, 10 * width_modifier])

    if max(width_from, width_to) > 0:
        if equidistant:
            plot_line_width_equidistant(ax, x, y, width_from, width_to)
        else:
            plot_segment_line_width(ax, x, y, width_from, width_to)


def plot_segment_line_width(ax, x, y, width_from_m, width_to_m):
    """
    Plot coloured line width around line either horizontally or vertically
    """
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
