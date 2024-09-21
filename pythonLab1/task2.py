import numpy as np

def get_user_input():
    while True:
        try:
            a, b, c = map(int, input("Enter a b c : ").split())
            return a, b, c
        except ValueError:
            print("Try again")

def solve_quadratic_equation(a, b, c):
    if a == 0:
        if b == 0:
            if c == 0:
                return "Infinite solutions", None
            else:
                return None, None
        else:
            return -c / b, None

    d = b ** 2 - 4 * a * c
    if d > 0:
        x1 = (-b + np.sqrt(d)) / (2 * a)
        x2 = (-b - np.sqrt(d)) / (2 * a)
        return x1, x2
    elif d == 0:
        x = -b / (2 * a)
        return x, None
    else:
        return None, None

a, b, c = get_user_input()
result = solve_quadratic_equation(a, b, c)

if result[0] == "Infinite solutions":
    print("Infinite solutions")
elif result[0] is None:
    print("No real roots exist")
elif result[1] is None:
    print(f"x = {result[0]}")
else:
    print(f"x1 = {result[0]}, x2 = {result[1]}")