from algorithm.Astar import Find_Astar_Path
from CONSTANTS import *
from collections import namedtuple
import random
import pygame
pygame.init()


Point = namedtuple("Point", ["x", "y", "neighbors"])


class Node:
    def __init__(self, x:int, y:int, tot_rows:int, tot_cols:int):
        self.x = x
        self.y = y
        self.tot_rows = tot_rows
        self.tot_cols = tot_cols
        self.neighbors = []

    def get_pos(self):
        return self.x, self.y

    def update_neighbors(self, grid:list):
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y])
        if self.x < self.tot_rows - 1:
            self.neighbors.append(grid[self.x+1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1])
        if self.y < self.tot_cols - 1:
            self.neighbors.append(grid[self.x][self.y+1])

    def __lt__(self, other):
        return False


class MAP:
    def __init__(self, rows:int, cols:int):
        self.rows = rows
        self.cols = cols
        self.map = []
        self.snake = None
        self.food = None

        for i in range(rows):
            self.map.append([])
            for j in range(cols):
                self.map[-1].append(Point(i, j, []))
        for i in range(rows):
            for j in range(cols):
                if i > 0:
                    self.map[i][j].neighbors.append(self.map[i-1][j])
                if i < rows - 1:
                    self.map[i][j].neighbors.append(self.map[i+1][j])
                if j > 0:
                    self.map[i][j].neighbors.append(self.map[i][j-1])
                if j < cols - 1:
                    self.map[i][j].neighbors.append(self.map[i][j+1])

    def copy(self, flat:bool):
        result = []
        for row in self.map:
            if flat:
                result.extend(row[:])
            else:
                result.append(row[:])
        return result

    def get_grid(self):
        result = []
        for i in range(self.rows):
            result.append([Node(i, j, self.rows, self.cols) for j in range(self.cols)])
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j].update_neighbors(result)
        return result

    def set_food(self, x:int, y:int):
        self.food = self.map[x][y]


class SnakeGame():
    def __init__(self, w, h, dlen):
        self.w = w
        self.h = h
        self.r = h//BLOCK_SIZE
        self.c = w//BLOCK_SIZE
        self.dlen = dlen

        self.window = pygame.display.set_mode((self.w, self.h))
        self.FPS = pygame.time.Clock().tick
        self.reset()


    def reset(self):
        self.direction = Directions.RIGHT

        self.map = MAP(self.r, self.c)

        self.head = self.map.map[self.r//2][self.c//2]
        self.snake = [
            self.head
        ] + [
            self.map.map[
                self.head.x-i
            ][self.head.y] for i in range(1, self.dlen)
        ]

        self.frame = 0
        self.score = 0

        self.place_apple()

        self.update_path()


    def place_apple(self):
        pts = [pt for pt in self.map.copy(flat=True) if pt not in self.snake]
        while(self.map.food in self.snake or not self.map.food):
            apple = pts.pop(random.randrange(0, len(pts)))
            self.map.set_food(apple.x, apple.y)


    def update(self):
        self.frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_over = self.update_snake()

        self.draw()
        self.FPS(GAME_SPEED)
        return game_over
    

    def update_snake(self):
        if self.path:
            next_step = self.path.pop(0)
            self.head = self.map.map[next_step.x][next_step.y]
            self.snake.insert(0, self.head)

            if self.check_collision() or self.frame > 100*len(self.snake):
                return True

            if self.head == self.map.food:
                self.score += 1
                self.place_apple()
            else:
                self.snake.pop()
                self.update_path()

            if not self.path:
                print("NewPath")
                self.update_path()
            return False
        else:
            print("No Path Dead!!!!!!!!")
            return True


    def update_path(self):
        grid = self.map.get_grid()
        self.path = Find_Astar_Path(
            grid,
            [grid[p.x][p.y] for p in self.snake],
            grid[self.head.x][self.head.y],
            grid[self.map.food.x][self.map.food.y]
        )


    def check_collision(self):
        if self.head in self.snake[1:]:
            return True
        elif self.head.x > self.r-1 or self.head.x < 0:
            return True
        elif self.head.y > self.c-1 or self.head.y < 0:
            return True
        return False


    def draw(self):
        self.window.fill(BACKGROUND)

        for p in self.snake:
            pygame.draw.rect(
                self.window,
                SNAKECOLOR,
                pygame.Rect(
                    (p.y*BLOCK_SIZE)+BORDER_WIDTH,
                    (p.x*BLOCK_SIZE)+BORDER_WIDTH,
                    BLOCK_SIZE-(BORDER_WIDTH*2),
                    BLOCK_SIZE-(BORDER_WIDTH*2)
                )
            )

        pygame.draw.rect(
            self.window,
            FOOD_COLOR,
            pygame.Rect(
                (self.map.food.y*BLOCK_SIZE)+BORDER_WIDTH,
                (self.map.food.x*BLOCK_SIZE)+BORDER_WIDTH,
                BLOCK_SIZE-(BORDER_WIDTH*2),
                BLOCK_SIZE-(BORDER_WIDTH*2)
            )
        )

        self.window.blit(
            FONT.render(
                f"Score: {self.score}",
                True,
                SCORECOLOR
            ),
            (0, 0)
        )

        pygame.display.update()







Game = SnakeGame(GAME_WIDTH, GAME_HEIGHT, DEFAULT_LEN)
held = False
g = 0
while(True):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            break

    if Game.path:
        Game_Over = Game.update()
        if Game_Over:
            g+=1
            print(f"Game {g}: Dead")
            print(Game.score)
            print("\n\n")
            Game.reset()









