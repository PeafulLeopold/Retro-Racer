import pygame
import sys
import sqlite3

from colors import GREEN


class Registration:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 800
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Регистрация")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GRAY = (150, 150, 150)  
        self.ACT_COLOR = (0, 255, 0)
        self.ERROR_COLOR = (255, 0, 0)  # Цвет для ошибок

        self.font = pygame.font.Font(None, 60)
        self.title_font = pygame.font.Font(None, 80)  # Шрифт для заголовка

        self.name_input_rect = pygame.Rect(170, 200, 500, 70)
        self.password_input_rect = pygame.Rect(170, 350, 500, 70)
        self.confirm_pass_rect = pygame.Rect(170, 500, 500, 70)

        self.name_active = False
        self.psw_active = False
        self.confirm_active = False

        self.name_text = ''
        self.psw_text = ''
        self.confirm_psw_text = ''

        self.name_holder = "Введите игровое имя..."  
        self.password_input_holder = "Введите пароль..."
        self.confirm_pass_holder = "Повторите пароль..."  

        self.name_cursor_visible = True
        self.name_cursor = 0

        self.psw_cursor_visible = True
        self.psw_cursor = 0

        self.confirm_cursor_visible = True
        self.confirm_cursor = 0
        self.clock = pygame.time.Clock()
        self.running = True

        self.register_button_rect = pygame.Rect(140, 660, 560, 80)

        self.name_error = False
        self.password_error = False
        self.confirm_error = False
        self.error_message = ""
        self.success_message = ""

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.name_input_rect.collidepoint(event.pos):
                    self.name_active = True
                    self.psw_active = False
                    self.confirm_active = False
                    self.name_error = False  
                elif self.password_input_rect.collidepoint(event.pos):
                    self.name_active = False
                    self.psw_active = True
                    self.confirm_active = False
                    self.password_error = False  
                elif self.confirm_pass_rect.collidepoint(event.pos):
                    self.name_active = False
                    self.psw_active = False
                    self.confirm_active = True
                    self.confirm_error = False  
                elif self.register_button_rect.collidepoint(event.pos):
                    if not self.name_text:
                        self.name_error = True
                        self.error_message = "Ошибка: имя не может быть пустым!"
                    else:
                        self.name_error = False

                    if not self.psw_text:
                        self.password_error = True
                        self.error_message = "Ошибка: пароль не может быть пустым!"
                    else:
                        self.password_error = False

                    if not self.confirm_psw_text:
                        self.confirm_error = True
                        self.error_message = "Ошибка: подтвердите пароль!"
                    else:
                        self.confirm_error = False

                    if self.psw_text and self.confirm_psw_text and self.psw_text != self.confirm_psw_text:
                        self.password_error = True
                        self.confirm_error = True
                        self.error_message = "Ошибка: пароли не совпадают!"


                    if not self.name_error and not self.password_error and not self.confirm_error:
                        self.error_message = ""
                        self.success_message = "Регистрация прошла успешно!"
                        print("Регистрация прошла успешно!")
                else:
                    self.name_active = False
                    self.psw_active = False
                    self.confirm_active = False

            if event.type == pygame.KEYDOWN:
                if self.name_active:
                    if event.key == pygame.K_RETURN:
                        self.name_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.name_text = self.name_text[:-1]
                    else:
                        if len(self.name_text) < 20:
                            self.name_text += event.unicode

                elif self.psw_active:
                    if event.key == pygame.K_RETURN:
                        self.psw_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.psw_text = self.psw_text[:-1]
                    else:
                        if len(self.psw_text) < 20:
                            self.psw_text += event.unicode

                elif self.confirm_active:
                    if event.key == pygame.K_RETURN:
                        self.confirm_psw_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.confirm_psw_text = self.confirm_psw_text[:-1]
                    else:
                        if len(self.confirm_psw_text) < 20:
                            self.confirm_psw_text += event.unicode

    def update_cursors(self):  
        self.name_cursor += self.clock.get_rawtime()
        self.psw_cursor += self.clock.get_rawtime()
        self.confirm_cursor += self.clock.get_rawtime()

        if self.name_cursor > 500:  
            self.name_cursor_visible = not self.name_cursor_visible
            self.name_cursor = 0
        if self.psw_cursor > 500:  
            self.psw_cursor_visible = not self.psw_cursor_visible
            self.psw_cursor = 0
        if self.confirm_cursor > 500:  
            self.confirm_cursor_visible = not self.confirm_cursor_visible
            self.confirm_cursor = 0

    def draw(self):
        self.screen.fill(self.BLACK)
        title_surface = self.title_font.render("Регистрация", True, self.WHITE)
        title_rect = title_surface.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(title_surface, title_rect)

        name_color = self.ERROR_COLOR if self.name_error else (self.ACT_COLOR if self.name_active else self.GRAY)
        psw_color = self.ERROR_COLOR if self.password_error else (self.ACT_COLOR if self.psw_active else self.GRAY)
        confirm_color = self.ERROR_COLOR if self.confirm_error else (self.ACT_COLOR if self.confirm_active else self.GRAY)

        pygame.draw.rect(self.screen, name_color, self.name_input_rect, 2)
        pygame.draw.rect(self.screen, psw_color, self.password_input_rect, 2)
        pygame.draw.rect(self.screen, confirm_color, self.confirm_pass_rect, 2)

        name_display_text = self.name_text if self.name_text or self.name_active else self.name_holder
        name_text_color = self.WHITE if self.name_text or self.name_active else self.LIGHT_GRAY

        psw_display_text = self.psw_text if self.psw_text or self.psw_active else self.password_input_holder
        psw_text_color = self.WHITE if self.psw_text or self.psw_active else self.LIGHT_GRAY

        confirm_display_text = self.confirm_psw_text if self.confirm_psw_text or self.confirm_active else self.confirm_pass_holder
        confirm_text_color = self.WHITE if self.confirm_psw_text or self.confirm_active else self.LIGHT_GRAY

        name_text_surface = self.font.render(name_display_text, True, name_text_color)
        self.screen.blit(name_text_surface, (self.name_input_rect.x + 10, self.name_input_rect.y + 15))

        psw_text_surface = self.font.render(psw_display_text, True, psw_text_color)
        self.screen.blit(psw_text_surface, (self.password_input_rect.x + 10, self.password_input_rect.y + 15))
        confirm_text_surface = self.font.render(confirm_display_text, True, confirm_text_color)
        self.screen.blit(confirm_text_surface, (self.confirm_pass_rect.x + 10, self.confirm_pass_rect.y + 15))

        if self.name_active and self.name_cursor_visible:
            name_cursor_x = self.name_input_rect.x + 10 + name_text_surface.get_width()
            name_cursor_rect = pygame.Rect(name_cursor_x, self.name_input_rect.y + 15, 2, self.name_input_rect.height - 30)
            pygame.draw.rect(self.screen, self.WHITE, name_cursor_rect)

        if self.psw_active and self.psw_cursor_visible:
            psw_cursor_x = self.password_input_rect.x + 10 + psw_text_surface.get_width()
            psw_cursor_rect = pygame.Rect(psw_cursor_x, self.password_input_rect.y + 15, 2, self.password_input_rect.height - 30)
            pygame.draw.rect(self.screen, self.WHITE, psw_cursor_rect)

        if self.confirm_active and self.confirm_cursor_visible:
            confirm_cursor_x = self.confirm_pass_rect.x + 10 + confirm_text_surface.get_width()
            confirm_cursor_rect = pygame.Rect(confirm_cursor_x, self.confirm_pass_rect.y + 15, 2, self.confirm_pass_rect.height - 30)
            pygame.draw.rect(self.screen, self.WHITE, confirm_cursor_rect)

        pygame.draw.rect(self.screen, self.BLACK, self.register_button_rect)
        pygame.draw.rect(self.screen, self.WHITE, self.register_button_rect, 2) 
        register_text_surface = self.font.render("Зарегистрироваться", True, self.WHITE)
        register_text_rect = register_text_surface.get_rect(center=self.register_button_rect.center)
        self.screen.blit(register_text_surface, register_text_rect)
        
        if self.error_message:
            error_surface = self.font.render(self.error_message, True, self.ERROR_COLOR)
            error_rect = error_surface.get_rect(center=(self.WIDTH // 2, 610))
            self.screen.blit(error_surface, error_rect)
        
        elif self.success_message:
            self.success_message = ''

            success_surface = self.font.render("Регистрация прошла успешно!", True, GREEN)
            success_rect = success_surface.get_rect(center=(self.WIDTH // 2 + 10, 610))
            self.screen.blit(success_surface, success_rect)

            conn = sqlite3.connect('db/project_database.db')
            cursor = conn.cursor()

            cursor.execute('''
                           INSERT INTO Users (username, password)
                           VALUES (?, ?)
                           ''', (self.name_text, self.psw_text))

            conn.commit()
            conn.close()
            

            # Для себя
            print("Пользователь успешно добавлен!")

        pygame.display.flip()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update_cursors()
            self.draw()
            self.clock.tick(60)


