import numpy as np
import matplotlib.patches as mp_patches
from matplotlib.axes import Axes
from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from shapely.geometry import LineString


def get_width_polygon(ax: Axes,
                      x: list[float],
                      y: list[float],
                      density_from: int, density_to: int,
                      min_width_density: int, max_width_density: int,
                      width_modifier: float = 2,
                      equidistant: bool = False,
                      round_edges: bool = True,
                      ):
    width_from, width_to = np.interp([density_from, density_to],
                                     [min_width_density, max_width_density], [0, width_modifier])

    polygons = []
    width_from, width_to = width_from / 1000, width_to / 1000

    if max(width_from, width_to) > 0:

        if round_edges:
            polygons.extend(create_circle_endings(ax, x, y, width_from, width_to))

        if equidistant:
            patch = get_polygon_from_equidistant(ax, x, y, width_from, width_to)
            polygons.append(patch)
        else:
            patch = plot_segment_line_width(ax, x, y, width_from, width_to)

    return polygons


def plot_polygon_patch(ax, patches, color='red'):
    p = PatchCollection(patches)
    p.set_facecolor(color)
    ax.add_collection(p, autolim=False)
    return p


def create_circle_endings(ax, x, y, width_from, width_to, plot=False):
    patches = [Circle((x[0], y[0]), width_from), Circle((x[-1], y[-1]), width_to)]
    if plot:
        plot_polygon_patch(ax, patches)
    return patches


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


def get_polygon_from_equidistant(ax, x, y, width_from, width_to):
    distances = np.linspace(width_from, width_to, len(x))
    x_eq, y_eq, x_eq2, y_eq2 = calculate_equidistant_coords(x, y, distances)

    if len(x_eq) < 2:
        return None

    x = np.append(x_eq, np.flip(x_eq2))
    y = np.append(y_eq, np.flip(y_eq2))
    coords = list(zip(x, y))

    return mp_patches.Polygon(coords, closed=True)


def calculate_equidistant_coords(x, y, distances):
    # Mid points
    x_m = []
    y_m = []
    d_m = []
    k_m = []

    # Calculate middle points:
    for i in range(len(x) - 1):
        y_m.append((y[i + 1] - y[i]) / 2.0 + y[i])
        x_m.append((x[i + 1] - x[i]) / 2.0 + x[i])
        d_m.append((distances[i + 1] - distances[i]) / 2.0 + distances[i])

        if y[i + 1] == y[i]:
            k_m.append(1e8)
        else:
            k_m.append(-(x[i + 1] - x[i]) / (y[i + 1] - y[i]))

    # Add first elements
    x_m.insert(0, x[0])
    y_m.insert(0, y[0])
    d_m.insert(0, distances[0])
    k_m.insert(0, k_m[0])

    # Add last elements
    x_m.append(x[-1])
    y_m.append(y[-1])
    d_m.append(distances[-1])
    k_m.append(k_m[-1])

    # Convert into np.arrays
    x_m = np.array(x_m)
    y_m = np.array(y_m)
    k_m = np.array(k_m)
    d_m = np.array(d_m)

    # Calculate equidistant points
    x_eq = d_m * np.sqrt(1.0 / (1 + k_m ** 2))
    x_eq2 = np.zeros_like(x_eq)
    y_eq = np.zeros_like(x_eq)
    y_eq2 = np.zeros_like(x_eq)

    for i, x_shift in enumerate(x_eq):
        x_eq[i] = x_m[i] - abs(x_shift)
        x_eq2[i] = x_m[i] + abs(x_shift)

        y_eq[i] = (y_m[i] - k_m[i] * x_m[i]) + k_m[i] * x_eq[i]
        y_eq2[i] = (y_m[i] - k_m[i] * x_m[i]) + k_m[i] * x_eq2[i]

    # Switch lines that intersect the original line
    original_line = LineString(zip(x, y))

    for i in range(1, len(x_eq)):
        seg = LineString(zip(x_eq[i - 1:i + 1], y_eq[i - 1:i + 1]))

        if original_line.intersection(seg):
            x_eq[i], x_eq2[i] = x_eq2[i], x_eq[i]
            y_eq[i], y_eq2[i] = y_eq2[i], y_eq[i]

    return x_eq, y_eq, x_eq2, y_eq2
