"""
Searching logic and related functions
Author: Kilian Jakstis
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
    (248, 148, 18): 1,     # OPEN_LAND
    (255, 192, 0): 10,     # ROUGH_MEADOW
    (255, 255, 255): 1,    # EASY_FOREST
    (2, 208, 60): 2,       # SLOW_FOREST
    (2, 136, 40): 5,       # WALK_FOREST
    (71, 51, 3): 1,        # PAVED_ROAD
    (0, 0, 0): 1,          # FOOTPATH
    (205, 0, 101): None,   # OUT_OF_BOUNDS
    (5, 73, 24): None,     # IMPASSIBLE_VEGETATION
    (0, 0, 255): None      # WATER
}

# this one is good, make alterations to search function and add relevant ones
def get_route(terrain, elevations, poi_path):
    if len(poi_path) < 2:
        print("POI path not long enough")
        return
    total_distance = 0
    route = []
    start = poi_path.pop(0)
    target = poi_path.pop(0)
    # todo: convert to for
    while True:
        between_points, between_distance = search(start, target, terrain, elevations)
        print(target)
        # print(between_points)
        if between_points is None:
            continue
        route.extend(between_points)
        total_distance += between_distance
        if len(poi_path) == 0:
            break
        start = target
        target = poi_path.pop(0)
    print(f"Total Distance: {total_distance}m")
    return set(route)

# plug neighbors into this for cost function
def distance(coordinate, target, elevations, heuristic_bool):
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

# is this fine? 3d distance from current point to target, might want to pass in terrains
def heuristic(coordinate, target, elevations):
    return distance(coordinate, target, elevations, True)

# get neighbors
def get_neighbors(coordinate):
    # Todo: not gonna lie i think the coordinates are formatted as (y, x) but its working so ima keep it
    neighbors = []
    rows, cols = MAX_Y, MAX_X
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for y, x in directions:
        new_row, new_col = coordinate[1] + x, coordinate[0] + y
        if 0 <= new_row < rows and 0 <= new_col < cols and new_row < MAX_X and new_col < MAX_Y:
            neighbors.append((new_col, new_row))
    return neighbors

# backtrack to get path after A*
def construct_path(visited_nodes, start, end):
    path = []
    head = end
    while head is not start:  # backtrack until head is None to generate path
        path.append(head)
        head = visited_nodes.get(head)
    path.append(start)
    return path[::-1]

# A* stuff
def search(start, end, terrain, elevations):
    # todo: incorporate terrain data, distance, heuristic, etc
    # todo: distance calculations need to update to account for grid size, direction, etc
    visited = set()
    to_visit = []   # priority queue for new nodes to visit
    g_scores = {start: 0}
    f_scores = {start: heuristic(start, end, elevations)}
    parents = {}
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
            time_factor = terrain_types.get(terrain_type)       # todo: check indexing
            if time_factor is None:
                continue
            g_score = distance(current, neighbor, elevations, False) + g_scores.get(current)
            if neighbor not in g_scores or g_score < g_scores[neighbor]:
                g_scores[neighbor] = g_score
                f_scores[neighbor] = g_score + heuristic(neighbor, end, elevations) * time_factor   # comment out time factor if issues
                parents[neighbor] = current
                heapq.heappush(to_visit, (f_scores[neighbor], neighbor))
    return None, 0
