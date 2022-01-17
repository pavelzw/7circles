from math import pi

import numpy as np
from manim import Scene, Circle, Dot, Create, FadeIn, Line, \
    Transform, RED, ThreeDAxes, ApplyPointwiseFunction, MovingCameraScene, Flash, YELLOW

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import radian_to_point, mobius_transform, \
    tf_klein_to_poincare, get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles
from hexagon import HexagonCircles, HexagonMainDiagonals, HyperbolicArcBetweenPoints
from hexagon_util import create_phis, create_phi_transition
from hyperbolic_polygon import HyperbolicPolygon


class CircleWithArcs(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))

        phis = np.sort(np.random.uniform(0, 2 * pi, 6))
        dot = Dot(radian_to_point(phis[0]), color=RED)
        self.add_foreground_mobject(dot)
        self.play(Create(dot))

        # create hyperbolic hexagon
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            point = radian_to_point(phi2)
            if i < phis.shape[0] - 1:
                dot = Dot(point, color=RED)
                self.add_foreground_mobject(dot)
                self.play(Create(dot))
            # bug: if two adjacent points have distance > pi, then the direction needs to be flipped
            arc = HyperbolicArcBetweenPoints.from_angles(phi1, phi2)
            self.play(Create(arc))

        self.wait(duration=5)


class CircleWithArcsMoving(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)

        phi_old = create_phis(min_dist=.4)
        phi_new = create_phis(min_dist=.4)
        step_size = 10
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_phi_transition(phi_old, phi_new, step_size=step_size)

        hexagon = HyperbolicPolygon.from_polar(transition[0])
        self.add(hexagon)

        for t in range(1, step_size):
            hexagon_new = HyperbolicPolygon.from_polar(transition[t])
            self.play(Transform(hexagon, hexagon_new), run_time=0.2, rate_func=lambda a: a)

        # self.wait(duration=5)


class LineTransform(Scene):
    def construct(self):
        phis_a = []
        phis_b = []
        lines = []
        for i in np.arange(0, 3, 1):
            phis_a.append(radian_to_point(i))
            phis_b.append(radian_to_point(i + 3))

        for p in phis_a:
            for q in phis_b:
                lines.append(Line(start=p, end=q, shade_in_3d=False, stroke_width=0.5))

        for line in lines:
            line.insert_n_curves(1000)

        circle = Circle(shade_in_3d=True)
        self.add(circle, ThreeDAxes())

        # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        n = 5
        animations = [[] for _ in range(n)]

        for line in lines:
            animations[0].append(Create(line))
            animations[1].append(ApplyPointwiseFunction(lambda x: tf_klein_to_poincare(0.9999 * x), line))
            for i in range(2, n):
                for k in lines:
                    for h in k:
                        animations[i].append(ApplyPointwiseFunction(lambda x: mobius_transform(x, 1.01, 0., 0.), h))

        self.play(*animations[0])
        self.play(*animations[1])
        for i in range(2, n):
            self.play(*animations[i], run_time=1, rate_func=(lambda x: x))


class SmallCircles(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 8
        circle = Circle()
        self.add(circle)

        phis = create_phis(min_dist=.4)

        first_circle_radius = .25
        hexagon = HyperbolicPolygon.from_polar(phis)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius)
        hexagon_diagonals = HexagonMainDiagonals(hexagon)
        self.add(hexagon)
        self.add(hexagon_circles)
        self.add(hexagon_diagonals)

        # self.wait(duration=5)


class SevenCircles(Scene):
    def construct(self):
        circle = Circle()
        phis = create_phis(min_dist=.8, max_dist=1.2)
        first_circle_radius = .4

        hexagon = EuclideanHexagon(phis)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius)
        inner_intersections = get_intersections_of_n_tangent_circles(hexagon_circles.circles)
        outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles)
        diagonals = get_diagonals(hexagon)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]), color=YELLOW)

        self.play(FadeIn(circle))
        self.play(Create(hexagon_circles, run_time=5))
        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))
        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))
        self.play(Create(hexagon, run_time=5))
        for x in diagonals:
            self.play(Create(x), run_time=1)
        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)
