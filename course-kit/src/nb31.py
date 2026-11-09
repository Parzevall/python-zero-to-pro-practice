import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB31", title="Real-World Programs", intro="""
    How real programs are put together: command-line tools, configuration,
    small databases, other programs run as subprocesses, archives and package
    layout. Every task is a small real job (a to-do CLI, a shop database, a
    log summary, a backup). Command-line tools are driven by calling
    `parse_args([...])` with a list of arguments, databases live in memory
    (`":memory:"`), files live in temporary folders, and subprocesses only
    run `sys.executable`, so everything is safe to run anywhere.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    A greeting tool takes `--name` (text) and `--times` (a whole number,
    default 1). Build the parser, parse the given argument list, and print the
    greeting `Hello, <name>!` that many times.
""",
     given='argv = ["--name", "Ana", "--times", "2"]',
     solution="import argparse\n"
              "parser = argparse.ArgumentParser()\n"
              'parser.add_argument("--name")\n'
              'parser.add_argument("--times", type=int, default=1)\n'
              "args = parser.parse_args(argv)\n"
              "for _ in range(args.times):\n"
              '    print("Hello, " + args.name + "!")')

nb.q("Real-life", """
    Open a fresh in-memory database, create a table `pets` with a text `name`
    and an integer `age`, insert one pet (`Rex`, 4) using placeholders, and
    print the rows you get back with a `SELECT`.
""",
     solution="import sqlite3\n"
              'conn = sqlite3.connect(":memory:")\n'
              'conn.execute("CREATE TABLE pets (name TEXT, age INTEGER)")\n'
              'conn.execute("INSERT INTO pets VALUES (?, ?)", ("Rex", 4))\n'
              'print(conn.execute("SELECT * FROM pets").fetchall())')

nb.q("Real-life", """
    An app's settings arrive as TOML text. Parse it and print the database
    host and the debug flag.
""",
     given='settings_text = """\n[server]\nport = 8080\ndebug = true\n\n[database]\nhost = "db.local"\n"""',
     solution="import tomllib\n"
              "settings = tomllib.loads(settings_text)\n"
              'print(settings["database"]["host"])\n'
              'print(settings["server"]["debug"])')

nb.q("Real-life", """
    Read the setting `APP_PORT` from the environment as a number. Then read
    `APP_MODE`, falling back to `"production"` when it isn't set. Print both.
""",
     given='import os\nos.environ["APP_PORT"] = "8080"\nos.environ.pop("APP_MODE", None)',
     solution='port = int(os.environ["APP_PORT"])\n'
              'mode = os.environ.get("APP_MODE", "production")\n'
              "print(port)\nprint(mode)")

nb.q("Output-match", """
    Run a child Python process (using the same interpreter that runs this
    code) that prints the result of `6 * 7`. Capture its output as text and
    print the output without the trailing newline, then print its return code.
""",
     solution="import subprocess, sys\n"
              'result = subprocess.run([sys.executable, "-c", "print(6 * 7)"],\n'
              "                        capture_output=True, text=True)\n"
              "print(result.stdout.strip())\n"
              "print(result.returncode)")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    A user types their name into a search box and the program looks them up.
    Look up the user whose name is **exactly** `typed`, in a way that cannot
    be tricked by what the user types. Print how many rows matched, then
    prove the lookup still works by searching for `"Bea"` and printing that
    row.
""",
     given='import sqlite3\n'
           'conn = sqlite3.connect(":memory:")\n'
           'conn.execute("CREATE TABLE users (name TEXT, role TEXT)")\n'
           'conn.executemany("INSERT INTO users VALUES (?, ?)",\n'
           '                 [("Ana", "admin"), ("Bea", "guest"), ("Cy", "guest")])\n'
           "typed = \"x' OR '1'='1\"",
     solution='query = "SELECT * FROM users WHERE name = ?"\n'
              "print(len(conn.execute(query, (typed,)).fetchall()))\n"
              'print(conn.execute(query, ("Bea",)).fetchall())')

nb.q("Build", """
    A to-do tool has two sub-commands: `add TEXT` (with an optional
    `--priority`, a number, default 3) and `done ID` (ID is a number). Build
    the parser with sub-commands and parse each argument list in `commands`.
    For each, print the command name and then its values, as in the expected
    output.
""",
     given='commands = [["add", "buy milk", "--priority", "1"], ["add", "call mum"], ["done", "7"]]',
     solution="import argparse\n"
              "parser = argparse.ArgumentParser(prog=\"todo\")\n"
              'sub = parser.add_subparsers(dest="command", required=True)\n'
              'add = sub.add_parser("add")\n'
              'add.add_argument("text")\n'
              'add.add_argument("--priority", type=int, default=3)\n'
              'done = sub.add_parser("done")\n'
              'done.add_argument("id", type=int)\n'
              "for argv in commands:\n"
              "    args = parser.parse_args(argv)\n"
              '    if args.command == "add":\n'
              '        print("add", args.text, args.priority)\n'
              "    else:\n"
              '        print("done", args.id)')

nb.q("Real-life", """
    Query the `books` table so that each row can be read **by column name**
    instead of by position. Print each book as `title by author`, ordered by
    title.
""",
     given='import sqlite3\n'
           'conn = sqlite3.connect(":memory:")\n'
           'conn.execute("CREATE TABLE books (title TEXT, author TEXT, year INTEGER)")\n'
           'conn.executemany("INSERT INTO books VALUES (?, ?, ?)",\n'
           '                 [("Dune", "Herbert", 1965), ("Emma", "Austen", 1815), ("Ulysses", "Joyce", 1922)])',
     solution="conn.row_factory = sqlite3.Row\n"
              'for row in conn.execute("SELECT * FROM books ORDER BY title"):\n'
              '    print(row["title"], "by", row["author"])')

nb.q("Real-life", """
    Create three small text files in a temporary folder, pack them into one
    zip archive (also inside that folder), then open the archive and print
    its file names sorted. Finally print the contents of `b.txt` read
    straight from the archive.
""",
     given='import tempfile\nfrom pathlib import Path\nnames = ["a.txt", "b.txt", "c.txt"]',
     solution="import zipfile\n"
              "with tempfile.TemporaryDirectory() as folder:\n"
              "    for name in names:\n"
              '        Path(folder, name).write_text("data in " + name)\n'
              '    archive_path = Path(folder, "bundle.zip")\n'
              '    with zipfile.ZipFile(archive_path, "w") as archive:\n'
              "        for name in names:\n"
              "            archive.write(Path(folder, name), arcname=name)\n"
              '    with zipfile.ZipFile(archive_path) as archive:\n'
              "        print(sorted(archive.namelist()))\n"
              '        print(archive.read("b.txt").decode())')

nb.q("Puzzle", """
    A search page puts the user's text into HTML, and the text may contain
    `<` or `&`. A **t-string** (a string with a `t` in front, Python 3.14)
    keeps the values separate from the fixed text. Write `safe_html(template)`
    that joins the fixed text as it is, but runs every interpolated value
    through `html.escape` (as text). Use it on a t-string with the name
    `visitor` and print the result.
""",
     given='visitor = "<b>Eve & Co</b>"',
     solution="import html\n"
              "from string.templatelib import Interpolation\n"
              "def safe_html(template):\n"
              "    parts = []\n"
              "    for part in template:\n"
              "        if isinstance(part, Interpolation):\n"
              "            parts.append(html.escape(str(part.value)))\n"
              "        else:\n"
              "            parts.append(part)\n"
              '    return "".join(parts)\n'
              'print(safe_html(t"<p>Hello {visitor}</p>"))')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    Settings are layered: built-in defaults, then a TOML file, then
    environment variables, each layer overriding the one before it. Merge
    the layers (`env` already holds only the relevant values, with numbers as
    text) and print the final settings as a dict sorted by key.
""",
     given='import tomllib\n'
           'defaults = {"port": 80, "debug": False, "name": "app"}\n'
           'file_text = "port = 8080\\nname = \\"shop\\""\n'
           'env = {"APP_PORT": "9000"}',
     solution="from_file = tomllib.loads(file_text)\n"
              "from_env = {}\n"
              'if "APP_PORT" in env:\n'
              '    from_env["port"] = int(env["APP_PORT"])\n'
              "settings = defaults | from_file | from_env\n"
              "print(dict(sorted(settings.items())))")

nb.q("Real-life", """
    A bank transfer must move money **all or nothing**. Move `amount` from
    one account to the other inside one transaction (`with conn:`). The table
    refuses negative balances, so a transfer that is too large fails: catch
    the database's integrity error and print `Transfer failed`. After every
    transfer, successful or not, print both balances (as a list of tuples,
    ordered by name). Do this for both transfers in `amounts`, moving money
    from `ana` to `ben`.
""",
     given='import sqlite3\n'
           'conn = sqlite3.connect(":memory:")\n'
           'conn.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER CHECK (balance >= 0))")\n'
           'conn.executemany("INSERT INTO accounts VALUES (?, ?)", [("ana", 100), ("ben", 20)])\n'
           'conn.commit()\n'
           "amounts = [30, 500]",
     solution="for amount in amounts:\n"
              "    try:\n"
              "        with conn:\n"
              '            conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (amount, "ben"))\n'
              '            conn.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?", (amount, "ana"))\n'
              "    except sqlite3.IntegrityError:\n"
              '        print("Transfer failed")\n'
              '    print(conn.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall())')

nb.q("Build", """
    Create a tiny package in a temporary folder: a folder `greeter` holding an
    empty `__init__.py` and a `__main__.py` that prints `Hello from greeter`
    followed by any command-line arguments. Then run the package as a program
    (`-m greeter`, with the interpreter that runs this code, from inside the
    temporary folder) with the extra argument `Ana`, and print what it
    printed.
""",
     given="import subprocess, sys, tempfile\nfrom pathlib import Path",
     solution="with tempfile.TemporaryDirectory() as folder:\n"
              '    package = Path(folder, "greeter")\n'
              "    package.mkdir()\n"
              '    (package / "__init__.py").write_text("")\n'
              '    (package / "__main__.py").write_text(\n'
              '        "import sys\\nprint(\'Hello from greeter\', *sys.argv[1:])\\n")\n'
              '    result = subprocess.run([sys.executable, "-m", "greeter", "Ana"],\n'
              "                            cwd=folder, capture_output=True, text=True)\n"
              "    print(result.stdout.strip())")

nb.q("Real-life", """
    Run two child programs and treat their arguments safely: pass each
    argument as a separate list item, never glue a shell command together.
    The first child prints its own first argument back (use the nasty text
    `file; echo hacked` as that argument), the second exits with status 3.
    For the second, use `check=True`, catch the error and print its return
    code.
""",
     given="import subprocess, sys",
     solution="nasty = \"file; echo hacked\"\n"
              "echo = subprocess.run(\n"
              '    [sys.executable, "-c", "import sys; print(sys.argv[1])", nasty],\n'
              "    capture_output=True, text=True)\n"
              "print(echo.stdout.strip())\n"
              "try:\n"
              '    subprocess.run([sys.executable, "-c", "raise SystemExit(3)"], check=True)\n'
              "except subprocess.CalledProcessError as error:\n"
              '    print("child failed with", error.returncode)')

nb.q("Real-life", """
    The project's `pyproject.toml` is given as text. Parse it and print the
    project name and version on one line (`name version`), then the
    dependencies sorted alphabetically (one per line), then the command that
    the `[project.scripts]` table installs, as `command -> target`.
""",
     given='pyproject = """\n[project]\nname = "shopkit"\nversion = "0.3.1"\nrequires-python = ">=3.10"\n'
           'dependencies = ["requests>=2.30", "click", "attrs"]\n\n[project.scripts]\nshop = "shopkit.cli:main"\n"""',
     solution="import tomllib\n"
              "data = tomllib.loads(pyproject)\n"
              'project = data["project"]\n'
              'print(project["name"], project["version"])\n'
              'for dependency in sorted(project["dependencies"]):\n'
              "    print(dependency)\n"
              'for command, target in project["scripts"].items():\n'
              '    print(command, "->", target)')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    Write `main(argv)` for a log summary tool. It takes a log file path, an
    optional `--level` (only `INFO`, `WARN` or `ERROR`, default `ERROR`) and
    an optional `--top` (a number, default 2). It reads the file (each line
    is `LEVEL service message`), keeps the lines of that level, and prints
    how many there were, then the `--top` services with the most such lines
    (highest first, ties by name) as `service: count`. The log file is
    written for you in a temporary folder. Call `main` with two different
    argument lists.
""",
     given='import tempfile\nfrom pathlib import Path\n'
           'log_text = """ERROR db timeout\nINFO web started\nERROR web 500\nWARN db slow\n'
           'ERROR db refused\nERROR cache miss\nERROR web 502\nINFO db ok\n"""\n'
           'folder = tempfile.TemporaryDirectory()\n'
           'log_path = Path(folder.name, "app.log")\n'
           'log_path.write_text(log_text)',
     solution="import argparse\n"
              "from collections import Counter\n"
              "def main(argv):\n"
              "    parser = argparse.ArgumentParser()\n"
              '    parser.add_argument("path")\n'
              '    parser.add_argument("--level", choices=["INFO", "WARN", "ERROR"], default="ERROR")\n'
              '    parser.add_argument("--top", type=int, default=2)\n'
              "    args = parser.parse_args(argv)\n"
              "    counts = Counter()\n"
              "    for line in Path(args.path).read_text().splitlines():\n"
              "        level, service, _ = line.split(maxsplit=2)\n"
              "        if level == args.level:\n"
              "            counts[service] += 1\n"
              '    print(args.level, "lines:", sum(counts.values()))\n'
              "    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))\n"
              "    for service, count in ranked[:args.top]:\n"
              '        print(service + ": " + str(count))\n'
              "main([str(log_path)])\n"
              'main([str(log_path), "--level", "INFO", "--top", "1"])\n'
              "folder.cleanup()")

nb.q("Puzzle", """
    Find the **big spenders**: customers whose orders add up to more than 50,
    using the database to do the adding (`GROUP BY` and `HAVING`, with a
    placeholder for the limit). Print `customer total` for each, biggest
    total first.
""",
     given='import sqlite3\n'
           'conn = sqlite3.connect(":memory:")\n'
           'conn.execute("CREATE TABLE orders (customer TEXT, amount INTEGER)")\n'
           'conn.executemany("INSERT INTO orders VALUES (?, ?)", [\n'
           '    ("ana", 30), ("ben", 12), ("ana", 25), ("cy", 70), ("ben", 15), ("dee", 5), ("ben", 9)])\n'
           "limit = 50",
     solution='query = """SELECT customer, SUM(amount) AS total FROM orders\n'
              '         GROUP BY customer HAVING total > ? ORDER BY total DESC"""\n'
              "for customer, total in conn.execute(query, (limit,)):\n"
              "    print(customer, total)")

nb.q("Puzzle", """
    Back up and verify. Build a folder `project` with a few files (one in a
    sub-folder), pack it with `shutil.make_archive` as a zip, unpack the
    archive into a different folder with `shutil.unpack_archive`, and prove
    the copy is identical: print `True` if both trees have the same sorted
    relative file paths **and** the same SHA-256 hash for every file,
    otherwise `False`. Also print the number of files.
""",
     given='import tempfile\nfrom pathlib import Path\n'
           'files = {"readme.txt": "hello", "src/app.py": "print(1)", "src/util.py": "x = 2"}',
     solution="import hashlib\nimport shutil\n"
              "def fingerprint(root):\n"
              "    result = {}\n"
              "    for path in sorted(Path(root).rglob(\"*\")):\n"
              "        if path.is_file():\n"
              "            result[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()\n"
              "    return result\n"
              "with tempfile.TemporaryDirectory() as folder:\n"
              '    source = Path(folder, "project")\n'
              "    for name, text in files.items():\n"
              "        target = source / name\n"
              "        target.parent.mkdir(parents=True, exist_ok=True)\n"
              "        target.write_text(text)\n"
              '    archive = shutil.make_archive(str(Path(folder, "backup")), "zip", source)\n'
              '    restored = Path(folder, "restored")\n'
              "    shutil.unpack_archive(archive, restored)\n"
              "    print(fingerprint(source) == fingerprint(restored))\n"
              "    print(len(fingerprint(restored)))")

nb.q("Puzzle", """
    Schema migrations. A database remembers its version in `PRAGMA
    user_version`. Write `migrate(conn)` that applies, in order, only the
    migrations in `migrations` newer than the stored version, and after each
    one stores the new version number. Run it twice (the second run must do
    nothing), printing the version and the list of tables (sorted) after
    each run.
""",
     given='import sqlite3\n'
           'conn = sqlite3.connect(":memory:")\n'
           'migrations = [\n'
           '    "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)",\n'
           '    "ALTER TABLE users ADD COLUMN email TEXT",\n'
           '    "CREATE TABLE posts (id INTEGER PRIMARY KEY, user_id INTEGER, body TEXT)",\n'
           ']',
     solution="def migrate(conn):\n"
              '    version = conn.execute("PRAGMA user_version").fetchone()[0]\n'
              "    for number, sql in enumerate(migrations, start=1):\n"
              "        if number > version:\n"
              "            with conn:\n"
              "                conn.execute(sql)\n"
              '                conn.execute(f"PRAGMA user_version = {number}")\n'
              "def report(conn):\n"
              '    version = conn.execute("PRAGMA user_version").fetchone()[0]\n'
              '    tables = conn.execute("SELECT name FROM sqlite_master WHERE type = \'table\' ORDER BY name").fetchall()\n'
              "    print(version, [name for (name,) in tables])\n"
              "migrate(conn)\nreport(conn)\nmigrate(conn)\nreport(conn)")

# ------------------------------------------------------------ Q20 story project
nb.project("Expense Tracker CLI", story="""
    You are building a small command-line expense tracker for a friend who
    keeps losing receipts. Everything is driven the way a real tool is: an
    argument parser, a database, settings from a TOML file and the
    environment, logging, and a final check that runs the report in a child
    process. The database lives in memory and the files in a temporary folder,
    so you can run it as often as you like. Each step builds on the one
    before.
""",
     given='import tempfile\nfrom pathlib import Path\n\n'
           'workdir = tempfile.TemporaryDirectory()\n'
           'config_path = Path(workdir.name, "tracker.toml")\n'
           'config_path.write_text("[budget]\\nmonthly_cents = 20000\\n\\n[report]\\ntop = 2\\n")\n'
           'environment = {"TRACKER_TOP": "3"}      # stands in for os.environ',
     steps=[
         ("""
          Create the database: connect to `":memory:"` and make an `expenses`
          table (`id` integer primary key, `day` text, `category` text,
          `cents` integer, `note` text), with rows readable by column name.
          Write `add_expense(conn, day, category, cents, note)` using
          placeholders (inside a transaction). Add the four expenses in the
          solution and print how many rows the table holds.
          """,
          "import sqlite3\n"
          'conn = sqlite3.connect(":memory:")\n'
          "conn.row_factory = sqlite3.Row\n"
          'conn.execute("CREATE TABLE expenses (id INTEGER PRIMARY KEY, day TEXT, category TEXT, cents INTEGER, note TEXT)")\n'
          "def add_expense(conn, day, category, cents, note):\n"
          "    with conn:\n"
          '        conn.execute("INSERT INTO expenses (day, category, cents, note) VALUES (?, ?, ?, ?)",\n'
          "                     (day, category, cents, note))\n"
          'add_expense(conn, "2025-03-01", "food", 1250, "lunch")\n'
          'add_expense(conn, "2025-03-02", "travel", 8400, "train")\n'
          'add_expense(conn, "2025-03-03", "food", 3100, "dinner; \'friends\'")\n'
          'add_expense(conn, "2025-03-04", "fun", 4500, "cinema")\n'
          'print(conn.execute("SELECT COUNT(*) FROM expenses").fetchone()[0])'),
         ("""
          Build `make_parser()` with two sub-commands: `add DAY CATEGORY EUROS
          NOTE` (EUROS is a decimal number) and `report` (with an optional
          `--top`, a number). Parse `["add", "2025-03-05", "food", "12.50",
          "snack"]` and `["report", "--top", "2"]` and print `command` and the
          rest of each result's values (for `add` the four values with euros
          converted to whole cents; for `report` the top).
          """,
          "import argparse\n"
          "def make_parser():\n"
          '    parser = argparse.ArgumentParser(prog="tracker")\n'
          '    sub = parser.add_subparsers(dest="command", required=True)\n'
          '    add = sub.add_parser("add")\n'
          '    add.add_argument("day")\n'
          '    add.add_argument("category")\n'
          '    add.add_argument("euros", type=float)\n'
          '    add.add_argument("note")\n'
          '    report = sub.add_parser("report")\n'
          '    report.add_argument("--top", type=int)\n'
          "    return parser\n"
          "parser = make_parser()\n"
          'args = parser.parse_args(["add", "2025-03-05", "food", "12.50", "snack"])\n'
          'print(args.command, args.day, args.category, round(args.euros * 100), args.note)\n'
          'args = parser.parse_args(["report", "--top", "2"])\n'
          "print(args.command, args.top)"),
         ("""
          Load the settings: read the TOML file at `config_path` and take
          `top` from `[report]` and the monthly budget from `[budget]`; if
          `TRACKER_TOP` is in `environment`, it overrides the file's `top`
          (convert to a number). Print the budget in cents and the final
          `top`.
          """,
          "import tomllib\n"
          "settings = tomllib.loads(config_path.read_text())\n"
          'budget_cents = settings["budget"]["monthly_cents"]\n'
          'top = settings["report"]["top"]\n'
          'if "TRACKER_TOP" in environment:\n'
          '    top = int(environment["TRACKER_TOP"])\n'
          'print("budget:", budget_cents)\n'
          'print("top:", top)'),
         ("""
          Write `run(argv)` that parses `argv` with your parser and does the
          work. For `add` it adds the expense and logs `added <note>` at
          INFO level. For `report` it prints the total spent in cents, the
          categories with their totals (highest total first, at most `--top`
          of them, or the settings' `top` if not given) as `category: cents`,
          and logs a `WARNING` `over budget` when the total is above the
          budget. Set up logging to stdout with the format `LEVEL message`.
          Run the three argument lists in the solution: add a 2025-03-05
          `fun` expense of 99.99 euros called `concert`, then `report`, then
          `report --top 1`.
          """,
          "import logging\nimport sys\n"
          'logging.basicConfig(stream=sys.stdout, force=True, level=logging.INFO, format="%(levelname)s %(message)s")\n'
          "def run(argv):\n"
          "    args = parser.parse_args(argv)\n"
          '    if args.command == "add":\n'
          "        add_expense(conn, args.day, args.category, round(args.euros * 100), args.note)\n"
          '        logging.info("added %s", args.note)\n'
          "    else:\n"
          "        limit = args.top or top\n"
          '        total = conn.execute("SELECT SUM(cents) FROM expenses").fetchone()[0]\n'
          '        print("total:", total)\n'
          '        rows = conn.execute("SELECT category, SUM(cents) AS spent FROM expenses "\n'
          '                            "GROUP BY category ORDER BY spent DESC, category LIMIT ?", (limit,))\n'
          "        for row in rows:\n"
          '            print(row["category"] + ": " + str(row["spent"]))\n'
          "        if total > budget_cents:\n"
          '            logging.warning("over budget")\n'
          'run(["add", "2025-03-05", "fun", "99.99", "concert"])\n'
          'run(["report"])\n'
          'run(["report", "--top", "1"])'),
         ("""
          Export and verify with a child process. Write all expenses (ordered
          by id) as CSV lines `day,category,cents` into `expenses.csv`
          inside `workdir`, put that file into a zip called `export.zip` in
          the same folder, and then run a child Python process (the same
          interpreter) with `-c` code that opens the zip, counts the lines
          of `expenses.csv` and prints `lines in zip: N`. Pass the zip's path
          as a separate argument, never inside a shell string. Print what the
          child printed, then clean up the temporary folder.
          """,
          "import subprocess\nimport zipfile\n"
          'csv_path = Path(workdir.name, "expenses.csv")\n'
          'lines = [f"{row[\'day\']},{row[\'category\']},{row[\'cents\']}"\n'
          '         for row in conn.execute("SELECT * FROM expenses ORDER BY id")]\n'
          'csv_path.write_text("\\n".join(lines) + "\\n")\n'
          'zip_path = Path(workdir.name, "export.zip")\n'
          'with zipfile.ZipFile(zip_path, "w") as archive:\n'
          '    archive.write(csv_path, arcname="expenses.csv")\n'
          'child_code = ("import sys, zipfile\\n"\n'
          '              "with zipfile.ZipFile(sys.argv[1]) as z:\\n"\n'
          '              "    print(\'lines in zip:\', len(z.read(\'expenses.csv\').decode().splitlines()))")\n'
          "result = subprocess.run([sys.executable, \"-c\", child_code, str(zip_path)],\n"
          "                        capture_output=True, text=True, check=True)\n"
          "print(result.stdout.strip())\n"
          "workdir.cleanup()"),
     ])

nb.build()
