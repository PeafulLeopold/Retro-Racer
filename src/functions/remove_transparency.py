import pygame

def remove_transparency(img_path, bg_color=(0, 0, 0)):
        image = pygame.image.load(img_path).convert_alpha()
        w, h = image.get_width(), image.get_height()
        for y in range(h):
            for x in range(w):
                r, g, b, a = image.get_at((x, y))
                if a == 0:
                    image.set_at((x, y), (*bg_color, 255))
        
        return image