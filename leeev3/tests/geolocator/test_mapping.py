import os
import unittest

from leeev3.geolocator.mapping import Map, MapFromPicture


class TestAbstractMap(unittest.TestCase):

    def test_abstract_methods(self):
        m = Map()
        with self.assertRaises(NotImplementedError):
            m.get_color_at_pixel_position(0, 0)
        with self.assertRaises(NotImplementedError):
            m.get_color_at_physical_position(0.0, 0.0)


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
