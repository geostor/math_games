"""The Prediction of 34: a mind-reading game for kids.

Notes for grown-ups (none of this is shown to the player):

From "Mathemania" by Raymond Blum, as described at:
https://www.learn-with-math-games.com/cool-math-trick.html

How the game plays:
    1. The computer "seals" a prediction in an envelope before the game
       starts. Players can choose to peek inside first, so they can see
       the prediction was written down before they picked anything.
       (Peeking is fine: the trick still works, which makes it even
       spookier.)
    2. The player sees a grid of numbers in order, such as 1-16 on a
       4x4 board. The board size is picked at random (3x3 to 6x6).
    3. They circle any number. Everything else in that row and column is
       crossed out.
    4. They keep circling numbers that aren't crossed out until every
       row has one circled number.
    5. They add up their circled numbers (good addition practice).
    6. The envelope is opened, and the prediction matches their total.

The secret:
    The circled numbers always add up to the same total as either
    diagonal of the grid: 1 + 6 + 11 + 16 = 34 and 4 + 7 + 10 + 13 = 34.

Why it works:
    Crossing out a row and column means you end up with exactly one
    number from every row and every column. Every number in the grid is
    (a row start: 1, 5, 9 or 13) + (a column step: 0, 1, 2 or 3). Since
    each row and each column is used once, the total is always
        (1 + 5 + 9 + 13) + (0 + 1 + 2 + 3) = 28 + 6 = 34
    no matter which numbers are picked.

Other board sizes:
    The page suggests a different board the second time so the
    prediction isn't the same. Each round picks a random size from 3x3
    to 6x6, never the same size twice in a row. An n x n board always
    gives n * (n*n + 1) / 2:
        3x3 (1-9)  -> 15      5x5 (1-25) -> 65
        4x4 (1-16) -> 34      6x6 (1-36) -> 111
"""

import random
import time

# Every square board works. Bigger than 6x6 gets hard to read and add.
BOARD_SIZES = [3, 4, 5, 6]

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


def pause(seconds=0.8):
    time.sleep(seconds)


def opened_envelope(prediction):
    line = f"You will get {prediction}!"
    return f"""
     _____________________
    |                     |
    |   My prediction:    |
    |                     |
    |{line:^21}|
    |                     |
    |_____________________|
"""


def show_grid(grid, size, circled, crossed):
    print()
    for r in range(size):
        cells = []
        for c in range(size):
            if (r, c) in circled:
                cells.append(f"({grid[r][c]:>2})")
            elif (r, c) in crossed:
                cells.append("  X ")
            else:
                cells.append(f" {grid[r][c]:>2} ")
        print("    " + " ".join(cells))
    print()


def show_intro():
    print("=" * 44)
    print("        THE MIND-READING NUMBER GAME")
    print("=" * 44)
    print("""
I'm going to guess a number you haven't even
made yet! Here's how to play:

  1. You'll see a board full of numbers.
  2. Pick ANY number you like. I'll circle it.
  3. I'll cross out the other numbers in its
     row (across) and column (up and down).
  4. Pick another number that isn't crossed out.
  5. Keep going until you can't pick any more.
  6. Add up your circled numbers.

Then we'll open my secret envelope and see if
I read your mind!
""")


def play_round(size):
    grid = [[row * size + col + 1 for col in range(size)] for row in range(size)]
    prediction = size * (size * size + 1) // 2

    print("I've written my prediction and sealed it in this envelope.")
    print(SEALED_ENVELOPE)
    print("Think I'll cheat and change it later? You can peek inside")
    print("right now to see that it's already written down!")
    print()

    peeked = False
    while True:
        choice = input("Type P to peek in the envelope, "
                       "or press Enter to start: ").strip().lower()
        if choice.startswith("p") and not peeked:
            peeked = True
            print("\nOkay, just a quick peek...")
            pause()
            print(opened_envelope(prediction))
            print("See? My prediction is already written down.")
            print("Remember it! I'll seal the envelope back up now.")
            pause()
            print(SEALED_ENVELOPE)
        elif choice.startswith("p"):
            print("You already peeked! It still says the same thing.")
        else:
            break

    circled = []      # list of (row, col)
    crossed = set()   # set of (row, col)

    while len(circled) < size:
        show_grid(grid, size, circled, crossed)
        if not circled:
            prompt = "Pick any number on the board: "
        else:
            prompt = "Pick a number that isn't crossed out: "
        choice = input(prompt).strip()

        if not choice.isdigit() or not 1 <= int(choice) <= size * size:
            print(f"Oops! Type a number from 1 to {size * size}.")
            continue

        r, c = divmod(int(choice) - 1, size)

        if (r, c) in circled:
            print("You already circled that one! Pick a different number.")
            continue
        if (r, c) in crossed:
            print("That one's crossed out! Pick a number without an X.")
            continue

        circled.append((r, c))
        for i in range(size):
            if (r, i) != (r, c) and (r, i) not in circled:
                crossed.add((r, i))
            if (i, c) != (r, c) and (i, c) not in circled:
                crossed.add((i, c))

    show_grid(grid, size, circled, crossed)
    numbers = [grid[r][c] for r, c in circled]
    total = sum(numbers)

    print("All done! Your circled numbers are: " + ", ".join(map(str, numbers)))
    print()

    tries = 0
    while True:
        answer = input("Add them up. What's your total? ").strip()
        if answer.isdigit() and int(answer) == total:
            print(f"Yes! Your total is {total}.")
            break
        tries += 1
        if tries >= 2:
            print("Let's add them together:")
            print("    " + " + ".join(map(str, numbers)) + f" = {total}")
            break
        print("Hmm, not quite. Try adding them again!")

    print()
    print("Now let's open my secret envelope", end="", flush=True)
    for _ in range(3):
        pause()
        print(".", end="", flush=True)
    pause()
    print()
    print(opened_envelope(prediction))
    pause(0.5)
    print(f"I predicted {prediction}, and you got {total}!")
    if peeked:
        print("You even saw my prediction BEFORE you picked your numbers,")
        print("and you STILL got it. No cheating, just magic!")
    print("I READ YOUR MIND!")
    print()


def main():
    show_intro()
    size = random.choice(BOARD_SIZES)

    while True:
        play_round(size)
        again = input("Want to play again? (y/n) ").strip().lower()
        if not again.startswith("y"):
            print("\nThanks for playing! Try the trick on your friends!")
            break
        # Pick a different board each round so the prediction isn't the
        # same twice in a row.
        old_size = size
        size = random.choice([s for s in BOARD_SIZES if s != old_size])
        bigger = "BIGGER" if size > old_size else "smaller"
        print(f"\nLet's try a {bigger} {size}x{size} board this time!\n")


if __name__ == "__main__":
    main()
