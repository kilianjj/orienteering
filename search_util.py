"""
Searching logic and related functions
Author: Kilian Jakstis
"""

import heapq
import image_util

def get_route(terrain, elevations, poi_path):
    """
    Get the full route by constructing smaller routes between pairs of points in the specified order
    :param terrain: RGB array of terrain image
    :param elevations: elevation array
    :param poi_path: list of POIs in the order they must be visited
    :return: full route (as a list of coordinate tuples) in order of those visited
    """
    animate_on = True
    if len(poi_path) < 2:
        # only 1 point - no target
        return
    total_distance = 0
    route = []
    for i in range(len(poi_path) - 1):
        between_points, between_distance = search(poi_path[i], poi_path[i+1], terrain, elevations, route, animate_on)
        if between_points is None:
            # path not found
            continue
        route.extend(between_points)
        total_distance += between_distance
        if animate_on:
            animate_on = image_util.update_image_path(terrain, route, poi_path[i], poi_path[i+1])
    if animate_on:
        image_util.update_image_path(terrain, route, poi_path[0], poi_path[-1])
    print(f"Total Distance: {total_distance}m")
    return route

def distance(coordinate, target, elevations):
    """
    Calculate the distance between 2 points
    * indexing done y then x on elevations
    :param coordinate: current coordinate
    :param target: target coordinate
    :param elevations: elevation values
    :return: float distance between the two points
    """
    x = ((coordinate[0] - target[0]) * image_util.GRID_WIDTH) ** 2
    y = ((coordinate[1] - target[1]) * image_util.GRID_HEIGHT) ** 2
    z = (elevations[coordinate[1]][coordinate[0]] - elevations[target[1]][target[0]]) ** 2
    d = (x + y + z) ** (1/2)
    return d

def heuristic(coordinate, target, elevations):
    """
    Heuristic function for guiding A* search
    :param coordinate: current point
    :param target: goal point
    :param elevations: elevation values
    :return: estimated cost to target by using 3d Euclidean distance
    """
    return distance(coordinate, target, elevations)

def get_neighbors(coordinate):
    """
    Get neighbor coordinates from current
    :param coordinate: current point
    :return: list of neighbor coordinate tuples
    """
    neighbors = []
    rows, cols = image_util.MAX_Y, image_util.MAX_X
    directions = [
                  # (-1, -1),
                  (-1, 0),
                  # (-1, 1),
                  (0, -1),
                  (0, 1),
                  # (1, -1),
                  (1, 0),
                  # (1, 1)
                ]
    for y, x in directions:
        new_row, new_col = coordinate[1] + x, coordinate[0] + y
        if 0 <= new_row < rows and 0 <= new_col < cols and new_row < image_util.MAX_Y and new_col < image_util.MAX_X:
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

def search(start, end, terrain, elevations, route, animate):
    """
    A* search algorithm
    :param start: start point
    :param end: end point
    :param terrain: array of terrain image RGB values
    :param elevations: elevation data
    :return: quickest (time) path from start to end accounting for terrain types
    """
    visited = set()             # set to keep track of visited nodes
    to_visit = []               # priority queue for new nodes to visit
    animation_frontier = []     # list of nodes on frontier
    distances = {start: 0}      # dictionary for keeping track of distance associated with points
    times = {start: 0}          # dictionary for keeping track of times associated with visiting points
    f_scores = {start: 0}       # dictionary for keeping track of heuristic values of points
    parents = {}                # dictionary for storing points and their parents (used for backtracking to get path)
    heapq.heappush(to_visit, (0, start))
    while to_visit:
        if animate:
            image_util.update_search(terrain, animation_frontier, visited, route, start, end)
        current = heapq.heappop(to_visit)[1]
        if current in animation_frontier:
            animation_frontier.remove(current)
        if current == end:
            return construct_path(parents, start, end), distances.get(end)
        visited.add(current)
        for neighbor in get_neighbors(current):
            if neighbor in visited:
                continue
            terrain_type = (terrain[neighbor[1]][neighbor[0]][0],
                            terrain[neighbor[1]][neighbor[0]][1],
                            terrain[neighbor[1]][neighbor[0]][2])
            if terrain_type in image_util.TERRAIN_TYPES:
                time_factor = image_util.TERRAIN_TYPES.get(terrain_type)
            else:
                time_factor = 1
            if time_factor is None:
                continue
            local_distance = distance(current, neighbor, elevations)
            time = (local_distance * time_factor) + times.get(current)
            if neighbor not in times or time < times[neighbor]:
                times[neighbor] = time
                distances[neighbor] = local_distance + distances.get(current)
                f_scores[neighbor] = time + heuristic(neighbor, end, elevations)
                parents[neighbor] = current
                heapq.heappush(to_visit, (f_scores[neighbor], neighbor))
                animation_frontier.append(neighbor)
    return None, 0
