"""
Searching logic and related functions
Author: Kilian Jakstis
"""

# edit me
# def search(initial, end, words):
#     visited = set()
#     backtrack = {}
#     to_visit = [initial]
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
#         new_words = get_next(current, words)  # generate new words
#         for word in new_words:
#             if word not in backtrack:
#                 backtrack[word] = current  # mark new words' parent as current word
#         to_visit.extend(new_words)
#         visited.add(current)
#     path = []
#     head = end
#     while head is not None:  # backtrack until head is None to generate path
#         path.append(head)
#         head = backtrack.get(head)
#     return path[::-1]
