from math import pi

import numpy as np
from manim import Scene, Square, Circle, Dot, Group, Text, Create, FadeIn, FadeOut, MoveAlongPath, Line, WHITE, BLUE, \
    GREEN_B, Transform, MovingCameraScene, Uncreate, \
    VGroup, DecimalNumber, RIGHT, Tex, LEFT, UP, MathTex, Write, Unwrite, Indicate, TransformFromCopy, VMobject, RED, \
    DOWN, GREY_B, GREEN, ORIGIN, PURPLE, ORANGE, ArcBetweenPoints, ReplacementTransform, GREEN_D

from geometry_util import polar_to_point, hyperbolic_distance_function, create_min_circle_radius, moving_circle, \
    moving_line, get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon_util import create_phis, create_radius_transition
from hyperbolic_polygon import HyperbolicPolygon


class Scene1(MovingCameraScene):
    def construct(self):
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

        formula_size = 15

        timings = [8,  # hexagon
                   5]
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()
        self.camera.frame.width = 6
        circle = Circle(color=GREEN_B)
        self.play(Create(circle))

        # showing four random non ideal hexagons and an ideal hexagon
        for i in range(0, 5):
            radius = np.random.uniform(0.5, 0.7, 6)
            phis = create_phis(min_dist=0.6)
            hexagon = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02)
            if i == 4:
                hexagon = HyperbolicPolygon.from_polar(phis, dot_radius=0.02)
            self.play(FadeIn(hexagon))
            self.play(FadeOut(hexagon))

        # creating our nonideal hexagon
        radius = [0.5, 0.7, 0.6, 0.7, 0.5, 0.6]
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]

        hexagon = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02)
        hex_name = MathTex('P', font_size=15).move_to([0.6, 0.4, 0])
        self.play(Create(hexagon), run_time=timings.pop())
        self.play(Indicate(hexagon, color=WHITE), Indicate(hex_name, color=WHITE))
        self.wait(2)

        arc = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02, color=BLUE).arcs
        dots = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02,
                                            color=BLUE).dots
        # Kantenbeschriftung
        for i in range(0, 6):
            self.play(Create(arc[i]), Write(s_k[i]), Create(dots[i].set_color(BLUE)),
                      rate_func=lambda a: a, run_time=1)

        self.play(self.camera.frame.animate.set(width=6).move_to([1.5, 0, 0]))  # moves circle to left

        # Perimeter
        sum1 = per, sum_sk = VGroup(MathTex(r'\mathrm{Per}(P) = ', font_size=formula_size),
                                    MathTex(r'S_1 + S_2 + S_3 + S_4 + S_5 + S_6 ', font_size=formula_size)).arrange(
            buff=0.05).move_to([2.5, 0.2, 0])
        sum2 = alt_per, alt_sum = VGroup(MathTex(r'\mathrm{AltPer}(P) ', font_size=formula_size),
                                         MathTex(r' = S_1 - S_2 + S_3 - S_4 + S_5 - S_6  ',
                                                 # TODO red and blue would be nice
                                                 font_size=formula_size)).arrange(buff=0.05).next_to(sum1, .5 * DOWN)

        self.play(Write(per))
        self.play(TransformFromCopy(VGroup(*arc, *s_k), sum_sk))
        self.wait(3)

        # Alternating Perimeter
        hexagon_bi_colored = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02,
                                                          color=[BLUE, RED, BLUE, RED, BLUE, RED])

        self.play(FadeIn(hexagon_bi_colored, s_2_red, s_4_red, s_6_red, *dots))
        self.wait(2)
        self.play(TransformFromCopy(VGroup(hexagon_bi_colored, *s_k_colored), sum2))
        self.wait(3)


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        s_1 = MathTex('S_1', color=BLUE, font_size=15).move_to([0.2, .5, 0])
        s_1_orange = MathTex('S_1', color=ORANGE, font_size=15).move_to([0.2, .5, 0])
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

        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, color=[BLUE, RED, BLUE, RED, BLUE, RED])
        hexagon_grey = HyperbolicPolygon.from_polar(phis, add_dots=False, color=GREY_B)
        arc_colored = HyperbolicPolygon.from_polar(phis, add_dots=False, color=ORANGE).arcs[0]
        self.add(circle)
        self.play(Create(hexagon, run_time=5))
        self.play(FadeIn(s_k))
        self.play(self.camera.frame.animate.move_to([1, 0, 0]))
        self.wait(1)
        self.play(FadeIn(hexagon_grey), FadeOut(s_k), FadeOut(hexagon), FadeIn(arc_colored, s_1_orange))
        self.wait(1)

        point1 = hexagon.polygon_points[0]
        point2 = hexagon.polygon_points[1]
        arc = hexagon.arcs[0]

        distance_text, distance_number = label = VGroup(
            Tex(r'$\mathrm{length}(S_1)=$', font_size=20),
            DecimalNumber(np.exp(hyperbolic_distance_function(point1, point2)),
                          num_decimal_places=2, show_ellipsis=True, group_with_commas=False,
                          font_size=20))
        label.arrange()
        label.move_to([1.5, 0, 0], aligned_edge=LEFT)
        self.play(Create(label))  # TODO num_decimal_places is not 2??
        step_size = 50
        for t in range(1, step_size):
            interp_point1 = get_intersection_in_unit_circle_of_two_tangent_circles(arc.circle_center, arc.radius,
                                                                                   point1,
                                                                                   t / step_size * radius_disks[0])
            interp_point2 = get_intersection_in_unit_circle_of_two_tangent_circles(point2,
                                                                                   t / step_size * radius_disks[1],
                                                                                   arc.circle_center, arc.radius)
            new_arc = ArcBetweenPoints(interp_point2, interp_point1, color=ORANGE, radius=arc.radius)

            distance = np.exp(
                hyperbolic_distance_function(interp_point2, interp_point1))
            distance_number.font_size = 20
            label.arrange()
            label.move_to([1.5, 0, 0], aligned_edge=LEFT)
            self.play(Transform(arc_colored, new_arc), distance_number.animate.set_value(distance), run_time=0.05,
                      rate_func=lambda a: a)
        self.wait(3)


class Scene3(MovingCameraScene):  # former TransformingNonIdealIntoIdeal
    def construct(self):
        self.camera.frame.width = 6
        circle = Circle()
        self.add(circle)
        p1 = MathTex(r'P_1', font_size=20).move_to([0.2, 0.6, 0])
        konvergenz = MathTex(r'P_n \xrightarrow{n \rightarrow \infty}P_\infty', font_size=25).move_to([2, 0, 0])
        s_1 = MathTex(r'\tilde{S_1}', color=ORANGE, font_size=20).move_to([[.25, .6, 0]])
        s_2 = MathTex(r'\tilde{S_2}', color=ORANGE, font_size=20).move_to([-.65, .5, 0])
        s_3 = MathTex(r'\tilde{S_3}', color=ORANGE, font_size=20).move_to([-.8, -0.1, 0])
        s_4 = MathTex(r'\tilde{S_4}', color=ORANGE, font_size=20).move_to([-.14, -0.7, 0])
        s_5 = MathTex(r'\tilde{S_5}', color=ORANGE, font_size=20).move_to([0.53, -.6, 0])
        s_6 = MathTex(r'\tilde{S_6}', color=ORANGE, font_size=20).move_to([.7, -.1, 0])
        s_k = VGroup(s_1, s_2, s_3, s_4, s_5, s_6)
        radius = np.array([0.7, 0.6, .75, .56, .65, .53])
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]
        circle_radius = [.2, .25, .16, .29, .18, .12]  # radius for disks

        # without disks
        step_size = 50  # normally 100, but takes long
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_radius_transition(radius=radius, step_size=step_size)
        hexagon = HyperbolicPolygon.from_polar(phis, transition[0], dot_radius=0.02)
        self.play(Create(hexagon), run_time=5)
        self.play(Write(p1))
        self.play(FadeOut(p1))
        self.play(self.camera.frame.animate.move_to([1, 0, 0]))
        self.play(Write(konvergenz))

        for t in range(1, step_size - 1):
            hexagon_new = HyperbolicPolygon.from_polar(phis, transition[t], dot_radius=0.02)
            self.play(Transform(hexagon, hexagon_new), run_time=0.05,
                      rate_func=lambda a: a)

        hexagon_new = HyperbolicPolygon.from_polar(phis, transition[-1], dot_radius=0.02)
        self.play(Transform(hexagon, hexagon_new), run_time=0.05,
                  rate_func=lambda a: a)
        self.wait(duration=3)

        # with disks
        self.play(FadeOut(hexagon, konvergenz))
        hex_n_ideal = HyperbolicPolygon.from_polar(phis, radius, dot_radius=0.02)
        self.play(FadeIn(hex_n_ideal))

        for k in range(0, 6):  # creating disks
            point1 = hex_n_ideal.polygon_points[k]
            circle = Circle(arc_center=point1, radius=circle_radius[k], color=GREEN_B, fill_opacity=0.5)
            self.add_foreground_mobjects(circle)
            self.play(FadeIn(circle))

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
                                       radius=arc.radius).reverse_direction()
            self.play(Create(arc_new), Write(s_k[k]))
            if k == 0:
                distance_text, distance_number = label = VGroup(
                    Tex(r'$\mathrm{length}(\tilde{S_1})=$', font_size=20),
                    DecimalNumber(np.exp(hyperbolic_distance_function(intersection2, intersection1)),
                                  num_decimal_places=2, show_ellipsis=True, group_with_commas=False,
                                  font_size=20)).arrange(buff=.05).move_to([2.4, 0, 0])
                self.play(Write(label))
                self.wait(1)
                self.play(FadeOut(label))
        self.wait(3)
        sum2 = alt_per, alt_sum = VGroup(MathTex(r'\mathrm{AltPer}(\tilde{P}) =', font_size=20),
                                         MathTex(
                                             r' \tilde{S_1} - \tilde{S_2} + \tilde{S_3} - \tilde{S_4} + \tilde{S_5} - \tilde{S_6}',
                                             font_size=20)).arrange(direction=DOWN, aligned_edge=LEFT).move_to(
            [2.4, 1, 0])
        self.play(TransformFromCopy(s_k, sum2))
        self.wait(3)


class NonIdealHexagonAnimation(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)

        hexagon = HyperbolicPolygon.from_polar(phis, radius)
        self.play(Create(hexagon), run_time=5)
        self.wait(2)

        # try of hyperbolic distance, works alright. convergent to infinity?
        point1 = polar_to_point(0, 0.9)
        point2 = polar_to_point(pi / 4, 0.9)
        self.add(Dot([point1]), Dot([point2]))
        distance = hyperbolic_distance_function(point1, point2)
        print(distance)


# MovingCameraScene anstatt Scene
class HexagonWithSixDisks(Scene):
    def construct(self):
        circle = Circle(color=WHITE)
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.8)

        hexagon = HyperbolicPolygon.from_polar(phis, radius, stroke_width=4)
        self.add(hexagon)
        # case for first circle
        last_point = hexagon.polygon_points[0]
        point = hexagon.polygon_points[1]
        end_point = hexagon.polygon_points[5]

        circle_radius = create_min_circle_radius(end_point, last_point, point)
        circle = Circle(arc_center=last_point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
        self.add(circle)

        for k in range(2, 6):  # from 2 to 5
            next_point = polar_to_point(phis[k], radius[k])

            circle_radius = create_min_circle_radius(last_point, point, next_point)
            circle = Circle(arc_center=point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
            self.add(circle)
            last_point = point
            point = next_point

        # circle for last point
        circle = Circle(arc_center=point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
        self.add(circle)

        self.wait(5)


class TransformingHexagonWithDisks(MovingCameraScene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)
        circle_radius = np.zeros(shape=6)

        step_size = 50  # normally 100, but takes long
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_radius_transition(radius=radius, step_size=step_size)
        hexagon = HyperbolicPolygon.from_polar(phis, transition[0])
        self.add(hexagon)
        # creating 6 disks
        last_point = hexagon.polygon_points[0]
        first_point = last_point

        point = hexagon.polygon_points[1]
        end_point = hexagon.polygon_points[5]
        circle_radius[0] = create_min_circle_radius(end_point, last_point, point)
        circle = Circle(arc_center=last_point, radius=circle_radius[0], color=GREEN_B, fill_opacity=0.5)
        disks_group = VGroup()  # treating disks as a group
        disks_group.add(circle)
        for k in range(2, 6):  # from 2 to 5
            next_point = polar_to_point(phis[k], radius[k])
            circle_radius[k - 1] = create_min_circle_radius(last_point, point, next_point)
            circle = Circle(arc_center=point, radius=circle_radius[k - 1], color=GREEN_B, fill_opacity=0.5)
            last_point = point
            point = next_point
            disks_group.add(circle)
        circle_radius[5] = create_min_circle_radius(last_point, point, first_point)
        circle = Circle(arc_center=point, radius=circle_radius[5], color=GREEN_B,
                        fill_opacity=0.5)  # circle for last point
        disks_group.add(circle)
        self.play(Create(disks_group), run_time=3)

        # length of S_k
        s_1 = Tex(r'$S_1$')
        # label = VGroup(Tex(r'$\mathrm{length}(S_1)=$', font_size=35), DecimalNumber(
        #  hyperbolic_distance_function(hexagon.polygon_points[0]), hexagon.polygon_points[1])),
        #  num_decimal_places=2, show_ellipsis=True, group_with_commas=False, font_size=35))
        # label.move_to([2, 0, 0], aligned_edge=LEFT)
        # self.add(label)
        # todo s_1 in die mitte von p1, p2

        new_disk_group = VGroup()
        # transition of disks and hexagon
        disk_transition = create_radius_transition(radius=radius, step_size=step_size,
                                                   end_point=1 - circle_radius)
        for t in range(1, step_size):
            hexagon_new = HyperbolicPolygon.from_polar(phis, transition[t])
            s_1.next_to((hexagon_new.arcs[0]), RIGHT)

            # s_1_length = hyperbolic_distance_function(, ) of intersection between arc and circle

            # s_1 berechnung
            self.add(s_1)
            for i in range(0, 6):
                new_disk_group.add(
                    Circle(radius=circle_radius[i], arc_center=polar_to_point(phis[i], disk_transition[t][i]),
                           color=GREEN_B, fill_opacity=0.5))
            self.play(Transform(hexagon, hexagon_new), Transform(disks_group, new_disk_group), run_time=0.05,
                      rate_func=lambda a: a)
            new_disk_group = VGroup()  # nochmal leeren
        self.wait(duration=3)


class TransformingNonIdealIntoIdeal(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)

        step_size = 50  # normally 100, but takes long
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_radius_transition(radius=radius, step_size=step_size)
        hexagon = HyperbolicPolygon.from_polar(phis, transition[0])
        self.add(hexagon)

        point1_text = Tex('$P_1$', font_size=30)
        point2_text = Tex('$P_2$', font_size=30)
        distance_text, distance_number = label = VGroup(
            Tex(r'$\mathrm{dist}(P_1, P_2)=$', font_size=35),
            DecimalNumber(
                np.exp(hyperbolic_distance_function(hexagon.polygon_points[0], hexagon.polygon_points[1])),
                num_decimal_places=2, show_ellipsis=True, group_with_commas=False, font_size=35))
        label.move_to([2, 0, 0], aligned_edge=LEFT)
        self.add(label)
        for t in range(1, step_size - 1):
            hexagon_new = HyperbolicPolygon.from_polar(phis, transition[t])
            point1_text.next_to((hexagon_new.polygon_points[1]), LEFT, UP)
            point2_text.next_to((hexagon_new.polygon_points[0]), RIGHT, UP)
            self.add(point1_text, point2_text)
            distance = np.exp(
                hyperbolic_distance_function(hexagon_new.polygon_points[0], hexagon_new.polygon_points[1]))
            distance_number.font_size = 35
            label.arrange()
            label.move_to([2, 0, 0], aligned_edge=LEFT)
            self.play(Transform(hexagon, hexagon_new),
                      distance_number.animate.set_value(distance), run_time=0.05,
                      rate_func=lambda a: a)

        hexagon_new = HyperbolicPolygon.from_polar(phis, transition[-1])
        self.play(Transform(hexagon, hexagon_new),
                  Transform(distance_number, Tex(r'$\infty$').next_to(distance_text)), run_time=0.05,
                  rate_func=lambda a: a)
        self.wait(duration=3)


class AlternatingPerimeter(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)
        hexagon = HyperbolicPolygon.from_polar(phis, radius, color=[WHITE, BLUE, WHITE, BLUE, WHITE, BLUE])

        self.play(Create(hexagon), run_time=8)
        self.wait(2)


class EuclideanCircles(Scene):
    def construct(self):
        # euclidean situation in center
        eucl_center = np.array([0, 0, 0])
        new_center = np.array([4, 0, 0])
        point1 = eucl_center - np.array([1, 0, 0])
        point2 = point1 + np.array([1, 1, 0])
        point3 = eucl_center + np.array([0.5, -0.5, 0])
        points = np.array([eucl_center, point1, point2, point3])

        square = Square(side_length=4).move_to(eucl_center)
        circle = Circle(radius=1).move_to(eucl_center)
        dot = Dot().move_to(eucl_center)
        text = Text('Euclidean Center', font_size=15).next_to(dot)
        group = Group(circle, dot)
        self.play(Create(square))
        self.play(Create(dot))
        self.play(Create(circle))
        self.play(FadeIn(text))
        self.play(FadeOut(text))
        for i in range(3):
            self.play(MoveAlongPath(group, Line(start=points[i], end=points[i + 1])))

        # explaining radii
        radius_text = Text('radius 3', font_size=18)
        group2 = Group(group, square)
        circle_radii = Circle(radius=3)
        self.play(Transform(group2, circle_radii))
        self.play(Create(dot))
        radius1 = Line(start=eucl_center, end=eucl_center + np.array([3, 0, 0]))
        radius2 = Line(start=eucl_center, end=eucl_center + np.array([-1, -np.sqrt(8), 0]))
        self.play(Create(radius1))
        self.play(Create(radius2), FadeIn(radius_text.next_to(radius2)))
        self.play(Uncreate(radius2), Uncreate(radius_text), Uncreate(radius1))
    # radius with arc
    # moving everything to the right so we can continue with the horodisk


class Horodisk(Scene):
    def construct(self):
        # hyperbolic situation
        # points of position
        center = [0, 0, 0]
        start_points = np.array([center, center, center, center])
        length = [1, 1, -3]  # 1 is 1 unit to the left, -3 is 3 units to the right, way of circles moving

        angle1 = pi / 4
        angle2 = 4 * pi / 3
        angles = [0, angle1, angle2]

        outer_circle = Circle(color=WHITE, radius=2).move_to(center)
        circle = [Dot(color=BLUE), Circle(color=WHITE, radius=1.5),
                  Circle(color=WHITE, radius=1), Circle(color=WHITE, radius=0.5)]
        circles = Group(circle[0], circle[1], circle[2], circle[3]).move_to(center)

        # creating circles and dot
        self.play(FadeIn(outer_circle))
        self.play(FadeIn(circle[0]))
        self.wait(duration=2)
        self.play(Create(circle[1]), Create(circle[2]), Create(circle[3]))

        # circles moving along a line 3 times
        for i in range(3):
            end_points = np.array([start_points[0] - [1 * length[i], 0, 0],
                                   start_points[1] - [0.25 * length[i], 0, 0],
                                   start_points[2] - [0.5 * length[i], 0, 0],
                                   start_points[3] - [0.75 * length[i], 0, 0]])
            lines = moving_line(start_points, end_points)
            self.play(MoveAlongPath(circle[0], lines[0]), MoveAlongPath(circle[1], lines[1]),
                      MoveAlongPath(circle[2], lines[2]), MoveAlongPath(circle[3], lines[3]))
            self.wait(duration=1)
            start_points = end_points

        # circles moving along part circle twice
        for i in range(2):
            arcs = moving_circle(angles[i], angles[i + 1], center)
            self.play(MoveAlongPath(circle[0], arcs[0]), MoveAlongPath(circle[1], arcs[1]),
                      MoveAlongPath(circle[2], arcs[2]), MoveAlongPath(circle[3], arcs[3]))
            self.wait(duration=1)
