from abc import ABC

import numpy as np
from manim import Group
from math import pi

from util import get_arc, radian_to_point, get_intersection, get_intersection_line_unit_circle


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
        arcs = []
        for i in range(phis.shape[0]):
            phi_1 = phis[i]
            phi_2 = phis[(i + 1) % 6]
            point = radian_to_point(phi_2)
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            arc = get_arc(phi_1, phi_2).reverse_direction()
            arcs.append(arc)
        self.add(arcs[0], arcs[1], arcs[2], arcs[3], arcs[4], arcs[5])
