import numpy as np
from manim import MovingCameraScene, Rectangle, WHITE, GREEN_B, PURPLE, DARK_GREY, GREY, ORANGE, YELLOW, Circle, Dot, \
    FadeIn, Write, Create, Flash, RED, BLUE, MathTex, LEFT, ReplacementTransform, GREEN_E, PURPLE_E, DOWN, Group, \
    Square, FadeOut, Transform, TransformFromCopy, ImageMobject, Polygon, Line, UP, RIGHT, Arrow, VGroup, Uncreate, \
    VMobject, BLACK, DecimalNumber, ArcBetweenPoints, GREY_B

from animation_constants import OUTER_CIRCLE_COLOR, OUTER_CIRCLE_STROKE_WIDTH, HEXAGON_STROKE_WIDTH
from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import get_intersection_from_angles
from hexagon import HexagonAngles, HexagonCircles
from geometry_util import get_intersections_of_n_tangent_circles, get_intersections_of_circles_with_unit_circle, \
    get_intersection_from_angles, get_intersection_points_of_n_tangent_circles, \
    get_intersection_in_unit_circle_of_two_tangent_circles, polar_to_point, \
    get_both_intersections_line_with_unit_circle, tf_klein_to_poincare, hyperbolic_distance_function
from hexagon import HexagonAngles, HexagonCircles, HexagonMainDiagonals
from hyperbolic_polygon import HyperbolicPolygon, HyperbolicArcBetweenPoints


class Rectangles(MovingCameraScene):
    def construct(self):
        # todo implement
        pass


class Scene1(MovingCameraScene):
    def construct(self):
        # todo create different hexagons

        self.camera.frame.scale(.3)
        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=2)

        # keyframe hexagons
        phis1 = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))
        phis2 = HexagonAngles(np.array([.3, 1.2, 2.7, 3.6, 4.2]))
        phis3 = HexagonAngles(np.array([.7, 1.4, 2.3, 3.0, 4.1]))

        first_circle_radius = 0.4

        self.add(circle)
        self.add_foreground_mobject(circle)

        frame_rate = 60
        frame_time = 1 / 60
        run_time = 2
        frames = run_time * frame_rate

        i = 0
        phis = np.array([phis1[j] + ((i * (phis2[j] - phis1[j])) / frames) for j in range(5)])
        hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
        hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
        diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
        diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                    color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

        self.add(*hex_circles.circles, *diagonals, diagonal_intersection)

        for i in range(1, frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis1[j] + ((i * (phis2[j] - phis1[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        for i in range(frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis2[j] + ((i * (phis3[j] - phis2[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        for i in range(frames):
            prev_hex_circles = hex_circles
            prev_diagonals = diagonals
            prev_diagonal_intersection = diagonal_intersection

            phis = np.array([phis3[j] + ((i * (phis1[j] - phis3[j])) / frames) for j in range(5)])
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=HEXAGON_COLOR, stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2, color=INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=DIAGONAL_COLOR, stroke_width=2)
            diagonal_intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                                        color=DIAGONAL_INTERSECTION_COLOR, radius=.05)

            self.play(Transform(prev_hex_circles[0], hex_circles[0]),
                      Transform(prev_hex_circles[1], hex_circles[1]),
                      Transform(prev_hex_circles[2], hex_circles[2]),
                      Transform(prev_hex_circles[3], hex_circles[3]),
                      Transform(prev_hex_circles[4], hex_circles[4]),
                      Transform(prev_hex_circles[5], hex_circles[5]),
                      Transform(prev_diagonals[0], diagonals[0]),
                      Transform(prev_diagonals[1], diagonals[1]),
                      Transform(prev_diagonals[2], diagonals[2]),
                      Transform(prev_diagonal_intersection, diagonal_intersection),
                      run_time=frame_time
                      )
            self.remove(*prev_hex_circles, *prev_diagonals, prev_diagonal_intersection)

        self.add(*hex_circles, *diagonals, diagonal_intersection)


class Scene2(MovingCameraScene):
    def construct(self):
        pass


class Scene3(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 4

        OUTER_CIRCLE_COLOR = WHITE
        INNER_CIRCLE_COLOR = GREEN_B
        INNER_INTERSECTION_COLOR = PURPLE
        OUTER_INTERSECTION_COLOR = DARK_GREY
        HEXAGON_COLOR = GREY
        DIAGONAL_COLOR = ORANGE
        DIAGONAL_INTERSECTION_COLOR = YELLOW

        circle = Circle(color=OUTER_CIRCLE_COLOR, stroke_width=OUTER_CIRCLE_STROKE_WIDTH)
        self.add(circle)
        self.add_foreground_mobject(circle)

        phis = HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3]))

        hexagon = HyperbolicPolygon.from_polar(phis, color=HEXAGON_COLOR, add_dots=False,
                                               stroke_width=HEXAGON_STROKE_WIDTH)
        inner_circles = HexagonCircles(hexagon, first_circle_radius=.4, color=GREEN_B,
                                       stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, color=ORANGE, stroke_width=HEXAGON_STROKE_WIDTH)

        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(diagonals.arc1.circle_center,
                                                                              diagonals.arc1.radius,
                                                                              diagonals.arc2.circle_center,
                                                                              diagonals.arc2.radius)
        intersection_dot = Dot(intersection, color=YELLOW, radius=.03)

        self.play(FadeIn(hexagon, inner_circles, diagonals, intersection_dot))
        self.add_foreground_mobjects(hexagon, diagonals, intersection_dot, circle)
        self.wait(1)

        # transform hyperbolic hexagon to euclidean hexagon
        euclidean_hexagon = EuclideanHexagon(phis, color=GREY, stroke_width=2)
        euclidean_diagonals = get_diagonals(hexagon, color=ORANGE, stroke_width=2)
        euclidean_intersection_dot = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]), color=YELLOW,
                                         radius=.03)
        self.add_foreground_mobjects(hexagon, diagonals, intersection_dot, circle)

        self.play(*[ReplacementTransform(hexagon.arcs[i], euclidean_hexagon.edges[i]) for i in range(6)],
                  ReplacementTransform(diagonals.arc1, euclidean_diagonals[0].reverse_direction()),
                  ReplacementTransform(diagonals.arc2, euclidean_diagonals[1].reverse_direction()),
                  ReplacementTransform(diagonals.arc3, euclidean_diagonals[2].reverse_direction()),
                  ReplacementTransform(intersection_dot, euclidean_intersection_dot),
                  run_time=3)
        self.wait(2)

        # quick fix such that hexagon gets transformed into old shape
        hexagon = HyperbolicPolygon.from_polar(phis, color=HEXAGON_COLOR, add_dots=False,
                                               stroke_width=HEXAGON_STROKE_WIDTH)
        diagonals = HexagonMainDiagonals(hexagon, color=ORANGE, stroke_width=HEXAGON_STROKE_WIDTH)

        intersection = get_intersection_in_unit_circle_of_two_tangent_circles(diagonals.arc1.circle_center,
                                                                              diagonals.arc1.radius,
                                                                              diagonals.arc2.circle_center,
                                                                              diagonals.arc2.radius)
        intersection_dot = Dot(intersection, color=YELLOW, radius=.03)

        self.play(*[ReplacementTransform(euclidean_hexagon.edges[i], hexagon.arcs[i]) for i in range(6)],
                  ReplacementTransform(euclidean_diagonals[0], diagonals.arc1),
                  ReplacementTransform(euclidean_diagonals[1], diagonals.arc2),
                  ReplacementTransform(euclidean_diagonals[2], diagonals.arc3),
                  ReplacementTransform(euclidean_intersection_dot, intersection_dot),
                  run_time=3)
        self.wait(2)


class Scene4(MovingCameraScene):
    def construct(self):
        center = np.array([0, 0, 0])

        klein_origin = np.array([3.5, 0, 0])
        poincare_origin = np.array([-3.5, 0, 0])

        MY_BLUE = "#22c1dd"

        klein_model = ImageMobject("tessellation_klein.png").scale(0.7).move_to(klein_origin)
        poincare_model = ImageMobject("tessellation_poincare.png").scale(0.7).move_to(poincare_origin)

        scale_back = 2.5
        phis = [[0.4, 2], [3.3, 5.2]]

        kcircle = Circle(color=MY_BLUE, stroke_width=1).scale(scale_back).move_to(klein_origin)
        pcircle = Circle(color=MY_BLUE, stroke_width=1).scale(scale_back).move_to(poincare_origin)

        p_geodesics_raw = [HyperbolicArcBetweenPoints(polar_to_point(x), polar_to_point(y)) for [x, y] in phis]
        p_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(poincare_origin) for geo in
                       p_geodesics_raw]

        k_geodesics_raw = [Line(polar_to_point(x), polar_to_point(y)) for [x, y] in phis]
        k_geodesics = [geo.scale(scale_back).move_to(geo.get_center() * scale_back).shift(klein_origin) for geo in
                       k_geodesics_raw]

        arrow_lr = Arrow(start=2.5 * LEFT, end=2.5 * RIGHT, stroke_width=4, max_tip_length_to_length_ratio=.5)
        arrow_rl = Arrow(start=2.5 * RIGHT, end=2.5 * LEFT, stroke_width=4, max_tip_length_to_length_ratio=.5)
        arrow_group = VGroup(arrow_lr, arrow_rl).arrange(DOWN)

        p_geo0 = p_geodesics[0].copy()
        p_geo0 = p_geo0.shift(-poincare_origin).scale(0.7).move_to(p_geo0.get_center() * 0.7).shift(
            poincare_origin + 1.5 * LEFT)
        p_geo0_copy = p_geo0.copy()

        p_geo1 = p_geodesics[1].copy()
        p_geo1 = p_geo1.shift(-poincare_origin).scale(0.7).move_to(p_geo1.get_center() * 0.7).shift(
            poincare_origin + 1.5 * LEFT)

        k_geo0 = k_geodesics[0].copy()
        k_geo0 = k_geo0.shift(-klein_origin).scale(0.7).move_to(k_geo0.get_center() * 0.7).shift(
            klein_origin + 1.5 * RIGHT)

        k_geo1 = k_geodesics[1].copy()
        k_geo1 = k_geo1.shift(-klein_origin).scale(0.7).move_to(k_geo1.get_center() * 0.7).shift(
            klein_origin + 1.5 * RIGHT)
        k_geo1_copy = k_geo1.copy()

        # todo here
        poincare_model.scale(0.7).shift(1.5 * LEFT)
        klein_model.scale(0.7).shift(1.5 * RIGHT)

        self.play(FadeIn(poincare_model, klein_model), Write(arrow_group))

        self.add(pcircle.scale(0.7).shift(1.5 * LEFT), kcircle.scale(0.7).shift(1.5 * RIGHT))

        self.wait(1)
        self.play(Create(p_geo0), FadeOut(poincare_model))
        self.add(p_geo0_copy)

        self.wait(1)

        self.play(Transform(p_geo0, k_geo0), FadeOut(klein_model))

        self.wait(1)

        self.play(Create(k_geo1))
        self.add(k_geo1_copy)

        self.wait(1)

        self.play(Transform(k_geo1, p_geo1))

        self.wait(3)


class Scene5(MovingCameraScene):
    def construct(self):
        self.camera.frame.move_to([1, 0, 0])
        self.camera.frame.width = 6
        radius_disks = [.5, .4]
        circle = Circle(color=WHITE, stroke_width=HEXAGON_STROKE_WIDTH)
        phis = [0.47654, 2.065432, 2.876, 3.87623, 5.024, 5.673]

        hexagon = HyperbolicPolygon.from_polar(phis, add_dots=False, color=GREY_B, stroke_width=2)
        arc_colored = HyperbolicPolygon.from_polar(phis, add_dots=False, color=ORANGE, stroke_width=2).arcs[0]

        point1 = hexagon.polygon_points[0]
        point2 = hexagon.polygon_points[1]
        arc = hexagon.arcs[0]

        distance_text = MathTex(r'\mathrm{dist_h}(a,b) =', font_size=20).move_to([1.2, 0, 0],
                                                                                 aligned_edge=LEFT)  # partially new
        infinity = MathTex(r'\infty', font_size=20).next_to(distance_text, buff=.05)
        s_0 = Dot(hexagon.polygon_points[0], radius=.02, color=ORANGE)
        s_1 = Dot(hexagon.polygon_points[1], radius=.02, color=ORANGE)
        a = MathTex(r'a', font_size=15, color=ORANGE).next_to(s_0, direction=0.16 * DOWN + 0.01 * LEFT)  # new
        b = MathTex(r'b', font_size=15, color=ORANGE).next_to(s_1, direction=0.18 * DOWN + 0.01 * LEFT)  # new
        self.play(FadeIn(hexagon, circle, arc_colored, a, b, s_0, s_1),
                  Write(VGroup(distance_text, infinity), stroke_width=.5))
        self.add_foreground_mobjects(a, b, circle)
        self.wait(2)
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
            new_arc = ArcBetweenPoints(interp_point2, interp_point1, color=ORANGE,
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
                          Transform(s_0, Dot(interp_point1, radius=.02, color=ORANGE)),
                          Transform(s_1, Dot(interp_point2, radius=.02, color=ORANGE)),
                          Transform(distance_number, infinity),
                          run_time=1 / 60, rate_func=lambda a: a)
            else:
                self.play(Transform(arc_colored, new_arc),
                          Transform(s_0, Dot(interp_point1, radius=.02, color=ORANGE)),
                          Transform(s_1, Dot(interp_point2, radius=.02, color=ORANGE)),
                          distance_number.animate.set_value(distance), run_time=1 / 60,
                          rate_func=lambda a: a)
        self.remove(s_0, s_1)
        self.wait(2)
        everything = VGroup(*filter(lambda x: isinstance(x, VMobject), self.mobjects))
        self.play(FadeOut(everything))


class Scene6(MovingCameraScene):
    def construct(self):
        pass
