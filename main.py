import pygame
import map_logic
import settings
import player
import hostile
import bomb
############################## MAIN ##############################
# 1. Init
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
pygame.display.set_caption("Bomberman 2026")

active_bombs = []

# 2. Ziskanie mapy
active_map = map_logic.get_level_1()
active_player = None
active_hostile = None

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
                    active_bombs.append(new_bomb)
                    my_player.ammo_descrease()
    
    ### Movement
    if my_player:
        my_player.move(active_map)

    ## Bomby update
    for bomb_item in active_bombs[:]:
        exploded = bomb_item.update()
        if exploded:
            active_bombs.remove(bomb_item)
            if my_player:
                my_player.ammo_descrease()

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

    if my_hostile:
        my_hostile.draw(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()

