def print_field(N, x, y):
    for row in range(N, 0, -1):
        line = ""
        for col in range(1, N + 1):
            if row == x and col == y:
                line += "R "
            else:
                line += ". "
        print(line)
    print("\n")

def move_robot(N, x, y):
    x = max(1, min(N, x))
    y = max(1, min(N, y))

    print("Initial position:")
    print_field(N, x, y)

    while True:
        command = input("Enter command (N, S, W, E, X): ").strip().upper()

        if command == "N":
            if x < N:
                x += 1
        elif command == "S":
            if x > 1:
                x -= 1
        elif command == "W":
            if y > 1:
                y -= 1
        elif command == "E":
            if y < N:
                y += 1
        elif command == "X":
            print("Shutting down")
            break
        else:
            print("Invalid command")
            continue

        print("\nNew position:")
        print_field(N, x, y)

N = int(input("Enter room size N: "))
x = int(input("Enter initial x position: "))
y = int(input("Enter initial y position: "))

move_robot(N, x, y)