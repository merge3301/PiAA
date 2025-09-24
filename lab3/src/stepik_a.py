def levenshtein(price, s1, s2):
    m, n = len(s1), len(s2)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for j in range(1, n + 1):
        matrix[0][j] = j * price[1]
    for i in range(1, m + 1):
        matrix[i][0] = i * price[2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            a, b = s1[i - 1], s2[j - 1]
            match_or_replace = 0 if a == b else price[0]
            cost_replace = matrix[i - 1][j - 1] + match_or_replace
            cost_insert = matrix[i][j - 1] + price[1]
            cost_delete = matrix[i - 1][j] + price[2]
            matrix[i][j] = min(cost_replace, cost_insert, cost_delete)
    return matrix[m][n]


if __name__ == "__main__":
    price = list(map(int, input().split()))
    s1 = input().strip()
    s2 = input().strip()

    dist = levenshtein(price, s1, s2)
    print(dist)
