import math

import numpy as np
from manim import Create, Circle, MovingCameraScene, BLUE, Tex, Write, FadeOut

from geometry_util import radian_to_point
from hexagon import HexagonMainDiagonals, IntersectionTriangle, HexagonAngles, HyperbolicTriangle
from hyperbolic_hexagon import HyperbolicHexagon


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = [5,  # hexagon
                   6,  # diagonals
                   2,  # triangle
                   10,  # wait
                   10,  # proposition
                   5,  # wait
                   ]
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.add_foreground_mobjects(circle)
        self.play(Create(circle))

        # phis = create_phis_non_intersecting()
        phis = HexagonAngles(np.array([1.80224806, 2.30601184, 2.77326535, 3.20993453, 4.48582486, 6.15595698]))
        print(f'Phis = {phis}')
        hexagon = HyperbolicHexagon(phis, stroke_width=2)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)

        self.play(Create(hexagon),
                  run_time=timings.pop(),
                  subcaption="Betrachten wir nun einmal ein ideales Hexagon.")
        self.play(Create(diagonals),
                  run_time=timings.pop(),
                  subcaption="Wenn wir bei diesem Hexagon nun die "
                             "gegenüberliegenden Seiten verbinden, sehen wir,")

        triangle = IntersectionTriangle(diagonals, color=BLUE, stroke_width=2)
        triangle.set_fill(BLUE, opacity=0.5)
        self.play(Create(triangle),
                  run_time=timings.pop(),
                  subcaption="dass ein Dreieck in der Mitte entsteht.")

        self.wait(timings.pop())

        self.play(FadeOut(circle, triangle, hexagon, diagonals))

        self.clear()
        proposition = Tex(r'Für jedes ideale Hexagon $P$ ist der '
                          r'alternierende Umfang \\ bis auf das Vorzeichen '
                          r'genau zweimal der Umfang \\ von dem Dreieck $T_P$, '
                          r'das durch die geodätischen Diagonalen \\ aufgespannt wird.', font_size=20)
        self.play(Write(proposition,
                        run_time=timings.pop(), stroke_width=.5))

        self.wait(timings.pop())


class Scene2(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 6
        timings = []
        # timings = [.1, .1, .1, .1, .1, 10]
        timings.reverse()

        circle = Circle()
        self.play(Create(circle))

        phis = np.random.uniform(0, 2 * math.pi, 3)
        p1 = radian_to_point(phis[0])
        p2 = radian_to_point(phis[1])
        p3 = radian_to_point(phis[2]) * np.random.uniform(0.3, .7)
        print(p1, p2, p3)

        # p1 = np.array([.2, 0.4, 0])
        # p2 = np.array([1, 0, 0])
        # p3 = np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0])

        self.play(Create(HyperbolicTriangle(p1, p2, p3, stroke_width=2)))
        self.wait(5)
