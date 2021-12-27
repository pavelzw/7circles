import numpy as np


def get_intersections_of_circles(c0: np.array, r0: float, c1: np.array, r1: float):
    # circle 1: center c0, radius r0
    # circle 2: center c1, radius r1

    x0, y0, _ = c0
    x1, y1, _ = c1

    d = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        raise ValueError(f'Circles non intersecting\n{c0}\n{r0}\n{c1}\n{r1}')
    # One circle within other
    if d < abs(r0 - r1):
        raise ValueError('One circle within other\n{c0}\n{r0}\n{c1}\n{r1}')
    # coincident circles
    if d == 0 and r0 == r1:
        raise ValueError('Coincident circles\n{c0}\n{r0}\n{c1}\n{r1}')
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = np.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        # we only want the one intersection with ||.|| < 1
        intersection1 = np.array((x3, y3, 0))
        intersection2 = np.array((x4, y4, 0))
        if np.abs(np.linalg.norm(intersection1) - 1) < 0.0001:
            return intersection2
        return intersection1


def radian_to_point(angle):
    return np.array((np.cos(angle), np.sin(angle), 0))


def radian_to_point_with_radius(radius, angle):
    return np.array((radius * np.cos(angle), radius * np.sin(angle), 0))


def get_circle_middle(phi_1, phi_2):
    if np.sin(phi_2) == 0:  # phi_2 != 0, PI because else we divide by 0
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    x = (-np.sin(phi_1) + np.sin(phi_2)) / (-np.cos(phi_2) * np.sin(phi_1) + np.cos(phi_1) * np.sin(phi_2))
    y = (1 - x * np.cos(phi_2)) / np.sin(phi_2)
    return np.array((x, y, 0))


def get_intersection(p1, p2, p3, p4):
    # uses this formula: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    x1, y1, _ = p1
    x2, y2, _ = p2
    x3, y3, _ = p3
    x4, y4, _ = p4
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    intersection1 = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    intersection2 = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    intersection1 /= denominator
    intersection2 /= denominator
    return np.array([intersection1, intersection2, 0])


def get_intersection_line_unit_circle(start_point, direction):
    # solves (x + at)^2 + (y + bt)^2 = 1
    # with x^2 + y^2 = 1
    x, y, _ = start_point
    a, b, _ = direction

    t = - 2 * (a * x + b * y) / (a ** 2 + b ** 2)
    return start_point + t * direction


def get_both_intersections_line_with_unit_circle_wolfram_alpha(point1, point2):
    # by wolfram alpha https://mathworld.wolfram.com/Circle-LineIntersection.html
    x1, y1, _ = point1
    x2, y2, _ = point2
    dx = x2 - x1
    dy = y2 - y1
    dr = np.sqrt((dx ** 2) + (dy ** 2))
    D = x1 * y2 - x2 * y1
    if dy >= 0:
        new_x1 = (D * dy + dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
        new_x2 = (D * dy - dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    else:
        new_x1 = (D * dy - dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
        new_x2 = (D * dy + dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)

    new_y1 = (-D * dx + np.abs(dy) * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    new_y2 = (-D * dx - np.abs(dy) * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    return np.array([new_x1, new_y1, new_x2, new_y2])  # array mit 4 einträgen für 2 punkte
