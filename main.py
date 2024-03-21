"""
Orienteering routing and A* visualization program
Author: Kilian Jakstis
"""

import argparse
import os
import time
import file_util
import search_util
import image_util

def handle_cmdline_args():
    parser = argparse.ArgumentParser(description="A* visualization program")
    parser.add_argument('terrain_image', help="terrain map image file")  # terrain map
    parser.add_argument('path_file', help="file with poi coordinates to visit")  # points to visit
    parser.add_argument('elevation_file', help="terrain elevations file")  # elevation values - defaults to 0s if "none"
    return parser.parse_args()

def begin_animation(x, y):
    # see if user ready for animation
    user_input = input("Hit 'q' at any time during the animation to quit and hit 'p' to pause. \n"
                       "Enter anything to begin the animation: ")
    if user_input.strip() == "q":
        return
    image_util.init_window(x, y)

def after_alg(t_map, route):
    user_input = input("Enter 'y' to save output path image or anything else to terminate: ")
    if user_input.strip() == "y":
        download_dir = image_util.get_download_directory()
        if download_dir:
            if image_util.save_image(t_map, route, download_dir):
                print("Route image saved to user downloads: ", download_dir)
        else:
            if image_util.save_image(t_map, route, os.getcwd()):
                print("Route image saved to this directory: ", download_dir)

# Process the necessary files, compute ideal path and distance, draw and save modified map
def main():
    # commandline args
    args = handle_cmdline_args()
    # read in the image, elevations, and poi list
    map_array = image_util.read_image(args.terrain_image)
    elevations = file_util.get_elevations(args.elevation_file, map_array.shape)
    poi_path = file_util.get_poi_path(args.path_file)
    max_x = map_array.shape[1]
    max_y = map_array.shape[0]
    if poi_path is not None and elevations is not None and map_array is not None:
        begin_animation(max_x, max_y)
        # compute the path and print distance
        route = search_util.get_route(map_array, elevations, poi_path, max_x, max_y)
        image_util.clean_windows()
        if route:
            after_alg(map_array, route)
        else:
            print("No path found.")
    else:
        print("Error with algorithm arguments.")

if __name__ == '__main__':
    main()
