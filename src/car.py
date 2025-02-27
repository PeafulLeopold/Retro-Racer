import pygame

class Car:
    def __init__(self, x, y, car_img, speed, control_scheme="arrows"):
        self.image = pygame.transform.scale(car_img, (210, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.move_bounds = pygame.Rect(0, 0, 0, 0)
        self.control_scheme = control_scheme

    def set_move_bounds(self, road_rect):
        self.move_bounds = road_rect.inflate(100, 100)

    def update(self, keys):
        if self.control_scheme == "arrows":
            if keys[pygame.K_UP]: 
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y += self.speed
            if keys[pygame.K_LEFT]: 
                self.rect.x -= self.speed * 1.5
            if keys[pygame.K_RIGHT]: 
                self.rect.x += self.speed * 1.5
        elif self.control_scheme == "wasd":
            if keys[pygame.K_w]: 
                self.rect.y -= self.speed
            if keys[pygame.K_s]: 
                self.rect.y += self.speed
            if keys[pygame.K_a]: 
                self.rect.x -= self.speed * 1.5
            if keys[pygame.K_d]: 
                self.rect.x += self.speed * 1.5
        
        self.rect.clamp_ip(self.move_bounds)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
