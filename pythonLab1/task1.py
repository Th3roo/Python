import random

def get_user_input():
    while True:
        choice = input("Choose: rock (r), paper (p), scissors (s): ").lower()
        if choice in ['r', 'p', 's']:
            return choice
        print("Invalid input")

def play():
    user_input = get_user_input()
    random_input = random.choice(['r', 'p', 's'])

    print(f"User_input: {user_input}")
    print(f"Random_input: {random_input}")

    if user_input == random_input:
        print("Same")
        return
    if (user_input == 'r' and random_input == 's') or (user_input == 'p' and random_input == 'r') or (user_input == 's' and random_input == 'p'):
        print("Player Win!")
    else:
        print("Computer Win")

play()