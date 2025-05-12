import time
import matplotlib.pyplot as plt  # type: ignore
from MatrixCreator import MatrixCreator
from ADO_MOD_algorithm import ADO_MOD_algorithm
from LittleAlgorithm import LittleAlgorithm


def test_algorithm(matrix_sizes, num_tests_per_size):
    results = {}

    for size in matrix_sizes:
        times = []
        for _ in range(num_tests_per_size):
            matrix = MatrixCreator().generate_matrix(True, size, 10, 20)
            # little_algo = LittleAlgorithm(matrix)
            # i_index = [i for i in range(size)]
            # j_index = [j for j in range(size)]

            start_time = time.time()
            ADO_MOD_algorithm(matrix).find_res(1)
            # little_algo.method_Little(matrix, {}, 0, i_index, j_index)
            end_time = time.time()

            times.append(end_time - start_time)

        avg_time = sum(times) / num_tests_per_size
        results[size] = avg_time
        print(f"Size: {size}, Average Time: {avg_time:.4f} seconds")

    return results


def plot_results(results):
    sizes = list(results.keys())
    times = list(results.values())

    plt.figure(figsize=(12, 6))

    plt.plot(
        sizes,
        times,
        marker="o",
        linestyle="-",
        color="b",
        label="Время выполнения алгоритма",
    )

    plt.title("Зависимость времени выполнения от размера матрицы")
    plt.xlabel("Размер матрицы")
    plt.ylabel("Время выполнения (секунды)")
    plt.grid(True)
    plt.legend()
    plt.show()


if __name__ == "__main__":
    matrix_sizes = range(2, 20)
    num_tests_per_size = 50

    results = test_algorithm(matrix_sizes, num_tests_per_size)
    plot_results(results)
