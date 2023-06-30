import pygame
import json
from settings import Settings
from human import SnakeGame

class ReturnToMenuException(Exception):
    pass

class Button:
    def __init__(self, text, x, y, command):
        self.text = text
        self.x = x
        self.y = y
        self.command = command
        self.surface = None
        self.rect = None

    def create_surface(self, font, color):
        self.surface = font.render(self.text, True, color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))

    def draw(self, window):
        window.blit(self.surface, self.rect)

    def execute_command(self):
        self.command()

# Text input class
class TextInput:
    def __init__(self, x, y, width, height, mode):
        # Set up the font
        font_size = 24
        self.font = pygame.freetype.Font(None, font_size)

        # Mode
        self.mode = mode

        # Setting object
        self.settings = Settings()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = self.settings.font_color
        self.text = ""
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    SnakeGame(self.mode, self.text)
                    self.text = ""
                    raise ReturnToMenuException
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        self.font.render_to(screen, (self.rect.x + 5, self.rect.y + 5), self.text, self.color)

class User:
    def __init__(self, mode):
        pygame.init()

        # Setting object
        self.settings = Settings()

        self.window = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        self.buttons = []
        self.mode = mode

        self.names = []
        self.current_name_index = 0

        self.load_data()
        self.run()

    def load_data(self):
        # Load data from JSON file
        try:
            if self.mode == 1:
                with open('data/normal.json') as file:
                    data = json.load(file)
            elif self.mode == 2:
                with open('data/godmode.json') as file:
                    data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}

        self.names = list(data.keys())

        self.update_buttons()

    def update_buttons(self):
        self.buttons = []
        names_to_display = self.names[self.current_name_index:self.current_name_index + 6]

        button_spacing = 70
        button_x = self.settings.window_width // 2 - 160
        button_y = self.settings.window_height // 2 - (len(names_to_display[:3]) * button_spacing) // 2 + 150

        for index, name in enumerate(names_to_display):
            if index % 3 == 0 and index != 0:
                button_x += 320  # Adjusting x-coordinate after every 3 names
                button_y = self.settings.window_height // 2 - (len(names_to_display[index:index+3]) * button_spacing) // 2 + 150  # Reset y-coordinate

            # Display the name button
            name_button = Button(name, button_x, button_y, lambda n=name: self.button_command(n))
            name_button.create_surface(self.settings.user_font, self.settings.font_color)
            self.buttons.append(name_button)

            button_y += button_spacing

    def run(self):
        running = True

        # Create an instance of the TextInput class
        input_box = TextInput(self.settings.window_width / 2 - 125, 170, 250, 40, self.mode)

        # Define the button dimensions and positions
        button_width = 60
        button_height = 40
        button_y = (self.settings.window_height / 4) * 3 - button_height  # Adjusted button y-axis position

        # Back button
        back_button_rect = pygame.Rect(20, 20, 30, 30)  # Rect for back button

        # Left button
        left_button_rect = pygame.Rect(20, button_y, button_width, button_height)
        left_button_active_color = self.settings.font_color
        left_button_inactive_color = self.settings.dark_gray
        left_button_color = left_button_active_color

        # Right button
        right_button_rect = pygame.Rect(self.settings.window_width - 20 - button_width, button_y, button_width, button_height)
        right_button_active_color = self.settings.font_color
        right_button_inactive_color = self.settings.dark_gray
        right_button_color = right_button_active_color

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        mouse_pos = pygame.mouse.get_pos()
                        # Check if any button was clicked
                        for button in self.buttons:
                            if button.rect.collidepoint(mouse_pos):
                                button.execute_command()  # Execute the associated command for the clicked button
                        if back_button_rect.collidepoint(mouse_pos):
                            self.back_button_command()
                        if left_button_rect.collidepoint(mouse_pos):
                            if self.current_name_index > 0:
                                self.current_name_index -= 6
                                self.update_buttons()
                        if right_button_rect.collidepoint(mouse_pos):
                            if self.current_name_index + 6 < len(self.names):
                                self.current_name_index += 6
                                self.update_buttons()

                # Handle input box
                input_box.handle_event(event)

            # Draw the background image
            background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
            background.set_alpha(128)  # Set opacity (128 is 50%)
            self.window.blit(background, (0, 0))

            # Display some texts using the score font
            text = self.settings.score_font.render("- Choose your name -", True, self.settings.font_color)
            text_rect = text.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 4))
            self.window.blit(text, text_rect)

            # Another text
            text2 = self.settings.font1.render("or add a new one", True, self.settings.font_color)
            text2_rect = text2.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 2 - 80))
            self.window.blit(text2, text2_rect)

            # Draw the input box
            input_box.draw(self.window)

            # Draw the buttons
            for button in self.buttons:
                button.draw(self.window)

            # Drawing back button arrow
            pygame.draw.polygon(self.window, self.settings.font_color, [(35, 40), (45, 30), (45, 50)])

            # Drawing left button
            left_button_points = [(30, button_y),
                                (30, button_y + button_height),
                                (20, button_y + button_height / 2)]
            pygame.draw.polygon(self.window, left_button_color, left_button_points)

            # Drawing right button
            right_button_points = [(self.settings.window_width - 30, button_y),
                                (self.settings.window_width - 30, button_y + button_height),
                                (self.settings.window_width - 20, button_y + button_height / 2)]
            pygame.draw.polygon(self.window, right_button_color, right_button_points)

            # Update left button color
            if self.current_name_index == 0:
                left_button_color = left_button_inactive_color
            else:
                left_button_color = left_button_active_color

            # Update right button color
            if self.current_name_index + 6 >= len(self.names):
                right_button_color = right_button_inactive_color
            else:
                right_button_color = right_button_active_color

            pygame.display.flip()

        pygame.quit()

    def button_command(self, name):
        print(f"Logged in as {name}!")
        # Add actions or logic specific to the button
        SnakeGame(self.mode, f"{name}")
        raise ReturnToMenuException

    def back_button_command(self):
        raise ReturnToMenuException
    
    def left_button_command(self):
        if self.current_name_index > 0:
            self.current_name_index -= 6
            self.update_buttons()

    def right_button_command(self):
        if self.current_name_index + 6 < len(self.names):
            self.current_name_index += 6
            self.update_buttons()
