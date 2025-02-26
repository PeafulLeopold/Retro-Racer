import pygame


class Settings:
    def __init__(self):
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

    def draw_text(self, text, x, y, color, size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw(self):
        self.screen.fill(self.colors["background"])
        self.draw_text("Настройки", self.width // 2 - 50, 30, self.colors["primary"], 48)
        self.draw_text("Громкость музыки", 50, 150, self.colors["primary"], 36)
        self.draw_text("Громкость звуков", 50, 250, self.colors["primary"], 36)
        self.draw_text("Управление", 50, 350, self.colors["primary"], 36)
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