"""
Orienteering routing and A* visualization program
Author: Kilian Jakstis
"""

import argparse
import os
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
    animation_dir = get_download_directory()
    user_input = input("Hit 'q' at any time during the animation to quit and hit 'p' to pause. \n"
                       "Enter anything to begin the animation: ")
    if user_input.strip() == "q":
        return
    return image_util.init_window(x, y, animation_dir)

def get_download_directory():
    home_directory = os.path.expanduser("~")    # the user's home directory
    download_directory = os.path.join(home_directory, "Downloads")     # see if the Downloads directory exists
    if os.path.exists(download_directory) and os.path.isdir(download_directory):
        print("animation will save to downloads folder")
        return download_directory   # if it exists and is a directory
    else:
        print("animation will save to current directory")
        return os.getcwd()

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
        animation_out = begin_animation(max_x, max_y)
        # compute the path and print distance
        # route = search_util.get_route(map_array, elevations, poi_path, max_x, max_y, animation_out)
        search_util.get_route(map_array, elevations, poi_path, max_x, max_y, animation_out)
        animation_out.release()
        image_util.clean_windows()
    else:
        print("Error with algorithm arguments.")

if __name__ == '__main__':
    main()
