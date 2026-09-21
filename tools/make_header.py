"""Regenerate assets/header.svg from the real question data.

Every dot is one question, shaded by difficulty. Because it is generated from
content/, the picture can never drift from what is actually in the notebooks.

    python tools/make_header.py

Difficulty is ordered magnitude, so the ramp is a single hue varying in
lightness rather than a green-to-red rainbow: on a dark surface the easy
questions stay quiet and the hard ones glow, which also means the encoding
survives colour-blindness (luminance alone carries it).
"""

import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from content import all_notebooks

RAMP = {1: "#1c3a5e", 2: "#1f5fa9", 3: "#2f81f7", 4: "#6cb6ff", 5: "#cae8ff"}
LABEL = {
    1: "L1  Extremely Easy", 2: "L2  Easy", 3: "L3  Intermediate",
    4: "L4  Somewhat Difficult", 5: "L5  Hard",
}
SHORT = {
    1: "Foundations", 2: "Strings", 3: "Lists &amp; Tuples", 4: "Dicts &amp; Sets",
    5: "Control Flow", 6: "Functions", 7: "Comprehensions", 8: "OOP",
    9: "Generators", 10: "Stdlib &amp; Regex",
}

W, H = 1200, 452
X0, PITCH, DOT = 252, 14.0, 4.5      # 44 dots must clear the legend at x=900
ROW_Y0, ROW_H = 190, 23.5
LEGEND_X, LEGEND_Y = 900, 196

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"


def build() -> str:
    rows = [(nb.number, sorted(int(q.level) for q in nb.questions)) for nb in all_notebooks()]
    counts = Counter(level for _, levels in rows for level in levels)
    total = sum(len(levels) for _, levels in rows)

    o = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="{total} Python practice questions across {len(rows)} notebooks. Each dot is one '
        'question, shaded from dim for easy to bright for hard. Difficulty rises left to right within a '
        'notebook and top to bottom across them.">',
        '<defs>'
        '<linearGradient id="bg" x1="0" y1="0" x2="0.65" y2="1">'
        '<stop offset="0%" stop-color="#090d13"/><stop offset="100%" stop-color="#131c2a"/></linearGradient>'
        '<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0%" stop-color="#1c3a5e"/><stop offset="100%" stop-color="#cae8ff"/></linearGradient>'
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        f'<rect x="0" y="0" width="4" height="{H}" fill="#2f81f7"/>',
        f'<text x="70" y="70" font-family="{MONO}" font-size="15" letter-spacing="5.5" '
        'fill="#6cb6ff">PYTHON · ZERO TO PRO</text>',
        f'<text x="70" y="124" font-family="{SERIF}" font-size="46" font-weight="700" '
        'fill="#f0f6fc">Every dot is a question you can&#8217;t fake.</text>',
        f'<text x="70" y="156" font-family="{SANS}" font-size="16" fill="#8b949e">'
        f'{total} of them. Hidden hints, hidden solutions, and every answer graded the moment you write it.</text>',
        f'<text x="{LEGEND_X}" y="{LEGEND_Y - 16}" font-family="{MONO}" font-size="10.5" '
        'letter-spacing="1.8" fill="#6e7681">DIFFICULTY</text>',
    ]

    for i, level in enumerate(range(1, 6)):
        y = LEGEND_Y + i * 23
        o.append(f'<circle cx="{LEGEND_X + 5}" cy="{y}" r="5" fill="{RAMP[level]}"/>')
        o.append(f'<text x="{LEGEND_X + 20}" y="{y + 4}" font-family="{MONO}" font-size="11.5" '
                 f'fill="#8b949e">{LABEL[level]}</text>')
        o.append(f'<text x="1130" y="{y + 4}" font-family="{MONO}" font-size="11.5" fill="#484f58" '
                 f'text-anchor="end">{counts[level]}</text>')

    o.append(f'<line x1="{LEGEND_X}" y1="{LEGEND_Y + 128}" x2="1130" y2="{LEGEND_Y + 128}" '
             'stroke="#21262d" stroke-width="1"/>')
    o.append(f'<text x="{LEGEND_X}" y="{LEGEND_Y + 152}" font-family="{MONO}" font-size="11.5" '
             f'fill="#6e7681">{len(rows)} notebooks · {len(rows)} projects</text>')

    for i, (number, levels) in enumerate(rows):
        y = ROW_Y0 + i * ROW_H
        o.append(f'<text x="70" y="{y + 4}" font-family="{MONO}" font-size="11.5" fill="#3d444d">{number:02d}</text>')
        o.append(f'<text x="96" y="{y + 4}" font-family="{MONO}" font-size="11.5" fill="#8b949e">{SHORT[number]}</text>')
        for j, level in enumerate(levels):
            o.append(f'<circle cx="{X0 + j * PITCH:.1f}" cy="{y}" r="{DOT}" fill="{RAMP[level]}"/>')
        end = X0 + len(levels) * PITCH + 10
        assert end < LEGEND_X - 8, f"row {number} count label at {end:.0f} collides with legend"
        o.append(f'<text x="{end:.1f}" y="{y + 4}" font-family="{MONO}" font-size="11" '
                 f'fill="#3d444d">{len(levels)}</text>')

    o.append(f'<rect x="70" y="{H - 26}" width="1060" height="3" rx="1.5" fill="url(#rule)" opacity="0.5"/>')
    o.append('</svg>')

    svg = "\n".join(o)
    # notebook titles contain bare ampersands; SVG needs them escaped
    return re.sub(r'&(?!(?:amp|lt|gt|quot|apos|#\d+|#x[0-9A-Fa-f]+);)', '&amp;', svg)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets" / "header.svg"
    svg = build()
    ET.fromstring(svg)                       # fail loudly on malformed output
    out.write_text(svg)
    print(f"wrote {out} ({len(svg)} bytes)")
