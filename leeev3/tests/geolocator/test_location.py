import unittest

from leeev3.geolocator.location import Location


class TestLocation(unittest.TestCase):

    def test_location_distance(self):
        l_1 = Location(0, 0)
        l_2 = Location(1, 0)
        l_3 = Location(0, 2)

        self.assertEqual(1, Location.distance_between_locations(l_1, l_2))
        self.assertEqual(2, Location.distance_between_locations(l_1, l_3))
