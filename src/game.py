import pygame
from colors import WHITE
from road import Road
from car import Car
from hole import Hole
from forest import Forest

class Game:
    def __init__(self):
        self.speed = 1
        self.WIDTH, self.HEIGHT = 1100, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        hole_path = "data/images/hole.png"
        car_path = "data/images/car.png"
        forest_path = "data/images/forest.jpg"
        road_path = "data/images/road.png"

        self.road_img = pygame.image.load(road_path).convert_alpha()
        self.hole_img = pygame.image.load(hole_path)
        self.car_img = pygame.image.load(car_path)
        self.forest_img = pygame.image.load(forest_path)


        pygame.display.set_caption("Retro Racer")
        self.clock = pygame.time.Clock()

    def game_loop(self):
        running = True
        car = Car(self.WIDTH // 2, self.HEIGHT // 2 + 150, self.car_img, self.speed)
        road = Road(self.HEIGHT, self.WIDTH, self.road_img, self.speed)
        hole = Hole(self.HEIGHT, self.hole_img, self.speed)
        forest = Forest(self.HEIGHT, self.forest_img, self.speed)

        while running:
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            car.update(keys)
            forest.draw(self.screen)
            road.draw(self.screen)
            hole.draw(self.screen)
            car.draw(self.screen)
            road.update()
            hole.update()
            forest.update()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        quit()

