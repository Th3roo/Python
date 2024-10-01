import numpy as np

m1 = np.random.randint(1, 11, size=10)
m2 = np.random.randint(1, 11, size=10)

# Сформировать массив m3, содержащий элементы, которые есть либо только в m1, либо только в m2
m3 = np.setxor1d(m1, m2)

# Заменить в m1 все значения, кратные 3 или 2, на число 1
m1 = np.where((m1 % 2 == 0) | (m1 % 3 == 0), 1, m1)

# Слить массивы m1 и m2 в один и преобразовать в матрицу 4x5
merged = np.concatenate((m1, m2))
matrix = merged.reshape(4, 5)

matrix = np.delete(matrix, [0, 3], axis=1)

# Транспонирование
result = matrix.T

print(f"m1: {m1}")
print(f"m2: {m2}")
print(f"m3: {m3}")
print(f"Матрица после объединения m1 и m2 и преобразования в 4x5:\n{matrix}")
print(f"Транспонированная матрица после удаления 1-го и 4-го столбцов:\n{result}")