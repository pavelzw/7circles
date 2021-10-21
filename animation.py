from manim import *


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation

class CircleAndStraightLine(Scene):
    def construct(self):
        circle = Circle() #create circle
        line1 = Line() #creates line

        self.play(Create(circle))
        self.play(Create(line1))

class CirclesNextToEachOther(Scene):
    def construct(self):
        circle1 = Circle()
        circle2 = Circle()
        circle2.move_to([2, 0, 0]) #moves circle2 to the right by 2

        self.play(Create(circle1))
        self.play(Create(circle2))

class CircleAndGeodesic(Scene):
    def construct(self):
        circle1 = Circle()
        geod = Arc(angle=PI/2) #creates quarter cirle
        geod.move_to([-0.5,-0.5,0]) # moves to bottom left, but why 0.5??????

        self.play(Create(circle1))
        self.play(Create(geod))

