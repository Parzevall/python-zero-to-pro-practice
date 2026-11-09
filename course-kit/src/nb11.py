import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB11", title="Recursion", intro="""
    Functions that call themselves: a **base case** that stops, a **recursive
    case** that shrinks the problem, and how Python's call stack and recursion
    limit behave. You will recurse on numbers, strings, lists and nested data,
    split problems in half, try every possibility (backtracking) and make slow
    recursion fast with caching.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Build", "Write a recursive `countdown(n)` that prints `n`, `n-1`, ... down to 1 (one per line) and then prints `Liftoff!`. Call it with 4.",
     solution='def countdown(n):\n    if n == 0:\n        print("Liftoff!")\n    else:\n        print(n)\n        countdown(n - 1)\ncountdown(4)')

nb.q("Output-match", "Write a recursive `factorial(n)` (with `factorial(0)` being 1) and print `factorial(6)`.",
     solution="def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\nprint(factorial(6))")

nb.q("Real-life", "A staircase has `n` steps and step number `k` has `k` handrail posts. Write a recursive `posts(n)` that returns the total number of posts for `n` steps (1 + 2 + ... + n). Print it for 10 steps.",
     solution="def posts(n):\n    if n == 0:\n        return 0\n    return n + posts(n - 1)\nprint(posts(10))")

nb.q("Puzzle", "Write a recursive `power(base, exp)` that multiplies `base` by itself `exp` times (no `**`; `exp` is a whole number, 0 or more). Print `power(2, 10)` and `power(5, 0)`.",
     solution="def power(base, exp):\n    if exp == 0:\n        return 1\n    return base * power(base, exp - 1)\nprint(power(2, 10), power(5, 0))")

nb.q("Real-life", "A lottery game adds up the digits of your ticket number. Write a recursive `digit_sum(n)` using `// 10` and `% 10` (no strings), and print the result for the ticket 90417.",
     solution="def digit_sum(n):\n    if n == 0:\n        return 0\n    return n % 10 + digit_sum(n // 10)\nprint(digit_sum(90417))")

# ------------------------------------------------------------ Combine
nb.q("Build", "Write a recursive `reverse(text)` that returns the text backwards, using a slice for \"everything but the first letter\" (no `[::-1]`). Print `reverse(\"recursion\")`.",
     solution='def reverse(text):\n    if text == "":\n        return ""\n    return reverse(text[1:]) + text[0]\nprint(reverse("recursion"))')

nb.q("Puzzle", "Euclid's rule: the greatest common divisor of `a` and `b` is `a` when `b` is 0, otherwise it is the gcd of `b` and `a % b`. Write a recursive `gcd(a, b)` and print it for 84 and 36, then for 17 and 5.",
     solution="def gcd(a, b):\n    if b == 0:\n        return a\n    return gcd(b, a % b)\nprint(gcd(84, 36))\nprint(gcd(17, 5))")

nb.q("Real-life", "The till has a list of prices to add up. Write a recursive `total(prices)` with no loop and no `sum()`: an empty list is 0, otherwise the first price plus the total of the rest. Print the total.",
     given="prices = [4.5, 3.25, 10, 2.25]",
     solution="def total(prices):\n    if prices == []:\n        return 0\n    return prices[0] + total(prices[1:])\nprint(total(prices))")

nb.q("Build", "A function with no base case never stops. Write `broken(n)` that returns `broken(n + 1)`, call it inside `try` / `except RecursionError`, and print `Too deep!` when it fails. Then print whether `sys.getrecursionlimit()` is at least 1000.",
     solution="import sys\n\ndef broken(n):\n    return broken(n + 1)\n\ntry:\n    broken(0)\nexcept RecursionError:\n    print(\"Too deep!\")\nprint(sys.getrecursionlimit() >= 1000)")

nb.q("Puzzle", "Python does not optimise \"tail\" recursion. Write `add_up(n, acc=0)` that returns `acc` when `n` is 0, otherwise `add_up(n - 1, acc + n)`. Calling it with 50000 fails: catch the `RecursionError`, print `Too deep for recursion`, and then print the same sum (1 + 2 + ... + 50000) with a `for` loop.",
     solution='def add_up(n, acc=0):\n    if n == 0:\n        return acc\n    return add_up(n - 1, acc + n)\n\ntry:\n    print(add_up(50000))\nexcept RecursionError:\n    print("Too deep for recursion")\n    total = 0\n    for i in range(1, 50001):\n        total += i\n    print(total)')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A shopping list was typed in groups, and the groups contain more groups.
    Write a recursive `flatten(items)` that returns one flat list of all the
    products in order (use `isinstance(item, list)`). Print the result.
""",
     given='shopping = ["milk", ["eggs", ["flour", "sugar"], "butter"], "tea", [["salt"]]]',
     solution='def flatten(items):\n    flat = []\n    for item in items:\n        if isinstance(item, list):\n            flat += flatten(item)\n        else:\n            flat.append(item)\n    return flat\nprint(flatten(shopping))')

nb.q("Real-life", """
    A company chart is a nested dict: each person maps to a dict of the people
    who report to them (empty for the team members). Write a recursive
    `headcount(chart)` that returns how many people the chart contains in total
    and print it. Then print the headcount of just Dana's team (`chart["Ada"]["Dana"]`).
""",
     given='chart = {"Ada": {"Ben": {}, "Dana": {"Eli": {}, "Fay": {"Gus": {}}}, "Cy": {}}}',
     solution="def headcount(chart):\n    count = 0\n    for person in chart:\n        count += 1 + headcount(chart[person])\n    return count\nprint(headcount(chart))\nprint(headcount(chart[\"Ada\"][\"Dana\"]))")

nb.q("Real-life", """
    A library sorts book ids on the shelf. Write a recursive binary search
    `find(ids, target, low, high)` that returns the **index** of `target` or
    `-1` when it isn't there (look at the middle, then search only the left or
    right half). Print the result for 61 and for 40, starting with the whole list.
""",
     given="ids = [3, 8, 15, 22, 37, 44, 61, 75, 90]",
     solution="def find(ids, target, low, high):\n    if low > high:\n        return -1\n    mid = (low + high) // 2\n    if ids[mid] == target:\n        return mid\n    if ids[mid] < target:\n        return find(ids, target, mid + 1, high)\n    return find(ids, target, low, mid - 1)\nprint(find(ids, 61, 0, len(ids) - 1))\nprint(find(ids, 40, 0, len(ids) - 1))")

nb.q("Puzzle", """
    A pizza place offers these extra toppings. Write a recursive `subsets(items)`
    that returns a list of **all** the possible combinations (including the empty
    one and the full one), each as a list. Print how many there are, then the
    combinations sorted, one per line.
""",
     given='toppings = ["ham", "olives", "corn"]',
     solution="def subsets(items):\n    if items == []:\n        return [[]]\n    rest = subsets(items[1:])\n    return rest + [[items[0]] + s for s in rest]\n"
              "result = subsets(toppings)\nprint(len(result))\nfor combo in sorted(result):\n    print(combo)")

nb.q("Build", """
    The naive `fib(n)` calls itself twice and recomputes the same values again
    and again, which is painfully slow for big `n`. Write `fib(n, memo)` that stores results in the dict `memo` and checks
    it first. Print `fib(80)` starting with an empty dict.
""",
     solution="def fib(n, memo):\n    if n in memo:\n        return memo[n]\n    if n < 2:\n        return n\n    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)\n    return memo[n]\nprint(fib(80, {}))")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    Some friends race and you want every possible finishing order. Write a
    recursive `orders(names)` that returns a list of all the orderings (each a
    list). For the three runners below print how many there are, then print
    them sorted, one per line.
""",
     given='runners = ["Ana", "Bo", "Cy"]',
     solution="def orders(names):\n    if len(names) <= 1:\n        return [names]\n    result = []\n    for i in range(len(names)):\n        rest = names[:i] + names[i + 1:]\n        for order in orders(rest):\n            result.append([names[i]] + order)\n    return result\n"
              "all_orders = orders(runners)\nprint(len(all_orders))\nfor order in sorted(all_orders):\n    print(order)")

nb.q("Puzzle", """
    Write a recursive merge sort: `merge_sort(items)` returns a new sorted list
    by splitting the list in half, sorting each half and merging the two sorted
    halves (take the smaller front item each time). Print the sorted result of
    the scores below.
""",
     given="scores = [52, 7, 91, 33, 18, 64, 7, 80]",
     solution="def merge_sort(items):\n    if len(items) <= 1:\n        return items\n    mid = len(items) // 2\n    left = merge_sort(items[:mid])\n    right = merge_sort(items[mid:])\n    merged = []\n    i = 0\n    j = 0\n    while i < len(left) and j < len(right):\n        if left[i] <= right[j]:\n            merged.append(left[i])\n            i += 1\n        else:\n            merged.append(right[j])\n            j += 1\n    return merged + left[i:] + right[j:]\nprint(merge_sort(scores))")

nb.q("Puzzle", """
    A vending machine has coins of 1, 5, 10, 25 and 50 cents. Using
    `functools.cache`, write `ways(amount, n_coins)` that counts how many
    different combinations of the first `n_coins` coins add up to `amount`
    (use the coin or skip the last coin type). Print the number of ways to make
    100 cents.
""",
     given="coins = [1, 5, 10, 25, 50]",
     solution="from functools import cache\n\n@cache\ndef ways(amount, n_coins):\n    if amount == 0:\n        return 1\n    if amount < 0 or n_coins == 0:\n        return 0\n    return ways(amount - coins[n_coins - 1], n_coins) + ways(amount, n_coins - 1)\nprint(ways(100, len(coins)))")

nb.q("Puzzle", """
    Place 6 queens on a 6x6 chess board so that none can capture another (no
    two share a row, column or diagonal). Write a backtracking `place(row, cols)`
    where `cols` is the list of columns used by earlier rows; it returns the
    number of complete solutions. Print the count for a 6x6 board.
""",
     given="size = 6",
     solution="def safe(col, cols):\n    row = len(cols)\n    for r in range(row):\n        c = cols[r]\n        if c == col or abs(c - col) == row - r:\n            return False\n    return True\n\ndef place(row, cols):\n    if row == size:\n        return 1\n    count = 0\n    for col in range(size):\n        if safe(col, cols):\n            count += place(row + 1, cols + [col])\n    return count\nprint(place(0, []))")

# ------------------------------------------------------------ Q20 story project
nb.project("Folder Size Calculator", story="""
    Your laptop is almost full and you want to know where the space went.
    The file system is modelled as a **nested dict**: a folder is a dict, a
    file is a number (its size in MB). Each step uses recursion on the tree
    from the step before.
""",
     given='''tree = {
    "projects": {
        "app": {"main.py": 4, "utils.py": 2,
                "assets": {"logo.png": 120, "icon.png": 30}},
        "notes.txt": 3,
    },
    "photos": {
        "2024": {"a.jpg": 500, "b.jpg": 450},
        "2025": {},
    },
    "todo.txt": 1,
}''',
     steps=[
         ("Write a recursive `total_size(node)`: a number is its own size, a folder is the sum of everything inside it. Print the size of the whole `tree` and of `tree[\"photos\"]`.",
          'def total_size(node):\n    if isinstance(node, int):\n        return node\n    total = 0\n    for child in node.values():\n        total += total_size(child)\n    return total\nprint("Everything:", total_size(tree))\nprint("Photos:", total_size(tree["photos"]))'),
         ("Write `count_files(node)` that returns how many files (numbers) the tree holds, and print it.",
          'def count_files(node):\n    if isinstance(node, int):\n        return 1\n    count = 0\n    for child in node.values():\n        count += count_files(child)\n    return count\nprint("Files:", count_files(tree))'),
         ("Write `folder_sizes(name, node, sizes)` that fills the dict `sizes` with the total size of **every folder**, keyed by its name (skip files), by recursing into the sub-folders. Call it for the whole tree named `home`, then print the name and size of the largest folder other than `home`.",
          'def folder_sizes(name, node, sizes):\n    sizes[name] = total_size(node)\n    for child_name in node:\n        if isinstance(node[child_name], dict):\n            folder_sizes(child_name, node[child_name], sizes)\nsizes = {}\nfolder_sizes("home", tree, sizes)\ndel sizes["home"]\nbiggest = max(sizes, key=sizes.get)\nprint("Largest folder:", biggest, sizes[biggest])'),
         ("Write `show(name, node, depth)` that prints the tree: every line is indented by two spaces per level, folders end with `/` and show their total size in brackets, files show their size in brackets. Print the whole tree starting with the name `home` at depth 0.",
          'def show(name, node, depth):\n    indent = "  " * depth\n    if isinstance(node, int):\n        print(indent + name + " [" + str(node) + "]")\n    else:\n        print(indent + name + "/ [" + str(total_size(node)) + "]")\n        for child_name in node:\n            show(child_name, node[child_name], depth + 1)\nshow("home", tree, 0)'),
         ("Write `depth(node)` that returns how many folder levels are nested inside the tree (an empty folder or a file adds nothing below it; the top folder counts as 1, and a file counts as 0). Print the depth, then print the names of all folders that are empty.",
          'def depth(node):\n    if isinstance(node, int):\n        return 0\n    deepest = 0\n    for child in node.values():\n        deepest = max(deepest, depth(child))\n    return 1 + deepest\nprint("Depth:", depth(tree))\nempty = [name for name in sizes if sizes[name] == 0]\nprint("Empty folders:", empty)'),
     ])

nb.build()
