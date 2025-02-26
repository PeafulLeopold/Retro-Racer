import pygame
import random
from colors import WHITE, RED, GREEN
from car import Car
from hole import Hole
from road import Road
from forest import Forest

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1100, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Retro Racer")

        # Загрузка изображений
        self.car_img = pygame.image.load("data/images/car.png").convert_alpha()
        self.road_img = pygame.image.load("data/images/road.png").convert_alpha()
        self.forest_img = pygame.image.load("data/images/forest.jpg").convert()

        # Инициализация объектов
        self.player = Car(self.WIDTH//2, self.HEIGHT//2 + 150, self.car_img, 5)
        self.road = Road(self.HEIGHT, self.WIDTH, self.road_img, 3)
        self.forest = Forest(self.HEIGHT, self.forest_img, 1)
        self.holes = []
        self.player.set_move_bounds(self.road.rect)
        
        # Параметры спавна
        self.spawn_cooldown = 1500
        self.min_vertical_spacing = 400  # Минимальное расстояние по вертикали
        self.occupied_lanes = set()     # Занятые полосы
        self.last_spawn = pygame.time.get_ticks()

        # Игровые параметры
        self.lives = 3
        self.score = 0
        self.distance = 0
        self.score_timer = pygame.time.get_ticks()

    def can_spawn_hole(self, new_hole):
        """Проверка условий для спавна новой дыры"""
        # Проверка занятости полосы
        if new_hole.lane in self.occupied_lanes:
            return False
            
        # Проверка вертикального расстояния
        for hole in self.holes:
            if abs(new_hole.rect.y - hole.rect.y) < self.min_vertical_spacing:
                return False
        return True

    def spawn_hole(self):
        """Создание новой дыры с учетом ограничений"""
        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.spawn_cooldown:
            # Генерация позиции
            available_lanes = [0, 1, 2]  # 0-левая, 1-центр, 2-правая
            if len(self.occupied_lanes) >= 2:
                available_lanes = [lane for lane in available_lanes if lane not in self.occupied_lanes]
            
            if not available_lanes:
                return
                
            lane = random.choice(available_lanes)
            new_hole = Hole(self.HEIGHT, "data/images/hole.png", 3, lane)
            
            if self.can_spawn_hole(new_hole):
                self.holes.append(new_hole)
                self.occupied_lanes.add(lane)
                self.last_spawn = now
                self.spawn_cooldown = random.randint(1200, 2500)

    def update_score(self):
        """Обновление счета каждую секунду"""
        now = pygame.time.get_ticks()
        if now - self.score_timer > 1000:
            self.score += 10
            self.distance += self.player.speed
            self.score_timer = now

    def check_collision(self):
        for hole in self.holes[:]:
            offset_x = hole.rect.x - self.player.rect.x
            offset_y = hole.rect.y - self.player.rect.y
            
            if self.player.mask.overlap(hole.mask, (offset_x, offset_y)):
                self.lives -= 1
                self.occupied_lanes.discard(hole.lane)
                self.holes.remove(hole)
                return True
        return False

    def game_loop(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Обновление состояния
            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.road.update()
            self.forest.update()
            self.spawn_hole()
            self.update_score()

            # Обновление дыр
            for hole in self.holes[:]:
                hole.update()
                if hole.rect.y > self.HEIGHT + 200:
                    self.occupied_lanes.discard(hole.lane)
                    self.holes.remove(hole)

            # Проверка коллизий
            if self.check_collision() and self.lives <= 0:
                running = False

            # Отрисовка
            self.screen.fill(WHITE)
            self.forest.draw(self.screen)
            self.road.draw(self.screen)
            
            for hole in self.holes:
                hole.draw(self.screen)
            
            self.player.draw(self.screen)

            # HUD
            self.draw_text(f"Жизни: {self.lives}", 30, 30, RED, 36)
            self.draw_text(f"Очки: {self.score}", 30, 70, GREEN, 36)
            self.draw_text(f"Дистанция: {self.distance}m", 30, 110, GREEN, 36)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def draw_text(self, text, x, y, color, size):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))