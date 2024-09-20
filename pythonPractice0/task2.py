'''
Напишите программу «Угадайка», в которой компьютер
«загадывает» целое число от 1 до 100 и предлагает пользователю
угадать его. После каждого ответа пользователя должно выводиться
сообщение, больше загаданное число или меньше.
'''

import numpy as np

def get_int_input(promt):
    while True:
        try:
            return int(input(promt))
        except ValueError:
            print("Enter a NUMBER")

def predict_number():
    randint = np.random.randint(0,100)
    input_number = get_int_input("Enter a number: ")
    while input_number != randint:
        if input_number < randint:
            print("Too low")
        else:
            print("Too high")
        input_number = get_int_input("Try again: ")
    print("YOU WIN!")

predict_number()


