"""Example: the ham and eggs set meal. Run with `python3 tools/recipe_art/ham_egg_teishoku.py`."""

import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images" / "ham-egg-teishoku.svg"

def hamegg():
    rnd = random.Random(62)
    b = wood("#cfa978", "#a9824f") + tray()
    PX, PY = 400, 190
    b += f'<ellipse cx="{PX}" cy="{PY}" rx="260" ry="118" fill="#ffffff" stroke="#e3e0da" stroke-width="3"/>'
    # cabbage + cherry tomatoes on the right
    for _ in range(150):
        x, y = PX + 140 + rnd.uniform(-70, 70), PY + rnd.uniform(-60, 60)
        if ((x-(PX+140))/75)**2 + ((y-PY)/62)**2 > 1: continue
        b += f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-14,14):.0f},{rnd.uniform(-4,4):.0f}" stroke="{rnd.choice(["#d9edb4","#c5e39a","#eaf5d6"])}" stroke-width="3" stroke-linecap="round"/>'
    for (tx, ty) in [(PX + 205, PY - 55), (PX + 215, PY + 40)]:
        b += f'<circle cx="{tx}" cy="{ty}" r="17" fill="#e53935"/><circle cx="{tx-5}" cy="{ty-5}" r="4" fill="#ff8a80"/>'
    # three overlapping ham slices with crispy edges
    for i, (hx, hy) in enumerate([(PX - 150, PY - 10), (PX - 95, PY + 15), (PX - 40, PY - 5)]):
        b += f'<circle cx="{hx}" cy="{hy}" r="62" fill="#c96d6a"/><circle cx="{hx}" cy="{hy}" r="56" fill="#f2a7a0"/>'
        for _ in range(6):
            b += f'<circle cx="{hx+rnd.uniform(-40,40):.0f}" cy="{hy+rnd.uniform(-40,40):.0f}" r="3" fill="#fbd0ca" opacity="0.8"/>'
    # egg whites spreading over ham with frilly crisp edges, two yolks
    b += blob(PX - 95, PY + 2, 95, "#fffdf6", rnd, n=14, jitter=0.16, stroke="#e8c98a")
    for (yx, yy) in [(PX - 130, PY - 10), (PX - 60, PY + 15)]:
        b += f'<circle cx="{yx}" cy="{yy}" r="24" fill="#f6a313" stroke="#e48409" stroke-width="2"/><ellipse cx="{yx-7}" cy="{yy-8}" rx="8" ry="5" fill="#ffd27a"/>'
    for _ in range(14):
        b += f'<circle cx="{PX-95+rnd.uniform(-70,70):.0f}" cy="{PY+rnd.uniform(-60,60):.0f}" r="1.4" fill="#3b3024"/>'
    b += rice_bowl(165, 430, rnd) + miso_bowl(395, 435, rnd) + takuan_dish() + tray_chopsticks()
    # small soy sauce cruet (the "what do you put on it" question)
    b += '<rect x="640" y="360" width="44" height="70" rx="12" fill="#ffffff" stroke="#c9c2b2" stroke-width="2"/><rect x="648" y="380" width="28" height="42" rx="8" fill="#3b1f12"/><rect x="654" y="346" width="16" height="18" rx="4" fill="#c62828"/>'
    return svg(b)

if __name__ == "__main__":
    OUT.write_text(hamegg())
    print(f"wrote {OUT}")
