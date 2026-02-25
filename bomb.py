import pygame
import settings

class Bomb:
    def __init__(self, x, y):
        center_x = x // settings.TILE_SIZE
        center_y = y // settings.TILE_SIZE
        self.rect = pygame.Rect(center_x * settings.TILE_SIZE + 2, center_y * settings.TILE_SIZE + 2, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4) # x, y - urcit prob podla playera bomba sa polozi tam kde bude on
        self.range = 2 # dosah bomby TILE kde stoji + jeden dalsi do kazdej strany 
        self.time = 3 * 60 # 3 sekundy od polozenia do vybuchu
        self.color = settings.COLOR_BOMB

    def update(self):
        self.time -= 1

        if self.time <= 0:
            return True
        else:
            return False

    def range_increase(self):
        self.range += 1
        
    def draw(self, screen):
        pygame.draw.rect(screen ,self.color, self.rect)