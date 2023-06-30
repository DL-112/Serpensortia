import pygame
from settings import Settings
import os
from easy_json import edit_value

class ReturnToMenuFromSettings(Exception):
    pass

class Restart(Exception):
    pass

class Settings_GUI:
    def __init__(self):
        self.settings = Settings()

        # Initializing pygame
        pygame.init()

        # Creating window
        self.window = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Settings")

        self.clock = pygame.time.Clock()

        # List of image filenames
        image_filenames = ["amazon.jpg", "anime.jpg", "heaven.jpg", "hell.jpg", "mars.jpg", "myanmar.jpg", "pyramid.jpg", "stone_age.jpg", "underwater.jpg"]

        # Load the images
        self.images = []
        for filename in image_filenames:
            image_path = os.path.join("pictures", filename)
            image = pygame.image.load(image_path)
            self.images.append(image)

        # List of unique texts corresponding to each image
        texts = ["Amazon", "Anime", "Heaven", "Hell", "Mars", "Myanmar", "Pyramid", "Stone Age", "Underwater"]

        # Calculate the positions for the rectangles
        rect_width = 150
        rect_height = 80
        row_gap = 50  # Gap between rows
        col_gap = 40  # Gap between columns
        rows = 3
        cols = 3
        total_rect_width = rect_width * cols
        total_rect_height = rect_height * rows
        total_row_gap = row_gap * (rows - 1)
        total_col_gap = col_gap * (cols - 1)
        total_width = total_rect_width + total_col_gap
        total_height = total_rect_height + total_row_gap
        start_x = (self.settings.window_width - total_width) // 2
        start_y = (self.settings.window_height - total_height) // 2

        self.rect_positions = []
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (rect_width + col_gap)
                y = start_y + row * (rect_height + row_gap)
                self.rect_positions.append((x, y))

        self.texts = texts

        self.run()

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        self.handle_click(mouse_pos)

            # Clear the screen
            # self.window.fill(self.settings.black)

            # Draw the background image
            background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
            background.set_alpha(128)  # Set opacity (128 is 50%)
            self.window.blit(background, (0, 0))

            # Render and display the text "Choose your theme"
            text = self.settings.user_font.render("Choose your theme", True, self.settings.font_color)
            text_rect = text.get_rect(center=(self.settings.window_width // 2, 30))
            self.window.blit(text, text_rect)

            # Draw the rectangles
            rect_color = (255, 0, 0)  # Red color
            rect_width = 150
            rect_height = 80

            for position, image, text in zip(self.rect_positions, self.images, self.texts):
                rect = pygame.Rect(position[0], position[1], rect_width, rect_height)
                pygame.draw.rect(self.window, rect_color, rect)

                # Resize the image to fit within the rectangle
                image = pygame.transform.scale(image, (rect_width, rect_height))
                image_rect = image.get_rect(center=rect.center)
                self.window.blit(image, image_rect)

                # Render and display the text below the image
                text_surface = self.settings.font1.render(text, True, self.settings.font_color)
                text_rect = text_surface.get_rect(center=(rect.centerx, rect.bottom + 20))
                self.window.blit(text_surface, text_rect)

            # Drawing back button arrow
            pygame.draw.polygon(self.window, self.settings.font_color, [(35, 40), (45, 30), (45, 50)])

            # Update the display
            pygame.display.update()

            # Control the frame rate
            self.clock.tick(60)

        # Quit the game
        pygame.quit()

    def handle_click(self, mouse_pos):
        for i, rect_position in enumerate(self.rect_positions):
            rect = pygame.Rect(rect_position[0], rect_position[1], 150, 80) # 150 and 80 are rect width and height
            if rect.collidepoint(mouse_pos):
                # Process the click based on the index i
                self.process_click(i)
                break

        # Check if the back button is clicked
        if self.is_back_button_clicked(mouse_pos):
            self.process_click(-1)

    def process_click(self, index):
        
        # Additional check for the back button
        if index == -1:
            self.back_button_command()

        if index == 0:
            print("Clicked on Amazon")
            edit_value("theme", "amazon", "data/settings.json")
        elif index == 1:
            print("Clicked on Anime")
            edit_value("theme", "anime", "data/settings.json")
        elif index == 2:
            print("Clicked on Heaven")
            edit_value("theme", "heaven", "data/settings.json")
        elif index == 3:
            print("Clicked on Hell")
            edit_value("theme", "hell", "data/settings.json")
        elif index == 4:
            print("Clicked on Mars")
            edit_value("theme", "mars", "data/settings.json")
        elif index == 5:
            print("Clicked on Myanmar")
            edit_value("theme", "myanmar", "data/settings.json")
        elif index == 6:
            print("Clicked on Pyramid")
            edit_value("theme", "pyramid", "data/settings.json")
        elif index == 7:
            print("Clicked on Stone age")
            edit_value("theme", "stone_age", "data/settings.json")
        elif index == 8:
            print("Clicked on Underwater")
            edit_value("theme", "underwater", "data/settings.json")

        edit_value("restart", 1, "data/settings.json")
        raise Restart

    def is_back_button_clicked(self, mouse_pos):
        back_button_rect = pygame.Rect(10, 10, 50, 50)  # Back button rectangle
        return back_button_rect.collidepoint(mouse_pos)

    def back_button_command(self):
        raise ReturnToMenuFromSettings
