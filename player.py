import pygame
import settings
import bomb


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, settings.TILE_SIZE - 4, settings.TILE_SIZE - 4)
        self.color = settings.COLOR_PLAYER
        self.speed = 4
        self.current_bombs = 0
        self.max_bombs = 1
    
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
    
    def move(self, active_map):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            if self.check_collision(active_map):
                self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            if self.check_collision(active_map):
                self.rect.x += self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            if self.check_collision(active_map):
                self.rect.y -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            if self.check_collision(active_map):
                self.rect.x -= self.speed

    def can_place_bomb(self):
        if self.current_bombs < self.max_bombs:
            return True
        return False
    
    def ammo_descrease(self):
        self.current_bombs += 1

    def draw(self, screen):
        pygame.draw.rect(screen ,self.color, self.rect)