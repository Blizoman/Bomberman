import pygame
import settings
import pathfinder

class Hostile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4)
        self.color = settings.COLOR_HOSTILE
        self.speed = 1
        self.path = []
        self.last_player_grid = None

    def kill(self):
        print("Hostile died!")
        # ++ hracove body/killy/HP/mana na gadget idk 

    def check_collision(self, active_map):
        corners = [
            (self.rect.left, self.rect.top),
            (self.rect.right, self.rect.top),
            (self.rect.left, self.rect.bottom),
            (self.rect.right, self.rect.bottom),
        ]
        for (x_px, y_px) in corners:
            grid_x = x_px // settings.TILE_SIZE
            grid_y = y_px // settings.TILE_SIZE

            if 0 <= grid_y < len(active_map) and 0 <= grid_x < len(active_map[0]):
                tile_value = active_map[grid_y][grid_x]

                if tile_value != 0:
                    return True
        return False

    def move(self, player_rect, active_map): # Automatizacia A-star cez AI ? 
        enemy_grid = (self.rect.centerx // settings.TILE_SIZE, self.rect.centery // settings.TILE_SIZE)
        player_grid = (player_rect.centerx // settings.TILE_SIZE, player_rect.centery // settings.TILE_SIZE)

        if player_grid != self.last_player_grid:
            self.path = pathfinder.find_path(enemy_grid, player_grid, active_map)
            self.last_player_grid = player_grid

        if self.path and len(self.path) > 1:
            next_step = self.path[1]

            target_x = next_step[0] * settings.TILE_SIZE + settings.TILE_SIZE // 2
            target_y = next_step[1] * settings.TILE_SIZE + settings.TILE_SIZE // 2

            if self.rect.centerx < target_x: self.rect.centerx += self.speed
            elif self.rect.centerx > target_x: self.rect.centerx -= self.speed

            if self.rect.centery < target_y: self.rect.centery += self.speed
            elif self.rect.centery > target_y: self.rect.centery -= self.speed

            if abs(self.rect.centerx - target_x) < self.speed and abs(self.rect.centery - target_y) < self.speed:
                self.path.pop(0)


    def draw(self, screen):
        pygame.draw.rect(screen ,self.color, self.rect)