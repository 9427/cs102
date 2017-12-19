"""
Требуется найти выход из лабиринта с помощью алгоритма поиска в глубину.
Лабиринт задается в текстовом файле следующего вида:
S X _ X
_ _ _ _
_ X _ X
_ X G X

Где:
    - "S" означает вход в лабиринт;
    - "X" стену;
    - "G" выход из лабиринта;
    - "_" возможный ход.
"""

"""
Задание 1: Напишите функцию чтения лабиринта из файла. Лабиринт должен быть
представлен списком списков, например:

>>> maze = read_maze('maze.txt')
>>> maze
[['S', 'X', '_', 'X'], ['_', '_', '_', '_'], ['_', 'X', '_', 'X'], ['_', 'X', 'G', 'X']]
"""


def read_maze(filename):
    """ Прочитать лабиринт из файла """
    grid = []
    with open(filename) as file:
        for i, line in enumerate(file):
            grid.append([c for j, c in enumerate(line) if c in 'SXG_'])
    return grid


"""
Задание 2. Напишите функцию отображения лабиринта:
>>> print_maze(maze)
S X _ X
_ _ _ _
_ X _ X
_ X G X
"""


def print_maze(maze):
    """ Отрисовать лабиринт """
    s = ''
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            s += maze[row][col]
            s += ' '
        s += '\n'
    print(s)
    pass


"""
Задание 3. Допишите представленный ниже класс опираясь на следующий пример
поведения класса:

# Пример создания графа
g = Graph()

# Добавляем вершины
g.add_vertex('1')
g.add_vertex('2')
g.add_vertex('3')
g.add_vertex('4')

# Добавляем ребра
g.add_edge(('1', '2'))
g.add_edge(('2', '1'))
g.add_edge(('1', '3'))
g.add_edge(('3', '1'))
g.add_edge(('2', '3'))
g.add_edge(('3', '2'))
g.add_edge(('3', '4'))
g.add_edge(('4', '3'))

# Выводим граф
g.graph
{'1': ['2', '3'], '2': ['1', '3'], '3': ['1', '2', '4'], '4': ['3']}
"""


class Graph:

    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        """ Добавить новую вершину vertex в граф """
        self.graph[vertex] = []
        return self

    def add_edge(self, edge):
        """ Добавить новое ребро edge в граф """
        vertex1, vertex2 = edge
        self.graph[vertex1].append(vertex2)
        return self


"""
Лабиринт можно представить в виде графа, например, исходный лабиринт:
S X _ X
_ _ _ _
_ X _ X
_ X G X

Соответствующий граф:
(0,0)           (0,2)
  |               |
(1,0) - (1,1) - (1,2) - (1,3)
  |               |
(2,0)           (2,2)
  |               |
(3,0)           (3,2)

Как такой граф получить? Можно создать его руками:

# Создаем пустой граф
>>> g = Graph()

# Добавляем вершины
>>> g.add_vertex((0,0))
>>> g.add_vertex((1,0))
>>> g.add_vertex((2,0))
>>> g.add_vertex((3,0))
...

>>> # Создаем связи (ребра)
>>> g.add_edge(((0,0), (1,0))
>>> g.add_edge(((1,0), (0,0))
...

>>> g.graph
{(0, 0): [(1, 0)],
 (0, 2): [(1, 2)],
 (1, 0): [(0, 0), (2, 0), (1, 1)],
 (1, 1): [(1, 0), (1, 2)],
 (1, 2): [(0, 2), (2, 2), (1, 1), (1, 3)],
 (1, 3): [(1, 2)],
 (2, 0): [(1, 0), (3, 0)],
 (2, 2): [(1, 2), (3, 2)],
 (3, 0): [(2, 0)],
 (3, 2): [(2, 2)]}

Процедура довольно долгая, да и лабиринты разные могут быть.
Задание 4. Напишите функцию, которая создает граф из лабиринта и возвращает
вход и выход из лабиринта
"""


def maze2graph(maze):
    """ Преобразовать лабиринт в граф """
    g = Graph()
    start = end = None
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] != 'X':
                if maze[row][col] == 'S':
                    start = (row, col)
                if maze[row][col] == 'G':
                    end = (row, col)
                g.add_vertex((row, col))
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if (row, col) in g.graph.keys():
                if (row - 1, col) in g.graph.keys():
                    g.add_edge(((row, col), (row - 1, col)))
                if (row + 1, col) in g.graph.keys():
                    g.add_edge(((row, col), (row + 1, col)))
                if (row, col - 1) in g.graph.keys():
                    g.add_edge(((row, col), (row, col - 1)))
                if (row, col + 1) in g.graph.keys():
                    g.add_edge(((row, col), (row, col + 1)))
    return g, start, end


"""
Найти выход из лабиринта можно по следующему алгоритму, который называется 
алгоритмом поиска в глубину (DFS):

1. Если текущая позиция является выходом из лабиринта, то вернуть ее
2. Иначе отметить текующую позицию как посещенную
3. Создать список всех возможных следующих позиций (где мы еще не были?)
4. Для каждой возможной позиции вызвать DFS
    - Если DFS вернул путь до выхода, то добавить текущую позицию к пути и вернуть новый путь
5. Если нет пути до выхода, то вернуть None

Пример. Начинаем искать выход из следующего лабиринта:

S X _ X
_ _ _ _
_ X _ X
_ X G X

Так как находимся в позиции (0, 0) и она не является выходом, то помечаем ее 
как посещенную и генерируем список возможных путей из нее, а это лишь одна 
позиция (1, 0). Тогда:

possible_paths = [(1, 0)]

Для возможных позиций вызываем DFS, оказываемся на позиции (1, 0):

V X _ X
S _ _ _
_ X _ X
_ X G X

Символом V обозначена позиция, в которой мы уже побывали, а S текущая. 
Итак, (1, 0) не является выходом из лабиринта, а следовательно генерируем 
список возможных позиций:

possible_paths = [(2, 0), (1, 1)]

Проходим по каждому из них.

1) Идем по пути (2, 0). 

V X _ X
V _ _ _
S X _ X
_ X G X

Так как он не явлется выходом из лабиринта, то снова генерируем список 
возможных путей, обратите внимание еще раз, что мы не включаем в возможные 
позиции те, в которых мы уже побывали (т.е. те, которые отмечены символом V):

possible_paths = [(3, 0)]

Проходимся по возможным путям и попадаем в (3, 0):

V X _ X
V _ _ _
V X _ X
S X G X

Текущая позиция не явлется выходом из лабиринта, генерируем список возможных 
путей. Этот список окажется пуст, так как мы не нашли выхода возвращаем None.

2) Идем по пути (1, 1)

V X _ X
V S _ _
V X _ X
V X G X

Так как этот путь не является выходом из лабиринта, то генерируем список 
возможных путей:

possible_paths = [(1, 2)]

Я думаю идея должна быть ясна, поэтому перейду к самому концу. В какой момент 
мы будем находится на позиции (2, 2):

V X _ X
V V V _
V X S X
V X G X

Генерируем возможные пути:

possible_paths = [(3, 2)]

И проходим по ним: 

V X _ X
V V V _
V X V X
V X S X

Оказываемся в позиции (3, 2), которая является выходом из лабиринта. 
Возвращаем ее, формируя путь от начала к концу лабиринта:

new_path = [(2, 2)] + [(3, 2)] # где (2,2) это текущая(!) позиция, а (3,2) 
позиция, которую нам только что вернули

В итоге получим такую цепочку "ретурнов":

new_path = [(1, 2)] + [(2, 2), (3, 2)]
new_path = [(1, 1)] + [(1, 2), (2, 2), (3, 2)]
new_path = [(1, 0)] + [(1, 1), (1, 2), (2, 2), (3, 2)]

И самый последний, который содержит выход из лабиринта:

new_path = [(0, 0)] + [(1, 0), (1, 1), (1, 2), (2, 2), (3, 2)]

Задание 5. Напишите функцию поиска всех путей в лабиринте между указанными
точками.
"""

'''
def dfs_paths(g, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for v_next in g.graph[vertex]:
            if v_next not in path:
                if v_next == goal:
                    return path + [v_next]
                else:
                    stack.append((v_next, path + [v_next]))



def dfs1_paths(g, start, end, path=None):
    if not path:
        path = []
    path = path + [start]
    if start == end:
        return path
    if not g.graph[start]:
        return None
    for possible_path in g.graph[start]:
        if possible_path not in path:
            new_path = dfs_paths(g, possible_path, end, path)
            if new_path:
                return new_path
    return None


def dfs2_paths(g, start, end, path=None):
    if not path:
        path = []
    path = path + [start]
    if start == end:
        return path
    if not g.graph[start]:
        return None
    for possible_path in g.graph[start]:
        if possible_path not in path:
            new_path = dfs_paths(g, possible_path, end, path)
            if new_path:
                return new_path
    return None
'''


def dfs_paths(g, start, goal):
    stack = [(start, [start])]
    path_list = []
    while stack:
        (vertex, path) = stack.pop()
        for v_next in g.graph[vertex]:
            if v_next not in path:
                if v_next == goal:
                    path_list.append(path + [v_next])
                else:
                    stack.append((v_next, path + [v_next]))
    return path_list


if __name__ == '__main__':
    # 1
    print(read_maze('maze.txt'))
    # 2
    print_maze(read_maze('maze.txt'))
    # 5
    print(dfs_paths(*maze2graph(read_maze('maze.txt'))))
