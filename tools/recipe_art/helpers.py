"""Shared drawing helpers for the flat SVG recipe illustrations in frontend/public/images.

Every image is an 800x600 top-down scene: a background (cloth, wood, ...), a plate or bowl
centered at (CX, CY), and the food drawn as simple shapes. Randomness is seeded per image so
re-running a script reproduces the same picture.
"""

import math, random
W, H = 800, 600
CX, CY = 400, 310

def svg(body, defs=""):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><defs>{defs}<radialGradient id="shadow"><stop offset="0.7" stop-color="#000" stop-opacity="0.25"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>{body}</svg>'

def shadow(r):
    return f'<ellipse cx="{CX+14}" cy="{CY+22}" rx="{r+30}" ry="{r+26}" fill="url(#shadow)"/>'

def blob(cx, cy, r, color, rnd, n=9, jitter=0.18, stroke=None, rot=0):
    pts = []
    for i in range(n):
        a = 2*math.pi*i/n + rot
        rr = r*(1+rnd.uniform(-jitter, jitter))
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)*0.9))
    d = ""
    for i in range(n):
        p0 = pts[i]; p1 = pts[(i+1)%n]
        mx, my = (p0[0]+p1[0])/2, (p0[1]+p1[1])/2
        if i == 0:
            pm = pts[-1]; d += f"M{(pm[0]+p0[0])/2:.1f},{(pm[1]+p0[1])/2:.1f} "
        d += f"Q{p0[0]:.1f},{p0[1]:.1f} {mx:.1f},{my:.1f} "
    s = f' stroke="{stroke}" stroke-width="3"' if stroke else ""
    return f'<path d="{d}Z" fill="{color}"{s}/>'

def in_circle(rnd, r):
    while True:
        x, y = rnd.uniform(-r, r), rnd.uniform(-r, r)
        if x*x+y*y < r*r: return CX+x, CY+y

def leaf(x, y, size, color, angle, vein="#ffffff55"):
    return (f'<g transform="translate({x:.1f},{y:.1f}) rotate({angle:.0f})">'
            f'<path d="M0,0 Q{size*0.5},{-size*0.45} {size},0 Q{size*0.5},{size*0.45} 0,0Z" fill="{color}"/>'
            f'<path d="M2,0 L{size*0.9},0" stroke="{vein}" stroke-width="1.5"/></g>')

def cloth(c1, c2, size=50):
    s = f'<rect width="{W}" height="{H}" fill="{c1}"/>'
    for i in range(0, W, size*2):
        s += f'<rect x="{i}" y="0" width="{size}" height="{H}" fill="{c2}" opacity="0.5"/>'
    for j in range(0, H, size*2):
        s += f'<rect x="0" y="{j}" width="{W}" height="{size}" fill="{c2}" opacity="0.5"/>'
    return s

def wood(base, line):
    s = f'<rect width="{W}" height="{H}" fill="{base}"/>'
    for y in range(0, H, 60):
        s += f'<rect x="0" y="{y}" width="{W}" height="2" fill="{line}" opacity="0.5"/>'
        s += f'<path d="M0,{y+30} C200,{y+22} 400,{y+38} 800,{y+28}" stroke="{line}" stroke-width="1.2" fill="none" opacity="0.35"/>'
    return s

def chopsticks(x=690):
    return (f'<rect x="{x}" y="60" width="12" height="480" rx="5" fill="#8a5a36" transform="rotate(6 {x} 300)"/>'
            f'<rect x="{x+26}" y="60" width="12" height="480" rx="5" fill="#9c6a42" transform="rotate(6 {x+26} 300)"/>')

# Set-meal (teishoku) tray parts, shared by the set-meal series
def tray():
    return ('<rect x="38" y="38" width="724" height="524" rx="22" fill="#000" opacity="0.18"/>'
            '<rect x="30" y="30" width="724" height="524" rx="22" fill="#5a2a1a"/><rect x="44" y="44" width="696" height="496" rx="16" fill="#6e3420"/>')

def rice_bowl(x, y, rnd):
    s = f'<circle cx="{x}" cy="{y}" r="88" fill="#ffffff" stroke="#2c4d7a" stroke-width="6"/>'
    s += blob(x, y, 70, "#fdfcf7", rnd, n=10, jitter=0.08)
    for _ in range(70):
        a = rnd.uniform(0, 2*math.pi); r = rnd.uniform(0, 62)
        px, py = x + r*math.cos(a), y + r*math.sin(a)
        s += f'<ellipse cx="{px:.0f}" cy="{py:.0f}" rx="5" ry="3" fill="#ffffff" stroke="#e6e2d4" stroke-width="0.8" transform="rotate({rnd.uniform(0,180):.0f} {px:.0f} {py:.0f})"/>'
    return s

def miso_bowl(x, y, rnd):
    s = f'<circle cx="{x}" cy="{y}" r="82" fill="#1b1b1b"/><circle cx="{x}" cy="{y}" r="72" fill="#8e1f1f"/><circle cx="{x}" cy="{y}" r="66" fill="#c08a4a"/>'
    for _ in range(6):
        s += blob(x + rnd.uniform(-35, 35), y + rnd.uniform(-35, 35), 16, "#d4a564", rnd, n=7, jitter=0.4)
    for _ in range(5):
        px, py = x + rnd.uniform(-35, 35), y + rnd.uniform(-35, 35)
        s += f'<rect x="{px-9:.0f}" y="{py-9:.0f}" width="18" height="18" rx="3" fill="#fbf6e8"/>'
    for _ in range(5):
        s += blob(x + rnd.uniform(-38, 38), y + rnd.uniform(-38, 38), 11, "#2f5a2a", rnd, n=7, jitter=0.4)
    return s

def takuan_dish(x=560, y=470):
    s = f'<rect x="{x}" y="{y}" width="120" height="58" rx="12" fill="#efe9dc" stroke="#c9bfa8" stroke-width="2"/>'
    for i in range(3):
        s += f'<ellipse cx="{x+30+i*16}" cy="{y+29}" rx="16" ry="14" fill="#f5d33c" stroke="#e0b81e" stroke-width="2"/>'
    return s

def tray_chopsticks():
    return '<rect x="250" y="530" width="300" height="10" rx="5" fill="#8a5a36"/><rect x="250" y="544" width="300" height="10" rx="5" fill="#9c6a42"/>'
