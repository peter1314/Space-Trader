"""File for storing the Coordinate class"""
from math import sqrt

class Coordinate:
    """Class for storing the x and y coordinates of a region"""
    def __init__(self, xray, yankee):
        """Creates a cordinate from a given x and y"""
        self.xray = xray
        self.yankee = yankee

    @classmethod
    def distance_coord(cls, coordinate1, coordinate2):
        """Creates a coordinate representing the vector between two coordinates"""
        return cls(coordinate1.xray - coordinate2.xray, coordinate1.yankee - coordinate2.yankee)

    def pretty_print(self):
        """Returns stylized string with the coordinates information"""
        return "({}, {})".format(self.xray, self.yankee)

    def distance_to(self, other):
        """Returns the distance between two coordinates"""
        return sqrt((self.xray - other.xray)**2 +
                    (self.yankee - other.yankee)**2)
