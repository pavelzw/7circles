from abc import ABC
from math import pi

from manim import *

from hexagon import Hexagon
from hyperbolic_hexagon import HexagonAngles, radian_to_point


class EuclideanHexagon(Hexagon, Group, ABC):
    def __init__(self, phis: HexagonAngles, **kwargs):
        super().__init__(phis, **kwargs)

        self._phis = phis
        edges = self.edges
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            line = LineBetweenPointsOnUnitDisk(phi1, phi2).reverse_direction()
            edges.append(line)
        self.add(edges[0], edges[1], edges[2], edges[3], edges[4], edges[5])

    @property
    def phis(self) -> HexagonAngles:
        return self._phis


class LineBetweenPointsOnUnitDisk(Line, ABC):
    def __init__(self, phi1, phi2, color=WHITE, **kwargs):
        assert phi1 >= 0
        assert phi1 < 2 * pi
        assert phi2 >= 0
        assert phi2 < 2 * pi

        if phi1 >= phi2:
            tmp = phi2
            phi2 = phi1
            phi1 = tmp
        assert phi1 < phi2

        point1 = radian_to_point(phi1)
        point2 = radian_to_point(phi2)

        if phi2 - phi1 < pi:
            super().__init__(start=point2, end=point1, color=color)
        else:
            super().__init__(start=point1, end=point2, color=color)
