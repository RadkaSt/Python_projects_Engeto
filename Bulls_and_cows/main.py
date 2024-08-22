"""
project_2.py: second project for Engeto Online Python Academy
author: Radka Štorchová
email: r.storchova@gmail.com
discord: radkastorchova
"""
# imports
from functions import calculate_bulls_and_cows, welcome, guess_number, generate_number, save_statistics
import time

# Input user name
user_name = str(input("How should I call you?:"))
# Welcome to the game of Bulls and Cows
welcome(user_name)
# Generating secret number for the game
secret_number = generate_number()

# Assessing if the guess number fulfills the conditions:
attempts = 0  # initializing the counter of guesses
start_time = time.time()  # Records the start time
while True:
    guess = guess_number()
    # print(f"guess: {guess}, secret_number: {secret_number}") #used only to try the code
    print(calculate_bulls_and_cows(guess, secret_number))
    attempts += 1
    if guess == secret_number:
        end_time = time.time()  # Records the end time
        elapsed_time = end_time - start_time
        print(f"Congratulations {user_name}! You won!")
        print(f"Secret_number was {secret_number}.")
        print(f"You guessed it in {attempts} guesses.")
        print(f"Time taken: {elapsed_time:.2f} seconds.")
        save_statistics(user_name, attempts)
        break
    else:
        continue
