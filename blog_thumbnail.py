"""Scene1 from introduction.py with configurable colors, used for the blog thumbnail."""
import numpy as np
from manim import (BLACK, GREEN_B, GREEN_E, GREY, GREY_D, MovingCameraScene, ORANGE, WHITE, YELLOW,
                   YELLOW_E, Circle, Dot, Transform, config)

from euclidean_hexagon import EuclideanHexagon, get_diagonals
from geometry_util import get_intersection_from_angles
from hexagon import HexagonAngles, HexagonCircles


class ThumbnailBase(MovingCameraScene):
    OUTER_CIRCLE_COLOR = WHITE
    INNER_CIRCLE_COLOR = GREEN_B
    HEXAGON_COLOR = GREY
    DIAGONAL_COLOR = ORANGE
    DIAGONAL_INTERSECTION_COLOR = YELLOW
    BACKGROUND = BLACK

    def construct(self):
        config.background_color = self.BACKGROUND
        self.camera.background_color = self.BACKGROUND
        self.camera.frame.scale(.3)

        circle = Circle(color=self.OUTER_CIRCLE_COLOR, stroke_width=2)
        keyframes = [
            HexagonAngles(np.array([.3, 1.6, 2.2, 3, 4.3])),
            HexagonAngles(np.array([.3, 1.2, 2.7, 3.6, 4.2])),
            HexagonAngles(np.array([.7, 1.4, 2.3, 3.0, 4.1])),
        ]
        first_circle_radius = 0.4
        frame_rate = 60
        frame_time = 1 / frame_rate
        run_time = 4
        frames = run_time * frame_rate

        self.add(circle)
        self.add_foreground_mobject(circle)

        def build(phis):
            hexagon = EuclideanHexagon(HexagonAngles(np.array(phis)), color=self.HEXAGON_COLOR,
                                       stroke_width=2)
            hex_circles = HexagonCircles(hexagon, first_circle_radius, stroke_width=2,
                                         color=self.INNER_CIRCLE_COLOR)
            diagonals = get_diagonals(hexagon, color=self.DIAGONAL_COLOR, stroke_width=2)
            intersection = Dot(get_intersection_from_angles(phis[0], phis[3], phis[1], phis[4]),
                               color=self.DIAGONAL_INTERSECTION_COLOR, radius=.05)
            return hex_circles, diagonals, intersection

        def interp(a, b, i):
            return np.array([a[j] + ((i * (b[j] - a[j])) / frames) for j in range(5)])

        hex_circles, diagonals, intersection = build(interp(keyframes[0], keyframes[1], 0))
        self.add(*hex_circles.circles, *diagonals, intersection)

        for k in range(3):
            start, end = keyframes[k], keyframes[(k + 1) % 3]
            for i in range(1 if k == 0 else 0, frames):
                prev = (hex_circles, diagonals, intersection)
                hex_circles, diagonals, intersection = build(interp(start, end, i))
                self.play(
                    *[Transform(prev[0][n], hex_circles[n]) for n in range(6)],
                    *[Transform(prev[1][n], diagonals[n]) for n in range(3)],
                    Transform(prev[2], intersection),
                    run_time=frame_time,
                )
                self.remove(*prev[0], *prev[1], prev[2])

        self.add(*hex_circles, *diagonals, intersection)


class ThumbnailDark(ThumbnailBase):
    pass


class ThumbnailLight(ThumbnailBase):
    OUTER_CIRCLE_COLOR = BLACK
    INNER_CIRCLE_COLOR = GREEN_E
    HEXAGON_COLOR = GREY_D
    DIAGONAL_COLOR = ORANGE
    DIAGONAL_INTERSECTION_COLOR = YELLOW_E
    BACKGROUND = WHITE
