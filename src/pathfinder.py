# G-skóre: Presný počet krokov od štartu (príšery) na toto políčko.

# H-skóre (Heuristika): Odhadovaný počet krokov od tohto políčka k cieľu (hráčovi). Tu použiješ spomínaný vzorec: abs(x1 - x2) + abs(y1 - y2).

# F-skóre: Súčet G + H.

EMPTY = 0

def get_current_neighbors(current):
    current_col, current_row = current

    directions = [
        (1, 0),  # left
        (-1, 0), # right
        (0, 1),  # top
        (0, -1)  # bottom
    ]

    neighbors = []
    for dir_col, dir_row in directions:
        neighbor_col = current_col + dir_col 
        neighbor_row = current_row + dir_row
        neighbors.append((neighbor_col, neighbor_row))
    
    return neighbors

def get_h(start, target):
    dist_x = abs(start[0] - target[0])
    dist_y = abs(start[1] - target[1])

    return dist_x + dist_y

def get_path(parents, current):
    path = []
    path.append(current)

    while current in parents:
        current = parents[current]
        path.append(current)
    
    path.reverse()
    return path

def find_path(start, target, active_map):
    open_list = []
    closed_list = []
    parents = {} #format dieta:rodic

    g_scores = {start: 0}
    f_scores = {start: get_h(start, target)}

    open_list.append(start)

    while len(open_list) > 0:

        current = min(open_list, key=lambda node: f_scores[node]) #funkcia najde najmensie policko s hodnotou F, vymaze ho z open_list
        open_list.remove(current)
        closed_list.append(current)

        if current != target:
            current_neighbors = get_current_neighbors(current)
            for neighbor in current_neighbors:  # right, left, top, bottom
                neighbor_col = neighbor[0]
                neighbor_row = neighbor[1]

                if 0 <= neighbor_row < len(active_map) and 0 <= neighbor_col < len(active_map[0]):
                    if not neighbor in closed_list:
                        if (active_map[neighbor_row][neighbor_col] in [0, 3, 7] or neighbor == target):  
                            g_score = g_scores[current] + 1
                            
                            if not neighbor in open_list:
                                open_list.append(neighbor)
                            
                            elif not g_score >= g_scores.get(neighbor, 999999):
                                continue
                            parents[neighbor] = current
                            g_scores[neighbor] = g_score
                            f_scores[neighbor] = g_score + get_h(neighbor, target)
        else:
            return get_path(parents, current) # vyskalda cestu podla slovnicka cez rodicov 
                    