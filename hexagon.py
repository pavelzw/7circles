from abc import ABC
from math import pi

from manim import *
from manim import Group, BLUE, Circle, WHITE, ArcBetweenPoints, Angle, TangentLine

from geometry_util import radian_to_point, get_intersection, get_intersection_line_unit_circle, \
    get_intersection_of_two_tangent_circles, get_circle_middle


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
        self.add(Circle(radius=first_circle_radius, color=color).move_to(first_circle_center))
        self.circles = []

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
        intersection = get_intersection_of_two_tangent_circles(center, radius, arc_center, arc.radius)
        assert intersection is not None
        middle_between_phi_new_and_intersection = (intersection + radian_to_point(phi_new)) / 2
        direction = intersection - radian_to_point(phi_new)
        orthogonal_direction = np.array([-direction[1], direction[0], 0])
        center_of_circle = get_intersection(radian_to_point(phi_new), np.array([0, 0, 0]),
                                            middle_between_phi_new_and_intersection,
                                            orthogonal_direction + middle_between_phi_new_and_intersection)
        return center_of_circle, np.linalg.norm(center_of_circle - radian_to_point(phi_new))


class HexagonMainDiagonals(Group, ABC):
    def __init__(self, hexagon: Hexagon, color=WHITE, **kwargs):
        super().__init__(**kwargs)
        phis = hexagon.phis
        self.add(ArcBetweenPointsOnUnitDisk(phis[0], phis[3], color=color))
        self.add(ArcBetweenPointsOnUnitDisk(phis[1], phis[4], color=color))
        self.add(ArcBetweenPointsOnUnitDisk(phis[2], phis[5], color=color))


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

        middle = get_circle_middle(phi1, phi2)
        r = np.linalg.norm(middle - point1)

        # gets angle between two tangents
        angle = Angle(TangentLine(Circle(), alpha=phi1 / (2 * pi)),
                      TangentLine(Circle(), alpha=phi2 / (2 * pi)))

        ang = angle.get_value(degrees=False)
        if phi2 - phi1 < pi:
            super().__init__(start=point2, end=point1, angle=-ang, radius=r, color=color)
        else:
            super().__init__(start=point1, end=point2, angle=-ang, radius=r, color=color)
