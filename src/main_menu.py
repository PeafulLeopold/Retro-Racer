import pygame
import sys
from colors import BLACK, WHITE
from game import Game
from log_in import Log_In  # Используем окно входа для авторизации
from register import Registration
from garage import Garage
from settings import Settings
from leaderboard import Leaderboard
from login import Login  # Окно выбора: регистрация/вход

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

game_name_font = pygame.font.Font(None, 120)
button_font = pygame.font.Font(None, 48)

pygame.mixer.music.load("data/sounds/menu_sound.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Загружаем аватарку
avatar_icon = pygame.image.load("data/images/account.png").convert_alpha()
avatar_icon = pygame.transform.scale(avatar_icon, (60, 60))
avatar_rect = avatar_icon.get_rect()
avatar_rect.topright = (WIDTH - 20, 20)

def draw_button(text, center_x, center_y, width, height):
    button_rect = pygame.Rect(0, 0, width, height)
    button_rect.center = (center_x, center_y)
    pygame.draw.rect(screen, BLACK, button_rect)
    pygame.draw.rect(screen, WHITE, button_rect, 2)
    text_surface = button_font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def draw_text(text, center_x, center_y, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(center_x, center_y))
    screen.blit(text_surface, text_rect)

def show_user_info(game_state):
    # Отрисовка модального окна с информацией о пользователе
    info_rect = pygame.Rect(0, 0, 400, 300)
    info_rect.center = (WIDTH // 2, HEIGHT // 2)
    info_font = pygame.font.Font(None, 36)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        # Рисуем полупрозрачный оверлей
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        # Рисуем окно с черным фоном и зеленой обводкой
        pygame.draw.rect(screen, BLACK, info_rect)
        pygame.draw.rect(screen, (0, 255, 0), info_rect, 4)
        # Выводим информацию о пользователе белым текстом
        username_text = info_font.render("Имя: " + game_state.username, True, WHITE)
        balance_text = info_font.render("Баланс: " + str(game_state.money) + "$", True, WHITE)
        screen.blit(username_text, (info_rect.x + 20, info_rect.y + 40))
        screen.blit(balance_text, (info_rect.x + 20, info_rect.y + 100))
        prompt_text = info_font.render("Нажмите ESC для выхода", True, WHITE)
        prompt_rect = prompt_text.get_rect(center=(info_rect.centerx, info_rect.bottom - 30))
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()
        pygame.time.delay(30)

def main_menu(game_state):
    while True:
        screen.fill(BLACK)
        # Если пользователь не залогинен – отображается кнопка "Войти"
        if game_state.username is None:
            login_button = draw_button("Войти", WIDTH - 80, 40, 120, 50)
        else:
            # Если залогинен – отображается аватарка
            screen.blit(avatar_icon, avatar_rect)
        draw_text("Retro-Racer", WIDTH // 2, 140, game_name_font, WHITE)
        play_button = draw_button("Играть", WIDTH // 2, 300, 300, 60)
        garage_button = draw_button("Гараж", WIDTH // 2, 380, 300, 60)
        settings_button = draw_button("Настройки", WIDTH // 2, 460, 300, 60)
        leaders_button = draw_button("Таблица лидеров", WIDTH // 2, 540, 300, 60)
        # Вывод баланса только для авторизованных пользователей
        if game_state.user_id is not None:
            draw_text(f"Баланс: {game_state.money}$", 150, 50, button_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    return "play"
                if settings_button.collidepoint(mouse_pos):
                    return "settings"
                if leaders_button.collidepoint(mouse_pos):
                    return "leaders"
                if garage_button.collidepoint(mouse_pos):
                    return "garage"
                if game_state.username is None:
                    # Если не залогинен, проверяем кнопку "Войти"
                    if draw_button("Войти", WIDTH - 80, 40, 120, 50).collidepoint(mouse_pos):
                        return "login"
                else:
                    # Если залогинен, проверяем нажатие по аватарке
                    if avatar_rect.collidepoint(mouse_pos):
                        show_user_info(game_state)
        pygame.display.flip()

class GameState:
    def __init__(self):
        self.money = 100  # Начальное количество денег для теста
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
            game = Game(game_state, settings)
            game.game_loop()
            pygame.mixer.music.play(-1)
        elif action == "login":
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
        elif action == "garage":
            if game_state.user_id is None:
                print("Пожалуйста, войдите, чтобы воспользоваться гаражом!")
            else:
                garage = Garage(game_state)
                garage.run()
        elif action == "settings":
            settings.run()
        elif action == "leaders":
            leads = Leaderboard()
            leads.run()
