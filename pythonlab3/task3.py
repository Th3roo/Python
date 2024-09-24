import random

def generate_random_guess(possible_numbers, max_count):
    possible_list = list(possible_numbers)
    count = random.randint(1, min(max_count, len(possible_list)))
    return set(random.sample(possible_list, count))

N = int(input("Введите максимальное число: "))
possible_numbers = set(range(1, N + 1))

max_guess_count = min(10, N)

while len(possible_numbers) > 1:
    guessed_numbers = generate_random_guess(possible_numbers, max_guess_count)
    guesses_str = ' '.join(map(str, sorted(guessed_numbers)))

    print(f"Нужное число есть среди вот этих чисел: {guesses_str}")

    response = input("Ответ Ивана (Да/Нет/Помогите!): ").strip().lower()

    if response == "да":

        possible_numbers &= guessed_numbers
    elif response == "нет":
        possible_numbers -= guessed_numbers
    elif response == "помогите!":
        break

if len(possible_numbers) == 1:
    print(f"Иван загадал число: {next(iter(possible_numbers))}")
elif possible_numbers:
    print("Иван мог загадать следующие числа:", ' '.join(map(str, sorted(possible_numbers))))
else:
    print("Иван не мог загадать ни одно число.")