"""Home-made simmered chashu pork (nibuta). Run with `python3 tools/recipe_art/chashu.py`."""

import math
import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images" / "homemade-chashu.svg"


def chashu_slice(x, y, rot, rnd):
    # round slice: dark glazed rim, pink-brown meat with fat marbling
    g = f'<g transform="rotate({rot:.0f} {x:.0f} {y:.0f})">'
    g += f'<ellipse cx="{x}" cy="{y}" rx="70" ry="54" fill="#5a2a12"/>'
    g += f'<ellipse cx="{x}" cy="{y}" rx="62" ry="47" fill="#c98a68"/>'
    for _ in range(4):
        a = rnd.uniform(0, math.pi)
        g += f'<path d="M{x-45+rnd.uniform(-5,5):.0f},{y+rnd.uniform(-25,25):.0f} q45,{rnd.uniform(-20,20):.0f} 90,{rnd.uniform(-8,8):.0f}" stroke="#f3dcc8" stroke-width="{rnd.uniform(3,6):.0f}" fill="none" opacity="0.85"/>'
    g += f'<ellipse cx="{x-18}" cy="{y-16}" rx="16" ry="6" fill="#ffffff" opacity="0.25"/>'
    return g + "</g>"


def chashu():
    rnd = random.Random(110)
    b = wood("#3b2a22", "#2a1d17")  # dark wood
    b += shadow(225)
    b += f'<circle cx="{CX}" cy="{CY}" r="232" fill="#1f1f1f"/><circle cx="{CX}" cy="{CY}" r="218" fill="#2b2b2b"/>'  # black plate
    # glossy sauce pool
    b += blob(CX, CY + 10, 170, "#4a1f0c", rnd, n=12, jitter=0.1)
    # fanned slices
    for i in range(5):
        a = math.radians(-150 + i * 30)
        x, y = CX + 70 * math.cos(a), CY + 40 + 70 * math.sin(a)
        b += chashu_slice(x, y, -20 + i * 10, rnd)
    # halved ajitama (seasoned soft-boiled egg)
    for (ex, ey) in [(CX + 120, CY + 95), (CX + 40, CY + 130)]:
        b += f'<ellipse cx="{ex}" cy="{ey}" rx="40" ry="32" fill="#b8763e"/><ellipse cx="{ex}" cy="{ey}" rx="34" ry="26" fill="#f6ead2"/>'
        b += f'<ellipse cx="{ex}" cy="{ey}" rx="18" ry="14" fill="#e88a12"/><ellipse cx="{ex-4}" cy="{ey-4}" rx="7" ry="4" fill="#f6b04a"/>'
    # shiraga negi (fine white leek) and green onion
    for _ in range(40):
        x, y = CX - 100 + rnd.uniform(-35, 35), CY + 90 + rnd.uniform(-22, 22)
        b += f'<path d="M{x:.0f},{y:.0f} q8,-10 18,-6" stroke="#f8f8ee" stroke-width="2" fill="none"/>'
    for _ in range(14):
        x, y = CX + rnd.uniform(-60, 60), CY + rnd.uniform(-40, 30)
        b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#b5e08a" stroke="#4f9a3a" stroke-width="1.5"/>'
    # kitchen twine leftover + deep frying pan hint (top right)
    b += '<circle cx="700" cy="90" r="70" fill="#2b2b2b" stroke="#444" stroke-width="6"/><circle cx="700" cy="90" r="56" fill="#4a1f0c"/>'
    b += '<rect x="560" y="80" width="80" height="18" rx="8" fill="#1b1b1b" transform="rotate(-10 600 90)"/>'
    b += chopsticks(40)
    return svg(b)


if __name__ == "__main__":
    OUT.write_text(chashu())
    print(f"wrote {OUT.name}")
