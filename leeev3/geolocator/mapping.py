from PIL import Image
from typing import List

from leeev3.geolocator.tolerances import Tolerances


class Map(object):
    """
    Base class of a rectangular world map for the robot
    """

    def get_color_at_pixel_position(self, x: int, y: int):
        raise NotImplementedError('Must override get_color_at_pixel_position in derived classes')

    def get_color_at_physical_position(self, x: float, y: float):
        raise NotImplementedError('Must override get_color_at_physical_position in derived classes')

    @staticmethod
    def sample_physical_positions(physical_x: float, physical_y: float, max_physical_x: float, max_physical_y: float):
        if physical_x < 0 or physical_x > max_physical_x or physical_y < 0 or physical_y > max_physical_y:
            raise Exception(
                'Mapping issue, attempted to sample map positions at out of range point: (%s, %s)' % (
                    physical_x, physical_y
                )
            )
        x_spots_to_check = []
        y_spots_to_check = []
        if physical_x >= Tolerances.SamplingEpsilon:
            x_spots_to_check.append(physical_x - Tolerances.SamplingEpsilon)
        else:
            x_spots_to_check.append(0.0)
        if physical_x <= max_physical_x - Tolerances.SamplingEpsilon:
            x_spots_to_check.append(physical_x + Tolerances.SamplingEpsilon)
        else:
            x_spots_to_check.append(max_physical_x)
        if physical_y >= Tolerances.SamplingEpsilon:
            y_spots_to_check.append(physical_y - Tolerances.SamplingEpsilon)
        else:
            y_spots_to_check.append(0.0)
        if physical_y <= max_physical_y - Tolerances.SamplingEpsilon:
            y_spots_to_check.append(physical_y + Tolerances.SamplingEpsilon)
        else:
            y_spots_to_check.append(max_physical_y)
        final_coordinate_set = []
        for x in x_spots_to_check:
            for y in y_spots_to_check:
                final_coordinate_set.append((x, y))
        return final_coordinate_set


class MapFromPicture(Map):
    """
    This would be a way to input the map from a picture.
    It would be *really* great to know if this is good enough.
    I think we need to find something that we have both in a printed state and also in a digital state and try it out
    """

    def __init__(self, path_to_image: str, actual_map_width: float, actual_map_height: float):
        """

        :param path_to_image: File path to image
        :param actual_map_width: Physical width of playing map in real life, in meters
        :param actual_map_height: Physical height of playing map in real life, in meters
        """
        self.image_path = path_to_image
        self.image = Image.open(path_to_image)
        self.width_pixels = self.image.size[0]
        self.height_pixels = self.image.size[1]
        self.pixels = self.image.load()
        self.actual_map_width = actual_map_width
        self.actual_map_height = actual_map_height
        self.x_scale = self.width_pixels / self.actual_map_width
        self.y_scale = self.height_pixels / self.actual_map_height

    def get_color_at_pixel_position(self, x: int, y: int):
        return self.pixels[x, y]

    def get_color_at_physical_position(self, x: float, y: float):
        points_to_check = Map.sample_physical_positions(x, y, self.actual_map_width, self.actual_map_height)
        totals = [0, 0, 0]
        for point in points_to_check:
            x_to_use = min(int(point[0] * self.x_scale), self.width_pixels-1)
            y_to_use = min(int(point[1] * self.y_scale), self.height_pixels-1)
            this_pixel = self.pixels[x_to_use, y_to_use]
            totals[0] += this_pixel[0]
            totals[1] += this_pixel[1]
            totals[2] += this_pixel[2]
        totals[0] /= len(points_to_check)
        totals[1] /= len(points_to_check)
        totals[2] /= len(points_to_check)
        return tuple(totals)


# class MapFromSensors(Map):
#     """
#     This would be a way to input the map manually from sensed color data.
#     I imagine it would be like this:
#     - This class is essentially a wrapper around a JSON file containing the data
#     - To generate the data, this class would have a static method with a parameter for the grid spacing to be used
#     - The function would then go into a manual input mode and you would start the robot at the "bottom left" origin,
#       and press space bar, which would read the sensed data and store that.  Then move the robot the spacing amount, &
#       press space bar again, continuing until you hit the end of the world.  Then press enter maybe, signaling you are
#       done with that line.  Then move up a spacing amount, go back to the left, and press space bar again to get the
#       first reading on that line.  And continue.
#
#     Note: We would need to figure out how to offset for the robot size itself, plus the fact that we can't reach the
#           edges of the table, etc.  Maybe have to just scan using the color sensor first without the robot so we can
#           get the entirety of the table.
#     """
#
#     def get_color_at_physical_position(self, x: int, y: int):
#         pass
#
#     def get_color_at_pixel_position(self, x: float, y: float):
#         pass


class MapFromData(Map):
    """
    This would be a way to input the map from "pixel" data.
    Basically, give a list of lists of color data and a couple parameters about pixel size and create a map from it
    """

    def __init__(self, map_data: List, actual_map_width: float, actual_map_height: float):
        if not isinstance(map_data, list):
            raise Exception('Bad type for map_data, must be a list of rows, which are lists of columns of RGB data')
        pixels_wide = None
        for row_num, row in enumerate(map_data):
            if not isinstance(row, list):
                raise Exception('Bad type for map_data row %s, should be a list of columns of RGB data' % row_num)
            if row_num == 0:
                pixels_wide = len(row)
            else:
                if pixels_wide != len(row):
                    raise Exception('Bad row length for map_data row %s, all rows must be same length' % row_num)
            for col_num, col_value in enumerate(row):
                if not isinstance(col_value, tuple):
                    raise Exception(
                        'Bad datum in map_data, items must be tuples of (R, G, B), at row,column=%s,%s' % (
                            row_num, col_num
                        )
                    )
        pixels_tall = len(map_data)
        self.pixels = map_data
        self.width_pixels = pixels_wide
        self.height_pixels = pixels_tall
        self.x_scale = self.width_pixels / actual_map_width
        self.y_scale = self.height_pixels / actual_map_height

    def get_color_at_pixel_position(self, x: int, y: int):
        return self.pixels[y][x]

    def get_color_at_physical_position(self, x: float, y: float):
        x_to_use = min(int(x * self.x_scale), self.width_pixels - 1)
        y_to_use = min(int(y * self.y_scale), self.height_pixels - 1)
        return self.pixels[y_to_use][x_to_use]
