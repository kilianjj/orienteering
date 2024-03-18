"""
Image functionalities
Author: Kilian Jakstis
"""

from PIL import Image
import numpy as np
import os
import global_values as values

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

# def save_image(im, route, output_path):
#     """
#     Draw the ideal path on the terrain map and save in the desired location
#     :param im: numpy array of the terrain map
#     :param route: the ideal path
#     :param output_path: path at which to save output image
#     """
#     try:
#         image = Image.fromarray(im)
#         image = image.convert('RGB')
#         pixels = image.load()
#         for pixel in route:
#             pixels[pixel[0], pixel[1]] = PATH_COLOR
#         image.save(output_path)
#     except Exception as e:
#         print(f"Error writing output image: {e}")

# for testing - just opens the image
def save_image(im, route, output_path):
    """
    Draw the ideal path on the terrain map and show image
    :param im: numpy array of the terrain map
    :param route: the ideal path (currently in tuples of coordinates***)
    :param output_path: path at which to save output image
    """
    try:
        image = Image.fromarray(im)
        image = image.convert('RGB')
        pixels = image.load()
        for pixel in route:
            pixels[pixel[0], pixel[1]] = values.PATH_COLOR
        image.show()
    except Exception as e:
        print(f"Error writing output image: {e}")

def get_download_directory():
    home_directory = os.path.expanduser("~")    # the user's home directory
    download_directory = os.path.join(home_directory, "Downloads")     # see if the Downloads directory exists
    if os.path.exists(download_directory) and os.path.isdir(download_directory):
        return download_directory   # if it exists and is a directory
    else:
        return None
