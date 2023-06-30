import pygame
from easy_json import get_value

class Settings():
    def __init__(self):

        # Initializing pygame
        pygame.init()

        # Dimensions
        self.window_width = 640
        self.window_height = 480

        self.header_width = 640
        self.header_height = 50

        # Colors
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0 , 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self.cyan = (0, 255, 255)
        self.magenta = (255, 0, 255)
        self.gray = (220, 220, 220)
        self.dark_gray = (51, 51, 51)

        self.available_themes = {
                                    "amazon": ["amazon.jpg","amazon.otf",(255,94,0),(0,118,20),(225,255,0)],
                                    "anime": ["anime.jpg","anime.TTF",(220, 220, 220),(247,128,239),(255,255,255)],
                                    "heaven": ["heaven.jpg","heaven.ttf",(219, 172, 52),(178,192,190),(219, 172, 52)], # (255,167,100)
                                    "hell": ["hell.jpg","hell.ttf",(0, 0, 0),(0,0,0),(225,255,0)], # (255,68,0)
                                    "mars": ["mars.jpg","mars.TTF",(255,255,255),(239,0,255),(255,255,255)],
                                    "myanmar": ["myanmar.jpg","myanmar.ttf",(255,255,255),(255,255,255),(255,255,255)],
                                    "pyramid": ["pyramid.jpg","pyramid.ttf",(192,119,25),(48,61,35),(255,162,0)],
                                    "stone_age": ["stone_age.jpg","stone_age.ttf",(0, 0, 0),(169,25,25),(162,233,144)], # 189,195,183
                                    "underwater": ["underwater.jpg","underwater.TTF",(0, 255, 255),(32,238,231),(245,135,237)]
                                }

        self.theme = self.available_themes[get_value('theme', 'data/settings.json')]

        self.snake_color = self.theme[3]
        self.food_color = self.theme[4]
        self.font_color = self.theme[2]

        font = "fonts/" + str(self.theme[1])

        # Fonts
        self.font0 = pygame.font.Font(font, 15)  # XS
        self.font1 = pygame.font.Font(font, 24)  # Small
        self.font2 = pygame.font.Font(font, 30)  # Medium
        self.font3 = pygame.font.Font(font, 70)  # Large
        self.font4 = pygame.font.Font(font, 85)  # XL

        self.score_font = pygame.font.Font(font, 45) # For score and others
        self.user_font = pygame.font.Font(font, 36) # for usernames

        self.copyright = pygame.font.Font(font, 20) # For copyright
        self.copyright.set_italic(True)

        self.best_player_font = pygame.font.Font(font, 40) # For best player
        self.other_players_font = pygame.font.Font(font, 30) # For other players

        # Define button dimensions
        self.button_width = 100
        self.button_height = 50

        # Images
        self.settings_icon = pygame.image.load("pictures/settings_icon.png")
        self.background = pygame.image.load("pictures/" + str(self.theme[0]))
        self.esc_icon = pygame.image.load("pictures/esc_icon.png")

        # Sizes
        self.block_size = 20