import random
import math

original_list = [random.randint(-20, 20) for _ in range(20)]
print("Исходный список:", original_list)
print()

modified_list = [x * 2 if x < 0 else (math.sqrt(x) if x > 0 else 0) for x in original_list]
print("Модифицированный список:", modified_list)
print()

i = 0
while i < len(modified_list):
    if modified_list[i] < 0:
        modified_list.insert(i, 0)
        i += 2
    else:
        i += 1
print("Список с нулями перед отрицательными элементами:", modified_list)
print()

K = int(input("Введите значение K для удаления: "))
while K in modified_list:
    modified_list.remove(K)
print(f"Список после удаления элементов со значением {K}:", modified_list)
print()

Z = int(input("Введите значение Z для добавления в конец: "))
modified_list = [0, 0, 0] + modified_list + [Z, Z, Z]
print("Расширенный список:", modified_list)
print()

sorted_list = sorted(modified_list)
print("Отсортированный список:", sorted_list)
