import pygame
import settings

class bomb:
    def __init__(self):
        self.rect = pygame.Rect(x, y, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4) # x, y - urcit prob podla playera bomba sa polozi tam kde bude on
        self.range = 2 # dosah bomby TILE kde stoji + dva dalsie do kazdej strany 