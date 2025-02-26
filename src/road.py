import pygame

class Road:
    def __init__(self, screen_height, screen_width, road_img, speed):
        self.road_image = pygame.transform.scale(road_img, (600, 800))
        self.speed = speed
        self.x = (screen_width - 600) // 2  # Центрирование по X
        self.rect = pygame.Rect(  # Границы дороги
            self.x + 50,          # + отступ слева
            50,                   # + отступ сверху
            600 - 100,            # - отступы по бокам
            screen_height - 100   # - отступы сверху/снизу
        )

    def update(self):
        # Прокрутка дороги (логика остается прежней)
        pass

    def draw(self, screen):
        # Отрисовка дороги (прежняя логика)
        screen.blit(self.road_image, (self.x, 0))