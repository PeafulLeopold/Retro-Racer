import pygame

from colors import WHITE
from road import Road
from car import Car


speed = 1

WIDTH, HEIGHT = 1100, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

car_path = "data/images/car.jpg"
road_path = "data/images/road.png"

road_img = pygame.image.load(road_path)
car_img = pygame.image.load(car_path)

pygame.display.set_caption("Retro Racer")
clock = pygame.time.Clock()

def game_loop():
    running = True
    car = Car(WIDTH // 2, HEIGHT // 2, car_img, speed)
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
