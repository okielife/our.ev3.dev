class Map(object):
    """
    Base class of a rectangular world map for the robot
    """
    def get_color_at_position(self):
        pass

    @staticmethod
    def dummy_function():
        from PIL import Image
        im = Image.open('/tmp/small88.png')  # Can be many different formats.
        pix = im.load()
        x = 2
        y = 3
        print(im.size)  # Get the width and hight of the image for iterating over
        print(pix[x, y])  # Get the RGBA Value of the a pixel of an image


class MapFromPicture(Map):
    """
    This would be a way to input the map from a picture.
    It would be *really* great to know if this is good enough.
    I think we need to find something that we have both in a printed state and also in a digital state and try it out
    """
    pass


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
    pass
