from .colors import *

import random

class Apple:
    def __init__(self, snake, rows, cols):
        self.snake = snake
        self.x = random.randrange(0, rows)
        self.y = random.randrange(0, cols)
        while(self.snake.isAppleOnSnake(self)):
            self.x = random.randrange(0, rows)
            self.y = random.randrange(0, cols)
        print(snake, self)

    def isAtPosition(self, x, y):
        return self.x == x and self.y == y

    def getDisplay(self):
        return [
            self.y*self.snake.game.blockSize + self.snake.game.outlineLength,
            self.x*self.snake.game.blockSize + self.snake.game.outlineLength, 
            self.snake.game.blockSize - self.snake.game.outlineLength*2,
            self.snake.game.blockSize - self.snake.game.outlineLength*2
        ]
