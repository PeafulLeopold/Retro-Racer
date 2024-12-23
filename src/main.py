import pygame

from colors import WHITE
from road import Road
from car import Car


WIDTH, HEIGHT = 1100, 800
speed = 7

car_path = 'data/images/car.jpg'

road_img = pygame.image.load("data/images/road.png")
car_img = pygame.image.load(car_path)

pygame.display.set_caption("Retro Racer")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def game_loop():
    running = True
    car = Car(WIDTH // 2, HEIGHT // 2, car_img, car_path, speed)
    road = Road(HEIGHT, WIDTH, road_img, speed)

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        car.update(keys)

        road.draw(screen)

        car.draw(screen)

        road.update()

        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()

game_loop()
