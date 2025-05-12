from operator import itemgetter


# Узел дерева
class Node:
    def __init__(self, link=None, name="root"):
        self.parent = None
        self.children: dict[str, Node] = {}
        self.suffix_link = link
        self.terminal_link = None
        self.terminate = 0  # Номер шаблона, если узел терминальный
        self.name = name  # Имя узла (символ или "root")
        self.deep: int = 0  # Глубина узла

    def __str__(self):
        return (
            f"Node name: {self.name};\n"
            f"Parent name: {self.parent.name if self.parent else None};\n"
            f"Children dict: {list(self.children.keys()) if self.children.keys() else None};\n"
            f"Suffix link: {self.suffix_link.name if self.suffix_link else None};\n"
            f"Terminate value: {True if self.terminate else False};\n"
            f"Deep value: {self.deep}."
        )


# Создание дерева
def create_trie(patterns: dict) -> Node:
    root = Node()
    list_patterns = list(patterns.keys())
    for i in range(len(list_patterns)):
        node = root

        for symbol in list_patterns[i]:

            if symbol not in node.children.keys():
                temp_node = Node(name=symbol)
                temp_node.deep = node.deep + 1
                node.children[symbol] = temp_node
                temp_node.parent = node
                node = temp_node
            else:
                node = node.children[symbol]

        node.terminate = patterns[list_patterns[i]]

    return root


def create_suffix_links(root: Node) -> None:
    queue = []
    for child in root.children.values():
        child.suffix_link = root
        queue.append(child)
    while queue:
        cur_node = queue.pop(0)
        for child in cur_node.children.values():
            queue.append(child)
            symbol = child.name
            link = cur_node.suffix_link

            while link and (symbol not in link.children.keys()):
                link = link.suffix_link

            if link:
                child.suffix_link = link.children[symbol]
            else:
                child.suffix_link = root


def _create_terminal_links(root) -> None:
    queue = [x for x in root.children.values()]
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


def Aho_Korasik() -> list[str]:
    text = input()
    pattern_input, joker, patterns, len_patt = get_pattern()
    tree = create_trie(patterns)
    create_suffix_links(tree)
    _create_terminal_links(tree)
    result = [0] * len(text)
    node = tree
    for index in range(len(text)):

        while node and (text[index] not in node.children.keys()):
            node = node.suffix_link

        if node:
            node = node.children[text[index]]
            temp = node

            while temp:
                if temp.terminate:
                    # подстрока текста, которая соответствует подшаблону, заканчивающемуся в текущем узле.
                    pattern = text[index - temp.deep + 1 : index + 1]
                    for j in patterns[pattern]:
                        if (index_j := index - temp.deep - j + 1) >= 0:
                            result[index_j] += 1
                temp = temp.terminal_link
        else:
            node = tree

    k = sum([len(elem) for elem in list(patterns.values())])
    ban_symbol: str = "~"

    output = []
    for i in range(len(result) - len_patt + 1):
        if k == result[i]:
            find_ban = []
            text_patt = text[i : i + len_patt]
            for j in range(len_patt):
                if pattern_input[j] == joker:
                    find_ban.append(text_patt[j])

            if ban_symbol not in find_ban:
                output.append(str(i + 1))
    return output


def get_pattern():
    pattern = input()
    joker = input()
    patterns = get_sub_patterns(pattern, joker)
    return pattern, joker, patterns, len(pattern)


def get_sub_patterns(pattern: str, joker: str) -> dict[str, list[int]]:
    patterns: dict[str, list[int]] = {}
    j = -1

    for i in range(len(pattern)):
        if pattern[i] == joker:
            if j < i - 1:
                s = pattern[j + 1 : i]
                if s not in patterns.keys():
                    patterns[s] = []
                patterns[s].append(j + 1)
            j = i

    if j != len(pattern) - 1:
        s = pattern[j + 1 :]
        if s not in patterns.keys():
            patterns[s] = []
        patterns[s].append(j + 1)

    return patterns


def main():

    result = Aho_Korasik()
    if result:
        print("\n" + "\n".join(result))
    else:
        print("No such pattern in the text.")


if __name__ == "__main__":
    main()
