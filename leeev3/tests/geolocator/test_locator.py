import os
import unittest

# from leeev3.geolocator.locator import LocatorA
from leeev3.geolocator.mapping import MapFromPicture


color_names_from_rgb = {
    '(0, 0, 0)': 'blk',
    '(255, 0, 0)': 'red',
    '(0, 255, 0)': 'grn',
    '(0, 0, 255)': 'blu',
    '(0, 255, 255)': 'cyn',
    '(255, 0, 255)': 'pnk',
    '(255, 255, 0)': 'ylo',
    '(255, 255, 255)': 'wht',
}


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
        m = MapFromPicture(self.image_to_use, 16, 16)
        pixel_string = ''
        for y in range(16):
            for x in range(16):
                # pixel_string += str(m.get_color_at_pixel_position(x, y)) + ', '
                pixel_string += color_names_from_rgb[str(m.get_color_at_pixel_position(x, y))] + ', '
            pixel_string += '\n'
        print(pixel_string)
        # locator = LocatorA(m, 0.05)
