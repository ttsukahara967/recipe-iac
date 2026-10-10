"""Budget set-meal (teishoku) series, plus the shishamo set meal. Run with `python3 tools/recipe_art/budget_teishoku.py`.

All images share the same tray, rice, miso soup and pickles; only the main plate changes.
"""

import math
import random
from pathlib import Path

from helpers import *  # noqa: F403  (drawing helpers and canvas constants)

OUT_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "images"
PX, PY = 400, 190  # main plate center


def plate():
    return f'<ellipse cx="{PX}" cy="{PY}" rx="260" ry="118" fill="#ffffff" stroke="#e3e0da" stroke-width="3"/>'


def cabbage(rnd, cx=PX + 140, cy=PY, rx=75, ry=62, tomatoes=True):
    s = ""
    for _ in range(150):
        x, y = cx + rnd.uniform(-rx, rx), cy + rnd.uniform(-ry, ry)
        if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 > 1:
            continue
        s += f'<path d="M{x:.0f},{y:.0f} l{rnd.uniform(-14,14):.0f},{rnd.uniform(-4,4):.0f}" stroke="{rnd.choice(["#d9edb4","#c5e39a","#eaf5d6"])}" stroke-width="3" stroke-linecap="round"/>'
    if tomatoes:
        s += f'<circle cx="{cx+65}" cy="{cy-55}" r="17" fill="#e53935"/><circle cx="{cx+60}" cy="{cy-60}" r="4" fill="#ff8a80"/>'
    return s


def in_ellipse(rnd, cx, cy, rx, ry):
    while True:
        x, y = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
        if x * x + y * y < 1:
            return cx + x * rx, cy + y * ry


def scene(main, seed):
    rnd = random.Random(seed)
    b = wood("#cfa978", "#a9824f") + tray() + plate()
    b += main(rnd)
    b += rice_bowl(165, 430, rnd) + miso_bowl(395, 435, rnd) + takuan_dish() + tray_chopsticks()
    return svg(b)


def moyashi(rnd):
    s = blob(PX, PY, 150, "#f3ead0", rnd, n=12, jitter=0.1)
    s = f'<g transform="translate(0,0) scale(1,0.72) translate(0,{PY*0.39:.0f})">{s}</g>'
    for _ in range(90):
        x, y = in_ellipse(rnd, PX, PY, 175, 80)
        a = rnd.uniform(0, 180)
        s += f'<g transform="rotate({a:.0f} {x:.0f} {y:.0f})"><path d="M{x-16:.0f},{y:.0f} q16,-7 32,0" stroke="#fdfbf0" stroke-width="5" fill="none" stroke-linecap="round"/><circle cx="{x-16:.0f}" cy="{y:.0f}" r="3.2" fill="#f2e3a0"/></g>'
    for _ in range(12):
        x, y = in_ellipse(rnd, PX, PY, 160, 70)
        s += blob(x, y, rnd.uniform(10, 14), "#d9a98a", rnd, n=7, jitter=0.3, stroke="#b9876a")
    for _ in range(14):
        x, y = in_ellipse(rnd, PX, PY, 160, 70)
        s += f'<rect x="{x-14:.0f}" y="{y-2.5:.0f}" width="28" height="5" rx="2" fill="{rnd.choice(["#2f8a32","#3f9a3a"])}" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    for _ in range(8):
        x, y = in_ellipse(rnd, PX, PY, 160, 70)
        s += f'<rect x="{x-10:.0f}" y="{y-2:.0f}" width="20" height="4" rx="2" fill="#ef7d2d" transform="rotate({rnd.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>'
    return s


def shogayaki(rnd):
    s = cabbage(rnd)
    for i in range(6):
        x = PX - 190 + i * 34
        y = PY - 10 + (i % 2) * 18
        s += f'<g transform="rotate({-15 + i*6} {x+40} {y})"><path d="M{x},{y} q40,-34 90,-6 q-10,40 -90,30 z" fill="#9c5a2c" stroke="#7a3f1c" stroke-width="2"/><path d="M{x+10},{y+4} q34,-20 70,-4" stroke="#e7b48a" stroke-width="3" fill="none"/></g>'
    for _ in range(6):
        x, y = in_ellipse(rnd, PX - 90, PY, 90, 55)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="10" ry="3.5" fill="#ffffff" opacity="0.35" transform="rotate(-25 {x:.0f} {y:.0f})"/>'
    s += blob(PX - 40, PY + 50, 14, "#f7d08a", rnd, n=7, jitter=0.2)  # grated ginger
    return s


def tofu_steak(rnd):
    s = cabbage(rnd)
    for (x, y, r) in [(PX - 150, PY - 5, -8), (PX - 50, PY + 10, 6)]:
        s += f'<g transform="rotate({r} {x} {y})"><rect x="{x-48}" y="{y-34}" width="96" height="68" rx="10" fill="#e3a54a"/><rect x="{x-42}" y="{y-28}" width="84" height="56" rx="8" fill="#f0c374"/><rect x="{x-42}" y="{y-28}" width="84" height="22" rx="8" fill="#8a4a22" opacity="0.85"/></g>'
    for _ in range(18):
        x, y = in_ellipse(rnd, PX - 100, PY, 100, 40)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4" fill="#b5e08a" stroke="#4f9a3a" stroke-width="1.2"/>'
    for _ in range(18):
        x, y = in_ellipse(rnd, PX - 100, PY - 10, 100, 30)
        s += f'<path d="M{x:.0f},{y:.0f} q5,-4 10,0" stroke="#c98d5e" stroke-width="2.5" fill="none"/>'
    return s


def chikuwa(rnd):
    s = cabbage(rnd)
    for i in range(7):
        x = PX - 200 + (i % 4) * 52
        y = PY - 35 + (i // 4) * 62 + (i % 2) * 8
        s += f'<g transform="rotate({rnd.uniform(-30,30):.0f} {x} {y})"><rect x="{x-30}" y="{y-16}" width="60" height="32" rx="14" fill="#e3b45a"/>'
        for _ in range(10):
            s += f'<circle cx="{x+rnd.uniform(-24,24):.0f}" cy="{y+rnd.uniform(-11,11):.0f}" r="2" fill="#2f7d32"/>'
        s += f'<ellipse cx="{x+30}" cy="{y}" rx="8" ry="14" fill="#f6e3c0"/><ellipse cx="{x+30}" cy="{y}" rx="4" ry="8" fill="#c9a06a"/></g>'
    s += f'<path d="M{PX+30},{PY+60} a18,18 0 1,1 0.1,0 z" fill="#f4e04d" stroke="#d9c22a" stroke-width="2"/>'  # lemon wedge-ish
    return s


def wiener(rnd):
    s = blob(PX, PY, 150, "#f6e9cf", rnd, n=12, jitter=0.1)
    s = f'<g transform="scale(1,0.72) translate(0,{PY*0.39:.0f})">{s}</g>'
    for _ in range(18):
        x, y = in_ellipse(rnd, PX, PY, 170, 75)
        s += blob(x, y, rnd.uniform(16, 22), rnd.choice(["#cfe8a6", "#e3f2c6", "#b9dc8a"]), rnd, n=6, jitter=0.35, stroke="#9cc66a")
    for _ in range(10):
        x, y = in_ellipse(rnd, PX, PY, 160, 65)
        a = rnd.uniform(0, 180)
        s += f'<g transform="rotate({a:.0f} {x:.0f} {y:.0f})"><rect x="{x-24:.0f}" y="{y-10:.0f}" width="48" height="20" rx="10" fill="#c9503a" stroke="#9c3322" stroke-width="2"/>'
        s += "".join(f'<path d="M{x-12+k*10:.0f},{y-9:.0f} l-4,18" stroke="#9c3322" stroke-width="2"/>' for k in range(3)) + '</g>'
    for _ in range(10):
        x, y = in_ellipse(rnd, PX, PY, 150, 60)
        s += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="14" ry="6" fill="#d63a2a" opacity="0.55"/>'
    return s


def atsuage(rnd):
    s = cabbage(rnd)
    for (x, y) in [(PX - 170, PY - 20), (PX - 95, PY - 25), (PX - 160, PY + 40), (PX - 85, PY + 35)]:
        s += f'<rect x="{x-32}" y="{y-28}" width="64" height="56" rx="8" fill="#c98a3a"/><rect x="{x-27}" y="{y-23}" width="54" height="46" rx="6" fill="#f4ead2"/>'
        s += blob(x, y - 4, 22, "#7a3e1c", rnd, n=8, jitter=0.25)
        for _ in range(8):
            s += f'<circle cx="{x+rnd.uniform(-16,16):.0f}" cy="{y-4+rnd.uniform(-14,14):.0f}" r="3" fill="#8e4a22"/>'
    for _ in range(16):
        x, y = in_ellipse(rnd, PX - 128, PY + 5, 70, 60)
        s += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3.5" fill="#b5e08a" stroke="#4f9a3a" stroke-width="1.2"/>'
    return s


def tamagoyaki(rnd):
    s = ""
    for i in range(4):
        x0 = PX - 200 + i * 62
        y0 = PY - 50
        s += f'<rect x="{x0}" y="{y0}" width="56" height="100" rx="12" fill="#f2c94c" stroke="#e0ad2e" stroke-width="3"/>'
        for k in range(1, 5):
            s += f'<path d="M{x0+6},{y0+k*20} q22,{rnd.uniform(-4,4):.0f} 44,0" stroke="#fbe38e" stroke-width="3" fill="none"/>'
    s += leaf(PX + 60, PY + 30, 70, "#3f8f3a", -70, vein="#6fb35a88")
    s += blob(PX + 90, PY - 10, 26, "#fbfbf6", rnd, n=10, jitter=0.18, stroke="#e8e8df")  # grated daikon
    # hiyayakko in a small indigo bowl
    s += f'<circle cx="{PX+175}" cy="{PY+5}" r="62" fill="#2c4d7a"/><circle cx="{PX+175}" cy="{PY+5}" r="54" fill="#f4f1ea"/>'
    s += f'<rect x="{PX+138}" y="{PY-30}" width="74" height="70" rx="8" fill="#fdfaf1" stroke="#e5dcc4" stroke-width="2"/>'
    s += blob(PX + 175, PY - 8, 12, "#f7d08a", rnd, n=7, jitter=0.2)
    for _ in range(10):
        s += f'<circle cx="{PX+175+rnd.uniform(-25,25):.0f}" cy="{PY+5+rnd.uniform(-22,22):.0f}" r="3.5" fill="#b5e08a" stroke="#4f9a3a" stroke-width="1.2"/>'
    for _ in range(12):
        s += f'<path d="M{PX+160+rnd.uniform(0,30):.0f},{PY+rnd.uniform(-10,25):.0f} q5,-4 10,0" stroke="#c98d5e" stroke-width="2.5" fill="none"/>'
    return s


def shishamo(rnd):
    s = ""
    for i in range(5):
        x = PX - 175 + i * 52
        y = PY - 45 + i * 20
        s += f'<g transform="rotate(-22 {x} {y})">'
        # body: silver back, golden grilled belly bulging with roe
        s += f'<path d="M{x-62},{y} Q{x-20},{y-18} {x+36},{y-6} L{x+58},{y-14} L{x+54},{y} L{x+58},{y+14} L{x+36},{y+6} Q{x-20},{y+22} {x-62},{y} Z" fill="#c9a26a" stroke="#8a6a3a" stroke-width="2"/>'
        s += f'<path d="M{x-58},{y-3} Q{x-20},{y-14} {x+34},{y-4}" stroke="#7d8790" stroke-width="5" fill="none" stroke-linecap="round"/>'
        s += f'<path d="M{x-40},{y+6} Q{x-10},{y+16} {x+20},{y+6}" stroke="#f2c46a" stroke-width="6" fill="none" stroke-linecap="round"/>'
        s += f'<circle cx="{x-50}" cy="{y-3}" r="4" fill="#2b2b2b"/><circle cx="{x-51}" cy="{y-4}" r="1.3" fill="#ffffff"/>'
        for k in range(3):
            s += f'<rect x="{x-30+k*20}" y="{y-9}" width="9" height="5" rx="2" fill="#4a3020" opacity="0.65"/>'
        s += '</g>'
    s += blob(PX + 150, PY + 30, 34, "#fbfbf6", rnd, n=10, jitter=0.18, stroke="#e8e8df")
    s += f'<path d="M{PX+170},{PY-60} a28,28 0 0,1 40,40 z" fill="#f4e04d" stroke="#d9c22a" stroke-width="2"/>'
    s += f'<path d="M{PX+176},{PY-48} l22,22" stroke="#fbf3a0" stroke-width="3"/>'
    return s


SERIES = [
    ("moyashi-itame-teishoku", moyashi),
    ("pork-shogayaki-teishoku", shogayaki),
    ("tofu-steak-teishoku", tofu_steak),
    ("chikuwa-isobeyaki-teishoku", chikuwa),
    ("wiener-cabbage-teishoku", wiener),
    ("atsuage-nikumiso-teishoku", atsuage),
    ("tamagoyaki-hiyayakko-teishoku", tamagoyaki),
    ("shishamo-teishoku", shishamo),
]

if __name__ == "__main__":
    for i, (name, fn) in enumerate(SERIES):
        (OUT_DIR / f"{name}.svg").write_text(scene(fn, 70 + i))
        print(f"wrote {name}.svg")
