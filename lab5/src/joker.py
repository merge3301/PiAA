from operator import itemgetter
from colors import Colors


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
def create_tree(patterns: dict) -> Node:
    root = Node()
    list_patterns = list(patterns.keys())

    print(Colors.blue("============ Creating trie ============"))

    for i in range(len(list_patterns)):
        node = root
        print(
            f"***********************\nAdding {Colors.magenta(list_patterns[i])} to trie:\n***********************"
        )

        for symbol in list_patterns[i]:
            print(f"Symbol: {Colors.magenta(symbol)}\n")

            if symbol not in node.children.keys():
                temp_node = Node(name=symbol)
                temp_node.deep = node.deep + 1
                node.children[symbol] = temp_node
                temp_node.parent = node
                node = temp_node
                print(
                    f"{Colors.green('[+] ')}Creating and adding node:\n{temp_node}\n{Colors.yellow('----------------------------')}"
                )
            else:
                print(
                    f"Already have this symbol:\n{node.children[symbol]}\n{Colors.yellow('----------------------------')}\n"
                )
                node = node.children[symbol]

        node.terminate = patterns[list_patterns[i]]
        print(f"Adding terminate for last node:\n{node}\n")

    return root


# Создание суффиксных ссылок
def create_suffix_links(root: Node) -> None:
    print(Colors.blue("\n============ Making Suffix Links ============\n"))

    queue = []
    for child in root.children.values():
        child.suffix_link = root
        queue.append(child)
        print(f"Set suffix link for node '{child.name}' -> root")

    while queue:
        cur_node = queue.pop(0)
        print(f"\nProcessing parent node: '{cur_node.name}'")

        for child in cur_node.children.values():
            queue.append(child)
            symbol = child.name
            link = cur_node.suffix_link

            print(
                f"{Colors.yellow('----------------------------')}\nProcessing parent node: '{cur_node.name}'"
            )
            print(
                f"  Current suffix link of parent '{cur_node.name}': '{link.name if link else 'None'}'"
            )

            while link and (symbol not in link.children.keys()):
                print(
                    f"    Symbol '{symbol}' not found in children of '{link.name}'. Moving to suffix link: '{link.suffix_link.name if link.suffix_link else 'None'}'"
                )
                link = link.suffix_link

            if link:
                child.suffix_link = link.children[symbol]
                print(
                    f"  Set suffix link for node '{child.name}' -> '{link.children[symbol].name}'"
                )
            else:
                child.suffix_link = root
                print(f"  Set suffix link for node '{child.name}' -> root")


def _create_terminal_links(root) -> None:
    print(Colors.blue("\n============ Making Terminal Links ============\n"))
    queue = [x for x in root.children.values()]
    while queue:
        cur_node = queue.pop(0)
        temp = cur_node
        for child in cur_node.children.values():
            queue.append(child)

        while temp.name != "root":
            if temp.terminate and temp != cur_node:
                cur_node.terminal_link = temp
                print(
                    f"{Colors.yellow('----------------------------')}\nTerminal link for node: '{cur_node.name}' -> {temp.name}"
                )
                break
            temp = temp.suffix_link


# Функция с алгоритмом Ахо-Корасик
def Aho_Corasick() -> list[str]:
    text = get_text()
    pattern_input, joker, patterns, len_patt = get_pattern()
    print("Splitted patterns: ", patterns)
    tree = create_tree(patterns)
    create_suffix_links(tree)
    _create_terminal_links(tree)
    print(Colors.blue("\n=== Aho Korasik algorithm start === \n"))
    result = [0] * len(text)
    node = tree
    for index in range(len(text)):
        colored_text = (
            f'{Colors.yellow("------------------------")}\n'
            + text[:index]
            + Colors.red(text[index])
            + text[index + 1 :]
        )
        print(colored_text)

        while node and (text[index] not in node.children.keys()):
            node = node.suffix_link

        if node:
            node = node.children[text[index]]
            print(f"Symbol {Colors.red(node.name)} was found in child node:\n{node}\n")
            temp = node

            while temp:
                if temp.terminate:
                    # Вырезает из текста подстроку, соответствующую найденному шаблону.
                    pattern = text[index - temp.deep + 1 : index + 1]
                    print(
                        f'Get terminate value for "{pattern}" at index = {index - temp.deep + 2}. Pattern number is {temp.terminate}.\n'
                    )
                    # j — позиция подшаблона в исходном шаблоне.
                    for j in patterns[pattern]:
                        # Вычисляет, где начался исходный шаблон в тексте, и увеличивает счётчик вхождений.
                        if (index_j := index - temp.deep - j + 1) >= 0:
                            result[index_j] += 1
                temp = temp.terminal_link
        else:
            node = tree

    k = sum([len(elem) for elem in list(patterns.values())])
    print(f"Get result C[i]:\n{result[:len(result) - len_patt + 1]}\n")

    ban_symbol: str = input(Colors.cyan("Input banned symbol: "))
    if len(ban_symbol) != 1:
        raise ValueError("Invalid ban symbol!")

    print(
        f"\nCount of patterns = {k}.\nTrying to find joker_pattern in the result list (C[i]).\n"
    )

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


def get_text() -> str:
    return input(Colors.cyan("Enter text: "))


def get_pattern():
    pattern = input(Colors.cyan("Enter pattern: "))
    joker = input(Colors.cyan("Enter joker symbol: "))
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
    result = Aho_Corasick()
    if result:
        print("Result:\n" + "\n".join(result))
    else:
        print("No such pattern in the text.")


if __name__ == "__main__":
    main()
