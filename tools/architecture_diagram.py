"""Draws docs/architecture.svg. Run with `python3 tools/architecture_diagram.py`."""

from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "docs" / "architecture.svg"
W, H = 1180, 660
FONT = "font-family=\"-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif\""

parts = []


def add(s):
    parts.append(s)


def group(x, y, w, h, title, stroke, fill, dash=False):
    d = ' stroke-dasharray="8 6"' if dash else ""
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"{d}/>')
    add(f'<text x="{x+16}" y="{y+26}" font-size="15" font-weight="700" fill="{stroke}">{escape(title)}</text>')


def box(x, y, w, h, title, sub="", color="#232f3e", fill="#ffffff"):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{color}" stroke-width="2"/>')
    ty = y + h / 2 + (5 if not sub else -4)
    add(f'<text x="{x+w/2}" y="{ty}" font-size="15" font-weight="700" fill="{color}" text-anchor="middle">{escape(title)}</text>')
    if sub:
        add(f'<text x="{x+w/2}" y="{ty+19}" font-size="12" fill="#555" text-anchor="middle">{escape(sub)}</text>')


def arrow(x1, y1, x2, y2, label="", lx=None, ly=None, color="#444"):
    add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#arrow)"/>')
    if label:
        lx = (x1 + x2) / 2 if lx is None else lx
        ly = (y1 + y2) / 2 - 8 if ly is None else ly
        add(f'<text x="{lx}" y="{ly}" font-size="12" fill="#333" text-anchor="middle">{escape(label)}</text>')


add(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
add(f'<text x="24" y="38" font-size="22" font-weight="800" fill="#232f3e">おうちレシピ帖 — architecture (develop)</text>')

# Browser
box(16, 256, 144, 78, "Browser", "develop.ouchirecipes.com", color="#333")

# Frontend: SST
group(176, 64, 330, 470, "Frontend — SST (frontend/sst.config.ts)", "#8c4fff", "#f6f1ff")
box(196, 100, 290, 56, "Route 53 + ACM (us-east-1)", "site domain & certificate", color="#8c4fff")
box(196, 250, 290, 90, "CloudFront", "CloudFront Function routes requests", color="#8c4fff")
box(196, 410, 130, 100, "S3", "images, JS / CSS", color="#3f8624")
box(346, 410, 140, 100, "Lambda", "Next.js SSR (OpenNext)", color="#d86613")

# Backend: Terraform
group(540, 64, 616, 470, "Backend — Terraform (infra/stack)", "#5c4ee5", "#f3f2ff")
box(560, 100, 180, 56, "Route 53 + ACM", "api.develop… record & cert", color="#5c4ee5")
box(760, 100, 180, 56, "Secrets Manager", "DB password", color="#dd344c")
box(960, 100, 176, 56, "CloudWatch Logs", "ECS task logs", color="#e7157b")
group(560, 176, 576, 342, "VPC 10.10.0.0/16 (no NAT Gateway)", "#248814", "#f4fbf2", dash=True)
group(576, 214, 372, 290, "public subnets", "#248814", "#ffffff", dash=True)
box(596, 260, 150, 90, "ALB", "HTTPS :443", color="#8c4fff")
box(772, 260, 160, 90, "ECS Fargate", "FastAPI (arm64)", color="#d86613")
group(964, 214, 156, 290, "private subnets", "#248814", "#ffffff", dash=True)
box(978, 260, 128, 90, "Aurora", "PostgreSQL", color="#3b48cc")
add('<text x="1042" y="372" font-size="11" fill="#555" text-anchor="middle">Serverless v2</text>')
add('<text x="1042" y="388" font-size="11" fill="#555" text-anchor="middle">auto-pause when idle</text>')

# Bootstrap (account-wide)
group(176, 556, 980, 84, "Account-wide — Terraform (infra/bootstrap)", "#7a7a7a", "#fafafa")
box(196, 586, 220, 44, "S3", "Terraform state", color="#3f8624")
box(772, 586, 160, 44, "ECR", "API image", color="#d86613")

# Arrows
arrow(160, 295, 194, 295, "HTTPS", ly=286)
arrow(290, 340, 270, 408, "static", lx=258, ly=380)
arrow(390, 340, 410, 408, "pages", lx=420, ly=380)
arrow(486, 470, 594, 330, "SSR fetch (HTTPS)", lx=548, ly=392)
arrow(746, 305, 770, 305)
arrow(932, 305, 976, 305, ":5432", ly=296)
arrow(852, 158, 852, 258, "inject secret", lx=900, ly=196)
arrow(852, 584, 852, 352, "pull image", lx=900, ly=470)

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" {FONT}>'
       '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
       '<path d="M0,0 L10,5 L0,10 z" fill="#444"/></marker></defs>' + "".join(parts) + "</svg>")

if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg)
    print(f"wrote {OUT}")
