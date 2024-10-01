import numpy as np

names = np.array(['Вася', 'Коля', 'Петя', 'Вася', 'Коля'])
grades = np.array([
    [4, 5, 4, 3, 4, 5],
    [2, 3, 4, 3, 2, 3],
    [4, 4, 3, 3, 2, 3],
    [5, 5, 5, 5, 4, 5],
    [3, 3, 4, 3, 4, 5]
])

print(names)

target_name = input("Введите имя ученика: ")

mask = names == target_name

filtered_grades = grades[mask]

print(f"Оценки ученика {target_name}:")
for i, row in enumerate(filtered_grades, start=1):
    print(f"{i}: {row}")