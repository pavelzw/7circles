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
        line1 = Line() #creates line
        geod = Arc(angle=PI/2) #creates quarter cirle
        geod.move_to([-0.5,-0.5,0]) # moves to bottom left, but why 0.5??????

        self.play(Create(circle1))
        self.play(Create(line1))
        self.play(Create(geod))

class Horodisk(Scene):
    def construct(self):
        circle1 = Circle(color = WHITE, radius = 2)
        circle2 = Circle(color = WHITE, radius = 1.5)
        circle3 = Circle(color = WHITE, radius = 1)
        circle4 = Circle(color = WHITE, radius = 0.5)
        dot = Dot()

        self.play(Create(circle1))
        self.play(Create(circle2))
        self.play(Create(circle3))
        self.play(Create(circle4))
        self.play(Create(dot))

    #moving horodisks and dot to the right
        line1 = Line(start = ORIGIN, end = [2,0,0] ) #to coordinate moving of horodisks and point
        line2 = Line(start = ORIGIN, end = [0.5,0,0])
        line3 = Line(start = ORIGIN, end = [1,0,0])
        line4 = Line(start = ORIGIN, end = [1.5,0,0])

        self.play(MoveAlongPath(dot, line1),MoveAlongPath(circle2, line2),MoveAlongPath(circle3, line3),MoveAlongPath(circle4, line4)) #moves dot to the right

