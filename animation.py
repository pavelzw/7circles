from decimal import Decimal

from manim import *
from numpy import *
import numpy as np
import math


class Try(Scene):
    def construct(self):
        circle3 = Circle(radius=0.5).move_to([-3, 0, 0])
        line3 = Line(start=array([-3, 0, 0]), end=array([-3, 0, 0]) - array([0.75, 0, 0]))

        circle2 = Circle().move_to([-3, 0, 0])
        line2 = Line(start=array([-3, 0, 0]), end=array([-3, 0, 0]) - array([0.5, 0, 0]))

        circle1 = Circle(radius=1.5).move_to([-3, 0, 0])
        line1 = Line(start=array([-3, 0, 0]), end=array([-3, 0, 0]) - array([0.25, 0, 0]))

        self.add(Circle(radius=2).move_to([-3, 0, 0]))
        self.play(MoveAlongPath(circle3, line3), MoveAlongPath(circle2, line2),
                  MoveAlongPath(circle1, line1))  # creates line


class EuclidianCircles(Scene):
    def construct(self):
        # euclidian situation in center
        eucl_center = array([0, 0, 0])
        new_center = array([4, 0, 0])
        point1 = eucl_center - array([1, 0, 0])
        point2 = point1 + array([1, 1, 0])
        point3 = eucl_center + array([0.5, -0.5, 0])
        points = array([eucl_center, point1, point2, point3])

        square = Square(side_length=4).move_to(eucl_center)
        circle = Circle(radius=1).move_to(eucl_center)
        dot = Dot().move_to(eucl_center)
        text = Text('Euclidian Center', font_size=15).next_to(dot)
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
        radius1 = Line(start=eucl_center, end=eucl_center + array([3, 0, 0]))
        radius2 = Line(start=eucl_center, end=eucl_center + array([-1, -math.sqrt(8), 0]))
        self.play(Create(radius1))
        self.play(Create(radius2), FadeIn(radius_text.next_to(radius2)))
        self.play(Uncreate(radius2), Uncreate(radius_text), Uncreate(radius1))
    # radius with arc
    # moving everything to the right  so we can continue with the horodisk


class Horodisk(Scene):
    def construct(self):

        # hyperbolic situation
        # points of position
        center = [-4, 0, 0]
        start_points = array([center, center, center, center])
        length = [1, 1, -3]  # 1 is 1 unit to the left, -3 is 3 units to the right, way of circles moving

        angle1 = PI / 4
        angle2 = 4 * PI / 3
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
            end_points = array([start_points[0] - [1 * length[i], 0, 0], start_points[1] - [0.25 * length[i], 0, 0],
                                start_points[2] - [0.5 * length[i], 0, 0], start_points[3] - [0.75 * length[i], 0, 0]])
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


class CircleWithArcs(Scene):
    def construct(self):
        circle = Circle()
        self.play(Create(circle))

        phis = np.sort(np.random.uniform(0, 2 * PI, 6))
        dot = Dot(radian_to_point(phis[0]), color=RED)
        self.add_foreground_mobject(dot)
        self.play(Create(dot))

        # create hyperbolic hexagon
        for i in range(phis.shape[0]):
            phi_1 = phis[i]
            phi_2 = phis[(i + 1) % 6]
            point = radian_to_point(phi_2)
            if i < phis.shape[0] - 1:
                dot = Dot(point, color=RED)
                self.add_foreground_mobject(dot)
                self.play(Create(dot))
            # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
            arc = get_arc(phi_1, phi_2).reverse_direction()
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

        arcs = create_arcs(transition[0])
        self.add(arcs)

        for t in range(1, step_size):
            arcs_new = create_arcs(transition[t])
            self.play(Transform(arcs, arcs_new), run_time=0.2, rate_func=lambda a: a)

        # self.wait(duration=5)


def create_phi_transition(phi_old, phi_new, step_size=10):
    assert phi_old.shape == phi_new.shape
    transition = np.empty(shape=(step_size, phi_old.shape[0]))
    for t in range(step_size):
        transition[t] = phi_old * (1 - t / step_size) + phi_new * t / step_size
    return transition


def radian_to_point(angle):
    return np.array((cos(angle), sin(angle), 0))


def create_arcs(phis):
    # create hyperbolic hexagon
    arcs = []
    for i in range(phis.shape[0]):
        phi_1 = phis[i]
        phi_2 = phis[(i + 1) % 6]
        point = radian_to_point(phi_2)
        # bug: if two adjacent points have distance > PI, then the direction needs to be flipped
        arc = get_arc(phi_1, phi_2).reverse_direction()
        arcs.append(arc)
    arcs = Group(arcs[0], arcs[1], arcs[2], arcs[3], arcs[4], arcs[5])
    return arcs


def get_arc(phi_1, phi_2):
    assert phi_1 >= 0
    assert phi_1 < 2 * PI
    assert phi_2 >= 0
    assert phi_2 < 2 * PI

    if phi_1 >= phi_2:
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    assert phi_1 < phi_2

    point_1 = radian_to_point(phi_1)
    point_2 = radian_to_point(phi_2)

    middle = get_circle_middle(phi_1, phi_2)
    r = np.linalg.norm(middle - point_1)

    # gets angle between two tangents
    angle = Angle(TangentLine(Circle(), alpha=phi_1 / (2 * PI)),
                  TangentLine(Circle(), alpha=phi_2 / (2 * PI)))

    ang = angle.get_value(degrees=False)
    if phi_2 - phi_1 < PI:
        arc = ArcBetweenPoints(start=point_2, end=point_1, angle=-ang, radius=r)
    else:
        arc = ArcBetweenPoints(start=point_1, end=point_2, angle=-ang, radius=r)
    return arc


def create_phis(min_dist=0.4):
    phis = np.sort(np.random.uniform(0, 2 * PI, 6))
    while np.min(np.abs(np.roll(phis, shift=1) - phis)) < min_dist or phis[0] < phis[5] - 2 * PI + min_dist:
        phis = np.sort(np.random.uniform(0, 2 * PI, 6))
    return phis


def get_circle_middle(phi_1, phi_2):
    if sin(phi_2) == 0:  # phi_2 != 0, PI because else we divide by 0
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    x = (-sin(phi_1) + sin(phi_2)) / (-cos(phi_2) * sin(phi_1) + cos(phi_1) * sin(phi_2))
    y = (1 - x * cos(phi_2)) / sin(phi_2)
    return np.array((x, y, 0))
