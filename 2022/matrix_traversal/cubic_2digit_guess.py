import random

while True:
    x = random.randint(10, 99)
    x3 = x * x * x
    guess = int(input(f"GUESS: {x3} is cube of ?: "))
    if guess == x:
        print("Correct!")
    else:
        print(f"Wrong! {x3} is cube of {x}")
