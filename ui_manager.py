import pygame
import settings


class Manager:

    def __init__(self):
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Impact", 80)
        self.font_big = pygame.font.SysFont("Impact", 64)
        self.font_small = pygame.font.SysFont("Arial", 24)
        self.state = "MENU"
        self.menu_options = ["START GAME", "QUIT"]
        self.menu_selected = 0

    def draw(self, screen):
        if self.state == "GAME_OVER":
            self.render_overlay(screen, "YOU DIED!", (200, 0, 0), "Press R to Restart or ESC for Menu")
        elif self.state == "WIN":
            self.render_overlay(screen, "LEVEL PASSED!", (0, 200, 0), "Press R to Restart or ESC for Menu")
        elif self.state == "PAUSED":
            self.render_overlay(screen, "PAUSED", (200, 200, 200), "Press ESC to Resume or Q for Menu")
        elif self.state == "MENU":
            self.draw_main_menu(screen)

    def draw_main_menu(self, screen):
        screen.fill((20, 20, 40))
        
        # Title
        title_surf = self.font_title.render("BOMBERMAN 2026", True, (255, 255, 0))
        title_rect = title_surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 3))
        screen.blit(title_surf, title_rect)

        # Options
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 255) if i == self.menu_selected else (100, 100, 100)
            opt_surf = self.font_big.render(option, True, color)
            opt_rect = opt_surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 2 + i * 80))
            screen.blit(opt_surf, opt_rect)

        # Instructions
        inst_surf = self.font_small.render("Use UP/DOWN to select, ENTER to confirm", True, (150, 150, 150))
        inst_rect = inst_surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H - 50))
        screen.blit(inst_surf, inst_rect)

    def handle_menu_input(self, event):
        if event.key == pygame.K_UP:
            self.menu_selected = (self.menu_selected - 1) % len(self.menu_options)
        elif event.key == pygame.K_DOWN:
            self.menu_selected = (self.menu_selected + 1) % len(self.menu_options)
        elif event.key == pygame.K_RETURN:
            if self.menu_selected == 0:
                self.state = "PLAYING"
                return "START"
            elif self.menu_selected == 1:
                return "QUIT"
        return None

    def render_overlay(self, screen, text, color, instruction):
        overlay = pygame.Surface((settings.SCREEN_W, settings.SCREEN_H))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # 2. Hlavný text
        surf = self.font_big.render(text, True, color)
        rect = surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 2 - 20))
        screen.blit(surf, rect)

        # 3. Inštrukcia pre hráča
        retry_surf = self.font_small.render(instruction, True, (255, 255, 255))
        retry_rect = retry_surf.get_rect(center=(settings.SCREEN_W // 2, settings.SCREEN_H // 2 + 50))
        screen.blit(retry_surf, retry_rect)

    def player_death(self):
        self.state = "GAME_OVER"

    def player_win(self):
        self.state = "WIN"

    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
        elif self.state == "PAUSED":
            self.state = "PLAYING" 
