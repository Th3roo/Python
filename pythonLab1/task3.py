

def get_money(amount):
    money = [5000, 1000, 500, 200, 100]
    result = {}

    if amount % money[-1] != 0:
        return "Unable to dispense"

    for note in money:
        count = amount // note
        if count > 0:
            result[note] = count
            amount -= count * note
    if amount ==0:
        return result
    else:
        return "Unable to dispense"

withdraw = int(input("Enter amount to withdraw: "))
result = get_money(withdraw)
print (result)