import os
import unittest

from leeev3.geolocator.locator import LocatorA
from leeev3.geolocator.mapping import MapFromPicture


color_rgb_from_name = {
    'blk': (0, 0, 0),
    'red': (255, 0, 0),
    'grn': (0, 255, 0),
    'blu': (0, 0, 255),
    'cyn': (0, 255, 255),
    'pnk': (255, 0, 255),
    'ylo': (255, 255, 0),
    'wht': (255, 255, 255),
}
color_name_from_rgb = {v: k for k, v in color_rgb_from_name.items()}


class TestLocatorA(unittest.TestCase):

    # For reference, here is the layout of colors in the picture, with the mapping above to give RGB
    #      00   01   02   03   04   05   06   07   08   09   10   11   12   13   14   15
    # 00: ylo, cyn, blu, ylo, cyn, blu, ylo, wht, grn, blk, cyn, blk, pnk, grn, wht, blu
    # 01: red, wht, pnk, blu, wht, pnk, blu, blk, cyn, pnk, wht, cyn, cyn, blk, red, wht
    # 02: blu, red, ylo, wht, cyn, wht, cyn, red, wht, blu, ylo, red, wht, pnk, ylo, red
    # 03: wht, cyn, pnk, cyn, blu, grn, blk, pnk, ylo, grn, pnk, ylo, grn, blk, blk, cyn
    # 04: pnk, blk, grn, red, blk, pnk, wht, blu, blk, red, wht, cyn, red, wht, grn, wht
    # 05: red, cyn, red, wht, ylo, wht, blu, ylo, grn, wht, cyn, blk, wht, grn, wht, blu
    # 06: wht, pnk, wht, blu, red, grn, ylo, blu, red, pnk, cyn, ylo, blu, cyn, red, wht
    # 07: blu, blk, grn, blu, cyn, wht, grn, wht, blk, wht, red, blu, wht, red, wht, blu
    # 08: ylo, cyn, pnk, wht, pnk, ylo, grn, red, blu, pnk, blk, ylo, blu, red, blk, wht
    # 09: red, blk, blu, ylo, cyn, blu, wht, ylo, blk, wht, cyn, blu, blu, wht, grn, ylo
    # 10: wht, grn, red, blu, red, wht, red, grn, red, blu, ylo, wht, pnk, cyn, wht, cyn
    # 11: grn, ylo, wht, grn, wht, pnk, blu, wht, ylo, blk, grn, red, blu, wht, red, ylo
    # 12: ylo, blk, pnk, grn, red, wht, cyn, grn, pnk, red, wht, grn, cyn, pnk, blk, grn
    # 13: wht, grn, blu, pnk, wht, grn, pnk, blk, wht, red, cyn, wht, blu, wht, cyn, wht
    # 14: red, pnk, wht, red, blu, blu, wht, grn, pnk, cyn, blu, wht, ylo, blk, red, blu
    # 15: grn, blu, pnk, grn, red, blk, cyn, red, wht, ylo, ylo, blu, cyn, red, blu, red

    def setUp(self):
        self.cur_dir_path = os.path.dirname(os.path.realpath(__file__))
        self.resource_dir = os.path.join(self.cur_dir_path, 'resources')
        self.image_to_use = os.path.join(self.resource_dir, 'colorful16x16.png')

    def test_a(self):
        # Ultimately what we want from this test is to "drop" the robot on a specific location, and move it a certain
        # amount, and have the code be able to identify where the robot is (or most likely is), and which direction it
        # is facing.
        # We will use the colorful16x16 image, scaled up to 32cm x 32cm
        # The robot will have a distance between the left/right color sensors of 6cm
        # Don't tell the library code, but ssh: The robot will be moving from left to right, with the right sensor
        # in the middle of row 10, column 2 -- at this location, the robot will be seeing left=grn and right=red
        # The robot will then walk forward 4 cm -- at this location, the robot will be seeing left=cyn and right=red
        m = MapFromPicture(path_to_image=self.image_to_use, actual_map_width=0.32, actual_map_height=0.32)
        locator = LocatorA(world_map=m, color_sensor_separation=0.06)
        locator.get_location_and_angle(
            left_color_1=color_rgb_from_name['grn'], right_color_1=color_rgb_from_name['red'],
            left_color_2=color_rgb_from_name['cyn'], right_color_2=color_rgb_from_name['red'],
            distance_moved=0.04
        )
        # let's try to find all the possible vectors from yellow to white.  With this spacing there should be at least
        # one, from (0, 0), straight down to (0, 3)
        pairs = locator.get_possible_position_vectors(
            left_color=color_rgb_from_name['ylo'], right_color=color_rgb_from_name['wht']
        )
        # let's try to track down the ones from 0, 0 to 0, 3, there could be several but should be at least one
        pairs_starting_in_row_0_column_0 = [
            pair for pair in pairs if 0 < pair[0][0] < 0.02 and 0 < pair[0][1] < 0.02
        ]
        pairs_also_ending_in_row_3_column_0 = [
            pair for pair in pairs_starting_in_row_0_column_0 if 0 < pair[1][0] < 0.02 and 0.06 < pair[1][1] < 0.08
        ]
        # black_spots = locator.get_possible_locations((0, 0, 0))
        self.assertGreaterEqual(len(pairs_also_ending_in_row_3_column_0), 1)
