import pygame

class Car:
    def __init__(self, x, y, car_img, speed):
        self.x = x
        self.y = y
        self.scrolling_speed = speed
        self.car_image = pygame.transform.scale(car_img, (210, 200))
        self.car_rect = self.car_image.get_rect(center=(self.x, self.y))
    
    def update(self, keys):
        if keys[pygame.K_UP]:
            self.y -= self.scrolling_speed
        if keys[pygame.K_DOWN]:
            self.y += self.scrolling_speed
        if keys[pygame.K_LEFT]:
            self.x -= self.scrolling_speed
        if keys[pygame.K_RIGHT]:
            self.x += self.scrolling_speed
        
        self.car_rect.center = (self.x, self.y)
    
    def draw(self, screen):
        screen.blit(self.car_image, self.car_rect)
    


    


        