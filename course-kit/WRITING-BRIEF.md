# Brief: writing one notebook in format v3

REPO = /home/topg/Projects/PCS/Py_DS_ML_Bootcamp-master/Refactored_Py_DS_ML_Bootcamp-master/01-Python-Crash-Course/pythonsprints
Your notebook NBxx -> write REPO/course-kit/src/nbxx.py (lowercase, two digits).

## Read first
1. REPO/course-kit/builder.py — the builder (`q(kind, prompt, solution=, given=)`, `project(...)`).
2. REPO/course-kit/src/nb01.py — THE REFERENCE for tone, prompt length, variety and story-project style. Read it fully.
3. REPO/course-kit/src/nb07.py — a later-tier example (functions everywhere).
4. Your entry in REPO/course-kit/plan_data.py (covers / traps / samples / project idea) and the earlier entries (what the learner already knows).

## Format (decided with the learner — don't deviate)
- Exactly 19 `nb.q()` calls, then `nb.project()` as Q20 with 4-6 steps, then `nb.build()`.
- Ramp, intermediate/advanced: Q1-5 one to three lines, Q6-10 3-6 lines, Q11-15 6-12 lines, Q16-19 10-20 lines; project 30-60 lines total across steps that build on each other.
- Write questions only. kinds: "Build", "Output-match", "Puzzle", "Real-life" — mix them (at least 3 Puzzle, several Real-life).
- Real situations (shop, bank, school, logs, files, APIs, games, schedules, inventory, users) and puzzles, fun like a classic exercise sheet, not abstract trivia. Every question drills one concept from YOUR covers list; cover most of the list. Plant the plan's "traps" inside the given data of normal Write tasks (no Fix/Predict/Error/Refactor questions exist any more).
- No hints, no "why" notes, one plain solution per question. Never type the expected output into the prompt (the builder runs the code and shows it); describe the target format in words. Exact text samples are fine only if literally what the solution prints.
- Solutions: the simple, clear way a learner at THIS point writes it, using only what this notebook and earlier ones teach (the builder enforces most of this via course-kit/checker.py `too_early`; respect the spirit too).
- given = starting data in the learner's cell (use it instead of input()).

## Hard rules (the build fails on most of these)
- Deterministic output: sorted() before printing sets; `random` only after `random.seed(...)`; no now()/time() values, timings, memory addresses or default object reprs (`<X object at 0x..>`) in output.
- Solutions must print(). No input(). No asyncio.run() — use top-level `await main()` (supported). No multiprocessing / ProcessPoolExecutor.
- File questions: create files inside `tempfile.TemporaryDirectory()` (put it in given or the solution), never depend on the current directory. Exception: the capstone's `%%writefile` modules (see below).
- Logging: `logging.basicConfig(stream=sys.stdout, force=True, format=...)` or a StringIO you print; never stderr.
- unittest: run with `unittest.TextTestRunner(stream=io.StringIO())`, print only stable facts (wasSuccessful, counts, names), never the timing line.
- Networking: only 127.0.0.1 with port 0, timeouts, always shut servers down, never print port numbers. No real internet.
- Python is 3.14 here, but keep to 3.10+ features unless your notebook is specifically about newer ones. Never 3.14-only syntax like unparenthesized `except A, B:`; no bare `except:`; no return/break inside `finally`. Solutions model good practice.
- Use natural variable names; solutions run in a separate process, so nothing clashes with the builder.
- Advanced tier: the topics are "under the hood", but keep tasks concrete and real (a retry decorator for a flaky API call, a timer context manager, a plugin registry, a rate limiter, a typed config loader), not abstract metaprogramming trivia.

## Build loop
`cd REPO/course-kit/src && python3 nbxx.py` until it prints "OK wrote ...". Then print the expected outputs:
`python3 REPO/course-kit/show_outputs.py REPO/<tier>/NBxx-*.ipynb`
and check each prompt really matches its output (format, labels, numbers).

## Capstones only (NB20, NB32)
A capstone has NO `nb.q()` calls: one `nb.project(title, story=, given=, given_files=, steps=)` with 5-6 milestones, rendered as the whole notebook.
- A step can be `(prompt, solution)` or `(prompt, solution, {"module.py": code})`. Files become `%%writefile` cells; the solution then imports and uses them and must print proof it works. Each file name is written exactly once (no rewriting a module later — add a new module or put new functions in the next file).
- `given_files={"teammate_module.py": code, "data.json": text}` = starter files the learner runs first. Use it for "a teammate wrote this module; read it and build on it".
- Prompts: 3-8 sentences, clear spec of functions/classes and what to print.

## Rules for you
- Do not edit any other file. Do not git commit. Other writers are doing other notebooks in parallel.
- Final report: under 80 words — "OK" or what failed, plus real concerns only. No file dumps.
