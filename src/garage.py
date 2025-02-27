import pygame
import os
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

        self.selected_index = 0  # Индекс выбранного автомобиля
        self.cars = self.load_cars()
        self.running = True

    def load_cars(self):
        """
        Загружает список всех автомобилей и отмечает, какие из них уже куплены пользователем.
        Если файл изображения отсутствует, подставляется дефолтное изображение.
        """
        all_cars = get_cars()
        owned_ids = [car[0] for car in get_owned_cars(self.user_id)]
        
        default_image_path = "data/images/car.png"  # Путь к дефолтному изображению
        if not os.path.exists(default_image_path):
            raise FileNotFoundError(f"Файл дефолтного изображения {default_image_path} не найден!")

        cars = []
        for car in all_cars:
            image_path = car[5] if os.path.exists(car[5]) else default_image_path  # Проверяем наличие изображения
            
            car_dict = {
                'id': car[0],
                'name': car[1],
                'speed': car[2],
                'accel': car[3],
                'price': car[4],
                'image_path': image_path,
                'image': pygame.image.load(image_path).convert_alpha(),
                'owned': car[0] in owned_ids
            }
            cars.append(car_dict)
        
        return cars

    def draw_text(self, text, x, y, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_garage(self):
        self.screen.fill(BLACK)
        # Заголовок
        title_surface = self.title_font.render("Гараж", True, WHITE)
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 20))

        # Если список автомобилей пуст, выводим сообщение
        if not self.cars:
            self.draw_text("Нет автомобилей для отображения", self.width // 2 - 200, self.height // 2, WHITE)
            return

        # Если выбранный индекс выходит за пределы, сбрасываем его
        if self.selected_index >= len(self.cars):
            self.selected_index = 0

        selected_car = self.cars[self.selected_index]

        # Левая панель (информация о машине)
        panel_width = 300
        panel_height = 600
        panel_x = 50
        panel_y = 100
        pygame.draw.rect(self.screen, WHITE, (panel_x, panel_y, panel_width, panel_height), 2)

        info_lines = [
            f"Название: {selected_car['name']}",
            f"Скорость: {selected_car['speed']}",
            f"Ускорение: {selected_car['accel']}",
        ]
        if selected_car['owned']:
            info_lines.append("Статус: Куплено")
        else:
            info_lines.append(f"Цена: ${selected_car['price']}K")
            if self.game_state.money >= selected_car['price']:
                info_lines.append("Опция: Приобрести (ENTER)")
            else:
                info_lines.append("Недостаточно средств")

        for i, line in enumerate(info_lines):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (panel_x + 20, panel_y + 20 + i * 40))

        # Правая панель (изображение автомобиля)
        image_panel_x = panel_x + panel_width + 50
        image_panel_y = panel_y
        image_panel_width = self.width - image_panel_x - 50
        image_panel_height = panel_height
        pygame.draw.rect(self.screen, WHITE, (image_panel_x, image_panel_y, image_panel_width, image_panel_height), 2)

        # Масштабирование изображения с сохранением пропорций
        car_image = selected_car['image']
        img_rect = car_image.get_rect()
        scale_factor = min(image_panel_width / img_rect.width, image_panel_height / img_rect.height)
        new_width = int(img_rect.width * scale_factor)
        new_height = int(img_rect.height * scale_factor)
        scaled_image = pygame.transform.scale(car_image, (new_width, new_height))
        img_x = image_panel_x + (image_panel_width - new_width) // 2
        img_y = image_panel_y + (image_panel_height - new_height) // 2
        self.screen.blit(scaled_image, (img_x, img_y))

        # Инструкции по навигации
        nav_text = "← Предыдущая  |  → Следующая  |  ESC Выйти"
        nav_surface = self.font.render(nav_text, True, WHITE)
        self.screen.blit(nav_surface, (self.width // 2 - nav_surface.get_width() // 2, self.height - 50))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    if self.selected_index > 0:
                        self.selected_index -= 1
                if event.key == pygame.K_RIGHT:
                    if self.selected_index < len(self.cars) - 1:
                        self.selected_index += 1
                if event.key == pygame.K_RETURN:
                    selected_car = self.cars[self.selected_index]
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
        buy_car(self.user_id, car['id'])
        new_balance = self.game_state.money - car['price']
        update_balance(self.user_id, new_balance)
        self.game_state.money = new_balance
        car['owned'] = True
        print(f"Куплена машина: {car['name']} за {car['price']}K")

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.draw_garage()
            self.handle_events()
            pygame.display.flip()
            clock.tick(60)
