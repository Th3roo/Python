import numpy as np

arr = np.random.uniform(-20, 20, size=20)
print("Random array: ")
print(arr)

new_arr = np.where(arr < 0, arr * 2, np.sqrt(np.abs(arr)))
print("\nNumber<0 multiplied by 2 and other thing: ")
print(new_arr)

mask = new_arr < 0
indices = np.where(mask)[0]
result = np.insert(new_arr, indices, 0)
print("\nInsert zero's: ")
print(result)

K = float(input("Enter K to remove: "))
result = result[result != K]
print("\nArray with K removed: ", K)
print(result)

Z = float(input("Enter Z to append: "))
result = np.concatenate(([0, 0, 0], result, [Z, Z, Z]))
print("\nNew array:")
print(result)

result = np.sort(result)
print("\nSorted array:")
print(result)