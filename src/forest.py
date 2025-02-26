import pygame

class Forest:
    def __init__(self, screen_height, forest_img, speed):
        self.WIDTH, self.HEIGHT = 1100, 800
        self.forest_image = pygame.transform.scale(forest_img, (self.WIDTH, self.HEIGHT))
        self.y_pos = 0
        self.speed = speed
        self.screen_height = screen_height

    def update(self):
        self.y_pos += self.speed
        if self.y_pos >= self.screen_height:
            self.y_pos = 0

    def draw(self, screen):
        screen.blit(self.forest_image, (0, self.y_pos - self.screen_height))
        screen.blit(self.forest_image, (0, self.y_pos))