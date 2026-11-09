import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB15", title="Stdlib Essentials", intro="""
    Python ships with batteries included. This notebook tours the standard
    library tools you will reach for again and again: `collections`,
    `itertools`, `datetime` and `zoneinfo`, seeded `random`, `statistics`,
    and the text helpers `string`, `textwrap` and `pprint`. Every date is
    fixed and every random draw is seeded, so your output can match exactly.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "A word game shows the three most common letters of a word. Print them as a list of `(letter, count)` pairs.",
     given='word = "mississippi"',
     solution="from collections import Counter\nprint(Counter(word).most_common(3))")

nb.q("Real-life", "A project starts on 14 March 2026 and ships on 25 December 2026. Print how many days that is.",
     solution="from datetime import date\nprint((date(2026, 12, 25) - date(2026, 3, 14)).days)")

nb.q("Puzzle", "Run-length encoding: print each run of equal neighbouring letters as the letter followed by its length, all on one line (like `a3b1`). Use `itertools.groupby`.",
     given='text = "aaabbbaaac"',
     solution="from itertools import groupby\n"
              'result = ""\nfor letter, run in groupby(text):\n    result += letter + str(len(list(run)))\nprint(result)')

nb.q("Real-life", "Group the shop's products by their first letter into a `defaultdict(list)` and print the group for `\"b\"` and the group for `\"c\"`.",
     given='products = ["bread", "butter", "cheese", "cake", "banana", "carrot"]',
     solution="from collections import defaultdict\n"
              "groups = defaultdict(list)\nfor product in products:\n    groups[product[0]].append(product)\n"
              'print(groups["b"])\nprint(groups["c"])')

nb.q("Build", "Make a `namedtuple` called `Book` with fields `title` and `pages`. Create one book and print its title, its pages, and the whole thing.",
     solution="from collections import namedtuple\n"
              'Book = namedtuple("Book", ["title", "pages"])\n'
              'book = Book("Dune", 612)\nprint(book.title)\nprint(book.pages)\nprint(book)')

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    A thermostat only remembers its last 3 readings. Append every new reading
    to a `deque(maxlen=3)`, then print what it remembers and the average of
    those readings rounded to 1 decimal place.
""",
     given="readings = [20.5, 21.0, 22.5, 23.0, 21.5]",
     solution="from collections import deque\n"
              "recent = deque(maxlen=3)\nfor reading in readings:\n    recent.append(reading)\n"
              "print(list(recent))\nprint(round(sum(recent) / len(recent), 1))")

nb.q("Real-life", """
    A shop has `stock` and has made some `sales`. Subtract the sales from the
    stock with `Counter` arithmetic and print what is left, one item per line
    in alphabetical order, as `item: count`.
""",
     given='from collections import Counter\nstock = Counter(apple=5, pear=2, plum=3)\nsales = Counter(apple=2, pear=4, plum=3)',
     solution="left = stock - sales\nfor item in sorted(left):\n    print(item + \":\", left[item])")

nb.q("Real-life", """
    A ticket says `"2026-03-14 18:30"`. Parse it into a `datetime`, add 90
    minutes with `timedelta`, and print the new time formatted like
    `Sat 14 Mar 2026, 20:00`.
""",
     given='ticket = "2026-03-14 18:30"',
     solution="from datetime import datetime, timedelta\n"
              'start = datetime.strptime(ticket, "%Y-%m-%d %H:%M")\n'
              "end = start + timedelta(minutes=90)\n"
              'print(end.strftime("%a %d %b %Y, %H:%M"))')

nb.q("Puzzle", "Four players enter a chess club. Use `itertools.combinations` to print how many different pairings exist, then print each pairing as `A vs B` on its own line.",
     given='players = ["Ana", "Ben", "Cy", "Dee"]',
     solution="from itertools import combinations\n"
              "pairs = list(combinations(players, 2))\nprint(len(pairs))\n"
              "for first, second in pairs:\n    print(first, \"vs\", second)")

nb.q("Real-life", """
    A raffle: seed the generator with 7, pick the winner with `random.choice`,
    then draw two different runners-up from the *remaining* entrants with
    `random.sample`. Print the winner and the runners-up.
""",
     given='entrants = ["Ana", "Ben", "Cy", "Dee", "Eli", "Fay"]',
     solution="import random\nrandom.seed(7)\nwinner = random.choice(entrants)\n"
              "others = [name for name in entrants if name != winner]\n"
              "runners_up = random.sample(others, 2)\n"
              'print("Winner:", winner)\nprint("Runners-up:", runners_up)')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Print a small statistics report for the exam `scores` using the
    `statistics` module: mean, median, mode and standard deviation
    (`stdev`), each labelled and rounded to 2 decimal places.
""",
     given="scores = [72, 85, 85, 90, 64, 85, 78, 91]",
     solution="import statistics\n"
              'print("Mean:", round(statistics.mean(scores), 2))\n'
              'print("Median:", round(statistics.median(scores), 2))\n'
              'print("Mode:", round(statistics.mode(scores), 2))\n'
              'print("Stdev:", round(statistics.stdev(scores), 2))')

nb.q("Real-life", """
    A bank statement lists January's and February's `transactions` (deposits
    are positive, withdrawals negative). Chain both lists together and use
    `itertools.accumulate` to print the running balance after each
    transaction, starting from a balance of 0, as one list.
""",
     given="january = [500, -120, -60]\nfebruary = [200, -300, 80]",
     solution="from itertools import chain, accumulate\n"
              "transactions = chain(january, february)\n"
              "print(list(accumulate(transactions)))")

nb.q("Real-life", """
    Each invoice is due 30 days after its date. Assuming today is
    1 June 2026, print one line per invoice: the id, the due date as
    `YYYY-MM-DD` (`isoformat`), and either `overdue by N days` or
    `due in N days`.
""",
     given="from datetime import date\ninvoices = {\"A-17\": date(2026, 4, 20), \"B-02\": date(2026, 5, 15), \"C-33\": date(2026, 5, 31)}\ntoday = date(2026, 6, 1)",
     solution="from datetime import timedelta\n"
              "for invoice_id, issued in invoices.items():\n"
              "    due = issued + timedelta(days=30)\n"
              "    days = (today - due).days\n"
              "    if days > 0:\n"
              '        status = "overdue by " + str(days) + " days"\n'
              "    else:\n"
              '        status = "due in " + str(-days) + " days"\n'
              "    print(invoice_id, due.isoformat(), status)")

nb.q("Build", """
    An app reads its settings from three layers: command-line options first,
    then the user's file, then the defaults. Combine them with
    `collections.ChainMap` (highest priority first) and print the final
    `theme`, `font_size` and `language`. Then print whether the layered
    `font_size` still shows 12 in the `defaults` dictionary itself.
""",
     given='defaults = {"theme": "light", "font_size": 12, "language": "en"}\nuser_file = {"theme": "dark", "font_size": 14}\ncommand_line = {"font_size": 18}',
     solution="from collections import ChainMap\n"
              "settings = ChainMap(command_line, user_file, defaults)\n"
              'print(settings["theme"])\nprint(settings["font_size"])\nprint(settings["language"])\n'
              'print(defaults["font_size"] == 12)')

nb.q("Real-life", """
    Generate a password for a new user: seed the generator with 2026, then
    build a 10-character password by choosing each character at random from
    `string.ascii_letters + string.digits`. Print the password.
""",
     solution="import random\nimport string\n"
              "random.seed(2026)\nalphabet = string.ascii_letters + string.digits\n"
              'password = ""\nfor _ in range(10):\n    password += random.choice(alphabet)\nprint(password)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    A meeting starts at 09:00 in New York on 10 March 2026. Make it a
    timezone-aware `datetime` with `zoneinfo`, then print the same moment in
    London and in Tokyo as `YYYY-MM-DD HH:MM`, one per line, labelled with the
    city. Then print the number of hours between New York 09:00 and London
    09:00 *on the same date* (a negative number means London is ahead; use
    `.total_seconds() / 3600`).
""",
     solution="from datetime import datetime\nfrom zoneinfo import ZoneInfo\n"
              'ny = ZoneInfo("America/New_York")\nlondon = ZoneInfo("Europe/London")\ntokyo = ZoneInfo("Asia/Tokyo")\n'
              "meeting = datetime(2026, 3, 10, 9, 0, tzinfo=ny)\n"
              'print("London:", meeting.astimezone(london).strftime("%Y-%m-%d %H:%M"))\n'
              'print("Tokyo:", meeting.astimezone(tokyo).strftime("%Y-%m-%d %H:%M"))\n'
              "ny_nine = datetime(2026, 3, 10, 9, 0, tzinfo=ny)\n"
              "london_nine = datetime(2026, 3, 10, 9, 0, tzinfo=london)\n"
              "print((ny_nine - london_nine).total_seconds() / 3600)")

nb.q("Puzzle", """
    Piggy-bank puzzle: using exactly 4 coins taken from the denominations
    1, 2, 5 and 10 (coins may repeat), find every *different* set of coins
    that adds up to 17. Use `itertools.product(coins, repeat=4)`, sort each
    combination so the same set is not counted twice, and print the sets in
    sorted order, one per line, followed by how many there are.
""",
     given="coins = [1, 2, 5, 10]\ntarget = 17",
     solution="from itertools import product\n"
              "found = set()\nfor combo in product(coins, repeat=4):\n    if sum(combo) == target:\n        found.add(tuple(sorted(combo)))\n"
              "for combo in sorted(found):\n    print(combo)\nprint(len(found), \"sets\")")

nb.q("Puzzle", """
    Five friends sit in a row of five seats. Ana and Ben had an argument and
    must **not** sit next to each other. Use `itertools.permutations` and
    `itertools.pairwise` to count the valid seatings, then print the first
    three valid seatings (in the order `permutations` produces them) as
    names joined with ` - `.
""",
     given='friends = ["Ana", "Ben", "Cy", "Dee", "Eli"]',
     solution="from itertools import permutations, pairwise\n"
              "valid = []\nfor seating in permutations(friends):\n"
              "    ok = True\n"
              "    for left, right in pairwise(seating):\n"
              '        if {left, right} == {"Ana", "Ben"}:\n'
              "            ok = False\n"
              "    if ok:\n        valid.append(seating)\n"
              "print(len(valid))\nfor seating in valid[:3]:\n    print(\" - \".join(seating))")

nb.q("Real-life", """
    A teacher needs two things. First, split the `students` into teams of 3
    with `itertools.batched` (the last team may be smaller) and print each team
    as a list. Second, sales `records` are not sorted by city: sort them, use
    `itertools.groupby` to print each city with its total sales, and use
    `zip_longest` to print the two team lists side by side
    (`first_team_member second_team_member`, filling missing names with `-`)
    for the first two teams.
""",
     given='students = ["Ana", "Ben", "Cy", "Dee", "Eli", "Fay", "Gus", "Hal"]\nrecords = [("Oslo", 40), ("Rome", 25), ("Oslo", 15), ("Rome", 30), ("Bern", 10), ("Oslo", 5)]',
     solution="from itertools import batched, groupby, zip_longest\n"
              "teams = [list(team) for team in batched(students, 3)]\n"
              "for team in teams:\n    print(team)\n"
              "records.sort()\n"
              "for city, rows in groupby(records, key=lambda row: row[0]):\n"
              "    print(city, sum(amount for _, amount in rows))\n"
              "for a, b in zip_longest(teams[0], teams[1], fillvalue=\"-\"):\n    print(a, b)")

# ------------------------------------------------------------ Q20 story project
nb.project("Web Log Analytics", story="""
    The *Rivertown Library* website keeps an access log, and the librarian
    wants a daily report. The log is a list of text lines, each in the form
    `date time METHOD path status user`. Every step builds on the one before.
""",
     given='lines = [\n'
           '    "2026-05-01 09:15:02 GET /home 200 alice",\n'
           '    "2026-05-01 09:40:11 GET /books 200 bob",\n'
           '    "2026-05-01 09:41:30 GET /books/42 404 bob",\n'
           '    "2026-05-01 10:05:00 POST /login 200 carol",\n'
           '    "2026-05-01 10:07:45 GET /home 200 carol",\n'
           '    "2026-05-01 10:30:18 GET /books 500 alice",\n'
           '    "2026-05-01 10:30:59 GET /books 500 alice",\n'
           '    "2026-05-01 10:31:20 GET /books 503 bob",\n'
           '    "2026-05-01 11:02:09 GET /home 200 dave",\n'
           '    "2026-05-01 11:20:33 GET /books 200 dave",\n'
           '    "2026-05-01 11:55:00 GET /home 200 alice",\n'
           '    "2026-05-01 12:01:12 GET /books/7 404 carol",\n'
           ']',
     steps=[
         ("Turn every line into a `namedtuple` called `Hit` with fields `time` (a `datetime` parsed with `strptime`), "
          "`method`, `path`, `status` (an int) and `user`. Keep them in a list `hits`, then print how many there are "
          "and the first hit.",
          "from collections import namedtuple\nfrom datetime import datetime\n"
          'Hit = namedtuple("Hit", ["time", "method", "path", "status", "user"])\n'
          "hits = []\nfor line in lines:\n"
          "    day, clock, method, path, status, user = line.split()\n"
          '    when = datetime.strptime(day + " " + clock, "%Y-%m-%d %H:%M:%S")\n'
          "    hits.append(Hit(when, method, path, int(status), user))\n"
          "print(len(hits))\nprint(hits[0])"),
         ("Use `Counter` to print the three most common paths and how many times each status code appeared "
          "(status codes in increasing order, one per line as `status: count`).",
          "from collections import Counter\n"
          "paths = Counter(hit.path for hit in hits)\nprint(paths.most_common(3))\n"
          "statuses = Counter(hit.status for hit in hits)\n"
          "for status in sorted(statuses):\n    print(str(status) + \":\", statuses[status])"),
         ("The hits are already in time order. Use `groupby` on the hour (`hit.time.hour`) to print how many hits "
          "happened in each hour as `HH:00 count`. Then use a `defaultdict(set)` to print, for each user in "
          "alphabetical order, the sorted list of different paths they visited.",
          "from itertools import groupby\nfrom collections import defaultdict\n"
          "for hour, group in groupby(hits, key=lambda hit: hit.time.hour):\n"
          '    print(str(hour).zfill(2) + ":00", len(list(group)))\n'
          "visited = defaultdict(set)\nfor hit in hits:\n    visited[hit.user].add(hit.path)\n"
          "for user in sorted(visited):\n    print(user, sorted(visited[user]))"),
         ("Spot an outage: slide a `deque(maxlen=3)` over the hits' status codes. Whenever the window is full and "
          "all three are 500 or higher, print the time of the latest hit as `HH:MM:SS`. Then print how long the "
          "log covers (last hit minus first hit) with `timedelta` arithmetic.",
          "from collections import deque\n"
          "window = deque(maxlen=3)\nfor hit in hits:\n    window.append(hit.status)\n"
          "    if len(window) == 3 and all(status >= 500 for status in window):\n"
          '        print("Outage at", hit.time.strftime("%H:%M:%S"))\n'
          'print("Covered:", hits[-1].time - hits[0].time)'),
         ("Finish with a report dictionary `report` holding `total`, `errors` (hits with status 400 or more), "
          "`busiest_path` and `users` (sorted list of users). Print it with `pprint.pprint`, then print a "
          "one-sentence summary, wrapped to width 40 with `textwrap.fill`.",
          "import pprint\nimport textwrap\n"
          "report = {\n"
          '    "total": len(hits),\n'
          '    "errors": len([hit for hit in hits if hit.status >= 400]),\n'
          '    "busiest_path": paths.most_common(1)[0][0],\n'
          '    "users": sorted(visited),\n'
          "}\npprint.pprint(report)\n"
          'summary = ("Today the library site served " + str(report["total"]) + " requests, " + str(report["errors"]) + " of them failed, and the busiest page was " + report["busiest_path"] + ".")\n'
          "print(textwrap.fill(summary, width=40))"),
     ])

nb.build()
