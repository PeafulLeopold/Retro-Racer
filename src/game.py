import pygame
import random
from colors import WHITE, RED, GREEN, BLACK
from car import Car
from hole import Hole
from road import Road
from forest import Forest
from database import update_high_score

def get_lane_center(road_rect, lane):
    lane_width = road_rect.width / 3
    return road_rect.left + lane_width * (lane + 0.5)

# монеты и сердца
class Bonus:
    def __init__(self, bonus_type, image_path, speed, lane_center):
        self.bonus_type = bonus_type  # "coin" или "heart"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.mask = pygame.mask.from_surface(self.image)
        self.speed = speed
        self.x = lane_center
        self.y = -50
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        self.y += self.speed
        self.rect.centery = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self, game_state, settings):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Retro Racer")

        if game_state.selected_car:
            raw_car_img = pygame.image.load(game_state.selected_car['image_path']).convert_alpha()
            car_speed = game_state.selected_car['speed']
        else:
            raw_car_img = pygame.image.load("data/images/car.png").convert_alpha()
            car_speed = 5

        self.road_img = pygame.image.load("data/images/road.png").convert_alpha()
        self.forest_img = pygame.image.load("data/images/forest.jpg").convert()

        pygame.mixer.music.load("data/sounds/car_sound.mp3")
        self.crash_sound = pygame.mixer.Sound("data/sounds/car_crash.mp3")

        self.player = Car(self.WIDTH // 2, self.HEIGHT // 2 + 150, raw_car_img, car_speed, settings.control_scheme)
        self.player.image = pygame.transform.scale(self.player.image, (220, 210))
        self.player.mask = pygame.mask.from_surface(self.player.image)
        self.player.rect = self.player.image.get_rect(center=self.player.rect.center)

        self.road = Road(self.HEIGHT, self.WIDTH, self.road_img, 3)
        self.forest = Forest(self.HEIGHT, self.forest_img, 1)
        self.holes = []
        self.player.set_move_bounds(self.road.rect)

        self.bonuses = []
        self.bonus_spawn_cooldown = random.randint(5000, 10000)
        self.last_bonus_spawn = pygame.time.get_ticks()

        self.spawn_cooldown = 1500
        self.last_spawn = pygame.time.get_ticks()

        self.lives = 3
        self.score = 0
        self.distance = 0
        self.game_state = game_state
        self.score_timer = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()
        self.earned_money = 0

        self.panel_visible = True

        pygame.mixer.music.play(-1)

    def spawn_hole(self):
        now = pygame.time.get_ticks()
        if now - self.last_spawn > self.spawn_cooldown:
            lane = random.choice([0, 1, 2])
            lane_center = get_lane_center(self.road.rect, lane)
            new_hole = Hole(self.HEIGHT, "data/images/hole.png", 3, lane)
            new_hole.rect.centerx = lane_center  # Центрируем яму по полосе
            new_hole.image = pygame.transform.scale(new_hole.image, (80, 80))
            new_hole.mask = pygame.mask.from_surface(new_hole.image)
            self.holes.append(new_hole)
            self.last_spawn = now
            self.spawn_cooldown = random.randint(1200, 2500)

    def spawn_bonus(self):
        now = pygame.time.get_ticks()
        if now - self.last_bonus_spawn > self.bonus_spawn_cooldown:
            bonus_type = "coin" if random.random() < 0.7 else "heart"
            lane = random.choice([0, 1, 2])
            lane_center = get_lane_center(self.road.rect, lane)
            image_path = "data/images/coin.png" if bonus_type == "coin" else "data/images/heart.png"
            bonus = Bonus(bonus_type, image_path, speed=3, lane_center=lane_center)
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
                self.earned_money += 5
            self.score_timer = now

    def check_collision(self):
        for hole in self.holes[:]:
            offset_x = hole.rect.x - self.player.rect.x
            offset_y = hole.rect.y - self.player.rect.y
            if self.player.mask.overlap(hole.mask, (offset_x, offset_y)):
                self.lives -= 1
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

    def draw_info_panel(self):
        panel_rect = pygame.Rect(10, 10, 240, 120)
        pygame.draw.rect(self.screen, BLACK, panel_rect)  
        pygame.draw.rect(self.screen, GREEN, panel_rect, 2)     

        info_font = pygame.font.Font(None, 28)
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        texts = [
            f"Жизни: {self.lives}",
            f"Заработано: {self.earned_money}$",
            f"Время: {elapsed_time:.1f} сек",
            f"Дистанция: {self.distance}m"
        ]
        for i, line in enumerate(texts):
            text_surface = info_font.render(line, True, WHITE)
            self.screen.blit(text_surface, (panel_rect.x + 10, panel_rect.y + 10 + i * 28))

    def game_loop(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_p:
                        self.panel_visible = not self.panel_visible

            keys = pygame.key.get_pressed()
            self.player.update(keys)
            self.road.update()
            self.forest.update()
            self.spawn_hole()
            self.spawn_bonus()
            self.update_score()

            for hole in self.holes[:]:
                hole.update()
                if hole.rect.y > self.HEIGHT + 200:
                    self.holes.remove(hole)
            for bonus in self.bonuses[:]:
                bonus.update()
                if bonus.rect.y > self.HEIGHT + 50:
                    self.bonuses.remove(bonus)

            self.check_bonus_collision()
            if self.check_collision() and self.lives <= 0:
                break

            self.screen.fill(WHITE)
            self.forest.draw(self.screen)
            self.road.draw(self.screen)
            for hole in self.holes:
                hole.draw(self.screen)
            for bonus in self.bonuses:
                bonus.draw(self.screen)
            self.player.draw(self.screen)

            if self.panel_visible:
                self.draw_info_panel()

            pygame.display.flip()
            clock.tick(60)

        pygame.mixer.music.stop()
        pygame.mixer.stop()
        self.show_statistics()

    def show_statistics(self):
        if self.game_state.user_id is not None:
            update_high_score(self.game_state.user_id, self.score)
        self.game_state.money += self.earned_money
        pygame.mixer.music.stop()
        pygame.mixer.stop()
