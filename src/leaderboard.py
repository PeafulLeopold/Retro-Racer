import pygame
import sqlite3
import os

class Leaderboard:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.colors = {
            "background": (20, 20, 20),
            "primary": (255, 255, 255),
            "secondary": (40, 40, 40),
            "accent": (180, 180, 180)
        }
        self.running = True

    def get_leaderboard(self):
        db_path = os.path.join('db', 'project_database.db')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT username, high_score FROM Users ORDER BY high_score DESC, username ASC LIMIT 10')
        leaderboard = cursor.fetchall()
        conn.close()
        return leaderboard

    def draw_text(self, text, x, y, color, size=24, center=False):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        if center:
            x = x - text_surface.get_width() // 2
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        self.screen.fill(self.colors["background"])
        title = "Таблица лидеров"
        self.draw_text(title, self.width // 2, 30, self.colors["primary"], 48, center=True)

        leaderboard = self.get_leaderboard()
        y = 150
        for i, (username, score) in enumerate(leaderboard):
            entry_text = f"{i + 1}. {username}: {score}"
            self.draw_text(entry_text, 50, y, self.colors["primary"], 36)
            y += 50

        self.draw_text("Нажмите Esc для выхода", 50, self.height - 60, self.colors["accent"], 22)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False

            self.draw()
            pygame.display.flip()
            clock.tick(60)
