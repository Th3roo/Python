import numpy as np

def solve_quadratic_equation(a, b, c):
    d = b**2 - 4 * a * c
    if d >= 0:
        x1 = (-b + np.sqrt(d)) / (2 * a)
        x2 = (-b - np.sqrt(d)) / (2 * a)
        return x1, x2
    else:
        return None, None

a, b, c = 1, 1, 1
x1,x2 = solve_quadratic_equation(a, b, c)

if x1 is None:
    print("No real roots exists")
else:
    print(f"x1 = {x1}, x2 = {x2}")