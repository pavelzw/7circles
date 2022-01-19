from manim import Create, Circle, MovingCameraScene, BLUE, Tex, Write, FadeOut, WHITE, FadeIn, YELLOW, GREEN, Uncreate, \
    UP, RED, VGroup, LEFT, DOWN, Dot, RIGHT, TransformFromCopy, Transform, Flash, MathTex, ReplacementTransform, \
    ApplyWave, PURPLE
from manim.utils import rate_functions

from geometry_util import polar_to_point, get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon import HexagonMainDiagonals, IntersectionTriangle
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = [5,  # hexagon
                   6,  # diagonals
                   2,  # triangle
                   5,  # wait
                   6,  # colored_hexagon
                   10,  # proposition
                   5,  # wait
                   ]
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.add_foreground_mobjects(circle)
        self.play(Create(circle))

        # phis = create_phis_non_intersecting()
        # phis = HexagonAngles(np.array([1.80224806, 2.30601184, 2.77326535, 3.20993453, 4.48582486, 6.15595698]))
        phis = [1.80224806, 2.30601184, 2.77326535, 3.20993453, 4.48582486, 6.15595698]
        print(f'Phis = {phis}')
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=2)
        hexagon_label = MathTex('P', font_size=15).move_to([-.05, .8, 0])
        print(hexagon.phis)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)

        self.play(Create(hexagon),
                  run_time=timings.pop(),
                  subcaption="Betrachten wir nun einmal ein ideales Hexagon.")
        self.play(Write(hexagon_label))
        self.play(Create(diagonals),
                  run_time=timings.pop(),
                  subcaption="Wenn wir bei diesem Hexagon nun die "
                             "gegenüberliegenden Seiten verbinden, sehen wir,")

        triangle = IntersectionTriangle(diagonals, color=GREEN, add_dots=False, stroke_width=2)
        triangle_label = MathTex('T_P', color=GREEN, font_size=15).move_to([-.2, .25, 0])
        self.play(Create(triangle), Write(triangle_label),
                  run_time=timings.pop(),
                  subcaption="dass ein Dreieck in der Mitte entsteht.")
        self.play(Flash(triangle, color=GREEN, line_stroke_width=2))

        self.wait(timings.pop())

        self.play(self.camera.frame.animate.set(width=4).move_to([.8, 0, 0]))

        hexagon_colored = HyperbolicPolygon.from_polar(phis, color=[RED, BLUE, RED, BLUE, RED, BLUE],
                                                       add_dots=False, stroke_width=2)
        self.add_subcaption("Wir zeigen nun den folgenden Satz: Für jedes ideale Hexagon gilt, dass der "
                            "alternierende Umfang bis auf das Vorzeichen genau zweimal dem Umfang von "
                            "dem Dreieck T_P entspricht", duration=10)
        self.play(Create(hexagon_colored), run_time=timings.pop())
        self.remove(hexagon)

        proposition = Tex(r'Für jedes ideale Hexagon $P$ gilt:', font_size=11).move_to([1.9, .1, 0])
        formula = altper, equal, per = VGroup(MathTex(r'\mathrm{altPer}(P)', font_size=11),
                                              MathTex(r'= \pm 2 \cdot ', font_size=11),
                                              MathTex(r'\mathrm{Per}(T_P)', font_size=11)).arrange(buff=.05)
        formula.next_to(proposition, .5 * DOWN)
        self.play(Write(proposition))
        self.play(TransformFromCopy(VGroup(*hexagon_colored.arcs), altper))
        self.play(Write(equal), TransformFromCopy(triangle, per))

        self.wait(timings.pop())


def get_y_g_triangles(hexagon: HyperbolicPolygon, color_y=YELLOW, color_g=GREEN):
    diagonals = HexagonMainDiagonals(hexagon)
    c1, r1 = diagonals.arc1.circle_center, diagonals.arc1.radius
    c2, r2 = diagonals.arc2.circle_center, diagonals.arc2.radius
    c3, r3 = diagonals.arc3.circle_center, diagonals.arc3.radius
    intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(c2, r2, c3, r3)
    intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c3, r3)
    intersection3 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c2, r2)

    # y triangles
    y1 = HyperbolicPolygon([hexagon.polygon_points[5], hexagon.polygon_points[0], intersection2],
                           add_dots=False, color=color_y)
    y2 = HyperbolicPolygon([hexagon.polygon_points[1], hexagon.polygon_points[2], intersection1],
                           add_dots=False, color=color_y)
    y3 = HyperbolicPolygon([hexagon.polygon_points[3], hexagon.polygon_points[4], intersection3],
                           add_dots=False, color=color_y)

    # g triangles
    g1 = HyperbolicPolygon([hexagon.polygon_points[2], hexagon.polygon_points[3], intersection2],
                           add_dots=False, color=color_g)
    g2 = HyperbolicPolygon([hexagon.polygon_points[4], hexagon.polygon_points[5], intersection1],
                           add_dots=False, color=color_g)
    g3 = HyperbolicPolygon([hexagon.polygon_points[0], hexagon.polygon_points[1], intersection3],
                           add_dots=False, color=color_g)
    return y1, y2, y3, g1, g2, g3


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.play(Create(circle))

        p1 = polar_to_point(.2)
        p2 = polar_to_point(.8)
        p3 = polar_to_point(0.7) * 0.3
        print(p1, p2, p3)

        triangle = HyperbolicPolygon([p1, p2, p3], color=[BLUE, WHITE, WHITE], stroke_width=2)
        triangle.dots[0].set_color(BLUE)
        triangle.dots[1].set_color(BLUE)
        self.add_foreground_mobjects(triangle.arcs[0], triangle.dots[0], triangle.dots[1])

        self.play(Create(triangle, run_time=3), subcaption="Ein semiideales Dreieck ist ein hyperbolisches Dreieck "
                                                           "mit zwei idealen Knoten, also am Rand des Kreises, "
                                                           "und einem Knoten in der hyperbolischen Ebene.")

        self.play(FadeOut(triangle))
        self.clear()
        self.add(circle)
        self.add_foreground_mobject(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=2)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)

        self.play(FadeIn(hexagon, diagonals), self.camera.frame.animate.set(width=4),
                  subcaption="In unserem idealen Sechseck gibt es drei semiideale Dreiecke")

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon)
        y1_label = MathTex('Y_1', font_size=15).move_to([.5, 0, 0])
        y2_label = MathTex('Y_2', font_size=15).move_to([-.2, .55, 0])
        y3_label = MathTex('Y_3', font_size=15).move_to([-.35, -.25, 0])
        g1_label = MathTex('G_1', font_size=15).move_to([-.3, .15, 0])
        g2_label = MathTex('G_2', font_size=15).move_to([.1, -.2, 0])
        g3_label = MathTex('G_3', font_size=15).move_to([.2, .25, 0])
        self.play(FadeIn(y1), Write(y1_label), subcaption="Y1, ")
        self.play(FadeOut(y1), FadeIn(y2), Write(y2_label), subcaption="Y2 ")
        self.play(FadeOut(y2), FadeIn(y3), Write(y3_label), subcaption="sowie Y3.")
        self.play(FadeOut(y3))

        self.add_subcaption("Auf den jeweils gegenüberliegenden Seiten gibt es "
                            "außerdem noch drei weitere semiideale Dreiecke, welche das innere Dreieck T_P schneiden.",
                            duration=3)
        self.wait(3)
        self.play(FadeIn(g1), Write(g1_label), subcaption="Die nennen wir G1, ")
        self.play(FadeOut(g1), FadeIn(g2), Write(g2_label), subcaption="G2 ")
        self.play(FadeOut(g2), FadeIn(g3), Write(g3_label), subcaption="sowie G3.")
        self.play(FadeOut(g3))

        self.wait(5)


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.add_foreground_mobject(circle)
        self.add(circle)

        p1 = polar_to_point(.2)
        p2 = polar_to_point(2.1)
        p3 = polar_to_point(5) * 0.3
        print(p1, p2, p3)
        triangle = HyperbolicPolygon([p1, p2, p3], add_dots=False)
        self.play(Create(triangle), subcaption="Wir definieren uns eine ähnliche Größe wie den alternierenden Umfang "
                                               "für hyperbolische Dreiecke.")

        circle1_radius = .2
        circle1_center = (1 - circle1_radius) * p1
        circle2_radius = .15
        circle2_center = (1 - circle2_radius) * p2
        circle1 = Circle(radius=circle1_radius, color=GREEN, fill_opacity=.5).move_to(circle1_center)
        circle2 = Circle(radius=circle2_radius, color=GREEN, fill_opacity=.5).move_to(circle2_center)
        self.add_foreground_mobjects(circle1, circle2)
        self.play(Create(circle1), Create(circle2),
                  subcaption="Wenn wir disjunkte Horodisks von den beiden idealen Knoten des Dreiecks entfernen, ")

        # L1'
        arc = triangle.arcs[1]
        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                              arc.circle_center, arc.radius)
        l1_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE)
        l1_prime_label = Tex("$L_1'$", color=BLUE, font_size=20).move_to([-.3, .1, 0])
        self.play(Create(l1_prime), Write(l1_prime_label), subcaption="erhalten wir die Längen L_1',")

        # L2'
        arc = triangle.arcs[2]
        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(circle1_center, circle1_radius,
                                                                              arc.circle_center, arc.radius)
        l2_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE)
        l2_prime_label = Tex("$L_2'$", color=BLUE, font_size=20).move_to([.4, -.25, 0])
        self.play(Create(l2_prime), Write(l2_prime_label), subcaption="L_2'")

        # L3' is on the connection between the ideal points
        arc = triangle.arcs[0]
        intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(circle1_center, circle1_radius,
                                                                               arc.circle_center, arc.radius)
        intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                               arc.circle_center, arc.radius)
        l3_prime = HyperbolicArcBetweenPoints(intersection1, intersection2, color=RED)
        l3_prime_label = Tex("$L_3'$", color=RED, font_size=20).move_to([.2, .55, 0])
        self.play(Create(l3_prime), Write(l3_prime_label),
                  subcaption="Und L_3' als Verbindung zwischen den idealen Punkten.")

        # können wir uns die Größe A(V) definieren.

        formula0, formula1, plus, formula2, minus, formula3 = formula = VGroup(Tex("$A(V) = $", font_size=15),
                                                                               Tex("$L_1'$", color=BLUE, font_size=15),
                                                                               Tex("$+$", font_size=15),
                                                                               Tex("$L_2'$", color=BLUE, font_size=15),
                                                                               Tex("$-$", font_size=15),
                                                                               Tex("$L_3'$", color=RED, font_size=15))
        # todo align by center in VGroup?
        formula.move_to([0, -1.4, 0])
        formula.arrange(buff=.05, center=False)
        self.add_subcaption("Jetzt können wir uns den alternierenden Umfang eines semiidealen Dreiecks definieren, "
                            "indem wir die beiden blauen Längen aufeinander addieren und die rote abziehen.",
                            duration=4)
        self.play(Write(formula0))
        self.play(TransformFromCopy(l1_prime_label, formula1))
        self.play(Write(plus), TransformFromCopy(l2_prime_label, formula2))
        self.play(Write(minus), TransformFromCopy(l3_prime_label, formula3))

        # todo insert alternating perimeter image?

        # change small circle radius
        step_size_one_direction = 10
        # forward and back
        circle1_radii_transition = [circle1_radius * (
                1 - t / step_size_one_direction) + .1 * t / step_size_one_direction for t in
                                    range(step_size_one_direction)] + [
                                       circle1_radius * t / step_size_one_direction + .1 * (
                                               1 - t / step_size_one_direction) for t
                                       in range(step_size_one_direction + 1)]
        print(circle1_radii_transition)
        num_steps = 2 * step_size_one_direction + 1

        self.add_subcaption("A(V) hängt auch nicht von der Größe der einzelnen Kreise ab, da jeweils das gleiche "
                            "dazuaddiert wird, was auch abgezogen wird.", duration=3)
        for t in range(num_steps):
            radius = circle1_radii_transition[t]
            center = triangle.polygon_points[0] * (1 - radius)
            new_circle = Circle(radius, color=GREEN, fill_opacity=.5) \
                .move_to(center)

            # L3'
            arc = triangle.arcs[0]
            intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(center, radius,
                                                                                   arc.circle_center, arc.radius)
            intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                                   arc.circle_center, arc.radius)
            new_l3_prime = HyperbolicArcBetweenPoints(intersection1, intersection2, color=RED)

            # L2'
            arc = triangle.arcs[2]
            intersection = get_intersection_in_unit_circle_of_two_tangent_circles(center, radius,
                                                                                  arc.circle_center, arc.radius)
            new_l2_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE)

            # total runtime 2 seconds
            self.play(Transform(circle1, new_circle), Transform(l2_prime, new_l2_prime),
                      Transform(l3_prime, new_l3_prime), rate_func=lambda a: a, run_time=3 / num_steps)
        self.wait(5)


class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.add_foreground_mobject(circle)
        self.add(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=2)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)
        self.add(hexagon, diagonals)

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon)
        dot1 = Dot(y1.polygon_points[2], radius=.04)
        dot2 = Dot(y2.polygon_points[2], radius=.04)
        dot3 = Dot(y3.polygon_points[2], radius=.04)

        self.add_subcaption("Die Dreiecke G_k und Y_k teilen sich jeweils genau einen Knoten "
                            "für k = 1, 2, 3.", duration=4)
        self.play(FadeIn(y1, g1, dot1))
        self.play(Flash(dot1, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y1, g1, dot1), FadeIn(y2, g2, dot2))
        self.play(Flash(dot2, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y2, g2, dot2), FadeIn(y3, g3, dot3))
        self.play(Flash(dot3, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y3, g3, dot3))

        self.add_subcaption("Es gibt jeweils eine Isometrie I_k, die die gegenüberliegende Dreiecke "
                            "aufeinander abbildet. Also I_k(Y_k) = G_k.", duration=3)
        self.play(FadeIn(y1))
        self.play(ReplacementTransform(y1, g1))
        self.play(FadeOut(g1))

        # todo explain why the isometry is there

        self.wait(5)


class Scene5(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        formula = MathTex("A(Y_k) = A(G_k)")
        self.wait(.5)
        self.play(Write(formula), subcaption="Da wir eine Isometrie zwischen den beiden "
                                             "Dreiecken haben, sind die Umfänge der Dreiecke gleich, "
                                             "es gilt also A(Y_k) = A(G_k).")
        self.wait(5)
        formula1, formula2, formula3 = VGroup(MathTex("A(Y_1) = A(G_1)"),
                                              MathTex("A(Y_2) = A(G_2)"),
                                              MathTex("A(Y_3) = A(G_3)")).arrange(DOWN)

        self.play(TransformFromCopy(formula, formula1), TransformFromCopy(formula, formula2),
                  TransformFromCopy(formula, formula3), FadeOut(formula),
                  subcaption="Diese Formeln können wir explizit für alle drei Dreieckspaare aufschreiben.")
        self.wait(2)

        formula1_transformed, formula2_transformed, formula3_transformed = formulas_transformed = VGroup(
            MathTex("A(Y_1) - A(G_1) = 0"),
            MathTex("A(Y_2) - A(G_2) = 0"),
            MathTex("A(Y_3) - A(G_3) = 0")).arrange(DOWN)

        self.play(ReplacementTransform(formula1, formula1_transformed),
                  ReplacementTransform(formula2, formula2_transformed),
                  ReplacementTransform(formula3, formula3_transformed),
                  subcaption="Und das A(G_k) auf die andere Seite bringen.")
        self.wait(2)

        formula_combined = MathTex("A(Y_1) + A(Y_2) + A(Y_3) - (A(G_1) + A(G_2) + A(G_3)) = 0", font_size=20)

        self.play(ReplacementTransform(formulas_transformed, formula_combined),
                  subcaption="Nun können wir alle Formeln zusammenaddieren und erhalten diese Formel hier.")
        self.wait(5)


class Scene6(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        self.camera.frame.move_to([.8, 0, 0])
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.add_foreground_mobject(circle)
        self.add(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=2)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)
        self.add(hexagon, diagonals)

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon, BLUE, RED)
        intersecting_triangle = IntersectionTriangle(diagonals, color=RED)
        intersecting_triangle2 = IntersectionTriangle(diagonals, color=PURPLE)

        formula = MathTex('0 &=', 'A(Y_1)', '+', 'A(Y_2)', '+', 'A(Y_3)', r'\\',
                          '&-(', 'A(G_1)', '+', 'A(G_2)', '+', 'A(G_3)', ')', font_size=17).move_to([1.25, .5, 0],
                                                                                                    aligned_edge=LEFT)

        self.add(formula)

        self.add_subcaption("Nun zählen wir mal zusammen, was alles herauskommt, wenn wir "
                            "die Längen aufeinander addieren und voneinander abziehen.",
                            duration=10)
        # A(Y_1)
        self.play(formula[1].animate.set_color(BLUE), ApplyWave(formula[1], amplitude=.1))
        self.play(Create(y1), run_time=3)
        # A(Y_2)
        self.play(formula[3].animate.set_color(BLUE), ApplyWave(formula[3], amplitude=.1))
        self.play(Create(y2), run_time=3)
        # A(Y_3)
        self.play(formula[5].animate.set_color(BLUE), ApplyWave(formula[5], amplitude=.1))
        self.play(Create(y3), run_time=3)

        # todo make animations smoother using rate_functions (ease_in, ease_out)
        # A(G_1)
        self.add_subcaption("Wenn wir den Umfang der G Dreiecke abziehen, kürzt sich ein Teil mit dem "
                            "Umfang der Y Dreiecke weg.")
        self.play(formula[8].animate.set_color(RED), ApplyWave(formula[8], amplitude=.1))
        self.play(Create(g1.arcs[0]))
        self.play(Uncreate(y3.arcs[2]))
        self.play(Create(intersecting_triangle.arcs[1].reverse_direction()))
        self.play(Create(intersecting_triangle.arcs[0].reverse_direction()), rate_func=rate_functions.ease_out_cubic)
        self.play(Uncreate(y2.arcs[1]))

        # A(G_2)
        self.play(formula[10].animate.set_color(RED), ApplyWave(formula[10], amplitude=.1))
        self.play(Create(g2.arcs[0]))
        self.play(Uncreate(y1.arcs[2]))
        self.play(Create(intersecting_triangle2.arcs[0].reverse_direction()))
        self.play(Create(intersecting_triangle.arcs[2].reverse_direction()))
        self.play(Uncreate(y3.arcs[1]))

        # A(G_3)
        self.play(formula[12].animate.set_color(RED), ApplyWave(formula[12], amplitude=.1))
        self.play(Create(g3.arcs[0]))
        self.play(Uncreate(y2.arcs[2]))
        self.play(Create(intersecting_triangle2.arcs[2].reverse_direction()))
        self.play(Create(intersecting_triangle2.arcs[1].reverse_direction()))
        self.play(Uncreate(y1.arcs[1]))

        self.add_subcaption("Wir sehen, dass wir also insgesamt zweimal den Umfang des inneren Dreiecks "
                            "aufsummiert haben sowie den alternierenden Umfang des Hexagons.", duration=5)
        self.wait(5)

        formula2 = MathTex(r'\mathrm{altPer}(P) \mp 2 \cdot \mathrm{Per}(T_P) = 0', font_size=17) \
            .next_to(formula, DOWN)
        self.play(TransformFromCopy(formula, formula2))
        self.wait(3)

        self.add_subcaption("Und so kommen wir auf die Behauptung, die wir zeigen wollten.")
        formula3 = MathTex(r'\mathrm{altPer}(P) = \pm 2 \cdot \mathrm{Per}(T_P) = 0', font_size=17) \
            .next_to(formula2, DOWN)
        self.play(TransformFromCopy(formula2, formula3))

        self.wait(5)
