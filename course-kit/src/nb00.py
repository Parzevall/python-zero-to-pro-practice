import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB00", title="Start Here", intro="""
    Your very first notebook. The only tool you need is `print()`: several
    values at once, `sep=` between them, `end=` after them, and `#` comments.
    Write your code, run the cell, compare with the expected output, then open
    the solution.
""")

# ------------------------------------------------------------ Warm-up (1 line)
nb.q("Output-match", "Greet the world: print `Hello, Python!` exactly, capital letters and punctuation included.",
     solution='print("Hello, Python!")')

nb.q("Real-life", "You're writing a text to a friend. Print `On my way, be there in 10 minutes!`",
     solution='print("On my way, be there in 10 minutes!")')

nb.q("Output-match", "Print the result of 12 times 12. Let Python do the maths.",
     solution="print(12 * 12)")

nb.q("Output-match", "Print `red | green | blue` with **one** `print()` call, giving it three separate values and using `sep=`.",
     solution='print("red", "green", "blue", sep=" | ")')

nb.q("Puzzle", "A pizza has 8 slices and 5 friends each eat 1. Print how many slices are left, calculated inside `print()`.",
     solution="print(8 - 5)")

# ------------------------------------------------------- Combine (2-4 lines)
nb.q("Real-life", "A shop receipt needs two lines: `Coffee` on the first and `Croissant` on the second. Use two `print()` calls.",
     solution='print("Coffee")\nprint("Croissant")')

nb.q("Puzzle", """
    Print `Loading...` and then `Done!` so that both appear on the **same line**
    (separated by a single space), using two `print()` calls.
""",
     solution='print("Loading...", end=" ")\nprint("Done!")')

nb.q("Build", "Print a date as `2025/12/31` with one `print()` call. The numbers must be given as separate values and `sep=` does the slashes.",
     solution='print(2025, 12, 31, sep="/")')

nb.q("Real-life", """
    Add a comment line above your code that says `Greeting for the sign`, then
    print `Welcome to Pythonville` on one line and `Population: 1500` on the
    next. The comment must not show in the output.
""",
     solution='# Greeting for the sign\nprint("Welcome to Pythonville")\nprint("Population:", 1500)')

nb.q("Puzzle", """
    Count down to a rocket launch on a **single line**: `3 2 1 Liftoff!`, using
    four `print()` calls and `end=`.
""",
     solution='print(3, end=" ")\nprint(2, end=" ")\nprint(1, end=" ")\nprint("Liftoff!")')

# ------------------------------------------------ Small real tasks (5-8 lines)
nb.q("Real-life", """
    A phone number is shown as `555-867-5309`. Print it with one `print()`
    call from three separate numbers and `sep=`.
    Then print your own two-line address label: `Ada Lovelace` and `12 Analytical Street`.
""",
     solution='print(555, 867, 5309, sep="-")\nprint("Ada Lovelace")\nprint("12 Analytical Street")')

nb.q("Output-match", """
    Print this smiley box with three `print()` calls, exactly as shown:

    ```text
    +-----+
    | ^_^ |
    +-----+
    ```
""",
     solution='print("+-----+")\nprint("| ^_^ |")\nprint("+-----+")')

nb.q("Puzzle", """
    Print the multiplication facts 6 x 7 on one line as `6 x 7 = 42`, but
    let Python compute the 42. Use `print()` with separate values (a number,
    text, a number, text, a calculation).
""",
     solution='print(6, "x", 7, "=", 6 * 7)')

nb.q("Real-life", """
    A shopping list on one line: `milk, eggs, bread.` Use a separate `print()`
    for each item and `end=` for the gaps and the final dot.
""",
     solution='print("milk", end=", ")\nprint("eggs", end=", ")\nprint("bread", end=".")\nprint()')

nb.q("Real-life", """
    A café menu board with prices. Print three lines like `Espresso ..... 2.5`
    (name, five dots, price) using `sep=` so you don't type the dots between
    the name and price yourself: Espresso 2.5, Latte 3.75, Tea 2.
""",
     solution='print("Espresso", 2.5, sep=" ..... ")\nprint("Latte", 3.75, sep=" ..... ")\nprint("Tea", 2, sep=" ..... ")')

# ------------------------------------------------ Puzzles & builds (8-15 lines)
nb.q("Build", """
    Draw a small house with `print()`: a triangle roof of three lines and a
    two-line body, centred like this:

    ```text
      /\\
     /  \\
    /____\\
    |    |
    |____|
    ```
""",
     solution='print("  /\\\\")\nprint(" /  \\\\")\nprint("/____\\\\")\nprint("|    |")\nprint("|____|")')

nb.q("Real-life", """
    A mini timetable. Print a header line `Time  Class`, a line of 11 dashes,
    and then three rows: `9:00  Maths`, `10:30  Art`, `13:00  Python`.
    Each row is the time, two spaces, and the class name, made from two values
    and `sep=`.
""",
     solution='print("Time", "Class", sep="  ")\nprint("-----------")\n'
              'print("9:00", "Maths", sep="  ")\nprint("10:30", "Art", sep="  ")\nprint("13:00", "Python", sep="  ")')

nb.q("Puzzle", """
    Print the sum, difference, product and quotient of 20 and 4 on **one
    line**, with ` | ` between the four results (all four from one `print()`).
    Then, on the next line, print `Done`.
""",
     solution='print(20 + 4, 20 - 4, 20 * 4, 20 / 4, sep=" | ")\nprint("Done")')

nb.q("Output-match", """
    A "typing" effect: print the letters `P`, `y`, `t`, `h`, `o`, `n` with one
    `print()` each so they join into the word `Python`, followed by `!!!` on
    the same line, then a final line `Ready.`
    Use separate `print()` calls with `end=""` where needed.
""",
     solution='print("P", end="")\nprint("y", end="")\nprint("t", end="")\nprint("h", end="")\n'
              'print("o", end="")\nprint("n", end="")\nprint("!!!")\nprint("Ready.")')

# ------------------------------------------------------------ Q20 story project
nb.project("Business Card", story="""
    You're a freelance developer printing your first business card at the
    copy shop, but the printer only understands `print()`. Build the card
    one piece at a time with `print()`, `sep=` and `end=`.
""",
     steps=[
         ("Print the top border: a line of 24 `=` characters, without typing all 24 by hand.",
          'print("=" * 24)'),
         ("Print your name `Sam Rivera` on one line and your job `Freelance Python Developer` on the next.",
          'print("Sam Rivera")\nprint("Freelance Python Developer")'),
         ("Print the contact line `Phone: 555-0142`.",
          'print("Phone: 555-0142")'),
         ("Print `Email: sam@rivera.dev` and `Web: rivera.dev` on one line, separated by ` | `, in a single `print()`.",
          'print("Email: sam@rivera.dev", "Web: rivera.dev", sep=" | ")'),
         ("Print the closing slogan `Code that works.` followed on the **same line** by ` Thanks!`, using two prints and `end=`, then add the bottom border of 24 `=`.",
          'print("Code that works.", end="")\nprint(" Thanks!")\nprint("=" * 24)'),
     ])

nb.build()
