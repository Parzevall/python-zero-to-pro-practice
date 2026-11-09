import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB18", title="Pythonic Idioms & Pattern Matching", intro="""
    The habits that make Python code read like Python: unpacking with `*`,
    the walrus operator `:=`, careful thinking about names versus objects,
    `for`/`else`, sentinels, EAFP, and the full power of `match`
    (sequence, mapping and class patterns). Every question is a small
    task to write; the story project at the end is a text adventure driven
    by `match`.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Output-match", """
    Unpack the word `"python"` in one line into its first letter, its last
    letter and the list of letters in between. Print the three on one line.
""",
     solution='first, *middle, last = "python"\nprint(first, middle, last)')

nb.q("Real-life", """
    A report row starts with a student's name followed by any number of
    scores. Unpack it in one line into `name` and `scores`, then print the
    name and the best score.
""",
     given='row = ["Ada", 90, 85, 77]',
     solution="name, *scores = row\nprint(name, max(scores))")

nb.q("Puzzle", """
    Build the boarding list in **one list literal**, using `*` and no `+` or
    `extend`: all the `vip` guests, then the text `"--- general ---"`, then
    all the `general` guests. Print it.
""",
     given='vip = ["Zed", "Amy"]\ngeneral = ["Bob", "Cy", "Di"]',
     solution='boarding = [*vip, "--- general ---", *general]\nprint(boarding)')

nb.q("Real-life", """
    A chat app limits messages to 10 characters. Print `Too long: N characters`
    (with the real length) if `message` is longer, otherwise print `OK`.
    Work out the length only once, inside the `if` line itself.
""",
     given='message = "Meet at the station"',
     solution='if (n := len(message)) > 10:\n    print(f"Too long: {n} characters")\nelse:\n    print("OK")')

nb.q("Real-life", """
    Two shops list the same item. Their prices were read from text. Print
    `True` if the two prices are equal in value.
""",
     given='price_a = int("1000")\nprice_b = int("1000")',
     solution="print(price_a == price_b)")

# ------------------------------------------------------- Combine
nb.q("Real-life", """
    Before a customer adds more things, keep a backup of the cart. Add
    `"milk"` to the cart, then print the cart and the backup. The backup must
    stay unchanged.
""",
     given='cart = ["apple", "bread"]',
     solution='backup = cart.copy()\ncart.append("milk")\nprint(cart)\nprint(backup)')

nb.q("Build", """
    A settings dict may hold `None` on purpose (meaning "no limit"). Write
    `get_setting(settings, key)` that returns the stored value, even when it
    is `None`, but returns the text `"unset"` when the key is absent. Use a
    unique sentinel object as the default for `.get()`. Print the result for
    `"timeout"`, `"retries"` and `"colour"`.
""",
     given='settings = {"timeout": None, "retries": 3}',
     solution="MISSING = object()\n\n"
              "def get_setting(settings, key):\n"
              "    value = settings.get(key, MISSING)\n"
              '    return "unset" if value is MISSING else value\n\n'
              'print(get_setting(settings, "timeout"))\n'
              'print(get_setting(settings, "retries"))\n'
              'print(get_setting(settings, "colour"))')

nb.q("Real-life", """
    Write `check(team)` that prints `Admin: <name>` for the first user whose
    role is `"admin"`, or `No admin` if the loop finds none. Use the `else`
    clause of the `for` loop. Call it for both teams.
""",
     given='team_a = [{"name": "Ann", "role": "viewer"}, {"name": "Raj", "role": "admin"}, {"name": "Li", "role": "admin"}]\n'
           'team_b = [{"name": "Eve", "role": "viewer"}, {"name": "Tom", "role": "editor"}]',
     solution="def check(team):\n"
              "    for user in team:\n"
              '        if user["role"] == "admin":\n'
              '            print("Admin:", user["name"])\n'
              "            break\n"
              "    else:\n"
              '        print("No admin")\n\n'
              "check(team_a)\ncheck(team_b)")

nb.q("Real-life", """
    A form returned messy entries. Build the list of entries that are not
    empty after stripping, **already stripped**. Strip each entry only once
    (use `:=` inside the comprehension) and print the list.
""",
     given='raw = ["3.5", "", " 7 ", "  ", "2"]',
     solution="cleaned = [text for item in raw if (text := item.strip())]\nprint(cleaned)")

nb.q("Real-life", """
    A game reads typed commands. For each command, split it into words and use
    `match` to print `Walking <direction>` for `go <direction>`, `Picked up
    <item>` for `take <item>`, `Bye` for the single word `quit`, and
    `Unknown: <command>` for anything else.
""",
     given='commands = ["go north", "take lamp", "quit now", "dance"]',
     solution="for command in commands:\n"
              "    match command.split():\n"
              '        case ["go", direction]:\n'
              '            print("Walking", direction)\n'
              '        case ["take", item]:\n'
              '            print("Picked up", item)\n'
              '        case ["quit"]:\n'
              '            print("Bye")\n'
              "        case _:\n"
              '            print("Unknown:", command)')

# ------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A UI sends events as dicts. Use `match` with mapping patterns to print:
    `Click at (x, y)` for clicks, `Key: <key>` for key presses, `Scroll up` or
    `Scroll down` for scroll events (negative `delta` is up), and `Ignored`
    for anything else. Handle every event.
""",
     given='events = [\n'
           '    {"type": "click", "x": 10, "y": 20, "button": "left"},\n'
           '    {"type": "key", "key": "Enter"},\n'
           '    {"type": "scroll", "delta": -3},\n'
           '    {"type": "scroll", "delta": 5},\n'
           '    {"type": "resize", "width": 800},\n'
           ']',
     solution="for event in events:\n"
              "    match event:\n"
              '        case {"type": "click", "x": x, "y": y}:\n'
              '            print(f"Click at ({x}, {y})")\n'
              '        case {"type": "key", "key": key}:\n'
              '            print("Key:", key)\n'
              '        case {"type": "scroll", "delta": delta} if delta < 0:\n'
              '            print("Scroll up")\n'
              '        case {"type": "scroll"}:\n'
              '            print("Scroll down")\n'
              "        case _:\n"
              '            print("Ignored")')

nb.q("Puzzle", """
    A traffic-light controller keeps its colours as constants inside the
    `Color` class. Write `action(light)` with `match` that returns `"stop"`
    for red, `"go"` for green, `"slow"` for yellow and `"broken"` for
    anything else, comparing against the `Color` constants (not
    string literals). Print the action for the four lights.
""",
     given='class Color:\n    RED = "red"\n    GREEN = "green"\n    YELLOW = "yellow"\n\n'
           'lights = ["green", "red", "yellow", "purple"]',
     solution="def action(light):\n"
              "    match light:\n"
              "        case Color.RED:\n"
              '            return "stop"\n'
              "        case Color.GREEN:\n"
              '            return "go"\n'
              "        case Color.YELLOW:\n"
              '            return "slow"\n'
              "        case _:\n"
              '            return "broken"\n\n'
              "for light in lights:\n"
              "    print(light, action(light))")

nb.q("Real-life", """
    Read the `stream` five characters at a time. Loop until a read returns
    an empty string, printing each chunk between `[` and `]`. Read in the
    `while` condition itself with `:=`, so there is a single `read` call in
    your code.
""",
     given='import io\nstream = io.StringIO("The quick brown fox")',
     solution="while chunk := stream.read(5):\n    print(f\"[{chunk}]\")")

nb.q("Real-life", """
    Write `read_port(config)` that returns the port from
    `config["server"]["port"]` as an int. If a key is missing return
    `"missing"`, if the port isn't a number return `"bad"`. Ask forgiveness
    rather than permission: use `try` / `except` / `else`, with the
    conversion in the `try`. Print the result for each config.
""",
     given='configs = [{"server": {"port": "8080"}}, {"server": {}}, {"server": {"port": "eighty"}}, {}]',
     solution="def read_port(config):\n"
              "    try:\n"
              '        port = int(config["server"]["port"])\n'
              "    except KeyError:\n"
              '        return "missing"\n'
              "    except ValueError:\n"
              '        return "bad"\n'
              "    else:\n"
              "        return port\n\n"
              "for config in configs:\n"
              "    print(read_port(config))")

nb.q("Puzzle", """
    Use sequence patterns. Write `total(items)` that sums a list **recursively**
    (empty list is 0, otherwise the first item plus the total of the rest).
    Then write `describe(items)` that returns `"empty"` for an empty list,
    `"one item: X"` for one, and `"from X to Y"` for longer lists. Print
    `total([1, 2, 3, 4, 5])` and the description of three lists.
""",
     solution="def total(items):\n"
              "    match items:\n"
              "        case []:\n"
              "            return 0\n"
              "        case [head, *tail]:\n"
              "            return head + total(tail)\n\n"
              "def describe(items):\n"
              "    match items:\n"
              "        case []:\n"
              '            return "empty"\n'
              "        case [only]:\n"
              '            return f"one item: {only}"\n'
              "        case [first, *_, last]:\n"
              '            return f"from {first} to {last}"\n\n'
              "print(total([1, 2, 3, 4, 5]))\n"
              "print(describe([]))\n"
              'print(describe(["solo"]))\n'
              "print(describe([4, 8, 15, 16]))")

# ------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Evaluate arithmetic trees written as nested tuples. A node is a plain
    number, `("add", a, b)`, `("mul", a, b)`, `("neg", a)` or `("div", a, b)`.
    Write `evaluate(node)` with `match`: numbers (int or float) return
    themselves, and dividing by zero returns the text `"div by zero"`. Print
    the result for each tree.
""",
     given='trees = [\n'
           '    ("add", 2, ("mul", 3, 4)),\n'
           '    ("neg", ("add", 1, 2.5)),\n'
           '    ("div", ("mul", 6, 4), ("add", 1, 2)),\n'
           '    ("div", 5, ("add", 2, -2)),\n'
           ']',
     solution="def evaluate(node):\n"
              "    match node:\n"
              "        case int() | float():\n"
              "            return node\n"
              '        case ("add", left, right):\n'
              "            return evaluate(left) + evaluate(right)\n"
              '        case ("mul", left, right):\n'
              "            return evaluate(left) * evaluate(right)\n"
              '        case ("neg", inner):\n'
              "            return -evaluate(inner)\n"
              '        case ("div", left, right):\n'
              "            bottom = evaluate(right)\n"
              "            if bottom == 0:\n"
              '                return "div by zero"\n'
              "            return evaluate(left) / bottom\n\n"
              "for tree in trees:\n"
              "    print(evaluate(tree))")

nb.q("Real-life", """
    A drawing app has `Circle` and `Rect` shapes. Write `describe(shape)` with
    **class patterns** that returns: `"invalid"` for a circle whose radius is
    0 or less; `"circle, area A"` for other circles; `"square, side S"` for a
    rectangle whose width equals its height; `"rect, area A"` for other
    rectangles; and `"unknown"` for anything else. Round areas to 1 decimal
    place (use 3.14159 for pi). Print one line per shape.
""",
     given='class Circle:\n'
           '    __match_args__ = ("radius",)\n'
           '    def __init__(self, radius):\n'
           '        self.radius = radius\n\n'
           'class Rect:\n'
           '    __match_args__ = ("width", "height")\n'
           '    def __init__(self, width, height):\n'
           '        self.width = width\n'
           '        self.height = height\n\n'
           'shapes = [Circle(2), Circle(0), Rect(3, 3), Rect(2, 5), "blob"]',
     solution="def describe(shape):\n"
              "    match shape:\n"
              "        case Circle(radius) if radius <= 0:\n"
              '            return "invalid"\n'
              "        case Circle(radius):\n"
              '            return f"circle, area {round(3.14159 * radius ** 2, 1)}"\n'
              "        case Rect(width, height) if width == height:\n"
              '            return f"square, side {width}"\n'
              "        case Rect(width, height):\n"
              '            return f"rect, area {width * height}"\n'
              "        case _:\n"
              '            return "unknown"\n\n'
              "for shape in shapes:\n"
              "    print(describe(shape))")

nb.q("Puzzle", """
    Build a 3x3 board of zeros as a list of three **separate** rows. Set the
    centre cell to 5. Take a snapshot copy that is fully independent (also its
    rows), then set the top-left cell of the board to 9. Print the board, the
    snapshot, and whether the first two rows of the board are the same object.
""",
     solution="import copy\n\n"
              "board = [[0] * 3 for _ in range(3)]\n"
              "board[1][1] = 5\n"
              "snapshot = copy.deepcopy(board)\n"
              "board[0][0] = 9\n"
              'print("Board:", board)\n'
              'print("Snapshot:", snapshot)\n'
              'print("Same row object:", board[0] is board[1])')

nb.q("Puzzle", """
    For each number, find its smallest divisor greater than 1 (try 2, 3, 4,
    ... up to but not including the number itself). Print `<n> is prime` if
    there is none, otherwise `<n> = <divisor> x <rest>`. Use the `else` clause
    of the `for` loop, with no flag variable.
""",
     given="numbers = [29, 35, 49, 53, 91]",
     solution="for n in numbers:\n"
              "    for d in range(2, n):\n"
              "        if n % d == 0:\n"
              '            print(f"{n} = {d} x {n // d}")\n'
              "            break\n"
              "    else:\n"
              '        print(f"{n} is prime")')

# ------------------------------------------------------------ Q20 project
nb.project("Cave Text Adventure", story="""
    You are writing the command interpreter for a tiny text adventure. The
    world is a handful of rooms; the player types commands like `go north` or
    `take lamp`. Build the pieces one at a time, then let `match` tie them
    together.
""",
     given='rooms = {\n'
           '    "hall": {"desc": "A cold stone hall.", "exits": {"north": "kitchen", "east": "library"}, "items": ["lamp"]},\n'
           '    "kitchen": {"desc": "A dusty kitchen.", "exits": {"south": "hall"}, "items": ["knife"]},\n'
           '    "library": {"desc": "Shelves of old books.", "exits": {"west": "hall"}, "items": ["key"]},\n'
           '}\n'
           'state = {"room": "hall", "inventory": []}',
     steps=[
         ("Write `describe(state)`. It prints the description of the current room, then `Exits: ` and the exit names "
          "sorted and joined by `, `, and, only if the room has items, `You see: ` and the items joined by `, `. "
          "Call it once for the starting state.",
          "def describe(state):\n"
          '    room = rooms[state["room"]]\n'
          '    print(room["desc"])\n'
          '    print("Exits:", ", ".join(sorted(room["exits"])))\n'
          '    if room["items"]:\n'
          '        print("You see:", ", ".join(room["items"]))\n\n'
          "describe(state)"),
         ("Write `move(state, direction)`. If the current room has an exit that way, change the state's room and "
          "call `describe`; otherwise print `You can't go <direction>`. Try `east`, then `up`.",
          "def move(state, direction):\n"
          '    exits = rooms[state["room"]]["exits"]\n'
          "    if direction in exits:\n"
          '        state["room"] = exits[direction]\n'
          "        describe(state)\n"
          "    else:\n"
          '        print("You can\'t go", direction)\n\n'
          'move(state, "east")\n'
          'move(state, "up")'),
         ("Write `take(state, item)`. If the item is in the current room, move it from the room's items to the "
          "player's inventory and print `Taken: <item>`; otherwise print `No <item> here`. Try `key`, then `key` again.",
          "def take(state, item):\n"
          '    items = rooms[state["room"]]["items"]\n'
          "    if item in items:\n"
          "        items.remove(item)\n"
          '        state["inventory"].append(item)\n'
          '        print("Taken:", item)\n'
          "    else:\n"
          '        print("No", item, "here")\n\n'
          'take(state, "key")\n'
          'take(state, "key")'),
         ("Write `execute(state, line)` that lowercases and splits the line, then uses `match`: `look`; `go` or "
          "`walk` plus a direction; `take` plus an item; `inventory` or `i` (print `Carrying: ` and the sorted items, "
          "or `Carrying nothing`); an empty line (print `Say something`); and anything else (print `I don't "
          "understand: <line>`). Try it on the list of lines given in the expected output.",
          "def execute(state, line):\n"
          "    match line.lower().split():\n"
          '        case ["look"]:\n'
          "            describe(state)\n"
          '        case ["go" | "walk", direction]:\n'
          "            move(state, direction)\n"
          '        case ["take", item]:\n'
          "            take(state, item)\n"
          '        case ["inventory" | "i"]:\n'
          '            if state["inventory"]:\n'
          '                print("Carrying:", ", ".join(sorted(state["inventory"])))\n'
          "            else:\n"
          '                print("Carrying nothing")\n'
          "        case []:\n"
          '            print("Say something")\n'
          "        case _:\n"
          '            print("I don\'t understand:", line)\n\n'
          'for line in ["LOOK", "walk west", "i", "", "dance now"]:\n'
          '    print(">", line)\n'
          "    execute(state, line)"),
         ("Play a whole game from a script. Start a fresh `state` in the hall. Take lines from the front of the "
          "script list with `pop(0)`, in the `while` condition itself with `:=`; a line `quit` ends the game. Echo each line as `> <line>`, run it with `execute`, and when the "
          "game ends print `Game over in <room>` and the player's sorted inventory.",
          'state = {"room": "hall", "inventory": []}\n'
          'lines = ["take lamp", "go north", "take knife", "go south", "go up", "i", "quit", "look"]\n'
          'while (line := lines.pop(0)) != "quit":\n'
          '    print(">", line)\n'
          "    execute(state, line)\n"
          'print("Game over in", state["room"])\n'
          'print(sorted(state["inventory"]))'),
     ])

nb.build()
