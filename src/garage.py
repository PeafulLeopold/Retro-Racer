import pygame

class Garage:
    def __init__(self):
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.selected_car = 0
        self.car_offset = 0
        
        self.cars = [
            {"name": "CyberTruck", "image": "data/images/cybertruck.png", "speed": 280, "accel": 4.5, "price": "$120k"},
            {"name": "Porshe 911 Brabus", "image": "data/images/porshe.png", "speed": 320, "accel": 3.8, "price": "$150k"},
            {"name": "Mercedes AMG", "image": "data/images/amg.png", "speed": 300, "accel": 4.2, "price": "$135k"},
            {"name": "Ferrari SF90", "image": "data/images/ferrari.png", "speed": 290, "accel": 4.7, "price": "$110k"},
            {"name": "McLaren 765", "image": "data/images/mclaren.png", "speed": 310, "accel": 3.9, "price": "$160k"},
            {"name": "Bugatti Chiron", "image": "data/images/bugatti.png", "speed": 330, "accel": 3.5, "price": "$180k"},
        ]
        
        for car in self.cars:
            try:
                car["image"] = pygame.image.load(car["image"])
            except:
                car["image"] = pygame.Surface((200, 100))  # Заглушка если изображение не найдено
        
        self.colors = {
            "background": (20, 20, 20),
            "primary": (255, 255, 255),
            "secondary": (40, 40, 40),
            "accent": (180, 180, 180)
        }

        self.running = True

        # Баланс игрока
        self.balance = 0  # Пример начального баланса

    def draw_rounded_rect(self, surface, color, rect, radius=20):
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        
    def draw_stats_panel(self, x, y):
        panel_width = 300
        panel_height = 200
        self.draw_rounded_rect(self.screen, self.colors["secondary"], (x, y, panel_width, panel_height))
        
        car = self.cars[self.selected_car]
        stats_y = y + 20
        self.draw_text(f"Название: {car['name']}", x + 20, stats_y, self.colors["primary"], 24)
        self.draw_text(f"Скорость: {car['speed']} km/h", x + 20, stats_y + 40, self.colors["accent"])
        self.draw_text(f"Разгон до 100: {car['accel']}s", x + 20, stats_y + 70, self.colors["accent"])
        self.draw_text(f"Цена: {car['price']}", x + 20, stats_y + 100, self.colors["primary"], 24)

    def draw_text(self, text, x, y, color, size=24):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
        
    def draw_car_selection(self):
        """Отрисовывает галерею автомобилей"""
        start_x = 50
        start_y = 150
        spacing = 220
        
        for i, car in enumerate(self.cars[self.car_offset:self.car_offset+3]):
            x = start_x + i * spacing
            y = start_y
            
            border_color = self.colors["primary"] if i + self.car_offset == self.selected_car else self.colors["secondary"]
            pygame.draw.rect(self.screen, border_color, (x-10, y-10, 220, 220), 2, border_radius=15)
            
            img = pygame.transform.scale(car["image"], (200, 200))
            self.screen.blit(img, (x, y))
            
            self.draw_text(car["name"], x + 20, y + 210, self.colors["primary"], 22)

    def draw_balance(self):
        balance_text = f"Баланс: ${self.balance:,}"
        text_width, text_height = self.font.size(balance_text)
        x = self.width - text_width - 20  
        y = 30  
        
        self.draw_rounded_rect(self.screen, self.colors["secondary"], (x - 10, y - 10, text_width + 20, text_height + 20))
        self.draw_text(balance_text, x, y, self.colors["primary"], 36)

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.selected_car < len(self.cars) - 1:
                self.selected_car += 1
                if self.selected_car - self.car_offset >= 3:
                    self.car_offset += 1
            elif event.key == pygame.K_LEFT and self.selected_car > 0:
                self.selected_car -= 1
                if self.selected_car < self.car_offset:
                    self.car_offset -= 1
            elif event.key == pygame.K_ESCAPE:
                self.running = False

    def draw(self):
        """Основной метод отрисовки гаража"""
        self.screen.fill(self.colors["background"])
        
        # Заголовок
        self.draw_text("Гараж", self.width // 2 - 50, 30, self.colors["primary"], 48)
        
        # Баланс
        self.draw_balance()
        
        # Галерея автомобилей
        self.draw_car_selection()
        
        # Панель характеристик
        self.draw_stats_panel(self.width // 2 - 150, 450)
        
        # Инструкции
        self.draw_text("Используйте стрелки клавиатуры для навигации", 50, self.height - 60, self.colors["accent"], 22)
        self.draw_text("Нажмите Esc для выхода", self.width - 300, self.height - 60, self.colors["accent"], 22)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_input(event)
            
            self.draw()
            pygame.display.flip()
            clock.tick(60)