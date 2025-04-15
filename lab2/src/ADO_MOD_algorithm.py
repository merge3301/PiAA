import copy
from math import inf


class ADO_MOD_algorithm:
    def __init__(self, matrix: list[list[int]]) -> None:
        self.src_matrix = copy.deepcopy(matrix)
        self.matrix = matrix
        self.ost = []

    def prim(self, start: int) -> None:
        # будущее остовное дерево
        self.ost = [
            [0 for i in range(len(self.matrix))] for i in range(len(self.matrix))
        ]
        # вершины, уже включенные в дерево
        visited = [start]
        weight = []
        while len(visited) != len(self.matrix):
            for row in self.ost:
                print(row)
            print("Включенные вершины:", *[x + 1 for x in visited])
            min_w = inf
            i, j = 0, 0
            # проходим по всем вершинам остовного дерева
            for elem in visited:
                if min_w > min(self.matrix[elem]):
                    print(self.matrix[elem])
                    # находим самое легкое ребро
                    min_w = min(self.matrix[elem])
                    i = elem
                    j = self.matrix[elem].index(min_w)
                    print(
                        "Найдена новая вершина для добавления:",
                        j + 1,
                        " вес ребра = ",
                        min_w,
                    )
            if j not in visited:
                print(f"Добавляем ребро {i + 1} {j + 1} в МОД")
                weight.append(min_w)
                visited.append(j)
                self.ost[i][j] = min_w
                self.ost[j][i] = min_w
            self.matrix[i][j] = inf

    # поиск в глубину
    def dfs(self, matr: list[list[int]], start: int, res: list[int]) -> None:
        res.append(start)
        for i, elem in enumerate(matr[start]):
            if elem != 0 and i not in res:
                self.dfs(matr, i, res)

    def find_res(self, start: int) -> list[int]:
        start = start - 1
        self.prim(start)
        way = []
        print("Итоговое минимальное остовное дерево:")
        for row in self.ost:
            print(row)
        print("Запущен поиск в глубину")
        self.dfs(self.ost, start, way)

        # Подсчёт стоимости рёбер
        cost = 0
        for i in range(len(way) - 1):
            cost += self.src_matrix[way[i]][way[i + 1]]
        cost += self.src_matrix[way[-1]][way[0]]  # Замыкаем цикл

        print(
            "Полученный приближенный путь коммивояжера:",
            " - ".join(str(x + 1) for x in way),
        )
        print("Его стоимость:", cost)
        return [x + 1 for x in way]
