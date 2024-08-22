import random


def welcome(user_name):
    """ Welcomes user in a game and explains few rules of the game."""
    # Welcome message:
    print(f"Hello {user_name}!\nWelcome to the game of Bulls and Cows. "
          f"\nI have generated a 4-digit number with unique digits which does not start with 0."
          f"\nYou can now try to guess the number. "
          f"\nYou will get a bull for every correctly guessed digit at correct location and "
          f"\na cow for correct digit at wrong location.")


def generate_number() -> int:
    """Generates 4 digit number with unique digits. The number cannot start with zero."""
    first = random.choice(range(1, 10))
    leftover = list(set(range(10)) - {first})
    rest = random.sample(leftover, 3)
    digits = [first] + rest
    number = int(''.join(map(str, digits)))
    return number


def guess_number():
    """Takes a guess number from user and assess if the input meets the conditions."""
    number = str(input("Guess a 4-digit number with unique digits that cannot start with zero:"))
    if len(number) != 4:
        print("Your number has to be 4 digits long.")
    elif number[0] == '0':
        print("Your number should not start with 0.")
    elif len(set(number)) != 4:
        print("Your number should have unique digits.")
    elif not number.isdigit():
        print("You should enter numbers.")
    else:
        return int(number)


def calculate_bulls_and_cows(guess, secret_number):
    """Calculate the number of bulls and cows in the guess and secret number"""
    bulls = sum(s == g for s, g in zip(str(secret_number), str(guess)))
    common_digits = set(str(secret_number)) & set(str(guess))
    cows = sum(min(str(secret_number).count(d), str(guess).count(d)) for d in common_digits) - bulls
    # Handle singular and plural forms
    bull_text = "bull" if bulls == 1 else "bulls"
    cow_text = "cow" if cows == 1 else "cows"

    return bulls, bull_text, cows, cow_text

def save_statistics(user_name, num_guesses):
    with open("statistics.txt", "a") as file:
        file.write(f"{user_name}  | {num_guesses}\n")


if __name__ == '__main__':
    print(f"Generating random 4-digit number: {generate_number()}")
    print(guess_number())
    print(calculate_bulls_and_cows(1234, 9234))
