import pygame

#button class
class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, right_click_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color, self.right_click_color = base_color, hovering_color, right_click_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.last_click_time = 0
        
    def get_value(self):
        return int(self.text_input)

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position, left_click, right_click):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            if right_click:
                self.text = self.font.render(self.text_input, True, self.right_click_color)
            else:
                self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def check_click(self, mouse_pos, left_click, right_click):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_click_time > 100:  # 100 milliseconds (0.1 seconds) delay
            self.last_click_time = current_time

            if self.rect.collidepoint(mouse_pos):
                if left_click:
                    return 1
                elif right_click:
                    return -1
        return 0
    
    def update_text(self):
        self.text = self.font.render(self.text_input, True, self.base_color)

    def increment_value(self):
        current_value = int(self.text_input)
        new_value = max(0, current_value + 1)
        self.text_input = str(new_value)
        self.update_text()
    
    def decrement_value(self):
        current_value = int(self.text_input)
        new_value = max(0, current_value - 1)
        self.text_input = str(new_value)
        self.update_text()
