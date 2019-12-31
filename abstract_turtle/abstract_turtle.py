from abc import ABC, abstractmethod

from math import pi, sin, cos

from .model import Color, Position

class Canvas(ABC):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @abstractmethod
    def draw_line(self, start, end, color, width):
        """
        Draw a 1 width line from START to END with the given color COLOR
        """
        pass

    @abstractmethod
    def draw_circle(self, center, radius, color, width, is_filled):
        """
        Draw a circle of width 1 with the given center CENTER, radius RADIUS, and color COLOR

        Fill the circle if IS_FILLED is true.
        """
        pass

    @abstractmethod
    def fill_polygon(self, points, color):
        """
        Fill the given polygon with edge points POINTS and fill color COLOR.
        """
        pass

    @abstractmethod
    def set_bgcolor(self, color):
        """
        Fill the entire background with the given COLOR
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Clear everything in the foreground
        """
        pass

class BaseTurtle:
    """
    Manages all the basic turtle functionality. The other turtle methods can be expressed in terms of these.
    """
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__x = 0
        self.__y = 0
        self.__line_width = 1
        self.__theta = pi/2
        self.__pen_color = Color(0, 0, 0)
        self.__fill_color = Color(0, 0, 0)
        self.__pen_down = True
        self.__degrees = 360
        self.__polygon = None

    def goto(self, x, y):
        """
        Go to the given position (X, Y).
        """
        if self.__pen_down:
            self.__canvas.draw_line(self.__current_pos, Position(x, y), self.__pen_color, self.__line_width)
        self.__x = x
        self.__y = y
        if self.filling():
            self.__polygon.append(self.__current_pos)
    setpos = setposition = goto

    def forward(self, amount):
        """
        Move forward the given amount.
        """
        self.goto(self.xcor() + amount * cos(self.__theta), self.ycor() + amount * sin(self.__theta))
    fd = forward

    def setheading(self, heading):
        """
        Set the heading to the given value in degrees
        """
        self.__theta = self.__to_real_angle(heading)
    seth = setheading

    def circle(self, radius):
        """
        Draw a circle at the given point with the given RADIUS
        """
        if self.__pen_down:
            self.__canvas.draw_circle(self.__current_pos, radius, self.__line_width, self.__pen_color, True)

    def dot(self, size=None):
        """
        Draw a dot at the current location. If size is not specified, set it to
            (pensize + 4, pensize * 2)
        """
        if size is None:
            size = max(self.__line_width + 4, self.__line_width * 2)
        if self.__pen_down:
            self.__canvas.draw_circle(self.__current_pos, size, self.__line_width, self.__pen_color, False)

    def xcor(self):
        """
        Get the current x coordinate
        """
        return self.__x

    def ycor(self):
        """
        Get the current y coordinate
        """
        return self.__y

    def heading(self):
        """
        Get the current heading
        """
        return self.__from_real_angle(self.__theta)

    def degrees(self, amount):
        """
        Set the number of degrees in a circle
        """
        self.__degrees = amount

    def pendown(self):
        """
        Do draw when moving
        """
        self.__pen_down = True
    pd = down = pendown

    def penup(self):
        """
        Do not draw when moving
        """
        self.__pen_down = False
    pu = up = penup

    def pensize(self, width=None):
        """
        Set or get the pen size. If WIDTH is None, get it, otherwise set it.
        """
        if width is None:
            return self.__line_width
        self.__line_width = width
    width = pensize

    def isdown(self):
        """
        Return if the pen is down or not
        """
        return self.__pen_down

    def pencolor(self, *color):
        """
        Set the pen color as COLOR
        """
        self.__pen_color = self.__convert_color(color)

    def fillcolor(self, *color):
        """
        Set the fill color as COLOR
        """
        self.__fill_color = self.__convert_color(color)

    def filling(self):
        """
        Return whether the canvas is filling.
        """
        return self.__polygon is not None

    def begin_fill(self):
        """
        Begin setting the polygon to fill
        """
        self.__polygon = [self.__current_pos]

    def end_fill(self):
        """
        End setting the polygon to fill, and fill it in.
        """
        self.__canvas.fill_polygon(self.__polygon, self.__fill_color)
        self.__polygon = None

    def clear(self):
        """
        Clear the canvas, but do not move the turtle.
        """
        self.__canvas.clear()

    @property
    def __current_pos(self):
        return Position(self.__x, self.__y)

    def __to_real_angle(self, amount):
        return (90 - amount) * (2 * pi) / self.__degrees

    def __from_real_angle(self, angle):
        return 90 - angle * self.__degrees / (2 * pi)

    @staticmethod
    def __convert_color(color):
        return Color.of(*color)


class Turtle(BaseTurtle):
    """
    This entire class should only use public methods of the BaseTurtle class.
    """

    def backward(self, amount):
        """
        Move backward the given amount.
        """
        self.forward(-amount)
    bk = back = backward

    def right(self, amount):
        """
        Rotate right the given amount.
        """
        self.setheading(self.heading() + amount)
    rt = right

    def left(self, amount):
        """
        Rotate left the given amount.
        """
        self.right(-amount)
    lt = left

    def setx(self, x):
        """
        Move so that the x coordinate is X
        """
        self.goto(x, self.xcor())

    def sety(self, y):
        """
        Move so that the y coordinate is Y
        """
        self.goto(self.ycor(), y)

    def home(self):
        """
        Set location to (0, 0) and set heading to 0
        """
        self.goto(0, 0)
        self.setheading(0)

    def position(self):
        """
        Get the current position as a tuple
        """
        return self.xcor(), self.ycor()
    pos = position

    def distance(self, other):
        """
        Get the distance between this and the other location/turtle.
        """
        if isinstance(other, Turtle):
            return self.distance(other.position())
        x, y = other
        return ((x - self.xcor()) ** 2 + (y - self.ycor()) ** 2) ** 0.5

    def radians(self):
        """
        Set angle units to radians
        """
        return self.degrees(2 * pi)

    def color(self, color):
        """
        Set both the pen and fill colors
        """
        self.pencolor(color)
        self.fillcolor(color)

    def reset(self):
        self.home()
        self.clear()