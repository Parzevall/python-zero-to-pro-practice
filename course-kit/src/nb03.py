import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB03", title="Conditionals", intro="""
    Making your program choose: `if` / `elif` / `else`, combining conditions,
    truthiness, the one-line conditional expression, `match`, and `pass`.
    Values that would come from `input()` in a real program are given to you
    as variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "If `temp` is above 30 print `hot`, otherwise print `ok`.",
     given="temp = 33",
     solution='if temp > 30:\n    print("hot")\nelse:\n    print("ok")')

nb.q("Output-match", "Print `even` or `odd` for `n`, in one line.",
     given="n = 17",
     solution='print("even" if n % 2 == 0 else "odd")')

nb.q("Real-life", "A shop gives members a discount. Print `Member price` if `is_member` is true, otherwise `Full price`.",
     given="is_member = True",
     solution='print("Member price" if is_member else "Full price")')

nb.q("Puzzle", "Print `Caught!` if `speed` is over the `limit`, otherwise `Safe`.",
     given="speed = 72\nlimit = 50",
     solution='print("Caught!" if speed > limit else "Safe")')

nb.q("Real-life", """
    The sign-up form left `name` empty. Print `Welcome, ` followed by the name,
    or `Welcome, guest` when the name is empty.
""",
     given='name = ""',
     solution='print("Welcome,", name if name else "guest")')

# ------------------------------------------------------------ Combine
nb.q("Build", """
    Turn `score` into a letter: 90 or more is `A`, 80 or more `B`, 70 or more
    `C`, 60 or more `D`, anything lower `F`. Print the letter.
""",
     given="score = 83",
     solution='if score >= 90:\n    print("A")\nelif score >= 80:\n    print("B")\n'
              'elif score >= 70:\n    print("C")\nelif score >= 60:\n    print("D")\n'
              'else:\n    print("F")')

nb.q("Real-life", """
    Cinema tickets: under 5 is free, ages 5 to 12 cost 6, 65 and over cost 7,
    everyone else pays 12. Print the price for `age`.
""",
     given="age = 65",
     solution='if age < 5:\n    price = 0\nelif age <= 12:\n    price = 6\n'
              'elif age >= 65:\n    price = 7\nelse:\n    price = 12\nprint("Ticket:", price)')

nb.q("Real-life", """
    Shipping is free for orders of 50 or more, **or** for members. Otherwise it
    costs 4.99. Print the shipping cost.
""",
     given="total = 42.5\nis_member = False",
     solution="if total >= 50 or is_member:\n    print(0)\nelse:\n    print(4.99)")

nb.q("Real-life", """
    A password is `Strong` if it has at least 8 characters **and** contains at
    least one capital letter, otherwise `Weak`. Print the verdict.
""",
     given='password = "sunny2024day"',
     solution='if len(password) >= 8 and password != password.lower():\n'
              '    print("Strong")\nelse:\n    print("Weak")')

nb.q("Puzzle", """
    Print `weekend` if `day` is `"Sat"` or `"Sun"`, otherwise `weekday`.
""",
     given='day = "Mon"',
     solution='if day == "Sat" or day == "Sun":\n    print("weekend")\nelse:\n    print("weekday")')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A media player gets a `command`. Use `match`: `start` prints `Playing`,
    `stop` or `quit` prints `Stopped`, `pause` prints `Paused`, anything else
    prints `Unknown command`.
""",
     given='command = "quit"',
     solution='match command:\n    case "start":\n        print("Playing")\n'
              '    case "stop" | "quit":\n        print("Stopped")\n'
              '    case "pause":\n        print("Paused")\n'
              '    case _:\n        print("Unknown command")')

nb.q("Real-life", """
    A customer pays `paid` for a bill of `bill`. Print `Paid in full` if the
    two amounts are the same, otherwise print `Check the amount`. Floats are
    fuzzy, so don't trust `==` here.
""",
     given="bill = 0.3\npaid = 0.1 + 0.2",
     solution='if abs(paid - bill) < 0.01:\n    print("Paid in full")\nelse:\n    print("Check the amount")')

nb.q("Build", """
    Caught speeding! Over the `limit` by up to 10 costs a 50 fine, up to 20
    over costs 100, more than that costs 200, and at or under the limit there
    is no fine. It's the driver's birthday, so a fine is **halved**. Print the
    fine, or `No fine`.
""",
     given="speed = 68\nlimit = 50\nbirthday = True",
     solution='over = speed - limit\n'
              'if over <= 0:\n    print("No fine")\nelse:\n'
              '    if over <= 10:\n        fine = 50\n    elif over <= 20:\n        fine = 100\n'
              '    else:\n        fine = 200\n'
              '    if birthday:\n        fine = fine / 2\n'
              '    print("Fine:", fine)')

nb.q("Real-life", """
    An ATM withdrawal. If `pin_ok` is false print `Wrong PIN`. Otherwise, if
    `amount` is more than `balance` print `Insufficient funds`, otherwise print
    the new balance.
""",
     given="balance = 120\namount = 150\npin_ok = True",
     solution='if not pin_ok:\n    print("Wrong PIN")\n'
              'elif amount > balance:\n    print("Insufficient funds")\n'
              'else:\n    print("New balance:", balance - amount)')

nb.q("Puzzle", """
    FizzBuzz for a single number: print `FizzBuzz` if `n` divides by both 3 and
    5, `Fizz` if only by 3, `Buzz` if only by 5, otherwise the number itself.
""",
     given="n = 15",
     solution='if n % 3 == 0 and n % 5 == 0:\n    print("FizzBuzz")\n'
              'elif n % 3 == 0:\n    print("Fizz")\n'
              'elif n % 5 == 0:\n    print("Buzz")\nelse:\n    print(n)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Classify a triangle from sides `a`, `b`, `c`. If one side is as long as the
    other two together (or longer) it's `invalid`. Otherwise print
    `equilateral`, `isosceles` or `scalene`, and on a second line print
    `right-angled` if `a² + b² == c²` (only when valid).
""",
     given="a = 3\nb = 4\nc = 5",
     solution='if a + b <= c or a + c <= b or b + c <= a:\n    print("invalid")\nelse:\n'
              '    if a == b == c:\n        print("equilateral")\n'
              '    elif a == b or b == c or a == c:\n        print("isosceles")\n'
              '    else:\n        print("scalene")\n'
              '    if a ** 2 + b ** 2 == c ** 2:\n        print("right-angled")')

nb.q("Real-life", """
    Validate the date `day`/`month`/`year`. Months with 30 days (April, June,
    September, November) have at most 30 days, February has 28 (29 in a leap
    year: divisible by 4, except by 100, unless also by 400), the rest have 31.
    Print `Valid` or `Invalid date` plus the largest allowed day.
""",
     given="day = 29\nmonth = 2\nyear = 1900",
     solution='match month:\n    case 4 | 6 | 9 | 11:\n        max_day = 30\n'
              '    case 2:\n'
              '        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):\n'
              '            max_day = 29\n        else:\n            max_day = 28\n'
              '    case _:\n        max_day = 31\n'
              'if 1 <= day <= max_day:\n    print("Valid")\nelse:\n'
              '    print("Invalid date, the month only has", max_day, "days")')

nb.q("Puzzle", """
    Rock, paper, scissors. Rock beats scissors, scissors beats paper, paper
    beats rock. Print `Tie`, `Player 1 wins` or `Player 2 wins`.
""",
     given='p1 = "paper"\np2 = "scissors"',
     solution='if p1 == p2:\n    print("Tie")\n'
              'elif (p1 == "rock" and p2 == "scissors") or (p1 == "scissors" and p2 == "paper") or (p1 == "paper" and p2 == "rock"):\n'
              '    print("Player 1 wins")\nelse:\n    print("Player 2 wins")')

nb.q("Real-life", """
    Parcel prices depend on `zone` and `weight` (kg). Use `match` on `zone`:
    `local` costs 5, `eu` costs 9 up to 2 kg and 15 above that, `world` costs
    25, and any other zone prints `Unknown zone`. Print the price, and add a
    line `Heavy parcel` if the weight is over 20 kg.
""",
     given='zone = "eu"\nweight = 3.5',
     solution='match zone:\n    case "local":\n        price = 5\n'
              '    case "eu" if weight <= 2:\n        price = 9\n'
              '    case "eu":\n        price = 15\n'
              '    case "world":\n        price = 25\n'
              '    case _:\n        price = None\n'
              'if price is None:\n    print("Unknown zone")\nelse:\n    print("Price:", price)\n'
              'if weight > 20:\n    print("Heavy parcel")')

# ------------------------------------------------------------ Q20 project
nb.project("Tax Day", story="""
    You're building the tax calculator for a tiny country. Tax is
    **progressive**: each slice of income is taxed at its own rate. Up to
    10,000 is tax free, 10,000 to 40,000 pays 10%, 40,000 to 90,000 pays 20%,
    and everything above 90,000 pays 30%. Each step builds on the one before.
""",
     given='income = 65000\nstatus = "married"\nalready_paid = 9000',
     steps=[
         ("Print which bracket `income` falls in: `Bracket 1`, `Bracket 2`, `Bracket 3` or `Bracket 4`.",
          'if income <= 10000:\n    bracket = 1\nelif income <= 40000:\n    bracket = 2\n'
          'elif income <= 90000:\n    bracket = 3\nelse:\n    bracket = 4\nprint("Bracket", bracket)'),
         ("Work out the tax in each band (a band with no income pays 0) and print "
          "the three taxed bands. `max(0, ...)` is handy.",
          "band2 = max(0, min(income, 40000) - 10000) * 0.10\n"
          "band3 = max(0, min(income, 90000) - 40000) * 0.20\n"
          "band4 = max(0, income - 90000) * 0.30\n"
          'print("10% band:", band2)\nprint("20% band:", band3)\nprint("30% band:", band4)'),
         ("Print the total tax and the effective rate (total tax as a percentage of income, 1 decimal place).",
          'total_tax = band2 + band3 + band4\n'
          'print("Total tax:", total_tax)\n'
          'print("Effective rate:", round(total_tax / income * 100, 1), "%")'),
         ("A `match` on `status` gives a credit: `single` 0, `married` 1500, "
          "`student` or `retired` 800, anything else 0. Subtract it from the tax "
          "(never below 0) and print the tax after credit.",
          'match status:\n    case "married":\n        credit = 1500\n'
          '    case "student" | "retired":\n        credit = 800\n'
          '    case _:\n        credit = 0\n'
          'tax_due = max(0, total_tax - credit)\nprint("Tax after credit:", tax_due)'),
         ("Compare with `already_paid`. Print `Refund: ...` if too much was paid, "
          "`Owe: ...` if too little, or `All settled` if exactly right.",
          'if already_paid > tax_due:\n    print("Refund:", already_paid - tax_due)\n'
          'elif already_paid < tax_due:\n    print("Owe:", tax_due - already_paid)\n'
          'else:\n    print("All settled")'),
     ])

nb.build()
