import pygame
import random
import map_logic
import settings
import player
import hostile
import bomb
import ui_manager
import explosion

EMPTY = 0
WALL = 1
BREAKABLE_WALL = 2
GADGET = 3
BOMB = 4
PLAYER = 5
HOSTILE = 6

def boom_direction(target_col, target_row):
    if 0 <= target_row < len(active_map) and 0 <= target_col < len(active_map[0]): # overenie zasahu mimo mapy
        if map_logic.check_tile(target_col, target_row, active_map) == BREAKABLE_WALL:
            # Drop gadget with a 30% chance
            if random.random() < 0.3:
                active_map[target_row][target_col] = GADGET
            else:
                active_map[target_row][target_col] = EMPTY
            return False
        if map_logic.check_tile(target_col, target_row, active_map) == WALL:
            return False
        if map_logic.check_tile(target_col, target_row, active_map) == GADGET:
            active_map[target_row][target_col] = EMPTY # Explosion destroys gadget
            return False
        return True
    return False
    
def reset_game():
    new_map = map_logic.get_level_1()
    new_player = None
    new_hostiles = []
    
    for row_idx, row in enumerate(new_map):
        for col_idx, tile in enumerate(row):
            spawn_x = col_idx * settings.TILE_SIZE + 2
            spawn_y = row_idx * settings.TILE_SIZE + 2
            if tile == 5:
                new_player = player.Player(spawn_x, spawn_y)
                new_map[row_idx][col_idx] = 0
            elif tile == 6:
                new_hostiles.append(hostile.Hostile(spawn_x, spawn_y))
                new_map[row_idx][col_idx] = 0
                
    return new_map, new_player, new_hostiles

############################## MAIN ##############################
# 1. Init
pygame.init()
screen = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
pygame.display.set_caption("Bomberman 2026")

active_bombs = []
active_explosions = []
game_over = False

# 2. Ziskanie mapy
manager = ui_manager.Manager()

active_map, my_player, active_hostiles = reset_game()

# 3. Game loop
running = True
clock = pygame.time.Clock()

while running:

    ### Game eventy 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if manager.state == "MENU":
                action = manager.handle_menu_input(event)
                if action == "START":
                    active_map, my_player, active_hostiles = reset_game()
                    active_bombs = []
                    active_explosions = []
                elif action == "QUIT":
                    running = False

            elif manager.state == "PLAYING":
                if event.key == pygame.K_ESCAPE:
                    manager.toggle_pause()

                elif event.key == pygame.K_SPACE:
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

            elif manager.state == "PAUSED":
                if event.key == pygame.K_ESCAPE:
                    manager.toggle_pause()
                elif event.key == pygame.K_q:
                    manager.state = "MENU"

            elif manager.state in ["GAME_OVER", "WIN"]:
                if event.key == pygame.K_r:
                    active_map, my_player, active_hostiles = reset_game()
                    active_bombs = []
                    active_explosions = []
                    manager.state = "PLAYING"
                elif event.key == pygame.K_ESCAPE:
                    manager.state = "MENU"
      

    ### Movement & Logic Update
    if manager.state == "PLAYING":
        if my_player:
            my_player.move(active_map)
            
            # Gadget Pickup Logic
            grid_x = my_player.rect.centerx // settings.TILE_SIZE
            grid_y = my_player.rect.centery // settings.TILE_SIZE
            if 0 <= grid_y < len(active_map) and 0 <= grid_x < len(active_map[0]):
                if active_map[grid_y][grid_x] == GADGET:
                    active_map[grid_y][grid_x] = EMPTY
                    # Increase bomb range (as an example)
                    for mb in active_bombs: # Or increase global bomb range for the player later.
                        # Wait, bomb range is on the Bomb object, we need to increase it for the player.
                        # Since player doesn't currently hold a 'bomb_range', we'll add it simply for future bombs:
                        pass
                    if not hasattr(my_player, 'bomb_range'):
                        my_player.bomb_range = 2
                    my_player.bomb_range += 1

        for current_hostile in active_hostiles:
            current_hostile.move(my_player.rect, active_map)
            if my_player.rect.colliderect(current_hostile.rect):
                manager.player_death()

        ## Bomby update
        for bomb_item in active_bombs[:]:
            if hasattr(my_player, 'bomb_range'):
                 bomb_item.range = my_player.bomb_range

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

                explosion_rects = [bomb_item.rect, explosion_rect_right, explosion_rect_left, explosion_rect_top, explosion_rect_bottom]
                active_explosions.append(explosion.Explosion(explosion_rects))
                
        ## Explozie update a kolizie
        for exp in active_explosions[:]:
            if exp.update():
                active_explosions.remove(exp)
            else:
                for r in exp.rects:
                    if my_player.rect.colliderect(r):
                        manager.player_death()

                for current_hostile in active_hostiles[:]:
                    for r in exp.rects:
                        if current_hostile.rect.colliderect(r):
                            current_hostile.kill()
                            if current_hostile in active_hostiles:
                                active_hostiles.remove(current_hostile)
                            if len(active_hostiles) == 0:
                                manager.player_win()
                            break


    ### Kreslenie
    if manager.state != "MENU":
        for row_idx, row in enumerate(active_map):  # Kreslenie jednotlivych policok TODO do funkcie?!
            for col_idx, tile in enumerate(row):

                x = col_idx * settings.TILE_SIZE
                y = row_idx * settings.TILE_SIZE

                if tile == 0:
                    color = settings.COLOR_GRASS
                elif tile == 1:
                    color = settings.COLOR_WALL
                elif tile == 2:
                    color = settings.COLOR_WALL_BR
                
                if tile in [0, 1, 2]:
                    pygame.draw.rect(screen, color, (x, y, settings.TILE_SIZE, settings.TILE_SIZE))
                
                # Render Gadget manually
                if tile == 3:
                    # Render grass underneath first
                    pygame.draw.rect(screen, settings.COLOR_GRASS, (x, y, settings.TILE_SIZE, settings.TILE_SIZE))
                    # Render Gadget Box (blueish cyan inside)
                    pygame.draw.rect(screen, (0, 255, 255), (x + 10, y + 10, settings.TILE_SIZE - 20, settings.TILE_SIZE - 20))

        for bomb_item in active_bombs:
            bomb_item.draw(screen)

        for exp in active_explosions:
            exp.draw(screen)

        if my_player:
            my_player.draw(screen)

        for current_hostile in active_hostiles:
            current_hostile.draw(screen)

    manager.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()