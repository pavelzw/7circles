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
        eps = 0.01
        phi_1 = PI
        # phi_2 != 0, PI because else we divide by 0
        phi_2 = PI / 3

        # bugs:
        # phi_1 = 0.1, phi_2 = 0.5
        # phi_1 = 0.1, phi_2 = 3.5
        # phi_1 = 0.1, phi_2 = 4.5

        point_1 = radian_to_point(phi_1)
        point_2 = radian_to_point(phi_2)
        self.play(Create(Dot(point_1, color=RED)))
        self.play(Create(Dot(point_2, color=BLUE)))

        middle = get_circle_middle(phi_1, phi_2)

        # todo remove
        line_1 = TangentLine(circle, alpha=phi_1 / (2 * PI), length=4)
        line_2 = TangentLine(circle, alpha=phi_2 / (2 * PI), length=4)

        self.play(Create(circle))
        self.play(Create(line_1))
        self.play(Create(line_2))
        self.play(Create(Dot(middle)))
        arc = get_arc(phi_1, phi_2)
        self.play(Create(arc))

        self.wait(duration=2)


class LineTransform(Scene):
    def construct(self):
        m = 2
        phisA = []
        phisB = []
        lines = [[] for _ in range(m)]

        for j in range(m):

            for i in np.arange(0, 3, 1):
                phisA.append(radian_to_point(i))
                phisB.append(radian_to_point(i + 3))

            for p in phisA:
                for q in phisB:
                    lines[j].append(Line(start=p, end=q, shade_in_3d=False, stroke_width=0.3))

            for l in lines[j]:
                l.insert_n_curves(1000)

            circle = Circle(shade_in_3d=True)
            self.add(circle, ThreeDAxes())

            # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

            n = 5
            animations = [[] for _ in range(n)]

            for l in lines[j]:
                animations[0].append(Create(l))
                animations[1].append(ApplyPointwiseFunction(lambda x: tf_klein_to_poincare(0.9999 * x), l))
                for i in range(2, n):
                    for k in lines:
                        for h in k:
                            animations[i].append(ApplyPointwiseFunction(lambda x: mobius_transform(x, 1.01, 0., 0.), h))

            self.play(*animations[0])
            self.play(*animations[1])
            for i in range(2, n):
                self.play(*animations[i], run_time=1, rate_func=(lambda x: x))

        phisA = []
        phisB = []

            # self.play(Create(Sphere()))


def tf_klein_to_hem(point):
    x = point[0]
    y = point[1]
    assert x ** 2 + y ** 2 <= 1
    return array([x, y, sqrt(1 - (x ** 2) - (y ** 2))])


def tf_hem_to_poincare(point):
    x = point[0]
    y = point[1]
    z = point[2]
    return array([x / (1 + z), y / (1 + z), 0.])


def tf_klein_to_poincare(point):
    return tf_hem_to_poincare(tf_klein_to_hem(point))


def mobius_transform(point, x, y, u):
    res = complex_mobius_transform(complex(point[0], point[1]), x, y, u)
    # print(res)
    return array([real(res), imag(res), point[2]])


def complex_mobius_transform(z, x, y, u):
    a = complex(x, y)
    b = complex(u, sqrt(-pow(u, 2) + pow(x, 2) + pow(y, 2) - 1))
    # if absolute(z) == 1:
    #    return complex(0, 0)
    return divide(add(multiply(a, z), conj(b)), add(multiply(b, z), conj(a)))


def radian_to_point(angle):
    return np.array((cos(angle), sin(angle), 0))


def get_arc(phi_1, phi_2):
    assert phi_1 >= 0
    assert phi_2 >= 0

    point_1 = radian_to_point(phi_1)
    point_2 = radian_to_point(phi_2)

    middle = get_circle_middle(phi_1, phi_2)

    r = np.linalg.norm(middle - point_1)
    start_angle = arcsin((point_1[1] - middle[1]) / r)
    angle = arcsin((point_2[0] - middle[0]) / r) - PI / 2 - start_angle

    arc = Arc(radius=r, arc_center=middle, start_angle=start_angle, angle=angle)
    return arc


def get_circle_middle(phi_1, phi_2):
    x = (-sin(phi_1) + sin(phi_2)) / (-cos(phi_2) * sin(phi_1) + cos(phi_1) * sin(phi_2))
    y = (1 - x * cos(phi_2)) / sin(phi_2)
    return np.array((x, y, 0))

if __name__ == '__main__':

    import subprocess

    params = 'manim -pql animation.py LineTransform -v DEBUG'.split()
    subprocess.run(params,
                   check=True,
                   capture_output=True,
                   text=True)

