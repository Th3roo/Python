def is_cyclic_shift(str1, str2):
    if len(str1) != len(str2):
        return False
    
    double_str2 = str2 + str2
    for i in range(len(str2)):
        if double_str2[i:i+len(str1)] == str1:
            return i

    return False

first_string = input("Введите первую строку: ")
second_string = input("Введите вторую строку: ")

shift = is_cyclic_shift(first_string, second_string)

if shift is False:
    print("Первую строку нельзя получить из второй с помощью циклического сдвига.")
else:
    print(f"Первая строка получается из второй со сдвигом {shift}.")