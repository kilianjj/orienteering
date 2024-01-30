"""
Searching logic and related functions
Author: Kilian Jakstis
*** elevations and terrain image indexed by y then x
"""

import heapq

# max coordinate values
MAX_X = 395
MAX_Y = 500
# grid sizes
GRID_WIDTH = 10.29
GRID_HEIGHT = 7.55
# RGB values for the various terrain types and the associated heuristic cost value
terrain_types = {
    (248, 148, 18): 10,     # OPEN_LAND
    (255, 192, 0): 1,     # ROUGH_MEADOW
    (255, 255, 255): 10,    # EASY_FOREST
    (2, 208, 60): 5,       # SLOW_FOREST
    (2, 136, 40): 2,       # WALK_FOREST
    (71, 51, 3): 10,        # PAVED_ROAD
    (0, 0, 0): 10,          # FOOTPATH
    (205, 0, 101): None,   # OUT_OF_BOUNDS
    (5, 73, 24): None,     # IMPASSIBLE_VEGETATION
    (0, 0, 255): None      # WATER
}

def get_route(terrain, elevations, poi_path):
    """
    Get the full route by constructing smaller routes between pairs of points in the specified order
    :param terrain: RGB array of terrain image
    :param elevations: elevation array
    :param poi_path: list of POIs in the order they must be visited
    :return: full route (as a list of coordinate tuples) in order of those visited
    """
    if len(poi_path) < 2:
        print("POI path not long enough")
        return
    total_distance = 0
    route = []
    for i in range(len(poi_path) - 1):
        between_points, between_distance = search(poi_path[i], poi_path[i+1], terrain, elevations)
        # print(between_points)
        if between_points is None:
            print("Path not found for this section")
            continue
        route.extend(between_points)
        total_distance += between_distance
    print(f"Total Distance: {total_distance}m")
    return route

def distance(coordinate, target, elevations, heuristic_bool):
    """
    Calculates the distance between 2 points
    :param coordinate: current coordinate
    :param target: target coordinate
    :param elevations: elevation values
    :param heuristic_bool: true if this is being used to calculate heuristic (heuristic is unit-less, cost is in meters)
    :return: float distance between the two points
    """
    x = (coordinate[0] - target[0]) ** 2
    y = (coordinate[1] - target[1]) ** 2
    z = (elevations[coordinate[1]][coordinate[0]] - elevations[target[1]][target[0]]) ** 2      # indexing y then x
    d = (x + y + z) ** (1/3)
    if heuristic_bool:
        return d
    if x == 0:
        return GRID_HEIGHT * d
    elif y == 0:
        return GRID_WIDTH * d
    else:
        return (((GRID_HEIGHT ** 2) + (GRID_WIDTH ** 2)) ** (1/2)) * d

def heuristic(coordinate, target, elevations, terrain_time):
    """
    Heuristic function for guiding A* search
    :param coordinate: current point
    :param target: goal point
    :param elevations: elevation values
    :param terrain_time: terrain time estimate
    :return: estimated cost to target by using 3d Euclidean distance
    """
    return distance(coordinate, target, elevations, True) / terrain_time

def get_neighbors(coordinate):
    """
    Get neighbor coordinates from current
    :param coordinate: current point
    :return: list of neighbor coordinate tuples
    """
    neighbors = []
    rows, cols = MAX_Y, MAX_X
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y, x in directions:
        new_row, new_col = coordinate[1] + x, coordinate[0] + y
        if 0 <= new_row < rows and 0 <= new_col < cols and new_row < MAX_X and new_col < MAX_Y:
            neighbors.append((new_col, new_row))
    return neighbors

def construct_path(visited_nodes, start, end):
    """
    Reconstruct path by backtracking after running A*
    :param visited_nodes: dictionary of visited points and their parents
    :param start: start point
    :param end: end point
    :return: list of coordinate tuples in order of when they were visited
    """
    path = []
    head = end
    while head is not start:
        path.append(head)
        head = visited_nodes.get(head)
    path.append(start)
    return path[::-1]

def search(start, end, terrain, elevations):
    """
    A* search algorithm
    :param start: start point
    :param end: end point
    :param terrain: array of terrain image RGB values
    :param elevations: elevation data
    :return: quickest path from start to end accounting for terrain
    """
    # todo: check that backtrack, heuristic is working correctly
    visited = set()     # set to keep track of visited nodes
    to_visit = []       # priority queue for new nodes to visit
    g_scores = {start: 0}   # dictionary for keeping track of cost associated with points
    f_scores = {start: 0}   # dictionary for keeping track of heuristic values of points
    parents = {}        # dictionary for storing points and their parents (used for backtracking to get path)
    heapq.heappush(to_visit, (0, start))
    while to_visit:
        current = heapq.heappop(to_visit)[1]
        if current == end:
            return construct_path(parents, start, end), g_scores.get(end)
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue
            terrain_type = (terrain[neighbor[1]][neighbor[0]][0],
                            terrain[neighbor[1]][neighbor[0]][1],
                            terrain[neighbor[1]][neighbor[0]][2])
            if terrain_type in terrain_types:
                time_factor = terrain_types.get(terrain_type)
            else:
                time_factor = 1
            if time_factor is None:
                continue
            g_score = distance(current, neighbor, elevations, False) + g_scores.get(current)
            if neighbor not in g_scores or g_score < g_scores[neighbor]:
                g_scores[neighbor] = g_score
                f_scores[neighbor] = g_score + heuristic(neighbor, end, elevations, time_factor)
                parents[neighbor] = current
                heapq.heappush(to_visit, (f_scores[neighbor], neighbor))
    return None, 0
