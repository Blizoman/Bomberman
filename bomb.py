import pygame
import settings

class Bomb:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4) # x, y - urcit prob podla playera bomba sa polozi tam kde bude on
        self.range = 2 # dosah bomby TILE kde stoji + dva dalsie do kazdej strany 
        self.time = 3 * 60 # 3 sekundy od polozenia do vybuchu
        self.color = settings.COLOR_BOMB

    def update(self):
        self.time -= 1

        if self.time <= 0:
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.rect(screen ,self.color, self.rect)