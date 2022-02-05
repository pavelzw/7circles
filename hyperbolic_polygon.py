from abc import ABC
from typing import Union

import numpy as np
from manim import Dot, VGroup, WHITE, ArcBetweenPoints, Create, override_animation, AnimationGroup
from math import pi

from animation_constants import HEXAGON_DOT_CIRCLE_RADIUS
from geometry_util import polar_to_point, \
    point_to_polar, tf_poincare_to_klein, get_both_intersections_line_with_unit_circle, get_circle_middle


class HyperbolicArcBetweenPoints(ArcBetweenPoints, ABC):
    """
    ArcBetweenPoints that is a geodesic in the Poincaré model, i.e.,
    the arc connecting the two points intersects the unit sphere orthogonally.
    """

    @classmethod
    def from_angles(cls, phi1, phi2, **kwargs):
        return cls(polar_to_point(phi1), polar_to_point(phi2), **kwargs)

    def __init__(self, p1: np.ndarray, p2: np.ndarray, arcs_meeting_circle=False, **kwargs):
        klein_point1 = tf_poincare_to_klein(p1)  # transform points from poincare to klein model
        klein_point2 = tf_poincare_to_klein(p2)

        intersection1, intersection2 = get_both_intersections_line_with_unit_circle(klein_point1, klein_point2)

        if np.linalg.norm(intersection1 - p2) < np.linalg.norm(intersection1 - p1):
            tmp = intersection1
            intersection1 = intersection2
            intersection2 = tmp

        # get polar coordinates of intersections
        phi1, _ = point_to_polar(intersection1)
        phi2, _ = point_to_polar(intersection2)

        if phi1 < 0:  # for assertion phi >= 0
            phi1 += 2 * pi
        if phi2 < 0:
            phi2 += 2 * pi

        # calculate radius of arc
        self.circle_center = get_circle_middle(phi1, phi2)
        radius = np.linalg.norm(self.circle_center - intersection1)

        diff = phi2 - phi1
        if diff < 0:
            diff += 2 * pi
        if diff < pi:
            if arcs_meeting_circle:
                super(HyperbolicArcBetweenPoints, self).__init__(polar_to_point(phi2),
                                                                 polar_to_point(phi1),
                                                                 radius=radius, **kwargs)
            else:
                super(HyperbolicArcBetweenPoints, self).__init__(p2, p1, radius=radius, **kwargs)
            self.reverse_direction()
        else:
            if arcs_meeting_circle:
                super(HyperbolicArcBetweenPoints, self).__init__(polar_to_point(phi1),
                                                                 polar_to_point(phi2),
                                                                 radius=radius, **kwargs)
            else:
                super(HyperbolicArcBetweenPoints, self).__init__(p1, p2, radius=radius, **kwargs)


class HyperbolicPolygon(VGroup, ABC):
    @override_animation(Create)
    def _create(self, **kwargs):
        animations = []
        if len(self.dots) == 0:
            for arc in self.arcs:
                animations.append(Create(arc))
        else:
            for arc, dot in zip(self.arcs, self.dots):
                animations.append(Create(dot, run_time=0.00001))  # bug: run_time=0 doesn't work...
                animations.append(Create(arc))
        return AnimationGroup(*animations, lag_ratio=1, **kwargs)

    @classmethod
    def from_polar(cls, phis, radii=None, **kwargs):
        if radii is None:
            radii = [1] * len(phis)
        return cls([polar_to_point(arc, radius=radius) for arc, radius in zip(phis, radii)], **kwargs)

    def __init__(self, points: 'list[np.ndarray]', color: Union['list[str]', str] = None, add_dots=True,
                 dot_radius=HEXAGON_DOT_CIRCLE_RADIUS,
                 dot_color=WHITE,
                 **kwargs):
        super(HyperbolicPolygon, self).__init__()

        n = len(points)
        if type(color) == str:
            color = [color] * n
        if color is None:
            color = [WHITE] * n
        assert len(color) == n
        self._arcs = [HyperbolicArcBetweenPoints(points[i], points[(i + 1) % n], color=color[i], **kwargs)
                      for i in range(n)]

        self._dots = []

        if add_dots:
            self._dots.append(Dot(points[0], radius=dot_radius, color=dot_color))
            self.add(self._dots[-1])
        for i in range(n):
            if add_dots and i < n - 1:
                self._dots.append(Dot(points[i + 1], radius=dot_radius, color=dot_color))
                self.add(self._dots[-1])
            self.add(self.arcs[i])

        self._polygon_points = points

    @property
    def dots(self) -> 'list[Dot]':
        return self._dots

    @property
    def arcs(self) -> 'list[HyperbolicArcBetweenPoints]':
        return self._arcs

    @property
    def polygon_points(self) -> 'list[np.ndarray]':
        return self._polygon_points

    @property
    def phis(self) -> 'list[float]':
        return [point_to_polar(point)[0] for point in self.polygon_points]

    @property
    def radii(self) -> 'list[float]':
        return [point_to_polar(point)[1] for point in self.polygon_points]

    def __len__(self):
        return len(self.polygon_points)
