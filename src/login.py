import pygame
import sys
from colors import BLACK, GREEN, WHITE

class Login:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Вход/Регистрация")

        self.game_name_font = pygame.font.Font(None, 156)
        self.main_font = pygame.font.Font(None, 120)
        self.button_font = pygame.font.Font(None, 72)

    def draw_button(self, text, x, y, width, height):
        button_rect = pygame.Rect(x, y, width, height)

        pygame.draw.rect(self.screen, BLACK, button_rect)

        pygame.draw.rect(self.screen, WHITE, button_rect, 3)

        text_surface = self.button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        return button_rect

    def draw_text(self, text, x, y, font, color):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def main_loop(self):
        running = True

        while running:
            self.screen.fill(BLACK)
            login_button = self.draw_button("Войти", 150, self.HEIGHT // 2, 500, 75)
            registration_button = self.draw_button("Регистрация", 150, self.HEIGHT // 2 - 150, 500, 75)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if registration_button.collidepoint(event.pos):
                            return "register"
                        if login_button.collidepoint(event.pos):
                            return "log_in"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            pygame.display.flip()