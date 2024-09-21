from math import gcd


# Наибольший общий делитель
def lcm(a,b):
    return a*b // gcd(a,b) # Наименьший общий делитель

n = int(input("Team A Members: "))
m = int(input("Team B Members: "))

result = lcm(n,m)

print(f"Smallest number: {result}")