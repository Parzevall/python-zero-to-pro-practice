import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB19", title="Data Structures & Algorithms", intro="""
    How to choose the right container and the right method for the job:
    stacks, queues, heaps, linked lists, sorting, searching grids and maps,
    and a first taste of dynamic programming. Each question is a small real
    situation (queues, routes, schedules, leaderboards). The data is given
    to you as variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "Grades start at F below 60, then D (60), C (70), B (80), A (90). Use `bisect.bisect` on the cut-off list to print the letter for `score`.",
     given='score = 83\ncutoffs = [60, 70, 80, 90]\nletters = "FDCBA"',
     solution="import bisect\nprint(letters[bisect.bisect(cutoffs, score)])")

nb.q("Real-life", "A browser keeps its history as a stack in a list. The user presses Back: remove the most recent page, print it, then print the history that is left.",
     given='history = ["home", "news", "sports", "scores"]',
     solution="page = history.pop()\nprint(page)\nprint(history)")

nb.q("Real-life", "Customers wait in a line, and the first to arrive is served first. Use the `deque` as a queue: serve (remove) the first two customers, printing each name, then print the customers still waiting as a list.",
     given='from collections import deque\nline = deque(["Ana", "Ben", "Cleo", "Dev"])',
     solution="print(line.popleft())\nprint(line.popleft())\nprint(list(line))")

nb.q("Real-life", "Print the three best scores on the leaderboard, highest first, using `heapq`.",
     given="scores = [310, 95, 870, 455, 620, 120, 905]",
     solution="import heapq\nprint(heapq.nlargest(3, scores))")

nb.q("Real-life", "The club's member list has thousands of names and is checked again and again. Turn it into a structure where `in` is fast, then print `True` or `False` for each visitor.",
     given='members = ["ana", "ben", "cleo", "dev", "eli"]\nvisitors = ["cleo", "zoe"]',
     solution="member_set = set(members)\nfor visitor in visitors:\n    print(visitor in member_set)")

# ------------------------------------------------------------ Combine
nb.q("Puzzle", """
    Gift cards cost these prices (already sorted). Find two different cards
    that add up to exactly `budget`, using two pointers, one at each end,
    moving inwards. Print the two prices, or `No pair` if none fits.
""",
     given="prices = [5, 10, 15, 20, 35, 50]\nbudget = 55",
     solution="left = 0\nright = len(prices) - 1\nwhile left < right:\n"
              "    total = prices[left] + prices[right]\n"
              "    if total == budget:\n        print(prices[left], prices[right])\n        break\n"
              "    elif total < budget:\n        left += 1\n"
              "    else:\n        right -= 1\n"
              "else:\n    print(\"No pair\")")

nb.q("Real-life", """
    A shop wants to answer many questions like "how much did we sell from
    day 2 to day 5?". Build a prefix-sum list (`prefix[i]` is the total of
    the first `i` days), then print the sales from day 2 to day 5 (days count
    from 1, both included) using only the prefix list.
""",
     given="sales = [120, 80, 95, 200, 150, 60, 175]",
     solution="prefix = [0]\nfor amount in sales:\n    prefix.append(prefix[-1] + amount)\nprint(prefix[5] - prefix[1])")

nb.q("Real-life", """
    A website wants its busiest run of 3 days in a row. Slide a window of 3
    days over `visitors`, adding the new day and dropping the old one
    instead of re-adding each time. Print the best total and the day number
    (counting from 1) where that run starts.
""",
     given="visitors = [310, 280, 450, 520, 390, 610, 205, 330]\nk = 3",
     solution="window = sum(visitors[:k])\nbest = window\nstart = 1\n"
              "for i in range(k, len(visitors)):\n"
              "    window += visitors[i] - visitors[i - k]\n"
              "    if window > best:\n        best = window\n        start = i - k + 2\n"
              "print(best, start)")

nb.q("Puzzle", """
    The orders system should never process an order id twice. Walk through
    `order_ids` and print the first id that has already been seen, remembering
    the ids so far in a set. Print `All unique` if there is no repeat.
""",
     given='order_ids = ["A17", "B02", "C55", "B02", "A17", "D09"]',
     solution="seen = set()\nfor order_id in order_ids:\n"
              "    if order_id in seen:\n        print(order_id)\n        break\n"
              "    seen.add(order_id)\nelse:\n    print(\"All unique\")")

nb.q("Puzzle", """
    Write `quick_sort(items)` recursively: a list of 0 or 1 items is already
    sorted; otherwise take the first item as the pivot, and return the sorted
    smaller items, then the pivot, then the sorted larger ones (use list
    comprehensions). Sort the sprint times and print them.
""",
     given="times = [14.2, 11.8, 12.5, 13.9, 11.1, 12.5]",
     solution="def quick_sort(items):\n    if len(items) <= 1:\n        return items\n"
              "    pivot = items[0]\n"
              "    smaller = [x for x in items[1:] if x < pivot]\n"
              "    larger = [x for x in items[1:] if x >= pivot]\n"
              "    return quick_sort(smaller) + [pivot] + quick_sort(larger)\n"
              "print(quick_sort(times))")

# ------------------------------------------------------------ Small real tasks
nb.q("Build", """
    A playlist is a linked list: each `Node` holds a `song` and a link `next`
    to the following node (or `None`). Write the `Node` class, link the three
    songs in the order given, then walk from the head and print each song on
    its own line.
""",
     given='songs = ["Intro", "Sunrise", "Outro"]',
     solution="class Node:\n    def __init__(self, song):\n        self.song = song\n        self.next = None\n"
              "head = Node(songs[0])\ncurrent = head\n"
              "for song in songs[1:]:\n    current.next = Node(song)\n    current = current.next\n"
              "node = head\nwhile node is not None:\n    print(node.song)\n    node = node.next")

nb.q("Build", """
    Write `insertion_sort(items)` that sorts a list **in place** without using
    `sort` or `sorted`: for each item, shift the bigger items on its left one
    place right and drop it into the gap. Sort the parcel weights and print
    the list.
""",
     given="weights = [7.5, 2.0, 9.1, 4.4, 3.3]",
     solution="def insertion_sort(items):\n    for i in range(1, len(items)):\n"
              "        value = items[i]\n        j = i - 1\n"
              "        while j >= 0 and items[j] > value:\n"
              "            items[j + 1] = items[j]\n            j -= 1\n"
              "        items[j + 1] = value\n"
              "insertion_sort(weights)\nprint(weights)")

nb.q("Real-life", """
    A maze is a list of strings: `S` start, `E` exit, `#` wall, `.` floor. Use
    breadth-first search with a `deque` and a `visited` set to print the
    fewest steps (up, down, left, right) from `S` to `E`.
""",
     given='maze = [\n    "S..#..",\n    ".#.#.#",\n    ".#....",\n    ".##.#.",\n    "....#E",\n]',
     solution="from collections import deque\n"
              "for r in range(len(maze)):\n    for c in range(len(maze[0])):\n"
              '        if maze[r][c] == "S":\n            start = (r, c)\n'
              "queue = deque([(start, 0)])\nvisited = {start}\n"
              "while queue:\n    (r, c), steps = queue.popleft()\n"
              '    if maze[r][c] == "E":\n        print(steps)\n        break\n'
              "    for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n"
              "        nr, nc = r + dr, c + dc\n"
              "        inside = 0 <= nr < len(maze) and 0 <= nc < len(maze[0])\n"
              '        if inside and maze[nr][nc] != "#" and (nr, nc) not in visited:\n'
              "            visited.add((nr, nc))\n            queue.append(((nr, nc), steps + 1))")

nb.q("Real-life", """
    On a map `#` is land and `~` is sea. Count the islands (groups of land
    cells joined up, down, left or right). Use depth-first search with a list
    as a stack: when you find unvisited land, count one island and flood the
    rest of it.
""",
     given='grid = [\n    "##~~#",\n    "#~~~#",\n    "~~#~~",\n    "#~~##",\n]',
     solution="seen = set()\nislands = 0\n"
              "for r in range(len(grid)):\n    for c in range(len(grid[0])):\n"
              '        if grid[r][c] == "#" and (r, c) not in seen:\n'
              "            islands += 1\n            seen.add((r, c))\n            stack = [(r, c)]\n"
              "            while stack:\n                cr, cc = stack.pop()\n"
              "                for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:\n"
              "                    nr, nc = cr + dr, cc + dc\n"
              "                    if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):\n"
              '                        if grid[nr][nc] == "#" and (nr, nc) not in seen:\n'
              "                            seen.add((nr, nc))\n                            stack.append((nr, nc))\n"
              "print(islands)")

nb.q("Real-life", """
    A print shop serves jobs by priority (1 is most urgent) and, on equal
    priority, alphabetically. Push every `(priority, name)` job onto a heap
    with `heapq`, then pop them all and print each as `priority name`.
""",
     given='jobs = [(2, "invoice"), (1, "ticket"), (3, "flyer"), (1, "boarding pass")]',
     solution="import heapq\nheap = []\nfor job in jobs:\n    heapq.heappush(heap, job)\n"
              "while heap:\n    priority, name = heapq.heappop(heap)\n    print(priority, name)")

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Write `merge_sort(items)` recursively: split the list in half, sort each
    half, then merge the two sorted halves by repeatedly taking the smaller
    front item. Use it to sort the race finish times and print them.
""",
     given="finish = [64, 58, 71, 55, 69, 60, 58]",
     solution="def merge_sort(items):\n    if len(items) <= 1:\n        return items\n"
              "    mid = len(items) // 2\n"
              "    left = merge_sort(items[:mid])\n    right = merge_sort(items[mid:])\n"
              "    merged = []\n    i = 0\n    j = 0\n"
              "    while i < len(left) and j < len(right):\n"
              "        if left[i] <= right[j]:\n            merged.append(left[i])\n            i += 1\n"
              "        else:\n            merged.append(right[j])\n            j += 1\n"
              "    return merged + left[i:] + right[j:]\n"
              "print(merge_sort(finish))")

nb.q("Real-life", """
    The `flights` dict gives the ticket price of each direct flight (it works
    both ways). Write `cheapest(flights, start)` using Dijkstra's algorithm
    with a heap: it returns a dict of the lowest total price from `start` to
    every city. Print the prices for `"Oslo"` in alphabetical order of city,
    one `city price` pair per line.
""",
     given='flights = {\n    "Oslo": {"Rome": 120, "Paris": 80},\n    "Rome": {"Oslo": 120, "Paris": 30, "Cairo": 200},\n'
           '    "Paris": {"Oslo": 80, "Rome": 30, "Cairo": 260},\n    "Cairo": {"Rome": 200, "Paris": 260},\n}',
     solution="import heapq\n"
              "def cheapest(flights, start):\n    best = {start: 0}\n    heap = [(0, start)]\n"
              "    while heap:\n        price, city = heapq.heappop(heap)\n"
              "        if price > best[city]:\n            continue\n"
              "        for nxt, cost in flights[city].items():\n"
              "            total = price + cost\n"
              '            if total < best.get(nxt, float("inf")):\n'
              "                best[nxt] = total\n                heapq.heappush(heap, (total, nxt))\n"
              "    return best\n"
              'prices = cheapest(flights, "Oslo")\nfor city in sorted(prices):\n    print(city, prices[city])')

nb.q("Puzzle", """
    A vending machine has coins of the given values (unlimited supply of each).
    Write `fewest_coins(coins, amount)` with dynamic programming: `best[a]` is
    the fewest coins that make `a`, built up from 0 to `amount`. Return `-1`
    if the amount can't be made. Print the answer for each amount.
""",
     given="coins = [1, 3, 4]\namounts = [6, 7, 10]",
     solution="def fewest_coins(coins, amount):\n"
              '    best = [0] + [float("inf")] * amount\n'
              "    for a in range(1, amount + 1):\n"
              "        for coin in coins:\n"
              "            if coin <= a and best[a - coin] + 1 < best[a]:\n"
              "                best[a] = best[a - coin] + 1\n"
              '    return -1 if best[amount] == float("inf") else best[amount]\n'
              "for amount in amounts:\n    print(amount, fewest_coins(coins, amount))")

nb.q("Puzzle", """
    Two students typed from the same recording. Write `lcs_length(a, b)`, the
    length of their longest common subsequence (letters in the same order,
    not necessarily next to each other), using a table of
    `len(a) + 1` rows by `len(b) + 1` columns. If the letters match, take
    the diagonal value plus 1; otherwise the larger of the cell above and
    the cell to the left. Print the result.
""",
     given='first = "ABCBDAB"\nsecond = "BDCABA"',
     solution="def lcs_length(a, b):\n"
              "    table = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]\n"
              "    for i in range(1, len(a) + 1):\n"
              "        for j in range(1, len(b) + 1):\n"
              "            if a[i - 1] == b[j - 1]:\n"
              "                table[i][j] = table[i - 1][j - 1] + 1\n"
              "            else:\n"
              "                table[i][j] = max(table[i - 1][j], table[i][j - 1])\n"
              "    return table[len(a)][len(b)]\n"
              "print(lcs_length(first, second))")

# ------------------------------------------------------------ Project
nb.project("Route Planner", story="""
    A delivery van starts at the depot and must reach a drop-off point. The
    city map says how many minutes each road takes (roads work both ways).
    You will find the route with the fewest roads, then the quickest route,
    and finally print it turn by turn.
""",
     given='''
roads = {
    "Depot":   {"Park": 2, "Mill": 4, "Market": 10},
    "Park":    {"Depot": 2, "Mill": 1, "Bridge": 7},
    "Mill":    {"Depot": 4, "Park": 1, "Market": 5},
    "Bridge":  {"Park": 7, "Market": 3, "Station": 2},
    "Market":  {"Depot": 10, "Mill": 5, "Bridge": 3, "Station": 6},
    "Station": {"Bridge": 2, "Market": 6},
}
''',
     steps=[
         ("Print every place in alphabetical order with its number of roads, one per line like `Bridge 3`.",
          "for place in sorted(roads):\n    print(place, len(roads[place]))"),
         ("Write `fewest_roads(roads, start, goal)` using breadth-first search: it returns the list of places on a route with the fewest roads. Keep a `visited` set and, for each place reached, the route that got there. Print the route from `\"Depot\"` to `\"Station\"`.",
          "from collections import deque\n"
          "def fewest_roads(roads, start, goal):\n"
          "    queue = deque([[start]])\n    visited = {start}\n"
          "    while queue:\n        route = queue.popleft()\n"
          "        if route[-1] == goal:\n            return route\n"
          "        for nxt in sorted(roads[route[-1]]):\n"
          "            if nxt not in visited:\n                visited.add(nxt)\n                queue.append(route + [nxt])\n"
          "    return None\n"
          'print(fewest_roads(roads, "Depot", "Station"))'),
         ("Write `travel_times(roads, start)` with Dijkstra's algorithm and `heapq`: it returns a dict with the quickest total minutes from `start` to every place. Print the times from `\"Depot\"`, one `place minutes` line per place in alphabetical order.",
          "import heapq\n"
          "def travel_times(roads, start):\n    best = {start: 0}\n    heap = [(0, start)]\n"
          "    while heap:\n        minutes, place = heapq.heappop(heap)\n"
          "        if minutes > best[place]:\n            continue\n"
          "        for nxt, cost in roads[place].items():\n"
          "            total = minutes + cost\n"
          '            if total < best.get(nxt, float("inf")):\n'
          "                best[nxt] = total\n                heapq.heappush(heap, (total, nxt))\n"
          "    return best\n"
          'times = travel_times(roads, "Depot")\nfor place in sorted(times):\n    print(place, times[place])'),
         ("Write `quickest_route(roads, start, goal)` that does the same search but also remembers, for each place, which place you came from. It returns the total minutes and the list of places on the quickest route (walk back from the goal, then reverse). Print both for Depot to Station.",
          "def quickest_route(roads, start, goal):\n"
          "    best = {start: 0}\n    came_from = {}\n    heap = [(0, start)]\n"
          "    while heap:\n        minutes, place = heapq.heappop(heap)\n"
          "        if minutes > best[place]:\n            continue\n"
          "        for nxt, cost in roads[place].items():\n"
          "            total = minutes + cost\n"
          '            if total < best.get(nxt, float("inf")):\n'
          "                best[nxt] = total\n                came_from[nxt] = place\n"
          "                heapq.heappush(heap, (total, nxt))\n"
          "    route = [goal]\n"
          "    while route[-1] != start:\n        route.append(came_from[route[-1]])\n"
          "    route.reverse()\n    return best[goal], route\n"
          'minutes, route = quickest_route(roads, "Depot", "Station")\nprint(minutes)\nprint(route)'),
         ("Write `directions(roads, route)` that prints the route turn by turn, one line per road like `1. Depot -> Park (2 min)`, then a last line `Total: 11 min` (add up the road times, don't hard-code it). Call it with the quickest route you found.",
          "def directions(roads, route):\n    total = 0\n"
          "    for i in range(len(route) - 1):\n"
          "        cost = roads[route[i]][route[i + 1]]\n"
          "        total += cost\n"
          '        print(f"{i + 1}. {route[i]} -> {route[i + 1]} ({cost} min)")\n'
          '    print(f"Total: {total} min")\n'
          "directions(roads, route)"),
     ])

nb.build()
