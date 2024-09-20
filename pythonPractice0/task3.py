import math

def combinations(N,M):
    return math.comb(N,M)

n,m = 6, 5

print(f"Количество комбинаций лампочек: {combinations(n,m)}")