from typing import Union

import numpy as np
from manim import Create, Circle, MovingCameraScene, BLUE, Tex, Write, FadeOut, FadeIn, PURPLE, WHITE, YELLOW, GREEN, \
    Uncreate, RED, VGroup, LEFT, DOWN, Dot, TransformFromCopy, Transform, Flash, MathTex, ReplacementTransform, \
    ApplyWave, Group, GREY, GREEN_E, YELLOW_E, Unwrite, Square, Indicate, UP, TexTemplate, RIGHT
from manim.utils import rate_functions

from animation_constants import OUTER_CIRCLE_COLOR, HEXAGON_STROKE_WIDTH, HEXAGON_DOT_CIRCLE_RADIUS, \
    OUTER_CIRCLE_STROKE_WIDTH
from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import polar_to_point, get_intersection_in_unit_circle_of_two_tangent_circles, \
    get_intersections_of_n_tangent_circles, get_intersection_points_of_n_tangent_circles, \
    get_intersection_from_angles, mobius_transform_poincare_disk
from hexagon import HexagonMainDiagonals, IntersectionTriangle, HexagonAngles, HexagonCircles
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add_foreground_mobjects(circle)
        self.play(Create(circle))

        # phis = create_phis_non_intersecting()
        # phis = HexagonAngles(np.array([1.80224806, 2.30601184, 2.77326535, 3.20993453, 4.48582486, 6.15595698]))
        phis = [1.80224806, 2.30601184, 2.77326535, 3.20993453, 4.48582486, 6.15595698]
        print(f'Phis = {phis}')
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=HEXAGON_STROKE_WIDTH)
        hexagon_label = MathTex('P', font_size=15).move_to([-.05, .8, 0])
        print(hexagon.phis)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)

        self.play(Create(hexagon),
                  run_time=5,
                  subcaption="Betrachten wir nun ein ideales Hexagon.")
        self.play(Write(hexagon_label))
        self.play(Create(diagonals),
                  run_time=6,
                  subcaption="Wenn wir bei diesem Hexagon die "
                             "gegenüberliegenden Seiten verbinden, sehen wir,")

        triangle = IntersectionTriangle(diagonals, color=GREEN, add_dots=True, dot_radius=.01, dot_color=GREEN,
                                        stroke_width=HEXAGON_STROKE_WIDTH)
        triangle_label = MathTex('T_P', color=GREEN, font_size=15).move_to([-.2, .25, 0])
        self.play(Create(triangle), Write(triangle_label),
                  run_time=2,
                  subcaption="dass ein Dreieck in der Mitte entsteht. Nennen wir dieses Dreieck T_P.")
        self.play(Flash(triangle, color=GREEN, line_stroke_width=HEXAGON_STROKE_WIDTH))

        self.wait(5)

        self.play(self.camera.frame.animate.set(width=4).move_to([.8, 0, 0]))

        hexagon_colored = HyperbolicPolygon.from_polar(phis, color=[RED, BLUE, RED, BLUE, RED, BLUE],
                                                       add_dots=False, stroke_width=2)
        self.add_subcaption("Wir zeigen jetzt den folgenden Satz: Für jedes ideale Hexagon gilt, dass der "
                            "alternierende Umfang bis auf das Vorzeichen genau zweimal dem Umfang von "
                            "T_P entspricht.", duration=10)
        self.play(Create(hexagon_colored), run_time=6)
        self.remove(hexagon)

        proposition = Tex(r'Für jedes ideale Hexagon $P$ gilt:', font_size=11).move_to([1.9, .1, 0])
        formula = altper, equal, per = VGroup(MathTex(r'\mathrm{altPer}(P)', font_size=11),
                                              MathTex(r'= \pm 2 \cdot ', font_size=11),
                                              MathTex(r'\mathrm{Per}(T_P)', font_size=11)).arrange(buff=.05)
        formula.next_to(proposition, .5 * DOWN)
        self.play(Write(proposition))
        self.play(TransformFromCopy(VGroup(*hexagon_colored.arcs), altper))
        self.play(Write(equal), TransformFromCopy(triangle, per))

        self.wait(10)

        # transition to Scene2
        self.play(FadeOut(triangle, triangle_label, hexagon_colored, hexagon_label, diagonals, proposition, formula),
                  self.camera.frame.animate.set(width=6).move_to([0, 0, 0]))


def get_y_g_triangles(hexagon: HyperbolicPolygon,
                      color_y: Union[str, list] = YELLOW,
                      color_g: Union[str, list] = GREEN,
                      dot_color_y=None,
                      dot_color_g=None,
                      **kwargs):
    if dot_color_y is None:
        if type(color_y) == list:
            dot_color_y = color_y[-1]
        else:
            dot_color_y = color_y
    if dot_color_g is None:
        if type(color_g) == list:
            dot_color_g = color_g[-1]
        else:
            dot_color_g = color_g
    diagonals = HexagonMainDiagonals(hexagon)
    c1, r1 = diagonals.arc1.circle_center, diagonals.arc1.radius
    c2, r2 = diagonals.arc2.circle_center, diagonals.arc2.radius
    c3, r3 = diagonals.arc3.circle_center, diagonals.arc3.radius
    intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(c2, r2, c3, r3)
    intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c3, r3)
    intersection3 = get_intersection_in_unit_circle_of_two_tangent_circles(c1, r1, c2, r2)

    # y triangles
    y1 = HyperbolicPolygon([hexagon.polygon_points[5], hexagon.polygon_points[0], intersection2],
                           color=color_y, dot_color=dot_color_y, **kwargs)
    y2 = HyperbolicPolygon([hexagon.polygon_points[1], hexagon.polygon_points[2], intersection1],
                           color=color_y, dot_color=dot_color_y, **kwargs)
    y3 = HyperbolicPolygon([hexagon.polygon_points[3], hexagon.polygon_points[4], intersection3],
                           color=color_y, dot_color=dot_color_y, **kwargs)

    # g triangles
    g1 = HyperbolicPolygon([hexagon.polygon_points[2], hexagon.polygon_points[3], intersection2],
                           color=color_g, dot_color=dot_color_g, **kwargs)
    g2 = HyperbolicPolygon([hexagon.polygon_points[4], hexagon.polygon_points[5], intersection1],
                           color=color_g, dot_color=dot_color_g, **kwargs)
    g3 = HyperbolicPolygon([hexagon.polygon_points[0], hexagon.polygon_points[1], intersection3],
                           color=color_g, dot_color=dot_color_g, **kwargs)

    return y1, y2, y3, g1, g2, g3


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add(circle)
        self.add_foreground_mobjects(circle)

        p1 = polar_to_point(.2)
        p2 = polar_to_point(.8)
        p3 = polar_to_point(0.7) * 0.3
        print(p1, p2, p3)

        triangle = HyperbolicPolygon([p1, p2, p3], color=[BLUE, WHITE, WHITE], stroke_width=HEXAGON_STROKE_WIDTH,
                                     dot_radius=.04)
        triangle.dots[0].set_color(BLUE)
        triangle.dots[1].set_color(BLUE)
        triangle_dot = Dot(triangle.polygon_points[2], radius=HEXAGON_DOT_CIRCLE_RADIUS)
        self.add_subcaption("Für den Beweis definieren wir uns zuerst den Begriff des semiidealen Dreiecks. ",
                            duration=4)
        self.wait(3)
        self.play(Create(triangle.arcs[0]), run_time=1)
        self.add_subcaption("Es hat zwei Ecken am Rand des Kreises - "
                            "also ideale Punkte - sowie eine Ecke in der hyperbolischen Ebene.", duration=6)
        self.add_foreground_mobjects(triangle.arcs[0], circle)
        self.play(Create(triangle.arcs[1]), run_time=1)
        self.add(triangle_dot)
        self.play(Create(triangle.arcs[2]), run_time=1)
        self.add_foreground_mobjects(triangle.dots[0])
        self.play(Create(triangle.dots[0]))
        self.add_foreground_mobjects(triangle.dots[1])
        self.play(Create(triangle.dots[1]))
        self.wait(1.5)
        self.play(Create(triangle.dots[2]))
        self.wait(2.5)

        self.play(FadeOut(triangle, triangle_dot))
        self.clear()
        self.add(circle)
        self.add_foreground_mobject(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)

        self.add_subcaption("In unserem idealen Sechseck gibt es drei solcher Dreiecke:", duration=3)
        self.play(FadeIn(hexagon, diagonals), self.camera.frame.animate.set(width=4))
        self.wait(2)

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
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
                            "außerdem noch drei weitere semiideale Dreiecke, die das innere Dreieck T_P schneiden.",
                            duration=8)
        self.wait(8)
        self.play(FadeIn(g1), Write(g1_label), subcaption="Die nennen wir G1, ")
        self.play(FadeOut(g1), FadeIn(g2), Write(g2_label), subcaption="G2 ")
        self.play(FadeOut(g2), FadeIn(g3), Write(g3_label), subcaption="und G3.")
        self.play(FadeOut(g3))

        self.wait(3)

        # transition to Scene3
        self.play(Unwrite(y1_label), Unwrite(y2_label), Unwrite(y3_label),
                  Unwrite(g1_label), Unwrite(g2_label), Unwrite(g3_label),
                  FadeOut(hexagon, diagonals))
        self.wait(2)


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 4

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add_foreground_mobject(circle)
        self.add(circle)

        p1 = polar_to_point(.2)
        p2 = polar_to_point(2.1)
        p3 = polar_to_point(5) * 0.3
        print(p1, p2, p3)
        self.wait(1)
        triangle = HyperbolicPolygon([p1, p2, p3], stroke_width=HEXAGON_STROKE_WIDTH)
        self.add_subcaption("Wir definieren uns eine ähnliche Größe wie den alternierenden Umfang "
                            "für hyperbolische Dreiecke.", duration=4)
        triangle_label = MathTex('V', font_size=20).move_to([-.1, -.3, 0])
        self.play(Create(triangle, run_time=3), Write(triangle_label))

        # make intersection point of triangle more round
        dot = Dot(triangle.polygon_points[2], radius=HEXAGON_DOT_CIRCLE_RADIUS)
        self.add(dot)

        self.wait(3)

        circle1_radius = .2
        circle1_center = (1 - circle1_radius) * p1
        circle2_radius = .15
        circle2_center = (1 - circle2_radius) * p2
        circle1 = Circle(radius=circle1_radius, color=GREEN, fill_opacity=.5, stroke_width=HEXAGON_STROKE_WIDTH) \
            .move_to(circle1_center)
        circle2 = Circle(radius=circle2_radius, color=GREEN, fill_opacity=.5, stroke_width=HEXAGON_STROKE_WIDTH) \
            .move_to(circle2_center)
        self.add_foreground_mobjects(circle1, circle2)
        self.add_subcaption("Wenn wir disjunkte Horodisks von den beiden idealen Knoten des Dreiecks entfernen, ",
                            duration=5)
        self.play(Create(VGroup(circle1, circle2)), run_time=3)
        self.wait(2)

        # L1'
        arc = triangle.arcs[1]
        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                              arc.circle_center, arc.radius)
        l1_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE,
                                              stroke_width=HEXAGON_STROKE_WIDTH)
        l1_prime_label = Tex("$L_1'$", color=BLUE, font_size=20).move_to([-.3, .1, 0])
        self.play(Create(l1_prime), Write(l1_prime_label), subcaption="erhalten wir die Längen L_1',")
        dot.set_color(BLUE)

        # L2'
        arc = triangle.arcs[2]
        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(circle1_center, circle1_radius,
                                                                              arc.circle_center, arc.radius)
        l2_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE,
                                              stroke_width=HEXAGON_STROKE_WIDTH).reverse_direction()
        l2_prime_label = Tex("$L_2'$", color=BLUE, font_size=20).move_to([.4, -.25, 0])
        self.play(Create(l2_prime), Write(l2_prime_label), subcaption="L_2'")

        # L3' is on the connection between the ideal points
        arc = triangle.arcs[0]
        intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(circle1_center, circle1_radius,
                                                                               arc.circle_center, arc.radius)
        intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                               arc.circle_center, arc.radius)
        l3_prime = HyperbolicArcBetweenPoints(intersection1, intersection2, color=RED,
                                              stroke_width=HEXAGON_STROKE_WIDTH)
        l3_prime_label = Tex("$L_3'$", color=RED, font_size=20).move_to([.2, .55, 0])
        self.add_subcaption("und L_3'.", duration=2)
        self.play(Create(l3_prime), Write(l3_prime_label))
        self.wait(2)

        self.play(self.camera.frame.animate.set(width=4).move_to([.8, 0, 0]))

        template = TexTemplate()
        template.add_to_preamble(r"\usepackage{mathtools}")
        formula = MathTex(r'A(V) \coloneqq ', "L_1'", '+', "L_2'", '-', "L_3'", font_size=15, tex_template=template)
        formula[1].set_color(BLUE)
        formula[3].set_color(BLUE)
        formula[5].set_color(RED)
        formula.move_to([1.15, 0, 0], aligned_edge=LEFT)

        self.add_subcaption("Damit definieren wir uns den alternierenden Umfang eines semiidealen Dreiecks,",
                            duration=4)
        self.wait(1)
        self.play(Write(formula[0]), run_time=2)
        self.wait(1)
        self.add_subcaption("indem wir die beiden blauen Längen aufeinander addieren und die rote abziehen.",
                            duration=4)
        self.play(TransformFromCopy(l1_prime_label, formula[1]), run_time=1)

        self.play(Write(formula[2]), TransformFromCopy(l2_prime_label, formula[3]), run_time=1)
        self.play(Write(formula[4]), TransformFromCopy(l3_prime_label, formula[5]), run_time=1)
        self.wait(2)

        # change small circle radius
        step_size_one_direction = 10
        # forward and back
        circle1_radii_transition = [circle1_radius * (
                1 - t / step_size_one_direction) + .1 * t / step_size_one_direction
                                    for t in range(step_size_one_direction)] + [
                                       circle1_radius * t / step_size_one_direction + .1 * (
                                               1 - t / step_size_one_direction)
                                       for t in range(step_size_one_direction + 1)]
        print(circle1_radii_transition)
        num_steps = 2 * step_size_one_direction + 1

        self.add_subcaption("Der alternierende Umfang hängt nicht von der Größe der einzelnen Kreise ab, "
                            "da die gleiche Länge sowohl dazuaddiert als auch abgezogen wird.", duration=6)
        self.wait(2)
        for t in range(num_steps):
            radius = circle1_radii_transition[t]
            center = triangle.polygon_points[0] * (1 - radius)
            new_circle = Circle(radius, color=GREEN, fill_opacity=.5, stroke_width=HEXAGON_STROKE_WIDTH) \
                .move_to(center)

            # L3'
            arc = triangle.arcs[0]
            intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(center, radius,
                                                                                   arc.circle_center, arc.radius)
            intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(circle2_center, circle2_radius,
                                                                                   arc.circle_center, arc.radius)
            new_l3_prime = HyperbolicArcBetweenPoints(intersection1, intersection2, color=RED,
                                                      stroke_width=HEXAGON_STROKE_WIDTH)

            # L2'
            arc = triangle.arcs[2]
            intersection = get_intersection_in_unit_circle_of_two_tangent_circles(center, radius,
                                                                                  arc.circle_center, arc.radius)
            new_l2_prime = HyperbolicArcBetweenPoints(intersection, triangle.polygon_points[2], color=BLUE,
                                                      stroke_width=HEXAGON_STROKE_WIDTH).reverse_direction()

            # total runtime 2 seconds
            self.play(Transform(circle1, new_circle), Transform(l2_prime, new_l2_prime),
                      Transform(l3_prime, new_l3_prime), rate_func=lambda a: a, run_time=3 / num_steps)
        self.wait(5)

        # transition to Scene4
        self.play(FadeOut(formula, triangle, circle1, circle2, dot,
                          l1_prime, l1_prime_label, l2_prime, l2_prime_label, l3_prime, l3_prime_label, triangle_label),
                  self.camera.frame.animate.set(width=4).move_to([0, 0, 0]))
        self.remove(circle1, circle2)  # else they would still appear because in foreground
        self.wait(2)


class Scene4(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 4

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add_foreground_mobject(circle)
        self.add(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
        self.play(FadeIn(hexagon, diagonals))
        self.wait(2)

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
        dot1 = Dot(y1.polygon_points[2], radius=.04)
        dot2 = Dot(y2.polygon_points[2], radius=.04)
        dot3 = Dot(y3.polygon_points[2], radius=.04)

        self.add_subcaption("Die Dreiecke G_k und Y_k teilen sich jeweils genau einen Knoten "
                            "für k = 1, 2, 3.", duration=6)
        self.play(FadeIn(y1, g1, dot1))
        self.play(Flash(dot1, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y1, g1, dot1), FadeIn(y2, g2, dot2))
        self.play(Flash(dot2, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y2, g2, dot2), FadeIn(y3, g3, dot3))
        self.play(Flash(dot3, line_stroke_width=1, line_length=.1, color=WHITE))
        self.play(FadeOut(y3, g3, dot3))

        self.add_subcaption("Es gibt jeweils eine Isometrie I_k, die die gegenüberliegende Dreiecke "
                            "aufeinander abbildet.", duration=5)

        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon, GREEN, GREEN, stroke_width=HEXAGON_STROKE_WIDTH)
        isometry_label = MathTex(f"I_1", font_size=30).move_to([1.5, 0, 0])
        for i, (y, g) in enumerate(zip([y1, y2, y3], [g1, g2, g3])):
            if i == 0:
                self.play(FadeIn(y), Write(isometry_label))
            else:
                self.play(FadeIn(y),
                          Transform(isometry_label, MathTex(f"I_{i + 1}", font_size=30).move_to([1.5, 0, 0])))
            self.play(ReplacementTransform(y, g))
            self.wait(1 / 3)
            if i == 2:
                self.play(FadeOut(g), Unwrite(isometry_label))
            else:
                self.play(FadeOut(g))

        self.add_subcaption("Diese können wir uns folgendermaßen konstruieren.", duration=2)
        self.wait(2)

        self.add_subcaption("Mithilfe sogenannter Möbiustransformationen, Isometrien in "
                            "der hyperbolischen Ebene, ", duration=5)
        self.wait(5)
        # isometry explanation
        p = y1.polygon_points[2]
        zero = np.array([0, 0, 0])
        # move hexagon s. t. p is at zero
        mobius_transform = mobius_transform_poincare_disk(p, zero)
        transformed_hexagon_points = [mobius_transform(point) for point in hexagon.polygon_points]
        transformed_hexagon = HyperbolicPolygon(transformed_hexagon_points, add_dots=False,
                                                stroke_width=HEXAGON_STROKE_WIDTH)
        transformed_diagonals = HexagonMainDiagonals(transformed_hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
        dot_p = Dot(p, radius=.05, color=YELLOW)
        self.add_foreground_mobjects(dot_p)
        self.add_subcaption("können wir den Schnittpunkt der beiden Dreiecke auf den Ursprung abbilden.",
                            duration=3)
        self.play(Create(dot_p))

        self.play(dot_p.animate.move_to(mobius_transform(p)),
                  ReplacementTransform(hexagon, transformed_hexagon),
                  ReplacementTransform(diagonals, transformed_diagonals), run_time=2)
        self.wait(3)

        self.add_subcaption("Die beiden Diagonalen, die den Punkt schneiden, sind nun beides Geraden durch den "
                            "Ursprung.", duration=3)
        self.wait(1)

        self.add_foreground_mobjects(transformed_diagonals.arc1, transformed_diagonals.arc3)
        self.play(Indicate(transformed_diagonals.arc1), Indicate(transformed_diagonals.arc3))
        self.remove_foreground_mobjects(transformed_diagonals.arc1, transformed_diagonals.arc3)

        self.wait(4)
        self.add_subcaption("Deshalb können wir einfach eine Punktspiegelung am Ursprung durchführen, "
                            "sodass das rechte Dreieck auf das linke transformiert wird.", duration=7)
        triangle1 = HyperbolicPolygon([transformed_hexagon_points[-1], transformed_hexagon_points[0], zero],
                                      add_dots=False, color=YELLOW, stroke_width=HEXAGON_STROKE_WIDTH)
        triangle2 = HyperbolicPolygon([transformed_hexagon_points[2], transformed_hexagon_points[3], zero],
                                      add_dots=False, color=YELLOW, stroke_width=HEXAGON_STROKE_WIDTH)
        self.play(FadeIn(triangle1))
        self.wait(2)
        y1_label = MathTex('Y_1', font_size=15).move_to([.35, -.2, 0])
        g1_label = MathTex('G_1', font_size=15).move_to([-.4, .2, 0])
        isometry_formula1 = MathTex('I_1(Y_1) = G_1', font_size=20).move_to([1.35, 0, 0], LEFT)
        isometry_formula2 = MathTex('I_2(Y_1) = G_2', font_size=20).move_to([1.35, 0, 0], LEFT)
        isometry_formula3 = MathTex('I_3(Y_1) = G_2', font_size=20).next_to(isometry_formula2, DOWN, buff=.1)
        self.play(Write(y1_label), Write(g1_label))
        self.play(self.camera.frame.animate.set(width=6),
                  ReplacementTransform(triangle1, triangle2), Write(isometry_formula1))
        self.wait(4)

        self.add_subcaption("Das ganze geht natürlich nicht nur für das erste Dreieckspaar, sondern für alle.",
                            duration=3)
        self.wait(2)
        self.play(isometry_formula1.animate.next_to(isometry_formula2, UP, buff=.1))
        self.play(TransformFromCopy(isometry_formula1, isometry_formula2))
        self.play(TransformFromCopy(isometry_formula2, isometry_formula3))
        isometry_formula_transformed = MathTex('I_k(Y_k) = G_k', font_size=20).move_to([1.35, 0, 0], LEFT)
        self.play(ReplacementTransform(isometry_formula1, isometry_formula_transformed),
                  ReplacementTransform(isometry_formula2, isometry_formula_transformed),
                  ReplacementTransform(isometry_formula3, isometry_formula_transformed))
        self.wait(2)

        # transition to Scene5
        self.play(self.camera.frame.animate.move_to(isometry_formula_transformed.get_center()),
                  FadeOut(circle, g1_label, y1_label, transformed_hexagon, transformed_diagonals,
                          dot_p, triangle2),
                  isometry_formula_transformed.animate.set(font_size=48))
        self.remove(circle, dot_p)  # remove foreground mobjects
        self.wait(2)


class Scene5(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        isometry_formula = MathTex('I_k(Y_k) = G_k')
        formula = MathTex(r'\Rightarrow ', 'A(Y_k)', ' = ', 'A(G_k)')
        self.add(isometry_formula)
        self.add_subcaption("Da wir eine Isometrie zwischen den beiden "
                            "Dreiecken haben, sind die alternierenden Umfänge der Dreiecke gleich.", duration=6)
        self.wait(1)
        self.play(isometry_formula.animate.next_to(formula, UP))

        # shift 0.1*RIGHT to align on equals sign
        self.play(Write(formula.shift(0.1 * RIGHT)))
        self.wait(5)
        formula1, formula2, formula3 = VGroup(MathTex('A(Y_1)', ' = ', 'A(G_1)'),
                                              MathTex('A(Y_2)', ' = ', 'A(G_2)'),
                                              MathTex('A(Y_3)', ' = ', 'A(G_3)')).arrange(DOWN)

        self.add_subcaption("Diese Formeln können wir explizit für alle drei Dreieckspaare aufschreiben", duration=3)
        self.play(FadeOut(isometry_formula),
                  TransformFromCopy(formula[1], formula1[0]),
                  TransformFromCopy(formula[2], formula1[1]),
                  TransformFromCopy(formula[3], formula1[2]))
        self.play(TransformFromCopy(formula[1], formula3[0]),
                  TransformFromCopy(formula[2], formula3[1]),
                  TransformFromCopy(formula[3], formula3[2]))
        self.play(ReplacementTransform(formula[1], formula2[0]),
                  ReplacementTransform(formula[2], formula2[1]),
                  ReplacementTransform(formula[3], formula2[2]),
                  FadeOut(formula[0]))
        self.wait(2)

        formula1_transformed, formula2_transformed, formula3_transformed = VGroup(
            MathTex('A(Y_1)', ' - ', 'A(G_1)', ' = ', '0'),
            MathTex('A(Y_2)', ' - ', 'A(G_2)', ' = ', '0'),
            MathTex('A(Y_3)', ' - ', 'A(G_3)', ' = ', '0')).arrange(DOWN)

        self.add_subcaption("und den Umfang von G_k auf die andere Seite bringen.", duration=3)
        self.play(ReplacementTransform(formula1[0], formula1_transformed[0]),
                  ReplacementTransform(formula1[1], formula1_transformed[3]),
                  ReplacementTransform(formula1[2], formula1_transformed[2]),
                  Write(formula1_transformed[1]),
                  Write(formula1_transformed[4]),
                  ReplacementTransform(formula2[0], formula2_transformed[0]),
                  ReplacementTransform(formula2[1], formula2_transformed[3]),
                  ReplacementTransform(formula2[2], formula2_transformed[2]),
                  Write(formula2_transformed[1]),
                  Write(formula2_transformed[4]),
                  ReplacementTransform(formula3[0], formula3_transformed[0]),
                  ReplacementTransform(formula3[1], formula3_transformed[3]),
                  ReplacementTransform(formula3[2], formula3_transformed[2]),
                  Write(formula3_transformed[1]),
                  Write(formula3_transformed[4]))
        self.wait(3.5)

        formula_combined = MathTex('A(Y_1)', ' + ', 'A(Y_2)', ' + ', 'A(Y_3)', ' - ',
                                   '(', 'A(G_1)', ' + ', 'A(G_2)', ' + ', 'A(G_3)', ')', ' = ', '0', font_size=20)

        self.add_subcaption("Nun können wir alles zusammenaddieren und erhalten folgende Formel.", duration=4)
        # self.play(ReplacementTransform(formulas_transformed, formula_combined))
        self.play(ReplacementTransform(formula1_transformed[0], formula_combined[0]),
                  ReplacementTransform(formula2_transformed[0], formula_combined[2]),
                  ReplacementTransform(formula3_transformed[0], formula_combined[4]),
                  ReplacementTransform(formula1_transformed[2], formula_combined[7]),
                  ReplacementTransform(formula3_transformed[2], formula_combined[9]),
                  ReplacementTransform(formula2_transformed[2], formula_combined[11]),
                  FadeOut(formula1_transformed[1], formula2_transformed[1], formula3_transformed[1]),
                  ReplacementTransform(
                      VGroup(formula1_transformed[1], formula2_transformed[1], formula3_transformed[1]),
                      formula_combined[5]),
                  ReplacementTransform(
                      VGroup(formula1_transformed[3], formula2_transformed[3], formula3_transformed[3]),
                      formula_combined[13]),
                  ReplacementTransform(
                      VGroup(formula1_transformed[4], formula2_transformed[4], formula3_transformed[4]),
                      formula_combined[14]),
                  Write(formula_combined[1]), Write(formula_combined[3]),
                  Write(formula_combined[6]), Write(formula_combined[8]),
                  Write(formula_combined[10]), Write(formula_combined[12]))
        self.wait(3.5)

        # transition to Scene6
        circle = Circle(color=OUTER_CIRCLE_COLOR)
        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
        new_formula = MathTex('0 &=', 'A(Y_1)', '+', 'A(Y_2)', '+', 'A(Y_3)', r'\\',
                              '&-(', 'A(G_1)', '+', 'A(G_2)', '+', 'A(G_3)', ')', font_size=17) \
            .move_to([1.25, .5, 0], aligned_edge=LEFT)
        self.play(FadeIn(circle, hexagon, diagonals), ReplacementTransform(formula_combined, new_formula),

                  self.camera.frame.animate.move_to([.8, 0, 0]))

        self.wait(3)


class Scene6(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        self.camera.frame.move_to([.8, 0, 0])

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add_foreground_mobject(circle)
        self.add(circle)

        phis = [.3, 1.6, 2.2, 3.4, 4.3, 5.9]
        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)
        self.add(hexagon, diagonals)

        y1_label = MathTex('Y_1', font_size=15).move_to([.5, 0, 0])
        y2_label = MathTex('Y_2', font_size=15).move_to([-.2, .55, 0])
        y3_label = MathTex('Y_3', font_size=15).move_to([-.35, -.25, 0])
        g1_label = MathTex('G_1', font_size=15).move_to([-.3, .15, 0])
        g2_label = MathTex('G_2', font_size=15).move_to([.1, -.2, 0])
        g3_label = MathTex('G_3', font_size=15).move_to([.2, .25, 0])
        y1, y2, y3, g1, g2, g3 = get_y_g_triangles(hexagon, [RED, BLUE, BLUE], [BLUE, RED, RED],
                                                   stroke_width=HEXAGON_STROKE_WIDTH)
        intersecting_triangle = IntersectionTriangle(diagonals, color=RED, dot_color=RED,
                                                     stroke_width=HEXAGON_STROKE_WIDTH)
        intersecting_triangle2 = IntersectionTriangle(diagonals, color=PURPLE, dot_color=PURPLE,
                                                      stroke_width=HEXAGON_STROKE_WIDTH)

        formula1 = MathTex('0 &=', 'A(Y_1)', '+', 'A(Y_2)', '+', 'A(Y_3)', r'\\',
                           '&-(', 'A(G_1)', '+', 'A(G_2)', '+', 'A(G_3)', ')', font_size=17).move_to([1.25, .5, 0],
                                                                                                     aligned_edge=LEFT)

        self.add(formula1)

        self.add_subcaption("Was bedeutet diese Summe jetzt eigentlich? Betrachten wir das ganze im Bild.",
                            duration=4)
        self.wait(2)
        # A(Y_1)
        self.play(formula1[1].animate.set_color(BLUE), ApplyWave(formula1[1], amplitude=.05),
                  Write(y1_label))
        self.play(Create(y1), run_time=3)
        # A(Y_2)
        self.play(formula1[3].animate.set_color(BLUE), ApplyWave(formula1[3], amplitude=.05),
                  Unwrite(y1_label), Write(y2_label))
        self.play(Create(y2), run_time=3)
        # A(Y_3)
        self.play(formula1[5].animate.set_color(BLUE), ApplyWave(formula1[5], amplitude=.05),
                  Unwrite(y2_label), Write(y3_label))
        self.play(Create(y3), run_time=3)

        # todo make animations smoother using rate_functions (ease_in, ease_out)
        # A(G_1)
        self.add_subcaption("Wenn wir den Umfang der G_i abziehen, kürzt sich ein Teil mit dem "
                            "Umfang der Y_i weg.", duration=4)
        self.play(formula1[8].animate.set_color(RED), ApplyWave(formula1[8], amplitude=.05),
                  Unwrite(y3_label), Write(g1_label))
        self.play(Create(g1.arcs[0]))
        self.play(Uncreate(y3.arcs[2]))
        self.add(intersecting_triangle.dots[2])
        self.play(Create(intersecting_triangle.arcs[1].reverse_direction()))
        self.add(intersecting_triangle.dots[1])
        self.play(Create(intersecting_triangle.arcs[0].reverse_direction()), rate_func=rate_functions.ease_out_cubic)
        self.add(intersecting_triangle.dots[0])
        self.play(Uncreate(y2.arcs[1]))

        # A(G_2)
        self.play(formula1[10].animate.set_color(RED), ApplyWave(formula1[10], amplitude=.05),
                  Unwrite(g1_label), Write(g2_label))
        self.play(Create(g2.arcs[0]))
        self.play(Uncreate(y1.arcs[2]))
        self.add(intersecting_triangle2.dots[1])
        self.play(Create(intersecting_triangle2.arcs[0].reverse_direction()))
        self.add(intersecting_triangle2.dots[0])
        self.play(Create(intersecting_triangle.arcs[2].reverse_direction()))
        self.play(Uncreate(y3.arcs[1]))

        # A(G_3)
        self.play(formula1[12].animate.set_color(RED), ApplyWave(formula1[12], amplitude=.05),
                  Unwrite(g2_label), Write(g3_label))
        self.play(Create(g3.arcs[0]))
        self.play(Uncreate(y2.arcs[2]))
        self.play(Create(intersecting_triangle2.arcs[2].reverse_direction()))
        self.add(intersecting_triangle2.dots[2])
        self.play(Create(intersecting_triangle2.arcs[1].reverse_direction()))
        self.play(Uncreate(y1.arcs[1]))
        self.remove(*[intersecting_triangle.arcs[i] for i in range(3)])

        self.add_subcaption("Wir sehen, dass wir zweimal den Umfang des inneren Dreiecks "
                            "sowie den alternierenden Umfang des Hexagons aufsummiert haben.", duration=7)
        self.play(Unwrite(g3_label))
        self.wait(4)

        formula2 = MathTex(r'\mathrm{altPer}(P) - 2 \cdot \mathrm{Per}(T_P) = 0', font_size=17) \
            .next_to(formula1, DOWN)
        self.play(TransformFromCopy(formula1, formula2))
        self.wait(3)

        self.add_subcaption("Insgesamt folgt unsere Behauptung.", duration=3)
        formula3 = MathTex(r'\mathrm{altPer}(P) = 2 \cdot \mathrm{Per}(T_P)', font_size=17) \
            .next_to(formula2, DOWN)
        self.play(TransformFromCopy(formula2, formula3))

        self.wait(5)

        # transition to Scene7
        self.play(self.camera.frame.animate.move_to([0, 0, 0]),
                  FadeOut(formula1, formula2, formula3, hexagon, intersecting_triangle2,
                          diagonals, *[triangle.arcs[0] for triangle in [g1, g2, g3, y1, y2, y3]],
                          y1, y2, y3,
                          *intersecting_triangle.dots, *intersecting_triangle2.dots))
        self.wait(3)


class Scene7(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add(circle)
        self.add_foreground_mobject(circle)

        phis = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))

        hexagon = HyperbolicPolygon.from_polar(phis, color=[RED, BLUE, RED, BLUE, RED, BLUE], add_dots=False,
                                               stroke_width=HEXAGON_STROKE_WIDTH)

        self.add_subcaption("Jetzt beweisen wir endlich den Sieben-Kreise-Satz.", duration=3)
        self.wait(3)

        self.add_subcaption("Schauen wir uns hierfür ein hyperbolisches Hexagon "
                            "mit Kreisen an, die tangential zum großen Kreis liegen,", duration=5)
        self.play(Create(hexagon), run_time=4)
        inner_circles = HexagonCircles(hexagon, first_circle_radius=.4, color=GREEN, stroke_width=HEXAGON_STROKE_WIDTH)
        inner_intersections = get_intersections_of_n_tangent_circles(inner_circles.circles, color=YELLOW, radius=.03)
        # todo maybe also add
        #  outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles)
        inner_intersection_points = get_intersection_points_of_n_tangent_circles(inner_circles.circles)
        self.play(Create(inner_circles[0]), run_time=1)

        self.add_subcaption("wobei sich benachbarte Kreise in exakt einem Punkt berühren.", duration=5)
        for i in range(1, 6):
            self.play(Create(inner_circles.circles[i]), run_time=1)
            self.play(Create(inner_intersections[i - 1]), run_time=.5)
        self.play(Create(inner_intersections[-1]), run_time=.5)

        self.add_foreground_mobjects(*inner_intersections)

        self.play(self.camera.frame.animate.set(width=4).move_to([.8, 0, 0]))

        self.add_subcaption("Wenn wir nun den alternierenden Umfang dieses Hexagons betrachten, sehen wir, "
                            "dass dieser genau null ist, da sich die einzelnen Stücke in den Kreisen rauskürzen.",
                            duration=9)

        formula = MathTex(r'\mathrm{AltPer}(P)', '=', '0', '+', '0',
                          font_size=18).move_to([1.15, 0, 0], LEFT)

        self.play(Write(formula[0]))

        # create 0s from arcs and merge them all together one by one
        zero_0 = formula[2]
        plus_1 = formula[3].copy()
        zero_1 = formula[4].copy()
        plus_2 = formula[3].copy()
        zero_2 = formula[4].copy()
        plus_3 = formula[3].copy()
        zero_3 = formula[4].copy()
        plus_4 = formula[3].copy()
        zero_4 = formula[4].copy()
        plus_5 = formula[3].copy()
        zero_5 = formula[4].copy()

        arcs = self._get_half_arcs(inner_intersection_points, hexagon.polygon_points, 0, RED, BLUE)

        # arcs underneath red/blue arcs for visualization
        grey_arcs = []  # all grey arcs
        arcs_grey = self._get_half_arcs(inner_intersection_points, hexagon.polygon_points, 0, GREY, GREY)
        grey_arcs.append(arcs_grey)
        self.add(arcs_grey)
        self.add(arcs)
        self.play(Write(formula[1]), ReplacementTransform(arcs, zero_0))
        self.wait(1)

        grey_arcs.append(
            self._perform_arc_transform(plus_1, zero_1, zero_0, 1, inner_intersection_points, hexagon.polygon_points))
        grey_arcs.append(
            self._perform_arc_transform(plus_2, zero_2, zero_0, 2, inner_intersection_points, hexagon.polygon_points))
        grey_arcs.append(
            self._perform_arc_transform(plus_3, zero_3, zero_0, 3, inner_intersection_points, hexagon.polygon_points))
        grey_arcs.append(
            self._perform_arc_transform(plus_4, zero_4, zero_0, 4, inner_intersection_points, hexagon.polygon_points))
        grey_arcs.append(
            self._perform_arc_transform(plus_5, zero_5, zero_0, 5, inner_intersection_points, hexagon.polygon_points))

        self.add_subcaption(
            "Und das entspricht genau dem Umfang des Dreiecks in der Mitte aufgrund des Satzes, "
            "den wir gerade eben bewiesen haben.", duration=6)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=HEXAGON_STROKE_WIDTH)

        # replace formula with formula2 in order to animate it
        formula2 = MathTex(r'\mathrm{AltPer}(P) = 0', font_size=formula.font_size).move_to(formula.get_left(), LEFT)
        self.add(formula2)
        self.remove(formula[0], formula[1], formula[2])

        self.play(formula2.animate.set(font_size=12).move_to([1.1, 0, 0], LEFT))
        formula3 = MathTex(r'= \pm 2 \cdot \mathrm{Per}(T_P)', font_size=12).next_to(formula2, buff=.05)
        self.play(Write(formula3))
        self.wait(3)
        self.add_foreground_mobjects(*inner_circles, *inner_intersections, circle)
        self.play(Create(diagonals), run_time=3)

        self.add_subcaption("Also treffen sich die Hauptdiagonalen des Hexagons in einem Punkt.", duration=3)
        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(diagonals.arc1.circle_center,
                                                                              diagonals.arc1.radius,
                                                                              diagonals.arc2.circle_center,
                                                                              diagonals.arc2.radius)
        intersection_dot = Dot(intersection, color=YELLOW, radius=.03)

        # make original hexagon grey and remove grey arcs on top
        self.remove(*grey_arcs)
        for i in range(6):
            hexagon.arcs[i].set_color(GREY)
        # turn hexagon arcs white again
        self.play(Create(intersection_dot), *[hexagon.arcs[i].animate.set_color(WHITE) for i in range(6)])
        self.play(Flash(intersection_dot, line_stroke_width=HEXAGON_STROKE_WIDTH), FadeOut(formula2, formula3))
        self.wait(1)

        self.add_subcaption("Nun müssen wir nur noch die Transformation vom Poincaré-Modell in das Klein-Modell "
                            "durchführen.", duration=4)

        # transform hyperbolic hexagon to euclidean hexagon
        euclidean_hexagon = EuclideanHexagon(phis, stroke_width=2)
        euclidean_diagonals = get_diagonals(hexagon, stroke_width=2)
        euclidean_intersection_dot = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]), color=YELLOW,
                                         radius=.03)
        self.add_foreground_mobjects(hexagon, diagonals, *inner_circles, *inner_intersections, intersection_dot, circle)

        self.play(self.camera.frame.animate.set(width=6).move_to([0, 0, 0]))
        self.play(*[ReplacementTransform(hexagon.arcs[i], euclidean_hexagon.edges[i]) for i in range(6)],
                  ReplacementTransform(diagonals.arc1, euclidean_diagonals[0].reverse_direction()),
                  ReplacementTransform(diagonals.arc2, euclidean_diagonals[1].reverse_direction()),
                  ReplacementTransform(diagonals.arc3, euclidean_diagonals[2].reverse_direction()),
                  ReplacementTransform(intersection_dot, euclidean_intersection_dot),
                  # turn uninteresting parts dark
                  *[inner_circles[i].animate.set_color(GREEN_E) for i in range(len(inner_circles))],
                  *[inner_intersections[i].animate.set_color(YELLOW_E)
                    for i in range(len(inner_intersections))],
                  run_time=3)
        self.wait(2)
        self.add_subcaption("Die Aussage gilt auch hier, weil die Schnittpunkte der "
                            "Diagonalen weiterhin durch einen Punkt verlaufen.", duration=6)
        self.wait(6)
        self.add_subcaption("Das entspricht genau dem Szenario aus dem ursprünglichen "
                            "Sieben-Kreise-Satz, den wir somit bewiesen haben.",
                            duration=6)
        self.wait(6)
        proof_square = Square(side_length=.15, stroke_width=2).move_to([2, -1, 0], DOWN)
        self.play(Create(proof_square), run_time=2)
        self.wait(5)

    def _perform_arc_transform(self, plus, zero, zero_0, i, intersection_points, polygon_points):
        col1 = RED if i % 2 == 0 else BLUE
        col2 = BLUE if i % 2 == 0 else RED
        arcs = self._get_half_arcs(intersection_points, polygon_points, i, col1=col1, col2=col2)
        # arcs underneath red/blue arcs for visualization
        arcs_grey = self._get_half_arcs(intersection_points, polygon_points, i, col1=GREY, col2=GREY)
        self.add(arcs_grey)
        self.add(arcs)

        self.play(Write(plus), ReplacementTransform(arcs, zero))  # create 0 from arcs
        self.play(ReplacementTransform(Group(plus, zero), zero_0))  # merge 0 + 0
        self.wait(1)
        return arcs_grey

    @staticmethod
    def _get_half_arcs(intersection_points, polygon_points, i, col1, col2):
        arc1 = HyperbolicArcBetweenPoints(intersection_points[i], polygon_points[i], color=col1,
                                          stroke_width=HEXAGON_STROKE_WIDTH)
        arc2 = HyperbolicArcBetweenPoints(intersection_points[i - 1], polygon_points[i], color=col2,
                                          stroke_width=HEXAGON_STROKE_WIDTH)
        return Group(arc1, arc2)
