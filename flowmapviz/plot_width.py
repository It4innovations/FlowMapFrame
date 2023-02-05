import numpy as np
import matplotlib.patches as mp
from shapely.geometry import LineString


def get_polygon_from_equidistant(ax, x, y, width_from, width_to):
    distances = np.linspace(width_from, width_to, len(x))
    x_eq, y_eq, x_eq2, y_eq2 = calculate_equidistant_coords(x, y, distances)

    return create_polygon_between_lines(ax, x_eq, y_eq, x_eq2, y_eq2)


def create_polygon_between_lines(ax, x1, y1, x2, y2):
    if len(x1) < 2:
        return None

    x = np.append(x1, np.flip(x2))
    y = np.append(y1, np.flip(y2))
    coords = list(zip(x, y))

    return mp.Polygon(coords, closed=True)


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
