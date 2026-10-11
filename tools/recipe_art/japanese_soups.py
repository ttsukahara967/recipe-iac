"""Hearty Japanese soups: suiton and kenchin-jiru. Run with `python3 tools/recipe_art/japanese_soups.py`."""

import math
import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images"


def lacquer_bowl(rnd, broth):
    s = shadow(220)
    s += f'<circle cx="{CX}" cy="{CY}" r="226" fill="#161616"/><circle cx="{CX}" cy="{CY}" r="212" fill="#8e1f1f"/><circle cx="{CX}" cy="{CY}" r="202" fill="#1d1d1d"/>'
    s += f'<circle cx="{CX}" cy="{CY}" r="192" fill="{broth}"/><circle cx="{CX}" cy="{CY}" r="192" fill="#fff4d6" opacity="0.25"/>'
    for _ in range(30):  # oil droplets on the surface
        x, y = in_circle(rnd, 175)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2,6):.0f}" fill="#f6d68a" opacity="0.7"/>'
    return s


def root_vegetables(rnd, n=1.0):
    s = ""
    for _ in range(int(9 * n)):  # daikon half-moons
        x, y = in_circle(rnd, 150)
        s += f'<path d="M{x-18:.0f},{y:.0f} a18,18 0 0,1 36,0 z" fill="#f3efe2" stroke="#d9d2bd" stroke-width="2" transform="rotate({rnd.uniform(0,360):.0f} {x:.0f} {y:.0f})"/>'
    for _ in range(int(9 * n)):  # carrot quarter-moons
        x, y = in_circle(rnd, 150)
        s += f'<path d="M{x:.0f},{y:.0f} l16,0 a16,16 0 0,0 -16,-16 z" fill="#ef7d2d" transform="rotate({rnd.uniform(0,360):.0f} {x:.0f} {y:.0f})"/>'
    for _ in range(int(10 * n)):  # gobo shavings
        x, y = in_circle(rnd, 150)
        s += f'<path d="M{x-12:.0f},{y:.0f} q12,-5 24,0" stroke="#8a6a46" stroke-width="5" fill="none" stroke-linecap="round" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    for _ in range(int(4 * n)):  # shiitake slices
        x, y = in_circle(rnd, 140)
        s += f'<path d="M{x-14:.0f},{y:.0f} a14,10 0 0,1 28,0 z" fill="#6b4226" transform="rotate({rnd.uniform(0,360):.0f} {x:.0f} {y:.0f})"/>'
    return s


def green_onion(rnd, n=24, r=150):
    s = ""
    for _ in range(n):
        x, y = in_circle(rnd, r)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="5" fill="#b9e08a" stroke="#4f9a3a" stroke-width="2"/>'
    return s


def suiton():
    rnd = random.Random(90)
    b = wood("#c8a77d", "#a58257") + lacquer_bowl(rnd, "#c79a4e")
    b += root_vegetables(rnd)
    for _ in range(7):  # chicken
        x, y = in_circle(rnd, 140)
        b += blob(x, y, rnd.uniform(13, 17), "#e9cfae", rnd, n=7, jitter=0.3, stroke="#c9a77d")
    for _ in range(9):  # flour dumplings: irregular, glossy, white
        x, y = in_circle(rnd, 135)
        b += blob(x, y, rnd.uniform(22, 30), "#f6f1e4", rnd, n=8, jitter=0.35, stroke="#e2d6b8")
        b += f'<ellipse cx="{x-6:.0f}" cy="{y-7:.0f}" rx="8" ry="4" fill="#ffffff" opacity="0.7"/>'
    b += green_onion(rnd)
    b += chopsticks(690)
    return svg(b)


def kenchin():
    rnd = random.Random(91)
    b = wood("#8a6a4a", "#6b4f34") + lacquer_bowl(rnd, "#b9874a")
    b += root_vegetables(rnd)
    for _ in range(6):  # taro (satoimo)
        x, y = in_circle(rnd, 140)
        b += blob(x, y, rnd.uniform(16, 20), "#efe6d6", rnd, n=8, jitter=0.2, stroke="#bfae8f")
    for _ in range(7):  # konnyaku, torn
        x, y = in_circle(rnd, 145)
        b += blob(x, y, rnd.uniform(11, 15), "#6b5a4e", rnd, n=7, jitter=0.35)
    for _ in range(12):  # tofu crumbled by hand, lightly browned
        x, y = in_circle(rnd, 145)
        b += blob(x, y, rnd.uniform(10, 16), "#fbf6e8", rnd, n=7, jitter=0.4, stroke="#e3c48a")
    b += green_onion(rnd, n=18, r=120)
    b += chopsticks(690)
    return svg(b)


if __name__ == "__main__":
    for name, fn in [("gutakusan-suiton", suiton), ("kenchin-jiru", kenchin)]:
        (OUT_DIR / f"{name}.svg").write_text(fn())
        print(f"wrote {name}.svg")
