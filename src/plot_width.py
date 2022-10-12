import numpy as np
from shapely.geometry import LineString, Polygon, MultiPolygon


def plot_line_width_equidistant(ax, x, y, width_from_m, width_to_m):

    width_from_m = width_from_m / 10000
    width_to_m = width_to_m / 10000
    line = LineString(zip(x, y))

    distances = np.linspace(width_from_m, width_to_m, len(x))
    min_distance = min(width_from_m, width_to_m)
    max_distance = max(width_from_m, width_to_m)
    if min_distance == max_distance:
        pol = line.buffer(min_distance)
        plot_polygons(ax, pol)
    else:
        x_eq, y_eq, x_eq2, y_eq2 = eq(x, y, distances)

        plot_polygon_between_lines(ax, x_eq, y_eq, x_eq2, y_eq2, min_distance)


def plot_polygons(ax, pol):
    if type(pol) is MultiPolygon:
        for p in pol.geoms:
            ax.fill(*p.exterior.xy, 'red')
    else:
        ax.fill(*pol.exterior.xy, 'red')


def plot_polygon_between_lines(ax, x1, y1, x2, y2, min_distance):
    if len(x1) < 2:
        return
    l1 = LineString(zip(x1, y1))
    l2 = LineString(zip(x2, y2))

    pol = Polygon([*list(l1.coords), *list(l2.coords)[::-1]])
    pol = pol.buffer(min_distance)
    plot_polygons(ax, pol)


def eq(x, y, distances):
    line = LineString(zip(x, y))
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

    for i in range(1, len(x_eq) - 1):
        seg = LineString(zip(x_eq[i-1:i+1], y_eq[i-1:i+1]))
        if line.intersection(seg):
            x_eq[i], x_eq2[i] = x_eq2[i], x_eq[i]
            y_eq[i], y_eq2[i] = y_eq2[i], y_eq[i]

    return x_eq, y_eq, x_eq2, y_eq2
