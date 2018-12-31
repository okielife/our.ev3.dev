import math


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def distance_between_locations(location_1: 'Location', location_2: 'Location'):
        return math.sqrt((location_1.x - location_2.x)**2 + (location_1.y - location_2.y)**2)
