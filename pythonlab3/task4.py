def calculate_heights(tree, root, heights, current_height):
    """Рекурсивно вычисляет высоты всех потомков."""
    heights[root] = current_height
    for child in tree.get(root, []):
        calculate_heights(tree, child, heights, current_height + 1)

# Ввод данных
N = int(input("Введите количество человек: "))
relationships = {}
all_people = set()
children = set()

for i in range(N - 1):
    descendant, parent = input(f"{i + 1} пара: ").split()
    if parent not in relationships:
        relationships[parent] = []
    relationships[parent].append(descendant)
    all_people.add(parent)
    all_people.add(descendant)
    children.add(descendant)

# Определение корневого элемента (родоначальника)
root = list(all_people - children)[0]

# Вычисление высот
heights = {}
calculate_heights(relationships, root, heights, 0)

# Вывод результатов в лексикографическом порядке
print("“Высота” каждого члена семьи:")
for person in sorted(heights.keys()):
    print(f"{person} {heights[person]}")