from abc import ABC
from math import pi

import numpy as np
from manim import Group, BLUE, Circle, WHITE, ArcBetweenPoints, Angle, TangentLine, VMobject, VGroup, \
    Polygon, RED, Dot, RED_A, BLUE_A

from geometry_util import radian_to_point, get_intersection, get_intersection_line_unit_circle, \
    get_intersection_not_on_circle_of_two_tangent_circles, get_circle_middle, \
    get_intersection_in_unit_circle_of_two_tangent_circles, tf_poincare_to_klein, \
    get_both_intersections_line_with_unit_circle


class HexagonAngles(np.ndarray, ABC):
    def __new__(cls, phis, *args, **kwargs):
        if phis.shape[0] == 5:
            # one angle is missing -> calculate angle s.t. the main diagonals intersect
            obj = np.empty(shape=(6,)).view(IntersectingHexagonAngles)
            obj[:5] = phis
            new_phi = IntersectingHexagonAngles.get_last_phi(phis)
            obj[-1] = new_phi + 2 * pi if new_phi < 0 else new_phi
            return obj
        if phis.shape[0] == 6:
            obj = np.empty(shape=(6,)).view(NonIntersectingHexagonAngles)
            obj[:6] = phis
            return obj


class IntersectingHexagonAngles(HexagonAngles):
    def variable_angles(self) -> np.ndarray:
        return np.array(self[:5])

    @staticmethod
    def get_last_phi(phis: np.ndarray):
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


class NonIntersectingHexagonAngles(HexagonAngles):
    ...


class Hexagon(VMobject, Group, ABC):
    def __init__(self, phis: HexagonAngles, **kwargs):
        super().__init__(**kwargs)
        self.edges = []


class HexagonCircles(VMobject, Group, ABC):
    def __init__(self, hexagon: Hexagon, first_circle_radius: float, color=BLUE, **kwargs):
        super().__init__(**kwargs)
        phis = hexagon.phis
        p0 = radian_to_point(phis[0])
        first_circle_center = p0 * (1 - first_circle_radius)
        first_circle = Circle(radius=first_circle_radius, color=color).move_to(first_circle_center)
        self.add(first_circle)
        self.circles = [first_circle]

        new_center, new_radius = first_circle_center, first_circle_radius
        for i in range(1, 6):
            new_center, new_radius = self._get_next_circle(new_center, new_radius, phis[i - 1], phis[i])
            new_circle = Circle(radius=new_radius, color=color).move_to(new_center)
            self.circles.append(new_circle)
            self.add(new_circle)

    @staticmethod
    def _get_next_circle(center, radius, phi_old, phi_new):
        arc = ArcBetweenPointsOnUnitDisk(phi_old, phi_new)
        arc_center = get_circle_middle(phi_old, phi_new)
        intersection = get_intersection_not_on_circle_of_two_tangent_circles(center, radius, arc_center, arc.radius)
        assert intersection is not None
        middle_between_phi_new_and_intersection = (intersection + radian_to_point(phi_new)) / 2
        direction = intersection - radian_to_point(phi_new)
        orthogonal_direction = np.array([-direction[1], direction[0], 0])
        center_of_circle = get_intersection(radian_to_point(phi_new), np.array([0, 0, 0]),
                                            middle_between_phi_new_and_intersection,
                                            orthogonal_direction + middle_between_phi_new_and_intersection)
        return center_of_circle, np.linalg.norm(center_of_circle - radian_to_point(phi_new))


class HexagonMainDiagonals(VGroup, ABC):
    def __init__(self, hexagon: Hexagon, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        phis = hexagon.phis
        self.arc1 = ArcBetweenPointsOnUnitDisk(phis[0], phis[3], color=color, **kwargs)
        self.arc2 = ArcBetweenPointsOnUnitDisk(phis[1], phis[4], color=color, **kwargs)
        self.arc3 = ArcBetweenPointsOnUnitDisk(phis[2], phis[5], color=color, **kwargs)
        self.add(self.arc1, self.arc2, self.arc3)


class IntersectionTriangle(Polygon, ABC):
    # technically not an actual polygon but since the triangle is small, it is approximately the same
    def __init__(self, diagonals: HexagonMainDiagonals, **kwargs):
        c1, r1 = diagonals.arc1.circle_center, diagonals.arc1.radius
        c2, r2 = diagonals.arc2.circle_center, diagonals.arc2.radius
        c3, r3 = diagonals.arc3.circle_center, diagonals.arc3.radius
        intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(c2, r2, c3, r3)
        intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c3, r3)
        intersection3 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c2, r2)
        # todo make hyperbolic triangle, not euclidean triangle
        super(IntersectionTriangle, self).__init__(intersection1, intersection2, intersection3, **kwargs)


class HyperbolicTriangle(VGroup, ABC):
    def __init__(self, p1: np.ndarray, p2: np.ndarray, p3: np.ndarray, **kwargs):
        super(HyperbolicTriangle, self).__init__(**kwargs)
        arc1 = HyperbolicArcBetweenPoints(p1, p2, **kwargs)
        arc2 = HyperbolicArcBetweenPoints(p2, p3, **kwargs)
        arc3 = HyperbolicArcBetweenPoints(p3, p1, **kwargs)
        self.add(arc1, arc2, arc3)


class HyperbolicArcBetweenPoints(ArcBetweenPoints, ABC):
    def __init__(self, p1: np.ndarray, p2: np.ndarray, arcs_meeting_circle=False, **kwargs):
        klein_point1 = tf_poincare_to_klein(p1)  # transform points from poincare to klein model
        klein_point2 = tf_poincare_to_klein(p2)

        intersection1, intersection2 = get_both_intersections_line_with_unit_circle(klein_point1, klein_point2)

        if np.linalg.norm(intersection1 - p2) < np.linalg.norm(intersection1 - p1):
            tmp = intersection1
            intersection1 = intersection2
            intersection2 = tmp

        # get polar coordinates of intersections
        phi1 = np.arctan2(intersection1[1], intersection1[0])
        phi2 = np.arctan2(intersection2[1], intersection2[0])

        if phi1 < 0:  # for assertion phi >= 0
            phi1 += 2 * pi
        if phi2 < 0:
            phi2 += 2 * pi

        radius = ArcBetweenPointsOnUnitDisk(phi1, phi2).radius

        diff = phi2 - phi1
        if diff < 0:
            diff += 2 * pi
        if diff < pi:
            if arcs_meeting_circle:
                super(HyperbolicArcBetweenPoints, self).__init__(radian_to_point(phi2),
                                                                 radian_to_point(phi1),
                                                                 radius=radius, **kwargs)
            else:
                super(HyperbolicArcBetweenPoints, self).__init__(p2, p1, radius=radius, **kwargs)
            self.reverse_direction()
        else:
            if arcs_meeting_circle:
                super(HyperbolicArcBetweenPoints, self).__init__(radian_to_point(phi1),
                                                                 radian_to_point(phi2),
                                                                 radius=radius, **kwargs)
            else:
                super(HyperbolicArcBetweenPoints, self).__init__(p1, p2, radius=radius, **kwargs)


class ArcBetweenPointsOnUnitDisk(ArcBetweenPoints, ABC):
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

        self.circle_center = get_circle_middle(phi1, phi2)
        radius = np.linalg.norm(self.circle_center - point1)

        # gets angle between two tangents
        angle = Angle(TangentLine(Circle(), alpha=phi1 / (2 * pi)),
                      TangentLine(Circle(), alpha=phi2 / (2 * pi)))

        ang = angle.get_value(degrees=False)
        if phi2 - phi1 < pi:
            super().__init__(start=point2, end=point1, angle=-ang, radius=radius, color=color, **kwargs)
        else:
            super().__init__(start=point1, end=point2, angle=-ang, radius=radius, color=color, **kwargs)
