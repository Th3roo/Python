import numpy as np

matrix = np.random.randint(-10, 11, size=(8, 8))

print("Исходная матрица:")
print(matrix)

center = matrix[2:6, 2:6]
print("\nЦентральная часть матрицы 4x4:")
print(center)

min_element = np.min(matrix)
matrix = matrix[~np.any(matrix == min_element, axis=1)]

print("\nМатрица после удаления строк с минимальным элементом:")
print(matrix)

min_row = np.full((1, matrix.shape[1]), min_element)
matrix = np.vstack((min_row, matrix))

print("\nМатрица после вставки строки с минимальным элементом:")
print(matrix)

sum_elements = np.sum(matrix)
mean_elements = np.mean(matrix)

print(f"\nСумма всех элементов: {sum_elements}")
print(f"Среднее арифметическое всех элементов: {mean_elements:.2f}")