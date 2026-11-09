import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB13", title="Modules, Files, JSON & CSV", intro="""
    Code that lives in several files, and data that lives on disk: `import`
    in all its styles, your own modules and packages, `pathlib`, reading and
    writing text, JSON and CSV, a short tour of `configparser`, XML and
    `pickle`. Every exercise creates its files inside a throw-away
    `tempfile.TemporaryDirectory()`, so your real files are never touched.
    The folder is already set up for you in the starting code.
""")

TMP = "import tempfile\nfrom pathlib import Path\n\ntmp = tempfile.TemporaryDirectory()\nfolder = Path(tmp.name)\n"

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", """
    Save the shopping list to `shopping.txt` inside `folder`, one item per
    line. Read it back with `read_text()` and print it.
""",
     given=TMP + '\nitems = ["eggs", "milk", "bread"]',
     solution='path = folder / "shopping.txt"\n'
              'path.write_text("\\n".join(items) + "\\n")\n'
              'print(path.read_text(), end="")')

nb.q("Output-match", """
    For the path below, print three labelled lines: its file name, its name
    without the extension (the stem) and its extension (the suffix).
""",
     given='from pathlib import Path\n\nreport = Path("reports/2024/sales_final.csv")',
     solution='print("name:", report.name)\nprint("stem:", report.stem)\nprint("suffix:", report.suffix)')

nb.q("Puzzle", """
    A scoreboard with integer keys is saved as JSON text and loaded back.
    Print the keys of the loaded dictionary as a list, then print whether the
    loaded dictionary equals the original.
""",
     given='import json\n\nscores = {1: "Ada", 2: "Grace", 3: "Alan"}',
     solution="back = json.loads(json.dumps(scores))\nprint(list(back))\nprint(back == scores)")

nb.q("Build", """
    `log.txt` already holds one line. Add the lines `second` and `third` to
    the end without losing the first one, then print how many lines the file
    has now.
""",
     given=TMP + '\npath = folder / "log.txt"\npath.write_text("first\\n")',
     solution='with open(path, "a", encoding="utf-8") as f:\n'
              '    f.write("second\\nthird\\n")\n'
              'print(len(path.read_text().splitlines()))')

nb.q("Output-match", """
    Import `math` under the short name `m` and print the floor of 7.8. Then
    import `ceil` and `pi` straight from `math` and print the ceiling of 7.2
    and `pi` rounded to 3 decimal places, all on separate lines.
""",
     solution="import math as m\nfrom math import ceil, pi\n"
              "print(m.floor(7.8))\nprint(ceil(7.2))\nprint(round(pi, 3))")

# ------------------------------------------------------------ Combine
nb.q("Real-life", """
    `poem.txt` is a tiny poem. Open it with `with`, then print how many lines
    and how many words it has, labelled like the expected output.
""",
     given=TMP + '\npath = folder / "poem.txt"\n'
            'path.write_text("Roses are red\\nViolets are blue\\nPython is neat\\nAnd so are you\\n")',
     solution='with open(path, encoding="utf-8") as f:\n'
              '    text = f.read()\n'
              'print("Lines:", len(text.splitlines()))\n'
              'print("Words:", len(text.split()))')

nb.q("Puzzle", """
    The relative path `"*.txt"` only means something relative to the current
    folder. Remember where you are, move into `folder` with `os.chdir`, and
    use `glob` to print every `.txt` file there, smallest first, with its size
    in bytes. Then move back to where you started.
""",
     given='import glob\nimport os\n' + TMP +
           '\n(folder / "a.txt").write_text("hello world, this is long")\n'
           '(folder / "b.txt").write_text("hi")\n'
           '(folder / "c.log").write_text("not a text file")\n'
           '(folder / "d.txt").write_text("medium size")',
     solution="start = os.getcwd()\nos.chdir(folder)\n"
              'for name in sorted(glob.glob("*.txt"), key=os.path.getsize):\n'
              "    print(name, os.path.getsize(name))\n"
              "os.chdir(start)")

nb.q("Output-match", """
    Write the rows below to `prices.csv` with `csv.writer` (header first),
    then print the file's text. Note the name that contains a comma.
""",
     given='import csv\n' + TMP +
           '\nrows = [["name", "price"], ["Mug", 4.5], ["Plate, large", 7.25]]',
     solution='path = folder / "prices.csv"\n'
              'with open(path, "w", newline="", encoding="utf-8") as f:\n'
              '    csv.writer(f).writerows(rows)\n'
              'print(path.read_text(), end="")')

nb.q("Real-life", """
    `grades.csv` has a header row. Read it with `csv.DictReader`, print each
    student as `name: score` and then the average score rounded to 1 decimal
    place.
""",
     given='import csv\n' + TMP +
           '\npath = folder / "grades.csv"\n'
           'path.write_text("name,score\\nAda,92\\nGrace,85\\nAlan,78\\nLinus,64\\n")',
     solution='total = 0\ncount = 0\n'
              'with open(path, newline="", encoding="utf-8") as f:\n'
              '    for row in csv.DictReader(f):\n'
              '        print(row["name"] + ":", row["score"])\n'
              '        total += int(row["score"])\n'
              '        count += 1\n'
              'print("Average:", round(total / count, 1))')

nb.q("Build", """
    Save `settings` into `settings.json` with `json.dump`: indented by 2
    spaces and with the keys sorted. Then print the file's text.
""",
     given='import json\n' + TMP +
           '\nsettings = {"volume": 7, "theme": "dark", "autosave": True, "language": "en"}',
     solution='path = folder / "settings.json"\n'
              'with open(path, "w", encoding="utf-8") as f:\n'
              '    json.dump(settings, f, indent=2, sort_keys=True)\n'
              'print(path.read_text())')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A small package lives in `folder / "toolkit"`: an `__init__.py` that
    imports `shout` from a sibling module with a **relative import**, and a
    `text.py` that defines `shout(word)` (upper case plus `!`). Create both
    files from your code, make `folder` importable, import the package and
    print `shout("hey")`. Also print whether `"shout"` is in `dir(toolkit)`.
""",
     given='import sys\n' + TMP,
     solution='package = folder / "toolkit"\npackage.mkdir()\n'
              '(package / "text.py").write_text("def shout(word):\\n    return word.upper() + \'!\'\\n")\n'
              '(package / "__init__.py").write_text("from .text import shout\\n")\n'
              'sys.path.insert(0, str(folder))\n'
              'import toolkit\n'
              'print(toolkit.shout("hey"))\n'
              'print("shout" in dir(toolkit))')

nb.q("Real-life", """
    A report is saved once. Open `report.txt` for exclusive creation (mode
    `"x"`) and write `v1` to it. Do that twice in a loop: the second time the
    file exists, so catch the error and print `already exists`. Then try to
    read `missing.txt` and print `no such file` when it isn't there.
""",
     given=TMP,
     solution='path = folder / "report.txt"\n'
              'for attempt in range(2):\n'
              '    try:\n'
              '        with open(path, "x", encoding="utf-8") as f:\n'
              '            f.write("v1")\n'
              '        print("created")\n'
              '    except FileExistsError:\n'
              '        print("already exists")\n'
              'try:\n'
              '    open(folder / "missing.txt").read()\n'
              'except FileNotFoundError:\n'
              '    print("no such file")')

nb.q("Puzzle", """
    The module `shop.py` below is written into `folder`. Import everything
    from it with `from shop import *`, print `vat(100)`, then try to print
    `_margin` and catch the `NameError`, printing `private names stay home`.
    Finally `import shop` and print `shop.__name__`. Importing must not run
    the module's `if __name__ == "__main__":` part.
""",
     given='import sys\n' + TMP + '''
shop_code = """
def vat(price):
    return round(price * 1.2, 2)

_margin = 0.35

if __name__ == "__main__":
    print("running shop.py directly")
"""''',
     solution='(folder / "shop.py").write_text(shop_code)\n'
              'sys.path.insert(0, str(folder))\n'
              'from shop import *\n'
              'print(vat(100))\n'
              'try:\n'
              '    print(_margin)\n'
              'except NameError:\n'
              '    print("private names stay home")\n'
              'import shop\n'
              'print(shop.__name__)')

nb.q("Real-life", """
    Tidy a messy downloads folder: for every file in `folder`, make a
    sub-folder named after its extension (without the dot, e.g. `pdf`) and
    move the file into it with `rename`. Then print each sub-folder in
    alphabetical order followed by the sorted names inside it, like the
    expected output.
""",
     given=TMP + '\nfor name in ["cv.pdf", "notes.txt", "photo.jpg", "todo.txt", "book.pdf", "pic.jpg", "ideas.txt"]:\n'
                 '    (folder / name).write_text("x")',
     solution='for item in list(folder.iterdir()):\n'
              '    target = folder / item.suffix[1:]\n'
              '    target.mkdir(exist_ok=True)\n'
              '    item.rename(target / item.name)\n'
              'for sub in sorted(folder.iterdir()):\n'
              '    print(sub.name + ":", sorted(p.name for p in sub.iterdir()))')

nb.q("Real-life", """
    `access.log` has one request per line: date, method, path and status code,
    separated by spaces, plus a blank line somewhere. Read the file line by
    line, skip the blank lines, and count how often each status code appears.
    Print the codes in sorted order as `code: count`.
""",
     given=TMP + '\npath = folder / "access.log"\n'
            'path.write_text("2024-03-01 GET /home 200\\n2024-03-01 GET /about 200\\n'
            '2024-03-01 POST /login 302\\n\\n2024-03-02 GET /missing 404\\n'
            '2024-03-02 GET /home 200\\n2024-03-02 GET /secret 403\\n2024-03-02 GET /gone 404\\n")',
     solution='counts = {}\n'
              'with open(path, encoding="utf-8") as f:\n'
              '    for line in f:\n'
              '        if not line.strip():\n'
              '            continue\n'
              '        code = line.split()[3]\n'
              '        counts[code] = counts.get(code, 0) + 1\n'
              'for code in sorted(counts):\n'
              '    print(code + ":", counts[code])')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Build", """
    `stock.csv` lists products with a name, a price and a quantity. Read it
    with `DictReader`, turn price into a `float` and quantity into an `int`,
    and save the list of records to `stock.json` (indented by 2). Load the
    JSON back and print the number of records and the total stock value
    (sum of price times quantity), rounded to 2 decimal places.
""",
     given='import csv\nimport json\n' + TMP +
           '\n(folder / "stock.csv").write_text(\n'
           '    "name,price,quantity\\nPen,1.20,100\\nNotebook,3.50,40\\nBackpack,24.99,6\\nRuler,0.80,55\\n")',
     solution='records = []\n'
              'with open(folder / "stock.csv", newline="", encoding="utf-8") as f:\n'
              '    for row in csv.DictReader(f):\n'
              '        records.append({"name": row["name"], "price": float(row["price"]),\n'
              '                        "quantity": int(row["quantity"])})\n'
              'with open(folder / "stock.json", "w", encoding="utf-8") as f:\n'
              '    json.dump(records, f, indent=2)\n'
              'with open(folder / "stock.json", encoding="utf-8") as f:\n'
              '    loaded = json.load(f)\n'
              'value = sum(r["price"] * r["quantity"] for r in loaded)\n'
              'print("Records:", len(loaded))\n'
              'print("Stock value:", round(value, 2))')

nb.q("Puzzle", """
    Parse the INI text with `configparser`. Print the section names, then the
    database host, the port **as an integer plus 1**, and the `debug` flag as
    a real boolean. For `timeout`, which is missing from the file, use a
    fallback of 30. Print each result labelled like the expected output.
""",
     given='''import configparser

ini_text = """
[database]
host = db.example.com
port = 5432

[app]
debug = yes
name = Inventory
"""''',
     solution="config = configparser.ConfigParser()\n"
              "config.read_string(ini_text)\n"
              'print("Sections:", config.sections())\n'
              'print("Host:", config["database"]["host"])\n'
              'print("Next port:", config.getint("database", "port") + 1)\n'
              'print("Debug:", config.getboolean("app", "debug"))\n'
              'print("Timeout:", config.getint("app", "timeout", fallback=30))')

nb.q("Real-life", """
    A shop exports its books as XML. Parse the text with
    `xml.etree.ElementTree`, print each book as `title (year) - price`, taking
    the year from the `year` **attribute**, and then print the total price of
    all books rounded to 2 decimal places.
""",
     given='''import xml.etree.ElementTree as ET

xml_text = """
<library>
  <book year="1999"><title>Pragmatic Python</title><price>29.90</price></book>
  <book year="2015"><title>Data in Depth</title><price>41.50</price></book>
  <book year="2021"><title>Tiny Scripts</title><price>12.00</price></book>
</library>
"""''',
     solution="root = ET.fromstring(xml_text)\n"
              "total = 0\n"
              'for book in root.findall("book"):\n'
              '    title = book.find("title").text\n'
              '    price = float(book.find("price").text)\n'
              '    print(title, "(" + book.get("year") + ") -", price)\n'
              "    total += price\n"
              'print("Total:", round(total, 2))')

nb.q("Puzzle", """
    Push the same `save_game` dictionary through `json` and through `pickle`
    (`dumps` then `loads`), and print `True` or `False` for whether each copy
    equals the original. Then store the dictionary in a `shelve` file called
    `saves` inside `folder` under the key `"slot1"`, close it, open it again
    and print the stored level.
""",
     given='import json\nimport pickle\nimport shelve\n' + TMP +
           '\nsave_game = {"player": "Ada", "position": (4, 7), "level": 3}',
     solution='print("json:", json.loads(json.dumps(save_game)) == save_game)\n'
              'print("pickle:", pickle.loads(pickle.dumps(save_game)) == save_game)\n'
              'with shelve.open(str(folder / "saves")) as db:\n'
              '    db["slot1"] = save_game\n'
              'with shelve.open(str(folder / "saves")) as db:\n'
              '    print("level:", db["slot1"]["level"])')

# ------------------------------------------------------------ Q20 story project
nb.project("Contacts Manager", story="""
    Your small business keeps its contacts in a JSON file. A colleague sent a
    CSV of new contacts, but it is messy: stray spaces, odd capitals, blanks
    and people who are already in your list. Build the importer step by step;
    each step uses the variables from the step before.
""",
     given=r'''import csv
import json
import tempfile
from pathlib import Path

tmp = tempfile.TemporaryDirectory()
folder = Path(tmp.name)

existing = [
    {"name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0101"},
    {"name": "Alan Turing", "email": "alan@example.com", "phone": "555-0102"},
]
(folder / "contacts.json").write_text(json.dumps(existing))
(folder / "new_contacts.csv").write_text(
    "name,email,phone\n"
    "Grace Hopper,grace@example.com,555-0103\n"
    "ada lovelace,ADA@EXAMPLE.COM,555-0199\n"
    "Linus Torvalds,linus@example.com,\n"
    "  Alan Turing ,alan@example.com,555-0102\n"
    "margaret hamilton, Margaret@Example.com ,555-0104\n"
)''',
     steps=[
         ("Load `contacts.json` into a list called `contacts` with `json.load`. "
          "Print how many contacts there are, then each name on its own line.",
          'with open(folder / "contacts.json", encoding="utf-8") as f:\n'
          "    contacts = json.load(f)\n"
          'print("Contacts:", len(contacts))\n'
          "for contact in contacts:\n"
          '    print(contact["name"])'),
         ("Read `new_contacts.csv` with `DictReader` into a list `new_rows`. Clean every row: "
          "the name is stripped and title-cased, the email is stripped and lower-case, and a "
          "blank phone becomes `unknown`. Print the cleaned rows one per line as "
          "`name | email | phone`.",
          "new_rows = []\n"
          'with open(folder / "new_contacts.csv", newline="", encoding="utf-8") as f:\n'
          "    for row in csv.DictReader(f):\n"
          "        new_rows.append({\n"
          '            "name": row["name"].strip().title(),\n'
          '            "email": row["email"].strip().lower(),\n'
          '            "phone": row["phone"].strip() or "unknown",\n'
          "        })\n"
          "for row in new_rows:\n"
          '    print(row["name"], "|", row["email"], "|", row["phone"])'),
         ("Merge: two contacts are the same person when their emails match. Add each new row "
          "whose email is not known yet to `contacts`, and skip the others. Print the names "
          "you added, then how many duplicates you skipped.",
          'known = {c["email"] for c in contacts}\n'
          "added = []\n"
          "skipped = 0\n"
          "for row in new_rows:\n"
          '    if row["email"] in known:\n'
          "        skipped += 1\n"
          "    else:\n"
          "        contacts.append(row)\n"
          '        known.add(row["email"])\n'
          '        added.append(row["name"])\n'
          'print("Added:", added)\n'
          'print("Skipped duplicates:", skipped)'),
         ("Sort `contacts` by name and save them back to `contacts.json`, indented by 2. "
          "Load the file again and print the number of contacts and the first and last name.",
          'contacts.sort(key=lambda c: c["name"])\n'
          'with open(folder / "contacts.json", "w", encoding="utf-8") as f:\n'
          "    json.dump(contacts, f, indent=2)\n"
          'with open(folder / "contacts.json", encoding="utf-8") as f:\n'
          "    saved = json.load(f)\n"
          'print("Saved:", len(saved))\n'
          'print("First:", saved[0]["name"])\n'
          'print("Last:", saved[-1]["name"])'),
         ("Export a report to `report.csv` with `DictWriter` (columns name, email, phone, "
          "header first), using only the contacts whose phone is not `unknown`. Print the "
          "report's text.",
          'with open(folder / "report.csv", "w", newline="", encoding="utf-8") as f:\n'
          '    writer = csv.DictWriter(f, fieldnames=["name", "email", "phone"])\n'
          "    writer.writeheader()\n"
          "    for contact in saved:\n"
          '        if contact["phone"] != "unknown":\n'
          "            writer.writerow(contact)\n"
          'print((folder / "report.csv").read_text(), end="")'),
         ("Finish with a folder listing: print the names of all files in `folder` in "
          "alphabetical order, each with its size in bytes, then clean up with "
          "`tmp.cleanup()`.",
          "for path in sorted(folder.iterdir()):\n"
          "    print(path.name, path.stat().st_size)\n"
          "tmp.cleanup()"),
     ])

nb.build()
