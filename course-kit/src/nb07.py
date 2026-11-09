import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB07", title="Functions Basics", intro="""
    Packaging code into named, reusable functions: parameters, `return`,
    default values, keyword arguments and a first taste of scope. Every
    question asks you to **write a `def` and call it**. Values that would
    come from `input()` are given to you as variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", "Write `square(n)` that **returns** `n` times itself, then print `square(7)`.",
     solution="def square(n): return n * n\nprint(square(7))")

nb.q("Real-life", "Write `km_to_miles(km)` (1 km is 0.621371 miles) that returns the miles. Print the result for 42.195 km (a marathon), rounded to 2 decimal places.",
     solution="def km_to_miles(km): return km * 0.621371\nprint(round(km_to_miles(42.195), 2))")

nb.q("Output-match", "Write `shout(word)` that returns the word in upper case followed by three `!`. Print `shout(\"hello\")`.",
     solution='def shout(word): return word.upper() + "!!!"\nprint(shout("hello"))')

nb.q("Puzzle", "Write `is_even(n)` that returns `True` or `False`. Print the result for `n = 10` and for `n = 7`.",
     solution="def is_even(n): return n % 2 == 0\nprint(is_even(10), is_even(7))")

nb.q("Real-life", "Write `greet(name, greeting=\"Hello\")` that returns the greeting, a space and the name. Print one call using the default and one that passes `\"Good morning\"` as a keyword argument.",
     solution='def greet(name, greeting="Hello"): return greeting + " " + name\n'
              'print(greet("Ada"))\nprint(greet("Ada", greeting="Good morning"))')

# ------------------------------------------------------------ Combine
nb.q("Real-life", "Write `shipping(weight_kg, rate=2.5)` that returns the shipping cost: weight times rate, plus a flat 4.00 handling fee. Print the cost of a 3 kg parcel at the default rate, then at a rate of 4.",
     solution="def shipping(weight_kg, rate=2.5):\n    return weight_kg * rate + 4.00\n"
              "print(shipping(3))\nprint(shipping(3, rate=4))")

nb.q("Real-life", "Write `grade_stats(scores)` that returns the lowest, the highest and the average of a list of scores (three values). Unpack them into three variables and print them on one line.",
     given="scores = [72, 95, 58, 88, 100]",
     solution="def grade_stats(scores):\n    return min(scores), max(scores), sum(scores) / len(scores)\n"
              "low, high, avg = grade_stats(scores)\nprint(low, high, avg)")

nb.q("Build", "Write `show(text)` that only **prints** the text (no `return`). Then store the result of `show(\"hi\")` in `result` and print `result`.",
     solution='def show(text):\n    print(text)\nresult = show("hi")\nprint(result)')

nb.q("Build", "Write `area(width, height)` with a one-line docstring saying what it does. Print `area(height=4, width=5)`.",
     solution='def area(width, height):\n    """Return the area of a rectangle."""\n    return width * height\n'
              "print(area(height=4, width=5))")

nb.q("Puzzle", "Write `is_palindrome(text)` that returns `True` if the text reads the same backwards. Print the result for both words.",
     given='word_1 = "level"\nword_2 = "python"',
     solution="def is_palindrome(text):\n    return text == text[::-1]\n"
              "print(is_palindrome(word_1))\nprint(is_palindrome(word_2))")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Write `safe_int(text)` that returns the text as an int, or `None` if it
    isn't a valid whole number (use `try` / `except ValueError`). Loop over
    the form answers and print each result.
""",
     given='answers = ["42", "abc", "7", "3.5"]',
     solution="def safe_int(text):\n    try:\n        return int(text)\n    except ValueError:\n        return None\n"
              "for answer in answers:\n    print(safe_int(answer))")

nb.q("Real-life", """
    Write `password_ok(password)` that returns `True` only if the password
    has at least 8 characters, contains a digit and contains an upper-case
    letter. Use an early `return False` for each failed rule. Print the
    verdict for each candidate.
""",
     given='candidates = ["hunter2", "Sunshine99", "sunshine99", "SUNSHINEEE"]',
     solution="def password_ok(password):\n"
              "    if len(password) < 8:\n        return False\n"
              "    has_digit = False\n    has_upper = False\n"
              "    for ch in password:\n"
              "        if ch.isdigit():\n            has_digit = True\n"
              "        if ch.isupper():\n            has_upper = True\n"
              "    return has_digit and has_upper\n"
              "for candidate in candidates:\n    print(candidate, password_ok(candidate))")

nb.q("Real-life", """
    A shopping list function must not remember old calls. Write
    `add_item(item, basket=None)` that returns a **new** list containing the
    basket's items plus the item (start from an empty list when no basket is
    given). Call it twice without a basket, with `"milk"` and then `"eggs"`,
    and print both results.
""",
     solution="def add_item(item, basket=None):\n"
              "    if basket is None:\n        basket = []\n"
              "    return basket + [item]\n"
              'print(add_item("milk"))\nprint(add_item("eggs"))')

nb.q("Real-life", """
    Write `format_receipt_line(name, qty, price)` that returns a line like
    the expected output: the name padded to 10 characters, the quantity, and
    the line total (qty times price) with 2 decimal places. Print a line
    for each purchase.
""",
     given='purchases = [("coffee", 2, 3.2), ("croissant", 3, 1.85), ("tea", 1, 2.5)]',
     solution='def format_receipt_line(name, qty, price):\n'
              '    return f"{name:<10} x{qty}  {qty * price:.2f}"\n'
              "for name, qty, price in purchases:\n    print(format_receipt_line(name, qty, price))")

nb.q("Build", """
    A function that changes its argument surprises its caller. Write
    `without_negatives(numbers)` that returns a **new** list with the
    negatives removed and leaves the original alone. Print both lists.
""",
     given="data = [3, -1, 4, -5, 9]",
     solution="def without_negatives(numbers):\n"
              "    result = []\n"
              "    for n in numbers:\n        if n >= 0:\n            result.append(n)\n"
              "    return result\n"
              "cleaned = without_negatives(data)\nprint(cleaned)\nprint(data)")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Write `to_roman(n)` for 1 to 3999 using value/symbol pairs from largest
    to smallest (1000 M, 900 CM, 500 D, 400 CD, 100 C, 90 XC, 50 L, 40 XL,
    10 X, 9 IX, 5 V, 4 IV, 1 I). Print the Roman numeral for each year.
""",
     given="years = [1994, 2024, 49]",
     solution="def to_roman(n):\n"
              '    values = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]\n'
              '    symbols = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]\n'
              '    result = ""\n'
              "    for i in range(len(values)):\n"
              "        while n >= values[i]:\n"
              "            result += symbols[i]\n"
              "            n -= values[i]\n"
              "    return result\n"
              "for year in years:\n    print(year, to_roman(year))")

nb.q("Puzzle", """
    Write `my_split(text, sep=" ")` that behaves like `text.split(sep)` for a
    single-character separator, **without calling `split`**: walk through the
    characters, collecting a piece until you hit the separator. Print the
    result for a sentence and for a comma-separated line.
""",
     given='sentence = "the quick brown fox"\nline = "a,b,,c"',
     solution="def my_split(text, sep=\" \"):\n"
              "    parts = []\n"
              '    current = ""\n'
              "    for ch in text:\n"
              "        if ch == sep:\n"
              "            parts.append(current)\n"
              '            current = ""\n'
              "        else:\n"
              "            current += ch\n"
              "    parts.append(current)\n"
              "    return parts\n"
              "print(my_split(sentence))\nprint(my_split(line, \",\"))")

nb.q("Real-life", """
    A scoreboard keeps a running total in a global variable. Write
    `add_points(points)` that **adds** to that global total (it must use the
    `global` keyword) and returns nothing. Call it three times with the given
    points, then print the total.
""",
     given="total = 0\nround_points = [10, 25, 5]",
     solution="def add_points(points):\n"
              "    global total\n"
              "    total += points\n"
              "for p in round_points:\n    add_points(p)\nprint(total)")

nb.q("Build", """
    Write `bmi_report(weight_kg, height_m)` that returns **two** values: the
    BMI (weight / height squared, rounded to 1 decimal) and a category
    string: `"under"` below 18.5, `"normal"` below 25, `"over"` below 30,
    otherwise `"obese"`. Use early returns, and print one line per person.
""",
     given='people = [("Ana", 50, 1.70), ("Ben", 82, 1.80), ("Cy", 95, 1.75), ("Di", 60, 1.50)]',
     solution="def bmi_report(weight_kg, height_m):\n"
              "    bmi = round(weight_kg / height_m ** 2, 1)\n"
              "    if bmi < 18.5:\n        return bmi, \"under\"\n"
              "    if bmi < 25:\n        return bmi, \"normal\"\n"
              "    if bmi < 30:\n        return bmi, \"over\"\n"
              "    return bmi, \"obese\"\n"
              "for name, w, h in people:\n"
              "    bmi, category = bmi_report(w, h)\n"
              "    print(name, bmi, category)")

# ------------------------------------------------------------ Q20 project
nb.project("Text Statistics Toolkit", story="""
    You're building a tiny analysis toolkit for a writing app. Each step adds
    one small function; the last step puts them all together in a report.
""",
     given='text = "Python is fun. Functions make code reusable. Python is easy to read. Small functions are easy to test."',
     steps=[
         ("Write `get_words(text)` that returns a list of lower-case words with the full stops removed. Print how many words `text` has.",
          "def get_words(text):\n"
          '    return text.lower().replace(".", "").split()\n'
          "print(len(get_words(text)))"),
         ("Write `average_length(words)` that returns the average word length rounded to 2 decimal places. Print it for the words of `text`.",
          "def average_length(words):\n"
          "    total = 0\n"
          "    for word in words:\n        total += len(word)\n"
          "    return round(total / len(words), 2)\n"
          "print(average_length(get_words(text)))"),
         ("Write `top_words(words)` that returns the most common word and how many times it appears (two values; on a tie, the word that appears first wins). Print both.",
          "def top_words(words):\n"
          "    counts = {}\n"
          "    for word in words:\n        counts[word] = counts.get(word, 0) + 1\n"
          "    best = words[0]\n"
          "    for word in counts:\n        if counts[word] > counts[best]:\n            best = word\n"
          "    return best, counts[best]\n"
          "word, times = top_words(get_words(text))\nprint(word, times)"),
         ("Write `longest_sentence(text)` that returns the sentence with the most words (split the text on `.`, strip spaces, ignore empty pieces). Print it.",
          "def longest_sentence(text):\n"
          '    best = ""\n'
          '    for sentence in text.split("."):\n'
          "        sentence = sentence.strip()\n"
          "        if len(sentence.split()) > len(best.split()):\n            best = sentence\n"
          "    return best\n"
          "print(longest_sentence(text))"),
         ("Write `report(text)` that **prints** a four-line report using your other functions: word count, average word length, the top word with its count, and the longest sentence, labelled like the expected output. Call it.",
          "def report(text):\n"
          "    words = get_words(text)\n"
          "    word, times = top_words(words)\n"
          '    print("Words:", len(words))\n'
          '    print("Average length:", average_length(words))\n'
          '    print("Top word:", word, times)\n'
          '    print("Longest sentence:", longest_sentence(text))\n'
          "report(text)"),
     ])

nb.build()
