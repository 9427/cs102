import copy
import math
import random


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    """
    return [[values[i + j * n] for i in range(n)] for j in range(n)]


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row, col = pos
    return values[row]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    row, col = pos
    return [values[i][col] for i in range(len(values[0]))]


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos
    >>> get_block([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['8', '7', '6', '5'], ['4', '3', '2', '1']], (1,1))
    ['1', '2', '5', '6']
    >>> get_block([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['8', '7', '6', '5'], ['4', '3', '2', '1']], (1,2))
    ['3', '4', '7', '8']
    >>> get_block([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['8', '7', '6', '5'], ['4', '3', '2', '1']], (3,1))
    ['8', '7', '4', '3']
    >>> get_block([['1', '2', '3', '4'], ['5', '6', '7', '8'], ['8', '7', '6', '5'], ['4', '3', '2', '1']], (3,3))
    ['6', '5', '2', '1']
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    root = round(math.sqrt(len(values[0])))
    row, col = pos
    return [values[i][j] for i in range(((row // root) * root), ((row // root) * root + root)) for j in range(((col // root) * root), ((col // root) * root + root))]


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']])
    False
    """
    pos = False
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == '.':
                pos = row, col
                return pos
    return pos


def find_possible_values(grid, pos):
    """ Вернуть все возможные значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> set(values) == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> set(values) == {'2', '5', '9'}
    True
    """
    values = set('123456789') - set(get_col(grid, pos)) - set(get_block(grid, pos)) - set(get_row(grid, pos))
    return list(values)


def solve(grid):
    """ Решение пазла, заданного в grid
    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(solve(grid))
    True
    """
    if check_solution(grid):
        return grid
    pos = find_empty_positions(grid)
    if not pos:
        return False
    values = find_possible_values(grid, pos)
    if not values:
        return False
    row, col = pos
    while values:
        grid[row][col] = values.pop(0)
        grid_solved = solve(grid)
        if grid_solved:
            return grid
        grid[row][col] = '.'
    return False


def check_solution(grid):
    """ Если решение grid верно, то вернуть True, в противном случае False """
    num = set('123456789')
    for row in range(9):
        for col in range(9):
            pos = row, col
            if set(get_block(grid, pos)) != num:
                return False
            if set(get_row(grid, pos)) != num:
                return False
            if set(get_col(grid, pos)) != num:
                return False
    return True


def generate_sudoku(n):
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = rand_solve([['.'] * 9 for i in range(9)])
    for i in range(81 - n):
        row = random.randrange(9)
        col = random.randrange(9)
        while grid[row][col] == '.':
            row = random.randrange(9)
            col = random.randrange(9)
        grid[row][col] = '.'
    return grid


def rand_solve(grid):
    """ Функция solve(), использующая случайное подходящее значение вместо наименьшего при их переборе
    Необходима для генерации судоку

    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(rand_solve(grid))
    True
    """
    if check_solution(grid):
        return grid
    pos = find_empty_positions(grid)
    if not pos:
        return False
    values = find_possible_values(grid, pos)
    if not values:
        return False
    row, col = pos
    while values:
        grid[row][col] = values.pop(random.randrange(len(values)))
        grid_solved = solve(grid)
        if grid_solved:
            return grid
        grid[row][col] = '.'
    return False


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        puzzle = read_sudoku(fname)
        display(puzzle)
        solution = solve(puzzle)
        display(solution)
