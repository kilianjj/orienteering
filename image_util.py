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
    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
    # scale_factor_x = 800 / x
    # scale_factor_y = 800 / y
    # alter fps with example rn
    fps = 10
    # cv2.resizeWindow(WINDOW_NAME, int(x * scale_factor_x) if x * scale_factor_x < MAX_WINDOW_X else MAX_WINDOW_X,
    #                  int(y * scale_factor_y) if y * scale_factor_y < MAX_WINDOW_Y else MAX_WINDOW_Y)
    cv2.resizeWindow(WINDOW_NAME, x if x < MAX_WINDOW_X else MAX_WINDOW_X,
                     y if y < MAX_WINDOW_Y else MAX_WINDOW_Y)
    return cv2.VideoWriter(f"{directory}/animation.avi", cv2.VideoWriter_fourcc(*'MJPG'), int(fps * (1 / x * y)), (x, y))

def clean_windows():
    time.sleep(5)
    cv2.destroyAllWindows()

def format_color(display_type):
    return np.array([ANIMATION_COLORS[display_type][0],
              ANIMATION_COLORS[display_type][1],
              ANIMATION_COLORS[display_type][2],
              255], dtype=np.uint8)

def update_image(image, out):
    bgr_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    x = len(bgr_image[0])
    y = len(bgr_image)
    # scale_factor_x = 800 / x
    # scale_factor_y = 600 / y
    # resized = cv2.resize(bgr_image, (int(x * scale_factor_x), int(y * scale_factor_y)), interpolation=cv2.INTER_LINEAR)
    cv2.imshow(WINDOW_NAME, bgr_image)
    # bgr_image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    # image_np = cv2.UMat.get(bgr_image)
    # x = len(bgr_image[0])
    # y = len(bgr_image)
    # scale_factor = 500000 / (len(bgr_image[0]) * len(bgr_image))
    # resized = cv2.resize(image_np, (int(x * scale_factor), int(y * scale_factor)))
    # cv2.imshow(WINDOW_NAME, bgr_image)
    out.write(bgr_image)
    key = cv2.waitKey(30)
    if key == ord('q'):  # 'q' key to quit
        exit(1)  # just exit program
    elif key == ord('p'):  # 'p' key to pause
        cv2.waitKey(-1)

def update_image_path(original_image, route, start, end, out):
    image = copy.deepcopy(original_image)
    # change path segment colors
    path_values = format_color("path")
    for point in route:
        image[point[1]][point[0]] = path_values
    # change start point color
    start_values = format_color("start")
    image[start[1]][start[0]] = start_values
    # change target color
    image[end[1]][end[0]] = start_values
    update_image(image, out)

def update_search(original_image, frontier, visited, route, start, end, out):
    # update_image_path(original_image, route, poi_list)
    image = copy.deepcopy(original_image)
    # change points that were visited
    visited_values = format_color("visited")
    for point in visited:
        image[point[1]][point[0]] = visited_values
    # change points in frontier
    frontier_values = format_color("frontier")
    for point in frontier:
        image[point[1]][point[0]] = frontier_values
    update_image_path(image, route, start, end, out)

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
