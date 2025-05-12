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

    def _create_trie(self):
        print(Colors.blue("============ Creating trie ============"))
        list_patterns = list(self.patterns.keys())

        for pattern in list_patterns:
            node = self.root
            print(
                f"***********************\nAdding {Colors.magenta(pattern)} to trie:\n***********************"
            )

            for symbol in pattern:
                print(f"Symbol: {Colors.magenta(symbol)}\n")

                if symbol not in node.children:
                    temp_node = Node(link=self.root, name=symbol)
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

            # Устанавливаем terminate для последнего символа шаблона
            node.terminate = self.patterns[pattern]
            print(f"Adding terminate for last node:\n{node.name}\n")

    def _create_suffix_link_for_node(self, node):
        if node == self.root:
            return
        link = node.parent.suffix_link
        print(f"\n  Processing node: '{node.name}'")
        print(
            f"  Current suffix link of parent '{node.parent.name}': '{link.name if link else 'None'}'"
        )

        while link and (node.name not in link.children.keys()):
            print(
                f"    Symbol '{node.name}' not found in children of '{link.name}'. Moving to suffix link: '{link.suffix_link.name if link.suffix_link else 'root'}'"
            )
            link = link.suffix_link

        if link:
            node.suffix_link = link.children[node.name]
            print(
                f"  Set suffix link for node '{node.name}' -> '{link.children[node.name].name}'"
            )

    def _create_suffix_links(self):
        print(Colors.blue("\n=== Making Suffix Links ===\n"))

        queue = [x for x in self.root.children.values()]

        while queue:
            cur_node = queue.pop(0)
            print(
                f"{Colors.yellow('----------------------------')}\nProcessing parent node: '{cur_node.name}'"
            )
            for child in cur_node.children.values():
                queue.append(child)
                self._create_suffix_link_for_node(child)

    def _create_terminal_links(self):
        print(Colors.blue("\n============ Making Terminal Links ============\n"))
        queue = [x for x in self.root.children.values()]

        while queue:
            cur_node = queue.pop(0)
            temp = cur_node
            for child in cur_node.children.values():
                queue.append(child)

            while temp.name != "root":
                if temp.terminate and temp != cur_node:
                    cur_node.terminal_link = temp
                    print(f"\nTerminal link for node: '{cur_node.name}' -> {temp.name}")
                    break
                temp = temp.suffix_link

    def Aho_Corasick(self, text: str) -> list[str]:
        print(
            Colors.blue("\n============ Aho Corasick algorithm start ============ \n")
        )
        result = []
        node = self.root

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
                print(
                    f"Symbol {Colors.red(node.name)} was found in child node:\n{node}\n"
                )
                temp = node

                while temp:
                    if temp.terminate:
                        print(
                            f'Get terminate value for "{self.terminate_patterns[temp.terminate]}" '
                            f"at index = {index - len(self.terminate_patterns[temp.terminate]) + 2}. "
                            f"Pattern number is {temp.terminate}.\n"
                        )
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
    return input(Colors.cyan("Enter text "))


def get_patterns() -> dict:
    n = int(input(Colors.cyan("Enter amount of patterns ")))
    patterns: dict = {}

    for pattern_n in range(n):
        pattern = input(Colors.cyan("Enter pattern "))
        patterns[pattern] = pattern_n + 1
    return patterns


# Основная функция
def main():
    text = get_text()
    patterns = get_patterns()
    # patterns = {"her": 1, "she": 2, "his": 3,"is":4,"i":5,"he":6}
    trie = Trie(patterns)
    result = trie.Aho_Corasick(text)
    print("\n".join(result))


if __name__ == "__main__":
    main()
