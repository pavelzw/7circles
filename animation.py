from manim import *
import numpy as np
from math import pi

from hyperbolic_hexagon import HyperbolicHexagon, HyperbolicHexagonCircles, HyperbolicHexagonMainDiagonals, \
    ArcBetweenPointsOnUnitDisk
from geometry_util import radian_to_point, radian_to_point_with_radius, \
    get_both_intersections_line_with_unit_circle
from hexagon_util import create_phis, create_phi_transition


class EuclidianCircles(Scene):
    def construct(self):
        # euclidian situation in center
        eucl_center = np.array([0, 0, 0])
        new_center = np.array([4, 0, 0])
        point1 = eucl_center - np.array([1, 0, 0])
        point2 = point1 + np.array([1, 1, 0])
        point3 = eucl_center + np.array([0.5, -0.5, 0])
        points = np.array([eucl_center, point1, point2, point3])

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


class NonIdealHexagon(Scene):
    def construct(self):
        circle = Circle()
        self.add(circle)
        radius = np.random.uniform(0.4, 0.7, 6)
        phis = create_phis(min_dist=0.4)
        first_point = radian_to_point_with_radius(radius[0], phis[0])
        point1 = first_point
        self.play(Create(Dot(point1)))

        for i in range(0, 6):
            if i == 5:
                point1 = first_point
                point2 = radian_to_point_with_radius(radius[5], phis[5])
            else:
                point2 = radian_to_point_with_radius(radius[i + 1], phis[i + 1])

            self.play(Create(Dot(point2)))
            klein_point1 = tf_poincare_to_klein(point1)  # transform points from poincare to klein model
            klein_point2 = tf_poincare_to_klein(point2)
            intersections = get_both_intersections_line_with_unit_circle(klein_point1, klein_point2)
            x, y = intersections[0], intersections[1]  # new intersections, unclear which belongs to which pointi
            a, b = intersections[2], intersections[3]

            unit_point1 = np.arctan2(y, x)  # get polar coordinates of x,y and a,b
            unit_point2 = np.arctan2(b, a)

            if unit_point1 < 0:  # for assertion phi >= 0
                unit_point1 = unit_point1 + 2 * pi
            if unit_point2 < 0:
                unit_point2 = unit_point2 + 2 * pi

            point1 = point2
            # ArcBetweenPointsOnUnitCircle
            self.play(Create(ArcBetweenPointsOnUnitDisk(unit_point1, unit_point2, color=GREEN)))


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
        m = 2
        phis_a = []
        phis_b = []
        lines = [[] for _ in range(m)]

        for j in range(m):
            for i in np.arange(0, 3, 1):
                phis_a.append(radian_to_point(i))
                phis_b.append(radian_to_point(i + 3))

            for p in phis_a:
                for q in phis_b:
                    lines[j].append(Line(start=p, end=q, shade_in_3d=False, stroke_width=0.3))

            for line in lines[j]:
                line.insert_n_curves(1000)

            circle = Circle(shade_in_3d=True)
            self.add(circle, ThreeDAxes())

            # self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

            n = 5
            animations = [[] for _ in range(n)]

            for line in lines[j]:
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


def tf_klein_to_hem(point):
    x = point[0]
    y = point[1]
    assert x ** 2 + y ** 2 <= 1
    return np.array([x, y, np.sqrt(1 - (x ** 2) - (y ** 2))])


def tf_hem_to_poincare(point):
    x = point[0]
    y = point[1]
    z = point[2]
    return np.array([x / (1 + z), y / (1 + z), 0.])


def tf_klein_to_poincare(point):
    return tf_hem_to_poincare(tf_klein_to_hem(point))


# all other transformation directions
def tf_hem_to_klein(point):  # 3 coord to 2 coord
    x = point[0]
    y = point[1]
    return np.array([x, y, 0])


def tf_poincare_to_hem(point):  # 2 coord to 3 coord
    x = point[0]
    y = point[1]
    new_coord = np.array([2 * x, 2 * y, 1 - (x ** 2) - (y ** 2)])
    scalar = 1 / (1 + (x ** 2) + (y ** 2))
    return scalar * new_coord


def tf_poincare_to_klein(point):  # 2 coord to 2 coord
    return tf_poincare_to_hem(tf_hem_to_klein(point))


def mobius_transform(point, x, y, u):
    res = complex_mobius_transform(complex(point[0], point[1]), x, y, u)
    # print(res)
    return np.array([np.real(res), np.imag(res), point[2]])


def complex_mobius_transform(z, x, y, u):
    a = complex(x, y)
    b = complex(u, np.sqrt(-pow(u, 2) + pow(x, 2) + pow(y, 2) - 1))
    # if absolute(z) == 1:
    #    return complex(0, 0)
    return np.divide(np.add(np.multiply(a, z), np.conj(b)), np.add(np.multiply(b, z), np.conj(a)))


class SmallCircles(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 8
        circle = Circle()
        self.add(circle)

        phis = create_phis(min_dist=.4)

        first_circle_radius = .25
        hexagon = HyperbolicHexagon(phis)
        hexagon_circles = HyperbolicHexagonCircles(hexagon, first_circle_radius)
        hexagon_diagonals = HyperbolicHexagonMainDiagonals(hexagon)
        self.add(hexagon)
        self.add(hexagon_circles)
        self.add(hexagon_diagonals)

        # self.wait(duration=5)
