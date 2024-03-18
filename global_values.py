
# map pixel width and height
MAX_X = 395
MAX_Y = 500

# grid sizes
GRID_WIDTH = 10.29
GRID_HEIGHT = 7.55

# path color
PATH_COLOR = (118, 63, 231)

# RGB values for the various terrain types and the associated time cost scalar
TERRAIN_TYPES = {
    (248, 148, 18): 1,     # OPEN_LAND
    (255, 192, 0): 50,     # ROUGH_MEADOW
    (255, 255, 255): 3,    # EASY_FOREST
    (2, 208, 60): 5,       # SLOW_FOREST
    (2, 136, 40): 25,      # WALK_FOREST
    (71, 51, 3): 1,        # PAVED_ROAD
    (0, 0, 0): 3,          # FOOTPATH
    (205, 0, 101): None,   # OUT_OF_BOUNDS
    (5, 73, 24): None,     # IMPASSIBLE_VEGETATION
    (0, 0, 255): 1000      # WATER
}
