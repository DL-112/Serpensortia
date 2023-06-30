from settings import Settings
import pygame
import json

class ReturnToMenuFromScore(Exception):
    pass

class Score:
    def __init__(self, mode):
        # Initialize the game
        pygame.init()

        # Mode
        self.mode = mode

        # Calling objects
        self.settings = Settings()

        # Set the dimensions of the game window
        self.window = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Score Board")

        # Set the dimensions of each cell
        self.cell_width = self.settings.window_width // 3
        self.cell_height = self.settings.window_height // 8

        # Set the clock to control the game's frame rate
        self.clock = pygame.time.Clock()

        # Display range
        self.display_range = 6

        # Start the game
        self.start()

        # Some delay before going back
        pygame.time.delay(500)

    def start(self):
        # Load the data from the JSON file
        if self.mode == 1:
            with open("data/normal.json", "r") as json_file:
                self.data = json.load(json_file)
        elif self.mode == 2:
            with open("data/godmode.json", "r") as json_file:
                self.data = json.load(json_file)

        # Convert the data to a list of tuples
        self.data = [(name, score) for name, score in self.data.items()]

        # Track the starting index of the currently displayed names
        self.starting_index = 0

        # Initially display the first 6 names
        self.displayed_data = self.data[self.starting_index:self.starting_index + 6]

        # Back button
        back_button_rect = pygame.Rect(20, 20, 30, 30)  # Rect for back button

        # Colors for buttons
        active_color = self.settings.font_color
        inactive_color = self.settings.dark_gray

        # Rectangle in the bottom left corner
        down_button_rect = pygame.Rect(20, self.settings.window_height - 60, 30, 30)

        # Triangle in the bottom left corner (facing downward)
        down_button_points = [(25, self.settings.window_height - 45),
                              (35, self.settings.window_height - 35),
                              (45, self.settings.window_height - 45)]

        # Rectangle above the down button
        up_button_rect = pygame.Rect(20, self.settings.window_height - 100, 30, 30)

        # Triangle above the down button (facing upward)
        up_button_points = [(25, self.settings.window_height - 85),
                            (35, self.settings.window_height - 95),
                            (45, self.settings.window_height - 85)]

        # Game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button clicked
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button_rect.collidepoint(mouse_pos):
                            self.back_button_command()
                        elif down_button_rect.collidepoint(mouse_pos):
                            self.down_button_command()
                        elif up_button_rect.collidepoint(mouse_pos):
                            self.up_button_command()

            # Determine if scrolling up or down is possible
            can_scroll_up = self.display_range > 6
            can_scroll_down = len(self.data) > self.display_range

            # Set button colors based on scroll availability
            up_button_color = self.settings.white if can_scroll_up else self.settings.dark_gray
            down_button_color = self.settings.white if can_scroll_down else self.settings.dark_gray

            # Drawing buttons
            pygame.draw.polygon(self.window, down_button_color, down_button_points)
            pygame.draw.polygon(self.window, up_button_color, up_button_points)

            # Clear the window by filling it with a background color
            # self.window.fill(self.settings.black)

            # Draw the background image
            background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
            background.set_alpha(128)  # Set opacity (128 is 50%)
            self.window.blit(background, (0, 0))

            # Drawing back button arrow
            pygame.draw.polygon(self.window, self.settings.font_color, [(35, 40), (45, 30), (45, 50)])

            # Render the "Score Board" text
            score_board_text = self.settings.score_font.render("Score Board", True, self.settings.font_color)
            score_board_rect = score_board_text.get_rect(center=(self.settings.window_width // 2, self.cell_height // 2))
            self.window.blit(score_board_text, score_board_rect)

            # Draw data rows
            for i, row in enumerate(self.displayed_data):
                current_index = self.starting_index + i + 1

                if i == 0:
                    font_size = self.settings.best_player_font
                else:
                    font_size = self.settings.other_players_font

                name, score = row

                text_number = font_size.render(str(current_index) + ".", True, self.settings.font_color)
                text_name = font_size.render(name, True, self.settings.font_color)
                text_score = font_size.render(str(score), True, self.settings.font_color)

                text_number_rect = text_number.get_rect(center=(self.cell_width // 2, self.cell_height * (i + 2) + self.cell_height // 2))
                text_name_rect = text_name.get_rect(center=(self.cell_width + self.cell_width // 2 - 55, self.cell_height * (i + 2) + self.cell_height // 2))
                text_score_rect = text_score.get_rect(center=(self.cell_width * 2 + self.cell_width // 2 + 40, self.cell_height * (i + 2) + self.cell_height // 2))

                self.window.blit(text_number, text_number_rect)
                self.window.blit(text_name, text_name_rect)
                self.window.blit(text_score, text_score_rect)

            # Draw the polygon for the down button
            pygame.draw.polygon(self.window, down_button_color, down_button_points)

            # Draw the polygon for the up button
            pygame.draw.polygon(self.window, up_button_color, up_button_points)

            # Update the display
            pygame.display.update()

            # Limit the frame rate
            self.clock.tick(60)

        # Quit Pygame
        pygame.quit()

    def back_button_command(self):
        raise ReturnToMenuFromScore

    def down_button_command(self):
        # Move to the next set of names
        self.starting_index += 6

        # Check if there are more names to display
        if self.starting_index + 6 >= len(self.data):
            self.starting_index = len(self.data) - 6

        # Update the displayed data based on the new starting index
        self.displayed_data = self.data[self.starting_index:self.starting_index + 6]

        self.display_range += 6
        if self.display_range > len(self.data):
            self.display_range = len(self.data)

    def up_button_command(self):
        # Move to the previous set of names
        self.starting_index -= 6

        # Check if there are more names to display
        if self.starting_index < 0:
            self.starting_index = 0

        # Update the displayed data based on the new starting index
        self.displayed_data = self.data[self.starting_index:self.starting_index + 6]

        self.display_range -= 6
        if self.display_range < 6:
            self.display_range = 6
