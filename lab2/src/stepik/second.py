import copy
from math import inf
import sys


class ADO_MOD_algorithm:
    def __init__(self, matrix) -> None:
        self.src_matrix = copy.deepcopy(matrix)
        self.matrix = matrix
        self.ost = []

    def read_input(self):
        data = sys.stdin.read().strip().splitlines()
        if not data:
            return None, None
        start = int(data[0])
        matrix = [list(map(float, line.split())) for line in data[1:] if line.strip()]
        return start, matrix

    def prim(self, start) -> None:
        n = len(self.matrix)
        in_mst = [False] * n
        key = [inf] * n
        parent = [-1] * n
        key[start] = 0.0

        for _ in range(n):
            u = min(
                (i for i in range(n) if not in_mst[i]), key=lambda i: key[i], default=-1
            )
            if u == -1:
                break
            in_mst[u] = True
            for v in range(n):
                if (
                    not in_mst[v]
                    and self.matrix[u][v] != -1
                    and self.matrix[u][v] < key[v]
                ):
                    key[v], parent[v] = self.matrix[u][v], u
        return parent

    def build_mst(self, parent):
        adj = {i: [] for i in range(len(parent))}
        for v, u in enumerate(parent):
            if u != -1:
                adj[u].append(v)
                adj[v].append(u)
        return adj

    def dfs(self, u, adj, visited, path):
        visited.add(u)
        path.append(u)
        for v in sorted(
            (v for v in adj[u] if v not in visited), key=lambda v: self.matrix[u][v]
        ):
            self.dfs(v, adj, visited, path)

    def answer(self, tour):
        return sum(self.src_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))

    def find_res(self):
        start, matrix = self.read_input()
        if start is None or matrix is None:
            return

        self.matrix = matrix
        self.src_matrix = copy.deepcopy(matrix)

        parent = self.prim(start)
        adj = self.build_mst(parent)
        visited = set()
        path = []
        self.dfs(start, adj, visited, path)
        tour = path + [start]

        print(f"{self.answer(tour):.2f}\n{' '.join(map(str, tour))}")


if __name__ == "__main__":
    solution = ADO_MOD_algorithm([])
    solution.find_res()
