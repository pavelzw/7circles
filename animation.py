import numpy as np
from manim import Circle, Dot, Create, FadeIn, Line, \
    Transform, MovingCameraScene, Flash, YELLOW, Text, UP, Write, \
    DOWN, Tex, WHITE, PURPLE, GREY, Uncreate, AnimationGroup, Unwrite, ImageMobject, LEFT, RIGHT, \
    MarkupText, Polygon, PI, DecimalNumber, ValueTracker, Arrow, VGroup, FadeOut, Indicate, \
    ReplacementTransform, BLACK, VMobject, GREEN_B, ORANGE, DARK_GREY

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import polar_to_point, \
    tf_klein_to_poincare, get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles, get_parallel_to_line_through_point, tf_poincare_to_klein, \
    get_both_intersections_line_with_unit_circle, hyperbolic_distance_function
from hexagon import HexagonCircles, HexagonMainDiagonals, HyperbolicArcBetweenPoints, HexagonAngles
from hyperbolic_polygon import HyperbolicPolygon


class SevenCircles(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 9

        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        title = Text("Der Sieben-Kreise-Satz").scale(0.8)

        theorem_text_white = Tex(r"Sei $C_0\ $ein Kreis ", r"und $C_1, \ldots, C_6$ in $C_0$ enthaltene Kreise, ",
                                 "sodass jeder innere Kreis zu $C_0$ tangential ist ",
                                 "und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind. ",
                                 "Dann treffen sich die drei Diagonalen des Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird, ",
                                 "in einem Punkt.", "",
                                 stroke_width=.05).scale(
            0.5).move_to([0, -2, 0])

        theorem_text_colored = Tex(r"Sei $C_0\ $ein Kreis ", r"und $C_1, \ldots, C_6$ in $C_0$ enthaltene Kreise, ",
                                   "sodass jeder innere Kreis zu $C_0$ tangential ist ",
                                   "und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind. ",
                                   "Dann treffen sich die drei Diagonalen des Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird, ",
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

        self.add_subcaption("Wir beschäftigen uns heute mit dem Sieben-Kreise-Satz", duration=3)
        self.play(Write(title))

        self.wait(2)
        self.add_subcaption("Der Sieben-Kreise-Satz sagt Folgendes aus:", duration=2)

        self.play(title.animate.shift(1.4 * UP).scale(0.7), self.camera.frame.animate.shift(0.8 * DOWN))
        self.wait(1)

        self.add_subcaption("Sei C_0 ein Kreis", duration=2)

        self.play(Write(theorem_text_white[0], run_time=1))

        self.play(FadeIn(circle), FadeIn(theorem_text_colored[1]))
        self.add_foreground_mobject(circle)

        self.add_subcaption("und C_1,...,C_6 in C_0 enthaltene Kreise", duration=4)

        self.play(Write(theorem_text_white[1], run_time=3))

        self.play(Create(hexagon_circles, run_time=5), FadeIn(theorem_text_colored[4], run_time=1))
        self.remove_foreground_mobjects(circle)

        self.add_subcaption("sodass jeder innere Kreis zum äußeren Kreis tangential ist", duration=5)

        self.play(Write(theorem_text_white[2], run_time=3))
        self.play(FadeIn(theorem_text_colored[7]))
        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))

        self.add_foreground_mobjects(*outer_intersections)

        self.add_subcaption("und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind.",
                            duration=8)

        self.play(Write(theorem_text_white[3]), run_time=6)
        self.play(FadeIn(theorem_text_colored[10]))

        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))

        self.add_subcaption(
            "Dann treffen sich die drei Diagonalen des Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird,",
            duration=8)

        self.play(Write(theorem_text_white[4]), run_time=8)

        self.play(Create(hexagon, run_time=5), FadeIn(theorem_text_colored[15], run_time=1))
        self.play(FadeIn(theorem_text_colored[13]))
        for x in diagonals:
            self.play(Create(x), run_time=1)

        self.add_subcaption("in einem Punkt", duration=3)

        self.play(Write(theorem_text_white[5]), run_time=3)

        self.play(FadeIn(theorem_text_colored[18], run_time=1))

        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)

        self.add_subcaption("Unser Ziel ist es jetzt diesen Satz zu beweisen.", duration=4)
        self.wait(4)

        self.add_subcaption(
            "Das wird uns mithilfe einer Einbettung des Problems in einen hyperbolischen Rahmen gelingen.", duration=5)
        self.wait(5)

        self.add_subcaption("Zuerst geben wir dafür eine kleine Einführung in die hyperbolische Geometrie,", duration=4)
        self.wait(4)
        self.add_subcaption(
            "um das Problem mit unserem neugewonnenen Wissen umzuformulieren und weiter zu bearbeiten.", duration=4)
        self.wait(3)

        everything = VGroup()
        for mob in self.mobjects:
            if isinstance(mob, VMobject):
                everything.add(mob)

        endDot = Dot(color=BLACK)
        self.add(endDot)
        self.play(Transform(everything, endDot), run_time=2)
        self.wait(2)


class ParallelAxiom(MovingCameraScene):
    def construct(self):
        center = [0, 2, 0]
        left = -7
        right = 7

        title = Text("Parallelenaxiom").scale(0.7).shift(5.4 * UP)

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

        question = Text("Wie stellt man die hyperbolische Ebene im Euklidischen dar?").scale(0.65).move_to(center)

        self.camera.frame.move_to(center)
        self.add_subcaption("Axiomatisch unterscheidet sich der hyperbolische Raum vom Euklidischen", duration=4)
        self.wait(4)
        self.add_subcaption("dadurch, dass das Parallelenaxiom nicht gilt.", duration=4)
        self.wait(2)
        self.play(Write(title), run_time=2)
        self.add_subcaption("Das Parallelenaxiom sagt aus, dass zu jeder Geraden g", duration=3)
        self.play(Create(g))
        self.play(Write(g_text))
        self.wait(2)
        self.add_subcaption("und jedem Punkt P, der nicht auf g liegt", duration=3)
        self.play(Create(p))
        self.play(Write(p_text))
        self.add_foreground_mobject(p)
        self.wait(2)
        self.add_subcaption("genau eine Gerade h existiert, die durch P verläuft und zu g parallel ist.", duration=4)
        self.play(Create(h))
        self.play(Write(h_text))
        self.wait(2)
        self.add_subcaption(
            "Parallel heißt hier einfach, dass sich die beiden Geraden nicht schneiden.", duration=4)
        self.wait(5)
        self.add_subcaption("In hyperbolischer Geometrie ist diese Eigenschaft nicht gegeben.", duration=3)
        self.wait(4)
        self.add_subcaption(
            "Dort gibt es für jede solche g und P mehrere - sogar unendlich viele - Geraden durch P, die zu g parallel sind also g nicht schneiden.",
            duration=10)

        self.play(Create(similar_lines[0]))
        self.play(Create(similar_lines[1]))
        self.play(Create(similar_lines[2]))
        self.play(Create(similar_lines[3]))

        self.wait(6)

        self.add_subcaption(
            "Unsere Darstellung hier ist aber irreführend, denn natürlich wird g von allen außer der ursprünglichen Geraden h geschnitten, wenn wir ihnen nur lange genug folgen.",
            duration=10)
        self.wait(10)
        self.add_subcaption(
            "Allgemein haben wir das Problem, dass wir einen hyperbolischen Raum in der euklidischen Ebene - diesem Video - darstellen wollen.",
            duration=9)
        self.wait(9)
        self.add_subcaption(
            "Die Frage die wir jetzt angehen ist also: Wie stellt man die hyperbolische Ebene im Euklidischen dar?",
            duration=7)
        self.play(uncreate)
        self.wait(1)
        self.play(Write(question))
        self.wait(3)
        self.play(Unwrite(question))


class HyperbolicModelsPoincare(MovingCameraScene):
    def construct(self):
        center = np.array([0, 0, 0])

        klein_origin = np.array([3.5, -1, 0])
        poincare_origin = np.array([-3.5, -1, 0])

        MY_BLUE = "#22c1dd"

        title = MarkupText(
            "Modelle für die hyperbolische Ebene").scale(
            0.8).shift(3.5 * UP)

        klein_model = ImageMobject("tessellation_klein.png").scale(0.7).move_to(klein_origin)
        klein_text = Text("Klein-Modell").scale(0.6).move_to(3.5 * RIGHT + 2.2 * UP)
        poincare_model = ImageMobject("tessellation_poincare.png").scale(0.7).move_to(poincare_origin)
        poincare_text = Text("Poincaré-Modell").scale(0.6).move_to(3.5 * LEFT + 2.2 * UP)

        p1 = np.array([[0., 0., 0.], [1.25, 0, 0], [0.78, 0.98, 0]])
        p2 = np.array([[-.28, 1.23, 0], [-1.12, 0.55, 0], [-1.12, 1.42, 0]])

        scale_front = 0.4
        scale_back = 2.5

        p1 = scale_front * p1
        p2 = scale_front * p2

        pcircle = Circle(color=MY_BLUE, stroke_width=1).scale(scale_back).move_to(poincare_origin)

        ptri1 = HyperbolicPolygon(p1,
                                  stroke_width=1.5, dot_radius=.02, color=YELLOW, dot_color=YELLOW).scale(
            scale_back)
        ptri1.move_to(ptri1.get_center() * scale_back).shift(poincare_origin)
        ptri2 = HyperbolicPolygon(p2,
                                  stroke_width=1.5, dot_radius=.02, color=YELLOW, dot_color=YELLOW).scale(
            scale_back)
        ptri2.move_to(ptri2.get_center() * scale_back).shift(poincare_origin)
        # self.add(ktri1, ktri2, ptri1, ptri2)

        ptri1_text = Tex(r"$\Delta_1$").next_to(ptri1).scale(.6).shift(0.5 * LEFT)

        ptri2_text = Tex(r"$\Delta_2$").next_to(ptri2).scale(.6).shift(0.3 * LEFT)

        ptri_size_text = Tex(r"$A(\Delta_1) = A(\Delta_2)$", font_size=35).next_to(pcircle, buff=.4)

        phis = [[0.4, 2], [1.3, 6], [3.5, 5], [4, 1.5]]

        p_geodesics_raw = [HyperbolicArcBetweenPoints(polar_to_point(x), polar_to_point(y)) for [x, y] in phis]
        p_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(poincare_origin) for geo in
                       p_geodesics_raw]

        point_coords = [0, -0.3, 0]
        p_point = Dot(point_coords)
        p_point.move_to(p_point.get_center() * scale_back).shift(poincare_origin)

        p_point_text = Tex("$P$").scale(0.8).next_to(p_point, direction=UP + 0.2 * RIGHT)

        point_geodesic_point_phis = [0, 2.3, 2.9, 3.15, 3.4, 3.8, 4.1, 4.5, 5]
        p_point_geodesic_points = [polar_to_point(x) for x in point_geodesic_point_phis]
        p_point_geodesics_both_points = [
            get_both_intersections_line_with_unit_circle(x, tf_poincare_to_klein(point_coords)) for x in
            p_point_geodesic_points]
        p_point_geodesics = [HyperbolicArcBetweenPoints(points[0], points[1], color=MY_BLUE) for points in
                             p_point_geodesics_both_points]
        p_point_moved_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(poincare_origin)
                                   for geo in
                                   p_point_geodesics]

        p_moving_dot = Dot(poincare_origin)
        p_moving_text = Tex("$P$", font_size=25).next_to(p_moving_dot, 0.5 * RIGHT + 0.6 * UP, buff=0)
        p_moving_dot_phi = 5 * PI / 3
        norm_factor = 6 / pow(PI, 2)

        p_origin = Dot(poincare_origin)
        p_origin_text = Tex("0", font_size=25).next_to(p_origin, LEFT, buff=.1)

        p_current_point = np.array(center)

        p_distance_text = Tex(r"$\mathrm{dist}(0,P) = $ ", font_size=30).next_to(pcircle, buff=.2)
        p_distance_number = DecimalNumber(0.0,
                                          num_decimal_places=2, show_ellipsis=True, group_with_commas=False,
                                          font_size=35).next_to(p_distance_text, buff=.15)

        label = VGroup(p_distance_text, p_distance_number)
        p_distance_infty = Tex(r"$\infty$", font_size=30).next_to(p_distance_text, buff=.15)
        p_distance_tracker = ValueTracker(0.0)

        self.add_subcaption("Es gibt verschiedene Modelle für die hyperbolische Ebene.", duration=3)

        self.play(Write(title), run_time=2)
        self.add_foreground_mobject(title)
        self.wait(1)

        self.add_subcaption("Solche Modelle sind einfach Abbildungen von der hyperbolischen in die euklidische Ebene",
                            duration=5)

        self.wait(5)

        self.add_subcaption("Wir beschäftigen uns genauer mit dem Poincare-", duration=3)

        self.add_foreground_mobject(poincare_text)
        self.play(Write(poincare_text), FadeIn(poincare_model), run_time=3)

        self.add_subcaption("und dem Klein-Modell.", duration=3)

        self.add_foreground_mobject(klein_text)
        self.play(Write(klein_text), FadeIn(klein_model), run_time=3)
        self.wait(3)

        self.add_subcaption("Zuerst schauen wir uns das Poincare-Modell etwas genauer an.", duration=4)

        self.add(pcircle)
        self.play(self.camera.frame.animate.scale(0.8).move_to(np.add(poincare_origin, [0, 0.4, 0])),
                  FadeOut(klein_model), FadeOut(klein_text), FadeOut(poincare_model), run_time=1.5)

        self.wait(2.5)

        self.add_subcaption(
            "Die Darstellung der hyperbolischen Ebene im Poincare-Modell beschränkt sich auf die Einheitsscheibe",
            duration=6)

        self.wait(3)

        self.play(Indicate(pcircle, color=MY_BLUE, scale_factor=1.1))

        self.wait(2)

        self.add_subcaption(
            "Die Geodätischen des Poincare-Modells sind - im Gegensatz zu Geraden im Euklidischen - ",
            duration=5)

        self.play(Create(p_geodesics[0]))
        self.play(Create(p_geodesics[1]))
        self.play(Create(p_geodesics[2]))
        self.play(Create(p_geodesics[3]))

        self.wait(1)

        self.add_subcaption("Kreissegmente, die den Einheitskreis im rechten Winkel schneiden",
                            duration=4)

        self.wait(4)

        self.add_subcaption("Damit wird klar, dass das Parallelenaxiom hier nicht gilt:", duration=4)

        self.play(Uncreate(p_geodesics[1], run_time=3), Uncreate(p_geodesics[2], run_time=3),
                  Uncreate(p_geodesics[3], run_time=3), Create(p_point, run_time=1),
                  Write(p_point_text, run_time=1))

        self.wait(2)

        self.add_subcaption("Für einen Punkt P und eine Geodätische findet man", duration=3)

        self.add_foreground_mobject(p_point)
        self.add_foreground_mobject(p_point_text)
        self.wait(3)

        self.add_subcaption(
            "beliebig viele andere Geodätische, die P, aber nicht die ursprüngliche Geodätische schneiden.", duration=6)

        self.play(Create(p_point_moved_geodesics[0]))
        self.play(Create(p_point_moved_geodesics[1]))
        self.play(Create(p_point_moved_geodesics[2]))
        self.play(Create(p_point_moved_geodesics[3]))
        self.play(Create(p_point_moved_geodesics[4]))
        self.play(Create(p_point_moved_geodesics[5]))
        self.play(Create(p_point_moved_geodesics[6]))

        self.add_subcaption(
            "Auch wenn es auf den ersten Blick so scheint, ist die hyperbolische Ebene keineswegs beschränkt.",
            duration=6)

        self.wait(2)

        self.play(Uncreate(p_geodesics[0]),
                  Uncreate(p_point_moved_geodesics[0]),
                  Uncreate(p_point_moved_geodesics[1]),
                  Uncreate(p_point_moved_geodesics[2]),
                  Uncreate(p_point_moved_geodesics[3]),
                  Uncreate(p_point_moved_geodesics[4]),
                  Uncreate(p_point_moved_geodesics[5]),
                  Uncreate(p_point_moved_geodesics[6]),
                  Uncreate(p_point), Unwrite(p_point_text))

        self.wait(3)

        self.add_subcaption(
            "Lassen wir einen Punkt in der hyperbolischen Ebene mit konstanter Geschwindigkeit in eine Richtung laufen, so sehen wir, dass dieser den Rand des Poincare-Modell nie erreicht.",
            duration=12)

        self.play(Create(p_moving_dot), Create(p_origin), Write(p_distance_text), Write(p_origin_text),
                  Write(p_moving_text))
        self.play(Write(p_distance_number))

        self.wait(4)

        p_distance_number.add_updater(lambda d: d.set_value(p_distance_tracker.get_value()))

        steps = 30
        frames = 420
        duration = 7
        frame_rate = duration / frames
        batch_size = frames / steps
        offset = 0

        for t in range(1, frames):
            if batch_size == 1:
                r = t
            else:
                r = 1 + int(t / batch_size)

            if t % batch_size == 1 or batch_size == 1:
                offset = np.array(
                    polar_to_point(p_moving_dot_phi, norm_factor / (batch_size * pow(r, 2))))
            p_current_point = p_current_point + offset
            pos = p_current_point * scale_back + np.array(poincare_origin)
            moving_dot = Dot(pos, radius=0.08)

            p_distance_number.font_size = 35

            p_distance_tracker.set_value(np.exp(
                hyperbolic_distance_function(center, p_current_point)))
            label.arrange(buff=.15)
            label.next_to(pcircle, buff=.2)

            p_moving_text.next_to(p_moving_dot, 0.5 * RIGHT + 0.6 * UP, buff=0)
            self.play(Transform(p_moving_dot, moving_dot), run_time=frame_rate,
                      rate_func=lambda a: a)
            self.remove(p_moving_dot)
            p_moving_dot = moving_dot
        label.arrange(buff=.05)
        label.next_to(pcircle, buff=.2)

        self.add_subcaption("Der Einheitskreis liegt im Unendlichen und gehört nicht zum Poincare-Modell",
                            duration=5)

        moving_dot = Dot(polar_to_point(p_moving_dot_phi) * scale_back + np.array(poincare_origin))

        self.play(Transform(p_moving_dot, moving_dot), FadeOut(p_distance_number), FadeIn(p_distance_infty),
                  FadeOut(p_moving_text),
                  run_time=.25)

        self.wait(4)

        self.play(FadeOut(p_moving_dot), FadeOut(p_distance_infty), FadeOut(p_distance_text))

        self.add_subcaption("Zum weiteren Verständnis ist folgende Darstellung der Verzerrung hilfreich", duration=5)

        self.wait(3)

        self.play(FadeIn(poincare_model), FadeOut(pcircle), run_time=2)

        self.add_subcaption(
            "Dies ist eine Parkettierung der hyperbolischen Ebene. All diese Dreiecke haben die gleiche Form und Fläche im Hyperbolischen.",
            duration=8)
        self.play(Create(ptri1), run_time=2)
        self.play(Write(ptri1_text.shift(0.6 * LEFT + 0.15 * DOWN)))

        self.wait(1)

        self.play(Create(ptri2), run_time=2)
        self.play(Write(ptri2_text.shift(0.8 * LEFT + 0.07 * UP)))

        self.wait(1)

        self.play(Write(ptri_size_text), run_time=2)

        self.add_subcaption(
            "Das Poincare-Modell liefert also eine stark verzerrte Darstellung des hyperbolischen Raumes.", duration=6)

        self.wait(4)

        self.play(Uncreate(ptri1), Uncreate(ptri2), Unwrite(ptri1_text), Unwrite(ptri2_text),
                  Unwrite(ptri_size_text), run_time=2)

        self.play(self.camera.frame.animate.scale(1.25).move_to(center), FadeIn(klein_model), FadeIn(klein_text))

        self.wait(2)


class HyperbolicModelsKlein(MovingCameraScene):
    def construct(self):
        center = np.array([0, 0, 0])

        klein_origin = np.array([3.5, -1, 0])
        poincare_origin = np.array([-3.5, -1, 0])

        MY_BLUE = "#22c1dd"

        title = MarkupText(
            "Modelle für die hyperbolische Ebene").scale(
            0.8).shift(3.5 * UP)

        klein_model = ImageMobject("tessellation_klein.png").scale(0.7).move_to(klein_origin)
        klein_text = Text("Klein-Modell").scale(0.6).move_to(3.5 * RIGHT + 2.2 * UP)
        poincare_model = ImageMobject("tessellation_poincare.png").scale(0.7).move_to(poincare_origin)
        poincare_text = Text("Poincaré-Modell").scale(0.6).move_to(3.5 * LEFT + 2.2 * UP)

        title2 = Text("Transformationen zwischen hyperbolischen Modellen").scale(.75).shift(3.5 * UP)

        scale_back = 2.5

        phis = [[0.4, 2], [1.3, 6], [3.5, 5], [4, 1.5]]

        k1 = np.array([[0, 0, 0], [2, 0, 0], [1.24, 1.58, 0]])
        k2 = np.array([[-0.46, 1.95, 0], [-1.79, 0.89, 0], [-1.49, 1.86, 0]])

        raw_ktri1 = Polygon(*k1, color=YELLOW, stroke_width=1.5).shift(klein_origin)
        kpoints1 = [Dot(np.add(p, klein_origin), color=YELLOW, radius=.06) for p in k1]
        raw_ktri2 = Polygon(*k2, color=YELLOW, stroke_width=1.5).shift(klein_origin)
        kpoints2 = [Dot(np.add(p, klein_origin), color=YELLOW, radius=.06) for p in k2]

        kcircle = Circle(color=MY_BLUE, stroke_width=1).scale(scale_back).move_to(klein_origin)
        pcircle = Circle(color=MY_BLUE, stroke_width=1).scale(scale_back).move_to(poincare_origin)

        p_geodesics_raw = [HyperbolicArcBetweenPoints(polar_to_point(x), polar_to_point(y)) for [x, y] in phis]
        p_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(poincare_origin) for geo in
                       p_geodesics_raw]

        k_geodesics_raw = [Line(polar_to_point(x), polar_to_point(y)) for [x, y] in phis]
        k_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(klein_origin) for geo in
                       k_geodesics_raw]

        point_coords = [0, -0.3, 0]
        point_geodesic_point_phis = [0, 2.3, 2.9, 3.15, 3.4, 3.8, 4.1, 4.5, 5]
        k_point = Dot(point_coords)
        k_point.move_to(k_point.get_center() * scale_back).shift(klein_origin)

        k_point_text = Tex("$P$").scale(0.8).next_to(k_point, direction=UP + 0.2 * RIGHT)

        k_point_geodesics_intersections = [
            get_both_intersections_line_with_unit_circle(point_coords, polar_to_point(phi))
            for phi in point_geodesic_point_phis]
        k_point_geodesics_raw = [Line(x, y, color=MY_BLUE) for [x, y] in k_point_geodesics_intersections]
        k_point_geodesics = [l.scale(scale_back).move_to(l.get_center() * scale_back).shift(klein_origin) for l in
                             k_point_geodesics_raw]

        ktri1_text = Tex(r"$\Delta_1$").next_to(raw_ktri1, LEFT).scale(.6).shift(1.6 * RIGHT + 0.2 * DOWN)

        ktri2_text = Tex(r"$\Delta_2$").next_to(raw_ktri2, LEFT).scale(.6).shift(1.05 * RIGHT + .2 * UP)

        ktri_size_text = Tex(r"$A(\Delta_1) = A(\Delta_2)$", font_size=37).next_to(kcircle, LEFT, buff=.35)

        arrow_lr = Arrow(start=2.5 * LEFT, end=2.5 * RIGHT, stroke_width=4, max_tip_length_to_length_ratio=.5)
        arrow_rl = Arrow(start=2.5 * RIGHT, end=2.5 * LEFT, stroke_width=4, max_tip_length_to_length_ratio=.5)
        arrow_group = VGroup(arrow_lr, arrow_rl).arrange(DOWN)
        arrow_group.shift(DOWN)

        f_text = Tex(r"$f$", font_size=40).next_to(arrow_lr, UP, buff=0)
        f_inv_text = Tex(r"$f^{-1}$", font_size=40).next_to(arrow_rl, DOWN, buff=0)

        f_formula = Tex(r"$f(x,y) = \frac{1}{1+\sqrt{1-x^2-y^2}}(x,y)$", font_size=40).move_to(.5 * UP)
        f_inv_formula = Tex(r"$f^{-1}(x,y) = \frac{1}{1+x^2+y^2}(2x,2y)$", font_size=40).move_to(2.5 * DOWN)

        p_geo0 = p_geodesics[0].copy()
        p_geo0 = p_geo0.shift(-poincare_origin).scale(0.7).move_to(p_geo0.get_center() * 0.7).shift(
            poincare_origin + 1.5 * LEFT)
        p_geo0_copy = p_geo0.copy()

        p_geo1 = p_geodesics[2].copy()
        p_geo1 = p_geo1.shift(-poincare_origin).scale(0.7).move_to(p_geo1.get_center() * 0.7).shift(
            poincare_origin + 1.5 * LEFT)

        k_geo0 = k_geodesics[0].copy()
        k_geo0 = k_geo0.shift(-klein_origin).scale(0.7).move_to(k_geo0.get_center() * 0.7).shift(
            klein_origin + 1.5 * RIGHT)

        k_geo1 = k_geodesics[2].copy()
        k_geo1 = k_geo1.shift(-klein_origin).scale(0.7).move_to(k_geo1.get_center() * 0.7).shift(
            klein_origin + 1.5 * RIGHT)
        k_geo1_copy = k_geo1.copy()

        self.add(title, poincare_text, poincare_model, klein_text, klein_model)

        self.add_subcaption(
            "Nun betrachten wir das Klein-Modell. Wir werden starke Ähnlichkeiten zum Poincare-Modell erkennen.",
            duration=7)

        self.wait(4)

        self.add(kcircle)
        self.play(self.camera.frame.animate.scale(0.8).move_to(np.add(klein_origin, [0, 0.4, 0])),
                  FadeOut(poincare_model), FadeOut(poincare_text), FadeOut(klein_model))

        self.wait(2)

        self.add_subcaption(
            "Der größte Unterschied ist, dass Geodätische hier tatsächlich euklidischen Geraden entsprechen.",
            duration=6)

        self.play(Create(k_geodesics[0]))
        self.play(Create(k_geodesics[1]))
        self.play(Create(k_geodesics[2]))
        self.play(Create(k_geodesics[3]))

        self.wait(2)

        self.play(Uncreate(k_geodesics[1]), Uncreate(k_geodesics[2]), Uncreate(k_geodesics[3]), Create(k_point),
                  Write(k_point_text))

        self.add_subcaption(
            "Da diese aber wie im Poincare-Modell durch den Einheitskreis beschränkt werden, "
            "gilt das Parallelenaxiom auch hier nicht.",
            duration=7)

        self.add_foreground_mobject(k_point)
        self.add_foreground_mobject(k_point_text)

        self.wait(2)

        self.play(Create(k_point_geodesics[0]))
        self.play(Create(k_point_geodesics[1]))
        self.play(Create(k_point_geodesics[2]))
        self.play(Create(k_point_geodesics[3]))
        self.play(Create(k_point_geodesics[4]))
        self.play(Create(k_point_geodesics[5]))

        self.wait(2)

        self.play(Uncreate(k_geodesics[0]),
                  Uncreate(k_point_geodesics[0]),
                  Uncreate(k_point_geodesics[1]),
                  Uncreate(k_point_geodesics[2]),
                  Uncreate(k_point_geodesics[3]),
                  Uncreate(k_point_geodesics[4]),
                  Uncreate(k_point_geodesics[5]),
                  Uncreate(k_point), Unwrite(k_point_text))

        self.add_subcaption("Ebenso gibt es im Klein-Modell eine starke Verzerrung des Raumes", duration=4)

        self.wait(3)

        self.play(FadeIn(klein_model), FadeOut(kcircle))

        self.add_subcaption("Hier sehen wir die gleiche Parkettierung "
                            "der hyperbolischen Ebene im Klein-Modell.",
                            duration=6)

        self.play(Create(kpoints1[0]),
                  Create(kpoints1[1]),
                  Create(kpoints1[2]))
        self.play(Create(raw_ktri1), run_time=2)
        self.play(Write(ktri1_text))

        self.wait(1)

        self.play(Create(kpoints2[0]),
                  Create(kpoints2[1]),
                  Create(kpoints2[2]))
        self.play(Create(raw_ktri2), run_time=2)
        self.play(Write(ktri2_text))

        self.wait(1)

        self.add_subcaption("Zum Rand hin werden Distanzen auch hier immer größer", duration=4)

        self.play(Write(ktri_size_text), run_time=2)

        self.wait(4)

        self.play(Uncreate(raw_ktri1),
                  Uncreate(kpoints1[0]),
                  Uncreate(kpoints1[1]),
                  Uncreate(kpoints1[2]),
                  Uncreate(raw_ktri2),
                  Uncreate(kpoints2[0]),
                  Uncreate(kpoints2[1]),
                  Uncreate(kpoints2[2]),
                  Unwrite(ktri1_text), Unwrite(ktri2_text),
                  Unwrite(ktri_size_text), run_time=2)

        self.wait(2)

        self.play(self.camera.frame.animate.scale(1.25).move_to(center), FadeIn(poincare_model), FadeIn(poincare_text))

        self.add_subcaption(
            "Da beide Modelle den gleichen Raum darstellen, ist es naheliegend, dass es Abbildungen gibt, "
            "die die Punkte der Modelle miteinander identifizieren.",
            duration=8)

        self.wait(1)

        self.play(Transform(title, title2))

        self.wait(2)

        self.play(poincare_model.animate.scale(0.7).shift(1.5 * LEFT),
                  klein_model.animate.scale(0.7).shift(1.5 * RIGHT),
                  poincare_text.animate.shift(1.5 * LEFT + .5 * DOWN),
                  klein_text.animate.shift(1.5 * RIGHT + .5 * DOWN))

        self.add(pcircle.scale(0.7).shift(1.5 * LEFT), kcircle.scale(0.7).shift(1.5 * RIGHT))

        self.wait(3)

        self.add_subcaption("Tatsächlich gibt es diese, wir nennen sie f und f^-1. ", duration=4)

        self.play(Write(arrow_group))

        self.wait(3)

        self.play(Write(f_text), Write(f_inv_text))

        self.add_subcaption("Wie wir hier sehen, sind die Formeln für diese Abbildungen ziemlich einfach.", duration=4)

        self.wait(2)

        self.play(Write(f_formula))

        self.wait(1)

        self.play(Write(f_inv_formula))

        self.wait(5)

        self.add_subcaption(
            "Mit f und f^-1 können wir jetzt Objekte aus "
            "dem einen Modell ins andere übertragen. Insbesondere Geodätische.",
            duration=7)

        self.play(Create(p_geo0), FadeOut(poincare_model))
        self.add(p_geo0_copy)

        self.wait(2)

        self.play(Transform(p_geo0, k_geo0), FadeOut(klein_model), Indicate(f_text))

        self.wait(1)

        self.play(Create(k_geo1))
        self.add(k_geo1_copy)

        self.wait(1)

        self.play(Transform(k_geo1, p_geo1), Indicate(f_inv_text))

        self.add_subcaption(
            "Da die Abbildungen punktweise agieren, "
            "bleiben Schnittpunkte zwischen Geodätischen erhalten.",
            duration=6)

        self.wait(6)

        self.add_subcaption("Das liefert uns jetzt die folgende Umformulierung des Sieben-Kreise-Satzes.", duration=4)

        everything = VGroup(*filter(lambda x: isinstance(x, VMobject), self.mobjects))

        self.wait(3)

        endDot = Dot(color=BLACK)
        self.play(Transform(everything, endDot))
        self.wait(3)


class SevenCirclesHyperbolic(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 9

        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        title = Text("Der hyperbolische Sieben-Kreise-Satz").scale(0.8)

        theorem_text_colored = Tex(r"Sei $C_0\ $ein Kreis ", r"und $C_1, \ldots, C_6$ in $C_0$ enthaltene Kreise, ",
                                   "sodass jeder innere Kreis zu $C_0$ tangential ist ",
                                   "und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind. ",
                                   "Dann treffen sich die drei hyperbolischen Diagonalen des hyperbolischen Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird, ",
                                   "in einem Punkt.", "",
                                   substrings_to_isolate=[r"$C_0\ $", r"$C_1, \ldots, C_6$", "zu $C_0$ tangential",
                                                          "nebeneinanderliegende innere Kreise ebenfalls zueinander tangential",
                                                          "hyperbolischen Diagonalen", "hyperbolischen Hexagons",
                                                          "Punkt"],
                                   stroke_width=.05).set_color_by_tex(r"$C_0\ $",
                                                                      OUTER_CIRCLE_COLOR).set_color_by_tex(
            r"$C_1, \ldots, C_6$",
            INNER_CIRCLE_COLOR).set_color_by_tex(
            "zu $C_0$ tangential",
            OUTER_INTERSECTION_COLOR).set_color_by_tex(
            "nebeneinanderliegende innere Kreise ebenfalls zueinander tangential",
            INNER_INTERSECTION_COLOR).set_color_by_tex(
            "hyperbolischen Diagonalen", DIAGONAL_COLOR).set_color_by_tex(
            "hyperbolischen Hexagons", HEXAGON_COLOR).set_color_by_tex("Punkt", DIAGONAL_INTERSECTION_COLOR).scale(
            0.5).move_to([0, -2, 0])

        theorem_text_white = Tex(r"Sei $C_0\ $ein Kreis ", r"und $C_1, \ldots, C_6$ in $C_0$ enthaltene Kreise, ",
                                 "sodass jeder innere Kreis zu $C_0$ tangential ist ",
                                 "und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind. ",
                                 "Dann treffen sich die drei hyperbolischen Diagonalen des hyperbolischen Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird, ",
                                 "in einem Punkt.", "",
                                 stroke_width=.05).scale(
            0.5).move_to([0, -2, 0])

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=2)
        phis = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))
        # phis = create_phis(min_dist=.9, max_dist=1.2)
        first_circle_radius = .4

        hexagon = HyperbolicPolygon([polar_to_point(phi) for phi in phis], color=HEXAGON_COLOR,
                                    dot_color=OUTER_INTERSECTION_COLOR, stroke_width=2)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
        inner_intersections = get_intersections_of_n_tangent_circles(hexagon_circles.circles,
                                                                     color=INNER_INTERSECTION_COLOR)
        outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles,
                                                                            color=OUTER_INTERSECTION_COLOR)
        diagonals = HexagonMainDiagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
        diagonal_intersection = Dot(
            tf_klein_to_poincare(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4])),
            color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

        eucl_hexagon = EuclideanHexagon(phis, color=HEXAGON_COLOR, stroke_width=2)
        eucl_diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
        eucl_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

        self.camera.frame.shift(0.8 * DOWN)
        self.play(Write(title.shift(1.4 * UP).scale(.7)))

        self.wait(2)

        self.add_subcaption("Sei C_0 ein Kreis", duration=2)

        self.play(Write(theorem_text_white[0], run_time=2))

        self.play(FadeIn(circle), FadeIn(theorem_text_colored[1]))
        self.add_foreground_mobject(circle)

        self.add_subcaption("und C_1,...,C_6 in C_0 enthaltene Kreise", duration=4)

        self.play(Write(theorem_text_white[1], run_time=3))

        self.play(Create(hexagon_circles, run_time=4), FadeIn(theorem_text_colored[4], run_time=1))
        self.remove_foreground_mobjects(circle)

        self.add_subcaption("sodass jeder innere Kreis zum äußeren Kreis tangential ist", duration=5)

        self.play(Write(theorem_text_white[2], run_time=3))
        self.play(FadeIn(theorem_text_colored[7]))

        self.play(Create(outer_intersections[0]),
                  Create(outer_intersections[1]),
                  Create(outer_intersections[2]),
                  Create(outer_intersections[3]),
                  Create(outer_intersections[4]),
                  Create(outer_intersections[5]),
                  run_time=1)

        self.add_foreground_mobjects(*outer_intersections)

        self.add_subcaption("und je zwei nebeneinanderliegende innere Kreise ebenfalls zueinander tangential sind.",
                            duration=7)

        self.play(Write(theorem_text_white[3]), run_time=6)
        self.play(FadeIn(theorem_text_colored[10]))

        self.play(Create(inner_intersections[0]),
                  Create(inner_intersections[1]),
                  Create(inner_intersections[2]),
                  Create(inner_intersections[3]),
                  Create(inner_intersections[4]),
                  Create(inner_intersections[5]),
                  run_time=1)

        for i in range(6):
            self.add_foreground_mobject(inner_intersections[i])

        self.add_subcaption(
            "Dann treffen sich die drei hyperbolischen Diagonalen des hyperbolischen Hexagons, das von den Schnittpunkten der inneren Kreise mit dem äußeren Kreis gebildet wird,",
            duration=10)

        self.play(Write(theorem_text_white[4]), run_time=8)

        self.play(Create(hexagon, run_time=5), FadeIn(theorem_text_colored[15], run_time=1))
        self.play(FadeIn(theorem_text_colored[13]))
        for x in diagonals:
            self.play(Create(x), run_time=1)

        self.add_subcaption("in einem Punkt", duration=3)

        self.play(Write(theorem_text_white[5]), run_time=3)

        self.play(FadeIn(theorem_text_colored[18], run_time=1))

        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))

        self.add_subcaption(
            "Wenn wir diesen Satz bewiesen haben, wenden wir einfach die Transformation vom Poincare- zum Klein-Modell an",
            duration=6)

        self.wait(3)

        self.play(*[ReplacementTransform(hexagon.arcs[i], eucl_hexagon.edges[i]) for i in range(6)],
                  ReplacementTransform(diagonals.arc1, eucl_diagonals[0].reverse_direction()),
                  ReplacementTransform(diagonals.arc2, eucl_diagonals[1].reverse_direction()),
                  ReplacementTransform(diagonals.arc3, eucl_diagonals[2].reverse_direction()),
                  ReplacementTransform(diagonal_intersection, eucl_intersection),
                  # turn uninteresting parts dark
                  run_time=3)

        self.add_subcaption("und haben somit auch den ursprünglichen Satz bewiesen.", duration=4)

        self.wait(4)

        everything = VGroup()
        for mob in self.mobjects:
            if isinstance(mob, VMobject):
                everything.add(mob)

        endDot = Dot(color=BLACK)
        self.add(endDot)
        self.play(Transform(everything, endDot), run_time=2)
        self.wait(2)
