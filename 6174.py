"""The 6174 trick (Kaprekar's routine): a magic number game for kids.

Notes for grown-ups (none of this is shown to the player):

A four-digit subtraction game: start with any four-digit number and keep
rearranging and subtracting until you land on the "magic number" 6174.

How the trick works:
    1. Pick any four-digit number where at least one digit is different
       from the others (so 1111, 2222, ... are not allowed).
    2. Arrange its digits from largest to smallest.
    3. Reverse those digits (smallest to largest) and subtract the
       smaller number from the larger one.
    4. Take the answer and repeat steps 2-3.
    5. Keep going until you reach 6174. It works every time.

Example (starting from 4081):
    8410 - 0148 = 8262
    8622 - 2268 = 6354
    6543 - 3456 = 3087
    8730 - 0378 = 8352
    8532 - 2358 = 6174   -> done in 5 turns

Why 6174 is the stopping point:
    6174 maps to itself: 7641 - 1467 = 6174. Once you reach it, every
    further turn gives 6174 again, so it is a "fixed point" of the routine.

Notes:
    - Keep leading zeros. If an answer has fewer than four digits (for
      example 2111 - 1112 = 999), treat it as 0999 so there are still four
      digits to sort. Otherwise the trick can break.
    - Check each subtraction carefully. A single arithmetic slip can keep
      you from ever reaching 6174. The game checks each answer and shows
      the right one after two tries, so a slip never ruins the trick.
    - Any valid starting number reaches 6174 within 7 turns.
    - The routine is named after the Indian mathematician D. R. Kaprekar,
      who discovered it in 1949.

How the game plays:
    The player picks the starting number and guesses how many turns it
    will take. On each turn they arrange the digits biggest-first and
    smallest-first and do the subtraction themselves. A sealed envelope
    with the prediction "6174" is opened when they reach it.

Source: https://www.learn-with-math-games.com/math-tricks-for-kids.html
"""

import time

MAGIC = 6174
MAX_TRIES = 2

SEALED_ENVELOPE = r"""
     _____________________
    |\                   /|
    | \                 / |
    |  \_______________/  |
    |                     |
    |  MY PREDICTION      |
    |  (top secret!)      |
    |_____________________|
"""

OPENED_ENVELOPE = r"""
     _____________________
    |                     |
    |   My prediction:    |
    |                     |
    |  You will land on   |
    |      ** 6174 **     |
    |_____________________|
"""


def pause(seconds=0.8):
    time.sleep(seconds)


def four(n):
    """Show a number with 4 digits, keeping leading zeros (378 -> 0378)."""
    return f"{n:04d}"


def show_intro():
    print("=" * 44)
    print("          THE MAGIC NUMBER MACHINE")
    print("=" * 44)
    print("""
Pick ANY four-digit number, and I'll show you
that it always ends up in the same place!

Here's how each turn works:

  1. Put the digits in order, BIGGEST first.
  2. Put the digits in order, SMALLEST first.
  3. Subtract: biggest number - smallest number.
  4. Your answer is the number for the next turn!

Keep going until something magic happens.

Tip: always keep 4 digits. If you get 999,
it's really 0999!
""")


def ask_start_number():
    while True:
        text = input("Type a four-digit number: ").strip()
        if len(text) != 4 or not text.isdigit():
            print("Oops! It needs to be exactly 4 digits, like 3524.")
        elif len(set(text)) == 1:
            print("Sneaky! All the digits are the same. "
                  "Use at least two different digits.")
        else:
            return int(text)


def ask_guess():
    while True:
        text = input("How many turns do you think it will take? ").strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("Type a number, like 3 or 10.")


def ask_answer(question, correct, hint):
    """Ask until the player gets it right, or show the answer after 2 tries.

    Returns True if the player got it on their own.
    """
    for attempt in range(MAX_TRIES):
        text = input(question).strip()
        if text.isdigit() and int(text) == correct:
            print("  Correct!")
            return True
        if attempt < MAX_TRIES - 1:
            print(f"  Not quite. {hint}")
    print(f"  Good try! The answer is {four(correct)}.")
    return False


def play_round():
    print("Before we start, I've sealed my prediction in this envelope.")
    print("No peeking!")
    print(SEALED_ENVELOPE)

    current = ask_start_number()
    if current == MAGIC:
        print("\nWhoa, you picked my secret number! Let's open the envelope...")
        pause()
        print(OPENED_ENVELOPE)
        print("Are you reading MY mind? Pick a different number next time!\n")
        return
    guess = ask_guess()
    print(f"\nOkay! Let's feed {four(current)} into the Magic Number Machine...\n")
    pause()

    path = [current]
    turns = 0
    stars = 0

    while current != MAGIC:
        turns += 1
        digits = sorted(str(current).zfill(4))
        largest = int("".join(reversed(digits)))
        smallest = int("".join(digits))
        answer = largest - smallest

        print("-" * 44)
        print(f"TURN {turns}   Your number: {four(current)}")
        print("-" * 44)

        if ask_answer("Digits BIGGEST first: ", largest,
                      "Start with the biggest digit."):
            stars += 1
        if ask_answer("Digits SMALLEST first: ", smallest,
                      "Start with the smallest digit (zeros go first!)."):
            stars += 1
        print(f"\n  Now subtract:  {four(largest)}")
        print(f"               - {four(smallest)}")
        print("               ------")
        if ask_answer("  Your answer: ", answer,
                      "Check your borrowing and try again."):
            stars += 1

        current = answer
        path.append(current)
        print()
        print("  Your path so far: " + " -> ".join(four(n) for n in path))
        print()
        pause(0.5)

    print("=" * 44)
    print("  STOP! The machine landed on 6174!")
    print("=" * 44)
    pause()
    print("\nLet's open my envelope", end="", flush=True)
    for _ in range(3):
        pause()
        print(".", end="", flush=True)
    pause()
    print()
    print(OPENED_ENVELOPE)
    pause(0.5)

    print(f"You reached the magic number in {turns} turn(s)!")
    if guess == turns:
        print(f"You guessed {guess}. EXACTLY right! Are YOU a mind reader?")
    else:
        off = abs(guess - turns)
        print(f"You guessed {guess}, so you were {off} away.")

    possible = turns * 3
    print(f"You earned {stars} out of {possible} stars: " + "*" * stars)
    if stars == possible:
        print("Perfect math! Amazing!")
    print()


def main():
    show_intro()
    round_number = 1

    while True:
        play_round()
        if round_number == 1:
            question = "Think a different number will land somewhere else? Try it! (y/n) "
        else:
            question = "Want to try another number? (y/n) "
        again = input(question).strip().lower()
        if not again.startswith("y"):
            print("\nThanks for playing! Ask a grown-up to pick a number,")
            print("then predict where it'll end up. You know the secret now!")
            break
        round_number += 1
        print()


if __name__ == "__main__":
    main()
