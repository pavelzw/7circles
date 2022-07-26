import numpy as np
from manim import MovingCameraScene, Rectangle, WHITE, GREEN_B, PURPLE, DARK_GREY, GREY, ORANGE, YELLOW, Circle, Dot, \
    FadeIn, Write, Create, Flash, RED, BLUE, MathTex, LEFT, ReplacementTransform, GREEN_E, PURPLE_E, DOWN, Group, \
    Square, FadeOut, Transform, TransformFromCopy

from animation_constants import OUTER_CIRCLE_COLOR, OUTER_CIRCLE_STROKE_WIDTH, HEXAGON_STROKE_WIDTH
from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles, get_intersection_points_of_n_tangent_circles, \
    get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon import HexagonAngles, HexagonCircles, HexagonMainDiagonals
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Rectangles(MovingCameraScene):
    def construct(self):
        # todo implement
        pass


class Scene1(MovingCameraScene):
    def construct(self):
        # todo create different hexagons
        self.camera.frame.scale(.3)
        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=2)
        # phis = create_phis(min_dist=.9, max_dist=1.2)
        phis = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))
        first_circle_radius = .4

        hexagon = EuclideanHexagon(phis, color=HEXAGON_COLOR, stroke_width=2)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
        inner_intersections = get_intersections_of_n_tangent_circles(hexagon_circles.circles,
                                                                     color=INNER_INTERSECTION_COLOR)
        outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles,
                                                                            color=OUTER_INTERSECTION_COLOR)
        diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                    color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

        self.wait(2)

        self.play(FadeIn(circle))
        self.add_foreground_mobject(circle)

        self.play(Create(hexagon_circles, run_time=5))
        self.remove_foreground_mobjects(circle)

        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))

        self.add_foreground_mobjects(*outer_intersections)

        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))

        self.play(Create(hexagon, run_time=5))

        for x in diagonals:
            self.play(Create(x), run_time=1)

        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)


class Scene2(MovingCameraScene):
    def construct(self):
        pass


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 4

        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add(circle)
        self.add_foreground_mobject(circle)

        phis = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))

        hexagon = HyperbolicPolygon.from_polar(phis, color=HEXAGON_COLOR, add_dots=False,
                                               stroke_width=HEXAGON_STROKE_WIDTH)
        inner_circles = HexagonCircles(hexagon, first_circle_radius=.4, color=GREEN_B,
                                       stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, color=ORANGE, stroke_width=HEXAGON_STROKE_WIDTH)

        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(diagonals.arc1.circle_center,
                                                                              diagonals.arc1.radius,
                                                                              diagonals.arc2.circle_center,
                                                                              diagonals.arc2.radius)
        intersection_dot = Dot(intersection, color=YELLOW, radius=.03)

        self.play(FadeIn(hexagon, inner_circles, diagonals, intersection_dot))
        self.add_foreground_mobjects(hexagon, diagonals, intersection_dot, circle)
        self.wait(1)

        # transform hyperbolic hexagon to euclidean hexagon
        euclidean_hexagon = EuclideanHexagon(phis, color=GREY, stroke_width=2)
        euclidean_diagonals = get_diagonals(hexagon, color=ORANGE, stroke_width=2)
        euclidean_intersection_dot = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]), color=YELLOW,
                                         radius=.03)
        self.add_foreground_mobjects(hexagon, diagonals, intersection_dot, circle)

        self.play(*[ReplacementTransform(hexagon.arcs[i], euclidean_hexagon.edges[i]) for i in range(6)],
                  ReplacementTransform(diagonals.arc1, euclidean_diagonals[0].reverse_direction()),
                  ReplacementTransform(diagonals.arc2, euclidean_diagonals[1].reverse_direction()),
                  ReplacementTransform(diagonals.arc3, euclidean_diagonals[2].reverse_direction()),
                  ReplacementTransform(intersection_dot, euclidean_intersection_dot),
                  run_time=3)
        self.wait(2)

        # quick fix such that hexagon gets transformed into old shape
        hexagon = HyperbolicPolygon.from_polar(phis, color=HEXAGON_COLOR, add_dots=False,
                                               stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, color=ORANGE, stroke_width=HEXAGON_STROKE_WIDTH)

        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(diagonals.arc1.circle_center,
                                                                              diagonals.arc1.radius,
                                                                              diagonals.arc2.circle_center,
                                                                              diagonals.arc2.radius)
        intersection_dot = Dot(intersection, color=YELLOW, radius=.03)

        self.play(*[ReplacementTransform(euclidean_hexagon.edges[i], hexagon.arcs[i]) for i in range(6)],
                  ReplacementTransform(euclidean_diagonals[0], diagonals.arc1),
                  ReplacementTransform(euclidean_diagonals[1], diagonals.arc2),
                  ReplacementTransform(euclidean_diagonals[2], diagonals.arc3),
                  ReplacementTransform(euclidean_intersection_dot, intersection_dot),
                  run_time=3)
        self.wait(2)
