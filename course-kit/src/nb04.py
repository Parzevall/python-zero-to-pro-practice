import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB04", title="Loops", intro="""
    Do something many times without typing it many times: `for` over
    numbers and text, `while` until something happens, and `break` /
    `continue` to steer. Lists aren't taught yet, so you loop over
    strings and `range()`. Data that would be a list is a text like
    `"12,7,30"` that you split once.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Output-match", "Print the numbers 1 to 10 on one line, separated by spaces.",
     solution='for i in range(1, 11):\n    print(i, end=" ")')

nb.q("Output-match", "Print every third number from 3 up to and including 30 on one line.",
     solution='for i in range(3, 31, 3):\n    print(i, end=" ")')

nb.q("Real-life", "A rocket countdown: print 5 down to 1, each on its own line, then `Liftoff!`.",
     solution='for i in range(5, 0, -1):\n    print(i)\nprint("Liftoff!")')

nb.q("Real-life", """
    A phone number is stored with dashes. Print only its digits on one line
    with no spaces between them.
""",
     given='phone = "555-01-23-99"',
     solution='for ch in phone:\n    if ch == "-":\n        continue\n    print(ch, end="")')

nb.q("Output-match", "Print the sum of all the whole numbers from 1 to 100.",
     solution="total = 0\nfor i in range(1, 101):\n    total += i\nprint(total)")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    You save 10 euros every week, starting from `balance`. Print the balance
    after each of 8 weeks, one line per week, like the expected output.
""",
     given="balance = 100",
     solution='for week in range(1, 9):\n    balance += 10\n    print("Week", week, "balance:", balance)')

nb.q("Build", "Count the vowels (`a e i o u`) in the sentence and print the count.",
     given='sentence = "the quick brown fox jumps over the lazy dog"',
     solution='count = 0\nfor ch in sentence:\n    if ch in "aeiou":\n        count += 1\nprint(count)')

nb.q("Puzzle", """
    Print all multiples of 7 from 7 up to and including `limit` on one line,
    then on a new line how many there were.
""",
     given="limit = 49",
     solution='count = 0\nfor n in range(7, limit + 1, 7):\n    print(n, end=" ")\n    count += 1\nprint()\nprint(count)')

nb.q("Real-life", """
    A step counter exported a week of steps as one text. Print how many days
    reached the goal of 8000 steps (8000 counts).
""",
     given='steps = "4200,8100,9500,7999,12000,8000,3000"',
     solution='days = 0\nfor s in steps.split(","):\n    if int(s) >= 8000:\n        days += 1\nprint(days)')

nb.q("Output-match", "Print each letter of the word with its position, counting from 1, like the expected output.",
     given='word = "python"',
     solution='for i, ch in enumerate(word, 1):\n    print(i, ch)')

# ------------------------------------------------------------ Small real tasks
nb.q("Puzzle", """
    FizzBuzz for 1 to 15, all on one line: multiples of 3 print `Fizz`,
    multiples of 5 print `Buzz`, multiples of both print `FizzBuzz`, every
    other number prints itself.
""",
     solution='for i in range(1, 16):\n    if i % 15 == 0:\n        print("FizzBuzz", end=" ")\n'
              '    elif i % 3 == 0:\n        print("Fizz", end=" ")\n'
              '    elif i % 5 == 0:\n        print("Buzz", end=" ")\n'
              '    else:\n        print(i, end=" ")')

nb.q("Real-life", """
    A login allows at most 3 attempts. The attempts typed so far are in
    `tries` (separated by commas). Go through them in order: print
    `Attempt 1: wrong` and so on, and on the right password print
    `Welcome!` and stop. If none of the 3 attempts matched, print `Locked out`.
""",
     given='password = "hunter2"\ntries = "123456,qwerty,letmein,hunter2"',
     solution='n = 0\nfor t in tries.split(","):\n    n += 1\n    if n > 3:\n        print("Locked out")\n        break\n'
              '    if t == password:\n        print("Welcome!")\n        break\n'
              '    print("Attempt " + str(n) + ": wrong")')

nb.q("Real-life", """
    Your savings start at `money` and grow 7% a year. Using a `while` loop,
    print how many whole years until you have at least double the starting
    amount, and the money then, rounded to 2 decimals.
""",
     given="money = 1000.0",
     solution="start = money\nyears = 0\nwhile money < start * 2:\n    money = money * 1.07\n    years += 1\n"
              'print(years, "years")\nprint(round(money, 2))')

nb.q("Output-match", """
    Print a right-angled triangle of `*` with `rows` rows (1 star in the
    first row, 2 in the second, and so on).
""",
     given="rows = 4",
     solution='for r in range(1, rows + 1):\n    for _ in range(r):\n        print("*", end="")\n    print()')

nb.q("Puzzle", """
    A word game: compare `guess` with `secret` letter by letter. Print one
    symbol per position on a single line: `G` if the letters match, `-` if
    not. Then print how many matched.
""",
     given='secret = "crane"\nguess = "crate"',
     solution='hits = 0\nfor s, g in zip(secret, guess):\n    if s == g:\n        print("G", end="")\n        hits += 1\n'
              '    else:\n        print("-", end="")\nprint()\nprint(hits, "matched")')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Print every prime number from 2 to 30 on one line. A number is prime if
    no number from 2 up to just below it divides it evenly.
""",
     solution='for n in range(2, 31):\n    for d in range(2, n):\n        if n % d == 0:\n            break\n'
              '    else:\n        print(n, end=" ")')

nb.q("Puzzle", """
    Print the digit sum of `n` using a `while` loop and `%` / `//` (no
    converting to text), then print how many digits it has.
""",
     given="n = 98765",
     solution='left = n\ntotal = 0\ndigits = 0\nwhile left > 0:\n    total += left % 10\n    left //= 10\n    digits += 1\n'
              'print("Digit sum:", total)\nprint("Digits:", digits)')

nb.q("Puzzle", """
    Collatz: starting from `n`, if it is even halve it, otherwise do
    `3 * n + 1`. Repeat until you reach 1. Print how many steps it took and
    the highest value reached.
""",
     given="n = 27",
     solution='steps = 0\nhighest = n\nwhile n != 1:\n    if n % 2 == 0:\n        n = n // 2\n    else:\n        n = 3 * n + 1\n'
              '    steps += 1\n    if n > highest:\n        highest = n\nprint("Steps:", steps)\nprint("Highest:", highest)')

nb.q("Puzzle", """
    Run-length encode the string: each run of the same letter becomes the
    letter followed by its length, so `aaabcc` becomes `a3b1c2`. Print the result.
""",
     given='text = "aaabccdddd"',
     solution='result = ""\ncurrent = text[0]\ncount = 0\nfor ch in text:\n    if ch == current:\n        count += 1\n'
              '    else:\n        result += current + str(count)\n        current = ch\n        count = 1\n'
              'result += current + str(count)\nprint(result)')

# ------------------------------------------------------------ Project
nb.project("Guessing Game Replay", story="""
    A friend played a number guessing game and you have the log. The secret
    number and all their guesses (separated by commas) are below. Replay the
    game step by step.
""",
     given='secret = 37\nguesses = "50,25,31,40,37,12"',
     steps=[
         ("Print each guess on its own line, numbered from 1, like the expected output.",
          'for i, g in enumerate(guesses.split(","), 1):\n    print("Guess", i, "is", g)'),
         ("For each guess print `too high`, `too low` or `correct`, and stop replaying at the correct guess.",
          'for g in guesses.split(","):\n    g = int(g)\n    if g > secret:\n        print(g, "too high")\n'
          '    elif g < secret:\n        print(g, "too low")\n    else:\n        print(g, "correct")\n        break'),
         ("Count the guesses it took. If no guess was correct, the loop should say so with `else`. Print the verdict.",
          'tries = 0\nfor g in guesses.split(","):\n    tries += 1\n    if int(g) == secret:\n        print("Won in", tries, "guesses")\n        break\n'
          'else:\n    print("Never found it")'),
         ("A perfect player halves the range each time (1 to 100 needs at most 7 guesses). Using a `while` loop, print how many halvings it takes to get from 100 down to 1 (whole division by 2).",
          'size = 100\nhalvings = 0\nwhile size > 1:\n    size //= 2\n    halvings += 1\nprint("Halvings:", halvings)'),
     ])

nb.build()
