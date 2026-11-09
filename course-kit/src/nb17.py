import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB17", title="Regex", intro="""
    Describing the *shape* of text instead of one exact string: finding,
    checking, extracting and rewriting with the `re` module. Always write
    patterns as raw strings (`r"..."`). Each question gives you the text as a
    variable, so you only write the pattern and the code around it.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "Find every whole number in the sentence and print them as a list of strings.",
     given='sentence = "Order 66 shipped 12 boxes on day 305 to 4 stores"',
     solution="import re\nprint(re.findall(r\"\\d+\", sentence))")

nb.q("Real-life", "A product code must be exactly three capital letters, a dash and four digits. Print `True` or `False` for the code with `re.fullmatch`.",
     given='code = "ABC-1234"',
     solution='import re\nprint(bool(re.fullmatch(r"[A-Z]{3}-\\d{4}", code)))')

nb.q("Output-match", "Print the first word of the text that starts with a capital letter, using `re.search` and `.group()`.",
     given='text = "the quick Brown fox jumps over Lazy dogs"',
     solution='import re\nprint(re.search(r"[A-Z]\\w*", text).group())')

nb.q("Puzzle", "Check whether `line` **starts with** `ERROR` using `re.match`, then check whether it **contains** `ERROR` anywhere using `re.search`. Print both results as `True`/`False`.",
     given='line = "2024-05-01 ERROR disk full"',
     solution='import re\nprint(bool(re.match(r"ERROR", line)))\nprint(bool(re.search(r"ERROR", line)))')

nb.q("Real-life", "Replace every run of whitespace (spaces, tabs, newlines) in the messy text with a single space and print the result.",
     given='messy = "too   many\\t\\tspaces\\n\\nhere"',
     solution='import re\nprint(re.sub(r"\\s+", " ", messy))')

# ------------------------------------------------------------ Combine
nb.q("Real-life", "Find all the dates written like `2024-05-17` in the text and print the list.",
     given='notes = "Start 2024-05-17, review 2024-06-03, launch on 2024-07-01 (maybe 2024-7-1)."',
     solution='import re\nprint(re.findall(r"\\d{4}-\\d{2}-\\d{2}", notes))')

nb.q("Real-life", """
    Pull the year, month and day out of the date with **groups** and print
    them on one line as three integers.
""",
     given='stamp = "Released on 2023-11-09 at noon"',
     solution='import re\nm = re.search(r"(\\d{4})-(\\d{2})-(\\d{2})", stamp)\n'
              'year, month, day = int(m.group(1)), int(m.group(2)), int(m.group(3))\nprint(year, month, day)')

nb.q("Puzzle", """
    Find all prices like `$12.50` (the cents part is optional) and print the
    full text of each match, with the `$`, as a list. The pattern needs
    brackets around the optional part, but `findall` must still return whole
    matches.
""",
     given='menu = "Soup $4.50, steak $18.00, tea $2.25"',
     solution='import re\nprint(re.findall(r"\\$\\d+(?:\\.\\d{2})?", menu))')

nb.q("Build", """
    Words in the text may be separated by commas, semicolons or any amount of
    spaces. Split it into a clean list of words with `re.split`.
""",
     given='tags = "python,regex;  text   tools ,fun"',
     solution='import re\nprint(re.split(r"[,; ]+", tags))')

nb.q("Real-life", """
    Count how many times the word `the` appears in the text, ignoring case and
    only as a whole word (`there` and `other` must not count).
""",
     given='text = "The cat saw the dog. Then the other cat left there."',
     solution='import re\nprint(len(re.findall(r"\\bthe\\b", text, re.IGNORECASE)))')

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    The HTML has two bold tags. Print the text inside each `<b>...</b>` as a
    list. A greedy `.*` would swallow too much, so make it lazy.
""",
     given='html = "Buy <b>milk</b>, then <b>eggs</b> and bread"',
     solution='import re\nprint(re.findall(r"<b>(.*?)</b>", html))')

nb.q("Real-life", """
    Parse each access-log line with **named groups** (`ip`, `method`, `path`,
    `status`) and print one line per request like `GET /home -> 200 from
    10.0.0.5`.
""",
     given='logs = [\n    \'10.0.0.5 - "GET /home" 200\',\n    \'10.0.0.9 - "POST /login" 401\',\n    \'10.0.0.5 - "GET /missing" 404\',\n]',
     solution='import re\npattern = r\'(?P<ip>[\\d.]+) - "(?P<method>[A-Z]+) (?P<path>\\S+)" (?P<status>\\d{3})\'\n'
              'for line in logs:\n    m = re.search(pattern, line)\n'
              '    print(m["method"], m["path"], "->", m["status"], "from", m["ip"])')

nb.q("Real-life", """
    Convert the camelCase names to snake_case with `re.sub` and a
    backreference: put an underscore before each capital letter and make
    everything lower case. Print each converted name.
""",
     given='names = ["userName", "totalPriceEur", "id"]',
     solution='import re\nfor name in names:\n    snake = re.sub(r"([A-Z])", r"_\\1", name).lower()\n    print(snake)')

nb.q("Build", """
    Swap the date format from `DD/MM/YYYY` to `YYYY-MM-DD` in every date of the
    text, using groups and backreferences in `re.sub`.
""",
     given='text = "Due 05/11/2024, paid 17/12/2024."',
     solution='import re\nprint(re.sub(r"(\\d{2})/(\\d{2})/(\\d{4})", r"\\3-\\2-\\1", text))')

nb.q("Real-life", """
    Use a **compiled** pattern (`re.compile`) for UK-style phone numbers that
    look like `07123 456789` (5 digits, a space, 6 digits). Print each entry
    with `valid` or `invalid`. The check must cover the *whole* entry.
""",
     given='entries = ["07123 456789", "07123456789", "0712 3456789", "07123 4567890"]',
     solution='import re\nphone = re.compile(r"\\d{5} \\d{6}")\n'
              'for entry in entries:\n    ok = phone.fullmatch(entry)\n    print(entry, "valid" if ok else "invalid")')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Puzzle", """
    Use a **verbose** regex (`re.VERBOSE`, with spaces and `#` comments inside
    the pattern) to parse a time like `7:05pm` into hour, minute and am/pm
    named groups. Print the three values for each time.
""",
     given='times = ["7:05pm", "12:30am", "9:45PM"]',
     solution='import re\npattern = re.compile(r"""\n    (?P<hour>\\d{1,2})   # one or two digits\n    :\n    (?P<minute>\\d{2})\n    (?P<ampm>am|pm)\n""", re.VERBOSE | re.IGNORECASE)\n'
              'for t in times:\n    m = pattern.fullmatch(t)\n    print(m["hour"], m["minute"], m["ampm"].lower())')

nb.q("Puzzle", """
    Password rules with **lookaheads**: at least 8 characters, at least one
    digit, at least one capital letter and at least one lower-case letter. One
    pattern, `fullmatch`. Print each password with `ok` or `weak`.
""",
     given='passwords = ["Sunshine99", "sunshine99", "SUNSHINE99", "Short1a", "NoDigitsHere"]',
     solution='import re\nrule = re.compile(r"(?=.*\\d)(?=.*[A-Z])(?=.*[a-z]).{8,}")\n'
              'for pw in passwords:\n    print(pw, "ok" if rule.fullmatch(pw) else "weak")')

nb.q("Puzzle", """
    Format the big numbers with thousands separators using a **lookahead** in
    `re.sub`: insert a comma before every group of three digits that is
    followed only by more digit triples. Print each result.
""",
     given='numbers = ["1234", "1234567", "999", "1000000000"]',
     solution='import re\nfor n in numbers:\n    print(re.sub(r"(?<=\\d)(?=(?:\\d{3})+$)", ",", n))')

nb.q("Build", """
    Tokenise the arithmetic expression into numbers (with optional decimals),
    operators `+ - * /` and brackets. Use one `findall` with alternation,
    print the token list, then print how many of the tokens are numbers.
""",
     given='expr = "3.5*(12 + 4)-7/2"',
     solution='import re\ntokens = re.findall(r"\\d+(?:\\.\\d+)?|[-+*/()]", expr)\nprint(tokens)\n'
              'numbers = [t for t in tokens if t[0].isdigit()]\nprint(len(numbers))')

# ------------------------------------------------------------ Q20 story project
nb.project("Log Redactor", story="""
    Support wants to share server logs with a contractor, but they contain
    **emails, IP addresses and card numbers**. You'll find them, count them
    and mask them. Each step builds on the variables of the step before.
""",
     given='log_lines = [\n'
           '    "2024-05-01 10:02 login ok user=ada@example.com ip=192.168.1.20",\n'
           '    "2024-05-01 10:05 payment card=4111-1111-1111-1111 by bob.smith@mail.org",\n'
           '    "2024-05-01 10:09 login failed ip=10.0.0.7 user=carol@example.com",\n'
           '    "2024-05-01 10:15 payment card=5500 0000 0000 0004 ip=172.16.4.9",\n'
           '    "2024-05-01 10:20 cron finished in 12 seconds",\n'
           ']',
     steps=[
         ("Find all email addresses in all the lines (letters, digits, dots, `_`, `%`, `+`, `-` before the `@`; a domain with at least one dot after). Print the sorted list of unique emails.",
          'import re\nemail_re = r"[\\w.%+-]+@[\\w-]+(?:\\.[\\w-]+)+"\n'
          "emails = []\nfor line in log_lines:\n    emails += re.findall(email_re, line)\n"
          "print(sorted(set(emails)))"),
         ("Find the IPv4 addresses (four groups of 1 to 3 digits separated by dots). Print how many lines contain at least one IP address.",
          'ip_re = r"\\b\\d{1,3}(?:\\.\\d{1,3}){3}\\b"\n'
          "lines_with_ip = [line for line in log_lines if re.search(ip_re, line)]\n"
          "print(len(lines_with_ip))"),
         ("Card numbers are four groups of four digits separated by a dash or a space. Build `card_re` with a named group `last4` for the final four digits, and print the `last4` of every card found.",
          'card_re = r"\\d{4}[- ]\\d{4}[- ]\\d{4}[- ](?P<last4>\\d{4})"\n'
          "for line in log_lines:\n    m = re.search(card_re, line)\n    if m:\n        print(m[\"last4\"])"),
         ("Write `redact(line)` that returns the line with every email replaced by `<EMAIL>`, every IP by `<IP>` and every card by `****-****-****-` followed by its last four digits. Print the redacted version of all lines.",
          'def redact(line):\n'
          '    line = re.sub(email_re, "<EMAIL>", line)\n'
          '    line = re.sub(ip_re, "<IP>", line)\n'
          '    line = re.sub(card_re, r"****-****-****-\\g<last4>", line)\n'
          "    return line\n"
          "redacted = [redact(line) for line in log_lines]\nfor line in redacted:\n    print(line)"),
         ("Print a summary: how many emails, IPs and card numbers were masked in total (count the matches in the original lines), and `True` if no original email is left anywhere in `redacted`.",
          "email_count = sum(len(re.findall(email_re, l)) for l in log_lines)\n"
          "ip_count = sum(len(re.findall(ip_re, l)) for l in log_lines)\n"
          "card_count = sum(len(re.findall(card_re, l)) for l in log_lines)\n"
          'print("Emails:", email_count, "IPs:", ip_count, "Cards:", card_count)\n'
          "clean = all(not re.search(email_re, l) for l in redacted)\n"
          'print("Clean:", clean)'),
     ])

nb.build()
