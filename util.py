import numpy as np
from manim import PI
from manim import Angle, TangentLine, ArcBetweenPoints, Circle, Group


def get_arc(phi_1, phi_2):
    assert phi_1 >= 0
    assert phi_1 < 2 * PI
    assert phi_2 >= 0
    assert phi_2 < 2 * PI

    if phi_1 >= phi_2:
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    assert phi_1 < phi_2

    point_1 = radian_to_point(phi_1)
    point_2 = radian_to_point(phi_2)

    middle = get_circle_middle(phi_1, phi_2)
    r = np.linalg.norm(middle - point_1)

    # gets angle between two tangents
    angle = Angle(TangentLine(Circle(), alpha=phi_1 / (2 * PI)),
                  TangentLine(Circle(), alpha=phi_2 / (2 * PI)))

    ang = angle.get_value(degrees=False)
    if phi_2 - phi_1 < PI:
        arc = ArcBetweenPoints(start=point_2, end=point_1, angle=-ang, radius=r)
    else:
        arc = ArcBetweenPoints(start=point_1, end=point_2, angle=-ang, radius=r)
    return arc


def create_arcs(phis):
    # create hyperbolic hexagon
    arcs = []
    for i in range(phis.shape[0]):
        phi_1 = phis[i]
        phi_2 = phis[(i + 1) % 6]
        point = radian_to_point(phi_2)
        # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
        arc = get_arc(phi_1, phi_2).reverse_direction()
        arcs.append(arc)
    arcs = Group(arcs[0], arcs[1], arcs[2], arcs[3], arcs[4], arcs[5])
    return arcs


def get_intersections_of_circles(c0, r0, c1, r1):
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


def create_phis(min_dist=0.4):
    phis = np.sort(np.random.uniform(0, 2 * PI, 6))
    while np.min(np.abs(np.roll(phis, shift=1) - phis)) < min_dist or phis[0] < phis[5] - 2 * PI + min_dist:
        phis = np.sort(np.random.uniform(0, 2 * PI, 6))

    new_phi = get_last_phi(phis[:-1])
    phis[-1] = new_phi + 2 * PI if new_phi < 0 else new_phi

    return phis


def get_circle_middle(phi_1, phi_2):
    if np.sin(phi_2) == 0:  # phi_2 != 0, PI because else we divide by 0
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    x = (-np.sin(phi_1) + np.sin(phi_2)) / (-np.cos(phi_2) * np.sin(phi_1) + np.cos(phi_1) * np.sin(phi_2))
    y = (1 - x * np.cos(phi_2)) / np.sin(phi_2)
    return np.array((x, y, 0))


def get_next_circle(center, radius, phi_old, phi_new):
    arc = get_arc(phi_old, phi_new)
    arc_center = get_circle_middle(phi_old, phi_new)
    intersection = get_intersections_of_circles(center, radius, arc_center, arc.radius)
    assert intersection is not None
    middle_between_phi_new_and_intersection = (intersection + radian_to_point(phi_new)) / 2
    direction = intersection - radian_to_point(phi_new)
    orthogonal_direction = np.array([-direction[1], direction[0], 0])
    center_of_circle = get_intersection(radian_to_point(phi_new), np.array([0, 0, 0]),
                                        middle_between_phi_new_and_intersection,
                                        orthogonal_direction + middle_between_phi_new_and_intersection)
    return center_of_circle, np.linalg.norm(center_of_circle - radian_to_point(phi_new))


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


def create_phi_transition(phi_old, phi_new, step_size=10):
    assert phi_old.shape == phi_new.shape
    transition = np.empty(shape=(step_size, phi_old.shape[0]))
    for t in range(step_size):
        transition[t] = phi_old * (1 - t / step_size) + phi_new * t / step_size
    return transition


def get_intersection_line_unit_circle(start_point, direction):
    # solves (x + at)^2 + (y + bt)^2 = 1
    # with x^2 + y^2 = 1
    x, y, _ = start_point
    a, b, _ = direction

    t = - 2 * (a * x + b * y) / (a ** 2 + b ** 2)
    return start_point + t * direction


def get_last_phi(phis):
    assert phis.shape == (5,)
    p0 = radian_to_point(phis[0])
    p1 = radian_to_point(phis[1])
    p2 = radian_to_point(phis[2])
    p3 = radian_to_point(phis[3])
    p4 = radian_to_point(phis[4])
    intersection = get_intersection(p0, p3, p1, p4)
    point_on_circle = get_intersection_line_unit_circle(p2, intersection - p2)
    phi = np.arctan2(point_on_circle[1], point_on_circle[0])
    return phi
