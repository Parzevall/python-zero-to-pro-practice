from sprintcheck.constraints import check_constraints


def comp(grid):
    return [x for row in grid for x in row]


def looped(grid):
    out = []
    for row in grid:
        for x in row:
            out.append(x)
    return out


def recursive(n):
    return 1 if n <= 1 else n * recursive(n - 1)


def uses_sum(rows):
    return sum(rows, [])


def gen(n):
    for i in range(n):
        yield i


def test_no_loops_passes_comprehension_and_fails_loop():
    assert check_constraints(comp, ["no-loops"]) == []
    assert check_constraints(looped, ["no-loops"])


def test_needs_comprehension():
    assert check_constraints(comp, ["needs-comprehension"]) == []
    assert check_constraints(looped, ["needs-comprehension"])


def test_needs_recursion():
    assert check_constraints(recursive, ["needs-recursion"]) == []
    assert check_constraints(comp, ["needs-recursion"])


def test_no_builtin():
    assert check_constraints(uses_sum, ["no-builtin:sum"])
    assert check_constraints(comp, ["no-builtin:sum"]) == []


def test_needs_generator():
    assert check_constraints(gen, ["needs-generator"]) == []
    assert check_constraints(comp, ["needs-generator"])


def test_max_lines():
    assert check_constraints(comp, ["max-lines:2"]) == []
    assert check_constraints(looped, ["max-lines:2"])


def test_unreadable_source_is_reported_not_crashed():
    violations = check_constraints(len, ["no-loops"])
    assert violations and "source" in violations[0].lower()
