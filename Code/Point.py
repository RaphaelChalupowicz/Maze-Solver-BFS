"""POINT CLASS 

()

"""


class Point(object):  # Define a Point class

    def __init__(self, x=0, y=0):  # Constructor method to initialize a Point object with optional x and y coordinates
        self.x = x  # Initialize x coordinate
        self.y = y  # Initialize y coordinate

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
