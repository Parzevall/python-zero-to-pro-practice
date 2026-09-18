"""Asserts the spec's difficulty curve and P0 topic quotas hold."""

from collections import Counter

import pytest

from content import all_notebooks

# spec section 5.1 - (L1, L2, L3, L4, L5) per notebook
EXPECTED_DISTRIBUTION = {
    1: (12, 11, 8, 3, 2),   2: (11, 12, 9, 4, 2),   3: (10, 12, 10, 4, 2),
    4: (9, 12, 10, 5, 2),   5: (9, 11, 9, 4, 3),    6: (6, 10, 13, 9, 4),
    7: (5, 10, 13, 9, 5),   8: (4, 9, 14, 11, 6),   9: (2, 7, 13, 15, 7),
    10: (2, 6, 11, 16, 7),
}

# spec section 4 - minimum questions tagged with each P0 topic
TOPIC_QUOTAS = {
    1: {"Variables": 2, "Primitive Types": 2, "Casting": 3, "Arithmetic": 4,
        "Comparison": 2, "Logical": 2, "Identity": 1, "Membership": 2,
        "Environment": 2, "Dynamic Typing": 2},
}


def notebooks_by_number():
    return {nb.number: nb for nb in all_notebooks()}


@pytest.mark.parametrize("number,expected", sorted(EXPECTED_DISTRIBUTION.items()))
def test_difficulty_distribution_matches_spec(number, expected):
    books = notebooks_by_number()
    if number not in books:
        pytest.skip(f"notebook {number:02d} not authored yet")
    counts = Counter(int(q.level) for q in books[number].questions)
    actual = tuple(counts.get(level, 0) for level in range(1, 6))
    assert actual == expected, f"nb{number:02d} L1-L5 = {actual}, spec says {expected}"


@pytest.mark.parametrize("number,quotas", sorted(TOPIC_QUOTAS.items()))
def test_p0_topic_quotas_met(number, quotas):
    books = notebooks_by_number()
    if number not in books:
        pytest.skip(f"notebook {number:02d} not authored yet")
    counts = Counter(q.topic for q in books[number].questions)
    shortfall = {t: (counts.get(t, 0), need) for t, need in quotas.items()
                 if counts.get(t, 0) < need}
    assert not shortfall, f"nb{number:02d} topic shortfall (have, need): {shortfall}"


def test_every_notebook_ends_on_a_hard_question():
    for nb in all_notebooks():
        levels = [int(q.level) for q in nb.questions]
        assert max(levels) == 5, f"nb{nb.number:02d} has no L5 question"


def test_generated_notebooks_match_content():
    from build import NOTEBOOK_DIR, drifted

    for nb in all_notebooks():
        if not (NOTEBOOK_DIR / nb.filename).exists():
            continue
        assert not drifted(nb, NOTEBOOK_DIR), (
            f"{nb.filename} is out of date with content/ - "
            f"run `python build.py --force --only {nb.number}` "
            f"(this will discard answers written in that notebook)"
        )
