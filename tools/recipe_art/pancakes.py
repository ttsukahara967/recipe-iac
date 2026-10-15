"""Fluffy pancakes with butter, honey and strawberry jam. Run with `python3 tools/recipe_art/pancakes.py`."""

import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images" / "fluffy-pancakes.svg"


def pancakes():
    rnd = random.Random(120)
    b = wood("#c9a27a", "#a8835a")
    b += shadow(220)
    b += f'<circle cx="{CX}" cy="{CY}" r="228" fill="#ffffff" stroke="#e3e0da" stroke-width="3"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="205" fill="none" stroke="#f0ebe2" stroke-width="3"/>'
    # stack of three pancakes seen slightly from above: offset rims show the layers
    for i, dy in enumerate([40, 22, 4]):
        b += f'<ellipse cx="{CX}" cy="{CY+dy+10}" rx="150" ry="132" fill="#b8742e"/>'
        b += f'<ellipse cx="{CX}" cy="{CY+dy}" rx="150" ry="132" fill="#d9964a"/>'
    b += f'<ellipse cx="{CX}" cy="{CY+4}" rx="140" ry="122" fill="#c97f34"/>'
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="128" ry="110" fill="#d68c3c"/>'
    for _ in range(30):  # tiny bubbles on the browned surface
        x, y = CX + rnd.uniform(-100, 100), CY + rnd.uniform(-85, 85)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.5,3):.1f}" fill="#b8742e" opacity="0.6"/>'
    # honey dripping over the top and down the side
    b += blob(CX - 10, CY - 5, 85, "#f2b01e", rnd, n=11, jitter=0.25)
    b += blob(CX - 10, CY - 5, 85, "#ffd45a", rnd, n=11, jitter=0.25).replace('fill="#ffd45a"', 'fill="#ffd45a" opacity="0.35"')
    for (x, length) in [(CX - 90, 70), (CX + 40, 95), (CX + 95, 55)]:
        b += f'<path d="M{x},{CY+60} q4,{length/2} 0,{length}" stroke="#f2b01e" stroke-width="12" fill="none" stroke-linecap="round"/>'
    # butter pat with a melting edge
    b += f'<rect x="{CX-28}" y="{CY-40}" width="56" height="44" rx="6" fill="#fff1a8" stroke="#f0d86a" stroke-width="2" transform="rotate(10 {CX} {CY-18})"/>'
    b += f'<ellipse cx="{CX-20}" cy="{CY-32}" rx="12" ry="5" fill="#ffffff" opacity="0.7"/>'
    # strawberry jam in a small dish
    b += '<circle cx="640" cy="470" r="58" fill="#ffffff" stroke="#e3e0da" stroke-width="3"/>'
    b += blob(640, 470, 42, "#c8102e", rnd, n=9, jitter=0.2)
    for _ in range(10):
        b += f'<ellipse cx="{640+rnd.uniform(-28,28):.0f}" cy="{470+rnd.uniform(-24,24):.0f}" rx="5" ry="3.5" fill="#e5384f"/>'
    b += '<ellipse cx="628" cy="456" rx="12" ry="5" fill="#ffffff" opacity="0.4"/>'
    # honey jar with dipper
    b += '<rect x="110" y="410" width="90" height="110" rx="18" fill="#f6c03a" stroke="#d9a01e" stroke-width="3"/><rect x="104" y="396" width="102" height="22" rx="8" fill="#a0602a"/>'
    b += '<rect x="148" y="320" width="12" height="100" rx="6" fill="#8a5a36" transform="rotate(20 154 370)"/>'
    # fork and knife
    b += '<rect x="80" y="120" width="12" height="230" rx="5" fill="#c2c6ca" transform="rotate(-8 86 235)"/>'
    b += '<rect x="712" y="120" width="14" height="230" rx="6" fill="#c2c6ca" transform="rotate(8 719 235)"/>'
    return svg(b)


if __name__ == "__main__":
    OUT.write_text(pancakes())
    print(f"wrote {OUT.name}")
