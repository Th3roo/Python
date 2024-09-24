from collections import defaultdict

# сортировка по названию
def sort_pizzas(pizzas):
    return sorted(pizzas.items())


n = int(input("Введите кол-во заказов: "))


orders = defaultdict(lambda: defaultdict(int))


for i in range(1, n+1):
    order = input(f"{i} заказ: ").split()
    customer, pizza, quantity = order
    orders[customer][pizza] += int(quantity)


for customer in sorted(orders.keys()):
    print(f"{customer}:")
    for pizza, quantity in sort_pizzas(orders[customer]):
        print(f"{pizza}: {quantity}")
    print()