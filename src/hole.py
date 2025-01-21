import pygame
class Hole:
    def __init__(self, screen_height, hole_img, speed):
        self.hole_image = pygame.transform.scale(hole_img, (150, 150))
        self.screen_height = screen_height
        self.x_pos = 290
        self.y_pos = 0
        self.scrolling_speed = speed
        self.hole_rect = self.hole_image.get_rect()
    
    def update(self):
        self.y_pos += self.scrolling_speed
        
        if self.y_pos >= self.screen_height:
            self.y_pos = 0
    
    def draw(self, screen):
        screen.blit(self.hole_image, (self.x_pos, self.y_pos - self.screen_height))
        screen.blit(self.hole_image, (self.x_pos, self.y_pos))
