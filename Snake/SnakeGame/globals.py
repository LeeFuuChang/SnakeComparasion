from collections import namedtuple

INF = 10e9

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
