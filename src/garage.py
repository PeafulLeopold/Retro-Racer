import pygame
import sqlite3
from colors import WHITE, BLACK, GREEN

class Garage:
    def __init__(self, game_state):
        self.game_state = game_state
        self.user_id = game_state.user_id
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 36)
        self.selected_index = 0
        self.car_offset = 0
        self.cars = self.load_cars()
        self.running = True

    def load_cars(self):
        conn = sqlite3.connect('db/project_database.db')
        cursor = conn.cursor()
        # Загружаем все автомобили
        cursor.execute('SELECT * FROM Cars')
        all_cars = cursor.fetchall()
        # Получаем список id купленных авто для пользователя (если он залогинен)
        owned_ids = []
        if self.user_id is not None:
            cursor.execute('SELECT car_id FROM OwnedCars WHERE user_id = ?', (self.user_id,))
            owned_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        cars = []
        for car in all_cars:
            car_dict = {
                'id': car[0],
                'name': car[1],
                'speed': car[2],
                'accel': car[3],
                'price': car[4],
                'price_str': f"${car[4]}K",
                'image_path': car[5],
                'image': pygame.image.load(car[5]),
                'owned': car[0] in owned_ids
            }
            cars.append(car_dict)
        return cars

    def draw_car_selection(self):
        start_x, start_y = 50, 150
        spacing = 220
        
        visible_cars = self.cars[self.car_offset:self.car_offset+3]
        for i, car in enumerate(visible_cars):
            x = start_x + i * spacing
            # Рисуем рамку для каждого авто
            pygame.draw.rect(self.screen, WHITE, (x-10, start_y-10, 220, 220), 2)
            img = pygame.transform.scale(car['image'], (200, 200))
            self.screen.blit(img, (x, start_y))
            # Выводим название автомобиля
            self.draw_text(car['name'], x + 20, start_y + 210, WHITE)
            # Если автомобиль куплен, выводим метку, иначе – кнопку покупки с ценой
            if car['owned']:
                self.draw_text("OWNED", x + 20, start_y + 240, GREEN)
            else:
                self.draw_text(f"Buy {car['price_str']}", x + 20, start_y + 240, GREEN)
            # Выделяем выбранный автомобиль
            if self.selected_index == i:
                pygame.draw.rect(self.screen, GREEN, (x-10, start_y-10, 220, 220), 4)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Переключение выделения
                if event.key == pygame.K_LEFT:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                    elif self.car_offset > 0:
                        self.car_offset -= 1
                if event.key == pygame.K_RIGHT:
                    visible_count = len(self.cars[self.car_offset:self.car_offset+3])
                    if self.selected_index < visible_count - 1:
                        self.selected_index += 1
                    elif self.car_offset + 3 < len(self.cars):
                        self.car_offset += 1
                # Выбор автомобиля по Enter
                if event.key == pygame.K_RETURN:
                    index = self.car_offset + self.selected_index
                    selected_car = self.cars[index]
                    if not selected_car['owned']:
                        # Если автомобиль не куплен – пытаемся купить
                        if self.game_state.money >= selected_car['price']:
                            self.buy_car(selected_car)
                        else:
                            print("Not enough money to buy this car!")
                    else:
                        # Если куплен – сохраняем как выбранный для игры
                        self.game_state.selected_car = selected_car
                        print(f"Selected car: {selected_car['name']}")
                        self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = event.pos
                    start_x, start_y = 50, 150
                    spacing = 220
                    for i, car in enumerate(self.cars[self.car_offset:self.car_offset+3]):
                        rect = pygame.Rect(start_x + i * spacing - 10, start_y - 10, 220, 220)
                        if rect.collidepoint(mouse_pos):
                            if not car['owned']:
                                if self.game_state.money >= car['price']:
                                    self.buy_car(car)
                                else:
                                    print("Not enough money!")
                            else:
                                self.game_state.selected_car = car
                                print(f"Selected car: {car['name']}")
                                self.running = False

    def buy_car(self, car):
        conn = sqlite3.connect('db/project_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO OwnedCars (user_id, car_id) VALUES (?, ?)', (self.user_id, car['id']))
        conn.commit()
        conn.close()
        self.game_state.money -= car['price']
        car['owned'] = True
        print(f"Bought car: {car['name']} for {car['price_str']}")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(BLACK)
            self.draw_text("Ваш гараж", 300, 30, WHITE)
            self.draw_car_selection()
            self.handle_events()
            pygame.display.flip()
            clock.tick(60)
