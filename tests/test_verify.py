"""Tests for tools/verify.py, the checker every notebook relies on.

    python -m pytest -q
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))

import verify  # noqa: E402


# --------------------------------------------------------------- running

def test_run_captures_printed_output():
    assert verify.run('print("hi")\nprint(1 + 1)').shown == "hi\n2"


def test_run_reports_only_the_exception_name_after_any_output():
    result = verify.run('print("before")\nint("x")')
    assert result.error == "ValueError"
    assert result.shown == "before\nValueError"


def test_run_reports_a_syntax_error_and_runs_nothing():
    result = verify.run('print("first")\nprint("second)')
    assert result.shown == "SyntaxError"


def test_run_allows_top_level_await_like_jupyter():
    source = "import asyncio\nasync def f():\n    return 7\nprint(await f())"
    assert verify.run(source).shown == "7"


def test_run_gives_each_program_a_fresh_main_module():
    source = "from dataclasses import dataclass\n@dataclass\nclass P:\n    x: int\nprint(P(1))"
    assert verify.run(source).shown == "P(x=1)"


# ------------------------------------------------------------- the gate

def test_gate_blocks_a_loop_in_notebook_1():
    assert any("loop" in p for p in verify.too_early("for c in 'ab':\n    print(c)", 1))


def test_gate_allows_a_loop_once_it_is_taught():
    assert verify.too_early("for c in 'ab':\n    print(c)", 4) == []


def test_gate_blocks_list_methods_before_lists():
    assert verify.too_early("x = 'a b'.split()\nx.append('c')", 2)


def test_gate_flags_modules_missing_from_the_curriculum_map():
    problems = verify.too_early("import not_a_real_module", 32)
    assert problems and "curriculum map" in problems[0]


def test_gate_treats_cache_as_recursion_era_but_other_decorators_later():
    source = "from functools import cache\n@cache\ndef f(n):\n    return n\nprint(f(1))"
    assert verify.too_early(source, 11) == []
    assert verify.too_early("@shout\ndef f():\n    pass", 11)


def test_gate_ignores_code_that_does_not_parse():
    assert verify.too_early('print("oops)', 1) == []


def test_bare_final_expression_is_flagged_but_print_is_not():
    assert verify._ends_with_bare_expression("x = 1\nx + 1")
    assert not verify._ends_with_bare_expression("x = 1\nprint(x + 1)")


# --------------------------------------------------------------- parsing

QUESTION = """### NB01-Q02 · L1 · Arithmetic · Write

Print the total.

**Starting code (already in the cell below):**

```python
price = 2
```

<details><summary><b>Hint</b></summary>

Multiply.

</details>

<details><summary><b>Expected output</b></summary>

```text
4
```

</details>

<details><summary><b>Solution</b></summary>

```python
print(price * 2)
```

Why.

</details>

<details><summary><b>Senior dev solution</b></summary>

```python
print(price + price)
```

Note.

</details>"""


def test_parse_question_reads_every_part():
    q = verify.parse_question(QUESTION, "price = 2\n\n# your code here\n")
    assert (q.qid, q.level, q.type) == ("NB01-Q02", 1, "Write")
    assert q.shown == "price = 2"
    assert q.expected == "4"
    assert q.solution == "print(price * 2)"
    assert q.senior == "print(price + price)"
    assert q.dropdowns == list(verify.DROPDOWNS)


def test_a_correct_question_has_no_problems():
    q = verify.parse_question(QUESTION, "price = 2\n\n# your code here\n")
    assert verify.check_question(q, notebook=1, quick=True) == []


def test_a_wrong_expected_output_is_reported():
    q = verify.parse_question(QUESTION.replace("```text\n4", "```text\n5"), "price = 2\n")
    assert any("does not match" in p for p in verify.check_question(q, 1, quick=True))


def test_gate_allows_importing_a_module_the_program_writes_itself():
    program = 'Path("inventory.py").write_text("STOCK = 3")\nimport inventory'
    assert verify.too_early("import inventory", 13, program) == []
    assert verify.too_early("import inventory", 13)  # unknown without that context


def test_an_illustration_block_in_the_prompt_is_not_mistaken_for_starting_code():
    illustrated = QUESTION.replace(
        "Print the total.\n", "Print the total.\n\n```python\nprint('just an example')\n```\n")
    q = verify.parse_question(illustrated, "price = 2\n\n# your code here\n")
    assert q.shown == "price = 2"
