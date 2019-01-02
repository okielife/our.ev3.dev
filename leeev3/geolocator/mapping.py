from PIL import Image


class Map(object):
    """
    Base class of a rectangular world map for the robot
    """

    def get_color_at_pixel_position(self, x: int, y: int):
        raise NotImplementedError('Must override get_color_at_pixel_position in derived classes')

    def get_color_at_physical_position(self, x: float, y: float):
        raise NotImplementedError('Must override get_color_at_physical_position in derived classes')


class MapFromPicture(Map):
    """
    This would be a way to input the map from a picture.
    It would be *really* great to know if this is good enough.
    I think we need to find something that we have both in a printed state and also in a digital state and try it out
    """

    def __init__(self, path_to_image: str, actual_width: float, actual_height: float):
        """
        
        :param path_to_image: File path to image
        :param actual_width: Physical width of playing map in real life, in meters
        :param actual_height: Physical height of playing map in real life, in meters
        """
        self.image_path = path_to_image
        self.image = Image.open(path_to_image)
        self.width_pixels = self.image.size[0]
        self.height_pixels = self.image.size[1]
        self.pixels = self.image.load()
        self.x_scale = self.width_pixels / actual_width
        self.y_scale = self.height_pixels / actual_height

    def get_color_at_pixel_position(self, x: int, y: int):
        return self.pixels[x, y]

    def get_color_at_physical_position(self, x: float, y: float):
        x_to_use = min(int(x * self.x_scale), self.width_pixels-1)
        y_to_use = min(int(y * self.y_scale), self.height_pixels-1)
        return self.pixels[x_to_use, y_to_use]


class MapFromSensors(Map):
    """
    This would be a way to input the map manually from sensed color data.
    I imagine it would be like this:
    - This class is essentially a wrapper around a JSON file containing the data
    - To generated the data, this class would be a static method with a parameter for the grid spacing to be used
    - The function would then go into a manual input mode and you would start the robot at the "bottom left" origin,
      and press space bar, which would read the sensed data and store that.  Then move the robot the spacing amount, and
      press space bar again, continuing until you hit the end of the world.  Then press enter maybe, signaling you are
      done with that line.  Then move up a spacing amount, go back to the left, and press space bar again to get the
      first reading on that line.  And continue.

    Note: We would need to figure out how to offset for the robot size itself, plus the fact that we can't reach the
          edges of the table, etc.  Maybe have to just scan using the color sensor first without the robot so we can
          get the entirety of the table.
    """

    def get_color_at_physical_position(self, x, y):
        pass

    def get_color_at_pixel_position(self, x, y):
        pass
