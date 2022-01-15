from manim import Create, Circle, MovingCameraScene

from hexagon import HexagonMainDiagonals, IntersectionTriangle
from hexagon_util import create_phis, create_phis_non_intersecting
from hyperbolic_hexagon import HyperbolicHexagon


class Scene1(MovingCameraScene):
    def construct(self):
        self.camera.frame.width = 8
        self.play(Create(Circle()))
        phis = create_phis_non_intersecting()
        print(f'Phis = {phis}')
        hexagon = HyperbolicHexagon(phis, stroke_width=2)
        diagonals = HexagonMainDiagonals(hexagon, stroke_width=2)

        self.play(Create(hexagon),
                  run_time=4,
                  subcaption="Betrachten wir nun einmal ein ideales Hexagon.")
        self.play(Create(diagonals),
                  run_time=6,
                  subcaption="Wenn wir bei diesem Hexagon nun die "
                             "gegenüberliegenden Seiten verbinden, sehen wir, "
                             "dass ein Dreieck in der Mitte entsteht.")
        self.play(Create(IntersectionTriangle(diagonals)))
        self.wait(5)
