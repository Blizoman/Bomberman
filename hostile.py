import pygame
import settings
import pathfinder

class Hostile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4)
        self.color = settings.COLOR_HOSTILE
        self.speed = 2
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

    def move(self, active_map): # Automatizacia A-star cez AI ? 
        pass

    def draw(self, screen):
        pygame.draw.rect(screen ,self.color, self.rect)