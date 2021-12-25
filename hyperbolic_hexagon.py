from abc import ABC

import numpy as np
from manim import Group, Circle, BLUE, WHITE
from math import pi

from util import get_arc, radian_to_point, get_intersection, get_intersection_line_unit_circle, \
    get_intersections_of_circles, get_circle_middle


class HexagonAngles(np.ndarray):
    def __new__(cls, phis, *args, **kwargs):
        assert phis.shape[0] == 5
        obj = np.empty(shape=(6,)).view(cls)
        obj[:5] = phis
        new_phi = cls._get_last_phi(phis)
        obj[-1] = new_phi + 2 * pi if new_phi < 0 else new_phi
        return obj

    def variable_angles(self) -> np.ndarray:
        return np.array(self[:5])

    @staticmethod
    def _get_last_phi(phis: np.ndarray):
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


class HyperbolicHexagon(Group, ABC):
    def __init__(self, phis: HexagonAngles, **kwargs):
        super().__init__(**kwargs)
        self._phis = phis
        arcs = []
        for i in range(phis.shape[0]):
            phi_1 = phis[i]
            phi_2 = phis[(i + 1) % 6]
            point = radian_to_point(phi_2)
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            arc = get_arc(phi_1, phi_2).reverse_direction()
            arcs.append(arc)
        self.add(arcs[0], arcs[1], arcs[2], arcs[3], arcs[4], arcs[5])

    @property
    def phis(self) -> HexagonAngles:
        return self._phis


class HyperbolicHexagonCircles(Group, ABC):
    def __init__(self, hexagon: HyperbolicHexagon, first_circle_radius: float, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        phis = hexagon.phis
        p0 = radian_to_point(phis[0])
        first_circle_center = p0 * (1 - first_circle_radius)
        self.add(Circle(radius=first_circle_radius, color=color).move_to(first_circle_center))

        new_center, new_radius = first_circle_center, first_circle_radius
        for i in range(1, 6):
            new_center, new_radius = self._get_next_circle(new_center, new_radius, phis[i - 1], phis[i])
            self.add(Circle(radius=new_radius, color=color).move_to(new_center))

    @staticmethod
    def _get_next_circle(center, radius, phi_old, phi_new):
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


class HyperbolicHexagonMainDiagonals(Group, ABC):
    def __init__(self, hexagon: HyperbolicHexagon, color=WHITE, **kwargs):
        super().__init__()
        phis = hexagon.phis
        self.add(get_arc(phis[0], phis[3]))
        self.add(get_arc(phis[1], phis[4]))
        self.add(get_arc(phis[2], phis[5]))
