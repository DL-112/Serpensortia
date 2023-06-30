import pygame
from settings import Settings
from agent import train
import sys
from user import User, ReturnToMenuException
from settings_gui import Settings_GUI, ReturnToMenuFromSettings, Restart
from easy_json import get_value, edit_value
from score import Score, ReturnToMenuFromScore

class Menu:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        self.settings = Settings()

        # Creating window
        self.window = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Menu")

        self.clock = pygame.time.Clock()

        # Load and scale the menu background image
        self.menu_background = self.settings.background
        self.menu_background = pygame.transform.scale(self.menu_background, (self.settings.window_width, self.settings.window_height))

    def draw_button(self, button_rect, button_text):
        # Draw a button with given rectangle and text
        pygame.draw.rect(self.window, self.settings.gray, button_rect)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.window.blit(button_text, button_text_rect)

    def run(self):
        # Calculate button positions
        self.button_margin = 20
        self.text_top = self.button_margin + 100
        self.button_width = 300

        normal_snake_button = pygame.Rect(self.settings.window_width // 2 - self.button_width // 2, self.text_top + 90, self.button_width, self.settings.button_height)
        ai_snake_button = pygame.Rect(self.settings.window_width // 2 - self.button_width // 2, normal_snake_button.bottom + self.button_margin, self.button_width, self.settings.button_height)
        god_mode = pygame.Rect(self.settings.window_width // 2 - self.button_width // 2, ai_snake_button.bottom + self.button_margin, self.button_width, self.settings.button_height)

        try:
            while True:
                self.clock.tick(60)  # Limit frame rate to 60 FPS

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Left mouse button clicked
                            # Check if the Start button was clicked
                            if normal_snake_button.collidepoint(event.pos):
                                try:
                                    User(1)
                                except ReturnToMenuException:
                                    pass
                            elif ai_snake_button.collidepoint(event.pos):
                                self.AI_snake()
                                return
                            elif god_mode.collidepoint(event.pos):
                                try:
                                    User(2)
                                except ReturnToMenuException:
                                    pass
                            elif icon_rect.collidepoint(event.pos):  # Check if settings icon was clicked
                                try:
                                    Settings_GUI()
                                except ReturnToMenuFromSettings:
                                    pass
                                except Restart:
                                    pygame.event.post(pygame.event.Event(pygame.QUIT))  # Post a quit event
                            elif text_rect.collidepoint(event.pos):
                                try:
                                    Score(1)
                                except ReturnToMenuFromScore:
                                    pass

                # Display menu with background image
                self.window.blit(self.menu_background, (0, 0))

                # Display title
                text = self.settings.font3.render("Serpensortia", True, self.settings.font_color)
                text_rect = text.get_rect(center=(self.settings.window_width // 2, self.text_top + text.get_height() // 2 - 40))
                self.window.blit(text, text_rect)

                # Draw the settings icon at the top right corner
                icon_size = (30, 30)
                icon_rect = self.settings.settings_icon.get_rect(topright=(self.settings.window_width + 15, 10))
                settings_icon_resized = pygame.transform.scale(self.settings.settings_icon, icon_size)
                self.window.blit(settings_icon_resized, icon_rect)

                # Draw the Start button
                self.draw_button(normal_snake_button, self.settings.font1.render("Start", True, self.settings.black))

                # Draw the AI Snake button
                self.draw_button(ai_snake_button, self.settings.font1.render("AI Snake", True, self.settings.black))

                # Draw God mode button
                self.draw_button(god_mode, self.settings.font1.render("God mode", True, self.settings.black))

                # Display copyright
                Cfont = pygame.font.Font(None, 30)
                copyright = Cfont.render("Copyright © 2023 MIIT. All rights reserved.", True, self.settings.font_color)
                copyright_rect = copyright.get_rect(center=(self.settings.window_width // 2, self.settings.window_height - 15))
                self.window.blit(copyright, copyright_rect)

                pygame.display.flip()
        except pygame.error:
            pass

    # Clicked AI snake
    def AI_snake(self):

        # Calculate button positions
        ok_button_rect = pygame.Rect(self.settings.window_width // 2 - self.button_width // 2, self.text_top + 150, self.button_width, self.settings.button_height)
        cancel_button_rect = pygame.Rect(self.settings.window_width // 2 - self.button_width // 2, ok_button_rect.bottom + self.button_margin, self.button_width, self.settings.button_height)

        while True:
            for event in pygame.event.get():
                # Checking if Quit button is clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN:  # K_RETURN refers to Enter key
                        # Some delay before starting the game
                        pygame.time.delay(500)

                        # Initialize and run the AI SnakeGame
                        train()
                    if event.key == pygame.K_ESCAPE:
                        self.run()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check if Ok button was clicked
                        if ok_button_rect.collidepoint(event.pos):
                            # Some delay before starting the game
                            pygame.time.delay(500)

                            # Initialize and run the AI SnakeGame
                            train()
                        # Check if cancel button was clicked
                        elif cancel_button_rect.collidepoint(event.pos):
                            self.run()

            # Draw the background image
            background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
            background.set_alpha(128)  # Set opacity (128 is 50%)
            self.window.blit(background, (0, 0))

            # Display Notes
            text1 = self.settings.font2.render("Introducing the \"AI Self-Play Snake\" mode:", True, self.settings.font_color)
            text1_rect = text1.get_rect(center=(self.settings.window_width // 2, self.text_top + text1.get_height() // 2 + 20))
            self.window.blit(text1, text1_rect)

            text2 = self.settings.font2.render("Sit back and witness the snake train and grow", True, self.settings.font_color)
            text2_rect = text2.get_rect(center=(self.settings.window_width // 2, self.text_top + text2.get_height() // 2 + 45))
            self.window.blit(text2, text2_rect)

            text3 = self.settings.font2.render("without any user input required.", True, self.settings.font_color)
            text3_rect = text3.get_rect(center=(self.settings.window_width // 2, self.text_top + text3.get_height() // 2 + 70))
            self.window.blit(text3, text3_rect)

            # Draw the Ok button
            self.draw_button(ok_button_rect, self.settings.font1.render("Ok", True, self.settings.black))

            # Draw the Cancel button
            self.draw_button(cancel_button_rect, self.settings.font1.render("Cancel", True, self.settings.black))

            pygame.display.flip()

            # Delay to control the frame rate
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    while True:
        frame = Menu()
        frame.run()

        # Check for a condition to restart the program
        if get_value("restart", "data/settings.json") == 1:
            edit_value("restart", 0, "data/settings.json")  # Reset the restart condition in the JSON file
            del frame  # Delete the existing object
            continue  # Continue to the next iteration to create a new object
        else:
            break