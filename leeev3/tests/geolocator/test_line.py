import unittest

from leeev3.geolocator.line import LineSegment


class TestLineSegment(unittest.TestCase):

    def test_simple_lines(self):
        ls = LineSegment(x_1=0, y_1=0, x_2=1, y_2=1)
        self.assertEqual(1, ls.slope)
        self.assertEqual(0, ls.intercept)

        ls = LineSegment(x_1=0, y_1=1, x_2=1, y_2=2)
        self.assertEqual(1, ls.slope)
        self.assertEqual(1, ls.intercept)

    def test_horizontal_lines(self):
        ls = LineSegment(x_1=0, y_1=0, x_2=1, y_2=0)
        self.assertEqual(0, ls.slope)
        self.assertEqual(0, ls.intercept)

        ls = LineSegment(x_1=0, y_1=1, x_2=1, y_2=1)
        self.assertEqual(0, ls.slope)
        self.assertEqual(1, ls.intercept)

    def test_vertical_lines(self):
        ls = LineSegment(x_1=0, y_1=0, x_2=0, y_2=1)
        self.assertIsNone(ls.slope)
        self.assertIsNone(ls.intercept)

        ls = LineSegment(x_1=1, y_1=1, x_2=1, y_2=2)
        self.assertIsNone(ls.slope)
        self.assertIsNone(ls.intercept)
