class Road:
    def __init__(self, screen_height, screen_width, road_img, speed):
        self.road_image = road_img
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.y_pos = 0
        self.scrolling_speed = speed
        self.road_rect = self.road_image.get_rect()
    
    def update(self):
        self.y_pos += self.scrolling_speed
        
        if self.y_pos >= self.screen_height:
            self.y_pos = 0
    
    def draw(self, screen):
        screen.blit(self.road_image, (self.screen_width // 4.25, self.y_pos - self.screen_height))
        screen.blit(self.road_image, (self.screen_width // 4.25, self.y_pos))


