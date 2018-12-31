from math import sqrt

from leeev3.geolocator.tolerances import Tolerances


class LineSegment(object):

    def __init__(self, x_1: float, y_1: float, x_2: float, y_2: float):
        self.x_1 = x_1
        self.x_2 = x_2
        self.y_1 = y_1
        self.y_2 = y_2

        if abs(self.x_2 - self.x_1) < Tolerances.SlopeCalculationMinimumDeltaX:
            self.slope = None
            self.intercept = None
        else:
            self.slope = (self.y_2 - self.y_1) / (self.x_2 - self.x_1)
            self.intercept = y_1 - self.slope * x_1


class ParallelLineSegmentPair(object):
    """
    Represents a pair of parallel line segments
    """
    def __init__(self, line_1: LineSegment, line_2: LineSegment):
        """
        Constructs a pair of line segments, assuming they are parallel.  Use the are_parallel method to check before
        constructing it here
        :param line_1:
        :param line_2:
        """
        self.line_1 = line_1
        self.line_2 = line_2
        self.average_slope = (line_1.slope + line_2.slope) / 2.0

    @staticmethod
    def are_parallel(line_1: LineSegment, line_2: LineSegment) -> bool:
        return abs(line_1.slope - line_2.slope) < Tolerances.ParallelLineSlopeDelta

    def distance_between(self) -> float:
        """
        Calculates the distance between the two parallel lines

        https://math.tutorvista.com/geometry/distance-between-two-parallel-lines.html?view=simple

        :return:
        """
        return abs(self.line_1.intercept - self.line_2.intercept) / sqrt(1 + self.average_slope ** 2)
