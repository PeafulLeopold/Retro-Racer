import pygame
import sys
from colors import BLACK, GREEN, WHITE
from game import Game

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Вход/Регистрация")

game_name_font = pygame.font.Font(None, 156)
main_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 72)


def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, GREEN, button_rect)
    text_surface = button_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect


def draw_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


class Login:
    def login(self):
        while True:
            screen.fill(BLACK)
            login_button = draw_button("Войти", 150, HEIGHT // 2, 500, 75)
            registration_button = draw_button("Зарегистрироваться", 150, HEIGHT // 2 - 150, 500, 75)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if registration_button.collidepoint(event.pos):
                            return "register"
                        if login_button.collidepoint(event.pos):
                            return "login"
            pygame.display.flip()
