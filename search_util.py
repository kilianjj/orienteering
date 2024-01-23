"""
Searching logic and related functions
Author: Kilian Jakstis
"""

MAX_X = 394
MAX_Y = 499

######################## test version functions, work on ones below ####################################

def dumb_search(start, end):
    path = []
    max_y = max(start[1], end[1])
    min_y = min(start[1], end[1])
    max_x = max(start[0], end[0])
    min_x = min(start[0], end[0])
    for x in range(min_x, max_x):
        path.append((x, min_y))
    for y in range(min_y, max_y):
        path.append((max_x, y))
    return path

def get_route(terrain, elevations, poi_path):
    if len(poi_path) < 2:
        print("POI path not long enough")
        return
    route = []
    start = poi_path.pop(0)
    end = poi_path.pop(0)
    while True:
        between_points = dumb_search(start, end)
        route.extend(between_points)
        if len(poi_path) == 0:
            break
        start = end
        end = poi_path.pop(0)
    return route

########################## real functions below ##############################

# this one is good, make alterations to search function and add relevant ones
# def get_route(terrain, elevations, poi_path):
#     if len(poi_path) < 2:
#         print("POI path not long enough")
#         return
#     route = []
#     start = poi_path.pop(0)
#     end = poi_path.pop(0)
#     while True:
#         between_points = search(start, end, terrain, elevations)
#         route.extend(between_points)
#         if len(poi_path) == 0:
#             break
#         start = end
#         end = poi_path.pop(0)
#     return route
#
# # is this fine?
# def heuristic(coordinate, target, elevations):
#     long_distance = (coordinate[0] - target[0]) ** 2
#     lat_distance = (coordinate[1] - coordinate[1]) ** 2
#     height_distance = (elevations[coordinate[0]][coordinate[1]] - elevations[target[0]][target[1]]) ** 2
#     return (long_distance + lat_distance + height_distance) ** 1/3
#
# def search(start, end, terrain, elevations):
#     visited = set()
#     backtrack = {}
#     to_visit = [start]
#     parent = None
#     while len(to_visit) != 0:
#         current = to_visit.pop(0)
#         if current in visited:  # skip over words that have already been seen
#             continue
#         if parent is None:
#             backtrack[current] = None  # mark start word's parent as None
#             parent = False
#         if current == end:
#             break
#         # generate new positions
#         # for word in new_words:
#         #     if word not in backtrack:
#         #         backtrack[word] = current  # mark new words' parent as current word
#         # to_visit.extend(new_words)
#         # visited.add(current)
#     path = []
#     head = end
#     while head is not None:  # backtrack until head is None to generate path
#         path.append(head)
#         head = backtrack.get(head)
#     return path[::-1]
