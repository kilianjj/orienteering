"""
Orienteering routing and A* visualization program
Author: Kilian Jakstis
"""

import argparse
import os
import file_util
import search_util
import image_util

# Process the necessary files, compute ideal path and distance, draw and save modified map
def main():
    # commandline args
    parser = argparse.ArgumentParser(description="A* visualization program")
    parser.add_argument('terrain_image', help="terrain map image file")  # terrain map
    parser.add_argument('path_file', help="file with poi coordinates to visit")  # points to visit
    parser.add_argument('elevation_file', help="terrain elevations file")  # elevation values - defaults to 0s if "none"
    args = parser.parse_args()
    # read in the image, elevations, and poi list
    poi_path = file_util.get_poi_path(args.path_file)
    elevations = file_util.get_elevations(args.elevation_file)
    map_array = image_util.read_image(args.terrain_image)
    if poi_path is not None and elevations is not None and map_array is not None:
        # see if user ready for animation
        user_input = input("Enter anything to begin animation, or 'q' to quit: ")
        if user_input.strip() == "q":
            return
        # todo: animation
        # compute the path and print distance
        route = search_util.get_route(map_array, elevations, poi_path)
        if route is not None:
            # get path to save image
            download_dir = image_util.get_download_directory()
            if download_dir:
                image_util.save_image(map_array, route, download_dir)
                print("Output path saved to downloads: ", download_dir)
            else:
                image_util.save_image(map_array, route, os.getcwd())
                print("Output path saved to this directory: ", download_dir)
    else:
        print("Error with algorithm arguments.")

if __name__ == '__main__':
    main()
