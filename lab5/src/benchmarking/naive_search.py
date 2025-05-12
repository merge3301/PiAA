def naive_search(text: str, patterns: dict) -> list[str]:
    result = []
    for pattern, pattern_id in patterns.items():
        pattern_length = len(pattern)
        for i in range(len(text) - pattern_length + 1):
            if text[i : i + pattern_length] == pattern:
                result.append([i + 1, pattern_id])

    result = sorted(result, key=lambda x: (x[0], x[1]))
    result = [" ".join(map(str, elem)) for elem in result]
    return result


def main():
    text = input("Введите текст: ")
    n = int(input("Введите количество шаблонов: "))
    patterns = {}
    for i in range(n):
        pattern = input(f"Введите шаблон {i + 1}: ")
        patterns[pattern] = i + 1

    result = naive_search(text, patterns)
    print("\n".join(result))


if __name__ == "__main__":
    main()
