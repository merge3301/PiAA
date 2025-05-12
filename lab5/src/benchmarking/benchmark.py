import time
import matplotlib.pyplot as plt  # type: ignore
from a_c_step import Trie
from naive_search import naive_search


def generate_text(length: int) -> str:
    import random
    import string

    return "".join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_patterns(num_patterns: int, pattern_length: int) -> dict:
    import random
    import string

    patterns = {}
    for i in range(num_patterns):
        pattern = "".join(
            random.choice(string.ascii_lowercase) for _ in range(pattern_length)
        )
        patterns[pattern] = i + 1
    return patterns


def compare_algorithms(text_lengths: list[int], num_patterns_list: list[int]):
    # Для варьирования длины текста
    aho_times_text = []
    naive_times_text = []

    # Для варьирования количества шаблонов
    aho_times_patterns = []
    naive_times_patterns = []

    # Фиксированное количество шаблонов для тестирования длины текста
    fixed_num_patterns = 10
    patterns = generate_patterns(
        fixed_num_patterns, 5
    )  # Длина шаблона фиксирована на 5

    # Измерение времени для варьирования длины текста
    for text_length in text_lengths:
        text = generate_text(text_length)

        # Ахо-Корасик
        start_time = time.time()
        trie = Trie(patterns)
        trie.Aho_Korasik(text)
        aho_time = time.time() - start_time
        aho_times_text.append(aho_time)

        # Наивный поиск
        start_time = time.time()
        naive_search(text, patterns)
        naive_time = time.time() - start_time
        naive_times_text.append(naive_time)

    # Фиксированная длина текста для тестирования количества шаблонов
    fixed_text_length = 10000
    text = generate_text(fixed_text_length)

    # Измерение времени для варьирования количества шаблонов
    for num_patterns in num_patterns_list:
        patterns = generate_patterns(num_patterns, 5)  # Длина шаблона фиксирована на 5

        # Ахо-Корасик
        start_time = time.time()
        trie = Trie(patterns)
        trie.Aho_Korasik(text)
        aho_time = time.time() - start_time
        aho_times_patterns.append(aho_time)

        # Наивный поиск
        start_time = time.time()
        naive_search(text, patterns)
        naive_time = time.time() - start_time
        naive_times_patterns.append(naive_time)

    # Построение графиков
    plt.figure(figsize=(12, 6))

    # График для варьирования длины текста
    plt.subplot(1, 2, 1)
    plt.plot(text_lengths, aho_times_text, label="Ахо-Корасик")
    plt.plot(text_lengths, naive_times_text, label="Наивный поиск")
    plt.xlabel("Длина текста")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Сравнение при варьировании длины текста")
    plt.legend()

    # График для варьирования количества шаблонов
    plt.subplot(1, 2, 2)
    plt.plot(num_patterns_list, aho_times_patterns, label="Ахо-Корасик")
    plt.plot(num_patterns_list, naive_times_patterns, label="Наивный поиск")
    plt.xlabel("Количество шаблонов")
    plt.ylabel("Время выполнения (сек)")
    plt.title("Сравнение при варьировании количества шаблонов")
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    text_lengths = [1000, 5000, 6000, 8000, 10000]  # Длины текста для тестирования
    num_patterns_list = [10, 50, 60, 80, 100]  # Количество шаблонов для тестирования
    compare_algorithms(text_lengths, num_patterns_list)
