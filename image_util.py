"""
Image functionalities
Author: Kilian Jakstis
"""

from PIL import Image
import numpy as np

# RGB values for the various terrain types
OPEN_LAND = (248, 148, 18)
ROUGH_MEADOW = (255, 192, 0)
EASY_FOREST = (255, 255, 255)
SLOW_FOREST = (2, 208, 60)
WALK_FOREST = (2, 136, 40)
IMPASSIBLE_VEGETATION = (5, 73, 24)
WATER = (0, 0, 255)
PAVED_ROAD = (71, 51, 3)
FOOTPATH = (0, 0, 0)
OUT_OF_BOUNDS = (205, 0, 101)
PATH = (200, 100, 230)

def read_image(path):
    """
    Read in terrain image file
    :param path: path to the image
    :return: numpy array of the image
    """
    try:
        with Image.open(path) as im:
            return np.array(im)
    except Exception as e:
        print(f"Error reading in terrain file: {e}")
        return None

# do not delete: this is the one that saves image, using show for debugging rn
# def save_image(im, route, output_path):
#     """
#     Draw the ideal path on the terrain map and save in the desired location
#     :param im: numpy array of the terrain map
#     :param route: the ideal path (currently in tuples of coordinates***)
#     :param output_path: path at which to save output image
#     """
#     try:
#         image = Image.fromarray(im)
#         pixels = image.load()
#         for pixel in route:
#             pixels[pixel[0], pixel[1]] = PATH
#         image.save(output_path)
#     except Exception as e:
#         print(f"Error writing output image: {e}")

# delete this one after testing
def save_image(im, route, output_path):
    """
    Draw the ideal path on the terrain map and save in the desired location
    :param im: numpy array of the terrain map
    :param route: the ideal path (currently in tuples of coordinates***)
    :param output_path: path at which to save output image
    """
    try:
        image = Image.fromarray(im)
        pixels = image.load()
        for pixel in route:
            pixels[pixel[0], pixel[1]] = PATH
        image.show()
    except Exception as e:
        print(f"Error writing output image: {e}")

