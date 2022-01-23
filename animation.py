from math import pi

import numpy as np
from manim import Scene, Circle, Dot, Create, FadeIn, Line, \
    Transform, RED, ThreeDAxes, ApplyPointwiseFunction, MovingCameraScene, Flash, YELLOW, Text, RIGHT, UP, Write, \
    MoveToTarget, DOWN, Tex, LEFT, BLUE, GREEN, WHITE, PURPLE, GREY, PINK, Group

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import polar_to_point, mobius_transform, \
    tf_klein_to_poincare, get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles, get_parallel_to_line_through_point, create_min_circle_radius
from hexagon import HexagonCircles, HexagonMainDiagonals, HyperbolicArcBetweenPoints
from hexagon_util import create_phis, create_phi_transition, create_radius_transition
from hyperbolic_polygon import HyperbolicPolygon


class CircleWithArcs(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))

        phis = np.sort(np.random.uniform(0, 2 * pi, 6))
        dot = Dot(polar_to_point(phis[0]), color=RED)
        self.add_foreground_mobject(dot)
        self.play(Create(dot))

        # create hyperbolic hexagon
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            point = polar_to_point(phi2)
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
            phis_a.append(polar_to_point(i))
            phis_b.append(polar_to_point(i + 3))

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

        self.wait(5)


class SevenCircles(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 9

        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = BLUE
        INNER_INTERSECTION_COLOR = GREEN
        OUTER_INTERSECTION_COLOR = GREY
        HEXAGON_COLOR = PINK
        DIAGONAL_COLOR = PURPLE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        title = Text("Der Sieben Kreise Satz").scale(0.8)

        t0 = Tex("Sei ", "$C_0$", " ein Kreis ").set_color_by_tex("C_0", OUTER_CIRCLE_COLOR).move_to(LEFT + 1.5 * DOWN)
        t1 = Tex("und ", "$C_1, \ldots, C_6$", " in $C_0$ enthaltene Kreise ").set_color_by_tex("C_1",
                                                                                                INNER_CIRCLE_COLOR)
        t2 = Tex("sodass jeder innere Kreis ", "zu $C_0$ tangential", " ist ").set_color_by_tex("C_0",
                                                                                                OUTER_INTERSECTION_COLOR)
        t3 = Tex("und je ", "zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential",
                 " sind.\n").set_color_by_tex("innere", INNER_INTERSECTION_COLOR)
        t4 = Tex("Dann treffen sich die drei ", "Diagonalen",
                 " des von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildeten",
                 " Hexagons ").set_color_by_tex("Diagonalen", DIAGONAL_COLOR).set_color_by_tex("Hexagon", HEXAGON_COLOR)
        t5 = Tex("in einem ", "Punkt", ".").set_color_by_tex("Punkt", DIAGONAL_INTERSECTION_COLOR)
        theorem_text = Group(t0, t1, t2, t3, t4, t5).arrange(DOWN).scale(0.3).move_to(
            1.5 * DOWN + LEFT).align_on_border(LEFT)

        circle = Circle(color=OUTER_CIRCLE_COLOR)
        phis = create_phis(min_dist=.8, max_dist=1.2)
        first_circle_radius = .4

        hexagon = EuclideanHexagon(phis, color=PINK)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius)
        inner_intersections = get_intersections_of_n_tangent_circles(hexagon_circles.circles,
                                                                     color=INNER_INTERSECTION_COLOR)
        outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles,
                                                                            color=OUTER_INTERSECTION_COLOR)
        diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                    color=DIAGONAL_INTERSECTION_COLOR)

        self.play(Write(title))
        # self.add_subcaption("Wir beschäftigen uns heute mit dem Sieben-Kreise-Satz. Unser Ziel ist es diesen über "
        # "einen interessanten Weg, der hyperbolische Geometrie mit einschließt zu beweisen.")
        self.wait(4)
        # self.add_subcaption("Aber zuerst einmal: Was sagt der Sieben-Kreise-Satz überhaupt aus?")

        self.play(title.animate.shift(1.5 * UP).scale(0.7), self.camera.frame.animate.shift(0.8 * DOWN))
        self.wait(1)

        self.play(FadeIn(circle), Write(t0))
        self.play(Create(hexagon_circles, run_time=5), Write(t1))

        self.play(Write(t2))
        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))
        self.play(Write(t3))
        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))
        self.play(Create(hexagon, run_time=5), Write(t4))
        for x in diagonals:
            self.play(Create(x), run_time=1)
        self.play(Create(diagonal_intersection), Write(t5))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)


class ParallelAxiom(Scene):
    def construct(self):
        left = -7
        right = 7

        g_fun = lambda x: -0.7 * x
        g_points = [[left, g_fun(left), 0], [right, g_fun(right), 0]]
        g = Line(g_points[0], g_points[1], name="g")
        g_text = Text("g")

        p_array = polar_to_point(1)
        p = Dot(p_array, name="P")
        p_text = Text("P").next_to(p, UP)

        h_fun = get_parallel_to_line_through_point(g_points, p_array)
        h_points = [[left, h_fun(left), 0], [right, h_fun(right), 0]]
        h = Line(h_points[0], h_points[1], name="h")
        h_text = Text("h").next_to(h, RIGHT)

        self.add_subcaption("Das Parallelenaxiom sagt aus, dass zu jeder Gerade g")
        self.wait(5)
        self.play(Create(g), subcaption="und jedem Punkt P, der nicht auf g liegt")
        self.play(Create(g_text))
        self.wait(2)
        self.play(Create(p), subcaption="genau eine Gerade h existiert, die durch P verläuft und zu g parallel ist.")
        self.play(Create(p_text))
        self.wait(2)
        self.play(Create(h))
        self.play(Create(h_text))
        self.wait(2)
        self.add_subcaption(
            "Parallel heißt hier einfach, dass sich die beiden Geraden nicht schneiden.")
