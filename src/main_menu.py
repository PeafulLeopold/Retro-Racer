import pygame
import sys
from colors import BLACK, GREEN, WHITE
from game import Game

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

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

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text("Retro-Racer", WIDTH // 2, 50, game_name_font, WHITE)
        draw_text("Главное меню", WIDTH // 2, 150, main_font, WHITE)
        play_button = draw_button("Играть", 175, 200, 450, 75)
        garage_button = draw_button("Гараж", 175, 325, 450, 75)
        settings_button = draw_button("Настройки", 175, 450, 450, 75)
        leaders_button = draw_button("Таблица лидеров", 175, 575, 450, 75)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return "play"

        pygame.display.flip()

if __name__ == "__main__":
    while True:
        action = main_menu()
        if action == "play":
            game = Game()
            game.game_loop()
