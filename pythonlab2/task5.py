def compress_string(s):
    if not s:
        return ""
    
    compressed = []
    count = 1
    current_char = s[0]

    for char in s[1:]:
        if char == current_char:
            count += 1
        else:
            compressed.append(f"{current_char}{count}")
            current_char = char
            count = 1

    compressed.append(f"{current_char}{count}")
    return ''.join(compressed)

input_string = input("Введите строку: ")

compressed_string = compress_string(input_string)

print(f"Закодированная строка: {compressed_string}")