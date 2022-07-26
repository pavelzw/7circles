import numpy as np
from manim import MovingCameraScene, Rectangle, WHITE, GREEN_B, PURPLE, DARK_GREY, GREY, ORANGE, YELLOW, Circle, Dot, \
    FadeIn, Write, Create, Flash, RED, BLUE, MathTex, LEFT, ReplacementTransform, GREEN_E, PURPLE_E, DOWN, Group, \
    Square, FadeOut, Transform, TransformFromCopy
from manim import MovingCameraScene, WHITE, GREEN_B, PURPLE, DARK_GREY, GREY, ORANGE, YELLOW, Circle, Dot, Transform

from animation_constants import OUTER_CIRCLE_COLOR, OUTER_CIRCLE_STROKE_WIDTH, HEXAGON_STROKE_WIDTH
from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import get_intersection_from_angles
from hexagon import HexagonAngles, HexagonCircles
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

        # keyframe hexagons
        phis1 = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))
        phis2 = HexagonAngles(np.array([.3, 1.2, 2.7, 3.6, 4.2]))
        phis3 = HexagonAngles(np.array([.7, 1.4, 2.3, 3.0, 4.1]))

        first_circle_radius = 0.4

        self.add(circle)
        self.add_foreground_mobject(circle)

        frame_rate = 60
        frame_time = 1 / 60
        run_time = 2
        frames = run_time * frame_rate

        i = 0
        phis = np.array([phis1[j] + ((i * (phis2[j] - phis1[j])) / frames) for j in range(5)])
        hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
        hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
        diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                    color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

        self.add(*hex_circles.circles, *diagonals, diagonal_intersection)

        for i in range(1, frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis1[j] + ((i * (phis2[j] - phis1[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        for i in range(frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis2[j] + ((i * (phis3[j] - phis2[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        for i in range(frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis3[j] + ((i * (phis1[j] - phis3[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        self.add(*hex_circles, *diagonals, diagonal_intersection)


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
