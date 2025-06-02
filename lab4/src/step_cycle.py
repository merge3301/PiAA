def kmp_search(text, pattern):
    n = len(pattern)
    lps = [
        0
    ] * n  # lps[i] — длина наибольшего собственного префикса, совпадающего с суффиксом pattern[0:i+1]
    length = 0  # длина предыдущего совпадающего префикса
    i = 1

    while i < n:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    # Поиск pattern в text
    i = 0  # индекс для text
    j = 0  # индекс для pattern
    m = len(text)

    while i < m:

        if pattern[j] == text[i]:
            i += 1
            j += 1

            if j == n:
                return i - j  # найдено вхождение, возвращаем индекс начала
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


def main():
    A = input()
    B = input()

    if len(A) != len(B):
        print(-1)
        return

    if A == B:
        print(0)
        return

    text = B + B
    pos = kmp_search(text, A)

    if pos != -1 and pos < len(B):
        print((len(B) - pos) % len(B))
    else:
        print(-1)


if __name__ == "__main__":
    main()
