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

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    c = 0
    a = []
    while values:
        a.append([])
        for i in range(0, n):
            a[c].append(values.pop(0))
        c += 1
    return a


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    r, c = pos
    return values[r]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    a = []
    r, c = pos
    for i in range(len(values[0])):
        a.append(values[i][c])
    return a


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
    a = []
    n = round(math.sqrt(len(values[0])))
    r, c = pos
    for i in range(((r // n) * n), ((r // n) * n + n)):
        for j in range(((c // n) * n), ((c // n) * n + n)):
            a.append(values[i][j])
    return a


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
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == '.':
                pos = i, j
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
    r, c = pos
    grid[r][c] = '.'
    ans = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    a = get_block(grid, pos)
    ans = fpv_chk(a, ans)
    a = get_col(grid, pos)
    ans = fpv_chk(a, ans)
    a = get_row(grid, pos)
    ans = fpv_chk(a, ans)
    a = []
    for i in range(9):
        if ans[i] == 1:
            a.append(chr(i + 49))
    return a


def fpv_chk(a, ans):
    for i in range(len(a)):
        if a[i] != '.':
            ans[ord(a[i]) - 49] = 0
    return ans


def solve(grid):
    """ Решение пазла, заданного в grid
        Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(solve(grid))
    True
    """
    if check_solution(grid):
        return grid
    pos = find_empty_positions(grid)
    if not pos:
        return False
    a = find_possible_values(grid, pos)
    if not a:
        #print('beep')
        return False
    r, c = pos
    #print(a)
    while a:
        grid[r][c] = a.pop(0)
        #display(grid)
        grid_c = copy.deepcopy(grid)
        grid_s = solve(grid_c)
        if grid_s:
            return grid_s
    return False


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    num = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}
    for i in range(9):
        for j in range(9):
            pos = i, j
            if set(get_block(solution, pos)) != num:
                return False
            if set(get_row(solution, pos)) != num:
                return False
            if set(get_col(solution, pos)) != num:
                return False
    return True
    pass


def generate_sudoku(n):
    """ Генерация судоку заполненного на N элементов
    >>> check_solution(solve(generate_sudoku(45)))
    True
    """
    grid = rand_solve(read_sudoku('puzzle_empty.txt'))
    for i in range(81 - n):
        r = random.randrange(9)
        c = random.randrange(9)
        grid[r][c] = '.'
    return grid


def rand_solve(grid):
    """ Функция solve(), использующая случайное подходящее значение вместо наименьшего при их переборе
    Необходима для генерации судоку
    >>> grid = read_sudoku('puzzle1.txt')
    >>> check_solution(solve(grid))
    True
    """
    if check_solution(grid):
        return grid
    pos = find_empty_positions(grid)
    if not pos:
        return False
    a = find_possible_values(grid, pos)
    if not a:
        return False
    r, c = pos
    while a:
        grid[r][c] = a.pop(random.randrange(len(a)))
        grid_c = copy.deepcopy(grid)
        grid_s = solve(grid_c)
        if grid_s:
            return grid_s
    return False


if __name__ == '__main__':
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        display(solution)
