import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=20, speed=2):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        # Создание списка клеток
        self.clist = CellList(self.cell_width, self.cell_height, True)

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list()
            self.clist.update()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self):
        for row in range(self.clist.nrows):
            for col in range(self.clist.ncols):
                a = row * self.cell_size + 1
                b = col * self.cell_size + 1
                c = self.cell_size - 1
                d = self.cell_size - 1
                if self.clist.grid[row][col].is_alive():
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                        a, b, c, d))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (
                        a, b, c, d))


class Cell:

    def __init__(self, row, col, state=0):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.row = 0
        self.col = -1
        if randomize:
            self.grid = [[Cell(i, j, random.randint(0, 1)) for i in range(self.ncols)] for j in range(self.nrows)]
        else:
            self.grid = [[Cell(i, j, 0) for i in range(self.ncols)] for j in range(self.nrows)]

    def get_neighbours(self, cell):
        row = cell.row
        col = cell.col
        neighbours = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i or j:
                     if (0 <= row + i < self.nrows) and (0 <= col + j < self.ncols):
                         neighbours.append(self.grid[(row + i) % self.nrows][(col + j) % self.ncols])
        return neighbours

    def update(self):
        new_clist = []
        for row in range(self.nrows):
            new_clist.append([])
            for col in range(self.ncols):
                if ((1 < sum(c.state for c in self.get_neighbours(Cell(row, col))) < 4 and self.grid[row][col].is_alive())
                or (sum(c.state for c in self.get_neighbours(Cell(row, col))) == 3 and not self.grid[row][col].is_alive())):
                    new_clist[row].append(Cell(row, col, 1))
                else:
                    new_clist[row].append(Cell(row, col, 0))
        #new_clist.pop(0)
        self.grid = new_clist
        return self

    def __iter__(self):
        return self

    def __next__(self):
        if self.col == self.ncols-1:
            self.col = -1
            self.row += 1
        self.col += 1
        if self.row == self.nrows:
            self.row = 0
            self.col = -1
            raise StopIteration
        return self.grid[self.row][self.col]

    def __str__(self):
        s = ''
        for row in range(self.nrows):
            for col in range(self.ncols):
                if self.grid[row][col].is_alive():
                    s += '1 '
                else:
                    s += '0 '
            s += '\n'
        return s

    @classmethod
    def from_file(cls, filename):
        grid = []
        with open(filename) as file:
            for j, line in enumerate(file):
                grid.append([Cell(i, j, int(c)) for i, c in enumerate(line) if c != '\n'])
        clist = cls(len(grid), len(grid[0]), False)
        clist.grid = grid
        return clist


if __name__ == '__main__':
    #clist = CellList.from_file('grid.txt')
    #print([cell.state for cell in clist])

    clist = CellList.from_file('grid.txt')
    print(clist)
    for i in range(7):
        clist.update()
        c = 0
        row = []
        states = []                 #copied from test_can_update()
        for cell in clist:
            row.append(int(cell.is_alive()))
            c += 1
            if c % clist.ncols == 0:
                states.append(row)
                row = []
        print(i+1, states)
    #game = GameOfLife()
    #game.run()