import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB05", title="Lists & Tuples", intro="""
    Ordered collections: lists you can change, tuples you can't. You now have
    loops from NB04 to work through them, but no dictionaries, no
    comprehensions and no functions yet.
""")

# ------------------------------------------------------------ Warm-up (1 line)
nb.q("Real-life", "Print the first song, the last song and how many songs are on the playlist, on one line.",
     given='playlist = ["Intro", "Sunrise", "Late Train", "Echoes", "Outro"]',
     solution="print(playlist[0], playlist[-1], len(playlist))")

nb.q("Output-match", "Print the 2nd, 3rd and 4th items of `nums` as a list, using one slice.",
     given="nums = [10, 20, 30, 40, 50, 60]",
     solution="print(nums[1:4])")

nb.q("Build", "A podium has only one gold medal. Create a tuple holding just the text `\"gold\"` and print it.",
     solution='medal = ("gold",)\nprint(medal)')

nb.q("Real-life", "Print how many days were `\"rain\"` and the position (index) of the first `\"snow\"` day.",
     given='weather = ["sun", "rain", "snow", "rain", "sun", "snow", "rain"]',
     solution='print(weather.count("rain"), weather.index("snow"))')

nb.q("Real-life", "Print the scores ordered from highest to lowest, without changing the original list.",
     given="scores = [72, 95, 88, 61, 95, 79]",
     solution="print(sorted(scores, reverse=True))")

# ------------------------------------------------------- Combine (2-4 lines)
nb.q("Real-life", """
    Your to-do list needs updating. Add `"buy milk"` to the end, put
    `"wake up"` at the very start, and remove `"watch TV"`. Print the list.
""",
     given='todo = ["call mum", "watch TV", "pay rent"]',
     solution='todo.append("buy milk")\ntodo.insert(0, "wake up")\ntodo.remove("watch TV")\nprint(todo)')

nb.q("Build", """
    Guests 2 and 3 (the middle two) cancelled and three friends take their
    place: `"Zed"`, `"Yu"`, `"Xi"`. Replace them using slice assignment, then
    add the `late` guests to the end with one call. Print the list.
""",
     given='guests = ["Ann", "Bob", "Cy", "Di", "Eve"]\nlate = ["Flo", "Gus"]',
     solution='guests[1:3] = ["Zed", "Yu", "Xi"]\nguests.extend(late)\nprint(guests)')

nb.q("Build", """
    Unpack `result` into `winner` and `rest` (everything after the first),
    then print the winner and the rest.
""",
     given='result = ["Mia", "Noah", "Omar", "Pia"]',
     solution="winner, *rest = result\nprint(winner)\nprint(rest)")

nb.q("Puzzle", """
    Dig the text `"gold"` out of this nested list using only indexes, and print
    it. Then print the length of the list that contains it.
""",
     given='chest = ["dust", ["rope", ["coin", "map", ["key", "gold", "gem"]]], "bone"]',
     solution='box = chest[1][1][2]\nprint(box[1])\nprint(len(box))')

nb.q("Build", """
    Make a real backup of `original` (not just a second name for it). Add `4`
    to `original` only, then print both lists.
""",
     given="original = [1, 2, 3]",
     solution="backup = original.copy()\noriginal.append(4)\nprint(original)\nprint(backup)")

# ------------------------------------------------ Small real tasks (5-8 lines)
nb.q("Real-life", """
    Print a leaderboard, one line per player like the expected output
    (position, name, points), then the total points of everyone.
""",
     given='names = ["Ada", "Ben", "Cleo", "Dan"]\npoints = [310, 280, 275, 190]',
     solution="total = 0\n"
              "for i in range(len(names)):\n"
              '    print(i + 1, names[i], points[i])\n'
              "    total += points[i]\n"
              'print("Total:", total)')

nb.q("Build", """
    Build a 3-row, 4-column grid of zeros using loops, so each row is its own
    list. Then set the middle cell of the second row to `7` (row 1, column 2)
    and print the grid one row per line.
""",
     solution="grid = []\n"
              "for r in range(3):\n"
              "    row = []\n"
              "    for c in range(4):\n"
              "        row.append(0)\n"
              "    grid.append(row)\n"
              "grid[1][2] = 7\n"
              "for row in grid:\n"
              "    print(row)")

nb.q("Real-life", """
    A freezer alarm logged temperatures overnight. Keep only the readings
    that are **0 or above** and print the new list and how many were thrown away.
""",
     given="temps = [-2, -5, -1, 3, -4, -6, 1, -3]",
     solution="kept = []\n"
              "for t in temps:\n"
              "    if t >= 0:\n"
              "        kept.append(t)\n"
              "print(kept)\n"
              'print("Removed:", len(temps) - len(kept))')

nb.q("Puzzle", """
    Remove the duplicates from `tags` but keep the order of first appearance.
    Print the result.
""",
     given='tags = ["python", "loops", "python", "lists", "loops", "tuples", "python"]',
     solution="unique = []\n"
              "for tag in tags:\n"
              "    if tag not in unique:\n"
              "        unique.append(tag)\n"
              "print(unique)")

nb.q("Real-life", """
    A cinema seat map: `"X"` is taken, `"."` is free. Print each row as a line
    with the seats separated by spaces, then print how many seats are free.
""",
     given='seats = [["X", ".", ".", "X"], [".", "X", ".", "."], ["X", "X", ".", "X"]]',
     solution="free = 0\n"
              "for row in seats:\n"
              '    print(" ".join(row))\n'
              "    free += row.count(\".\")\n"
              'print("Free seats:", free)')

# ----------------------------------------------- Puzzles & builds (8-15 lines)
nb.q("Puzzle", """
    Print the **second-largest distinct** value in `nums` (the second 9 does
    not count as another distinct value). Do not modify `nums`.
""",
     given="nums = [7, 3, 9, 9, 5, 1, 7]",
     solution="unique = []\n"
              "for n in nums:\n"
              "    if n not in unique:\n"
              "        unique.append(n)\n"
              "unique.sort()\n"
              "print(unique[-2])\n"
              "print(nums)")

nb.q("Puzzle", """
    Rotate `nums` to the right by `k` places using slices (`[1, 2, 3, 4, 5]`
    by 1 becomes `[5, 1, 2, 3, 4]`). `k` can be bigger than the list. Print the
    rotated list.
""",
     given="nums = [1, 2, 3, 4, 5]\nk = 8",
     solution="k = k % len(nums)\n"
              "rotated = nums[-k:] + nums[:-k]\n"
              "print(rotated)")

nb.q("Puzzle", """
    Merge the two sorted lists into one sorted list with a `while` loop and
    two position counters. Do not use `sorted()` or `sort()`. Print it.
""",
     given="a = [1, 4, 7, 10]\nb = [2, 3, 8, 11, 15]",
     solution="merged = []\n"
              "i = 0\n"
              "j = 0\n"
              "while i < len(a) and j < len(b):\n"
              "    if a[i] <= b[j]:\n"
              "        merged.append(a[i])\n"
              "        i += 1\n"
              "    else:\n"
              "        merged.append(b[j])\n"
              "        j += 1\n"
              "merged.extend(a[i:])\n"
              "merged.extend(b[j:])\n"
              "print(merged)")

nb.q("Puzzle", """
    Print the 3x4 matrix in **spiral order**: along the top row, down the right
    column, back along the bottom row, up the left column, then the inside.
    Print the values in one list.
""",
     given="matrix = [[1, 2, 3, 4],\n          [5, 6, 7, 8],\n          [9, 10, 11, 12]]",
     solution="out = []\n"
              "top, bottom = 0, len(matrix) - 1\n"
              "left, right = 0, len(matrix[0]) - 1\n"
              "while top <= bottom and left <= right:\n"
              "    for c in range(left, right + 1):\n"
              "        out.append(matrix[top][c])\n"
              "    top += 1\n"
              "    for r in range(top, bottom + 1):\n"
              "        out.append(matrix[r][right])\n"
              "    right -= 1\n"
              "    if top <= bottom:\n"
              "        for c in range(right, left - 1, -1):\n"
              "            out.append(matrix[bottom][c])\n"
              "        bottom -= 1\n"
              "    if left <= right:\n"
              "        for r in range(bottom, top - 1, -1):\n"
              "            out.append(matrix[r][left])\n"
              "        left += 1\n"
              "print(out)")

# ------------------------------------------------------------ Q20 story project
nb.project("Class Gradebook", story="""
    Mr. Patel's class just finished the maths test. The scores sit in a list of
    `(score, name)` tuples. Build the report his students are waiting for. Each
    step builds on the one before.
""",
     given='gradebook = [(78, "Ana"), (92, "Ben"), (55, "Cara"), (84, "Dev"),\n'
           '             (67, "Eli"), (99, "Fay"), (45, "Gus")]',
     steps=[
         ("Loop over the gradebook, unpacking each tuple, and print the class average "
          "rounded to 1 decimal place.",
          "total = 0\n"
          "for score, name in gradebook:\n"
          "    total += score\n"
          "average = total / len(gradebook)\n"
          'print("Average:", round(average, 1))'),
         ("Make a **sorted copy** of the gradebook from best to worst (the original "
          "stays as it is). Print the top 3 as `1. Fay 99` etc.",
          "ranked = sorted(gradebook, reverse=True)\n"
          "for i in range(3):\n"
          "    score, name = ranked[i]\n"
          '    print(str(i + 1) + ".", name, score)'),
         ("Print each student's letter grade: 90+ is A, 80+ B, 65+ C, anything lower F. "
          "Use the ranked list.",
          "for score, name in ranked:\n"
          "    if score >= 90:\n"
          '        grade = "A"\n'
          "    elif score >= 80:\n"
          '        grade = "B"\n'
          "    elif score >= 65:\n"
          '        grade = "C"\n'
          "    else:\n"
          '        grade = "F"\n'
          '    print(name, grade)'),
         ("Draw a histogram: one line per student in the original order, with the name "
          "and one `*` for every 10 points (whole tens only).",
          "for score, name in gradebook:\n"
          '    print(name, "*" * (score // 10))'),
         ("Unpack the ranked list as `best`, `*middle`, `worst`. Print the best and worst "
          "student names and how many students are in the middle.",
          "best, *middle, worst = ranked\n"
          'print("Best:", best[1])\n'
          'print("Worst:", worst[1])\n'
          'print("In the middle:", len(middle))'),
     ])

nb.build()
