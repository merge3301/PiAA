from graphviz import Digraph  # type: ignore
from math import inf


class Visualiser:
    def visualise_graph(self, matrix, highlight_nodes=None):
        if highlight_nodes is None:
            highlight_nodes = []

        highlight_edges = []
        for i in range(len(highlight_nodes) - 1):
            highlight_edges.append((highlight_nodes[i], highlight_nodes[i + 1]))
        highlight_edges.append((highlight_nodes[-1], highlight_nodes[0]))

        dot = Digraph()
        dot.attr(size="15,15", bgcolor="lightblue")
        dot.attr()

        # Добавление вершин
        for i in range(len(matrix)):
            dot.node(str(i + 1), str(i + 1), style="filled", fillcolor="green")

        # Добавление рёбер
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != inf:
                    if (i + 1, j + 1) in highlight_edges:
                        dot.edge(
                            str(i + 1),
                            str(j + 1),
                            label=str(matrix[i][j]),
                            color="red",
                            penwidth="2.0",
                        )
                    else:
                        dot.edge(str(i + 1), str(j + 1), label=str(matrix[i][j]))
        dot.render("images/way", format="png", cleanup=True)

    def visualise_solution_tree(self, tree_data):
        graph = Digraph()
        graph.attr(size="50,50", bgcolor="lightblue")
        for item in tree_data:
            if item[0] == "node":
                _, node_id, label = item
                graph.node(node_id, label, style="filled", fillcolor="lightgreen")
            elif item[0] == "edge":
                _, from_node, to_node, label = item
                graph.edge(from_node, to_node, label)
        graph.render("images/tree", format="png", cleanup=True)
