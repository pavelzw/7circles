from decimal import Decimal

from manim import *
from numpy import *
import numpy as np
import math


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation


class CirclesNextToEachOther(Scene):
    def construct(self):
        circle1 = Circle()
        circle2 = Circle()
        circle2.move_to([2, 0, 0])  # moves circle2 to the right by 2

        self.play(Create(circle1))
        self.play(Create(circle2))


class CircleAndGeodesic(Scene):
    def construct(self):
        circle1 = Circle()
        line1 = Line()  # creates line
        geod = Arc(angle=PI / 2)  # creates quarter circle
        geod.move_to([-0.5, -0.5, 0])  # moves to bottom left, but why 0.5??????

        self.play(Create(circle1))
        self.play(Create(line1))
        self.play(Create(geod))


class Horodisk(Scene):
    def construct(self):
        # points of position
        posDot1 = array([-1, 0, 0])
        posDot2 = array([-2, 0, 0])
        posDot3 = array([1, 0, 0])

        circle1 = Circle(color=WHITE, radius=2)
        circle2 = Circle(color=WHITE, radius=1.5)
        circle3 = Circle(color=WHITE, radius=1)
        circle4 = Circle(color=WHITE, radius=0.5)
        dot = Dot(color=BLUE)
        ToDoText = Text('TODO:Gegenüberstellung euklidische und hyperbolische Horodisks, Center, Radii',
                        font_size=17).move_to([0, -3, 0])
        text_dot = Text('Center', font_size=15, color=BLUE).next_to(dot)

        # creating circles and dot
        self.play(FadeIn(circle1))
        self.play(FadeIn(dot))
        self.play(FadeIn(text_dot))
        self.wait(duration=2)
        self.play(FadeOut(text_dot))
        self.play(Create(circle2), Create(circle3), Create(circle4))
        self.add(ToDoText)

        # moving horodisks and dot to [-1,0,0]
        lines = moving_line(ORIGIN, posDot1)

        # moves everything to the left
        self.play(MoveAlongPath(dot, lines[0]), MoveAlongPath(circle2, lines[1]), MoveAlongPath(circle3, lines[2]),
                  MoveAlongPath(circle4, lines[3]))
        self.wait(duration=1)

        # moving to center [-2,0,0]
        lines = moving_line(posDot1, posDot2)

        self.play(MoveAlongPath(dot, lines[0]), MoveAlongPath(circle2, lines[1]),
                  MoveAlongPath(circle3, lines[2]), MoveAlongPath(circle4, lines[3]))
        self.wait(duration=1)

        # moving to [1,0,0]
        lines = moving_line(posDot2, posDot3)

        self.play(MoveAlongPath(dot, lines[0]), MoveAlongPath(circle2, lines[1]),
                  MoveAlongPath(circle3, lines[2]), MoveAlongPath(circle4, lines[3]))
        self.wait(duration=1)

        # moving to [1/sqrt(2),1/sqrt(2),0]
        arcs = moving_circle(0, PI / 4)

        self.play(MoveAlongPath(dot, arcs[0]), MoveAlongPath(circle2, arcs[1]),
                  MoveAlongPath(circle3, arcs[2]), MoveAlongPath(circle4, arcs[3]))
        self.wait(duration=2)

        arcs = moving_circle(PI / 4, 4 * PI / 3)
        self.play(MoveAlongPath(dot, arcs[0]), MoveAlongPath(circle2, arcs[1]),
                  MoveAlongPath(circle3, arcs[2]), MoveAlongPath(circle4, arcs[3]), run_time=2)
        self.wait(duration=2)


def moving_circle(startangle, angle):
    arc1 = Arc(start_angle=startangle, angle=angle)  # creates eighth of circle
    arc2 = Arc(start_angle=startangle, angle=angle, radius=0.25)
    arc3 = Arc(start_angle=startangle, angle=angle, radius=0.5)
    arc4 = Arc(start_angle=startangle, angle=angle, radius=0.75)
    return [arc1, arc2, arc3, arc4]


def moving_line(start_point, end_point):
    line1 = Line(start=start_point, end=end_point)
    line2 = Line(start=start_point * 0.25, end=end_point * 0.25)
    line3 = Line(start=start_point * 0.5, end=end_point * 0.5)
    line4 = Line(start=start_point * 0.75, end=end_point * 0.75)
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


def radian_to_point(angle):
    return np.array((cos(angle), sin(angle), 0))


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


def get_circle_middle(phi_1, phi_2):
    if sin(phi_2) == 0:  # phi_2 != 0, PI because else we divide by 0
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    x = (-sin(phi_1) + sin(phi_2)) / (-cos(phi_2) * sin(phi_1) + cos(phi_1) * sin(phi_2))
    y = (1 - x * cos(phi_2)) / sin(phi_2)
    return np.array((x, y, 0))
