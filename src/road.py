import pygame

class Road:
    def __init__(self, screen_height, screen_width, road_img, speed):
        self.road_image = pygame.transform.scale(road_img, (600, 800))
        self.speed = speed
        self.x = (screen_width - 600) // 2
        self.rect = pygame.Rect(self.x + 50, 50, 600 - 100, screen_height - 100)

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.road_image, (self.x, 0))