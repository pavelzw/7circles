from abc import ABC
from math import pi

from manim import VGroup, Line

from hexagon import HexagonAngles
from hyperbolic_polygon import polar_to_point


class EuclideanHexagon(VGroup, ABC):
    def __init__(self, phis: HexagonAngles, **kwargs):
        super().__init__(**kwargs)

        self._phis = phis
        self.edges = []
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            line = LineBetweenPointsOnUnitDisk(phi1, phi2, **kwargs).reverse_direction()
            self.edges.append(line)
        self.add(*self.edges)

    @property
    def phis(self) -> HexagonAngles:
        return self._phis


class LineBetweenPointsOnUnitDisk(Line, ABC):
    def __init__(self, phi1, phi2, **kwargs):
        assert phi1 >= 0
        assert phi1 < 2 * pi
        assert phi2 >= 0
        assert phi2 < 2 * pi

        if phi1 >= phi2:
            tmp = phi2
            phi2 = phi1
            phi1 = tmp
        assert phi1 < phi2

        point1 = polar_to_point(phi1)
        point2 = polar_to_point(phi2)

        if phi2 - phi1 < pi:
            super().__init__(start=point2, end=point1, **kwargs)
        else:
            super().__init__(start=point1, end=point2, **kwargs)


def get_diagonals(hexagon: EuclideanHexagon, **kwargs):
    diagonals = []
    phis = hexagon.phis
    for i in range(3):
        diagonals.append(LineBetweenPointsOnUnitDisk(phis[i], phis[i + 3], **kwargs))

    return diagonals
