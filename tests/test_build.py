import nbformat

from build import render
from content.schema import Case, Level, Notebook, Question


def sample_notebook():
    q = Question(
        qid="Q-001", level=Level.L1, topic="Variables",
        prompt="Return the number 7.", hint="Just return it.",
        solution="def seven():\n    return 7", explanation="Literal return.",
        kind="function", entry="seven",
        cases=[Case(expected=7), Case(expected=7), Case(expected=7)],
        starter="def seven():\n    ...",
    )
    return Notebook(number=1, slug="demo", title="Demo", intro="Intro text.", questions=[q])


def test_render_produces_a_valid_notebook():
    nb = render(sample_notebook())
    nbformat.validate(nb)


def test_kernel_is_the_portable_default():
    """Every Jupyter install provides "python3"; a custom kernel name would
    make these notebooks fail to open on anyone else's machine."""
    nb = render(sample_notebook())
    assert nb.metadata.kernelspec.name == "python3"


def test_question_header_uses_the_exact_label_format():
    nb = render(sample_notebook())
    md = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    assert "### Q-001 - L1 Extremely Easy - Variables" in md


def test_hint_and_solution_are_separate_collapsed_details_in_markdown():
    nb = render(sample_notebook())
    md = "\n".join(c.source for c in nb.cells if c.cell_type == "markdown")
    code = "\n".join(c.source for c in nb.cells if c.cell_type == "code")
    assert md.count("<details>") == 2
    assert "<summary>Hint</summary>" in md and "<summary>Solution</summary>" in md
    # the answer must never leak into an executable cell
    assert "return 7" not in code


def test_code_cell_has_starter_and_check_call():
    nb = render(sample_notebook())
    code = [c.source for c in nb.cells if c.cell_type == "code"]
    assert any("check('Q-001', seven)" in c for c in code)
    assert any("def seven():" in c for c in code)


def test_cells_have_no_execution_output():
    nb = render(sample_notebook())
    for cell in nb.cells:
        if cell.cell_type == "code":
            assert cell.outputs == [] and cell.execution_count is None


def test_write_refuses_to_clobber_without_force(tmp_path):
    from build import write
    nb = sample_notebook()
    write(nb, tmp_path)
    (tmp_path / nb.filename).write_text("LEARNER ANSWERS")
    write(nb, tmp_path)
    assert (tmp_path / nb.filename).read_text() == "LEARNER ANSWERS"
    write(nb, tmp_path, force=True)
    assert (tmp_path / nb.filename).read_text() != "LEARNER ANSWERS"
