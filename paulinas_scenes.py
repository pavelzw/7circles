from math import pi

import numpy as np
from manim import Scene, Circle, Dot, Create, FadeIn, FadeOut, WHITE, BLUE, \
    GREEN_B, Transform, MovingCameraScene, VGroup, DecimalNumber, RIGHT, Tex, LEFT, UP, MathTex, Write, Indicate, \
    TransformFromCopy, RED, \
    DOWN, GREY_B, ORANGE, ArcBetweenPoints, GREEN_D, ORIGIN, FadeTransform

from geometry_util import polar_to_point, hyperbolic_distance_function, create_min_circle_radius, \
    get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon_util import create_phis, create_radius_transition
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Scene1(MovingCameraScene):
    def construct(self):
        # todo text stroke width
        # todo coloring
        # todo arcs stroke width
        # Labels
        s_1 = MathTex('S_1', color=BLUE, font_size=15).move_to([0, .5, 0])
        s_2 = MathTex('S_2', color=BLUE, font_size=15).move_to([-.6, .45, 0])
        s_2_red = MathTex('S_2', color=RED, font_size=15).move_to([-.6, .45, 0])
        s_3 = MathTex('S_3', color=BLUE, font_size=15).move_to([-.7, -0.1, 0])
        s_4 = MathTex('S_4', color=BLUE, font_size=15).move_to([-.1, -0.6, 0])
        s_4_red = MathTex('S_4', color=RED, font_size=15).move_to([-.1, -0.6, 0])
        s_5 = MathTex('S_5', color=BLUE, font_size=15).move_to([0.4, -.55, 0])
        s_6 = MathTex('S_6', color=BLUE, font_size=15).move_to([.6, 0, 0])
        s_6_red = MathTex('S_6', color=RED, font_size=15).move_to([.6, 0, 0])
        s_k = [s_1, s_2, s_3, s_4, s_5, s_6]
        s_k_colored = [s_1, s_2_red, s_3, s_4_red, s_5, s_6_red]
        timings = [8,  # hexagon
                   5]
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()
        formula_size = 15
        self.camera.frame.width = 9

        # showing four random non ideal hexagons and an ideal hexagon
        text_non_ideal_ideal = VGroup(Tex(r'Nicht\,Ideales\, Sechseck', font_size=20, color=BLUE, stroke_width=1),
                                      Tex(r'Ideales\, Sechseck', font_size=20, color=GREEN_B,
                                          stroke_width=1)).arrange(aligned_edge=LEFT, direction=DOWN)
        position = [[-3, 1.3, 0], [0, 1.3, 0], [3, 1.3, 0], [-3, -1.3, 0], [0, -1.3, 0], [3, -1.3, 0]]
        fixed_phis = [[.2, 1.5, 1.8, 4, 4.8, 6], [.5, 1.5, 2.4, 3.2, 4, 5], [1, 1.8, 2.5, 3.3, 3.8, 5.5],
                      [.5, 2, 2.4, 2.9, 4, 4.6, 5], [1.5, 2.4, 3.2, 4, 5, 5.5]]
        fixed_radius = [[.7, .73, .8, .7, .6, .7], [.6, .8, .9, .66, .5, .6], [.5, .6, .7, .8, .6, .6],
                        [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
        for i in range(0, 6):
            if i == 5:
                self.play(Write(text_non_ideal_ideal.move_to(position[i]), stroke_width=.5))
            else:
                # radius = np.random.uniform(0.5, 0.7, 6)
                # phis = create_phis(min_dist=0.6)
                hexagon = HyperbolicPolygon.from_polar(fixed_phis[i], fixed_radius[i], dot_radius=.01, dot_color=BLUE,
                                                       stroke_width=2,
                                                       color=BLUE)
                group = VGroup(hexagon, Circle(color=WHITE)).move_to(position[i])
                if i == 3 or i == 4:
                    hexagon = HyperbolicPolygon.from_polar(fixed_phis[i], add_dots=False, stroke_width=2, color=GREEN_B)
                    group = VGroup(hexagon, Circle(color=WHITE)).move_to(position[i])
                    self.play(FadeIn(group[1]))
                    self.add_foreground_mobjects(group[1])
                    self.play(Create(group[0]), run_time=2.5, rate_func=lambda a: a)
                else:
                    self.play(FadeIn(Circle(color=WHITE).move_to(position[i])))
                    for k in range(0, 6):
                        self.add(hexagon.dots[k])
                        self.play(Create(group[0].arcs[k]), run_time=0.4, rate_func=lambda a: a)

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

        self.camera.frame.width = 6
        circle = Circle(color=WHITE)
        self.play(Create(circle))
        # creating our nonideal hexagon
        radius = [0.5, 0.7, 0.6, 0.7, 0.5, 0.6]
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]

        hexagon = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.01, stroke_width=2)
        hex_name = MathTex('P', font_size=15).move_to([0.6, 0.4, 0])

        self.play(FadeIn(hexagon, hex_name))
        self.wait(2)

        arc = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.01, color=BLUE, stroke_width=2).arcs
        dots = hexagon.dots
        # Kantenbeschriftung
        dots[-1].set_color(BLUE)
        for i in range(0, 6):
            dots[i].set_color(BLUE)
            self.play(Create(arc[i]), Write(s_k[i], stroke_width=.5),
                      rate_func=lambda a: a, run_time=1)

        self.play(self.camera.frame.animate.set(width=6).move_to([1.5, 0, 0]))  # moves circle to left

        # Perimeter
        sum1 = per, sum_sk = VGroup(MathTex(r'\mathrm{Per}(P) = ', font_size=formula_size),
                                    MathTex("S_1", ' +', " S_2", ' + ', "S_3", ' + ', "S_4", ' + ', "S_5", ' + ', "S_6",
                                            font_size=formula_size)).arrange(
            buff=0.05).move_to([2.5, 0.2, 0])
        sum_sk[0].set_color(BLUE), sum_sk[2].set_color(BLUE), sum_sk[4].set_color(BLUE)
        sum_sk[6].set_color(BLUE), sum_sk[8].set_color(BLUE), sum_sk[10].set_color(BLUE)

        alt_sum = MathTex("S_1", '-', " S_2", '+', " S_3", '-', " S_4", '+', " S_5", '-', " S_6", font_size=15)
        alt_sum[2].set_color(RED), alt_sum[6].set_color(RED), alt_sum[10].set_color(RED)  # alternating color
        alt_sum[0].set_color(BLUE), alt_sum[4].set_color(BLUE), alt_sum[8].set_color(BLUE)
        alt_per = MathTex(r'\mathrm{AltPer}(P) =', font_size=formula_size)
        sum2 = VGroup(alt_per, alt_sum).arrange(buff=.05).next_to(sum1, .5 * DOWN, aligned_edge=LEFT)
        self.play(Write(per, stroke_width=.5))
        self.play(TransformFromCopy(VGroup(*arc, *s_k), sum_sk))
        self.wait(3)

        # Alternating Perimeter
        hexagon_bi_colored = HyperbolicPolygon.from_polar(phis, radius, dot_radius=.01, dot_color=RED, stroke_width=2,
                                                          color=[BLUE, RED, BLUE, RED, BLUE, RED])

        self.play(FadeIn(hexagon_bi_colored, s_2_red, s_4_red, s_6_red), FadeOut(*hexagon.arcs, *arc, s_2, s_4, s_6))
        red_arcs = VGroup(hexagon_bi_colored.arcs[1], hexagon_bi_colored.arcs[3], hexagon_bi_colored.arcs[5], s_2_red,
                          s_4_red, s_6_red, *hexagon_bi_colored.dots)

        self.play(Indicate(red_arcs, color=RED))
        self.wait(2)
        self.play(Write(sum2[0], stroke_width=.5))
        self.play(TransformFromCopy(VGroup(hexagon_bi_colored, *s_k_colored), sum2[1]))
        self.wait(5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], FadeIn(Circle(color=WHITE)))
        self.play(self.camera.frame.animate.move_to([0, 0, 0]))
        self.wait(1)


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        s_1 = MathTex('S_1', color=BLUE, font_size=15).move_to([0.2, .5, 0])
        s_1_yellow = MathTex('S_1', color=GREEN_D, font_size=15).move_to([0.2, .5, 0])
        s_2 = MathTex('S_2', color=RED, font_size=15).move_to([-.65, .5, 0])
        s_3 = MathTex('S_3', color=BLUE, font_size=15).move_to([-.75, -0.1, 0])
        s_4 = MathTex('S_4', color=RED, font_size=15).move_to([-.2, -0.7, 0])
        s_5 = MathTex('S_5', color=BLUE, font_size=15).move_to([0.53, -.67, 0])
        s_6 = MathTex('S_6', color=RED, font_size=15).move_to([.7, 0, 0])
        s_k = VGroup(s_1, s_2, s_3, s_4, s_5, s_6)
        radius_disks = [.5, .4]
        circle = Circle(color=WHITE)
        self.add_foreground_mobjects(circle)
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]

        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, stroke_width=2,
                                               color=[BLUE, RED, BLUE, RED, BLUE, RED])
        hexagon_grey = HyperbolicPolygon.from_polar(phis, add_dots=False, color=GREY_B, stroke_width=2)
        arc_colored = HyperbolicPolygon.from_polar(phis, add_dots=False, color=GREEN_D, stroke_width=2).arcs[0]
        self.add(circle)
        self.play(Create(hexagon, run_time=5))
        self.play(FadeIn(s_k))
        self.play(self.camera.frame.animate.move_to([1, 0, 0]))
        self.wait(1)
        self.play(FadeIn(hexagon_grey), FadeOut(s_k), FadeOut(hexagon), FadeIn(arc_colored, s_1_yellow))
        self.wait(1)

        point1 = hexagon.polygon_points[0]
        point2 = hexagon.polygon_points[1]
        arc = hexagon.arcs[0]

        distance_text = MathTex(r'\mathrm{dist_h}(a,b) =', font_size=20).move_to([1.2, 0, 0],
                                                                                 aligned_edge=LEFT)  # partially new
        infinity = MathTex(r'\infty', font_size=20).next_to(distance_text, buff=.05)
        s_0 = Dot(hexagon.polygon_points[0], radius=.02, color=GREEN_D)
        s_1 = Dot(hexagon.polygon_points[1], radius=.02, color=GREEN_D)
        a = MathTex(r'a', font_size=15, color=GREEN_D).next_to(s_0, direction=0.16 * DOWN + 0.01 * LEFT)  # new
        b = MathTex(r'b', font_size=15, color=GREEN_D).next_to(s_1, direction=0.18 * DOWN + 0.01 * LEFT)  # new
        self.play(Write(VGroup(distance_text, infinity), stroke_width=.5), FadeIn(a, b, s_0, s_1))  # partially new
        self.add_foreground_mobjects(a, b)
        self.wait(6)
        distance_number = DecimalNumber(6343.242564,
                                        num_decimal_places=2, show_ellipsis=True, group_with_commas=False,
                                        font_size=20).next_to(distance_text, buff=.05)

        self.remove(infinity)
        # self.add(distance_number, s_0, s_1)
        label = VGroup(distance_text, distance_number)
        step_size = 450
        for t in range(1, step_size):
            if t < step_size / 2:
                transition = 2 * t / step_size
            else:
                transition = (1 - t / step_size) * 2
            interp_point1 = get_intersection_in_unit_circle_of_two_tangent_circles(arc.circle_center, arc.radius,
                                                                                   point1,
                                                                                   transition * radius_disks[0])
            interp_point2 = get_intersection_in_unit_circle_of_two_tangent_circles(point2,
                                                                                   transition * radius_disks[1],
                                                                                   arc.circle_center, arc.radius)
            new_arc = ArcBetweenPoints(interp_point2, interp_point1, color=GREEN_D,
                                       radius=arc.radius, stroke_width=2).reverse_direction()
            self.remove(a, b)  # new
            self.add(a.next_to(interp_point1, direction=0.2 * DOWN + 0.05 * LEFT),
                     b.next_to(interp_point2, direction=0.2 * DOWN + 0.1 * LEFT))  # new
            distance = np.exp(
                hyperbolic_distance_function(interp_point2, interp_point1))
            distance_number.font_size = 20
            label.arrange(buff=.05)
            label.move_to([1.2, 0, 0], aligned_edge=LEFT)

            if t == step_size - 1:
                self.play(Transform(arc_colored, new_arc),
                          Transform(s_0, Dot(interp_point1, radius=.02, color=GREEN_D)),
                          Transform(s_1, Dot(interp_point2, radius=.02, color=GREEN_D)),
                          Transform(distance_number, infinity),
                          run_time=1 / 60, rate_func=lambda a: a)
            else:
                self.play(Transform(arc_colored, new_arc),
                          Transform(s_0, Dot(interp_point1, radius=.02, color=GREEN_D)),
                          Transform(s_1, Dot(interp_point2, radius=.02, color=GREEN_D)),
                          distance_number.animate.set_value(distance), run_time=1 / 60,
                          rate_func=lambda a: a)
        self.remove(s_0, s_1)
        self.play(FadeOut(a, b))
        self.wait(9)

        # transition to Scene3
        self.play(*[FadeOut(mob) for mob in self.mobjects], FadeIn(Circle(color=WHITE)))
        self.play(self.camera.frame.animate.move_to([0, 0, 0]))
        self.wait(1)


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        circle = Circle(color=WHITE)
        self.add(circle)
        p1 = MathTex(r'P_1', font_size=20).move_to(ORIGIN)
        konvergenz = MathTex(r'P_n \xrightarrow{n \rightarrow \infty}P_\infty', font_size=25).move_to([2.5, 0, 0])
        s_1 = MathTex(r'\tilde{S_1}', color=ORANGE, font_size=20).move_to([[.25, .6, 0]])
        s_2 = MathTex(r'\tilde{S_2}', color=ORANGE, font_size=20).move_to([-.65, .5, 0])
        s_3 = MathTex(r'\tilde{S_3}', color=ORANGE, font_size=20).move_to([-.8, -0.1, 0])
        s_4 = MathTex(r'\tilde{S_4}', color=ORANGE, font_size=20).move_to([-.14, -0.7, 0])
        s_5 = MathTex(r'\tilde{S_5}', color=ORANGE, font_size=20).move_to([0.53, -.6, 0])
        s_6 = MathTex(r'\tilde{S_6}', color=ORANGE, font_size=20).move_to([.7, -.1, 0])
        s_k_text = VGroup(s_1, s_2, s_3, s_4, s_5, s_6)
        radius = np.array([0.7, 0.6, .75, .56, .65, .53])
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]
        circle_radius = np.array([.2, .25, .16, .29, .18, .12])  # radius for disks

        # without disks
        step_size = 50  # normally 100, but takes long
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_radius_transition(radius=radius, step_size=step_size)
        hexagon = HyperbolicPolygon.from_polar(phis, transition[0], dot_radius=0.01, stroke_width=2)
        for k in range(0, 6):
            self.add(hexagon.dots[k])
            self.play(Create(hexagon.arcs[k]), run_time=0.85, rate_func=lambda a: a)

        self.play(Write(p1, stroke_width=.5))  # todo keep it (move somewhere else though)
        self.play(FadeOut(p1))
        self.play(self.camera.frame.animate.move_to([1.5, 0, 0]))
        self.play(Write(konvergenz, stroke_width=.5))

        for t in range(1, step_size - 1):
            hexagon_new = HyperbolicPolygon.from_polar(phis, transition[t], dot_radius=0.01, stroke_width=2)
            self.play(Transform(hexagon, hexagon_new), run_time=0.05,
                      rate_func=lambda a: a)

        hexagon_new = HyperbolicPolygon.from_polar(phis, transition[-1], dot_radius=0.01, stroke_width=2)
        self.play(Transform(hexagon, hexagon_new), run_time=0.05,
                  rate_func=lambda a: a)
        self.wait(3)

        # with disks
        self.play(FadeOut(hexagon, konvergenz))
        hex_n_ideal = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.01, stroke_width=2)
        self.play(FadeIn(hex_n_ideal), Write(p1, stroke_width=.5))
        disks = []
        for k in range(0, 6):  # creating disks
            point1 = hex_n_ideal.polygon_points[k]
            circle = Circle(arc_center=point1, radius=circle_radius[k], color=GREEN_B, fill_opacity=0.5, stroke_width=2)
            disks.append(circle)
            self.add_foreground_mobjects(circle)
            self.play(FadeIn(circle))

        dynamic_arcs = []
        for k in range(0, 6):  # creating S_k tilde
            point1 = hex_n_ideal.polygon_points[k]
            point2 = hex_n_ideal.polygon_points[(k + 1) % 6]
            arc = hex_n_ideal.arcs[k]
            intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(arc.circle_center, arc.radius,
                                                                                   point1, circle_radius[k])
            intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(point2,
                                                                                   circle_radius[(k + 1) % 6],
                                                                                   arc.circle_center, arc.radius)
            arc_new = ArcBetweenPoints(intersection2, intersection1, color=ORANGE,
                                       radius=arc.radius, stroke_width=2).reverse_direction()
            dynamic_arcs.append(arc_new)
            self.play(Create(arc_new), Write(s_k_text[k], stroke_width=.5))
            if k == 0:
                distance_text, distance_number = label = VGroup(
                    Tex(r'$\mathrm{length}(\tilde{S_1})=$', font_size=20),
                    DecimalNumber(np.exp(hyperbolic_distance_function(intersection2, intersection1)),
                                  num_decimal_places=2, show_ellipsis=True, group_with_commas=False,
                                  font_size=20)).arrange(buff=.05).move_to([2.4, 0, 0])
                self.play(Write(label, stroke_width=.5))
                self.wait(1)
                self.play(FadeOut(label))
        formula = MathTex(r'&\tilde{S_1} - \tilde{S_2} + \tilde{S_3} - \tilde{S_4} + \tilde{S_5} - \tilde{S_6} \\',
                          r'= \, &S_1 - S_2 + S_3 - S_4 + S_5 - S_6 \\',
                          r'= \, &\mathrm{AltPer}', '(P_1)',
                          font_size=20).move_to([2.6, 1, 0])
        self.play(TransformFromCopy(s_k_text, formula[0]))
        self.wait(2)
        transformed_disk = disks[0]
        transformed_arc1 = dynamic_arcs[0]
        transformed_arc2 = dynamic_arcs[5]
        # changing disk in size
        step_size_one_direction = 20
        s_k = [hex_n_ideal.polygon_points[0], hex_n_ideal.polygon_points[1], hex_n_ideal.polygon_points[2],
               hex_n_ideal.polygon_points[3], hex_n_ideal.polygon_points[4], hex_n_ideal.polygon_points[5]]
        arc_k = [hex_n_ideal.arcs[0], hex_n_ideal.arcs[1], hex_n_ideal.arcs[2], hex_n_ideal.arcs[3],
                 hex_n_ideal.arcs[4], hex_n_ideal.arcs[5]]

        # transforming disk at s_0
        circle1_radii_transition = [circle_radius[0] * (
                1 - t / step_size_one_direction) + .1 * t / step_size_one_direction
                                    for t in range(step_size_one_direction)] + [
                                       circle_radius[0] * t / step_size_one_direction + .1 * (
                                               1 - t / step_size_one_direction)
                                       for t in range(step_size_one_direction + 1)]
        num_steps = 2 * step_size_one_direction + 1
        for t in range(num_steps):
            radius1 = circle1_radii_transition[t]
            new_circle = Circle(radius1, arc_center=hex_n_ideal.polygon_points[0], color=GREEN_B, fill_opacity=.5,
                                stroke_width=2)

            # S_1 tilde
            moving_intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(arc_k[0].circle_center,
                                                                                          arc_k[0].radius,
                                                                                          s_k[0], radius1)
            intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(s_k[1],
                                                                                   circle_radius[1],
                                                                                   arc_k[0].circle_center,
                                                                                   arc_k[0].radius)
            arc_new1 = ArcBetweenPoints(intersection1, moving_intersection1, color=ORANGE,
                                        radius=arc_k[0].radius, stroke_width=2).reverse_direction()
            # S_2 tilde
            moving_intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(s_k[0], radius1,
                                                                                          arc_k[5].circle_center,
                                                                                          arc_k[5].radius, )
            intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(arc_k[5].circle_center,
                                                                                   arc_k[5].radius,
                                                                                   s_k[5], circle_radius[5])
            arc_new2 = ArcBetweenPoints(moving_intersection2, intersection2, color=ORANGE,
                                        radius=arc_k[5].radius, stroke_width=2).reverse_direction()
            self.play(Transform(transformed_disk, new_circle), Transform(transformed_arc1, arc_new1),
                      Transform(transformed_arc2, arc_new2), rate_func=lambda a: a,
                      run_time=3 / num_steps)
        self.wait(7)
        # transforming all disks
        transformed_disks = VGroup(disks[0], disks[1], disks[2], disks[3], disks[4], disks[5])
        transformed_arcs = VGroup(dynamic_arcs[0], dynamic_arcs[1], dynamic_arcs[2], dynamic_arcs[3], dynamic_arcs[4],
                                  dynamic_arcs[5])
        circle_radii_transition = [circle_radius * (1 - t / step_size_one_direction) for t in
                                   range(step_size_one_direction)] + [
                                      circle_radius * t / step_size_one_direction
                                      for t in range(step_size_one_direction + 1)]
        num_steps = 2 * step_size_one_direction + 1
        new_circle_group = VGroup()
        new_arcs_group = VGroup()
        for t in range(num_steps):
            if t == (num_steps + 1) / 2:
                helping_dots = VGroup()
                for i in range(0, 6):
                    helping_dots.add(Dot(hex_n_ideal.polygon_points[i], color=ORANGE, radius=0.01))
                self.add(helping_dots)
                self.wait(2)
                self.play(TransformFromCopy(formula[0], formula[1]),
                          TransformFromCopy(formula[0], VGroup(formula[2], formula[3])))
                self.wait(3)
                self.remove(helping_dots)
            for i in range(0, 6):
                radius1 = circle_radii_transition[t][i]
                radius2 = circle_radii_transition[t][(i + 1) % 6]
                new_circle_group.add(
                    Circle(radius1, arc_center=hex_n_ideal.polygon_points[i], color=GREEN_B, fill_opacity=.5,
                           stroke_width=2))
                moving_intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(arc_k[i].circle_center,
                                                                                              arc_k[i].radius, s_k[i],
                                                                                              radius1)
                moving_intersection2 = get_intersection_in_unit_circle_of_two_tangent_circles(s_k[(i + 1) % 6], radius2,
                                                                                              arc_k[i].circle_center,
                                                                                              arc_k[i].radius)
                arc_new1 = ArcBetweenPoints(moving_intersection2, moving_intersection1, color=ORANGE,
                                            radius=arc_k[i].radius, stroke_width=2).reverse_direction()
                new_arcs_group.add(arc_new1)
            self.play(Transform(transformed_disks, new_circle_group), Transform(transformed_arcs, new_arcs_group),
                      rate_func=lambda a: a, run_time=3 / num_steps)
            new_circle_group = VGroup()
            new_arcs_group = VGroup()

        self.wait(3)
        self.play(FadeOut(s_k_text), FadeOut(p1))
        self.play(Write(konvergenz, stroke_width=.5))
        # transforming into ideal hexagon
        disks_group = VGroup(disks[0], disks[1], disks[2], disks[3], disks[4], disks[5])
        arc_group = VGroup(dynamic_arcs[0], dynamic_arcs[1], dynamic_arcs[2], dynamic_arcs[3], dynamic_arcs[4],
                           dynamic_arcs[5])
        step_size = 50
        new_disk_group = VGroup()
        new_arc_group = VGroup()
        transition = create_radius_transition(radius=radius, step_size=step_size)
        disk_transition = create_radius_transition(radius=radius, step_size=step_size, end_point=1 - circle_radius)
        for t in range(1, step_size):
            hexagon_new = HyperbolicPolygon.from_polar(phis, transition[t], dot_radius=0.01, stroke_width=2)
            for i in range(0, 6):
                circle = Circle(radius=circle_radius[i], arc_center=polar_to_point(phis[i], disk_transition[t][i]),
                                color=GREEN_B, fill_opacity=.5, stroke_width=2)
                new_disk_group.add(circle)
                # transforming orange s_k
                moving_arc = HyperbolicArcBetweenPoints(polar_to_point(phis[i], transition[t][i]),
                                                        polar_to_point(phis[(i + 1) % 6],
                                                                       transition[t][(i + 1) % 6]))
                moving_intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(
                    moving_arc.circle_center, moving_arc.radius,
                    polar_to_point(phis[i], disk_transition[t][i]),
                    circle_radius[i])
                intersection1 = get_intersection_in_unit_circle_of_two_tangent_circles(
                    polar_to_point(phis[(i + 1) % 6], disk_transition[t][(i + 1) % 6]),
                    circle_radius[(i + 1) % 6], moving_arc.circle_center, moving_arc.radius)
                arc_new = ArcBetweenPoints(intersection1, moving_intersection1, color=ORANGE,
                                           radius=moving_arc.radius, stroke_width=2).reverse_direction()
                new_arc_group.add(arc_new)

            self.play(Transform(hex_n_ideal, hexagon_new), Transform(disks_group, new_disk_group),
                      Transform(arc_group, new_arc_group), run_time=.05, rate_func=lambda a: a)
            new_disk_group = VGroup()  # nochmal leeren
            new_arc_group = VGroup()
        self.wait(2)
        # todo fine tune position, also transform parentheses
        self.play(FadeOut(konvergenz), formula.animate.shift(DOWN))
        altper_infty = MathTex(r'(P_\infty)', font_size=20).next_to(formula[2], direction=RIGHT,
                                                                    buff=.05)
        self.play(FadeTransform(formula[3], altper_infty))

        self.wait(6)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
