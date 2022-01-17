from abc import ABC

import numpy as np
from manim import Dot, VGroup, WHITE

from geometry_util import radian_to_point, \
    point_to_radian
from hexagon import HyperbolicArcBetweenPoints


class HyperbolicPolygon(VGroup, ABC):
    @classmethod
    def from_polar(cls, phis, radii=None, **kwargs):
        if radii is None:
            radii = [1] * len(phis)
        return cls([radian_to_point(arc, radius=radius) for arc, radius in zip(phis, radii)], **kwargs)

    def __init__(self, points: 'list[np.ndarray]', colors: 'list[str]' = None, add_dots=True, dot_radius=.04, **kwargs):
        super(HyperbolicPolygon, self).__init__()

        n = len(points)
        if type(colors) == str:
            colors = [colors] * n
        if colors is None:
            colors = [WHITE] * n
        self.arcs = [HyperbolicArcBetweenPoints(points[i], points[(i + 1) % n], color=colors[i], **kwargs)
                     for i in range(n)]

        self.dots = []

        if add_dots:
            self.dots.append(Dot(points[0], radius=dot_radius))
            self.add(self.dots[-1])
        for i in range(n):
            if add_dots and i < n - 1:
                self.dots.append(Dot(points[i + 1], radius=dot_radius))
                self.add(self.dots[-1])
            self.add(self.arcs[i])

        self.polygon_points = points

    @property
    def phis(self):
        return [point_to_radian(point)[0] for point in self.polygon_points]
