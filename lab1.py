"""
Orienteering path-solving program
CS 331 Lab 1
Author: Kilian Jakstis
"""

import argparse
import file_util
import search_util
import image_util

"""
Parse commandline args, read in the necessary files, compute ideal path and distance, draw and save modified map
"""
if __name__ == '__main__':
    # commandline args
    parser = argparse.ArgumentParser()
    parser.add_argument('terrain_image')
    parser.add_argument('elevation_file')
    parser.add_argument('path_file')
    parser.add_argument('output_image_filename')
    args = parser.parse_args()
    # read in the image, elevation, and path files
    poi_path = file_util.get_poi_path(args.path_file)
    elevations = file_util.get_elevations(args.elevation_file)
    map_array = image_util.read_image(args.terrain_image)
    if poi_path is not None and elevations is not None and map_array is not None:
        # compute the path and print distance
        route = search_util.get_route(map_array, elevations, poi_path)
        # draw the path on the image and save it to output file
        if route is not None:
            image_util.save_image(map_array, route, args.output_image_filename)
