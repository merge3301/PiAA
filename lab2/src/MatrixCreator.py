import math
import random


class MatrixCreator:
    def load_matrix(self, filename: str):
        f = open(filename)
        matrix = []
        for line in f:
            tmp = line.split(" ")
            res = []
            for x in tmp:
                try:
                    res.append(int(x))
                except ValueError:
                    res.append(math.inf)
            matrix.append(res)
        f.close()
        return matrix

    def generate_matrix(self, sym: bool, size: int, min_val: int, max_val: int):
        matrix = [[0 for j in range(size)] for i in range(size)]
        if sym:
            for i in range(size):
                for j in range(i, size):
                    a = random.randint(min_val, max_val)
                    matrix[i][j] = a
                    matrix[j][i] = a
                    if i == j:
                        matrix[i][j] = math.inf
        else:
            for i in range(size):
                for j in range(size):
                    a = random.randint(min_val, max_val)
                    matrix[i][j] = a
                    if i == j:
                        matrix[i][j] = math.inf
        return matrix

    def generate_euclidean_matrix(
        self, size: int, dimensions: int = 2, min_val: int = 0, max_val: int = 10
    ):
        # Генерация случайных точек в n-мерном пространстве
        points = [
            [random.randint(min_val, max_val) for _ in range(dimensions)]
            for _ in range(size)
        ]

        # Создание матрицы расстояний
        matrix = [[0 for _ in range(size)] for _ in range(size)]

        for i in range(size):
            for j in range(size):
                if i == j:
                    matrix[i][j] = math.inf
                else:
                    # Вычисление евклидова расстояния между точками i и j
                    distance = math.sqrt(
                        sum(
                            (points[i][k] - points[j][k]) ** 2
                            for k in range(dimensions)
                        )
                    )
                    matrix[i][j] = int(distance)
                    matrix[j][i] = int(distance)

        return matrix

    def save_matrix(self, matrix: list[list], filename: str):
        f = open(filename, "w")
        for elem in matrix:
            string = " ".join([str(x) for x in elem])
            f.write(string + "\n")
        f.close()
