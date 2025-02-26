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

        # Громкость музыки и звуков (от 0.0 до 1.0)
        self.music_volume = 0.5  # По умолчанию 50%

        # Позиции ползунков
        self.music_slider_x = 400  # Начальная позиция ползунка музыки
        self.slider_y = 200        # Y-позиция ползунков
        self.slider_width = 200    # Ширина ползунка
        self.slider_height = 10    # Высота ползунка
        self.handle_radius = 10    # Радиус ручки ползунка

        # Схема управления (по умолчанию стрелочки)
        self.control_scheme = "arrows"  # "arrows" или "wasd"

    def draw_text(self, text, x, y, color, size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_slider(self, x, y, width, height, handle_x, color):
        # Отрисовка полосы ползунка
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        # Отрисовка ручки ползунка
        pygame.draw.circle(self.screen, color, (handle_x, y + height // 2), self.handle_radius)

    def draw(self):
        self.screen.fill(self.colors["background"])
        self.draw_text("Настройки", self.width // 2 - 50, 30, self.colors["primary"], 48)
        
        # Громкость музыки
        self.draw_text("Громкость музыки", 50, 150, self.colors["primary"], 36)
        self.draw_slider(300, 170, self.slider_width, self.slider_height, self.music_slider_x, self.colors["accent"])
        self.draw_text(f"{int(self.music_volume * 100)}%", 520, 150, self.colors["primary"], 36)
        
        # Управление
        self.draw_text("Управление", 50, 350, self.colors["primary"], 36)
        control_text = "Стрелочки" if self.control_scheme == "arrows" else "WASD"
        self.draw_text(f"Текущее управление: {control_text}", 50, 400, self.colors["primary"], 36)
        self.draw_text("Нажмите C для смены управления", 50, 450, self.colors["accent"], 24)
        self.draw_text("Нажмите Esc для выхода", 50, self.height - 60, self.colors["accent"], 22)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_c:  # Переключение схемы управления
                    self.control_scheme = "wasd" if self.control_scheme == "arrows" else "arrows"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.handle_slider_click(event.pos)

    def handle_slider_click(self, mouse_pos):
        x, y = mouse_pos
        # Проверка клика на ползунке музыки
        if 170 <= y <= 170 + self.slider_height:
            if 300 <= x <= 300 + self.slider_width:
                self.music_slider_x = x
                self.music_volume = (x - 300) / self.slider_width
                # Применение громкости музыки
                pygame.mixer.music.set_volume(self.music_volume)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()  # Обработка событий
            self.draw()          # Отрисовка
            pygame.display.flip()
            clock.tick(60)