from graphviz import Digraph  # type: ignore
from Aho_Corasick import Trie


class TrieVisualizer:
    def __init__(self, trie):
        self.trie = trie
        self.graph = Digraph(comment="Trie Visualization", format="png")
        self.graph.attr(rankdir="LR")

    def _add_node(self, node, parent_name=None):
        node_name = f"{node.name}_{id(node)}"

        if node.terminate:
            self.graph.node(
                node_name,
                label=node.name,
                color="green",
                style="filled",
                fillcolor="lightgreen",
            )
        else:
            self.graph.node(node_name, label=node.name)

        if parent_name:
            self.graph.edge(parent_name, node_name)

        if node.suffix_link and node.suffix_link != self.trie.root:
            suffix_name = f"{node.suffix_link.name}_{id(node.suffix_link)}"
            self.graph.edge(
                node_name, suffix_name, style="dashed", color="blue", label="suffix"
            )

        if node.terminal_link and node.terminal_link != self.trie.root:
            terminal_link_name = f"{node.terminal_link.name}_{id(node.terminal_link)}"
            self.graph.edge(
                node_name, terminal_link_name, style="dashed", color="red", label="term"
            )

        for child in node.children.values():
            self._add_node(child, node_name)

    def visualize(self, filename="trie"):
        self._add_node(self.trie.root)
        self.graph.render(filename, cleanup=True)
        print(f"Дерево сохранено в файл {filename}.png")


patterns = {"her": 1, "she": 2, "his": 3, "is": 4, "i": 5, "he": 6}
trie = Trie(patterns)
visualizer = TrieVisualizer(trie)
visualizer.visualize(filename="images/trie_visualization")
