from abc import ABC
from math import pi

import numpy as np
from manim import Group, BLUE, YELLOW, ArcBetweenPoints, Dot, VGroup, WHITE

from geometry_util import radian_to_point, get_both_intersections_line_with_unit_circle, tf_poincare_to_klein
from hexagon import Hexagon, HexagonAngles, ArcBetweenPointsOnUnitDisk


class HyperbolicHexagon(Hexagon, Group, ABC):
    def __init__(self, phis: HexagonAngles, **kwargs):
        super().__init__(phis, **kwargs)

        self._phis = phis
        arcs = self.edges
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            arc = ArcBetweenPointsOnUnitDisk(phi1, phi2, **kwargs).reverse_direction()
            arcs.append(arc)
        self.add(arcs[0], arcs[1], arcs[2], arcs[3], arcs[4], arcs[5])

    @property
    def phis(self) -> HexagonAngles:
        return self._phis


class NonIdealHexagon(VGroup, ABC):
    def __init__(self, radius, phis, alternating_perimeter=False, arcs_meeting_circle=False, *mobjects, **kwargs):
        super().__init__(*mobjects, **kwargs)
        first_point = radian_to_point(phis[0], radius[0])
        point1 = first_point
        self.hexagon_arcs = []
        self.hexagon_points = []
        self.hexagon_points.append(point1)
        self.add(Dot(point1, radius=0.04))
        color1 = WHITE
        color2 = BLUE

        for i in range(0, 6):
            if i == 5:
                point1 = radian_to_point(phis[5], radius[5])
                point2 = first_point
                self.hexagon_points.append(point1)
            else:
                point2 = radian_to_point(phis[i + 1], radius[i + 1])
                self.hexagon_points.append(point2)
                self.add(Dot(point2, radius=0.04))

            # todo replace with HyperbolicArcBetweenPoints
            klein_point1 = tf_poincare_to_klein(point1)  # transform points from poincare to klein model
            klein_point2 = tf_poincare_to_klein(point2)
            intersection1, intersection2 = get_both_intersections_line_with_unit_circle(klein_point1, klein_point2)

            unit_point1 = np.arctan2(intersection1[1], intersection1[0])  # get polar coordinates of intersections
            unit_point2 = np.arctan2(intersection2[1], intersection2[0])

            if unit_point1 < 0:  # for assertion phi >= 0
                unit_point1 = unit_point1 + 2 * pi
            if unit_point2 < 0:
                unit_point2 = unit_point2 + 2 * pi
            # ArcBetweenPointsOnUnitCircle
            radius1 = ArcBetweenPointsOnUnitDisk(unit_point1, unit_point2).radius
            if arcs_meeting_circle:
                arc = ArcBetweenPointsOnUnitDisk(unit_point1, unit_point2, color=color1,
                                                 **kwargs)  # arcs in hexagon meet unit circle
            else:
                if alternating_perimeter:
                    if i % 2 == 0:
                        arc = ArcBetweenPoints(point2, point1, radius=radius1,
                                               color=color1, **kwargs)  # arcs in hexagon dont meet unit circle
                    else:
                        arc = ArcBetweenPoints(point2, point1, radius=radius1,
                                               color=color2, **kwargs)
                else:
                    arc = ArcBetweenPoints(point2, point1, radius=radius1,
                                           color=color1, **kwargs)
            self.add(arc.reverse_direction())
            self.hexagon_arcs.append(arc)
            point1 = point2
