"""Regenerate assets/header.svg from the notebooks themselves.

    python tools/make_header.py

One dot per question, shaded by difficulty, one row per notebook, with the
three tiers side by side. Because it reads the real notebooks, the picture can
never drift from what's actually in them.

Difficulty is ordered magnitude, so the ramp is a single hue varying in
lightness: on the dark ground easy questions stay quiet and hard ones glow, and
the encoding survives colour-blindness because luminance alone carries it.
"""

import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from verify import TIERS, load  # noqa: E402

RAMP = {1: "#1c3a5e", 2: "#1f5fa9", 3: "#2f81f7", 4: "#6cb6ff", 5: "#cae8ff"}
LABEL = {1: "L1 Extremely Easy", 2: "L2 Easy", 3: "L3 Intermediate",
         4: "L4 Somewhat Difficult", 5: "L5 Hard"}

W = 1200
COL_X = (70, 448, 826)            # left edge of each tier column
NAME_W, PITCH, DOT = 34, 6.6, 2.3
ROW_Y0, ROW_H = 232, 15.5

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"


def tier_rows(tier: str) -> list[tuple[str, list[int]]]:
    rows = []
    for path in sorted((ROOT / tier).glob("NB*.ipynb")):
        _, questions = load(path)
        rows.append((path.name[:4], [q.level for q in questions if not q.qid.endswith("-P")]))
    return rows


def build() -> str:
    tiers = {tier: tier_rows(tier) for tier in TIERS}
    levels = [lv for rows in tiers.values() for _, lvs in rows for lv in lvs]
    counts = Counter(levels)
    total = len(levels)
    notebooks = sum(len(rows) for rows in tiers.values())
    longest = max(len(rows) for rows in tiers.values())
    H = int(ROW_Y0 + longest * ROW_H + 40)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{total} Python practice questions across {notebooks} notebooks in '
        'three tiers. Each dot is one question, shaded from dim for easy to bright for hard.">',
        '<defs><linearGradient id="bg" x1="0" y1="0" x2="0.65" y2="1">'
        '<stop offset="0%" stop-color="#090d13"/><stop offset="100%" stop-color="#131c2a"/>'
        '</linearGradient><linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#1c3a5e"/><stop offset="100%" stop-color="#cae8ff"/>'
        '</linearGradient></defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<rect x="0" y="0" width="4" height="{H}" fill="#2f81f7"/>',
        f'<text x="70" y="64" font-family="{MONO}" font-size="15" letter-spacing="5.5" '
        'fill="#6cb6ff">PYTHON · ZERO TO PRO</text>',
        f'<text x="70" y="116" font-family="{SERIF}" font-size="44" font-weight="700" '
        'fill="#f0f6fc">From your first print() to asyncio.</text>',
        f'<text x="70" y="148" font-family="{SANS}" font-size="16" fill="#8b949e">'
        f'{total} questions in {notebooks} notebooks. Every dot is one question, and every '
        'solution is run and checked.</text>',
    ]

    # difficulty legend, one line across the top
    x = 70
    for level in range(1, 6):
        o.append(f'<circle cx="{x + 5}" cy="180" r="5" fill="{RAMP[level]}"/>')
        o.append(f'<text x="{x + 16}" y="184" font-family="{MONO}" font-size="11.5" '
                 f'fill="#8b949e">{LABEL[level]} · {counts[level]}</text>')
        x += 216

    for col, tier in zip(COL_X, TIERS):
        rows = tiers[tier]
        o.append(f'<text x="{col}" y="{ROW_Y0 - 18}" font-family="{MONO}" font-size="11" '
                 f'letter-spacing="1.8" fill="#6e7681">{tier.upper()}/ · '
                 f'{sum(len(lv) for _, lv in rows)}</text>')
        for i, (name, lvs) in enumerate(rows):
            y = ROW_Y0 + i * ROW_H
            o.append(f'<text x="{col}" y="{y + 3.5}" font-family="{MONO}" font-size="10" '
                     f'fill="#484f58">{name}</text>')
            for j, level in enumerate(lvs):
                o.append(f'<circle cx="{col + NAME_W + j * PITCH:.1f}" cy="{y}" r="{DOT}" '
                         f'fill="{RAMP[level]}"/>')
            end = col + NAME_W + len(lvs) * PITCH
            assert end < col + 372, f"{name}: {len(lvs)} dots overflow the column"

    o.append(f'<rect x="70" y="{H - 22}" width="1060" height="3" rx="1.5" fill="url(#rule)" '
             'opacity="0.5"/>')
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = ROOT / "assets" / "header.svg"
    svg = build()
    ET.fromstring(svg)  # fail loudly on malformed output
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
