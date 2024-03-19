"""
Image functionalities
Author: Kilian Jakstis
"""

from PIL import Image
import numpy as np
import os
import cv2
import copy

# map pixel width and height
MAX_X = 395
MAX_Y = 500

# grid sizes
GRID_WIDTH = 10.29
GRID_HEIGHT = 7.55

# window constants
WINDOW_NAME = 'A* Visualization'
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
SQUARE_SIZE = 50

# colors for animation
ANIMATION_COLORS = {
    "visited": (192, 255, 0),
    "frontier": (0, 255, 227),
    "path": (118, 63, 231),
    "poi": (255, 66, 232),
    "start": (255, 46, 46)
}

# RGB values for the various terrain types and the associated time cost scalar
TERRAIN_TYPES = {
    (248, 148, 18): 1,     # OPEN_LAND
    (255, 192, 0): 50,     # ROUGH_MEADOW
    (255, 255, 255): 3,    # EASY_FOREST
    (2, 208, 60): 5,       # SLOW_FOREST
    (2, 136, 40): 25,      # WALK_FOREST
    (71, 51, 3): 1,        # PAVED_ROAD
    (0, 0, 0): 3,          # FOOTPATH
    (205, 0, 101): None,   # OUT_OF_BOUNDS
    (5, 73, 24): None,     # IMPASSIBLE_VEGETATION
    (0, 0, 255): 1000      # WATER
}

def init_window():
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    # cv2.resizeWindow(WINDOW_NAME, WINDOW_WIDTH, WINDOW_HEIGHT)

def clean_windows():
    cv2.destroyAllWindows()

def update_image(image):
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    cv2.imshow(WINDOW_NAME, bgr_image)
    key = cv2.waitKey(30)
    if key == ord('q'):  # 'q' key to quit
        exit(1)  # just exit program
    elif key == ord('p'):  # 'p' key to pause
        cv2.waitKey(-1)

def update_image_path(original_image, route, start, end):
    image = copy.deepcopy(original_image)
    # change path segment colors
    path_values = np.array([ANIMATION_COLORS["path"][0],
                            ANIMATION_COLORS["path"][1],
                            ANIMATION_COLORS["path"][2],
                            255], dtype=np.uint8)
    for point in route:
        image[point[1]][point[0]] = path_values
    # change start point color
    start_values = np.array([ANIMATION_COLORS["start"][0],
                             ANIMATION_COLORS["start"][1],
                             ANIMATION_COLORS["start"][2],
                             255], dtype=np.uint8)
    image[start[1]][start[0]] = start_values
    # change target color
    target_values = np.array([ANIMATION_COLORS["poi"][0],
                           ANIMATION_COLORS["poi"][1],
                           ANIMATION_COLORS["poi"][2],
                           255], dtype=np.uint8)
    image[end[1]][end[0]] = target_values
    update_image(image)

def update_search(original_image, frontier, visited, route, start, end):
    # update_image_path(original_image, route, poi_list)
    image = copy.deepcopy(original_image)
    # change points that were visited
    visited_values = np.array([ANIMATION_COLORS["visited"][0],
                            ANIMATION_COLORS["visited"][1],
                            ANIMATION_COLORS["visited"][2],
                            255], dtype=np.uint8)
    for point in visited:
        image[point[1]][point[0]] = visited_values
    # change points in frontier
    frontier_values = np.array([ANIMATION_COLORS["frontier"][0],
                               ANIMATION_COLORS["frontier"][1],
                               ANIMATION_COLORS["frontier"][2],
                               255], dtype=np.uint8)
    for point in frontier:
        image[point[1]][point[0]] = frontier_values
    update_image_path(image, route, start, end)

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

def save_image(im, route, directory_path):
    """
    Draw the ideal path on the terrain map and save in the desired location
    :param im: numpy array of the terrain map
    :param route: the ideal path
    :param directory_path: directory in which to save output image
    """
    try:
        image = Image.fromarray(im)
        image = image.convert('RGB')
        pixels = image.load()
        for pixel in route:
            pixels[pixel[0], pixel[1]] = ANIMATION_COLORS["path"]
        image.save(f"{directory_path}/route.png")
        return True
    except Exception as e:
        print(f"Error writing output image: {e}")
        return False

# for testing - just opens the image
# def save_image(im, route, output_path):
#     """
#     Draw the ideal path on the terrain map and show image
#     :param im: numpy array of the terrain map
#     :param route: the ideal path (currently in tuples of coordinates***)
#     :param output_path: path at which to save output image
#     """
#     try:
#         image = Image.fromarray(im)
#         image = image.convert('RGB')
#         pixels = image.load()
#         for pixel in route:
#             pixels[pixel[0], pixel[1]] = ANIMATION_COLORS["path"]
#         image.show()
#     except Exception as e:
#         print(f"Error writing output image: {e}")

def get_download_directory():
    home_directory = os.path.expanduser("~")    # the user's home directory
    download_directory = os.path.join(home_directory, "Downloads")     # see if the Downloads directory exists
    if os.path.exists(download_directory) and os.path.isdir(download_directory):
        return download_directory   # if it exists and is a directory
    else:
        return None
