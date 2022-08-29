import numpy as np


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
