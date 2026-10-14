"""Spice chicken curry made with curry powder and garam masala. Run with `python3 tools/recipe_art/spice_curry.py`."""

import math
import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images" / "spice-chicken-curry.svg"


def spice_curry():
    rnd = random.Random(100)
    b = wood("#6b4a33", "#4f3524")
    # small spice dishes scattered on the table
    for (x, y, c) in [(90, 90, "#e0a020"), (720, 80, "#b5401c"), (90, 520, "#7a5a2a"), (720, 520, "#3f8f3a")]:
        b += f'<circle cx="{x}" cy="{y}" r="42" fill="#d8c7a8"/><circle cx="{x}" cy="{y}" r="34" fill="{c}"/>'
        for _ in range(20):
            b += f'<circle cx="{x+rnd.uniform(-26,26):.0f}" cy="{y+rnd.uniform(-26,26):.0f}" r="1.6" fill="#ffffff" opacity="0.35"/>'
    # star anise + cinnamon stick accents
    sx, sy = 160, 300
    for k in range(8):
        a = k * math.pi / 4
        b += f'<ellipse cx="{sx+14*math.cos(a):.0f}" cy="{sy+14*math.sin(a):.0f}" rx="12" ry="5" fill="#6b3418" transform="rotate({math.degrees(a):.0f} {sx+14*math.cos(a):.0f} {sy+14*math.sin(a):.0f})"/>'
    b += '<rect x="610" y="410" width="120" height="16" rx="8" fill="#a0602a" transform="rotate(-25 670 418)"/>'
    # large plate
    b += shadow(220)
    b += f'<circle cx="{CX}" cy="{CY}" r="228" fill="#f4efe6" stroke="#d9cfbf" stroke-width="3"/>'
    # yellow rice (left)
    b += blob(CX - 80, CY + 20, 120, "#f2cd5a", rnd, n=11, jitter=0.1)
    for _ in range(140):
        a = rnd.uniform(0, 2 * math.pi); r = 110 * math.sqrt(rnd.random())
        x, y = CX - 80 + r * math.cos(a), CY + 20 + r * math.sin(a) * 0.9
        b += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="6" ry="2.8" fill="{rnd.choice(["#f7dc7a","#fbe7a0","#efc548"])}" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    # metal katori bowl with curry (right)
    KX, KY = CX + 85, CY - 35
    b += f'<circle cx="{KX+6}" cy="{KY+8}" r="112" fill="#000" opacity="0.18"/>'
    b += f'<circle cx="{KX}" cy="{KY}" r="112" fill="#c9cdd2" stroke="#9aa0a6" stroke-width="3"/><circle cx="{KX}" cy="{KY}" r="98" fill="#a8adb3"/>'
    b += f'<circle cx="{KX}" cy="{KY}" r="94" fill="#a8441c"/>'
    for _ in range(10):
        a = rnd.uniform(0, 2 * math.pi); r = 80 * math.sqrt(rnd.random())
        b += blob(KX + r * math.cos(a), KY + r * math.sin(a), rnd.uniform(14, 22), "#b9532a", rnd, n=7, jitter=0.4)
    for _ in range(9):  # chicken
        a = rnd.uniform(0, 2 * math.pi); r = 70 * math.sqrt(rnd.random())
        b += blob(KX + r * math.cos(a), KY + r * math.sin(a), rnd.uniform(14, 18), "#d98a4e", rnd, n=7, jitter=0.3, stroke="#a8602e")
    # cream swirl + coriander
    b += f'<path d="M{KX-50},{KY+10} q25,-30 50,0 t50,0" stroke="#fff6e8" stroke-width="5" fill="none" stroke-linecap="round" opacity="0.9"/>'
    for _ in range(9):
        b += leaf(KX + rnd.uniform(-50, 40), KY + rnd.uniform(-45, 35), 22, rnd.choice(["#3f8f3a", "#4fa046"]), rnd.uniform(0, 360))
    # garam masala dusting
    for _ in range(60):
        a = rnd.uniform(0, 2 * math.pi); r = 85 * math.sqrt(rnd.random())
        b += f'<circle cx="{KX + r*math.cos(a):.0f}" cy="{KY + r*math.sin(a):.0f}" r="1.4" fill="#4a2410"/>'
    # spoon
    b += '<g transform="rotate(-30 640 500)"><ellipse cx="610" cy="500" rx="30" ry="20" fill="#d7dade"/><rect x="636" y="494" width="110" height="12" rx="6" fill="#c2c6ca"/></g>'
    return svg(b)


if __name__ == "__main__":
    OUT.write_text(spice_curry())
    print(f"wrote {OUT.name}")
