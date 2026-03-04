import pygame
import map_logic
import settings
import player
import hostile
import bomb

EMPTY = 0
WALL = 1
BREAKABLE_WALL = 2
GADGET = 3
BOMB = 4
PLAYER = 5
HOSTILE = 6


def boom_direction(target_col, target_row):
    if 0 <= target_row < len(active_map) and 0 <= target_col < len(active_map[0]): #overenie zasahu mimo mapy
        if(map_logic.check_tile(target_col, target_row, active_map) == BREAKABLE_WALL): #overenie bloku ci je znicitelny atd
            active_map[target_row][target_col] = EMPTY
            return False
        if(map_logic.check_tile(target_col, target_row, active_map) == WALL):
            return False
        return True
############################## MAIN ##############################
# 1. Init
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
pygame.display.set_caption("Bomberman 2026")

active_bombs = []
game_over = False

# 2. Ziskanie mapy
active_map = map_logic.get_level_1()
active_player = None
active_hostiles = []

# Spawning player and hostile
for row_idx, row in enumerate(active_map):
    for col_idx, tile in enumerate(row):
        if tile == 5:
            spawn_x = col_idx * settings.TILE_SIZE + 2
            spawn_y = row_idx * settings.TILE_SIZE + 2
            my_player = player.Player(spawn_x, spawn_y)
            active_map[row_idx][col_idx] = 0 # Nahrada spawnpointu za empty

        elif tile == 6:
            spawn_x = col_idx * settings.TILE_SIZE + 2
            spawn_y = row_idx * settings.TILE_SIZE + 2
            my_hostile = hostile.Hostile(spawn_x, spawn_y)
            active_map[row_idx][col_idx] = 0 # Nahrada spawnpointu za empty
            active_hostiles.append(my_hostile)

# 3. Game loop
running = True
clock = pygame.time.Clock()

while running:

    ### Game eventy 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:

                if my_player and my_player.can_place_bomb():
                    new_bomb = bomb.Bomb(my_player.rect.x, my_player.rect.y)
                    is_free = True

                    for bombito in active_bombs:
                        if bombito.rect.colliderect(new_bomb.rect):
                            is_free = False
                            break
                    if is_free:
                        active_bombs.append(new_bomb)
                        my_player.ammo_descrease()
                        

    ### Movement
    if my_player:
        my_player.move(active_map)

    for current_hostile in active_hostiles:
        current_hostile.move(my_player.rect, active_map)

    ## Bomby update
    for bomb_item in active_bombs[:]:
        exploded = bomb_item.update()

        if not bomb_item.isSolid and not my_player.rect.colliderect(bomb_item.rect):
            bomb_item.isSolid = True
            grid_x = bomb_item.rect.centerx // settings.TILE_SIZE
            grid_y = bomb_item.rect.centery // settings.TILE_SIZE
            active_map[grid_y][grid_x] = BOMB

        if exploded:
            grid_x = bomb_item.rect.centerx // settings.TILE_SIZE
            grid_y = bomb_item.rect.centery // settings.TILE_SIZE
            active_map[grid_y][grid_x] = EMPTY
            active_bombs.remove(bomb_item)
            my_player.ammo_increase()
            
            ranger = 1
            runner = True
            while(ranger <= bomb_item.range and runner):
                runner = boom_direction((bomb_item.rect.centerx + ranger * settings.TILE_SIZE) // settings.TILE_SIZE, bomb_item.rect.centery // settings.TILE_SIZE)
                ranger+=1
            right_ranger = ranger - 1

            ranger = 1
            runner = True
            while(ranger <= bomb_item.range and runner):
                runner = boom_direction((bomb_item.rect.centerx - ranger * settings.TILE_SIZE) // settings.TILE_SIZE, bomb_item.rect.centery // settings.TILE_SIZE)
                ranger+=1
            left_ranger = ranger - 1

            ranger = 1
            runner = True
            while(ranger <= bomb_item.range and runner):
                runner = boom_direction(bomb_item.rect.centerx // settings.TILE_SIZE, (bomb_item.rect.centery - ranger * settings.TILE_SIZE) // settings.TILE_SIZE)
                ranger+=1
            top_ranger = ranger - 1

            ranger = 1
            runner = True
            while(ranger <= bomb_item.range and runner):
                runner = boom_direction(bomb_item.rect.centerx // settings.TILE_SIZE, (bomb_item.rect.centery + ranger * settings.TILE_SIZE) // settings.TILE_SIZE)
                ranger+=1
            bottom_ranger = ranger - 1


            explosion_rect_right = pygame.Rect(
                bomb_item.rect.right,
                bomb_item.rect.top,
                right_ranger * settings.TILE_SIZE,
                settings.TILE_SIZE
            )
            explosion_rect_left = pygame.Rect(
                bomb_item.rect.x - left_ranger * settings.TILE_SIZE,
                bomb_item.rect.y,
                left_ranger * settings.TILE_SIZE,
                settings.TILE_SIZE
            )
            explosion_rect_top = pygame.Rect(
                bomb_item.rect.x,
                bomb_item.rect.y - top_ranger * settings.TILE_SIZE,
                settings.TILE_SIZE,
                top_ranger * settings.TILE_SIZE
            )
            explosion_rect_bottom = pygame.Rect(
                bomb_item.rect.x,
                bomb_item.rect.bottom,
                settings.TILE_SIZE,
                bottom_ranger * settings.TILE_SIZE
            )

            # Vykreslenie vybuchov bomb
            pygame.draw.rect(screen, (255, 255, 0), explosion_rect_right)
            pygame.draw.rect(screen, (255, 255, 0), explosion_rect_left)
            pygame.draw.rect(screen, (255, 255, 0), explosion_rect_top)
            pygame.draw.rect(screen, (255, 255, 0), explosion_rect_bottom)
            pygame.display.flip()

            if (my_player.rect.colliderect(bomb_item.rect) or
                my_player.rect.colliderect(explosion_rect_right) or 
                my_player.rect.colliderect(explosion_rect_left) or 
                my_player.rect.colliderect(explosion_rect_top) or 
                my_player.rect.colliderect(explosion_rect_bottom)
            ):
                my_player.kill()
                pygame.display.flip()
                pygame.time.delay(2000)
                
                #jump main menu
            for currecnt_hostile in active_hostiles[:]:
                if (currecnt_hostile.rect.colliderect(bomb_item.rect) or
                    currecnt_hostile.rect.colliderect(explosion_rect_right) or 
                    currecnt_hostile.rect.colliderect(explosion_rect_left) or 
                    currecnt_hostile.rect.colliderect(explosion_rect_top) or 
                    currecnt_hostile.rect.colliderect(explosion_rect_bottom)
                ):
                    currecnt_hostile.kill()
                    active_hostiles.remove(currecnt_hostile)


    ### Kreslenie
    for row_idx, row in enumerate(active_map):  # Kreslenie jednotlivych policok TODO do funkcie?!
        for col_idx, tile in enumerate(row):

            x = col_idx * settings.TILE_SIZE
            y = row_idx * settings.TILE_SIZE

            if tile == 0:
                color = settings.COLOR_GRASS
            elif tile == 1:
                color = settings.COLOR_WALL
            else:
                color = settings.COLOR_WALL_BR

            pygame.draw.rect(screen, color, (x, y, settings.TILE_SIZE, settings.TILE_SIZE))

    for bomb_item in active_bombs:
        bomb_item.draw(screen)

    if my_player:
        my_player.draw(screen)

    for current_hostile in active_hostiles:
        current_hostile.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

