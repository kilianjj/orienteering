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

def get_elevations(elevation_file):
    """
    Read the elevations in from relevant file
    :param elevation_file: path to elevation file
    :return: list of elevations if file read is successful - otherwise None
    """
    elevations = []
    try:
        with open(elevation_file) as file:
            for line in file:
                values = line.split()
                elevations.append([float(value) for value in values][:-5])
        return elevations
    except Exception as e:
        print(f"Error reading elevation file: {e}")
        return None
