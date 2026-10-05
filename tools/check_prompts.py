"""Report questions whose prompt shows a ```text example that differs from the
real expected output. A difference is not always wrong (some prompts show a
format sample), so read each one, but hand-computed numbers drift."""

import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"```text\n(.*?)\n```", re.S)

for name in sys.argv[1:]:
    for cell in json.loads(Path(name).read_text())["cells"]:
        src = "".join(cell["source"])
        if not src.startswith("#") or "<details>" not in src:
            continue
        prompt, _, rest = src.partition("<details>")
        exp = re.search(r"Expected output</b></summary>\s*```text\n(.*?)\n```", rest, re.S)
        shown = FENCE.findall(prompt)
        if exp and shown and exp.group(1) not in shown:
            print(f"{src.splitlines()[0]}\n  prompt:   {shown[-1]!r}\n  expected: {exp.group(1)!r}")
