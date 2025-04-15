import copy
from math import inf
import math


class MatrixHandler:
    def __init__(self, matrix: list[list]) -> None:
        self.matrix = matrix

    def __len__(self) -> int:
        return len(self.matrix)

    def __getitem__(self, index: int) -> None:
        if 0 <= index < len(self.matrix):
            return self.matrix[index]
        else:
            raise IndexError("Index out of range")

    def print_matrix(self) -> None:
        for row in self.matrix:
            print(row)

    def min_except(self, lst: int, idx: int) -> list:
        return min([x for i, x in enumerate(lst) if i != idx])

    def reduct(self) -> int:
        d = 0
        # Редукция строк
        for i, row in enumerate(self.matrix):
            min_row = min(row)
            if min_row == math.inf:
                return -1
            # вычитаем из всех элементов строки минимальный
            self.matrix[i] = [elem - min_row for elem in row]
            # добавляем к стоимости d
            d += min_row

        # Редукция столбцов
        for i in range(len(self.matrix)):
            min_column = min([row[i] for row in self.matrix])
            if min_column == math.inf:
                return -1
            for row in self.matrix:
                # вычитаем из всех элементов столбца минимальный
                row[i] -= min_column
            # добавляем к стоимости d
            d += min_column
        return d

    def find_heavy_zero(self) -> int:
        d_max = 0
        res = None
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                if self.matrix[i][j] == 0:
                    # находим сумму минимальных элементов
                    tmp = self.min_except(self.matrix[i], j) + self.min_except(
                        [row[j] for row in self.matrix], i
                    )
                    # если найденная сумма больше рекорда, перезаписываем рекорд и координаты тяжелого нуля
                    if tmp > d_max or not res:
                        d_max = tmp
                        res = (i, j)
        return res

    def find_longest_path(self, solution: dict, edge: tuple) -> list:
        start, end = edge
        path = []

        # Ищем путь в одну сторону
        current = start
        while current in solution.keys():
            path.append(solution[current])
            current = solution[current]

        # Ищем путь в другую сторону
        current = start
        path.insert(0, current)
        while current in solution.values():
            for key in solution.keys():
                if solution[key] == current:
                    current = key
            path.insert(0, current)

        return path

    def forbid_cycles(self, path: list, i_index: list, j_index: list) -> None:
        if len(path) < 2:
            return

        # Запрещаем ребро, которое замыкает цикл
        restore_i = path[-1]
        restore_j = path[0]
        if restore_i - 1 in i_index and restore_j - 1 in j_index:
            i_for_inf = i_index.index(restore_i - 1)
            j_for_inf = j_index.index(restore_j - 1)
            # запрещаем движение по обратному ребру
            self.matrix[i_for_inf][j_for_inf] = math.inf

    def delete_row_column(
        self, i: int, j: int, solution: dict, i_index: list, j_index: list
    ) -> None:
        # находим, каким вершинам графа соответствуют эти индексы
        restore_i = i_index[i]
        restore_j = j_index[j]
        # обновляем решение
        solution[restore_i + 1] = restore_j + 1
        path = self.find_longest_path(
            solution, (restore_i + 1, solution[restore_i + 1])
        )
        self.forbid_cycles(path, i_index, j_index)

        # Удаляем строку и столбец
        i_index.pop(i)
        j_index.pop(j)
        # удаляем строку
        self.matrix.pop(i)
        for row in self.matrix:
            # удаляем столбец
            row.pop(j)


class LittleAlgorithm:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.matrix_handler = MatrixHandler(matrix)
        self.best_solution = {}
        self.min_cost = inf
        self.tree_data = []

    def answer(self, start: int) -> list[int]:
        next_node = self.best_solution[start]
        res = [start]
        while next_node != start:
            res.append(next_node)
            next_node = self.best_solution[next_node]
        return res

    def handle2x2(
        self,
        tmp_solution: dict,
        current_cost: int,
        i_index: list[int],
        j_index: list[int],
    ) -> None:
        for i in range(len(self.matrix_handler)):
            for j in range(len(self.matrix_handler)):
                if self.matrix_handler[i][j] == inf:
                    # Вершина (i + 1) % 2 связывается с вершиной j (другая вершина в столбце).
                    tmp_solution[i_index[(i + 1) % 2] + 1] = j_index[j] + 1
                    # Вершина i связывается с вершиной (j + 1) % 2 (другая вершина в строке).
                    tmp_solution[i_index[i] + 1] = j_index[(j + 1) % 2] + 1
                    self.best_solution = tmp_solution
                    self.min_cost = current_cost

    def method_Little(
        self,
        matrix: list[list],
        tmp_solution: dict,
        cur_cost: int,
        i_index: list[int],
        j_index: list[int],
    ):
        self.matrix_handler.matrix = matrix
        step_cost = self.matrix_handler.reduct()
        if step_cost == -1:
            return

        current_cost = cur_cost + step_cost
        if current_cost >= self.min_cost:
            return

        if len(self.matrix_handler) == 2:
            self.handle2x2(tmp_solution, current_cost, i_index, j_index)
            return

        i, j = self.matrix_handler.find_heavy_zero()
        if i is None or j is None:
            return

        new_solution = tmp_solution.copy()
        left_matrix = copy.deepcopy(matrix)
        left_i_index = i_index[:]
        left_j_index = j_index[:]
        self.matrix_handler.matrix = left_matrix
        self.matrix_handler.delete_row_column(
            i, j, new_solution, left_i_index, left_j_index
        )
        self.method_Little(
            left_matrix, new_solution, current_cost, left_i_index, left_j_index
        )

        matrix[i][j] = inf
        self.method_Little(matrix, tmp_solution, current_cost, i_index[:], j_index[:])


if __name__ == "__main__":
    N = int(input())
    matrix = []
    for k in range(N):
        row = list(map(float, input().split()))
        matrix.append(row)

    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                matrix[i][j] = inf

    little_algo = LittleAlgorithm(matrix)
    i_index = [i for i in range(len(matrix))]
    j_index = [j for j in range(len(matrix))]
    little_algo.method_Little(matrix, {}, 0, i_index, j_index)
    x = little_algo.answer(1)
    x = [i - 1 for i in x]
    print(*x)
    print(float(little_algo.min_cost))
