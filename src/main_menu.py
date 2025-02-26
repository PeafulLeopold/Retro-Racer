import pygame
import sys

from colors import BLACK, WHITE
from game import Game
from login import Login
from register import Registration
from garage import Garage
from settings import Settings
from leaderboard import Leaderboard

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

game_name_font = pygame.font.Font(None, 156)
main_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 72)

# Загрузка и воспроизведение фоновой музыки
pygame.mixer.music.load("data/sounds/menu_sound.mp3")  # Загружаем музыку
pygame.mixer.music.set_volume(0.5)  # Устанавливаем громкость (от 0.0 до 1.0)
pygame.mixer.music.play(-1)  # Воспроизводим музыку бесконечно

def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, button_rect)  # Черный фон кнопки
    pygame.draw.rect(screen, WHITE, button_rect, 2)  # Белая обводка кнопки
    text_surface = button_font.render(text, True, WHITE)  # Белый текст
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main_menu(game_state):
    while True:
        screen.fill(BLACK)  # Темный фон
        login_button = draw_button("Войти", 640, 20, 150, 75)
        draw_text("Retro-Racer", WIDTH // 2, 185, game_name_font, WHITE)
        play_button = draw_button("Играть", 175, 300, 450, 75)
        garage_button = draw_button("Гараж", 175, 425, 450, 75)
        settings_button = draw_button("Настройки", 175, 550, 450, 75)
        leaders_button = draw_button("Таблица лидеров", 175, 675, 450, 75)

        # Отображение количества денег из game_state
        draw_text(f"Деньги: {game_state.money}$", 150, 25, button_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_button.collidepoint(event.pos):
                        return "play"
                    if login_button.collidepoint(event.pos):
                        return 'login'
                    if settings_button.collidepoint(event.pos):
                        return 'settings'
                    if leaders_button.collidepoint(event.pos):
                        return 'leaders'

        pygame.display.flip()

class GameState:
    def __init__(self):
        self.money = 0  # Количество денег

if __name__ == "__main__":
    game_state = GameState()  # Создаем объект GameState

    while True:
        action = main_menu(game_state)  # Передаем game_state в главное меню
        if action == "play":
            pygame.mixer.music.stop()  # Останавливаем музыку перед запуском игры
            game = Game(game_state)  # Передаем game_state в игру
            # В основном коде игры
            game.game_loop()  # Запускаем игровой цикл
            pygame.mixer.music.play(-1)  # Возобновляем музыку после завершения игры
        if action == 'login':
            login_window = Login()
            login_loop = login_window.main_loop()
           
            if login_loop == 'register':
                registration_window = Registration()
                registration_window.main_loop()
        if action == 'garage':
            garage = Garage(game_state)  # Передаем game_state в гараж
            garage.run()
        if action == 'settings':
            sets = Settings()
            game.player.control_scheme = sets.control_scheme
            sets.run()
        if action == 'leaders':
            leads = Leaderboard()
            leads.run()