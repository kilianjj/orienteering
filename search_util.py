"""
Searching logic and related functions
Author: Kilian Jakstis
"""

import heapq
import image_util
import time as sleep

def get_route(terrain, elevations, poi_path, x, y, out):
    """
    Get the full route by constructing smaller routes between pairs of points in the specified order
    :param terrain: RGB array of terrain image
    :param elevations: elevation array
    :param poi_path: list of POIs in the order they must be visited
    :param x: x dimension length
    :param y: y dimension length
    :param out: animation file writer
    :return: full route (as a list of coordinate tuples) in order of those visited
    """
    if len(poi_path) < 2:
        # only 1 point - no target
        return
    image_util.update_image(terrain, out)
    sleep.sleep(3)
    total_distance = 0
    route = []
    for i in range(len(poi_path) - 1):
        between_points, between_distance = search(poi_path[i], poi_path[i+1], terrain, elevations, route, x, y, out)
        if between_points is None:
            continue             # path not found
        route.extend(between_points)
        total_distance += between_distance
        # draw changes
        image_util.update_image_path(terrain, route, poi_path[i], poi_path[i+1], out)
    image_util.update_image_path(terrain, route, poi_path[0], poi_path[-1], out)
    # print(f"Total Distance: {total_distance}m")
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
    # x = ((coordinate[0] - target[0]) * image_util.GRID_WIDTH) ** 2
    # y = ((coordinate[1] - target[1]) * image_util.GRID_HEIGHT) ** 2
    x = (coordinate[0] - target[0]) ** 2
    y = (coordinate[1] - target[1]) ** 2
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

def get_neighbors(coordinate, max_x, max_y):
    """
    Get neighbor coordinates from current
    :param coordinate: current point
    :param max_x: max x value
    :param max_y: max y value
    :return: list of neighbor coordinate tuples
    """
    neighbors = []
    rows, cols = max_y, max_x
    # uncomment to get diagonal neighbors too
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
        if 0 <= new_row < rows and 0 <= new_col < cols and new_row < max_y and new_col < max_x:
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

def search(start, end, terrain, elevations, route, x, y, out):
    """
    A* search algorithm
    :param start: start point
    :param end: end point
    :param terrain: array of terrain image RGB values
    :param elevations: elevation data
    :param route: current route path between POIs
    :param x: width length
    :param y: height length
    :param out: animation file writer
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
    iteration = 0
    scale = 50
    max_animation_iterations = int(x * y / scale)
    ratio = distance(start, end, elevations) / distance((0, 0), (x-1, y-1), elevations) * (x * y) / 100000
    sleep.sleep(1)  # wait a second before starting new search
    while to_visit:
        # update display only after quite a few iterations to speed it up
        if iteration == int(max_animation_iterations * ratio):
            iteration = 0
            image_util.update_search(terrain, animation_frontier, visited, route, start, end, out)
        else:
            iteration += 1
        current = heapq.heappop(to_visit)[1]
        if current in animation_frontier:
            animation_frontier.remove(current)
        if current == end:
            return construct_path(parents, start, end), distances.get(end)
        visited.add(current)
        for neighbor in get_neighbors(current, x, y):
            if neighbor in visited:
                continue
            terrain_type = (terrain[neighbor[1]][neighbor[0]][0],
                            terrain[neighbor[1]][neighbor[0]][1],
                            terrain[neighbor[1]][neighbor[0]][2])
            time_factor = image_util.TERRAIN_TYPES.get(terrain_type) if terrain_type in image_util.TERRAIN_TYPES \
                else None
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
