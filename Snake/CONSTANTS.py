import pygame
pygame.init()

class Directions():
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    UP = 4
    clock_wise = [RIGHT, DOWN, LEFT, UP]

BACKGROUND = ( 22,  22,  22)
SNAKECOLOR = (  0, 150,   0)
FOOD_COLOR = (241,   9,  22)
SCORECOLOR = (255, 255, 255)

FONT = pygame.font.SysFont('arial', 25)

GAME_WIDTH = 1760
GAME_HEIGHT = 880
GAME_SPEED = 30
BLOCK_SIZE = 40
BORDER_WIDTH = 3
DEFAULT_LEN = 3