"""The 6174 trick (Kaprekar's routine): a vault-cracking game for kids.

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
    The vault has a secret code (6174). The player types any four-digit
    code into the lock and guesses how many turns it will take to crack
    it. On each turn they arrange the digits biggest-first and
    smallest-first and do the subtraction themselves, and the answer
    becomes the new code on the lock's dials. When the dials reach 6174
    the vault opens, and they collect a gold coin for every step they
    got right on their own. Playing again with a different code shows
    the vault always opens at the same code.

Source: https://www.learn-with-math-games.com/math-tricks-for-kids.html
"""

import time

SECRET_CODE = 6174
MAX_TRIES = 2
LOCK_WIDTH = 27


def pause(seconds=0.8):
    time.sleep(seconds)


def four(n):
    """Show a number with 4 digits, keeping leading zeros (378 -> 0378)."""
    return f"{n:04d}"


def show_lock(code, unlocked=False):
    """Draw the vault's combination lock with the code on its dials."""
    dials = "  ".join(f"[{d}]" for d in four(code))
    status = "*** UNLOCKED! ***" if unlocked else "LOCKED"
    print(f"""
     {"_" * LOCK_WIDTH}
    |  {"_" * (LOCK_WIDTH - 4)}  |
    | |{dials:^{LOCK_WIDTH - 4}}| |
    | |{"_" * (LOCK_WIDTH - 4)}| |
    |{status:^{LOCK_WIDTH}}|
    |{"_" * LOCK_WIDTH}|
""")


def spin_dials(code):
    print("  Spinning the dials", end="", flush=True)
    for _ in range(3):
        pause(0.4)
        print(" click", end="", flush=True)
    pause(0.4)
    print()
    show_lock(code)


def show_vault_open(coins):
    print("""
     ___________________________
    |                           |
    |   THE VAULT DOOR OPENS!   |
    |                           |
    |      $   $   $   $   $    |
    |    $   TREASURE!   $      |
    |      $   $   $   $   $    |
    |___________________________|
""")
    if coins is None:
        print("The whole treasure is yours!")
    elif coins:
        print(f"You found {coins} gold coin(s): " + "$" * coins)
    else:
        print("The vault is open! Get your math right next time for gold coins!")


def show_intro():
    print("=" * 44)
    print("          CRACK THE SECRET VAULT")
    print("=" * 44)
    print("""
There's a vault full of treasure, and it's
locked with a secret 4-digit code.

You don't know the code... but you don't need
to! Type in ANY code, then use this math spell
to change it, one turn at a time:

  1. Put the digits in order, BIGGEST first.
  2. Put the digits in order, SMALLEST first.
  3. Subtract: biggest number - smallest number.
  4. Your answer is the new code on the lock!

Keep casting the spell until the vault opens.
Every step you get right earns a gold coin.

Tip: codes always have 4 digits. If you get
999, the code is really 0999!
""")


def ask_start_code():
    while True:
        text = input("Type any 4-digit code into the lock: ").strip()
        if len(text) != 4 or not text.isdigit():
            print("Oops! The lock needs exactly 4 digits, like 3524.")
        elif len(set(text)) == 1:
            print("The lock won't take a code with all the same digits. "
                  "Try at least two different digits!")
        else:
            return int(text)


def ask_guess():
    while True:
        text = input("How many turns do you think it will take to open? ").strip()
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
            print("  Correct! +1 gold coin")
            return True
        if attempt < MAX_TRIES - 1:
            print(f"  Not quite. {hint}")
    print(f"  Good try! The answer is {four(correct)}.")
    return False


def play_round():
    current = ask_start_code()
    show_lock(current)

    if current == SECRET_CODE:
        print("Wait... the lock is clicking...")
        pause()
        show_lock(current, unlocked=True)
        print("WHOA! You typed the secret code on your very first try!")
        print("Are you a master safe-cracker?!")
        show_vault_open(None)
        print()
        return

    print("The lock says: LOCKED. Time to cast the math spell!\n")
    guess = ask_guess()
    print()

    codes = [current]
    turns = 0
    coins = 0

    while current != SECRET_CODE:
        turns += 1
        digits = sorted(four(current))
        largest = int("".join(reversed(digits)))
        smallest = int("".join(digits))
        answer = largest - smallest

        print("-" * 44)
        print(f"TURN {turns}   Code on the lock: {four(current)}")
        print("-" * 44)

        if ask_answer("Digits BIGGEST first: ", largest,
                      "Start with the biggest digit."):
            coins += 1
        if ask_answer("Digits SMALLEST first: ", smallest,
                      "Start with the smallest digit (zeros go first!)."):
            coins += 1
        print(f"\n  Now subtract:  {four(largest)}")
        print(f"               - {four(smallest)}")
        print("               ------")
        if ask_answer("  Your answer: ", answer,
                      "Check your borrowing and try again."):
            coins += 1

        current = answer
        codes.append(current)
        print()
        spin_dials(current)

        if current != SECRET_CODE:
            print("  Still LOCKED. Codes tried: "
                  + " -> ".join(four(n) for n in codes))
            print()
            pause(0.5)

    print("  ...wait... something's happening...")
    pause()
    print("  CLICK! CLICK! CLUNK!")
    pause()
    show_lock(current, unlocked=True)
    print(f"YOU CRACKED THE CODE: {four(SECRET_CODE)}!")
    print("Your codes: " + " -> ".join(four(n) for n in codes))
    pause(0.5)
    show_vault_open(coins)

    print()
    print(f"It took {turns} turn(s) to crack the vault.")
    if guess == turns:
        print(f"You guessed {guess}. EXACTLY right!")
    else:
        print(f"You guessed {guess}, so you were {abs(guess - turns)} away.")
    if coins == turns * 3:
        print("You got every step right. Perfect safe-cracking!")
    print()


def main():
    show_intro()
    round_number = 1

    while True:
        play_round()
        if round_number == 1:
            question = ("Do you think a DIFFERENT starting code would open "
                        "the vault too? Try it! (y/n) ")
        else:
            question = "Want to crack the vault with another code? (y/n) "
        again = input(question).strip().lower()
        if not again.startswith("y"):
            print("\nThanks for playing! Now you know the vault's secret code.")
            print("Ask a friend to try ANY code and watch it open at 6174!")
            break
        round_number += 1
        print("\nThe vault slams shut and locks again... CLUNK!\n")


if __name__ == "__main__":
    main()
