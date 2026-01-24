# 0 - empty, 1 - wall, 2 - breakable wall, 3 - gadget, 4 - bomb,5 - player spawn, 6 - hostile spawn, (5 and 6 will be changed after movement (of either player or hostile from that specific position) to 0, as empty)

def get_level_1():                              # Vytvorenie mapy 
    level = [
        [1,1,1,1,1],
        [1,0,0,5,1],
        [1,2,1,0,1],
        [1,6,2,0,1],
        [1,1,1,1,1]
    ]
    return level

def check_tile(x, y, map):                      # Typ policka
    return map[y][x]
