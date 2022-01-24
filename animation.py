from math import pi

import numpy as np
from manim import Scene, Circle, Dot, Create, FadeIn, Line, \
    Transform, RED, ThreeDAxes, ApplyPointwiseFunction, MovingCameraScene, Flash, YELLOW, Text, UP, Write, \
    DOWN, Tex, BLUE, GREEN, WHITE, PURPLE, GREY, PINK, Uncreate, AnimationGroup, Unwrite, ImageMobject, LEFT, RIGHT, \
    MarkupText, Polygon

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

        theorem_text = Tex(r"Sei $C_0\ $ein Kreis ", r"und $C_1, \ldots, C_6$ in $C_0$ enthaltene Kreise, ",
                           "sodass jeder innere Kreis zu $C_0$ tangential ist ",
                           "und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind. ",
                           "Dann treffen sich die drei Diagonalen des von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildeten Hexagons ",
                           "in einem Punkt.", "",
                           substrings_to_isolate=[r"$C_0\ $", r"$C_1, \ldots, C_6$", "zu $C_0$ tangential",
                                                  "nebeneinanderliegende innere Kreise ebenfalls zueinander tangential",
                                                  "Diagonalen", "Hexagons", "Punkt"],
                           stroke_width=.05).set_color_by_tex(r"$C_0\ $",
                                                              OUTER_CIRCLE_COLOR).set_color_by_tex(
            r"$C_1, \ldots, C_6$",
            INNER_CIRCLE_COLOR).set_color_by_tex(
            "zu $C_0$ tangential",
            OUTER_INTERSECTION_COLOR).set_color_by_tex(
            "nebeneinanderliegende innere Kreise ebenfalls zueinander tangential",
            INNER_INTERSECTION_COLOR).set_color_by_tex(
            "Diagonalen", DIAGONAL_COLOR).set_color_by_tex(
            "Hexagons", HEXAGON_COLOR).set_color_by_tex("Punkt", DIAGONAL_INTERSECTION_COLOR).scale(
            0.5).move_to([0, -2, 0])

        circle = Circle(color=OUTER_CIRCLE_COLOR)
        phis = create_phis(min_dist=.9, max_dist=1.2)
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

        self.play(Write(theorem_text[0], run_time=.2))
        self.play(Write(theorem_text[1], run_time=.4))
        self.play(Write(theorem_text[2], run_time=.4))

        self.play(FadeIn(circle))

        self.play(Write(theorem_text[3], run_time=.2))
        self.play(Write(theorem_text[4], run_time=.6))
        self.play(Write(theorem_text[5], run_time=1.8))

        self.play(Create(hexagon_circles, run_time=5))

        self.play(Write(theorem_text[6], run_time=1.6))
        self.play(Write(theorem_text[7], run_time=1.2))
        self.play(Write(theorem_text[8], run_time=.2))

        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))

        self.play(Write(theorem_text[9]), run_time=.6)
        self.play(Write(theorem_text[10]), run_time=4.6)
        self.play(Write(theorem_text[11]), run_time=.2)

        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))

        self.play(Write(theorem_text[12]), run_time=1.2)
        self.play(Write(theorem_text[13]), run_time=.8)
        self.play(Write(theorem_text[14]), run_time=5)
        self.play(Write(theorem_text[15]), run_time=.6)

        self.play(Create(hexagon, run_time=5))
        for x in diagonals:
            self.play(Create(x), run_time=1)

        self.play(Write(theorem_text[16]), run_time=.6)
        self.play(Write(theorem_text[17]), run_time=.2)
        self.play(Write(theorem_text[18], run_time=.2))
        self.play(Write(theorem_text[19]))

        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)


class ParallelAxiom(MovingCameraScene):
    def construct(self):
        center = [0, 2, 0]
        left = -7
        right = 7

        title = Text("Parallelenaxiom").scale(0.7).shift(5 * UP)

        g_fun = lambda x: -0.7 * x
        g_points = [[left, g_fun(left), 0], [right, g_fun(right), 0]]
        g = Line(g_points[0], g_points[1], name="g")
        g_text = Tex("$g$", stroke_width=0.05).move_to([-3.7, 3, 0])

        p_array = polar_to_point(1)
        p = Dot(p_array, name="P", color=YELLOW)
        p_text = Tex("$P$", stroke_width=0.05).next_to(p, UP)

        h_fun = get_parallel_to_line_through_point(g_points, p_array)
        h_points = [[left, h_fun(left), 0], [right, h_fun(right), 0]]
        h = Line(h_points[0], h_points[1], name="h")
        h_text = Tex("$h$", stroke_width=0.05).move_to([-1.7, 3, 0])

        similar_to_g = [lambda x: x * -.65, lambda x: x * -.8, lambda x: x * -.57, lambda x: x * -.77]
        similar_points = [[[left, _(left), 0.], [right, _(right), 0.]] for _ in similar_to_g]
        similar_funcs = [get_parallel_to_line_through_point(sim_points, p_array) for sim_points in similar_points]
        sim_h_points = [[[left, _(left), 0.], [right, _(right), 0.]] for _ in similar_funcs]
        similar_lines = [Line(_[0], _[1], stroke_width=1) for _ in sim_h_points]

        elements = [title, g, g_text, h, h_text, p, p_text, similar_lines[0], similar_lines[1],
                    similar_lines[2],
                    similar_lines[3]]

        uncreate = AnimationGroup(*[Uncreate(i, run_time=1) for i in elements])

        question = Text("Wie stellt man die hyperbolischen Ebene im Euklidischen dar?").scale(0.7).move_to(center)

        self.camera.frame.move_to(center)
        self.play(Create(title))
        self.add_subcaption("Das Parallelenaxiom sagt aus, dass zu jeder Gerade g", duration=3)
        self.play(Create(g))
        self.play(Create(g_text))
        self.wait(2)
        self.add_subcaption("und jedem Punkt P, der nicht auf g liegt", duration=3)
        self.play(Create(p))
        self.play(Create(p_text))
        self.add_foreground_mobject(p)
        self.wait(2)
        self.add_subcaption("genau eine Gerade h existiert, die durch P verläuft und zu g parallel ist.", duration=3)
        self.play(Create(h))
        self.play(Create(h_text))
        self.wait(2)
        self.add_subcaption(
            "Parallel heißt hier einfach, dass sich die beiden Geraden nicht schneiden.", duration=3)
        self.wait(5)
        self.add_subcaption("In der hyperbolischen Geometrie ist diese Eigenschaft nicht gegeben.", duration=3)
        self.wait(3)
        self.add_subcaption(
            "Dort gibt es für jedes solche g und P mehrere, sogar unendlich viele Geraden durch P, die zu g parallel sind also g nicht schneiden.",
            duration=4)

        self.play(Create(similar_lines[0]))
        self.play(Create(similar_lines[1]))
        self.play(Create(similar_lines[2]))
        self.play(Create(similar_lines[3]))

        self.add_subcaption(
            "Unsere Darstellung hier ist aber irreführend, denn natürlich schneiden alle außer der ursprünglichen Gerade $h$ $g$ wenn wir den Geraden nur lange genug folgen.",
            duration=4)
        self.wait(4)
        self.add_subcaption(
            "Allgemein haben wir das Problem, dass wir einen Raum in dem hyperbolische Geometrie herrscht in einem euklidischen zweidimensionalen Video darstellen wollen.",
            duration=4)
        self.wait(4)
        self.add_subcaption("Die Frage ist also: Wie stellt man die hyperbolischen Ebene im Euklidischen dar?",
                            duration=4)
        self.play(uncreate)
        self.wait(1)
        self.play(Write(question))
        self.wait(3)
        self.play(Unwrite(question))


class HyperbolicModels(MovingCameraScene):
    def construct(self):
        center = [0, 0, 0]

        klein_origin = [3.5, -1, 0]
        poincare_origin = [-3.5, -1, 0]

        title = MarkupText(
            f'<span underline="single" underline_color="white">Modelle für die hyperbolische Ebene</span>').scale(
            0.8).shift(3.5 * UP)

        klein_model = ImageMobject("tessellation_klein.png").move_to(1 * DOWN + 3.5 * RIGHT).scale(0.7)
        klein_text = Text("Klein-Modell").scale(0.6).move_to(3.5 * RIGHT + 2.2 * UP)
        poincare_model = ImageMobject("tessellation_poincare.png").move_to(1 * DOWN + 3.5 * LEFT).scale(0.7)
        poincare_text = Text("Poincaré-Modell").scale(0.6).move_to(3.5 * LEFT + 2.2 * UP)

        self.add(title, klein_model, klein_text, poincare_model, poincare_text)

        k1 = np.array([[0, 0, 0], [2, 0, 0], [1.24, 1.58, 0]])
        k2 = np.array([[-0.46, 1.95, 0], [-1.81, 0.89, 0], [-1.49, 1.86, 0]])

        p1 = np.array([[0., 0., 0.], [1.25, 0, 0], [0.78, 0.98, 0]])
        p2 = np.array([[-.28, 1.23, 0], [-1.12, 0.55, 0], [-1.12, 1.42, 0]])

        scale_front = 0.4
        scale_back = 2.5

        p1 = scale_front * p1
        p2 = scale_front * p2

        ktri1 = Polygon(*k1).shift(klein_origin)
        ktri2 = Polygon(*k2).shift(klein_origin)
        ptri1 = HyperbolicPolygon(p1).scale(scale_back).shift(np.add(poincare_origin, [0.38, 0.32, 0]))
        ptri2 = HyperbolicPolygon(p2).scale(scale_back).shift(np.add(poincare_origin, [-0.44, 0.59, 0]))

        self.add(ktri1, ktri2, ptri1, ptri2)

        # self.play(Write(title))
        # self.add_foreground_mobject(title)
        # self.wait(1)
#
# self.add_foreground_mobject(poincare_text)
# self.play(Write(poincare_text), FadeIn(poincare_model), run_time=3)
# self.wait(3)
#
# self.add_foreground_mobject(klein_text)
# self.play(Write(klein_text), FadeIn(klein_model), run_time=3)
# self.wait(3)
#
# self.play(self.camera.frame.animate.scale(0.8).move_to(np.add(poincare_origin, [0, 0.4, 0])),
#          FadeOut(klein_model), FadeOut(klein_text))
#
# self.wait(5)
#
# self.play(self.camera.frame.animate.scale(1.25).move_to(center), FadeIn(klein_model), FadeIn(klein_text))
#
# self.wait(5)
#
# self.play(self.camera.frame.animate.scale(0.8).move_to(np.add(klein_origin, [0, 0.4, 0])),
#          FadeOut(poincare_model), FadeOut(poincare_text))
#
# self.wait(5)
