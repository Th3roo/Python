import math

number = float(input("Введите число: "))

if number == 0:
    print("Формат плавающей точки: x = 0")
else:
    exponent = math.floor(math.log10(abs(number)))
    
    mantissa = number / (10 ** exponent)
    
    print(f"Формат плавающей точки: x = {mantissa}*10^{exponent}")