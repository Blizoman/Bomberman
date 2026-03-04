import pygame
import settings


class Manager:

    def __init__(self):
        pygame.font.init()
        self.font_big = pygame.font.SysFont("Impact", 64)
        self.font_small = pygame.font.SysFont("Arail", 24)
        self.state = "PLAYING"

    def draw(self, screen):
        if self.state == "GAME_OVER":
            self.render_overlay(screen, "YOU DIED!", (200, 0, 0))
        elif self.state == "WIN":
            self.render_overlay(screen, "LEVEL PASSED!", (0, 200, 0))

    def render_overlay(self, screen, text, color):
        overlay = pygame.Surface((settings.SCREEN_W, settings.SCREEN_H))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # 2. Hlavný text
        surf = self.font_big.render(text, True, color)
        rect = surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 2 - 20))
        screen.blit(surf, rect)

        # 3. Inštrukcia pre hráča
        retry_surf = self.font_small.render("Press R to Restart or ESC for Menu", True, (255, 255, 255))
        retry_rect = retry_surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 2 + 50))
        screen.blit(retry_surf, retry_rect)

    def player_death(self):
        self.state = "GAME_OVER"

    def player_win(self):
        self.state = "WIN"

    def monster_death(self):
        pass

    #TODO jump to menu????? 
