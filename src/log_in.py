import pygame
import sys
import sqlite3
from colors import BLACK, WHITE, GREEN, RED

class Log_In:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Вход")

        # Цвета и шрифты, аналогичные register.py
        self.BLACK = BLACK
        self.WHITE = WHITE
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (150, 150, 150)
        self.ACT_COLOR = (0, 255, 0)
        self.ERROR_COLOR = RED

        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)

        # Поля ввода: имя пользователя и пароль
        self.username_rect = pygame.Rect(170, 200, 500, 70)
        self.password_rect = pygame.Rect(170, 350, 500, 70)

        self.username = ''
        self.password = ''

        self.username_active = False
        self.password_active = False

        self.error_message = ""
        self.running = True

        # Для мигания курсора, как в register.py
        self.username_cursor_visible = True
        self.username_cursor = 0

        self.password_cursor_visible = True
        self.password_cursor = 0

        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.username_rect.collidepoint(event.pos):
                    self.username_active = True
                    self.password_active = False
                elif self.password_rect.collidepoint(event.pos):
                    self.username_active = False
                    self.password_active = True
                else:
                    self.username_active = False
                    self.password_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.username_active:
                    if event.key == pygame.K_RETURN:
                        self.username_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        if len(self.username) < 20:
                            self.username += event.unicode
                elif self.password_active:
                    if event.key == pygame.K_RETURN:
                        self.attempt_login()
                    elif event.key == pygame.K_BACKSPACE:
                        self.password = self.password[:-1]
                    else:
                        if len(self.password) < 20:
                            self.password += event.unicode

    def update_cursors(self):
        elapsed = self.clock.get_rawtime()
        self.username_cursor += elapsed
        self.password_cursor += elapsed

        if self.username_cursor > 500:
            self.username_cursor_visible = not self.username_cursor_visible
            self.username_cursor = 0
        if self.password_cursor > 500:
            self.password_cursor_visible = not self.password_cursor_visible
            self.password_cursor = 0

    def draw(self):
        self.screen.fill(self.BLACK)
        # Заголовок
        title_surface = self.title_font.render("Вход", True, self.WHITE)
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Поле ввода имени пользователя
        username_color = self.ACT_COLOR if self.username_active else self.GRAY
        pygame.draw.rect(self.screen, username_color, self.username_rect, 2)
        username_display = self.username if self.username or self.username_active else "Имя пользователя"
        username_text_color = self.WHITE if self.username or self.username_active else self.LIGHT_GRAY
        username_surface = self.font.render(username_display, True, username_text_color)
        self.screen.blit(username_surface, (self.username_rect.x + 10, self.username_rect.y + 15))
        if self.username_active and self.username_cursor_visible:
            cursor_x = self.username_rect.x + 10 + username_surface.get_width()
            cursor_rect = pygame.Rect(cursor_x, self.username_rect.y + 15, 2, self.username_rect.height - 30)
            pygame.draw.rect(self.screen, self.WHITE, cursor_rect)

        # Поле ввода пароля
        password_color = self.ACT_COLOR if self.password_active else self.GRAY
        pygame.draw.rect(self.screen, password_color, self.password_rect, 2)
        password_display = "*" * len(self.password) if self.password or self.password_active else "Пароль"
        password_text_color = self.WHITE if self.password or self.password_active else self.LIGHT_GRAY
        password_surface = self.font.render(password_display, True, password_text_color)
        self.screen.blit(password_surface, (self.password_rect.x + 10, self.password_rect.y + 15))
        if self.password_active and self.password_cursor_visible:
            cursor_x = self.password_rect.x + 10 + password_surface.get_width()
            cursor_rect = pygame.Rect(cursor_x, self.password_rect.y + 15, 2, self.password_rect.height - 30)
            pygame.draw.rect(self.screen, self.WHITE, cursor_rect)

        # Вывод сообщения об ошибке, если оно есть
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, self.ERROR_COLOR)
            error_rect = error_surface.get_rect(center=(self.WIDTH // 2, 450))
            self.screen.blit(error_surface, error_rect)

        pygame.display.flip()

    def attempt_login(self):
        conn = sqlite3.connect('db/project_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM Users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        conn.close()

        if not user:
            self.error_message = "Пользователь не найден!"
        elif user[2] != self.password:
            self.error_message = "Неверный пароль!"
        else:
            self.running = False
            return user
        return None

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update_cursors()
            self.draw()
            self.clock.tick(60)
        return self.attempt_login()

