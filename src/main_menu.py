import pygame
import sys

from colors import BLACK, WHITE
from game import Game
from log_in import Log_In  
from register import Registration
from garage import Garage
from settings import Settings
from leaderboard import Leaderboard
from login import Login 

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

game_name_font = pygame.font.Font(None, 156)
main_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 72)

pygame.mixer.music.load("data/sounds/menu_sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, BLACK, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 2)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_text(text, x, y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main_menu(game_state):
    while True:
        screen.fill(BLACK)
        # Если пользователь залогинен, показываем его имя вместо кнопки "Войти"
        if game_state.username is None:
            login_button = draw_button("Войти", 640, 20, 150, 75)
        else:
            login_button = draw_button(game_state.username, 640, 20, 150, 75)
        draw_text("Retro-Racer", WIDTH // 2, 185, game_name_font, WHITE)
        play_button = draw_button("Играть", 175, 300, 450, 75)
        garage_button = draw_button("Гараж", 175, 425, 450, 75)
        settings_button = draw_button("Настройки", 175, 550, 450, 75)
        leaders_button = draw_button("Таблица лидеров", 175, 675, 450, 75)
        draw_text(f"Деньги: {game_state.money}$", 150, 25, button_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Обработка выхода по ESC
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
                    if garage_button.collidepoint(event.pos):
                        return 'garage'
        pygame.display.flip()

class GameState:
    def __init__(self):
        self.money = 0  # Деньги для заезда начинаются с 0
        self.user_id = None
        self.username = None
        self.selected_car = None

if __name__ == "__main__":
    game_state = GameState()
    settings = Settings()

    while True:
        action = main_menu(game_state)
        if action == "play":
            pygame.mixer.music.stop()
            # Перед каждым заездом обнуляем деньги
            game_state.money = 0
            game = Game(game_state, settings)
            game.game_loop()
            pygame.mixer.music.play(-1)
        elif action == 'login':
            # Окно выбора: "Войти" или "Зарегистрироваться"
            log_or_reg = Login()
            res = log_or_reg.main_loop()
            if res == 'register':
                reg_window = Registration()
                user = reg_window.main_loop()
                if user:
                    game_state.user_id = user[0]
                    game_state.username = user[1]
            elif res == 'log_in':
                login_window = Log_In()
                user = login_window.main_loop()
                if user:
                    game_state.user_id = user[0]
                    game_state.username = user[1]
        elif action == 'garage':
            if game_state.user_id is None:
                print("Пожалуйста, войдите, чтобы воспользоваться гаражом!")
            else:
                garage = Garage(game_state)
                garage.run()
        elif action == 'settings':
            settings.run()
        elif action == 'leaders':
            leads = Leaderboard()
            leads.run()
