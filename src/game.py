import pygame
import random
from colors import WHITE, RED, GREEN, BLACK
from car import Car
from hole import Hole
from road import Road
from forest import Forest

# Функция для вычисления центра полосы на дороге на основе road.rect
def get_lane_center(road_rect, lane):
    # Делим ширину дороги на 3 равные части:
    # Центр левой полосы: left + width/6, средней: left + width/2, правой: left + 5*width/6.
    if lane == 0:
        return road_rect.left + road_rect.width / 6
    elif lane == 1:
        return road_rect.left + road_rect.width / 2
    elif lane == 2:
        return road_rect.left + 5 * road_rect.width / 6

# Класс бонусов: монеты и сердца
class Bonus:
    def __init__(self, bonus_type, screen_height, image_path, speed, lane, lane_center):
        self.bonus_type = bonus_type  # "coin" или "heart"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey(WHITE)  # Убираем белый фон
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.lane = lane
        self.x = lane_center
        self.y = -50
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.y += self.speed
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Основной класс игры (без вражеских машин)
class Game:
    def __init__(self, game_state, settings):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Retro Racer")

        # Загружаем изображение автомобиля: выбранный из гаража или дефолтное
        if game_state.selected_car:
            self.car_img = pygame.image.load(game_state.selected_car['image_path']).convert_alpha()
            car_speed = game_state.selected_car['speed']
        else:
            self.car_img = pygame.image.load("data/images/car.png").convert_alpha()
            car_speed = 5

        self.road_img = pygame.image.load("data/images/road.png").convert_alpha()
        self.forest_img = pygame.image.load("data/images/forest.jpg").convert()

        # Загрузка звуков
        pygame.mixer.music.load("data/sounds/car_sound.mp3")
        self.crash_sound = pygame.mixer.Sound("data/sounds/car_crash.mp3")

        # Инициализация игровых объектов
        self.player = Car(self.WIDTH // 2, self.HEIGHT // 2 + 150, self.car_img, car_speed, settings.control_scheme)
        self.road = Road(self.HEIGHT, self.WIDTH, self.road_img, 3)
        self.forest = Forest(self.HEIGHT, self.forest_img, 1)
        self.holes = []
        self.player.set_move_bounds(self.road.rect)

        # Инициализация бонусов
        self.bonuses = []
        self.bonus_spawn_cooldown = random.randint(5000, 10000)
        self.last_bonus_spawn = pygame.time.get_ticks()

        # Спавн ям (препятствий)
        self.spawn_cooldown = 1500
        self.min_vertical_spacing = 400
        self.occupied_lanes = set()
        self.last_spawn = pygame.time.get_ticks()

        # Игровые параметры
        self.lives = 3
        self.score = 0
        self.distance = 0
        self.game_state = game_state
        self.score_timer = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.earned_money = 0

        pygame.mixer.music.play(-1)

    def can_spawn_hole(self, new_hole):
        if new_hole.lane in self.occupied_lanes:
            return False
        for hole in self.holes:
            if abs(new_hole.rect.y - hole.rect.y) < self.min_vertical_spacing:
                return False
        return True

    def spawn_hole(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.spawn_cooldown:
            available_lanes = [0, 1, 2]
            if len(self.occupied_lanes) >= 2:
                available_lanes = [lane for lane in available_lanes if lane not in self.occupied_lanes]
            if not available_lanes:
                return
            lane = random.choice(available_lanes)
            new_hole = Hole(self.HEIGHT, "data/images/hole.png", 3, lane)
            # Пересчитываем x ямы по центру полосы, основываясь на границах дороги:
            new_x = get_lane_center(self.road.rect, lane)
            new_hole.x = new_x
            new_hole.rect.centerx = new_x
            if self.can_spawn_hole(new_hole):
                self.holes.append(new_hole)
                self.occupied_lanes.add(lane)
                self.last_spawn = now
                self.spawn_cooldown = random.randint(1200, 2500)

    def spawn_bonus(self):
        now = pygame.time.get_ticks()
        if now - self.last_bonus_spawn > self.bonus_spawn_cooldown:
            bonus_type = "coin" if random.random() < 0.7 else "heart"
            lane = random.choice([0, 1, 2])
            lane_center = get_lane_center(self.road.rect, lane)
            if bonus_type == "coin":
                image_path = "data/images/coin.png"
            else:
                image_path = "data/images/heart.png"
            bonus = Bonus(bonus_type, self.HEIGHT, image_path, speed=3, lane=lane, lane_center=lane_center)
            self.bonuses.append(bonus)
            self.last_bonus_spawn = now
            self.bonus_spawn_cooldown = random.randint(5000, 10000)

    def update_score(self):
        now = pygame.time.get_ticks()
        if now - self.score_timer > 1000:
            self.score += 10
            self.distance += self.player.speed
            elapsed_time = (now - self.start_time) / 1000
            if elapsed_time >= 3:
                self.earned_money += 1
            self.score_timer = now

    def check_collision(self):
        for hole in self.holes[:]:
            offset_x = hole.rect.x - self.player.rect.x
            offset_y = hole.rect.y - self.player.rect.y
            if self.player.mask.overlap(hole.mask, (offset_x, offset_y)):
                self.lives -= 1
                self.occupied_lanes.discard(hole.lane)
                self.holes.remove(hole)
                self.crash_sound.play()
                return True
        return False

    def check_bonus_collision(self):
        for bonus in self.bonuses[:]:
            offset_x = bonus.rect.x - self.player.rect.x
            offset_y = bonus.rect.y - self.player.rect.y
            if self.player.mask.overlap(bonus.mask, (offset_x, offset_y)):
                if bonus.bonus_type == "coin":
                    self.earned_money += 5
                elif bonus.bonus_type == "heart":
                    if self.lives < 3:
                        self.lives += 1
                self.bonuses.remove(bonus)

    def show_statistics(self):
        race_time = (pygame.time.get_ticks() - self.start_time) / 1000
        stats_font = pygame.font.Font(None, 50)
        title_font = pygame.font.Font(None, 80)
        running = True
        while running:
            self.screen.fill(WHITE)
            title_text = title_font.render("Игра окончена", True, RED)
            self.screen.blit(title_text, (self.WIDTH//2 - title_text.get_width()//2, 50))
            time_text = stats_font.render(f"Время заезда: {race_time:.2f} сек", True, BLACK)
            score_text = stats_font.render(f"Очки: {self.score}", True, BLACK)
            distance_text = stats_font.render(f"Дистанция: {self.distance}m", True, BLACK)
            money_text = stats_font.render(f"Заработано: {self.earned_money}$", True, BLACK)
            self.screen.blit(time_text, (self.WIDTH//2 - time_text.get_width()//2, 200))
            self.screen.blit(score_text, (self.WIDTH//2 - score_text.get_width()//2, 260))
            self.screen.blit(distance_text, (self.WIDTH//2 - distance_text.get_width()//2, 320))
            self.screen.blit(money_text, (self.WIDTH//2 - money_text.get_width()//2, 380))
            exit_text = stats_font.render("Нажмите ESC для возврата в главное меню", True, BLACK)
            self.screen.blit(exit_text, (self.WIDTH//2 - exit_text.get_width()//2, 500))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
        self.game_state.money += self.earned_money

    def game_loop(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

            self.player.update(keys)
            self.road.update()
            self.forest.update()
            self.spawn_hole()
            self.spawn_bonus()
            self.update_score()

            for hole in self.holes[:]:
                hole.update()
                if hole.rect.y > self.HEIGHT + 200:
                    self.occupied_lanes.discard(hole.lane)
                    self.holes.remove(hole)
            for bonus in self.bonuses[:]:
                bonus.update()
                if bonus.rect.y > self.HEIGHT + 50:
                    self.bonuses.remove(bonus)

            self.check_bonus_collision()
            if self.check_collision() and self.lives <= 0:
                running = False

            self.screen.fill(WHITE)
            self.forest.draw(self.screen)
            self.road.draw(self.screen)
            for hole in self.holes:
                hole.draw(self.screen)
            for bonus in self.bonuses:
                bonus.draw(self.screen)
            self.player.draw(self.screen)
            self.draw_text(f"Жизни: {self.lives}", 30, 30, RED, 36)
            self.draw_text(f"Очки: {self.score}", 30, 70, GREEN, 36)
            self.draw_text(f"Дистанция: {self.distance}m", 30, 110, GREEN, 36)
            self.draw_text(f"Заработано: {self.earned_money}$", 30, 150, GREEN, 36)
            pygame.display.flip()
            clock.tick(60)

        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.show_statistics()

    def draw_text(self, text, x, y, color, size):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
