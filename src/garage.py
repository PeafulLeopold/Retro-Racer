import pygame
import sys
from colors import BLACK, WHITE

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Shop")


class Product:
    def __init__(self, name, price, image_path):
        self.name = name
        self.price = price
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, (210, 200))
        self.is_purchased = False


class Shop:
    def __init__(self):
        self.cars = [
            Product("Car1", 100, "data/images/car1.png"),  
            Product("Car2", 200, "data/images/car2.jpeg"),
            Product("Car3", 300, "data/images/car3.jpeg"),
        ]
        self.money = 250  

    def draw_shop(self):
        y = 50
        font = pygame.font.SysFont(None, 36)
        for car in self.cars:
            text = f"{car.name} - {car.price} { 'Куплено' if car.is_purchased else 'Купить' }"
            img = font.render(text, True, WHITE)
            screen.blit(img, (50, y))
            if not car.is_purchased:
                screen.blit(car.image, (400, y - 50))
            y += 200

    def buy_car(self, car_index):
        car = self.cars[car_index]
        if not car.is_purchased and self.money >= car.price:
            self.money -= car.price
            car.is_purchased = True

    def draw_money(self):
        font = pygame.font.SysFont(None, 36)
        money_text = f"Деньги: {self.money}"
        img = font.render(money_text, True, WHITE)
        screen.blit(img, (600, 20))

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.buy_car(0)
                    elif event.key == pygame.K_2:
                        self.buy_car(1)
                    elif event.key == pygame.K_3:
                        self.buy_car(2)

            screen.fill(BLACK)
            self.draw_shop()
            self.draw_money()
            pygame.display.flip()