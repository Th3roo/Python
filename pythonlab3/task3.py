N = int(input("Введите максимальное число: "))

possible_numbers = set(range(1, N + 1))

while True:
    guess = input("Нужное число есть среди вот этих чисел: ")
    
    if guess == "Помогите!":
        break
    
    guessed_numbers = set(map(int, guess.split()))
    
    answer = input("Ответ Ивана: ").strip().lower()
    
    if answer == "да":
        possible_numbers &= guessed_numbers
    elif answer == "нет":
        possible_numbers -= guessed_numbers

print("Иван мог загадать следующие числа:", " ".join(map(str, sorted(possible_numbers))))