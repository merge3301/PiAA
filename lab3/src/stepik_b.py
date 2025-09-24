def compute_dp(price, A, B):
    m, n = len(A), len(B)
    matrix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        matrix[i][0] = i * price[2]

    for j in range(1, n + 1):
        matrix[0][j] = j * price[1]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost_replace = matrix[i - 1][j - 1] + (
                0 if A[i - 1] == B[j - 1] else price[0]
            )
            cost_insert = matrix[i][j - 1] + price[1]
            cost_delete = matrix[i - 1][j] + price[2]

            matrix[i][j] = min(cost_replace, cost_insert, cost_delete)

    return matrix


def backtrace(dp, price, A, B):
    i, j = len(A), len(B)
    ops = []
    while i > 0 or j > 0:
        if i == 0:
            ops.append("I")
            j -= 1
        elif j == 0:
            ops.append("D")
            i -= 1
        elif A[i - 1] == B[j - 1] and dp[i][j] == dp[i - 1][j - 1]:
            ops.append("M")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j - 1] + price[0]:
            ops.append("R")
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i][j - 1] + price[1]:
            ops.append("I")
            j -= 1
        elif dp[i][j] == dp[i - 1][j] + price[2]:
            ops.append("D")
            i -= 1

    ops.reverse()
    return "".join(ops)


if __name__ == "__main__":
    price = list(map(int, input().split()))
    A = input().strip()
    B = input().strip()

    dp = compute_dp(price, A, B)
    ops = backtrace(dp, price, A, B)

    print(ops)
    print(A)
    print(B)
