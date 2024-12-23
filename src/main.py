import pygame

from colors import WHITE
from road import Road


WIDTH, HEIGHT = 1100, 800

road_img = pygame.image.load('data/images/road_img.png')

pygame.display.set_caption('Retro Racer')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def game_loop():
    running = True
    road = Road(HEIGHT, WIDTH, road_img)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        road.update()

        screen.fill(WHITE)
        road.road_drawing(screen)

        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()
    quit()

game_loop()




