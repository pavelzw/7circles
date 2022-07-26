import numpy as np
from manim import MovingCameraScene, Rectangle, WHITE, GREEN_B, PURPLE, DARK_GREY, GREY, ORANGE, YELLOW, Circle, Dot, \
    FadeIn, Write, Create, Flash

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles
from hexagon import HexagonAngles, HexagonCircles


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
