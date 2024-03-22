"""
Image functionalities
Author: Kilian Jakstis
"""

from PIL import Image
import numpy as np
import cv2
import copy
import time

# window constants
WINDOW_NAME = 'A* Visualization'
MAX_WINDOW_X = 1200
MAX_WINDOW_Y = 1000

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
    (248, 148, 18): 2,     # OPEN_LAND
    (255, 192, 0): 200,     # ROUGH_MEADOW
    (255, 255, 255): 3,    # EASY_FOREST
    (2, 208, 60): 50,       # SLOW_FOREST
    (2, 136, 40): 100,      # WALK_FOREST
    (71, 51, 3): 1,        # PAVED_ROAD
    (0, 0, 0): 2,          # FOOTPATH
    (205, 0, 101): None,   # OUT_OF_BOUNDS
    (5, 73, 24): None,     # IMPASSIBLE_VEGETATION
    (0, 0, 255): 1000      # WATER
}

def init_window(x, y, directory):
    """
    Initialize the OpenCV display window
    :param x: x dimension of image
    :param y: y dimension of image
    :param directory: directory in which to save animation file
    :return: video writer object
    """
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    # alter fps with example length
    fps = 10
    cv2.resizeWindow(WINDOW_NAME, x if x < MAX_WINDOW_X else MAX_WINDOW_X,
                     y if y < MAX_WINDOW_Y else MAX_WINDOW_Y)
    return cv2.VideoWriter(f"{directory}/animation.avi", cv2.VideoWriter_fourcc(*'MJPG'),
                           int(fps * (1 / x * y)), (x, y))

def clean_windows():
    """
    Wait after visualization ends and then destroy window
    """
    time.sleep(5)
    cv2.destroyAllWindows()

def format_color(display_type):
    """
    Format colors as np array
    :param display_type: type of pixel to represent
    :return: np array with same info
    """
    return np.array([ANIMATION_COLORS[display_type][0],
              ANIMATION_COLORS[display_type][1],
              ANIMATION_COLORS[display_type][2],
              255], dtype=np.uint8)

def update_image(image, out):
    """
    Update the display and write changes to animation file
    :param image: image to update to
    :param out: video file writer
    """
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)     # convert to right form
    cv2.imshow(WINDOW_NAME, bgr_image)      # update window
    out.write(bgr_image)        # write to video file
    key = cv2.waitKey(30)
    if key == ord('q'):  # 'q' key to quit
        exit(1)  # just exit program
    elif key == ord('p'):  # 'p' key to pause
        cv2.waitKey(-1)

def update_image_path(original_image, route, start, end, out):
    """
    Update when new start/target points identified
    :param original_image: original map
    :param route: current solution path
    :param start: start pint of new section
    :param end: end point of new section
    :param out: video file writer
    """
    image = copy.deepcopy(original_image)           # for pass by value
    path_values = format_color("path")              # change path segment colors
    for point in route:
        image[point[1]][point[0]] = path_values     # change path point color
    start_values = format_color("start")            # change start point color
    image[start[1]][start[0]] = start_values
    image[end[1]][end[0]] = start_values            # change target color
    update_image(image, out)                        # update display to reflect changes

def update_search(original_image, frontier, visited, route, start, end, out):
    """
    Update display to reflect algorithm progress - to_visit queue and visited locations
    :param original_image: original map
    :param frontier: to visit node list
    :param visited: visited node list
    :param route: current solution route
    :param start: start coord
    :param end: end coord
    :param out: video file writer
    """
    image = copy.deepcopy(original_image)
    visited_values = format_color("visited")
    for point in visited:
        image[point[1]][point[0]] = visited_values      # change points that were visited
    frontier_values = format_color("frontier")
    for point in frontier:
        image[point[1]][point[0]] = frontier_values     # change points in frontier
    update_image_path(image, route, start, end, out)    # update display

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
