import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB08", title="Beginner Capstone", intro="""
    The beginner finale. You'll build a complete little program, a **bank
    simulator**, in six milestones: formatting money, deposits and withdrawals,
    transfers, processing a whole day of transactions, printing account
    statements, and a final report. Every milestone uses the functions you wrote
    in the ones before, and everything from NB00 to NB07 is fair game.
""")

nb.project("Byte Bank", story="""
    You've been hired as the first developer at *Byte Bank*, a tiny bank with
    three customers. Each night a file of the day's requests arrives, and so far
    a clerk has processed it by hand. Some requests are valid, some are not:
    overdrafts, unknown customers, nonsense amounts. Build the program that
    processes the file and prints each customer's statement. Run the starting
    data first, then work through the milestones in order.
""",
     given='''accounts = {"Ana": 500.0, "Bo": 120.0, "Cy": 0.0}

# (kind, account, amount as text)  or  ("transfer", from, to, amount as text)
transactions = [
    ("deposit", "Ana", "200"),
    ("withdraw", "Bo", "150"),
    ("transfer", "Ana", "Cy", "75.50"),
    ("withdraw", "Cy", "abc"),
    ("deposit", "Dee", "50"),
    ("transfer", "Bo", "Ana", "20"),
    ("deposit", "Bo", "-5"),
    ("withdraw", "Ana", "300"),
]''',
     steps=[
         ("Write `money(amount)` that returns a number as text with a dollar sign, "
          "a thousands separator and 2 decimals. Then write `show_balances(accounts)` "
          "that prints one line per customer in alphabetical order, with the name "
          "padded to 6 characters and the money right-aligned in 12 characters. "
          "Call it on the starting accounts.",
          'def money(amount):\n'
          '    return f"${amount:,.2f}"\n'
          '\n'
          'def show_balances(accounts):\n'
          '    for name in sorted(accounts):\n'
          '        print(f"{name:<6}{money(accounts[name]):>12}")\n'
          '\n'
          'show_balances(accounts)'),
         ("Write `deposit(accounts, name, amount)` and `withdraw(accounts, name, amount)`. "
          "Each changes the balance and returns `True`, or changes nothing and returns "
          "`False` when the customer doesn't exist, the amount isn't positive, or (for a "
          "withdrawal) the balance is too small. Test on a separate dict "
          '`trial = {"Ana": 100.0, "Bo": 50.0}`: deposit 25 to Ana, withdraw 80 from Bo, '
          "withdraw 30 from Bo, and deposit 10 to \"Zed\". Print each result, then the "
          "trial balances with `show_balances`.",
          'def deposit(accounts, name, amount):\n'
          '    if name not in accounts or amount <= 0:\n'
          '        return False\n'
          '    accounts[name] += amount\n'
          '    return True\n'
          '\n'
          'def withdraw(accounts, name, amount):\n'
          '    if name not in accounts or amount <= 0 or amount > accounts[name]:\n'
          '        return False\n'
          '    accounts[name] -= amount\n'
          '    return True\n'
          '\n'
          'trial = {"Ana": 100.0, "Bo": 50.0}\n'
          'print(deposit(trial, "Ana", 25))\n'
          'print(withdraw(trial, "Bo", 80))\n'
          'print(withdraw(trial, "Bo", 30))\n'
          'print(deposit(trial, "Zed", 10))\n'
          'show_balances(trial)'),
         ("Write `transfer(accounts, source, target, amount)` using your two functions. "
          "It must check that the target exists first, then withdraw from the source, "
          "and only if that worked deposit into the target. It returns `True` or `False` "
          "like the others, and money must never vanish on a failed transfer. Test it "
          "on `trial` with a valid transfer of 40 from Ana to Bo, one of 500 from Bo to "
          "Ana, and one of 5 from Ana to \"Zed\". Print each result and the balances.",
          'def transfer(accounts, source, target, amount):\n'
          '    if target not in accounts:\n'
          '        return False\n'
          '    if withdraw(accounts, source, amount):\n'
          '        deposit(accounts, target, amount)\n'
          '        return True\n'
          '    return False\n'
          '\n'
          'print(transfer(trial, "Ana", "Bo", 40))\n'
          'print(transfer(trial, "Bo", "Ana", 500))\n'
          'print(transfer(trial, "Ana", "Zed", 5))\n'
          'show_balances(trial)'),
         ("Write `process(accounts, transactions)`. For each transaction (numbered from 1) "
          "convert the amount text with `float()`; if that raises `ValueError`, the status "
          "is `\"bad amount\"`. Otherwise use `if`/`elif` on the kind to call your "
          "functions, giving status `\"ok\"` or `\"rejected\"`. Append a tuple "
          "`(number, kind, name, other, amount, status)` to a log list, where `other` is "
          "the target for transfers and an empty string otherwise (use 0.0 for a bad "
          "amount), and return the log. Save `opening = accounts.copy()`, run `process` "
          "on the real accounts, then print one line per log entry showing its number, "
          "kind, name and status, and the final balances.",
          'def process(accounts, transactions):\n'
          '    log = []\n'
          '    number = 0\n'
          '    for tx in transactions:\n'
          '        number += 1\n'
          '        kind = tx[0]\n'
          '        name = tx[1]\n'
          '        other = ""\n'
          '        text = tx[2]\n'
          '        if kind == "transfer":\n'
          '            other = tx[2]\n'
          '            text = tx[3]\n'
          '        try:\n'
          '            amount = float(text)\n'
          '        except ValueError:\n'
          '            log.append((number, kind, name, other, 0.0, "bad amount"))\n'
          '            continue\n'
          '        if kind == "deposit":\n'
          '            done = deposit(accounts, name, amount)\n'
          '        elif kind == "withdraw":\n'
          '            done = withdraw(accounts, name, amount)\n'
          '        else:\n'
          '            done = transfer(accounts, name, other, amount)\n'
          '        if done:\n'
          '            status = "ok"\n'
          '        else:\n'
          '            status = "rejected"\n'
          '        log.append((number, kind, name, other, amount, status))\n'
          '    return log\n'
          '\n'
          'opening = accounts.copy()\n'
          'log = process(accounts, transactions)\n'
          'for entry in log:\n'
          '    print(f"#{entry[0]} {entry[1]} {entry[2]}: {entry[5]}")\n'
          'show_balances(accounts)'),
         ("Write `statement(name, opening, log)` that prints a statement for one customer. "
          "First a header line with the name and opening balance. Then, for each log entry "
          "with status `\"ok\"` that involves the customer, one line with the transaction "
          "number, the kind, the signed amount (`+` when money comes in, `-` when it goes "
          "out, 2 decimals) and the running balance. A transfer counts as out for the "
          "sender and in for the receiver. Print the statement for \"Ana\".",
          'def statement(name, opening, log):\n'
          '    balance = opening[name]\n'
          '    print(f"--- {name} (opening {money(balance)}) ---")\n'
          '    for number, kind, who, other, amount, status in log:\n'
          '        if status != "ok":\n'
          '            continue\n'
          '        change = 0.0\n'
          '        if kind == "deposit" and who == name:\n'
          '            change = amount\n'
          '        elif kind == "withdraw" and who == name:\n'
          '            change = -amount\n'
          '        elif kind == "transfer" and who == name:\n'
          '            change = -amount\n'
          '        elif kind == "transfer" and other == name:\n'
          '            change = amount\n'
          '        if change != 0.0:\n'
          '            balance += change\n'
          '            print(f"#{number} {kind:<9}{change:>+9.2f}{balance:>10.2f}")\n'
          '\n'
          'statement("Ana", opening, log)'),
         ("Time for the finale. Print a title line, then the statement of every customer in "
          "alphabetical order. After that print how many transactions were rejected or had "
          "a bad amount, followed by a list of their numbers. Finally print the total money "
          "held by the bank using `money`, and the name of the richest customer. "
          "Everything uses the data and functions you've already built.",
          'print("=== BYTE BANK: END OF DAY ===")\n'
          'for name in sorted(opening):\n'
          '    statement(name, opening, log)\n'
          '\n'
          'failed = []\n'
          'for entry in log:\n'
          '    if entry[5] != "ok":\n'
          '        failed.append(entry[0])\n'
          'print("Failed transactions:", len(failed), failed)\n'
          '\n'
          'total = 0.0\n'
          'richest = ""\n'
          'best = -1.0\n'
          'for name in accounts:\n'
          '    total += accounts[name]\n'
          '    if accounts[name] > best:\n'
          '        best = accounts[name]\n'
          '        richest = name\n'
          'print("Total held:", money(total))\n'
          'print("Richest customer:", richest)'),
     ])

nb.build()
