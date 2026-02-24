# 0 - empty, 1 - wall, 2 - breakable wall, 3 - gadget, 4 - bomb,
# 5 - player spawn, 6 - hostile spawn, (5 and 6 will be changed after movement 
# (of either player or hostile from that specific position) to 0, as empty)


TILE_SIZE = 50 # Velkost jendoho policka bude 50 pixelov 
SCREEN_W = 800 #px
SCREEN_H = 600 #px

# Map
COLOR_GRASS = (0, 255, 0)
COLOR_WALL = (30, 30, 30)
COLOR_WALL_BR = (110, 110, 110)
COLOR_BOMB = (255, 255, 100)
#COLOR_GADGET
#COLOR_PSPAWN
#COLOR_HSPAWN

# Player
COLOR_PLAYER = (0, 20 , 255)

# Hostile
COLOR_HOSTILE = (255, 20, 0)
