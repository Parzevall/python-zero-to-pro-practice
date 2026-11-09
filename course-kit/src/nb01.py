import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB01", title="Variables, Types & Operators", intro="""
    Names that hold values, the basic types of value, and the operators that
    combine them. You only need `print()` from NB00: no `if`, no loops, no
    lists yet. Values that would come from `input()` in a real program are
    given to you as text, so you still practise converting them.
""")

# ------------------------------------------------------------ Warm-up (1 line)
nb.q("Real-life", "You buy `qty` tickets at `price` each. Print the total cost.",
     given="price = 4.5\nqty = 3",
     solution="print(price * qty)")

nb.q("Output-match", "What is 7 to the power of 4? Print it.",
     solution="print(7 ** 4)")

nb.q("Real-life", """
    `text_age` came from a sign-up form, so it's text. Print the person's age
    **next year** as a number.
""",
     given='text_age = "36"',
     solution="print(int(text_age) + 1)")

nb.q("Output-match", "Print a divider line made of 30 `=` signs, without typing 30 of them.",
     solution='print("=" * 30)')

nb.q("Real-life", "Three people bid on a bike. Print the winning (highest) bid.",
     given="bid_a = 120\nbid_b = 95\nbid_c = 140",
     solution="print(max(bid_a, bid_b, bid_c))")

# ------------------------------------------------------- Combine (2-4 lines)
nb.q("Build", """
    Convert `celsius` to Fahrenheit (`F = C × 9 / 5 + 32`) and print it.
    On a second line, print `True` if it's above 90 °F, otherwise `False`.
""",
     given="celsius = 34",
     solution="fahrenheit = celsius * 9 / 5 + 32\nprint(fahrenheit)\nprint(fahrenheit > 90)")

nb.q("Real-life", """
    3 pizzas with 8 slices each are shared fairly between 7 friends. Print how
    many whole slices each friend gets and how many are left over, as one
    sentence like the expected output.
""",
     given="pizzas = 3\nslices_per_pizza = 8\nfriends = 7",
     solution="slices = pizzas * slices_per_pizza\n"
              "each = slices // friends\n"
              "left = slices % friends\n"
              'print("Each friend gets", each, "slices,", left, "left over")')

nb.q("Build", "Someone poured the drinks into the wrong cups. Swap them in **one line**, then print both cups.",
     given='cup_a = "tea"\ncup_b = "coffee"',
     solution="cup_a, cup_b = cup_b, cup_a\nprint(cup_a, cup_b)")

nb.q("Real-life", """
    The coffee price came from a website form as text. Print the cost of
    `qty` coffees as a number.
""",
     given='price = "4.50"\nqty = 2',
     solution="print(float(price) * qty)")

nb.q("Real-life", """
    A quick email sanity check: print `True` if `email` contains an `@` **and**
    a `.` **and** no spaces, otherwise `False`. One expression.
""",
     given='email = "ada@example.com"',
     solution='print("@" in email and "." in email and " " not in email)')

# ------------------------------------------------ Small real tasks (5-8 lines)
nb.q("Real-life", """
    Dinner costs `bill`. Add a 15% tip, then split it evenly between `people`.
    Print the total with tip and what each person pays, both rounded to 2
    decimal places, labelled like the expected output.
""",
     given="bill = 84.60\npeople = 4",
     solution="total = round(bill * 1.15, 2)\n"
              "each = round(total / people, 2)\n"
              'print("Total with tip:", total)\n'
              'print("Each person pays:", each)')

nb.q("Real-life", """
    A road trip of `distance_km`. The car uses `litres_per_100km`, and fuel
    costs `price_per_litre`. Print the litres needed (1 decimal place) and the
    fuel cost (2 decimal places).
""",
     given="distance_km = 420\nlitres_per_100km = 6.5\nprice_per_litre = 1.89",
     solution="litres = distance_km * litres_per_100km / 100\n"
              "cost = litres * price_per_litre\n"
              'print("Litres needed:", round(litres, 1))\n'
              'print("Fuel cost:", round(cost, 2))')

nb.q("Build", """
    A year is a leap year if it divides by 4, **except** years that divide by
    100, **unless** they also divide by 400. Without `if`, print whether each
    of the three years is a leap year.
""",
     given="year_1 = 2024\nyear_2 = 1900\nyear_3 = 2000",
     solution="leap_1 = year_1 % 4 == 0 and (year_1 % 100 != 0 or year_1 % 400 == 0)\n"
              "leap_2 = year_2 % 4 == 0 and (year_2 % 100 != 0 or year_2 % 400 == 0)\n"
              "leap_3 = year_3 % 4 == 0 and (year_3 % 100 != 0 or year_3 % 400 == 0)\n"
              "print(year_1, leap_1)\nprint(year_2, leap_2)\nprint(year_3, leap_3)")

nb.q("Real-life", """
    An app shows height in feet and inches. Convert `height_m` (1 inch is
    0.0254 m, 1 foot is 12 inches). Print whole feet and the remaining inches
    rounded to a whole number.
""",
     given="height_m = 1.75",
     solution="total_inches = height_m / 0.0254\n"
              "feet = int(total_inches // 12)\n"
              "inches = round(total_inches % 12)\n"
              'print(feet, "ft", inches, "in")')

nb.q("Real-life", """
    A customer pays `paid` for something costing `price`. Print the change as
    whole euros and cents. Floats are fuzzy with money, so convert the change
    to whole cents first.
""",
     given="price = 13.70\npaid = 20",
     solution="change_cents = round((paid - price) * 100)\n"
              "euros = change_cents // 100\n"
              "cents = change_cents % 100\n"
              'print("Change:", euros, "euros and", cents, "cents")')

# ----------------------------------------------- Puzzles & builds (8-15 lines)
nb.q("Puzzle", """
    Reverse the 3-digit number `n` (472 becomes 274) using only `//` and `%`,
    then print it **as a number**, and print it doubled to prove it is one.
""",
     given="n = 472",
     solution="hundreds = n // 100\n"
              "tens = n // 10 % 10\n"
              "ones = n % 10\n"
              "reversed_n = ones * 100 + tens * 10 + hundreds\n"
              "print(reversed_n)\n"
              "print(reversed_n * 2)")

nb.q("Puzzle", """
    A night bus leaves at `hour`:`minute` and the trip takes `trip_minutes`.
    Print the arrival time on a 24-hour clock, wrapping past midnight, with
    two digits for hours and minutes (like `07:05`). No `if`, no f-strings.

    *Trick:* the tens digit of a number is `x // 10`, the ones digit is `x % 10`.
""",
     given="hour = 22\nminute = 45\ntrip_minutes = 135",
     solution="total = hour * 60 + minute + trip_minutes\n"
              "new_hour = total // 60 % 24\n"
              "new_minute = total % 60\n"
              "hh = str(new_hour // 10) + str(new_hour % 10)\n"
              "mm = str(new_minute // 10) + str(new_minute % 10)\n"
              'print("Arrives at " + hh + ":" + mm)')

nb.q("Build", """
    A cash machine pays out `amount` euros using the fewest notes: 50s first,
    then 20s, 10s and 5s, and anything left in 1-euro coins. Print how many of
    each, one per line, labelled like the expected output.
""",
     given="amount = 385",
     solution="fifties = amount // 50\n"
              "rest = amount % 50\n"
              "twenties = rest // 20\n"
              "rest = rest % 20\n"
              "tens = rest // 10\n"
              "rest = rest % 10\n"
              "fives = rest // 5\n"
              "coins = rest % 5\n"
              'print("50s:", fifties)\nprint("20s:", twenties)\nprint("10s:", tens)\n'
              'print("5s:", fives)\nprint("coins:", coins)')

nb.q("Build", """
    A delivery drone flies in a straight line from point A to point B. Use
    `import math` and Pythagoras (`distance = √(dx² + dy²)`) to print the
    distance. The battery starts at 100% and uses `drain_per_unit` % per unit
    flown: print the battery left, rounded to 1 decimal place, and `True` if
    it can still make the same trip back.
""",
     given="ax, ay = 2, 3\nbx, by = 14, 8\ndrain_per_unit = 0.4",
     solution="import math\n"
              "dx = bx - ax\n"
              "dy = by - ay\n"
              "distance = math.sqrt(dx ** 2 + dy ** 2)\n"
              "battery = 100 - distance * drain_per_unit\n"
              'print("Distance:", distance)\n'
              'print("Battery left:", round(battery, 1))\n'
              'print("Can fly back:", battery >= distance * drain_per_unit)')

# ------------------------------------------------------------ Q20 story project
nb.project("Café Closing Time", story="""
    It's 6 pm at *Byte Café* and you're closing up. The till exported today's
    numbers, but **everything came out as text**. Your manager wants the day's
    figures before you go home. Work through the steps; each one builds on the
    variables from the step before.
""",
     given='coffee_price = "3.20"\ncoffees_sold = "48"\n'
           'cake_price = "4.75"\ncakes_sold = "17"\n'
           'sandwich_price = "6.50"\nsandwiches_sold = "22"\n\n'
           "opening_cash = 150.0        # cash put in the till this morning\n"
           'cash_counted = "527.10"     # what you counted tonight\n'
           "tip_jar = 38                # euros in the tip jar\n"
           "staff = 3",
     steps=[
         ("Convert the prices and quantities to numbers and print the sales for "
          "each item, rounded to 2 decimal places.",
          "coffee_sales = round(float(coffee_price) * int(coffees_sold), 2)\n"
          "cake_sales = round(float(cake_price) * int(cakes_sold), 2)\n"
          "sandwich_sales = round(float(sandwich_price) * int(sandwiches_sold), 2)\n"
          'print("Coffee:", coffee_sales)\n'
          'print("Cake:", cake_sales)\n'
          'print("Sandwiches:", sandwich_sales)'),
         ("Print the total sales. Prices include 20% VAT, so the price without VAT "
          "is `total / 1.2`. Print that and the VAT part, both to 2 decimal places.",
          "total_sales = round(coffee_sales + cake_sales + sandwich_sales, 2)\n"
          "without_vat = round(total_sales / 1.2, 2)\n"
          "vat = round(total_sales - without_vat, 2)\n"
          'print("Total sales:", total_sales)\n'
          'print("Without VAT:", without_vat)\n'
          'print("VAT:", vat)'),
         ("The till should hold the opening cash plus today's sales. Print the "
          "difference between what you counted and what should be there (2 decimal "
          "places), and `True` if the till is within 1 cent of balanced.",
          "expected_cash = opening_cash + total_sales\n"
          "difference = round(float(cash_counted) - expected_cash, 2)\n"
          'print("Till difference:", difference)\n'
          'print("Balanced:", abs(difference) < 0.01)'),
         ("Split the tip jar between the staff in whole euros. Whatever can't be "
          "split stays in the jar for tomorrow. Print both.",
          "tip_each = tip_jar // staff\n"
          "tip_left = tip_jar % staff\n"
          'print("Tip each:", tip_each)\n'
          'print("Left for tomorrow:", tip_left)'),
         ("Print the manager's summary exactly like the expected output: a 28-character "
          "`=` line above and below, built with `+` and `str()` (no f-strings yet).",
          'line = "=" * 28\n'
          "print(line)\n"
          'print("BYTE CAFE · DAY SUMMARY")\n'
          'print("Sales: " + str(total_sales) + " EUR")\n'
          'print("Till off by: " + str(difference) + " EUR")\n'
          'print("Tips: " + str(tip_each) + " EUR x " + str(staff))\n'
          "print(line)"),
     ])

nb.build()
