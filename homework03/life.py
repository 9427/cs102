import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
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

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.clist)
            self.clist = self.update_cell_list(self.clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        if randomize:
            self.clist = [[random.randrange(2) for i in range(self.width // self.cell_size)] for j in range(self.height // self.cell_size)]
            return self.clist
        else:
            return [[0 for i in range(self.width // self.cell_size)] for j in range(self.height // self.cell_size)]


    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for row in range(len(clist)):
            for col in range(len(clist[0])):
                if clist[row][col] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (self.cell_size * col + 1, self.cell_size * row + 1, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (self.cell_size * col + 1, self.cell_size * row + 1, self.cell_size - 1, self.cell_size - 1))



    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (0 <= row + i < self.height // self.cell_size) and (0 <= col + j < self.width // self.cell_size) and (i or j):
                    neighbours.append(self.clist[row + i][col + j])
        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = [[]]
        old_clist = cell_list.copy()
        for col in range(len(old_clist)):
            for row in range(len(old_clist[0])):
                if old_clist[col][row] == 1:
                    if 1 < self.get_neighbours((col, row)).count(1) < 4:
                        new_clist[col].append(1)
                    else:
                        new_clist[col].append(0)
                elif self.get_neighbours((col, row)).count(1) == 3:
                    new_clist[col].append(1)
                else:
                    new_clist[col].append(0)
            new_clist.append([])
        new_clist.pop(len(new_clist)-1)
        return new_clist


if __name__ == '__main__':
    life = GameOfLife()
    life.run()