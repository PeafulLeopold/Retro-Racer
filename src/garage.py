import pygame
import sqlite3
from colors import WHITE, BLACK, GREEN, RED
from database import get_cars, get_owned_cars, buy_car, update_balance

class Garage:
    def __init__(self, game_state):
        pygame.init()
        self.game_state = game_state
        self.user_id = game_state.user_id
        self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Гараж")

        self.font = pygame.font.Font(None, 36)
        self.title_font = pygame.font.Font(None, 60)

        self.selected_index = 0  # Индекс выделенного автомобиля
        self.car_offset = 0  # Смещение для прокрутки списка автомобилей
        self.cars = self.load_cars()
        self.running = True

    def load_cars(self):
        """
        Загружает список всех автомобилей и отмечает, какие из них уже куплены пользователем.
        """
        all_cars = get_cars()
        owned_ids = [car[0] for car in get_owned_cars(self.user_id)]

        cars = []
        for car in all_cars:
            car_dict = {
                'id': car[0],
                'name': car[1],
                'speed': car[2],
                'accel': car[3],
                'price': car[4],
                'image_path': car[5],
                'image': pygame.image.load(car[5]).convert_alpha(),
                'owned': car[0] in owned_ids
            }
            cars.append(car_dict)
        return cars

    def draw_car_selection(self):
        """
        Отрисовывает список автомобилей (3 на экране одновременно).
        """
        start_x, start_y = 50, 150
        spacing = 220

        visible_cars = self.cars[self.car_offset:self.car_offset + 3]
        for i, car in enumerate(visible_cars):
            x = start_x + i * spacing
            pygame.draw.rect(self.screen, WHITE, (x - 10, start_y - 10, 220, 220), 2)
            img = pygame.transform.scale(car['image'], (200, 200))
            self.screen.blit(img, (x, start_y))

            # Название машины
            self.draw_text(car['name'], x + 20, start_y + 210, WHITE)

            # Если машина куплена, показываем статус "OWNED", иначе цену
            if car['owned']:
                self.draw_text("OWNED", x + 20, start_y + 240, GREEN)
            else:
                self.draw_text(f"${car['price']}K", x + 20, start_y + 240, RED)

            # Выделение выбранной машины
            if self.selected_index == i:
                pygame.draw.rect(self.screen, GREEN, (x - 10, start_y - 10, 220, 220), 4)

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def handle_events(self):
        """
        Обрабатывает ввод пользователя: прокрутка, покупка и выбор машины.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                    elif self.car_offset > 0:
                        self.car_offset -= 1
                if event.key == pygame.K_RIGHT:
                    visible_count = len(self.cars[self.car_offset:self.car_offset + 3])
                    if self.selected_index < visible_count - 1:
                        self.selected_index += 1
                    elif self.car_offset + 3 < len(self.cars):
                        self.car_offset += 1
                if event.key == pygame.K_RETURN:
                    index = self.car_offset + self.selected_index
                    selected_car = self.cars[index]

                    if not selected_car['owned']:
                        if self.game_state.money >= selected_car['price']:
                            self.buy_car(selected_car)
                        else:
                            print("Недостаточно денег для покупки!")
                    else:
                        self.game_state.selected_car = selected_car
                        print(f"Выбрана машина: {selected_car['name']}")
                        self.running = False

    def buy_car(self, car):
        """
        Покупает машину и обновляет баланс пользователя.
        """
        buy_car(self.user_id, car['id'])
        new_balance = self.game_state.money - car['price']
        update_balance(self.user_id, new_balance)

        # Обновляем состояние игры и UI
        self.game_state.money = new_balance
        car['owned'] = True
        print(f"Куплена машина: {car['name']} за {car['price']}K")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.screen.fill(BLACK)
            self.draw_text("Гараж", 320, 30, WHITE)
            self.draw_car_selection()
            self.handle_events()
            pygame.display.flip()
            clock.tick(60)
