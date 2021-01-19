import pygame

pygame.init()

CELL_WIDTH = 250
CELL_HEIGHT = 50
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CELL_BACKGROUND_COLOR_HEADER = (208, 208, 207) #Same as background
CELL_BACKGROUND_COLOR_VALUE = (208, 208, 207) #Same as background
CELL_TEXT_COLOR_HEADER = (12, 114, 49) #Green
CELL_TEXT_COLOR_VALUE = (0, 0, 0) #Black
TEXT_MARGIN_LEFT = 5
HEADER_FONT = pygame.font.Font('./Sprites/Fonts/cell_value.ttf', 35)
VALUE_FONT = pygame.font.Font('./Sprites/Fonts/cell_value.ttf', 20)
POPUP_HEADER_FONT = pygame.font.Font('./Sprites/Fonts/popup_header.ttf', 30)
POPUP_CONTENT_FONT = pygame.font.Font('./Sprites/Fonts/popup_value.ttf', 20)
MARGIN_TOP = 25
MARGIN_LEFT = 25
TABLE_MARGIN = 75
VERTICAL_WHITESPACE = 10
HORIZONTAL_WHITESPACE = 10
BACKGROUND_COLOR = (227, 227, 225) #Gray
PLAYER_SPEED = 500  # how many pixels to move
STATISTIC_FONT = pygame.font.Font('./Sprites/Fonts/cell_value.ttf', 35)
STATISTIC_TEXT_COLOR = (0, 0, 0) #Black
STATISTIC_MARGIN = 10
LEVEL = "Levels/gamedata rws.json"