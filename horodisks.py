from math import pi
from manim import *

import numpy as np
from manim import Scene, Square, Circle, Dot, Group, Text, Create, FadeIn, FadeOut, MoveAlongPath, Line, WHITE, BLUE, \
    GREEN_B, Transform, MovingCameraScene, Uncreate, \
    VGroup, DecimalNumber, RIGHT, Tex, LEFT, UP, MathTex, Write, Indicate, TransformFromCopy, RED, \
    DOWN, GREY_B, ORANGE, ArcBetweenPoints, BLUE_B, Rotate, NumberPlane, YELLOW, always_redraw, MovingCamera

from geometry_util import polar_to_point, hyperbolic_distance_function, create_min_circle_radius, moving_circle, \
    moving_line, get_intersection_in_unit_circle_of_two_tangent_circles
from hexagon_util import create_phis, create_radius_transition
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 8
        def_ball = MathTex(r'\mathrm{B}(z_0,r)=\{z:\mathrm{dist}(z,z_0)\leq r\}', font_size=20).move_to([0, -2, 0])
        def_dist_eukl = MathTex(r'\mathrm{dist_e}(a,b)=|b-a|', font_size=20).move_to([-2, -1.6, 0])
        def_dist_hyp = MathTex(r'\mathrm{dist_h}(a,b)=\ln \frac{(a-c)(b-d)}{(a-b)(c-d)}', font_size=20).move_to(
            [2, -1.6, 0])

        title_hyp = Tex(r'Hyperbolischer Raum', font_size=25, stroke_width=.5).move_to([2, 1.7, 0])
        subtitle_hyp = Tex(r'Poincar\'{e}-Modell', font_size=18, stroke_width=.5).move_to([2, 1.5, 0])
        title_eucl = Tex(r'Euklidischer Raum', font_size=25, stroke_width=.5).move_to([-2, 1.7, 0])
        self.add_foreground_mobjects(title_eucl)
        separating_line = Line(start=[0, 8, 0], end=[0, -3, 0], stroke_width=2)
        self.play(Write(title_eucl))
        self.play(FadeIn(separating_line))
        self.play(Write(title_hyp))
        self.play(Write(subtitle_hyp))
        self.wait(2)
        # euklidischer fall
        eucl_dot = Dot([-2, 0, 0], color=WHITE, radius=.03, stroke_width=2)
        eucl_dot_tex = MathTex(r'P', font_size=20).move_to([-1.9, 0.1, 0])
        eucl_circles = [Circle(arc_center=[-2, 0, 0], color=BLUE_A, stroke_width=2, radius=.25),
                        Circle(arc_center=[-2, 0, 0], color=BLUE, stroke_width=2, radius=.5),
                        Circle(arc_center=[-2, 0, 0], color=BLUE_E, stroke_width=2, radius=.75)]
        eucl_mov_points = np.array([[-2, 0, 0], [-2.5, 0, 0], [-3, 0, 0], [-1.5, 0, 0]])
        radius = Line(start=[-2, 0, 0], end=[-2.75, 0, 0], color=RED, stroke_width=2)
        grid = NumberPlane(x_range=[-8, -2, .25], y_range=[1, 9, .25], background_line_style={
            "stroke_color": GREY, "stroke_width": .5}).move_to([-3, 0, 0])
        self.play(Write(def_ball))

        # euklidische situation
        self.play(FadeIn(grid))
        self.play(FadeIn(eucl_dot), FadeIn(eucl_dot_tex))
        self.play(Create(eucl_circles[2]))
        self.play(Create(radius))
        # todo moving radius https://docs.manim.community/en/stable/examples.html?highlight=grid
        self.play(FadeOut(radius))
        self.play(Create(eucl_circles[0]), Create(eucl_circles[1]))
        circle_radius_group = VGroup(*eucl_circles, eucl_dot, eucl_dot_tex)
        self.play(Write(def_dist_eukl))
        self.wait(2)

        # hyperbolische situation
        center = [2, 0, 0]
        start_points = np.array([center, center, center, center])
        length = [1 / 2, 1 / 2, -3 / 2]  # 1 is 1 unit to the left, -3 is 3 units to the right, way of circles moving
        angles = [0, pi / 4, 4 * pi / 3]
        outer_circle = Circle(color=WHITE, radius=1).move_to(center)
        self.add_foreground_mobjects(outer_circle)
        circle = [Dot(color=WHITE, radius=0.04), Circle(color=BLUE_A, radius=0.25, stroke_width=2),
                  Circle(color=BLUE, radius=.5, stroke_width=2), Circle(color=BLUE_E, radius=0.75, stroke_width=2)]
        circles = Group(circle[0], circle[1], circle[2], circle[3]).move_to(center)
        # circle[0] is dot, circle[1] is smallest circle, circle[2] is middle circle, circle[3] is biggest circle
        self.play(FadeIn(outer_circle))
        self.play(FadeIn(circle[0]))
        self.wait(duration=2)
        self.play(Create(circle[1]), Create(circle[2]), Create(circle[3]))
        self.play(Write(def_dist_hyp))

        # circles moving along a line 3 times
        for t in range(3):
            end_points = np.array([start_points[0] - [1 * length[t], 0, 0],
                                   start_points[1] - [0.75 * length[t], 0, 0],
                                   start_points[2] - [0.5 * length[t], 0, 0],
                                   start_points[3] - [0.25 * length[t], 0, 0]])
            lines = moving_line(start_points, end_points)
            self.play(MoveAlongPath(circle_radius_group, Line(start=eucl_mov_points[t], end=eucl_mov_points[t + 1])),
                      # euclidean
                      MoveAlongPath(circle[0], lines[0]), MoveAlongPath(circle[3], lines[3]),  # hyperbolic
                      MoveAlongPath(circle[2], lines[2]), MoveAlongPath(circle[1], lines[1]), run_time=2)
            self.wait(duration=1)
            start_points = end_points

        # circles moving along part circle twice
        for t in range(2):
            arcs = moving_circle(angles[t], angles[t + 1], center)
            self.play(MoveAlongPath(circle_radius_group,  # euclidean
                                    Arc(start_angle=angles[t], angle=angles[t + 1], arc_center=[-2, 0, 0], radius=.5)),
                      MoveAlongPath(circle[0], arcs[0]), MoveAlongPath(circle[3], arcs[1]),
                      MoveAlongPath(circle[2], arcs[2]), MoveAlongPath(circle[1], arcs[3]), run_time=2)
            self.wait(duration=1)


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
