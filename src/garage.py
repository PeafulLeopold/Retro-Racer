import pygame
import sqlite3
from colors import WHITE

class Garage:
    def __init__(self, user_id):
        self.user_id = user_id
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.selected_car = 0
        self.car_offset = 0
        self.cars = self.load_cars()
        self.running = True

    def load_cars(self):
        conn = sqlite3.connect('db/project_database.db')
        cursor = conn.cursor()
        
        # Загрузка всех автомобилей
        cursor.execute('SELECT * FROM Cars')
        all_cars = cursor.fetchall()
        
        # Загрузка купленных автомобилей
        cursor.execute('''
            SELECT Cars.* FROM Cars
            JOIN OwnedCars ON Cars.id = OwnedCars.car_id
            WHERE OwnedCars.user_id = ?
        ''', (self.user_id,))
        owned_cars = cursor.fetchall()
        
        conn.close()
        
        # Форматирование данных
        return [{
            'id': car[0],
            'name': car[1],
            'speed': car[2],
            'accel': car[3],
            'price': f"${car[4]}K",
            'image': pygame.image.load(car[5])
        } for car in owned_cars]

    def draw_car_selection(self):
        start_x, start_y = 50, 150
        spacing = 220
        
        for i, car in enumerate(self.cars[self.car_offset:self.car_offset+3]):
            x = start_x + i * spacing
            pygame.draw.rect(self.screen, WHITE, (x-10, start_y-10, 220, 220), 2)
            img = pygame.transform.scale(car['image'], (200, 200))
            self.screen.blit(img, (x, start_y))
            self.draw_text(car['name'], x + 20, start_y + 210, WHITE)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.screen.fill((0, 0, 0))
            self.draw_text("Ваш гараж", 300, 30, WHITE)
            self.draw_car_selection()
            pygame.display.flip()
            clock.tick(60)