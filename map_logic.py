# 0 - empty, 1 - wall, 2 - breakable wall, 3 - gadget, 4 - bomb,5 - player spawn
# , 6 - hostile spawn, (5 and 6 will be changed after movement 
# (of either player or hostile from that specific position) to 0, as empty)
import random


def get_level_1():                              # Vytvorenie mapy 
    rows, cols = 15, 15
    level = []
    for y in range(rows):
        row = []
        for x in range(cols):
            if x == 0 or x == cols-1 or y == 0 or y == rows-1:
                row.append(1)
            elif x % 2 == 0 and y % 2 == 0:
                row.append(1)
            else:
                row.append(0)

            if row[x] == 0:
                if random.random() < 0.3:
                    row[x] = 2
        level.append(row)
    level[1][1] = 5
    level[1][cols-2] = 6
    level[rows-2][1] = 6
    level[rows-2][cols-2] = 6

    return level

def check_tile(x, y, map):                      # Typ policka
    return map[y][x]
