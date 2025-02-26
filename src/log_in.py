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

        # Цвета и шрифты
        self.COLORS = {
            "background": BLACK,
            "text": WHITE,
            "active": GREEN,
            "error": RED,
            "inactive": (150, 150, 150)
        }
        self.title_font = pygame.font.Font(None, 80)
        self.main_font = pygame.font.Font(None, 60)
        self.error_font = pygame.font.Font(None, 40)

        # Поля ввода
        self.username_rect = pygame.Rect(170, 200, 500, 70)
        self.password_rect = pygame.Rect(170, 400, 500, 70)
        self.username = ""
        self.password = ""
        self.username_active = False
        self.password_active = False
        self.error_message = ""
        self.running = True

    def draw_input_field(self, rect, text, active):
        color = self.COLORS["active"] if active else self.COLORS["inactive"]
        pygame.draw.rect(self.screen, color, rect, 2)
        text_surface = self.main_font.render(text, True, self.COLORS["text"])
        self.screen.blit(text_surface, (rect.x + 10, rect.y + 15))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.handle_keypress(event)

    def handle_click(self, pos):
        self.username_active = self.username_rect.collidepoint(pos)
        self.password_active = self.password_rect.collidepoint(pos)

    def handle_keypress(self, event):
        if self.username_active:
            if event.key == pygame.K_RETURN:
                self.username = ""
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

    def attempt_login(self):
        conn = sqlite3.connect('db/project_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM Users WHERE username = ?', (self.username,))
        user = cursor.fetchone()
        
        if not user:
            self.error_message = "Пользователь не найден!"
        elif user[2] != self.password:
            self.error_message = "Неверный пароль!"
        else:
            self.running = False
            return (user[0], user[1])  # Возвращаем (user_id, username)
        conn.close()
        return None

    def draw(self):
        self.screen.fill(self.COLORS["background"])
        # Заголовок
        title_surf = self.title_font.render("Вход", True, self.COLORS["text"])
        self.screen.blit(title_surf, (self.WIDTH//2 - title_surf.get_width()//2, 50))
        # Поля ввода
        self.draw_input_field(self.username_rect, self.username or "Имя пользователя", self.username_active)
        self.draw_input_field(self.password_rect, "*"*len(self.password) or "Пароль", self.password_active)
        # Ошибки
        if self.error_message:
            error_surf = self.error_font.render(self.error_message, True, RED)
            self.screen.blit(error_surf, (self.WIDTH//2 - error_surf.get_width()//2, 550))
        pygame.display.flip()

    def main_loop(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.draw()
            clock.tick(60)
        return self.attempt_login()