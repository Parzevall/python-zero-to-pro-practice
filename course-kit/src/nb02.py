import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB02", title="Strings", intro="""
    Text is everywhere: usernames, emails, receipts, product codes. Here you
    slice it, clean it, search it and format it. You only use what NB00 to NB02
    teach: no `if`, no loops, no lists, no functions. Data that would come from
    a user or a file is given to you as variables.
""")

# ------------------------------------------------------------ Warm-up (1 line)
nb.q("Real-life", "A sign-up form gave you a sloppy name. Print it without the outer spaces and in title case.",
     given='name = "  ada lovelace "',
     solution="print(name.strip().title())")

nb.q("Output-match", "Print the last character of the product code.",
     given='code = "PY-4821-X"',
     solution="print(code[-1])")

nb.q("Build", "Using **one** `print()` and an escape sequence, print a two-line message: `Dear Sam,` on the first line and `See you at 6.` on the second.",
     solution='print("Dear Sam,\\nSee you at 6.")')

nb.q("Real-life", "Emails are case-insensitive. Print this one in lowercase.",
     given='email = "ADA@Example.COM"',
     solution="print(email.lower())")

nb.q("Output-match", "Print how many characters the message has (spaces count).",
     given='message = "see you at the cafe"',
     solution="print(len(message))")

# ------------------------------------------------------- Combine (2-4 lines)
nb.q("Puzzle", """
    Print `word` reversed. On a second line print whether it reads the same
    both ways.
""",
     given='word = "level"',
     solution="backwards = word[::-1]\nprint(backwards)\nprint(word == backwards)")

nb.q("Real-life", """
    Build a username: the first letter of `first` followed by all of `last`,
    all in lowercase.
""",
     given='first = "Grace"\nlast = "HOPPER"',
     solution="username = first[0] + last\nprint(username.lower())")

nb.q("Real-life", """
    Print the extension of this file in lowercase, without the dot. Careful:
    the name has more than one dot.
""",
     given='filename = "holiday.photos.JPG"',
     solution='dot = filename.rfind(".")\nprint(filename[dot + 1:].lower())')

nb.q("Real-life", """
    A chat message arrived with messy spacing. Print it with exactly one space
    between the words and none at the ends.
""",
     given='message = "  too    many   spaces  here "',
     solution='print(" ".join(message.split()))')

nb.q("Output-match", """
    On three lines print: how many times `go` appears in `chant`, the position
    of the first `gadget`, and the position of `stop` (which isn't there).
    Use `find` for both positions.
""",
     given='chant = "go go gadget go"',
     solution='print(chant.count("go"))\nprint(chant.find("gadget"))\nprint(chant.find("stop"))')

# ------------------------------------------------ Small real tasks (5-8 lines)
nb.q("Real-life", """
    Mask the card number so only the last 4 digits show, the rest replaced by
    `*`, and print it. On a second line print the masked text's length.
""",
     given='card = "4929123456785678"',
     solution='masked = "*" * (len(card) - 4) + card[-4:]\nprint(masked)\nprint(len(masked))')

nb.q("Real-life", """
    Print a receipt line with an f-string: the item left-aligned in 10
    characters, the quantity right-aligned in 3, then ` x `, then the price
    right-aligned in 6 with 2 decimals. Then print the grand total with a
    thousands separator and 2 decimals.
""",
     given='item = "Coffee"\nqty = 12\nprice = 3.5\ntotal = 1234567.891',
     solution='print(f"{item:<10}{qty:>3} x {price:>6.2f}")\nprint(f"Total: {total:,.2f}")')

nb.q("Real-life", """
    A warehouse scanner checks codes. For each of the three values print the
    result of the right check: `code` only letters and digits, `digits` only
    digits, and `spaces` only whitespace. Print the three results on separate
    lines, then the result of `"".isdigit()`.
""",
     given='code = "AB12"\ndigits = "2024"\nspaces = "   "',
     solution='print(code.isalnum())\nprint(digits.isdigit())\nprint(spaces.isspace())\nprint("".isdigit())')

nb.q("Puzzle", """
    Shift the letter `letter` forward by `shift` places in the alphabet and
    print the new letter. Then print its position in the alphabet (`a` is 1)
    before the shift.
""",
     given='letter = "c"\nshift = 3',
     solution='print(chr(ord(letter) + shift))\nprint(ord(letter) - ord("a") + 1)')

nb.q("Real-life", """
    A date arrives as `2024-11-09`. Print it as `09/11/2024` using slicing and
    `+`. Then print everything from the 6th character on to the very end,
    asking for far too many characters (slice up to 100).
""",
     given='date = "2024-11-09"',
     solution='day = date[8:]\nmonth = date[5:7]\nyear = date[:4]\nprint(day + "/" + month + "/" + year)\nprint(date[5:100])')

# ----------------------------------------------- Puzzles & builds (8-15 lines)
nb.q("Real-life", """
    Take apart this email. Print the domain (everything after the `@`), how
    many dots the domain has, and the domain in uppercase. Then print where a
    `#` would be found in the email, using a method that answers `-1`
    instead of crashing.
""",
     given='email = "ada.lovelace@mail.example.com"',
     solution='at = email.index("@")\n'
              'domain = email[at + 1:]\n'
              'print(domain)\n'
              'print(domain.count("."))\n'
              'print(domain.upper())\n'
              'print(email.find("#"))')

nb.q("Puzzle", """
    Is this phrase a palindrome if you ignore case, spaces, commas and
    colons? Build a cleaned version (all lowercase, those characters removed),
    print it, then print `True` or `False` with one comparison.
""",
     given='phrase = "A man, a plan, a canal: Panama"',
     solution='cleaned = phrase.lower().replace(" ", "").replace(",", "").replace(":", "")\n'
              'print(cleaned)\n'
              'print(cleaned == cleaned[::-1])')

nb.q("Build", """
    Print a small name badge. The width is stored in `width`. Print a line of
    `*` that wide, the name centred in that width inside an f-string with a
    nested width, `name` in uppercase, and another line of `*`. Finally print
    `width=` and its value using the debugging form of an f-string.
""",
     given='name = "Ada Lovelace"\nwidth = 21',
     solution='line = "*" * width\n'
              'print(line)\n'
              'print(f"{name.upper():^{width}}")\n'
              'print(line)\n'
              'print(f"{width=}")')

nb.q("Puzzle", """
    A spy shifted every letter of a secret word **3 places forward**. Undo it:
    build the original word letter by letter with `ord`, `chr` and indexing,
    and print it. Then print `repr` of it (using `!r` in an f-string) and
    whether `"Z" < "a"` is true, the way Python orders letters.
""",
     given='coded = "Khoor"',
     solution='a = chr(ord(coded[0]) - 3)\n'
              'b = chr(ord(coded[1]) - 3)\n'
              'c = chr(ord(coded[2]) - 3)\n'
              'd = chr(ord(coded[3]) - 3)\n'
              'e = chr(ord(coded[4]) - 3)\n'
              'word = a + b + c + d + e\n'
              'print(word)\n'
              'print(f"{word!r}")\n'
              'print("Z" < "a")')

# ------------------------------------------------------------ Q20 story project
nb.project("Username Generator", story="""
    You're setting up accounts for new employees at a company. The HR export
    gives you messy text, and every account needs a clean username, initials,
    a masked email and an ID card. Each step builds on the variables from the
    step before.
""",
     given='first = "  grace "\nlast = "HOPPER"\nbirth_year = "1906"\n'
           'email = "grace.hopper@navy.example.com"\nemployee_no = 42',
     steps=[
         ("Clean the names: remove the outer spaces and print each in title case, one per line.",
          "first = first.strip().title()\n"
          "last = last.strip().title()\n"
          "print(first)\nprint(last)"),
         ("Build the username: first letter of the first name, the whole last name, "
          "and the last two digits of the birth year, all in lowercase. Print it.",
          "username = (first[0] + last + birth_year[-2:]).lower()\n"
          "print(username)"),
         ("Print the initials in capitals, with a dot after each (like `G.H.`).",
          'initials = first[0] + "." + last[0] + "."\n'
          "print(initials)"),
         ("Mask the email: keep its first letter and everything from the `@` on, "
          "and replace the characters in between with `*`. Print it.",
          'at = email.index("@")\n'
          'masked = email[0] + "*" * (at - 1) + email[at:]\n'
          "print(masked)"),
         ("Print an ID card of width 30: a line of `-`, then the lines "
          "`Name`, `User`, `Email` and `No.` labels left-aligned in 6 characters, "
          "with the employee number padded with zeros to 4 digits, then another line of `-`.",
          'line = "-" * 30\n'
          "print(line)\n"
          'print(f"{\'Name\':<6}{first} {last}")\n'
          'print(f"{\'User\':<6}{username}")\n'
          'print(f"{\'Email\':<6}{masked}")\n'
          'print(f"{\'No.\':<6}{employee_no:04d}")\n'
          "print(line)"),
     ])

nb.build()
