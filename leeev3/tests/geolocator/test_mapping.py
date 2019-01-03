import os
import unittest

from leeev3.geolocator.mapping import Map, MapFromPicture, MapFromData


class TestBaseMap(unittest.TestCase):

    def test_abstract_methods(self):
        m = Map()
        with self.assertRaises(NotImplementedError):
            m.get_color_at_pixel_position(0, 0)
        with self.assertRaises(NotImplementedError):
            m.get_color_at_physical_position(0.0, 0.0)

    def test_sampling_points(self):
        # first an easy one, the points right in the middle
        points = Map.sample_physical_positions(1, 1, 2, 2)
        self.assertEqual(4, len(points))
        self.assertEqual(2, len([1 for p in points if p[0] > 1]))
        self.assertEqual(2, len([1 for p in points if p[0] < 1]))
        self.assertEqual(2, len([1 for p in points if p[1] > 1]))
        self.assertEqual(2, len([1 for p in points if p[1] < 1]))
        # then how about each direction pushed off of the board (one at a time to catch each corner case)
        points = Map.sample_physical_positions(1.999, 1, 2, 2)
        self.assertEqual(4, len(points))
        self.assertEqual(2, len([1 for p in points if p[0] == 2]))  # should have two pushed up against the right side
        points = Map.sample_physical_positions(0.001, 1, 2, 2)
        self.assertEqual(4, len(points))
        self.assertEqual(2, len([1 for p in points if p[0] == 0]))  # should have two pushed up against the left side
        points = Map.sample_physical_positions(1, 1.999, 2, 2)
        self.assertEqual(4, len(points))
        self.assertEqual(2, len([1 for p in points if p[1] == 2]))  # should have two pushed up against the bottom (y=2)
        points = Map.sample_physical_positions(1, 0.001, 2, 2)
        self.assertEqual(4, len(points))
        self.assertEqual(2, len([1 for p in points if p[1] == 0]))  # should have two pushed up against the top (y=0)
        # now how about just completely off the board in any direction
        with self.assertRaises(Exception):
            Map.sample_physical_positions(-1, 1, 2, 2)
        with self.assertRaises(Exception):
            Map.sample_physical_positions(3, 1, 2, 2)
        with self.assertRaises(Exception):
            Map.sample_physical_positions(1, -1, 2, 2)
        with self.assertRaises(Exception):
            Map.sample_physical_positions(1, 3, 2, 2)


class TestMapFromPicture(unittest.TestCase):

    def setUp(self):
        self.cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.resource_dir = os.path.join(self.cur_dir_path, 'resources')

    def test_map_with_scale_one(self):
        small_image_88_path = os.path.join(self.resource_dir, 'small88.png')
        mfp = MapFromPicture(small_image_88_path, 8, 8)
        self.assertEqual((244, 242, 242), mfp.get_color_at_pixel_position(0, 0))
        self.assertEqual((244, 242, 242), mfp.get_color_at_physical_position(0.5, 0.5))
        self.assertEqual((231, 197, 197), mfp.get_color_at_pixel_position(5, 4))
        self.assertEqual((231, 197, 197), mfp.get_color_at_physical_position(5.5, 4.5))

    def test_map_with_scale_two(self):
        small_image_88_path = os.path.join(self.resource_dir, 'small88.png')
        mfp = MapFromPicture(small_image_88_path, 16, 16)
        self.assertEqual((244, 242, 242), mfp.get_color_at_pixel_position(0, 0))
        self.assertEqual((244, 242, 242), mfp.get_color_at_physical_position(0, 0))
        self.assertEqual((231, 197, 197), mfp.get_color_at_pixel_position(5, 4))
        self.assertEqual((231, 197, 197), mfp.get_color_at_physical_position(11, 9))

    def test_out_of_range_dimension(self):
        pass


class TestMapFromData(unittest.TestCase):

    def test_stretched_valid_map(self):
        pixel_data = [
            [(1, 1, 1), (2, 2, 2), (3, 3, 3), (4, 4, 4)],
            [(5, 5, 5), (6, 6, 6), (7, 7, 7), (8, 8, 8)],
            [(8, 8, 8), (7, 7, 7), (6, 6, 6), (5, 5, 5)],
            [(4, 4, 4), (3, 3, 3), (2, 2, 2), (1, 1, 1)],
        ]
        mfd = MapFromData(pixel_data, actual_map_width=2, actual_map_height=4)
        self.assertEqual((7, 7, 7), mfd.get_color_at_pixel_position(2, 1))
        self.assertEqual((5, 5, 5), mfd.get_color_at_physical_position(x=1.75, y=2.5))

    def test_bad_map_data(self):
        with self.assertRaises(Exception):
            # noinspection PyTypeChecker
            MapFromData(8, 1, 2)
        with self.assertRaises(Exception):
            MapFromData([8, 0, 2], 2, 1)
        with self.assertRaises(Exception):
            MapFromData([[(1, 1, 1), (1, 1, 1)], [(1, 1, 1)]], 3, 1)
        with self.assertRaises(Exception):
            MapFromData([[1]], 1, 1)
