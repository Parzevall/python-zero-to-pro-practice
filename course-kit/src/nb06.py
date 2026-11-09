import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB06", title="Dicts & Sets", intro="""
    Dictionaries look things up by key, and sets keep only unique values.
    Everything from NB00 to NB05 is fair game too: lists, loops and `if`.
    Sets have no fixed order, so always `sorted()` a set before printing it.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "Print the price of `\"apple\"` from the menu, and `0` for `\"mango\"`, which isn't on it. The program must not crash.",
     given='prices = {"apple": 0.5, "bread": 2.2, "cola": 1.8}',
     solution='print(prices.get("apple"))\nprint(prices.get("mango", 0))')

nb.q("Build", "Add `\"tea\"` at 1.5 to the menu, change the price of `\"cola\"` to 2.0, then print the menu.",
     given='prices = {"apple": 0.5, "bread": 2.2, "cola": 1.8}',
     solution='prices["tea"] = 1.5\nprices["cola"] = 2.0\nprint(prices)')

nb.q("Build", "Merge `defaults` and `user` into one dict where the user's choices win, and print it.",
     given='defaults = {"theme": "light", "font": 12, "lang": "en"}\nuser = {"theme": "dark", "font": 14}',
     solution="print(defaults | user)")

nb.q("Real-life", "Remove `\"bob\"` from the phone book and print his number (the removed value).",
     given='book = {"ada": "555-0101", "bob": "555-0102", "cy": "555-0103"}',
     solution='print(book.pop("bob"))')

nb.q("Real-life", "Print the unique tags in alphabetical order, as a list.",
     given='tags = ["python", "code", "python", "fun", "code", "python"]',
     solution="print(sorted(set(tags)))")

# ------------------------------------------------------------ Combine
nb.q("Real-life", "Print each contact on its own line like `ada: 555-0101`.",
     given='book = {"ada": "555-0101", "bob": "555-0102", "cy": "555-0103"}',
     solution='for name, number in book.items():\n    print(name + ": " + number)')

nb.q("Real-life", "Print the total value of the stock: each item's quantity times its price, added up.",
     given='stock = {"pens": 10, "books": 3, "bags": 2}\nprice = {"pens": 1.5, "books": 12.0, "bags": 25.0}',
     solution='total = 0\nfor item in stock:\n    total += stock[item] * price[item]\nprint(total)')

nb.q("Build", "Make an empty set called `seen`, add 5, 3 and 5 again to it, and print it sorted as a list.",
     solution="seen = set()\nseen.add(5)\nseen.add(3)\nseen.add(5)\nprint(sorted(seen))")

nb.q("Real-life", "Print the friends that both people have, in alphabetical order, as a list.",
     given='mine = ["ana", "ben", "cy", "dee"]\nhers = ["dee", "eli", "ben", "fay"]',
     solution="print(sorted(set(mine) & set(hers)))")

nb.q("Puzzle", "Print how many entries `codes` has, then the value stored under key `1`.",
     given='codes = {1: "a", True: "b", 1.0: "c"}',
     solution="print(len(codes))\nprint(codes[1])")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Count how many times each word appears in the sentence. Print one line per
    word, in alphabetical order, like `the 3`.
""",
     given='sentence = "the cat and the dog and the bird"',
     solution='counts = {}\nfor word in sentence.split():\n    counts[word] = counts.get(word, 0) + 1\n'
              'for word in sorted(counts):\n    print(word, counts[word])')

nb.q("Real-life", """
    Print each student's average grade rounded to 1 decimal place, one line
    per student, like `ana 8.0`.
""",
     given='grades = {"ana": [8, 9, 7], "ben": [6, 7, 10, 5], "cy": [10, 9]}',
     solution='for name, marks in grades.items():\n    print(name, round(sum(marks) / len(marks), 1))')

nb.q("Build", """
    Group the words by their first letter into a dict of lists, then print
    each letter and its words, letters in alphabetical order.
""",
     given='words = ["apple", "bear", "avocado", "bat", "cherry", "banana"]',
     solution='groups = {}\nfor w in words:\n    groups.setdefault(w[0], []).append(w)\n'
              'for letter in sorted(groups):\n    print(letter, groups[letter])')

nb.q("Build", """
    Invert the dict so the codes are the keys and the countries the values,
    then print the inverted dict.
""",
     given='codes = {"Spain": "ES", "France": "FR", "Italy": "IT"}',
     solution='inverted = {}\nfor country, code in codes.items():\n    inverted[code] = country\nprint(inverted)')

nb.q("Build", """
    Give every player their **own** empty list of scores, add a score of 10
    to `"ana"` only, and print the scoreboard.
""",
     given='players = ["ana", "ben", "cy"]',
     solution='scores = {}\nfor p in players:\n    scores[p] = []\nscores["ana"].append(10)\nprint(scores)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", "Dig the word `\"hello\"` out of the nested data and print it.",
     given='data = {"a": [1, {"b": {"c": ("x", "hello")}}]}',
     solution='print(data["a"][1]["b"]["c"][1])')

nb.q("Puzzle", """
    Two-sum: find the two positions in `nums` whose values add up to `target`,
    in one pass using a dict of value to position. Print the two positions as
    a list, smaller first.
""",
     given="nums = [2, 7, 11, 15, 3]\ntarget = 18",
     solution="seen = {}\nfor i in range(len(nums)):\n    need = target - nums[i]\n"
              "    if need in seen:\n        print([seen[need], i])\n        break\n    seen[nums[i]] = i")

nb.q("Puzzle", """
    Group the anagrams together (words made of the same letters). Print each
    group as a list of its words, in the order the groups first appeared.
""",
     given='words = ["listen", "google", "silent", "enlist", "gogole", "cat", "act"]',
     solution='groups = {}\nfor w in words:\n    key = "".join(sorted(w))\n    groups.setdefault(key, []).append(w)\n'
              'for key in groups:\n    print(groups[key])')

nb.q("Real-life", """
    Two classes sign up for clubs. Print, each on its own line and sorted as
    lists: everyone, students in both classes, only in class A, and students
    in exactly one class. Then print `True` if the `choir` is a subset of
    class A.
""",
     given='class_a = ["ana", "ben", "cy", "dee"]\nclass_b = ["cy", "dee", "eli"]\nchoir = {"ana", "cy"}',
     solution='a = set(class_a)\nb = set(class_b)\nprint(sorted(a | b))\nprint(sorted(a & b))\n'
              'print(sorted(a - b))\nprint(sorted(a ^ b))\nprint(choir <= a)')

# ------------------------------------------------------------ Q20
nb.project("Corner Shop Orders", story="""
    You run the corner shop's order system. Today's orders came in as a list
    of `(item, quantity)` pairs. Run them against the stock, then report.
    Each step builds on the one before.
""",
     given='stock = {"apple": 20, "batteries": 3, "bread": 5, "milk": 8, "rice": 7, "soap": 2, "tea": 12}\n'
           'price = {"apple": 0.5, "batteries": 5.0, "bread": 2.0, "milk": 1.2, "rice": 1.8, "soap": 3.0, "tea": 4.0}\n'
           'category = {"apple": "food", "batteries": "home", "bread": "food", "milk": "food", "rice": "food",\n'
           '            "soap": "home", "tea": "drinks"}\n'
           'orders = [("apple", 6), ("soap", 3), ("milk", 8), ("tea", 2), ("bread", 1), ("salt", 1), ("apple", 10)]',
     steps=[
         ("Run each order: if the item is in stock with enough quantity, subtract it from `stock` and add the order "
          "to a `filled` list; otherwise add the item name to a `shortages` list. Print both lists.",
          "filled = []\nshortages = []\nfor item, qty in orders:\n"
          "    if item in stock and stock[item] >= qty:\n"
          "        stock[item] -= qty\n        filled.append((item, qty))\n"
          "    else:\n        shortages.append(item)\n"
          'print("Filled:", filled)\nprint("Shortages:", shortages)'),
         ("Print the total revenue of the filled orders, then the revenue per category, one line each in "
          "alphabetical order, like `drinks 8.0`.",
          "revenue = {}\ntotal = 0\nfor item, qty in filled:\n"
          "    money = price[item] * qty\n    total += money\n"
          "    cat = category[item]\n    revenue[cat] = revenue.get(cat, 0) + money\n"
          'print("Total:", total)\nfor cat in sorted(revenue):\n    print(cat, revenue[cat])'),
         ("Print the restock list: items with fewer than 5 left, one per line in alphabetical order, like `soap: 0`.",
          "for item in sorted(stock):\n    if stock[item] < 5:\n        print(item + \": \" + str(stock[item]))"),
         ("Print, as sorted lists, the items nobody ordered today, and the ordered items that are not in the shop at all.",
          "ordered = set()\nfor item, qty in orders:\n    ordered.add(item)\n"
          "print(sorted(set(stock) - ordered))\nprint(sorted(ordered - set(stock)))"),
         ("Remove every item with 0 stock from `stock` (careful: don't change the dict's size while looping over it), "
          "then print the remaining dict.",
          "for item in list(stock):\n    if stock[item] == 0:\n        del stock[item]\nprint(stock)"),
     ])
nb.build()
