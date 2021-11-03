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
        positionDot1 = array([-1, 0, 0])
        positionDot2 = array([-2, 0, 0])
        positionDot3 = array([1, 0, 0])

        circle1 = Circle(color=WHITE, radius=2)
        circle2 = Circle(color=WHITE, radius=1.5)
        circle3 = Circle(color=WHITE, radius=1)
        circle4 = Circle(color=WHITE, radius=0.5)
        dot = Dot()

        # creating circles and dot
        self.play(FadeIn(circle1))
        self.play(FadeIn(dot))
        self.play(Create(circle2))
        self.play(Create(circle3))
        self.play(Create(circle4))

        # moving horodisks and dot to [-1,0,0]
        lineDot = Line(start=ORIGIN, end=positionDot1)  # to coordinate moving of horodisks and point
        line2 = Line(start=ORIGIN, end=positionDot1 * 0.25)
        line3 = Line(start=ORIGIN, end=positionDot1 * 0.5)
        line4 = Line(start=ORIGIN, end=positionDot1 * 0.75)

        # moves everything to the left
        self.play(MoveAlongPath(dot, lineDot), MoveAlongPath(circle2, line2), MoveAlongPath(circle3, line3),
                  MoveAlongPath(circle4, line4))
        self.wait(duration=1)

        # moving to center [-2,0,0]
        lineDot = Line(start=positionDot1, end=positionDot2)
        line2 = Line(start=positionDot1 * 0.25, end=positionDot2 * 0.25)
        line3 = Line(start=positionDot1 * 0.5, end=positionDot2 * 0.5)
        line4 = Line(start=positionDot1 * 0.75, end=positionDot2 * 0.75)

        self.play(MoveAlongPath(dot, lineDot), MoveAlongPath(circle2, line2), MoveAlongPath(circle3, line3),
                  MoveAlongPath(circle4, line4))
        self.wait(duration=1)

        # moving to [1,0,0]
        lineDot = Line(start=positionDot2, end=positionDot3)
        line2 = Line(start=positionDot2 * 0.25, end=positionDot3 * 0.25)
        line3 = Line(start=positionDot2 * 0.5, end=positionDot3 * 0.5)
        line4 = Line(start=positionDot2 * 0.75, end=positionDot3 * 0.75)

        self.play(MoveAlongPath(dot, lineDot), MoveAlongPath(circle2, line2), MoveAlongPath(circle3, line3),
                  MoveAlongPath(circle4, line4))
        self.wait(duration=1)

        # moving to [1/sqrt(2),1/sqrt(2),0]

        arcDot = Arc(angle=PI / 4)  # creates eighth of circle
        arc2 = Arc(angle=PI / 4, radius=0.25)
        arc3 = Arc(angle=PI / 4, radius=0.5)
        arc4 = Arc(angle=PI / 4, radius=0.75)

        self.play(MoveAlongPath(dot, arcDot), MoveAlongPath(circle2, arc2), MoveAlongPath(circle3, arc3),
                  MoveAlongPath(circle4, arc4))
        self.wait(duration=2)


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
