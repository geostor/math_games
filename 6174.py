"""The 6174 trick (Kaprekar's routine).

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
      you from ever reaching 6174.
    - Any valid starting number reaches 6174 within 7 turns.
    - The routine is named after the Indian mathematician D. R. Kaprekar,
      who discovered it in 1949.

Source: https://www.learn-with-math-games.com/math-tricks-for-kids.html
"""

raw_code = input("Enter a 4 digit non-repeating code: ").strip()

if len(raw_code) != 4 or not raw_code.isdigit() or len(set(raw_code)) == 1:
    print("Please enter exactly 4 digits that are not all the same.")
    raise SystemExit

current = int(raw_code)
turns = 0

while current != 6174:
    # zfill keeps leading zeros, e.g. 999 -> "0999"
    digits = [int(d) for d in str(current).zfill(4)]

    largest_digits = sorted(digits, reverse=True)  # copy sorted big -> small
    smallest_digits = sorted(digits)  # copy sorted small -> big

    largest = int("".join(map(str, largest_digits)))
    smallest = int("".join(map(str, smallest_digits)))

    current = largest - smallest
    turns += 1

    print(f"Turn {turns}: {largest:04d} - {smallest:04d} = {current:04d}")

print(f"\nReached 6174 in {turns} turn(s).")
