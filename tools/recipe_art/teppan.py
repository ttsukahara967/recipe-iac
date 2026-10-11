"""Konamon / teppan series: okonomiyaki and sauce yakisoba. Run with `python3 tools/recipe_art/teppan.py`."""

import math
import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images"


def iron_plate():
    # dark teppan griddle with a subtle sheen
    s = f'<rect width="{W}" height="{H}" fill="#2a2a2c"/>'
    for y in range(0, H, 24):
        s += f'<rect x="0" y="{y}" width="{W}" height="2" fill="#343438"/>'
    s += f'<ellipse cx="{CX-120}" cy="{CY-160}" rx="260" ry="60" fill="#ffffff" opacity="0.04"/>'
    return s


def toppings(rnd, cx, cy, rx, ry):
    s = ""
    for _ in range(140):  # aonori
        a = rnd.uniform(0, 2 * math.pi); r = math.sqrt(rnd.random())
        s += f'<circle cx="{cx + rx*r*math.cos(a):.0f}" cy="{cy + ry*r*math.sin(a):.0f}" r="{rnd.uniform(1.5,2.8):.1f}" fill="{rnd.choice(["#2f7d32","#3f9a3a","#1f5f22"])}"/>'
    for _ in range(36):  # katsuobushi
        a = rnd.uniform(0, 2 * math.pi); r = math.sqrt(rnd.random()) * 0.8
        x, y = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
        s += f'<path d="M{x:.0f},{y:.0f} q8,-6 16,0" stroke="{rnd.choice(["#d9a06a","#c98d5e","#e8b98a"])}" stroke-width="4" fill="none" stroke-linecap="round" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    return s


def okonomiyaki():
    rnd = random.Random(80)
    b = iron_plate()
    b += f'<ellipse cx="{CX+12}" cy="{CY+18}" rx="230" ry="215" fill="#000" opacity="0.35"/>'
    b += f'<circle cx="{CX}" cy="{CY}" r="215" fill="#a8652a"/><circle cx="{CX}" cy="{CY}" r="205" fill="#c98a45"/>'
    # pork belly strips seared on top
    for i in range(4):
        x = CX - 120 + i * 80
        b += f'<g transform="rotate(-12 {x} {CY})"><rect x="{x-26}" y="{CY-150}" width="52" height="300" rx="14" fill="#b86a4a" opacity="0.8"/><rect x="{x-8}" y="{CY-150}" width="12" height="300" fill="#f2d2c0" opacity="0.7"/></g>'
    # sauce layer
    b += blob(CX, CY, 175, "#5a2410", rnd, n=12, jitter=0.06)
    b += f'<ellipse cx="{CX-60}" cy="{CY-80}" rx="60" ry="16" fill="#ffffff" opacity="0.15" transform="rotate(-20 {CX-60} {CY-80})"/>'
    # mayo lattice and toppings, clipped to the sauce circle
    top = ""
    for i in range(-3, 4):
        top += f'<path d="M{CX-170},{CY + i*48 - 60} L{CX+170},{CY + i*48 + 60}" stroke="#fffbe8" stroke-width="6" stroke-linecap="round" opacity="0.95"/>'
    top += toppings(rnd, CX, CY, 165, 160)
    b += f'<g clip-path="url(#okonomi)">{top}</g>'
    for _ in range(14):  # beni shoga
        x, y = CX + 120 + rnd.uniform(-22, 22), CY - 110 + rnd.uniform(-16, 16)
        b += f'<rect x="{x-8:.0f}" y="{y-2:.0f}" width="16" height="4" rx="2" fill="#e8305a" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    # two metal spatulas (hera)
    for (x, y, r) in [(640, 470, -30), (700, 420, -45)]:
        b += f'<g transform="rotate({r} {x} {y})"><rect x="{x-38}" y="{y-26}" width="76" height="52" rx="6" fill="#c9cdd2" stroke="#9aa0a6" stroke-width="2"/><rect x="{x+38}" y="{y-6}" width="90" height="12" rx="5" fill="#6b4a33"/></g>'
    return svg(b, defs=f'<clipPath id="okonomi"><circle cx="{CX}" cy="{CY}" r="178"/></clipPath>')


def yakisoba():
    rnd = random.Random(81)
    b = iron_plate()
    b += shadow(225)
    b += f'<ellipse cx="{CX}" cy="{CY}" rx="270" ry="200" fill="#ffffff" stroke="#e3e0da" stroke-width="3"/>'
    b += blob(CX, CY, 165, "#8a4a1e", rnd, n=12, jitter=0.1)
    for _ in range(80):  # sauce-coated noodles
        r = rnd.uniform(15, 160); a0 = rnd.uniform(0, 2 * math.pi); span = rnd.uniform(0.7, 1.7)
        pts = " ".join(f"{CX+(r+7*math.sin(k))*math.cos(a0+span*k/10)*1.1:.1f},{CY+(r+7*math.sin(k))*math.sin(a0+span*k/10)*0.85:.1f}" for k in range(11))
        b += f'<polyline points="{pts}" fill="none" stroke="{rnd.choice(["#a85f2a","#b8692e","#9a5424","#c47a3a"])}" stroke-width="5" stroke-linecap="round"/>'
    for _ in range(12):  # cabbage
        x, y = in_circle(rnd, 130)
        b += blob(x, y, rnd.uniform(14, 20), rnd.choice(["#cfe8a6", "#b9dc8a"]), rnd, n=6, jitter=0.35)
    for _ in range(8):  # pork
        x, y = in_circle(rnd, 120)
        b += blob(x, y, rnd.uniform(11, 15), "#8e4a2a", rnd, n=7, jitter=0.3, stroke="#6b3418")
    for _ in range(16):  # bean sprouts
        x, y = in_circle(rnd, 130)
        b += f'<path d="M{x-12:.0f},{y:.0f} q12,-6 24,0" stroke="#efe2b8" stroke-width="4" fill="none" stroke-linecap="round" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    b += toppings(rnd, CX, CY, 150, 110)
    for _ in range(14):  # beni shoga
        x, y = CX + 130 + rnd.uniform(-20, 20), CY - 60 + rnd.uniform(-14, 14)
        b += f'<rect x="{x-8:.0f}" y="{y-2:.0f}" width="16" height="4" rx="2" fill="#e8305a" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    # fried egg on top
    b += blob(CX - 40, CY - 20, 52, "#fffdf6", rnd, n=12, jitter=0.15, stroke="#e8c98a")
    b += f'<circle cx="{CX-40}" cy="{CY-22}" r="20" fill="#f6a313" stroke="#e48409" stroke-width="2"/><ellipse cx="{CX-46}" cy="{CY-28}" rx="7" ry="4" fill="#ffd27a"/>'
    b += chopsticks(690)
    return svg(b)


if __name__ == "__main__":
    for name, fn in [("butatama-okonomiyaki", okonomiyaki), ("sauce-yakisoba", yakisoba)]:
        (OUT_DIR / f"{name}.svg").write_text(fn())
        print(f"wrote {name}.svg")
