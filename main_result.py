from tkinter import CENTER

from manim import Create, Circle, MovingCameraScene, BLUE, Tex, Write, FadeOut, WHITE, FadeIn, YELLOW, GREEN, Uncreate, \
    UP, RED, VGroup, LEFT, DOWN, Dot, RIGHT, TransformFromCopy
from pyglet.window.mouse import MIDDLE

from geometry_util import polar_to_point, get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon import HexagonMainDiagonals, IntersectionTriangle
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = [5,  # hexagon
                   6,  # diagonals
                   2,  # triangle
                   10,  # wait
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
        print(hexagon.phis)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)

        self.play(Create(hexagon),
                  run_time=timings.pop(),
                  subcaption="Betrachten wir nun einmal ein ideales Hexagon.")
        self.play(Create(diagonals),
                  run_time=timings.pop(),
                  subcaption="Wenn wir bei diesem Hexagon nun die "
                             "gegenüberliegenden Seiten verbinden, sehen wir,")

        triangle = IntersectionTriangle(diagonals, color=BLUE, add_dots=False, stroke_width=2)
        self.play(Create(triangle),
                  run_time=timings.pop(),
                  subcaption="dass ein Dreieck in der Mitte entsteht.")

        self.wait(timings.pop())

        self.play(FadeOut(circle, triangle, hexagon, diagonals))

        self.clear()
        proposition = Tex(r'Für jedes ideale Hexagon $P$ ist der '
                          r'alternierende Umfang \\ bis auf das Vorzeichen '
                          r'genau zweimal der Umfang \\ von dem Dreieck $T_P$, '
                          r'das durch die geodätischen Diagonalen \\ aufgespannt wird.', font_size=20)
        self.play(Write(proposition,
                        run_time=timings.pop(), stroke_width=.5))

        self.wait(timings.pop())


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

        c1, r1 = diagonals.arc1.circle_center, diagonals.arc1.radius
        c2, r2 = diagonals.arc2.circle_center, diagonals.arc2.radius
        c3, r3 = diagonals.arc3.circle_center, diagonals.arc3.radius
        intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(c2, r2, c3, r3)
        intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c3, r3)
        intersection3 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c2, r2)

        # y triangles
        y1 = HyperbolicPolygon([hexagon.polygon_points[5], hexagon.polygon_points[0], intersection2],
                               add_dots=False, color=YELLOW)
        y2 = HyperbolicPolygon([hexagon.polygon_points[1], hexagon.polygon_points[2], intersection1],
                               add_dots=False, color=YELLOW)
        y3 = HyperbolicPolygon([hexagon.polygon_points[3], hexagon.polygon_points[4], intersection3],
                               add_dots=False, color=YELLOW)
        y1_label = Tex('$Y_1$', font_size=15).move_to([.5, 0, 0])
        y2_label = Tex('$Y_2$', font_size=15).move_to([-.2, .55, 0])
        y3_label = Tex('$Y_3$', font_size=15).move_to([-.35, -.25, 0])
        self.play(FadeIn(y1), Write(y1_label), subcaption="Y1, ")
        self.play(FadeOut(y1), FadeIn(y2), Write(y2_label), subcaption="Y2 ")
        self.play(FadeOut(y2), FadeIn(y3), Write(y3_label), subcaption="sowie Y3.")
        self.play(FadeOut(y3))

        # g triangles
        g1 = HyperbolicPolygon([hexagon.polygon_points[2], hexagon.polygon_points[3], intersection2],
                               add_dots=False, color=GREEN)
        g2 = HyperbolicPolygon([hexagon.polygon_points[4], hexagon.polygon_points[5], intersection1],
                               add_dots=False, color=GREEN)
        g3 = HyperbolicPolygon([hexagon.polygon_points[0], hexagon.polygon_points[1], intersection3],
                               add_dots=False, color=GREEN)
        g1_label = Tex('$G_1$', font_size=15).move_to([-.3, .15, 0])
        g2_label = Tex('$G_2$', font_size=15).move_to([.1, -.2, 0])
        g3_label = Tex('$G_3$', font_size=15).move_to([.2, .25, 0])
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

        formula0, formula1, plus1, formula2, plus2, formula3 = formula = VGroup(Tex("$A(V) = $", font_size=15),
                                                                                Tex("$L_1'$", color=BLUE, font_size=15),
                                                                                Tex("$+$", font_size=15),
                                                                                Tex("$L_2'$", color=BLUE, font_size=15),
                                                                                Tex("$+$", font_size=15),
                                                                                Tex("$L_3'$", color=RED, font_size=15))
        # todo align by center in VGroup?
        formula.move_to([0, -1.4, 0])
        formula.arrange(buff=.05, center=False)
        self.add_subcaption("Jetzt können wir uns den alternierenden Umfang eines semiidealen Dreiecks definieren, "
                            "indem wir die beiden blauen Längen aufeinander addieren und die rote abziehen.",
                            duration=4)
        self.play(Write(formula0))
        self.play(TransformFromCopy(l1_prime_label, formula1))
        self.play(Write(plus1), TransformFromCopy(l2_prime_label, formula2))
        self.play(Write(plus2), TransformFromCopy(l3_prime_label, formula3))

        # todo insert alternating perimeter image?

        # todo diese hängt nicht mehr davon ab, wie wir diese Kreise wählen, da wir jeweils dieselbe Strecke
        #      dazuaddieren und abziehen -> animiere circles größer werdend, arcs verändernd

        self.wait(5)
