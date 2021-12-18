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


def get_intersection_line_unit_circle(start_point, direction):
    # solves (x + at)^2 + (y + bt)^2 = 1
    # with x^2 + y^2 = 1
    x, y, _ = start_point
    a, b, _ = direction

    t = - 2 * (a * x + b * y) / (a ** 2 + b ** 2)
    return start_point + t * direction


def get_last_phi(phis):
    assert phis.shape == (5,)
    p0 = radian_to_point(phis[0])
    p1 = radian_to_point(phis[1])
    p2 = radian_to_point(phis[2])
    p3 = radian_to_point(phis[3])
    p4 = radian_to_point(phis[4])
    intersection = get_intersection(p0, p3, p1, p4)
    point_on_circle = get_intersection_line_unit_circle(p2, intersection - p2)
    phi = np.arctan2(point_on_circle[1], point_on_circle[0])
    return phi


def get_intersection(p1, p2, p3, p4):
    # uses this formula: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection#Given_two_points_on_each_line
    x1, y1, _ = p1
    x2, y2, _ = p2
    x3, y3, _ = p3
    x4, y4, _ = p4
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    intersection1 = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    intersection2 = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
    intersection1 /= denominator
    intersection2 /= denominator
    return np.array([intersection1, intersection2, 0])


def create_phi_transition(phi_old, phi_new, step_size=10):
    assert phi_old.shape == phi_new.shape
    transition = np.empty(shape=(step_size, phi_old.shape[0]))
    for t in range(step_size):
        transition[t] = phi_old * (1 - t / step_size) + phi_new * t / step_size
    return transition


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


def get_intersections_of_circles(c0, r0, c1, r1):
    # circle 1: center c0, radius r0
    # circle 2: center c1, radius r1

    x0, y0, _ = c0
    x1, y1, _ = c1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        raise ValueError(f'Circles non intersecting\n{c0}\n{r0}\n{c1}\n{r1}')
    # One circle within other
    if d < abs(r0 - r1):
        raise ValueError('One circle within other\n{c0}\n{r0}\n{c1}\n{r1}')
    # coincident circles
    if d == 0 and r0 == r1:
        raise ValueError('Coincident circles\n{c0}\n{r0}\n{c1}\n{r1}')
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        # we only want the one intersection with ||.|| < 1
        intersection1 = np.array((x3, y3, 0))
        intersection2 = np.array((x4, y4, 0))
        if np.abs(np.linalg.norm(intersection1) - 1) < 0.0001:
            return intersection2
        return intersection1


def create_phis(min_dist=0.4):
    phis = np.sort(np.random.uniform(0, 2 * PI, 6))
    while np.min(np.abs(np.roll(phis, shift=1) - phis)) < min_dist or phis[0] < phis[5] - 2 * PI + min_dist:
        phis = np.sort(np.random.uniform(0, 2 * PI, 6))

    new_phi = get_last_phi(phis[:-1])
    phis[-1] = new_phi + 2 * PI if new_phi < 0 else new_phi

    return phis


def get_circle_middle(phi_1, phi_2):
    if sin(phi_2) == 0:  # phi_2 != 0, PI because else we divide by 0
        tmp = phi_2
        phi_2 = phi_1
        phi_1 = tmp
    x = (-sin(phi_1) + sin(phi_2)) / (-cos(phi_2) * sin(phi_1) + cos(phi_1) * sin(phi_2))
    y = (1 - x * cos(phi_2)) / sin(phi_2)
    return np.array((x, y, 0))


def get_next_circle(center, radius, phi_old, phi_new):
    arc = get_arc(phi_old, phi_new)
    arc_center = get_circle_middle(phi_old, phi_new)
    intersection = get_intersections_of_circles(center, radius, arc_center, arc.radius)
    assert intersection is not None
    middle_between_phi_new_and_intersection = (intersection + radian_to_point(phi_new)) / 2
    direction = intersection - radian_to_point(phi_new)
    orthogonal_direction = np.array([-direction[1], direction[0], 0])
    center_of_circle = get_intersection(radian_to_point(phi_new), np.array([0, 0, 0]),
                                        middle_between_phi_new_and_intersection,
                                        orthogonal_direction + middle_between_phi_new_and_intersection)
    return center_of_circle, np.linalg.norm(center_of_circle - radian_to_point(phi_new))


class SmallCircles(MovingCameraScene):
    def construct(self):
        self.camera.frame.set_width(8)
        circle = Circle()
        self.add(circle)

        phis = create_phis(min_dist=.4)

        first_circle_radius = .25
        p0 = radian_to_point(phis[0])
        first_circle_center = p0 * (1 - first_circle_radius)
        circle = Circle(radius=first_circle_radius, color=BLUE).move_to(first_circle_center)
        self.add(circle)

        new_center, new_radius = first_circle_center, first_circle_radius

        for i in range(1, 6):
            new_center, new_radius = get_next_circle(new_center, new_radius, phis[i - 1], phis[i])
            self.add(Circle(radius=new_radius, color=BLUE).move_to(new_center))

        self.add(create_arcs(phis))

        self.add(get_arc(phis[0], phis[3]))
        self.add(get_arc(phis[1], phis[4]))
        self.add(get_arc(phis[2], phis[5]))
        # self.wait(duration=5)
