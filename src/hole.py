import pygame


class Hole:
    LANE_POSITIONS = [350, 550, 750]
    
    def __init__(self, screen_height, hole_img_path, speed, lane):
        self.image = pygame.image.load(hole_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.mask = pygame.mask.from_surface(self.image)
        
        self.speed = speed
        self.HEIGHT = screen_height
        self.lane = lane
        self.x = self.LANE_POSITIONS[lane]
        self.y = -200
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.y += self.speed
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)