class Child:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.is_calm = True
        self.is_fed = True

    def __str__(self):
        return f"Child: {self.name}, Age: {self.age}, Calm: {'Yes' if self.is_calm else 'No'}, Fed: {'Yes' if self.is_fed else 'No'}"

class Parent:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def info(self):
        return f"Parent: {self.name}, Age: {self.age}, Number of children: {len(self.children)}"

    def calm_child(self, index):
        if 0 <= index < len(self.children):
            self.children[index].is_calm = True
            print(f"{self.name} calmed {self.children[index].name}")
        else:
            print("Invalid child index")

    def feed_child(self, index):
        if 0 <= index < len(self.children):
            self.children[index].is_fed = True
            print(f"{self.name} fed {self.children[index].name}")
        else:
            print("Invalid child index")

def main():
    parents = []
    n = int(input("Введите количество родителей: "))

    for i in range(n):
        name = input(f"Введите имя родителя {i+1}: ")
        age = int(input(f"Введите возраст родителя {i+1}: "))
        parent = Parent(name, age)

        num_children = int(input(f"Введите количество детей для родителя {name}: "))
        for j in range(num_children):
            child_name = input(f"Введите имя ребенка {j+1}: ")
            child_age = int(input(f"Введите возраст ребенка {j+1}: "))
            child = Child(child_name, child_age)
            parent.add_child(child)

        parents.append(parent)

    while True:
        print("\nМеню:")
        print("1. Информация о родителе")
        print("2. Информация о детях родителя")
        print("3. Выполнить действие с ребенком")
        print("4. Выход")

        choice = int(input("Выберите действие: "))

        if choice == 1:
            k = int(input("Введите номер родителя: "))
            if 0 <= k < len(parents):
                print(parents[k].info())
            else:
                print("Неверный номер родителя")

        elif choice == 2:
            k = int(input("Введите номер родителя: "))
            if 0 <= k < len(parents):
                for i, child in enumerate(parents[k].children):
                    print(f"{i+1}. {child}")
            else:
                print("Неверный номер родителя")

        elif choice == 3:
            k = int(input("Введите номер родителя: "))
            if 0 <= k < len(parents):
                child_index = int(input("Введите номер ребенка: "))
                action = input("Введите действие (успокоить/покормить): ").lower()
                if action == "успокоить":
                    parents[k].calm_child(child_index - 1)
                elif action == "покормить":
                    parents[k].feed_child(child_index - 1)
                else:
                    print("Неверное действие")
            else:
                print("Неверный номер родителя")

        elif choice == 4:
            print("Выход из программы")
            break

        else:
            print("Неверный выбор")

if __name__ == "__main__":
    main()
