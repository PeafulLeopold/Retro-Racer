import pygame
class Forest:
    def __init__(self, screen_height, forest_img, speed):
        self.hole_image = pygame.transform.scale(forest_img, (150, 150))
        self.forest_image = forest_img
        self.screen_height = screen_height
        self.y_pos = 0
        self.scrolling_speed = speed
        self.forest_rect = self.forest_image.get_rect()
    
    def update(self):
        self.y_pos += self.scrolling_speed
        
        if self.y_pos >= self.screen_height:
            self.y_pos = 0
    
    def draw(self, screen):
        screen.blit(self.forest_image, (0, self.y_pos - self.screen_height))
        screen.blit(self.forest_image, (0, self.y_pos))
