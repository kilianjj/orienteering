"""
Functions for file processing
Author: Kilian Jakstis
"""

def get_poi_path(path_file):
    """
    Read the POI points that must be visited in the event in from relevant file
    :param path_file: path to POI point coordinate file
    :return: list of POI point coordinates if file read is successful - otherwise None
    """
    path = []
    try:
        with open(path_file) as file:
            for line in file:
                coordinates = line.split()
                path.append((int(coordinates[0]), int(coordinates[1])))
        return path
    except Exception as e:
        print(f"Error reading path file: {e}")
        return None

def zero_elevations(y, x):
    """
    :return: 0 array for uniform elevations
    """
    elevations = [[0 for _ in range(x)] for __ in range(y)]
    return elevations

def get_elevations(elevation_file, shape):
    """
    Read the elevations in from relevant file
    :param elevation_file: path to elevation file - if None population with all 0s
    :param shape: dimensions of image array - used to generate elevation array if no file is provided
    :return: list of elevations if file read is successful - otherwise None
    """
    if elevation_file == "none":
        return zero_elevations(shape[0], shape[1])
    elevations = []
    try:
        with open(elevation_file) as file:
            for line in file:
                values = line.split()
                elevations.append([float(value) for value in values][:-5])
        print(elevations[0], len(elevations))
        if len(elevations) == shape[0] and len(elevations[0]) == shape[1]:
            return elevations
    except Exception as e:
        print(f"Error reading elevation file: {e}. Proceeding with uniform elevations.")
        return zero_elevations(shape[0], shape[1])
