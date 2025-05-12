import copy
from math import inf
from MatrixHandler import MatrixHandler


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

    def collect_tree_data(
        self,
        current_cost: int,
        parent_node: str,
        step_cost: float,
        i_index: list[int],
        j_index: list[int],
        branching_arc: tuple[int, int] = None,
    ) -> str:
        j_index_shifted = [j + 1 for j in j_index]
        header = "   | " + " | ".join(map(str, j_index_shifted)) + " |"
        matrix_rows = []
        for i, row in enumerate(self.matrix_handler.matrix):
            row_str = (
                f"{i_index[i]+1:2} | "
                + " | ".join(f"{'∞' if x == inf else x:2}" for x in row)
                + " |"
            )
            matrix_rows.append(row_str)

        # Объединяем все строки
        matrix_str = "\n".join([header] + matrix_rows)
        node_label = f"Matrix:\n{matrix_str}\nCost: {current_cost}"
        if branching_arc:
            node_label += f"\nBranching Arc: {branching_arc}"
        node_id = str(len(self.tree_data))
        self.tree_data.append(("node", node_id, node_label))
        if parent_node is not None:
            self.tree_data.append(("edge", parent_node, node_id, f"Cost: {step_cost}"))

        return node_id

    def handle2x2(
        self,
        tmp_solution: dict,
        current_cost: int,
        i_index: list[int],
        j_index: list[int],
    ):
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
        parent_node: str = None,
        branching_arc: tuple[int, int] = None,
    ):
        self.matrix_handler.matrix = matrix
        print("Матрица на текущем шаге")
        self.matrix_handler.print_matrix()
        step_cost = self.matrix_handler.reduct()
        print("Редуцированная матрица")
        self.matrix_handler.print_matrix()

        if step_cost == -1:
            return

        current_cost = cur_cost + step_cost
        node_id = self.collect_tree_data(
            current_cost, parent_node, step_cost, i_index, j_index, branching_arc
        )

        if current_cost >= self.min_cost:
            print(
                "Текущая стоимость пути уже не будет выгоднее чем рекорд, конец рекурсии",
                self.min_cost,
            )
            return

        if len(self.matrix_handler) == 2:
            print("Размерность матрицы = 2, конец этой ветки рекурсии")
            self.handle2x2(tmp_solution, current_cost, i_index, j_index)
            print("Найденное решение:", self.best_solution)
            return

        i, j = self.matrix_handler.find_heavy_zero()
        if i is None or j is None:
            return

        print("Начата левая ветвь:")
        new_solution = tmp_solution.copy()
        left_matrix = copy.deepcopy(matrix)
        left_i_index = i_index[:]
        left_j_index = j_index[:]
        self.matrix_handler.matrix = left_matrix
        self.matrix_handler.delete_row_column(
            i, j, new_solution, left_i_index, left_j_index
        )
        self.method_Little(
            left_matrix,
            new_solution,
            current_cost,
            left_i_index,
            left_j_index,
            node_id,
            branching_arc=(i_index[i] + 1, j_index[j] + 1),
        )

        print("Начата правая ветвь:")
        matrix[i][j] = inf
        self.method_Little(
            matrix,
            tmp_solution,
            current_cost,
            i_index[:],
            j_index[:],
            node_id,
            branching_arc=(i_index[i] + 1, j_index[j] + 1),
        )
