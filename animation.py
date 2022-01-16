import math
from math import pi

import numpy as np
from manim import Scene, Square, Circle, Dot, Group, Text, Create, FadeIn, FadeOut, MoveAlongPath, Line, WHITE, BLUE, \
    Arc, GREEN_B, Transform, RED, ThreeDAxes, ApplyPointwiseFunction, MovingCameraScene, Flash, YELLOW, Uncreate, \
    VGroup, DecimalNumber, ReplacementTransform, RIGHT, always, f_always, Tex, LEFT

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import radian_to_point, mobius_transform, \
    tf_klein_to_poincare, get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles, hyperbolic_distance_function, abs_complex
from hexagon import HexagonCircles, HexagonMainDiagonals, ArcBetweenPointsOnUnitDisk
from hexagon_util import create_phis, create_phi_transition, create_radius_transition
from hyperbolic_hexagon import HyperbolicHexagon, NonIdealHexagon


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
        center = [-4, 0, 0]
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


def moving_circle(start_angle, end_angle, center):
    arc1 = Arc(start_angle=start_angle, angle=end_angle).move_arc_center_to(center)  # creates eighth of circle
    arc2 = Arc(start_angle=start_angle, angle=end_angle, radius=0.25).move_arc_center_to(center)
    arc3 = Arc(start_angle=start_angle, angle=end_angle, radius=0.5).move_arc_center_to(center)
    arc4 = Arc(start_angle=start_angle, angle=end_angle, radius=0.75).move_arc_center_to(center)
    return [arc1, arc2, arc3, arc4]


def moving_line(start_points, end_points):
    line1 = Line(start=start_points[0], end=end_points[0])
    line2 = Line(start=start_points[1], end=end_points[1])
    line3 = Line(start=start_points[2], end=end_points[2])
    line4 = Line(start=start_points[3], end=end_points[3])
    return [line1, line2, line3, line4]


class NonIdealHexagonAnimation(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)

        hexagon = NonIdealHexagon(radius, phis)
        self.play(Create(hexagon), run_time=5)
        self.wait(2)

        # try of hyperbolic distance, works alright. convergent to infinity?
        point1 = radian_to_point(0, 0.9)
        point2 = radian_to_point(pi / 4, 0.9)
        self.add(Dot([point1]), Dot([point2]))
        distance = hyperbolic_distance_function(point1, point2)
        print(distance)


class HexagonWithSixDisks(Scene):
    def construct(self):
        circle = Circle(color=WHITE)
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.8)

        hexagon = NonIdealHexagon(radius, phis)
        self.add(hexagon)

        last_point = radian_to_point(phis[0], radius[0])
        point = radian_to_point(phis[1], radius[1])

        # case for first circle
        end_point = radian_to_point(phis[5], radius[5])
        circle_radius = min(abs_complex(last_point, point), abs_complex(last_point, end_point)) / 2.1
        circle = Circle(arc_center=last_point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
        self.add(circle)

        for k in range(2, 6):  # from 2 to 5
            next_point = radian_to_point(phis[k], radius[k])

            distance_last_present = abs_complex(last_point, point)
            distance_present_next = abs_complex(point, next_point)
            # circles might touch the unit circle
            circle_radius = min(distance_present_next, distance_last_present) / 2.2
            circle = Circle(arc_center=point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
            self.add(circle)

            last_point = point
            point = next_point

        # circle for last point
        circle = Circle(arc_center=point, radius=circle_radius, color=GREEN_B, fill_opacity=0.5)
        self.add(circle)


class TransformingNonIdealIntoIdeal(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.5, 0.7, 6)
        phis = create_phis(min_dist=0.6)

        step_size = 100
        # phis = np.array([0, 1, 2, 3, 4, 5])
        transition = create_radius_transition(radius=radius, step_size=step_size)
        hexagon = NonIdealHexagon(transition[0], phis)
        self.add(hexagon)

        distance_text, distance_number = label = VGroup(
            Tex(r'$\mathrm{dist}(P_1, P_2)=$', font_size=35),
            DecimalNumber(np.exp(hyperbolic_distance_function(hexagon.hexagon_points[0], hexagon.hexagon_points[1])),
                          num_decimal_places=2, show_ellipsis=True, group_with_commas=False, font_size=35))
        label.move_to([2, 0, 0], aligned_edge=LEFT)
        self.add(label)
        for t in range(1, step_size - 1):
            hexagon_new = NonIdealHexagon(transition[t], phis)
            distance = np.exp(
                hyperbolic_distance_function(hexagon_new.hexagon_points[0], hexagon_new.hexagon_points[1]))
            distance_number.font_size = 35
            label.arrange()
            label.move_to([2, 0, 0], aligned_edge=LEFT)
            self.play(Transform(hexagon, hexagon_new),
                      distance_number.animate.set_value(distance), run_time=0.05,
                      rate_func=lambda a: a)

            # hexagon_new.hexagon_points # liste von den punkten
            print(distance)
        hexagon_new = NonIdealHexagon(transition[-1], phis)
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
        hexagon = NonIdealHexagon(radius, phis, alternating_perimeter=True)

        # hexagon = NonIdealHexagon(radius, phis, YELLOW)

        self.play(Create(hexagon), run_time=8)
        self.wait(2)


class CircleWithArcs(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))

        phis = np.sort(np.random.uniform(0, 2 * pi, 6))
        dot = Dot(radian_to_point(phis[0]), color=RED)
        self.add_foreground_mobject(dot)
        self.play(Create(dot))

        # create hyperbolic hexagon
        for i in range(phis.shape[0]):
            phi1 = phis[i]
            phi2 = phis[(i + 1) % 6]
            point = radian_to_point(phi2)
            if i < phis.shape[0] - 1:
                dot = Dot(point, color=RED)
                self.add_foreground_mobject(dot)
                self.play(Create(dot))
            # bug: if two adjacent points have distance > pi, then the direction needs to be flipped
            arc = ArcBetweenPointsOnUnitDisk(phi1, phi2).reverse_direction()
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

        hexagon = HyperbolicHexagon(transition[0])
        self.add(hexagon)

        for t in range(1, step_size):
            hexagon_new = HyperbolicHexagon(transition[t])
            self.play(Transform(hexagon, hexagon_new), run_time=0.2, rate_func=lambda a: a)

        # self.wait(duration=5)


class LineTransform(Scene):
    def construct(self):
        phis_a = []
        phis_b = []
        lines = []
        for i in np.arange(0, 3, 1):
            phis_a.append(radian_to_point(i))
            phis_b.append(radian_to_point(i + 3))

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
        hexagon = HyperbolicHexagon(phis)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius)
        hexagon_diagonals = HexagonMainDiagonals(hexagon)
        self.add(hexagon)
        self.add(hexagon_circles)
        self.add(hexagon_diagonals)

        # self.wait(duration=5)


class SevenCircles(Scene):
    def construct(self):
        circle = Circle()
        phis = create_phis(min_dist=.8, max_dist=1.2)
        first_circle_radius = .4

        hexagon = EuclideanHexagon(phis)
        hexagon_circles = HexagonCircles(hexagon, first_circle_radius)
        inner_intersections = get_intersections_of_n_tangent_circles(hexagon_circles.circles)
        outer_intersections = get_intersections_of_circles_with_unit_circle(hexagon_circles.circles)
        diagonals = get_diagonals(hexagon)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]), color=YELLOW)

        self.play(FadeIn(circle))
        self.play(Create(hexagon_circles, run_time=5))
        for i in range(6):
            self.play(Create(inner_intersections[i], run_time=.5))
        for i in range(6):
            self.play(Create(outer_intersections[i], run_time=.5))
        self.play(Create(hexagon, run_time=5))
        for x in diagonals:
            self.play(Create(x), run_time=1)
        self.play(Create(diagonal_intersection))
        self.wait(1)
        self.play(Flash(diagonal_intersection))
        self.wait(1)
