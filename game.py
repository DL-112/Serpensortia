import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np
from settings import Settings

pygame.init()

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

SPEED = 20

class SnakeGameAI:

    def __init__(self):

        self.settings = Settings()

        self.w = self.settings.window_width
        self.h = self.settings.window_height
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('AI Snake')
        self.clock = pygame.time.Clock()
        self.reset()


    def reset(self):
        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-self.settings.block_size, self.head.y),
                      Point(self.head.x-(2*self.settings.block_size), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def _place_food(self):
        x = random.randint(0, (self.w-self.settings.block_size )//self.settings.block_size )*self.settings.block_size
        y = random.randint(0, (self.h-self.settings.block_size )//self.settings.block_size )*self.settings.block_size
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()


    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action) # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score


    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # hits boundary
        if pt.x > self.w - self.settings.block_size or pt.x < 0 or pt.y > self.h - self.settings.block_size or pt.y < 0:
            return True
        # hits itself
        if pt in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        # Draw the background image
        background = pygame.transform.scale(self.settings.background, (self.settings.window_width, self.settings.window_height))
        background.set_alpha(128)  # Set opacity (128 is 50%)
        self.display.blit(background, (0, 0))

        for pt in self.snake:
            pygame.draw.rect(self.display, self.settings.snake_color, pygame.Rect(pt.x, pt.y, self.settings.block_size, self.settings.block_size))
            pygame.draw.rect(self.display, self.settings.snake_color, pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, self.settings.food_color, pygame.Rect(self.food.x, self.food.y, self.settings.block_size, self.settings.block_size))

        text = self.settings.font1.render("Score: " + str(self.score), True, self.settings.white)
        self.display.blit(text, [10, 10])
        pygame.display.flip()

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += self.settings.block_size
        elif self.direction == Direction.LEFT:
            x -= self.settings.block_size
        elif self.direction == Direction.DOWN:
            y += self.settings.block_size
        elif self.direction == Direction.UP:
            y -= self.settings.block_size

        self.head = Point(x, y)