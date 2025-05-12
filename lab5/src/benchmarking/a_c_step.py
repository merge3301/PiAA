from operator import itemgetter


class Node:
    def __init__(self, link=None, name="root"):
        self.parent = None
        self.children: dict[str, Node] = {}
        self.suffix_link = link
        self.terminal_link = None
        self.terminate = 0  # Номер шаблона, если узел терминальный
        self.name = name  # Имя узла (символ или "root")

    def __str__(self):
        return (
            f"Node name: {self.name};\n"
            f"Parent name: {self.parent.name if self.parent else None};\n"
            f"Children dict: {list(self.children.keys()) if self.children.keys() else None};\n"
            f"Suffix link: {self.suffix_link.name if self.suffix_link else None};\n"
            f"Terminate value: {True if self.terminate else False}."
        )


class Trie:
    def __init__(self, patterns: dict):
        self.root = Node()
        self.patterns = patterns
        self.terminate_patterns = dict(zip(patterns.values(), patterns.keys()))
        self._create_trie()
        self._create_suffix_links()
        self._create_terminal_links()

    # Создание дерева
    def _create_trie(self):
        list_patterns = list(self.patterns.keys())

        for pattern in list_patterns:
            node = self.root
            for symbol in pattern:
                if symbol not in node.children:
                    temp_node = Node(link=self.root, name=symbol)
                    node.children[symbol] = temp_node
                    temp_node.parent = node
                    node = temp_node
                else:
                    node = node.children[symbol]
            node.terminate = self.patterns[pattern]

    def _create_suffix_link_for_node(self, node):

        link = node.parent.suffix_link

        while link and (node.name not in link.children.keys()):
            link = link.suffix_link

        if link:
            node.suffix_link = link.children[node.name]
        else:
            node.suffix_link = self.root

    def _create_suffix_links(self):
        queue = []
        for child in self.root.children.values():
            child.suffix_link = self.root
            queue.append(child)

        while queue:
            cur_node = queue.pop(0)

            for child in cur_node.children.values():
                queue.append(child)
                self._create_suffix_link_for_node(child)

    def _create_terminal_links(self):
        queue = [x for x in self.root.children.values()]

        while queue:
            cur_node = queue.pop(0)
            temp = cur_node
            for child in cur_node.children.values():
                queue.append(child)

            while temp.name != "root":
                if temp.terminate and temp != cur_node:
                    cur_node.terminal_link = temp
                    break
                temp = temp.suffix_link

    def Aho_Korasik(self, text: str) -> list[str]:

        result = []
        node = self.root

        for index in range(len(text)):
            while node and (text[index] not in node.children.keys()):
                node = node.suffix_link

            if node:
                node = node.children[text[index]]
                temp = node

                while temp:
                    if temp.terminate:
                        result.append(
                            [
                                index
                                - len(self.terminate_patterns[temp.terminate])
                                + 2,
                                temp.terminate,
                            ]
                        )
                    temp = temp.terminal_link
            else:
                node = self.root

        result = sorted(result, key=itemgetter(0, 1))
        result = [" ".join(map(str, elem)) for elem in result]
        return result


def get_text() -> str:
    return input()


def get_patterns() -> dict:
    n = int(input())
    patterns: dict = {}

    for pattern_n in range(n):
        pattern = input()
        patterns[pattern] = pattern_n + 1
    return patterns


def main():
    text = get_text()
    patterns = get_patterns()
    trie = Trie(patterns)
    result = trie.Aho_Korasik(text)
    print("\n".join(result))


if __name__ == "__main__":
    main()
