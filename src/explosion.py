import pygame

class Explosion:
    def __init__(self, rects, life_time=30):
        self.rects = rects
        self.life_time = life_time
        self.color = (255, 150, 0) # Oranzova pre explozie

    def update(self):
        self.life_time -= 1
        return self.life_time <= 0

    def draw(self, screen):
        for r in self.rects:
            pygame.draw.rect(screen, self.color, r)
