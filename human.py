import pygame
import random
import sys
from settings import Settings
import json
from score import Score, ReturnToMenuFromScore

class SnakeGame:
    def __init__(self, mode, username):
        # Initialize the game
        pygame.init()

        # Calling objects
        self.settings = Settings()

        # Game mode
        self.mode = mode

        # Set the dimensions of the game window
        self.window = pygame.display.set_mode((self.settings.window_width, self.settings.window_height))
        pygame.display.set_caption("Snake Game")

        # Initialize game variables
        self.score = 1
        self.direction = ""
        self.space_held = False
        self.game_over_flag = False
        self.game_exit_flag = False
        self.username = username

        # Create the snake
        self.snake_list = []
        self.snake_length = 1

        # Size and initial position of the food
        self.food_size = 20
        self.food_x = round(random.randrange(0, self.settings.window_width - self.food_size) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, self.settings.window_height - self.food_size) / 20.0) * 20.0

        # Size and initial position of the snake
        self.snake_block_size = 20
        self.snake_speed = 7
        self.snake_x = self.settings.window_width / 2
        self.snake_y = self.settings.window_height / 2
        self.snake_x_change = 0
        self.snake_y_change = 0

        # Creating a header frame
        self.header = pygame.Surface((self.settings.header_width, self.settings.header_height), pygame.SRCALPHA)  # Create a surface with per-pixel alpha
        self.header.fill((255, 255, 255, 0))  # Set the background color with transparency (RGBA values)

        # Score
        self.text = self.settings.font1.render("Score: " + str(self.score), True, self.settings.font_color)

        # Username
        self.username_text = self.settings.font1.render("Player: " + str(self.username), True, self.settings.font_color)
        self.header.blit(self.username_text, (self.settings.window_width - self.username_text.get_width() - 10 ,10))

        # Background image
        self.background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
        self.background.set_alpha(128)  # Set opacity (128 is 50%)

        # Set the clock to control the game's frame rate
        self.clock = pygame.time.Clock()

        # Start the game
        self.start()

        # Some delay before going back
        pygame.time.delay(500)
        return

    def generate_food(self):
        self.food_x = round(random.randrange(0, self.settings.window_width - self.food_size) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, self.settings.window_height - self.food_size) / 20.0) * 20.0

        while [self.food_x, self.food_y] in self.snake_list:
            self.food_x = round(random.randrange(0, self.settings.window_width - self.food_size) / 20.0) * 20.0
            self.food_y = round(random.randrange(0, self.settings.window_height - self.food_size) / 20.0) * 20.0

    def draw_food(self):
            pygame.draw.rect(self.window, self.settings.food_color, [self.food_x, self.food_y, self.food_size, self.food_size])

    # Function to draw food but god mode
    def god_mode(self):

        valid_food = False

        # Generate a random position for the food
        while not valid_food:
            food_x = round(random.randrange(0, self.settings.window_width - self.food_size) / 20.0) * 20.0
            food_y = round(random.randrange(0, self.settings.window_height - self.food_size) / 20.0) * 20.0

            # Check if the food position is overlapping with the snake
            if [food_x, food_y] not in self.snake_list:
                valid_food = True

        pygame.draw.rect(self.window, self.settings.font_color, [food_x, food_y, self.food_size, self.food_size])

    def draw_snake(self):
        for x in self.snake_list:
            pygame.draw.rect(self.window, self.settings.snake_color, [x[0], x[1], self.snake_block_size, self.snake_block_size])

    # Function to restart the game
    def restart_game(self):
        self.game_over_flag = False
        self.snake_x = self.settings.window_width / 2
        self.snake_y = self.settings.window_height / 2
        self.snake_x_change = 0
        self.snake_y_change = 0
        self.snake_list = []
        self.snake_length = 1
        self.score = 1
        self.space_held = False
        self.direction = ""
        self.food_x = round(random.randrange(0, self.settings.window_width - self.food_size) / 20.0) * 20.0
        self.food_y = round(random.randrange(0, self.settings.window_height - self.food_size) / 20.0) * 20.0

    # Game Over screen
    def game_over(self):

        # Calculate button positions
        restart_button_rect = pygame.Rect(self.settings.window_width / 2 - self.settings.button_width - 25, self.settings.window_height / 2 + 50, self.settings.button_width, self.settings.button_height)
        menu_button_rect = pygame.Rect(self.settings.window_width / 2 + 25, self.settings.window_height / 2 + 50, self.settings.button_width, self.settings.button_height)

        # Load the JSON data
        try:
            if self.mode == 1:
                with open('data/normal.json', 'r') as file:
                    data = json.load(file)
            elif self.mode == 2:
                with open('data/godmode.json', 'r') as file:
                    data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}

        if self.username not in data or data[self.username] < self.score:
            data[self.username] = self.score

        # Sort the scores in descending order
        sorted_scores = sorted(data.items(), key=lambda x: x[1], reverse=True)

        # Create a new dictionary with the sorted scores
        sorted_data = {name: score for name, score in sorted_scores}

        # Rewrite the original JSON file with the sorted data
        if self.mode == 1:
            with open('data/normal.json', 'w') as file:
                json.dump(sorted_data, file)
        elif self.mode == 2:
            with open('data/godmode.json', 'w') as file:
                json.dump(sorted_data, file)

        # Game Over screen
        while True:
            for event in pygame.event.get():
                # Checking if Quit button is clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RETURN: # K_RETURN refers to Enter key
                        self.restart_game()
                        return # Exit the game_over() function
                    if event.key == pygame.K_ESCAPE:
                        return "back"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Check if restart button was clicked
                        if restart_button_rect.collidepoint(event.pos):
                            self.restart_game()
                            return # Exit the game_over() function

                        # Check if menu button was clicked
                        elif menu_button_rect.collidepoint(event.pos):
                            return "back"
                        
                        elif score_text_rect.collidepoint(event.pos):
                            try:
                                Score(self.mode)
                            except ReturnToMenuFromScore:
                                pass

            # Draw the background image
            self.window.blit(self.background, (0, 0))

            # Display Game Over text
            # self.window.fill(self.settings.black)
            text = self.settings.font4.render("Game Over", True, self.settings.font_color)
            self.window.blit(text, [self.settings.window_width / 2 - text.get_width() / 2, self.settings.window_height / 2 - text.get_height() / 2 - 100])

            # Display the score text
            score_text = self.settings.score_font.render("Score: {}".format(self.score), True, self.settings.font_color)
            score_text_rect = score_text.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 2))
            self.window.blit(score_text, score_text_rect)

            # Note
            note = self.settings.font0.render("Press score for more infos!", True, self.settings.font_color)
            note_rect = note.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 2 + 20))
            self.window.blit(note, note_rect)

            # Display best score
            # best_score_text = self.settings.font1.render("Best score: {}".format(best_score), True, self.settings.font_color)
            # best_score_rect = best_score_text.get_rect(center=(self.settings.window_width / 2, self.settings.window_height / 2 + 40))
            # self.window.blit(best_score_text, best_score_rect)

            # Draw the restart button
            pygame.draw.rect(self.window, self.settings.white, restart_button_rect)
            restart_text = self.settings.font1.render("Restart", True, (0, 0, 0))
            restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
            self.window.blit(restart_text, restart_text_rect)

            # Draw the mwhite
            pygame.draw.rect(self.window, self.settings.white, menu_button_rect)
            menu_text = self.settings.font1.render("Menu", True, (0, 0, 0))
            menu_text_rect = menu_text.get_rect(center=menu_button_rect.center)
            self.window.blit(menu_text, menu_text_rect)

            pygame.display.flip()

            # Delay to control the frame rate
            pygame.time.Clock().tick(60)

    def start(self):

        while not self.game_exit_flag:
            while self.game_over_flag:
                # Draw the background image
                self.window.blit(self.background, (0, 0))

                back = self.game_over()
                if back == "back":
                    return None

            # Movements keys
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.space_held = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and self.direction != "R":
                        self.snake_x_change = -self.snake_block_size
                        self.snake_y_change = 0
                        self.direction = "L"
                    elif event.key == pygame.K_RIGHT and self.direction != "L":
                        self.snake_x_change = self.snake_block_size
                        self.snake_y_change = 0
                        self.direction = "R"
                    elif event.key == pygame.K_UP and self.direction != "D":
                        self.snake_y_change = -self.snake_block_size
                        self.snake_x_change = 0
                        self.direction = "U"
                    elif event.key == pygame.K_DOWN and self.direction != "U":
                        self.snake_y_change = self.snake_block_size
                        self.snake_x_change = 0
                        self.direction = "D"
                    elif event.key == pygame.K_SPACE:
                        self.space_held = True
                            
                if self.space_held:
                    self.snake_speed = 15
                else:
                    self.snake_speed = 7
                        
            if self.snake_x >= self.settings.window_width or self.snake_x < 0 or self.snake_y >= self.settings.window_height or self.snake_y < 0:
                self.game_over_flag = True

            # Increasing snake x, y positions
            self.snake_x += self.snake_x_change
            self.snake_y += self.snake_y_change

            # Draw the background image
            self.window.blit(self.background, (0, 0))

            # Drawing food
            if self.mode == 1:
                self.draw_food()
            elif self.mode == 2:
                self.god_mode()
            # pygame.draw.rect(window, self.settings.font_color, [food_x, food_y, food_size, food_size])

            snake_head = []
            snake_head.append(self.snake_x)
            snake_head.append(self.snake_y)
            self.snake_list.append(snake_head)

            # Snake moving animation frames
            if len(self.snake_list) > self.snake_length:
                del self.snake_list[0]

            # Checking for collision
            for x in self.snake_list[:-1]:
                if x == snake_head:
                    self.game_over_flag = True

            # Drawing snake
            self.draw_snake()

            # Header
            self.window.blit(self.header, (0,0))  # Draw the frame onto the main window

            # Clear the previous text object
            self.header.fill((255, 255, 255, 0), (10, 10, self.text.get_width(), self.text.get_height()))

            # Update the score text
            self.text = self.settings.font1.render("Score: " + str(self.score), True, self.settings.font_color)  # Render the text in white color
            self.header.blit(self.text, (10,10))

            pygame.display.update()

            # Eating food
            if self.snake_x == self.food_x and self.snake_y == self.food_y:
            
                # Check if the food coordinates match any snake coordinates
                self.generate_food()

                # Drawing food
                if self.mode == 1:
                    self.draw_food()
                elif self.mode == 2:
                    return
                elif self.mode == 3:
                    self.god_mode()

                self.snake_length += 1
                self.score += 1

            self.clock.tick(self.snake_speed)