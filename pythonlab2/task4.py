def calculate_debts():
    n = int(input("Введите количество друзей: "))
    k = int(input("Введите количество долговых расписок: "))
    
    balances = {i: 0 for i in range(1, n+1)}

    for i in range(k):
        print(f"\n{i+1} расписка")
        debtor = int(input("Кому: "))
        creditor = int(input("От кого: "))
        amount = int(input("Сколько: "))

        # Обновление баланса
        balances[debtor] -= amount
        balances[creditor] += amount

    print("\nБаланс друзей:")
    for friend, balance in balances.items():
        print(f"{friend} : {balance}")

calculate_debts()