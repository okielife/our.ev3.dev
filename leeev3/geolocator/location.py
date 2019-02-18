import math


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance_between_locations(location_1: 'Location', location_2: 'Location'):
        return math.sqrt((location_1.x - location_2.x)**2 + (location_1.y - location_2.y)**2)


class Vector(object):
    def __init__(self, x: float, y: float, angle: float = None, x2: float = None, y2: float = None):
        """
        There are two possible ways to create a vector here, from a point and an angle, or from two points
        In the first case, pass in x, y, and angle.  In the second case, pass in x, y, x2, and y2.  No other
        combinations are valid.

        :param x: Measured from the left, in meters
        :param y: Measured from the top, in meters
        :param angle: Measured counter clockwise from East, in radians, so East is 0, and North is pi/2
        :param x2: Measured from the left, in meters
        :param y2: Measured from the top, in meters
        """
        self.x = x
        self.y = y

        if x2 is not None and y2 is not None and angle is None:
            self.angle = math.atan2(y2-y, x2-x)  # TODO: might assume the wrong DeltaY direction?
        elif angle is not None and x2 is None and y2 is None:
            self.angle = angle
        else:
            raise Exception('Bad input argument combination in Vector constructor')

    def get_end_xy_at_radius(self, radius: float):
        x2 = self.x + radius * math.cos(self.angle)
        y2 = self.y + radius * math.sin(self.angle)
        return [x2, y2]
