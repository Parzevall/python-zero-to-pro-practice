import sys; sys.path.insert(0, "..")
from builder import Notebook

nb = Notebook("NB27", title="Concurrency & Asyncio", intro="""
    Doing several things at once: threads for blocking work, `asyncio` for
    lots of waiting. Jupyter already runs an event loop, so use top-level
    `await` in a cell instead of `asyncio.run()`. Every wait in this notebook
    is a few milliseconds, and every result is collected and printed in a fixed
    order, so your output is always the same.
""")

# ------------------------------------------------------------ Warm-up (1-3 lines)
nb.q("Real-life", """
    `send_email` is slow in real life. Run `send_email("ana@example.com")` in
    its own thread, wait for the thread to finish, then print `log`.
""",
     given='log = []\n\ndef send_email(address):\n    log.append("sent to " + address)',
     solution='import threading\n'
              't = threading.Thread(target=send_email, args=("ana@example.com",))\n'
              't.start()\nt.join()\nprint(log)')

nb.q("Puzzle", """
    Start the three fetches below at the same time, in the order slow, fast,
    medium, and print the list of results you get back from one `await`.
""",
     given='import asyncio\n\nasync def fetch(name, delay):\n    await asyncio.sleep(delay)\n    return name',
     solution='results = await asyncio.gather(fetch("slow", 0.04), fetch("fast", 0.01), fetch("medium", 0.02))\n'
              'print(results)')

nb.q("Real-life", """
    A shop applies the same discount to every price. Use a thread pool with 3
    workers to run `apply_discount` over `prices`, and print the results as a list.
""",
     given='prices = [20, 35.5, 50]\n\ndef apply_discount(price):\n    return round(price * 0.9, 2)',
     solution='from concurrent.futures import ThreadPoolExecutor\n'
              'with ThreadPoolExecutor(max_workers=3) as pool:\n'
              '    print(list(pool.map(apply_discount, prices)))')

nb.q("Output-match", """
    Turn `slow_square(7)` into a task so it starts running in the background.
    Print `started` straight away, then print the task's result.
""",
     given='import asyncio\n\nasync def slow_square(n):\n    await asyncio.sleep(0.01)\n    return n * n',
     solution='task = asyncio.create_task(slow_square(7))\nprint("started")\nprint(await task)')

nb.q("Real-life", """
    `read_report` blocks for a moment (`time.sleep`), which would freeze the
    event loop. Run it in a worker thread from async code and print what it returns.
""",
     given='import asyncio\nimport time\n\ndef read_report():\n    time.sleep(0.01)\n    return "report ready"',
     solution='print(await asyncio.to_thread(read_report))')

# ------------------------------------------------------- Combine (3-6 lines)
nb.q("Real-life", """
    A weather API can hang. Give `slow_api()` at most 0.01 seconds: print its
    data if it answers in time, otherwise print `timed out`.
""",
     given='import asyncio\n\nasync def slow_api():\n    await asyncio.sleep(0.05)\n    return "data"',
     solution='try:\n'
              '    async with asyncio.timeout(0.01):\n'
              '        print(await slow_api())\n'
              'except TimeoutError:\n'
              '    print("timed out")')

nb.q("Real-life", """
    Check all `items` with a thread pool using `submit`, then print one line
    per item (the item and whether it is in stock) in the order of `items`.
""",
     given='stock = {"apple": 5, "pear": 0, "plum": 12}\nitems = ["plum", "apple", "pear"]\n\n'
           'def in_stock(item):\n    return item, stock[item] > 0',
     solution='from concurrent.futures import ThreadPoolExecutor\n'
              'with ThreadPoolExecutor() as pool:\n'
              '    futures = [pool.submit(in_stock, item) for item in items]\n'
              '    for future in futures:\n'
              '        print(*future.result())')

nb.q("Build", """
    Check every url concurrently. One failing check must not cancel the others.
    Print one line per url, in order: the url and either `ok` or
    `failed:` plus the error message.
""",
     given='import asyncio\n\nasync def check(url):\n    await asyncio.sleep(0.01)\n'
           '    if "bad" in url:\n        raise ValueError("unreachable " + url)\n'
           '    return "ok"\n\nurls = ["a.com", "bad.org", "c.net"]',
     solution='results = await asyncio.gather(*(check(url) for url in urls), return_exceptions=True)\n'
              'for url, result in zip(urls, results):\n'
              '    if isinstance(result, Exception):\n'
              '        print(url, "failed:", result)\n'
              '    else:\n'
              '        print(url, result)')

nb.q("Build", """
    Use a `TaskGroup` to price every item concurrently (one task per item).
    When the group has finished, print the total price.
""",
     given='import asyncio\n\nasync def price_of(item):\n    await asyncio.sleep(0.01)\n    return len(item) * 10\n\n'
           'items = ["tea", "coffee", "cake"]',
     solution='async with asyncio.TaskGroup() as group:\n'
              '    tasks = [group.create_task(price_of(item)) for item in items]\n'
              'print(sum(task.result() for task in tasks))')

nb.q("Output-match", """
    Write an async generator `countdown(n)` that sleeps 0.001 seconds and then
    yields `n`, `n - 1`, ... down to 1. Loop over `countdown(3)` with
    `async for`, printing each number on its own line, then print `Liftoff!`.
""",
     given='import asyncio',
     solution='async def countdown(n):\n'
              '    while n > 0:\n'
              '        await asyncio.sleep(0.001)\n'
              '        yield n\n'
              '        n -= 1\n\n'
              'async for number in countdown(3):\n'
              '    print(number)\n'
              'print("Liftoff!")')

# ------------------------------------------------ Small real tasks (6-12 lines)
nb.q("Real-life", """
    A laundry worker thread takes jobs from a `queue.Queue`. The main thread
    puts every job in `jobs` on the queue, then a `None` to say "no more".
    The worker appends each job in upper case to `done` and stops at `None`.
    Wait for the worker, then print `done`.
""",
     given='import queue\nimport threading\n\njobs = ["wash", "dry", "fold", "iron"]\ndone = []',
     solution='tasks = queue.Queue()\n\n'
              'def worker():\n'
              '    while True:\n'
              '        job = tasks.get()\n'
              '        if job is None:\n'
              '            break\n'
              '        done.append(job.upper())\n\n'
              't = threading.Thread(target=worker)\nt.start()\n'
              'for job in jobs:\n    tasks.put(job)\n'
              'tasks.put(None)\nt.join()\nprint(done)')

nb.q("Real-life", """
    A download server may only serve 2 downloads at once. Download every file
    in `files` concurrently without ever exceeding that limit. Print the list
    of results (in the order of `files`), then the highest number of downloads
    that were active at the same time, labelled like the expected output.
""",
     given='import asyncio\n\nactive = 0\npeak = 0\n\nasync def download(name):\n'
           '    global active, peak\n    active += 1\n    peak = max(peak, active)\n'
           '    await asyncio.sleep(0.01)\n    active -= 1\n    return name.upper()\n\n'
           'files = ["a", "b", "c", "d", "e"]',
     solution='limit = asyncio.Semaphore(2)\n\n'
              'async def limited(name):\n'
              '    async with limit:\n'
              '        return await download(name)\n\n'
              'results = await asyncio.gather(*(limited(name) for name in files))\n'
              'print(results)\n'
              'print("Peak:", peak)')

nb.q("Real-life", """
    A kitchen has one order taker and one cook. The order taker puts every
    dish of `orders` on an `asyncio.Queue`, then a `None`. The cook takes dishes
    until `None` and prints `Cooked` plus the dish. Run both at the same time.
""",
     given='import asyncio\n\norders = ["pizza", "salad", "soup"]',
     solution='async def order_taker(queue):\n'
              '    for dish in orders:\n'
              '        await queue.put(dish)\n'
              '    await queue.put(None)\n\n'
              'async def cook(queue):\n'
              '    while True:\n'
              '        dish = await queue.get()\n'
              '        if dish is None:\n'
              '            break\n'
              '        print("Cooked", dish)\n\n'
              'queue = asyncio.Queue()\n'
              'await asyncio.gather(order_taker(queue), cook(queue))')

nb.q("Build", """
    Write an **async context manager** class `Connection`. Entering it waits
    0.001 seconds and records `open` in `events`; leaving records `close`. It
    has an `async` method `query(text)` that records `query: ` plus the text.
    Use it in an `async with` block that runs two queries, then print `events`.
""",
     given='import asyncio\n\nevents = []',
     solution='class Connection:\n'
              '    async def __aenter__(self):\n'
              '        await asyncio.sleep(0.001)\n'
              '        events.append("open")\n'
              '        return self\n\n'
              '    async def __aexit__(self, exc_type, exc, traceback):\n'
              '        events.append("close")\n\n'
              '    async def query(self, text):\n'
              '        events.append("query: " + text)\n\n'
              'async with Connection() as connection:\n'
              '    await connection.query("SELECT 1")\n'
              '    await connection.query("SELECT 2")\n'
              'print(events)')

nb.q("Real-life", """
    `flaky_api` fails with a `ConnectionError` the first two times it is called.
    Write a coroutine `retry(func, attempts)` that awaits `func()` up to
    `attempts` times and returns the first success; if the last attempt also
    fails, the error must propagate. Call it with 5 attempts and print the
    result, then the number of calls made.
""",
     given='import asyncio\n\ncalls = 0\n\nasync def flaky_api():\n    global calls\n    calls += 1\n'
           '    await asyncio.sleep(0.001)\n    if calls < 3:\n        raise ConnectionError("try again")\n'
           '    return "payload"',
     solution='async def retry(func, attempts):\n'
              '    for attempt in range(1, attempts + 1):\n'
              '        try:\n'
              '            return await func()\n'
              '        except ConnectionError:\n'
              '            if attempt == attempts:\n'
              '                raise\n\n'
              'print(await retry(flaky_api, 5))\n'
              'print("Calls:", calls)')

# ------------------------------------------------ Puzzles & builds (10-20 lines)
nb.q("Puzzle", """
    `add_one` reads the counter, lets other threads run, then writes back, so
    parallel calls lose updates. Without changing `add_one`, run 5 threads that
    each call it 20 times, and make the final `counter` exactly 100 by
    protecting the calls with a lock. Print the counter.
""",
     given='import threading\nimport time\n\ncounter = 0\n\ndef add_one():\n    global counter\n'
           '    current = counter\n    time.sleep(0)\n    counter = current + 1',
     solution='lock = threading.Lock()\n\n'
              'def add_many():\n'
              '    for _ in range(20):\n'
              '        with lock:\n'
              '            add_one()\n\n'
              'threads = [threading.Thread(target=add_many) for _ in range(5)]\n'
              'for thread in threads:\n    thread.start()\n'
              'for thread in threads:\n    thread.join()\n'
              'print(counter)')

nb.q("Puzzle", """
    Two players take strict turns: `ping` goes first, then `pong`, three rounds
    each. Use two `asyncio.Event` objects so each player waits for its turn
    (and clears the event when its turn starts). Each turn appends the player's
    name to `log`. Run both players together and print `log`.
""",
     given='import asyncio\n\nlog = []\nping_turn = asyncio.Event()\npong_turn = asyncio.Event()',
     solution='async def ping():\n'
              '    for _ in range(3):\n'
              '        await ping_turn.wait()\n'
              '        ping_turn.clear()\n'
              '        log.append("ping")\n'
              '        pong_turn.set()\n\n'
              'async def pong():\n'
              '    for _ in range(3):\n'
              '        await pong_turn.wait()\n'
              '        pong_turn.clear()\n'
              '        log.append("pong")\n'
              '        ping_turn.set()\n\n'
              'ping_turn.set()\n'
              'await asyncio.gather(ping(), pong())\n'
              'print(log)')

nb.q("Real-life", """
    Build a polite page fetcher. `fetch_with_retry(url)` may only run while
    holding a `Semaphore(2)`, gives each attempt at most 0.02 seconds
    (`asyncio.timeout`), and tries at most twice. It returns the page, or
    `gave up` if both attempts time out. Fetch every url concurrently and
    print one line per url, in order: the url, an arrow `->`, the result.
""",
     given='import asyncio\n\nasync def fake_fetch(url, attempt):\n'
           '    if url == "slow.com" or (url == "flaky.com" and attempt == 1):\n'
           '        await asyncio.sleep(0.05)\n'
           '    else:\n'
           '        await asyncio.sleep(0.001)\n'
           '    return "<html of " + url + ">"\n\n'
           'urls = ["a.com", "flaky.com", "slow.com", "b.com"]',
     solution='limit = asyncio.Semaphore(2)\n\n'
              'async def fetch_with_retry(url):\n'
              '    async with limit:\n'
              '        for attempt in (1, 2):\n'
              '            try:\n'
              '                async with asyncio.timeout(0.02):\n'
              '                    return await fake_fetch(url, attempt)\n'
              '            except TimeoutError:\n'
              '                pass\n'
              '        return "gave up"\n\n'
              'pages = await asyncio.gather(*(fetch_with_retry(url) for url in urls))\n'
              'for url, page in zip(urls, pages):\n'
              '    print(url, "->", page)')

nb.q("Real-life", """
    Seven tickets are left and ten customers (threads) all try to buy one at
    the same moment. Write a class `Stock` with a `count` and a method
    `reserve()` that returns `True` and takes one ticket if any are left,
    otherwise `False`. Between checking and taking, call `time.sleep(0)` to
    simulate work, and make `reserve` safe with a lock. Start the ten customers,
    wait for them, and print how many reservations succeeded and how many
    tickets are left.
""",
     given='import threading\nimport time\n\nresults = []',
     solution='class Stock:\n'
              '    def __init__(self, count):\n'
              '        self.count = count\n'
              '        self.lock = threading.Lock()\n\n'
              '    def reserve(self):\n'
              '        with self.lock:\n'
              '            if self.count > 0:\n'
              '                time.sleep(0)\n'
              '                self.count -= 1\n'
              '                return True\n'
              '            return False\n\n'
              'stock = Stock(7)\n\n'
              'def customer():\n'
              '    results.append(stock.reserve())\n\n'
              'threads = [threading.Thread(target=customer) for _ in range(10)]\n'
              'for thread in threads:\n    thread.start()\n'
              'for thread in threads:\n    thread.join()\n'
              'print("Reserved:", results.count(True))\n'
              'print("Left:", stock.count)')

# ------------------------------------------------------------ Q20 story project
nb.project("Async Site Crawler", story="""
    You're testing a link checker for a small website. There is no network:
    `SITE` maps each page to the pages it links to, and `fetch` pretends to
    download a page. Real crawlers are mostly waiting, which is exactly what
    `asyncio` is good at. Every step builds on the ones before.
""",
     given='SITE = {\n'
           '    "/": ["/about", "/blog", "/shop"],\n'
           '    "/about": ["/", "/team"],\n'
           '    "/team": [],\n'
           '    "/blog": ["/blog/1", "/missing"],\n'
           '    "/blog/1": ["/blog/2"],\n'
           '    "/blog/2": ["/"],\n'
           '    "/shop": ["/shop/cart", "/slow"],\n'
           '    "/shop/cart": [],\n'
           '    "/slow": ["/hidden"],\n'
           '}\n'
           'DELAYS = {"/slow": 0.05}      # every other page answers in 0.001 s',
     steps=[
         ("Write `async def fetch(url)`: wait `DELAYS.get(url, 0.001)` seconds (`asyncio.sleep`), raise `FileNotFoundError(url)` if the page is not in `SITE`, otherwise return its list of links. Print the links of `/about`.",
          "import asyncio\n"
          "async def fetch(url):\n"
          "    await asyncio.sleep(DELAYS.get(url, 0.001))\n"
          "    if url not in SITE:\n        raise FileNotFoundError(url)\n"
          "    return SITE[url]\n"
          'print(await fetch("/about"))'),
         ("Write `async def fetch_many(urls)` that fetches all the urls concurrently without letting one failure cancel the rest, and returns a dict from url to result (the links, or the exception). Call it with `/`, `/missing` and `/team`, and print one line per url: the url and either the number of links or `ERROR`.",
          "async def fetch_many(urls):\n"
          "    results = await asyncio.gather(*(fetch(url) for url in urls), return_exceptions=True)\n"
          "    return dict(zip(urls, results))\n"
          'pages = await fetch_many(["/", "/missing", "/team"])\n'
          "for url, result in pages.items():\n"
          '    print(url, "ERROR" if isinstance(result, Exception) else len(result))'),
         ("Write `async def crawl(start, limit)` that visits the site level by level (all pages of one level concurrently, at most `limit` at a time using a `Semaphore`) and keeps a list `seen` of every url found, in discovery order, and a list `broken` of urls that could not be fetched. Also record in a dict `stats` the highest number of fetches active at once under the key `peak`. Crawl from `/` with limit 2 and print the number of pages found, the sorted broken urls, and the peak, labelled like the expected output.",
          'stats = {"active": 0, "peak": 0}\n'
          "async def limited_fetch(url, limit):\n"
          "    async with limit:\n"
          '        stats["active"] += 1\n'
          '        stats["peak"] = max(stats["peak"], stats["active"])\n'
          "        try:\n"
          "            return await fetch(url)\n"
          "        finally:\n"
          '            stats["active"] -= 1\n'
          "async def crawl(start, limit):\n"
          "    gate = asyncio.Semaphore(limit)\n"
          "    seen = [start]\n"
          "    broken = []\n"
          "    level = [start]\n"
          "    while level:\n"
          "        results = await asyncio.gather(*(limited_fetch(url, gate) for url in level), return_exceptions=True)\n"
          "        next_level = []\n"
          "        for url, result in zip(level, results):\n"
          "            if isinstance(result, Exception):\n"
          "                broken.append(url)\n"
          "                continue\n"
          "            for link in result:\n"
          "                if link not in seen:\n"
          "                    seen.append(link)\n"
          "                    next_level.append(link)\n"
          "        level = next_level\n"
          "    return seen, broken\n"
          'seen, broken = await crawl("/", 2)\n'
          'print("Pages found:", len(seen))\n'
          'print("Broken:", sorted(broken))\n'
          'print("Peak:", stats["peak"])'),
         ("A real checker must not wait forever. Write `async def check(url, gate)` that, while holding the semaphore `gate`, fetches the url with a 0.02 second `asyncio.timeout` and returns `ok`, `broken` (page not found) or `timeout`. Check every url in `seen` with a `Semaphore(3)`, then print every url whose status is not `ok` as `url status` (sorted by url), and finally how many were ok.",
          "async def check(url, gate):\n"
          "    async with gate:\n"
          "        try:\n"
          "            async with asyncio.timeout(0.02):\n"
          "                await fetch(url)\n"
          '            return "ok"\n'
          "        except FileNotFoundError:\n"
          '            return "broken"\n'
          "        except TimeoutError:\n"
          '            return "timeout"\n'
          "gate = asyncio.Semaphore(3)\n"
          "statuses = await asyncio.gather(*(check(url, gate) for url in seen))\n"
          "for url, status in sorted(zip(seen, statuses)):\n"
          '    if status != "ok":\n'
          "        print(url, status)\n"
          'print("OK pages:", statuses.count("ok"))'),
         ("Finish with the report. Write an async generator `healthy(urls, statuses)` that yields the urls whose status is `ok` (await `asyncio.sleep(0)` before each yield). Collect them with an `async for` into a list, then use a `TaskGroup` to fetch all those pages at once. Print each healthy page (sorted) with its number of links, then the page with the most links.",
          "async def healthy(urls, statuses):\n"
          "    for url, status in zip(urls, statuses):\n"
          '        if status == "ok":\n'
          "            await asyncio.sleep(0)\n"
          "            yield url\n"
          "good = []\n"
          "async for url in healthy(seen, statuses):\n"
          "    good.append(url)\n"
          "async with asyncio.TaskGroup() as group:\n"
          "    tasks = {url: group.create_task(fetch(url)) for url in good}\n"
          "counts = {url: len(task.result()) for url, task in tasks.items()}\n"
          "for url in sorted(counts):\n"
          "    print(url, counts[url])\n"
          'print("Most links:", max(counts, key=counts.get))'),
     ])

nb.build()
