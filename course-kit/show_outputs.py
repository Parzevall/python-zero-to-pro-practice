import json, sys
for f in sys.argv[1:]:
    nb = json.load(open(f))
    print("==", f, len(nb["cells"]), "cells")
    for c in nb["cells"]:
        s = "".join(c["source"])
        if c["cell_type"] == "markdown" and "```text\n" in s:
            h = s.splitlines()[0]; e = s.split("```text\n")[1].split("\n```")[0]
            print(h, "=>", e.replace("\n", " | "))
