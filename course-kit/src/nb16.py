import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB16", title="Numbers, Bits, Bytes & Unicode", intro="""
    What numbers and text really are underneath: huge integers, floats and
    their rounding quirks, `Decimal` and `Fraction` for exact maths, binary and
    hex, bit flags, bytes versus text, and Unicode. Every question is a small
    task to write. Starting data is given to you as variables.
""")

# ------------------------------------------------------------ Warm-up
nb.q("Real-life", "A lottery machine multiplies 100 twos together. Print `2 ** 100` and, on a second line, how many digits it has.",
     solution="big = 2 ** 100\nprint(big)\nprint(len(str(big)))")

nb.q("Puzzle", "Print whether `0.1 + 0.2 == 0.3`, then print the result of comparing the same two values with `math.isclose`.",
     solution="import math\nprint(0.1 + 0.2 == 0.3)\nprint(math.isclose(0.1 + 0.2, 0.3))")

nb.q("Build", "Print `n` in binary, octal and hexadecimal, one per line, each with its `0b`, `0o` or `0x` prefix.",
     given="n = 202",
     solution="print(bin(n))\nprint(oct(n))\nprint(hex(n))")

nb.q("Output-match", "Turn the three texts into integers using their bases and print the three numbers on one line.",
     given='a = "ff"\nb = "1010"\nc = "777"',
     solution="print(int(a, 16), int(b, 2), int(c, 8))")

nb.q("Puzzle", "A sensor sometimes sends 'not a number'. Print whether `reading == reading`, then whether `math.isnan(reading)`.",
     given='import math\nreading = float("nan")',
     solution="print(reading == reading)\nprint(math.isnan(reading))")

# ------------------------------------------------------------ Combine
nb.q("Puzzle", """
    Build one `Decimal` from the float `0.1` and another from the text `"0.1"`.
    Print each on its own line, then print whether the two are equal.
""",
     given="from decimal import Decimal",
     solution='from_float = Decimal(0.1)\nfrom_text = Decimal("0.1")\nprint(from_float)\nprint(from_text)\nprint(from_float == from_text)')

nb.q("Real-life", """
    A till rounds prices to cents **half up**. For each price text, print the
    price, then the value rounded with `Decimal` and `ROUND_HALF_UP`
    (to `0.01`) on the same line.
""",
     given='from decimal import Decimal, ROUND_HALF_UP\nprices = ["2.675", "1.005", "0.125"]',
     solution="for p in prices:\n"
              '    rounded = Decimal(p).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)\n'
              "    print(p, rounded)")

nb.q("Real-life", """
    A recipe needs 3/4 cup of flour for the dough and 2/3 cup for the topping.
    Print the total as an exact `Fraction`, then the total as a float rounded
    to 3 decimal places.
""",
     given="from fractions import Fraction",
     solution="total = Fraction(3, 4) + Fraction(2, 3)\nprint(total)\nprint(round(float(total), 3))")

nb.q("Build", """
    A file has permission flags `READ = 1`, `WRITE = 2`, `EXEC = 4`. Combine
    READ and WRITE with `|` into `perm`. Print whether each of the three flags
    is set in `perm`, one per line. Then remove WRITE using `& ~` and print
    `perm` again.
""",
     given="READ = 1\nWRITE = 2\nEXEC = 4",
     solution="perm = READ | WRITE\n"
              "print(perm & READ != 0)\nprint(perm & WRITE != 0)\nprint(perm & EXEC != 0)\n"
              "perm = perm & ~WRITE\nprint(perm)")

nb.q("Real-life", """
    For each word, print the word, how many characters it has and how many
    bytes it needs in UTF-8, separated by spaces.
""",
     given='words = ["cafe", "café", "naïve", "日本", "😀"]',
     solution="for w in words:\n    print(w, len(w), len(w.encode(\"utf-8\")))")

# ------------------------------------------------------------ Small real tasks
nb.q("Real-life", """
    A file arrived as raw bytes. Decode it as UTF-8 and print the text. Then
    decode the same bytes as `latin-1` and print that garbled text too. Last,
    print the byte count, and print `"Zoë"` encoded to `ascii` with
    `errors="replace"`.
""",
     given='raw = b"caf\\xc3\\xa9"',
     solution='print(raw.decode("utf-8"))\n'
              'print(raw.decode("latin-1"))\n'
              "print(len(raw))\n"
              'print("Zoë".encode("ascii", errors="replace"))')

nb.q("Real-life", """
    A design tool gives you the colour `hex_colour`. Convert it to three
    integers (red, green, blue) and print them as a tuple. Then build the hex
    text back from the numbers with two lowercase hex digits per channel
    and a leading `#`, and print it.
""",
     given='hex_colour = "#ff8000"',
     solution="red = int(hex_colour[1:3], 16)\n"
              "green = int(hex_colour[3:5], 16)\n"
              "blue = int(hex_colour[5:7], 16)\n"
              "print((red, green, blue))\n"
              'back = "#" + format(red, "02x") + format(green, "02x") + format(blue, "02x")\n'
              "print(back)")

nb.q("Real-life", """
    Two sign-up forms store the name *Café*, but they were typed on different
    keyboards. Print `a == b` and the length of each. Then normalise both with
    `unicodedata.normalize("NFC", ...)` and print whether they are equal now.
""",
     given='import unicodedata\na = "Caf\\u00e9"\nb = "Cafe\\u0301"',
     solution="print(a == b)\n"
              "print(len(a), len(b))\n"
              'na = unicodedata.normalize("NFC", a)\n'
              'nb_ = unicodedata.normalize("NFC", b)\n'
              "print(na == nb_)")

nb.q("Puzzle", """
    For each number print it, how many `1` bits it has (`bit_count()`), and
    `True` if it is a power of two. Use the trick that a power of two ANDed
    with the number just below it gives 0.
""",
     given="numbers = [1, 6, 8, 12, 64, 100]",
     solution="for n in numbers:\n    print(n, n.bit_count(), n & (n - 1) == 0)")

nb.q("Real-life", """
    Pack a sensor record into exactly 7 bytes with `struct`: a device id (2-byte
    unsigned), a temperature (4-byte float) and an alarm flag (1 bool), in
    little-endian order. Print the byte count and the bytes as hex text
    (`.hex()`), then unpack the bytes and print the values back.
""",
     given="import struct\ndevice_id = 7\ntemperature = 21.5\nalarm = True",
     solution='packed = struct.pack("<Hf?", device_id, temperature, alarm)\n'
              "print(len(packed))\n"
              "print(packed.hex())\n"
              'print(struct.unpack("<Hf?", packed))')

# ------------------------------------------------------------ Puzzles & builds
nb.q("Real-life", """
    Build an invoice with `Decimal`. For each `(name, price, qty)`, the line
    total is `price * qty`. VAT is 19% of the line, rounded half up to 2
    decimal places. Print one line per item: name, line total, VAT. After the
    loop print the total of all lines and the total VAT, labelled.
""",
     given='from decimal import Decimal, ROUND_HALF_UP\n'
           'items = [("Notebook", "3.50", 3), ("Pen", "1.15", 7), ("Backpack", "39.99", 1)]\n'
           'vat_rate = Decimal("0.19")',
     solution='cent = Decimal("0.01")\n'
              "total = Decimal(0)\n"
              "total_vat = Decimal(0)\n"
              "for name, price, qty in items:\n"
              "    line = Decimal(price) * qty\n"
              "    vat = (line * vat_rate).quantize(cent, rounding=ROUND_HALF_UP)\n"
              "    total += line\n"
              "    total_vat += vat\n"
              "    print(name, line, vat)\n"
              'print("Total:", total)\n'
              'print("Total VAT:", total_vat)')

nb.q("Puzzle", """
    A router checks whether each address is inside the network `10.0.4.0/22`
    (prefix of 22 bits). Write `to_int(ip)` that turns a dotted address into
    one integer using shifts (`<<`) and `|`. Build the mask as 22 one-bits
    followed by 10 zero-bits, and call an address inside when
    `to_int(ip) & mask` equals the network address as an integer. Print each
    address and `True` or `False`.
""",
     given='network = "10.0.4.0"\nprefix = 22\naddresses = ["10.0.4.1", "10.0.7.255", "10.0.8.1", "10.1.4.9"]',
     solution="def to_int(ip):\n"
              "    result = 0\n"
              '    for part in ip.split("."):\n'
              "        result = (result << 8) | int(part)\n"
              "    return result\n"
              "\n"
              "mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF\n"
              "net = to_int(network)\n"
              "for ip in addresses:\n"
              "    print(ip, to_int(ip) & mask == net)")

nb.q("Puzzle", """
    A message sits in a `bytearray`. Change the first byte so the message
    starts with a lowercase `h`, using the number `ord("h")` (bytes are
    integers), then append the byte for `!`. Compute a checksum by XOR-ing
    (`^`) all the bytes together. Print the decoded message, its length and
    the checksum. Last, print the message decoded again after reversing the
    bytearray with `data[::-1]`.
""",
     given='data = bytearray(b"HELLO WORLD")',
     solution='data[0] = ord("h")\n'
              'data.append(ord("!"))\n'
              "checksum = 0\n"
              "for b in data:\n"
              "    checksum ^= b\n"
              "print(data.decode())\n"
              "print(len(data))\n"
              "print(checksum)\n"
              "print(data[::-1].decode())")

nb.q("Build", """
    For each character of `text`, print one line with the character, its code
    point as `U+` followed by four upper-case hex digits, its official Unicode
    name (`unicodedata.name`) and its UTF-8 byte count. Then print `title`
    with all accents removed: normalise to `"NFD"` and keep only the
    characters that are not combining marks (`unicodedata.combining(ch) == 0`).
""",
     given='import unicodedata\ntext = "é世😀"\ntitle = "Crème Brûlée"',
     solution="for ch in text:\n"
              '    code_point = "U+" + format(ord(ch), "04X")\n'
              "    print(ch, code_point, unicodedata.name(ch), len(ch.encode()))\n"
              'decomposed = unicodedata.normalize("NFD", title)\n'
              'plain = "".join(ch for ch in decomposed if unicodedata.combining(ch) == 0)\n'
              "print(plain)")

# ------------------------------------------------------------ Q20 story project
nb.project("Invoice Engine", story="""
    You're writing the billing core for *Byte Bazaar*, a small online shop.
    Money must never be a float, and the customer's discounts come packed
    into a single integer of flags. Each step builds on the variables from the
    step before.
""",
     given='from decimal import Decimal, ROUND_HALF_UP\nimport struct\n\n'
           'items = [("Notebook", "3.50", 4), ("Pen", "1.20", 10),\n'
           '         ("Backpack", "39.99", 1), ("Gift card", "15.00", 2)]\n'
           'tax_rate = Decimal("0.19")\n\n'
           "STUDENT = 1       # 10% off\nBULK = 2          # 5% off\nCOUPON = 4        # 3% off\n"
           "customer_flags = 5\ninvoice_no = 1042\ncustomer = \"Zoë Müller\"",
     steps=[
         ("Convert each price to a `Decimal` and print one line per item: the "
          "name and its line total (`price * qty`). Then print the subtotal of "
          "all lines.",
          "subtotal = Decimal(0)\n"
          "for name, price, qty in items:\n"
          "    line = Decimal(price) * qty\n"
          "    subtotal += line\n"
          "    print(name, line)\n"
          'print("Subtotal:", subtotal)'),
         ("Decode `customer_flags`: print the name of every discount flag that "
          "is set (`STUDENT`, `BULK`, `COUPON`), one per line, using `&`. Also "
          "print how many flags are set with `bit_count()`.",
          'for flag_name, flag in [("STUDENT", STUDENT), ("BULK", BULK), ("COUPON", COUPON)]:\n'
          "    if customer_flags & flag:\n"
          "        print(flag_name)\n"
          'print("Flags set:", customer_flags.bit_count())'),
         ("Add up the discount percentages of the set flags (10, 5 and 3). "
          "Compute the discount amount as `subtotal * percent / 100`, rounded "
          "half up to 2 decimal places, and print the percent, the discount "
          "and the subtotal after the discount.",
          "percent = 0\n"
          "if customer_flags & STUDENT:\n    percent += 10\n"
          "if customer_flags & BULK:\n    percent += 5\n"
          "if customer_flags & COUPON:\n    percent += 3\n"
          'cent = Decimal("0.01")\n'
          "discount = (subtotal * percent / 100).quantize(cent, rounding=ROUND_HALF_UP)\n"
          "after = subtotal - discount\n"
          'print("Discount %:", percent)\n'
          'print("Discount:", discount)\n'
          'print("After discount:", after)'),
         ("Add VAT (`tax_rate`) to the discounted amount, rounded half up to "
          "2 decimal places. Print the VAT and the final total. Then print the "
          "total as a whole number of cents (an `int`).",
          "vat = (after * tax_rate).quantize(cent, rounding=ROUND_HALF_UP)\n"
          "total = after + vat\n"
          'print("VAT:", vat)\n'
          'print("Total:", total)\n'
          "total_cents = int(total * 100)\n"
          'print("Cents:", total_cents)'),
         ("Pack the invoice for storage with `struct`: invoice number "
          "(2-byte unsigned), flags (1-byte unsigned) and the total in cents "
          "(4-byte unsigned), little-endian. Print the byte count and the hex "
          "text, then unpack and print the three values. Last, print how many "
          "bytes the customer name needs in UTF-8 versus how many characters "
          "it has.",
          'record = struct.pack("<HBI", invoice_no, customer_flags, total_cents)\n'
          'print("Bytes:", len(record))\n'
          "print(record.hex())\n"
          'print(struct.unpack("<HBI", record))\n'
          'print(customer, len(customer), len(customer.encode("utf-8")))'),
     ])

nb.build()
