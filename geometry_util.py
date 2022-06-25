import math
from typing import Callable

import numpy as np
from manim import Circle, Dot, WHITE, GREEN, Arc, Line


def get_both_intersection_of_two_tangent_circles(c0: np.array, r0: float, c1: np.array, r1: float):
    # circle 1: center c0, radius r0
    # circle 2: center c1, radius r1
    eps = 0.00001

    x0, y0, _ = c0
    x1, y1, _ = c1

    d = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d - eps > r0 + r1:
        raise ValueError(f'Circles non intersecting\n{c0}\n{r0}\n{c1}\n{r1}')
    # One circle within other
    # if d < abs(r0 - r1):
    #    raise ValueError('One circle within other\n{c0}\n{r0}\n{c1}\n{r1}')
    # coincident circles
    if d == 0 and r0 == r1:
        raise ValueError('Coincident circles\n{c0}\n{r0}\n{c1}\n{r1}')
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = 0
        tmp = r0 ** 2 - a ** 2
        if tmp >= 0:
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
        return intersection1, intersection2


def get_intersection_not_on_circle_of_two_tangent_circles(c0: np.array, r0: float, c1: np.array, r1: float):
    intersection1, intersection2 = get_both_intersection_of_two_tangent_circles(c0, r0, c1, r1)
    if np.abs(np.linalg.norm(intersection1) - 1) < 0.0001:
        return intersection2
    return intersection1


def get_intersection_in_unit_circle_of_two_tangent_circles(c0: np.array, r0: float, c1: np.array, r1: float):
    intersection1, intersection2 = get_both_intersection_of_two_tangent_circles(c0, r0, c1, r1)
    if np.linalg.norm(intersection1) < 1 - .01:
        return intersection1
    return intersection2


def get_intersection_points_of_n_tangent_circles(circles: [Circle]):
    points = []
    n = len(circles)
    for i in range(n):
        point = get_intersection_not_on_circle_of_two_tangent_circles(
            circles[i].get_center(), circles[i].radius, circles[(i + 1) % n].get_center(), circles[(i + 1) % n].radius
        )
        points.append(point)
    return points


def get_intersections_of_n_tangent_circles(circles: [Circle], color=GREEN, radius=.05, **kwargs):
    return list(map(lambda p: Dot(p, color=color, radius=radius, **kwargs),
                    get_intersection_points_of_n_tangent_circles(circles)))


def get_intersections_of_circles_with_unit_circle(circles: [Circle], color=WHITE):
    intersections = []
    n = len(circles)
    for i in range(n):
        point = get_intersection_not_on_circle_of_two_tangent_circles(circles[i].get_center(), circles[i].radius,
                                                                      [0., 0., 0.], 1.)
        intersections.append(Dot(point, color=color, radius=0.05))
    return intersections


def polar_to_point(angle, radius=1):
    return np.array((radius * np.cos(angle), radius * np.sin(angle), 0))


def point_to_polar(point):
    angle = np.arctan2(point[1], point[0])
    if angle < 0:
        angle += 2 * math.pi
    return angle, np.linalg.norm(point)


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


def get_intersection_from_angles(phi1, phi2, phi3, phi4):
    return get_intersection(polar_to_point(phi1), polar_to_point(phi2), polar_to_point(phi3), polar_to_point(phi4))


def get_intersection_line_unit_circle(start_point, direction):
    # solves (x + at)^2 + (y + bt)^2 = 1
    # with x^2 + y^2 = 1
    x, y, _ = start_point
    a, b, _ = direction

    t = - 2 * (a * x + b * y) / (a ** 2 + b ** 2)
    return start_point + t * direction


def get_both_intersections_line_with_unit_circle(point1, point2):
    # by wolfram alpha https://mathworld.wolfram.com/Circle-LineIntersection.html
    x1, y1, _ = point1
    x2, y2, _ = point2
    dx = x2 - x1
    dy = y2 - y1
    dr = np.sqrt((dx ** 2) + (dy ** 2))
    D = x1 * y2 - x2 * y1
    if dy >= 0:  # if condition because of signum function
        new_x1 = (D * dy + dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
        new_x2 = (D * dy - dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    else:
        new_x1 = (D * dy - dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
        new_x2 = (D * dy + dx * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)

    new_y1 = (-D * dx + np.abs(dy) * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    new_y2 = (-D * dx - np.abs(dy) * np.sqrt((dr ** 2) - (D ** 2))) / (dr ** 2)
    return np.array([new_x1, new_y1, 0]), np.array([new_x2, new_y2, 0])


def get_parallel_to_line_through_point(line_points, point):
    [a, b] = line_points
    m = (a[1] - b[1]) / (a[0] - b[0])
    b = point[1] - (point[0] * m)
    return lambda x: m * x + b


def tf_klein_to_hem(point):
    x = point[0]
    y = point[1]
    assert x ** 2 + y ** 2 <= 1
    return np.array([x, y, np.sqrt(1 - (x ** 2) - (y ** 2))])


def tf_hem_to_poincare(point):
    x = point[0]
    y = point[1]
    z = point[2]
    return np.array([x / (1 + z), y / (1 + z), 0.])


def tf_klein_to_poincare(point):
    return tf_hem_to_poincare(tf_klein_to_hem(point))


# all other transformation directions
def tf_hem_to_klein(point):  # 3 coord to 2 coord
    x = point[0]
    y = point[1]
    return np.array([x, y, 0])


def tf_poincare_to_hem(point):  # 2 coord to 3 coord
    x = point[0]
    y = point[1]
    new_coord = np.array([2 * x, 2 * y, 1 - (x ** 2) - (y ** 2)])
    scalar = 1 / (1 + (x ** 2) + (y ** 2))
    return scalar * new_coord


def tf_poincare_to_klein(point):  # 2 coord to 2 coord
    return tf_poincare_to_hem(tf_hem_to_klein(point))


def tf_poincare_disk_to_poincare_half_plane(point):
    # https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model#Relation_to_the_Poincar%C3%A9_half-plane_model
    assert point[0] <= 1 + .01
    assert point[1] <= 1 + .01
    x, y = point[0], point[1]
    return np.array([2 * x / (x ** 2 + (1 - y) ** 2), (1 - x ** 2 - y ** 2) / (x ** 2 + (1 - y) ** 2)])


def tf_poincare_half_plane_to_poincare_disk(point):
    # https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model#Relation_to_the_Poincar%C3%A9_half-plane_model
    assert point[1] >= 0 - .01
    x, y = point[0], point[1]
    return np.array([2 * x / (x ** 2 + (1 + y) ** 2), (x ** 2 + y ** 2 - 1) / (x ** 2 + (1 + y) ** 2), 0])


def mobius_transform_from_matrix(p, a, b, c, d):
    # ad - bc = 1
    assert abs(a * d - b * c - 1) <= 0.01
    # z |-> (a * z + b) / (c * z + d)
    z = complex(p[0], p[1])
    result = (a * z + b) / (c * z + d)
    return np.array([result.real, result.imag])


def mobius_transform_half_plane(p, q) -> Callable:
    """
    Returns the mobius transformation that maps `p` to `q`.

    :param p: array_like
        in the Poincaré half plane
    :param q: array_like
        in the Poincaré half plane
    :return: function that takes an array_like and applies the mobius transform to it
    """
    x, y = p[0], p[1]
    u, v = q[0], q[1]
    # T_b maps i to p = x + i*y
    # T_c maps i to q = u + i*v
    # => T_a = T_c \circ T_b^-1 maps p to q
    b = np.array([[1, x], [0, 1]]) @ np.array([[np.sqrt(y), 0], [0, 1 / np.sqrt(y)]])
    c = np.array([[1, u], [0, 1]]) @ np.array([[np.sqrt(v), 0], [0, 1 / np.sqrt(v)]])
    a = c @ np.linalg.inv(b)
    return lambda z: mobius_transform_from_matrix(z, a[0, 0], a[0, 1], a[1, 0], a[1, 1])


def mobius_transform_poincare_disk(p, q) -> Callable:
    """
    Returns the mobius transformation that maps `p` to `q`.

    :param p: array_like
        in the Poincaré unit disk
    :param q: array_like
        in the Poincaré unit disk
    :return: function that takes an array_like and applies the mobius transform to it
    """
    p_half_plane = tf_poincare_disk_to_poincare_half_plane(p)
    q_half_plane = tf_poincare_disk_to_poincare_half_plane(q)
    transform_half_plane = mobius_transform_half_plane(p_half_plane, q_half_plane)
    # transform from unit disk to half plane, do mobius transform there and then transform back
    return lambda x: tf_poincare_half_plane_to_poincare_disk(
        transform_half_plane(
            tf_poincare_disk_to_poincare_half_plane(x)
        )
    )


def mobius_transform(point, x, y, u):
    res = complex_mobius_transform(complex(point[0], point[1]), x, y, u)
    # print(res)
    return np.array([np.real(res), np.imag(res), point[2]])


def complex_mobius_transform(z, x, y, u):
    a = complex(x, y)
    b = complex(u, np.sqrt(-pow(u, 2) + pow(x, 2) + pow(y, 2) - 1))
    # if absolute(z) == 1:
    #    return complex(0, 0)
    return np.divide(np.add(np.multiply(a, z), np.conj(b)), np.add(np.multiply(b, z), np.conj(a)))


def hyperbolic_distance_function(b, c):  # b and c points on plane
    klein_point1 = tf_poincare_to_klein(b)  # transform points from poincare to klein model
    klein_point2 = tf_poincare_to_klein(c)
    intersection1, intersection2 = get_both_intersections_line_with_unit_circle(klein_point1, klein_point2)

    d = (intersection1[0], intersection1[1])  # a = a1 + i* a2
    a = (intersection2[0], intersection2[1])

    ac = abs_complex(a, c)
    bd = abs_complex(b, d)
    ab = abs_complex(a, b)
    cd = abs_complex(c, d)

    # BUG: are they always ordered a,b,c,d now?
    if ac > ab and bd > cd:  # wikipedia assertion
        log_argument = ac * bd / (ab * cd)
    else:  # switch a and d
        log_argument = cd * ab / (bd * ac)

    distance = math.log(log_argument)
    return distance


def abs_complex(x, y, z=0):
    # calculates |x-y|
    x1, x2 = x[0], x[1]
    y1, y2 = y[0], y[1]
    root_term1 = (x1 - y1) ** 2
    root_term2 = (x2 - y2) ** 2
    return math.sqrt(root_term1 + root_term2)


def create_min_circle_radius(last_point, point, next_point):
    distance_last_present = abs_complex(last_point, point)
    distance_present_next = abs_complex(point, next_point)
    distance_present_unit = 1 - np.linalg.norm(point)
    circle_radius = min(distance_present_next / 2.2, distance_last_present / 2.2, distance_present_unit / 1.5)
    return circle_radius


# for horodisks
def moving_circle(start_angle, end_angle, center):
    arc1 = Arc(start_angle=start_angle, angle=end_angle, radius=0.5).move_arc_center_to(
        center)  # creates eighth of circle
    arc2 = Arc(start_angle=start_angle, angle=end_angle, radius=0.125).move_arc_center_to(center)
    arc3 = Arc(start_angle=start_angle, angle=end_angle, radius=0.25).move_arc_center_to(center)
    arc4 = Arc(start_angle=start_angle, angle=end_angle, radius=0.375).move_arc_center_to(center)
    return [arc1, arc2, arc3, arc4]


# for horodisks
def moving_line(start_points, end_points):
    line1 = Line(start=start_points[0], end=end_points[0])
    line2 = Line(start=start_points[1], end=end_points[1])
    line3 = Line(start=start_points[2], end=end_points[2])
    line4 = Line(start=start_points[3], end=end_points[3])
    return [line1, line2, line3, line4]


def hyperbolic_circle_to_euclidean_circle(center, radius):
    eps = 0.001
    x2min = 1
    x2max = 1 / np.linalg.norm(center)
    x1min = 0
    x1max = 1

    x1 = (x1max + x1min) / 2
    curr_dist = hyperbolic_distance_function(x1 * center, center)
    # print(f"center = {center}, radius = {radius}")
    # i=0
    while np.abs(curr_dist - radius) >= eps:
        # print(f"x1 = {x1}, curr_dist = {curr_dist}, x1min = {x1min}, x1max = {x1max}")
        if curr_dist < radius:
            x1max = x1
        else:
            x1min = x1
        x1 = (x1max + x1min) / 2

        curr_dist = hyperbolic_distance_function(x1 * center, center)
        # i += 1
        # if i > 10: exit(0)

    x2 = (x2max + x2min) / 2
    curr_dist = hyperbolic_distance_function(x2 * center, center)
    while np.abs(curr_dist - radius) >= eps:
        if curr_dist < radius:
            x2min = x2
        else:
            x2max = x2
        x2 = (x2max + x2min) / 2

        curr_dist = hyperbolic_distance_function(x2 * center, center)

    return (x1 * center + x2 * center) / 2, np.linalg.norm(x1 * center - x2 * center) / 2
