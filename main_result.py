from manim import Create, Circle, MovingCameraScene, BLUE, Tex, Write, FadeOut, WHITE, FadeIn, YELLOW, GREEN

from geometry_util import polar_to_point, get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon import HexagonMainDiagonals, IntersectionTriangle
from hyperbolic_polygon import HyperbolicPolygon


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
