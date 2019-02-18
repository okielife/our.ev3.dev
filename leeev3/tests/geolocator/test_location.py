import unittest

from leeev3.geolocator.location import Location, Vector


class TestLocation(unittest.TestCase):

    def test_location_distance(self):
        l_1 = Location(0, 0)
        l_2 = Location(1, 0)
        l_3 = Location(0, 2)

        self.assertEqual(1, Location.distance_between_locations(l_1, l_2))
        self.assertEqual(2, Location.distance_between_locations(l_1, l_3))


class TestVector(unittest.TestCase):

    def test_vector_construction_by_points(self):
        v = Vector(2.0, 2.0, x2=1.0, y2=2.0)
        self.assertAlmostEqual(3.14, v.angle, 2)

    def test_vector_construction_by_angle(self):
        v = Vector(2.0, 2.0, angle=3.14/2.0)
        self.assertAlmostEqual(3.14/2.0, v.angle, 2)

    def test_bad_vector_arguments(self):
        with self.assertRaises(Exception):
            Vector(1, 1, x2=1, angle=3)
            # TODO: Add more combinations

    def test_get_end_xy_at_radius(self):
        v = Vector(2.0, 2.0, x2=2.0, y2=3.0)
        self.assertAlmostEqual(3.14/2.0, v.angle, 2)
        end_point = v.get_end_xy_at_radius(1.0)
        self.assertAlmostEqual(2.0, end_point[0], 2)
        self.assertAlmostEqual(3.0, end_point[1], 2)
