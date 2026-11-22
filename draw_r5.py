#!/usr/bin/env python3
# News 22 — ROUND 5, photo-lead revision of round 4 (one variable only).
# Same serif newspaper family, same layout, same 35 stories, same data as
# round 4 (spec v3 + spec v2 + §8 verification record). The ONLY change:
# the 3 lead scenes are real photographs (text-free, generated, 660x300)
# pasted into the 330x150 scene boxes, instead of PIL-drawn cartoons.
# All labels, headlines, tags and overlays are still drawn by PIL on top,
# exactly as round 4 does — so the comparison isolates one variable.
# Mediums (10) stay PIL-drawn, as in round 4. 35 stories, 7 regions.
# Zones (px): masthead 104, strip 84, region 32, clock 30, leads 270,
# mediums 250, map+briefs 170, DATE CHECK 84 = 1024.
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math, os, random, sys

W, H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# Round 5 lead photographs (text-free, generated): pasted into the 330x150
# lead scene boxes with ImageOps.fit (photos are 660x300, same 2.2:1
# aspect, so the fit does no cropping). The canvas `img` is a module
# global by the time the lead scene functions run, so the paste helper
# below can use it directly.
def _load_photo(name):
    return Image.open(os.path.join(HERE, "scenes", name)).convert("RGB")

PHOTO_COP31 = _load_photo("lead-cop31.png")
PHOTO_BARRAGE = _load_photo("lead-barrage.png")
PHOTO_BAHRAIN = _load_photo("lead-bahrain.png")

def _paste_photo(d, x, y, w, h, photo):
    img.paste(ImageOps.fit(photo, (w, h)), (x, y))

PAPER = (247, 242, 231)      # cream
PAPER2 = (238, 231, 214)     # slightly darker cream (strip)
INK = (30, 28, 26)
RED = (178, 34, 30)          # brick red
RED_D = (140, 25, 22)
GOLD = (198, 162, 78)
GREY = (110, 105, 95)
GREY_L = (200, 192, 176)
BLACK = (18, 16, 14)
WHITE = (252, 250, 246)

SF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SFB = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SFI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SSB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def tw(d, text, f):
    return d.textlength(text, font=f)

def assert_fit(d, text, f, max_w, what):
    w = tw(d, text, f)
    if w > max_w:
        print(f"OVERFLOW {what}: {w:.0f} > {max_w} :: {text!r}")
        sys.exit(2)

def fit_font(d, text, path, sizes, max_w):
    """Largest size from `sizes` whose single-line width fits max_w."""
    for s in sizes:
        f = font(path, s)
        if tw(d, text, f) <= max_w:
            return f, s
    f = font(path, sizes[-1])
    print(f"OVERFLOW fit_font: {tw(d, text, f):.0f} > {max_w} :: {text!r}")
    sys.exit(2)

def wrap_text(d, text, f, max_w):
    """Greedy word wrap to lines that each fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if tw(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def headline_lines(d, text, max_w, sizes=(30, 28, 26, 24)):
    """Largest size whose wrap is <= 2 lines. Returns (font, size, lines)."""
    for s in sizes:
        f = font(SFB, s)
        lines = wrap_text(d, text, f, max_w)
        if len(lines) <= 2:
            return f, s, lines
    f = font(SFB, sizes[-1])
    lines = wrap_text(d, text, f, max_w)
    print(f"OVERFLOW headline: {lines} :: {text!r}")
    sys.exit(2)

# ---------- drawing helpers (proven in r2/r3) ----------
def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)

def person(d, x, y, s, suit, skin=(214, 178, 142), hair=(40, 32, 24)):
    d.ellipse([x - 3.5 * s, y - 6 * s, x + 3.5 * s, y + 1 * s], fill=skin)
    d.pieslice([x - 4 * s, y - 7 * s, x + 4 * s, y - 1 * s], 180, 360, fill=hair)
    d.polygon([(x - 5 * s, y + 1 * s), (x + 5 * s, y + 1 * s),
               (x + 4 * s, y + 14 * s), (x - 4 * s, y + 14 * s)], fill=suit)
    d.polygon([(x - 5 * s, y + 1 * s), (x - 2 * s, y + 3 * s),
               (x, y + 1 * s), (x + 2 * s, y + 3 * s), (x + 5 * s, y + 1 * s)],
              fill=(250, 248, 244))
    d.polygon([(x - 1 * s, y + 2 * s), (x + 1 * s, y + 2 * s),
               (x, y + 6 * s)], fill=(150, 30, 28))

def car(d, x, y, w, h, body=(210, 60, 45)):
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=body)
    d.polygon([(x + w * 0.2, y), (x + w * 0.35, y - h * 0.55),
               (x + w * 0.65, y - h * 0.55), (x + w * 0.8, y)], fill=(40, 45, 60))
    d.ellipse([x + w * 0.12, y + h * 0.7, x + w * 0.3, y + h * 1.15], fill=(20, 20, 22))
    d.ellipse([x + w * 0.7, y + h * 0.7, x + w * 0.88, y + h * 1.15], fill=(20, 20, 22))

def flames(d, x, y, w, h, seed=0):
    rnd = random.Random(seed)
    for i in range(9):
        fx = x + rnd.random() * w
        fw = w * rnd.uniform(0.14, 0.3)
        fh = h * rnd.uniform(0.5, 1.0)
        col = rnd.choice([(240, 120, 30), (250, 170, 40), (230, 80, 20)])
        d.polygon([(fx - fw / 2, y), (fx, y - fh), (fx + fw / 2, y)], fill=col)

def smoke(d, x, y, n=5, seed=0, top=None):
    """Grey smoke puffs rising from (x, y). If top is given, no puff may
    cross above it (scenes must not paint over the card above)."""
    rnd = random.Random(seed)
    for i in range(n):
        r = 7 + rnd.random() * 9
        sx = x + (rnd.random() - 0.5) * 26
        sy = y - i * 9 - rnd.random() * 6
        if top is not None:
            sy = max(sy, top + r)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(110, 108, 105))

def glow(d, x, y, r, col=(250, 190, 80)):
    for k in range(3, 0, -1):
        rr = r * k / 3
        d.ellipse([x - rr, y - rr, x + rr, y + rr],
                  outline=col, width=2)

def moon(d, x, y, r=13):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(245, 240, 220))
    d.ellipse([x - r * 0.4, y - r * 0.3, x - r * 0.1, y], fill=(220, 212, 190))
    d.ellipse([x + r * 0.2, y + r * 0.2, x + r * 0.45, y + r * 0.45],
              fill=(220, 212, 190))

def stars(d, box, n=26, seed=1):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        sx = rnd.uniform(x0, x1)
        sy = rnd.uniform(y0, y1)
        r = rnd.choice([0.7, 1.0, 1.3])
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))

def sun(d, x, y, r=10):
    d.ellipse([x - r, y - r, x + r, y + r], fill=(250, 200, 60))
    for a in range(0, 360, 45):
        x2 = x + (r + 5) * math.cos(math.radians(a))
        y2 = y + (r + 5) * math.sin(math.radians(a))
        d.line([(x, y), (x2, y2)], fill=(250, 200, 60), width=2)

def tag_chip(d, x, y, text, bg=BLACK, fg=WHITE, size=10, pad=5):
    f = font(SSB, size)
    w = tw(d, text, f) + 2 * pad
    d.rectangle([x, y, x + w, y + size + 2 * pad - 2], fill=bg)
    d.text((x + pad, y + pad - 1), text, font=f, fill=fg)
    return w

# ---------- scenes (proven in r2/r3; COP31 changed for r4: deal near) ----------
def scene_cop31(d, x, y, w, h):
    # Round 5: real photograph — negotiation room, delegates, globe.
    _paste_photo(d, x, y, w, h, PHOTO_COP31)

def scene_bahrain(d, x, y, w, h):
    # Round 5: real photograph — aerial Gulf night, burning tankers + refinery.
    _paste_photo(d, x, y, w, h, PHOTO_BAHRAIN)

def scene_kryvyi(d, x, y, w, h):
    # Round 5: real photograph — night cityscape, fires, smoke, emergency lights.
    _paste_photo(d, x, y, w, h, PHOTO_BARRAGE)

def scene_sparta(d, x, y, w, h):
    # Sea, cargo ship with flames, rescue boats.
    vgrad(d, (x, y, x + w, y + h), (70, 110, 150), (25, 45, 75))
    sun(d, x + w * 0.82, y + h * 0.18, r=max(6, int(h * 0.08)))
    d.ellipse([x + w * 0.42, y + h * 0.62, x + w * 0.58, y + h * 0.68],
              fill=(240, 235, 225))
    d.ellipse([x + w * 0.55, y + h * 0.66, x + w * 0.68, y + h * 0.72],
              fill=(235, 230, 220))
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.85, y + h * 0.60],
                fill=(150, 45, 35))
    d.rectangle([x + w * 0.12, y + h * 0.28, x + w * 0.30, y + h * 0.42],
                fill=(240, 235, 225))
    d.rectangle([x + w * 0.60, y + h * 0.30, x + w * 0.72, y + h * 0.42],
                fill=(220, 215, 200))
    flames(d, x + w * 0.35, y + h * 0.42, w * 0.3, h * 0.22, seed=9)
    smoke(d, x + w * 0.48, y + h * 0.22, n=3, seed=10, top=y)
    for bx in (0.12, 0.72):
        d.polygon([(x + w * bx, y + h * 0.74), (x + w * (bx + 0.12), y + h * 0.74),
                   (x + w * (bx + 0.10), y + h * 0.82),
                   (x + w * (bx + 0.02), y + h * 0.82)], fill=(250, 140, 30))
        person(d, x + w * (bx + 0.06), y + h * 0.66, h / 44, (30, 60, 110))

def scene_hk(d, x, y, w, h):
    # Polling station: blue sky, ballot box, voters queue.
    vgrad(d, (x, y, x + w, y + h), (120, 160, 210), (210, 220, 235))
    d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(200, 195, 185))
    d.rectangle([x + w * 0.42, y + h * 0.38, x + w * 0.62, y + h * 0.66],
                fill=(40, 80, 150))
    d.rectangle([x + w * 0.46, y + h * 0.34, x + w * 0.58, y + h * 0.38],
                fill=(30, 60, 120))
    d.rectangle([x + w * 0.48, y + h * 0.30, x + w * 0.56, y + h * 0.34],
                fill=(250, 250, 250))
    for i, suit in enumerate([(30, 60, 110), (120, 30, 30), (40, 90, 50)]):
        person(d, x + w * (0.15 + 0.12 * i), y + h * 0.66, h / 44, suit)

def scene_cricket(d, x, y, w, h):
    # Guwahati oval: green outfield, pitch, batsman + bowler.
    vgrad(d, (x, y, x + w, y + h), (60, 130, 80), (30, 90, 50))
    d.ellipse([x, y + h * 0.50, x + w, y + h], fill=(70, 150, 85))
    d.rectangle([x + w * 0.42, y + h * 0.30, x + w * 0.58, y + h * 0.85],
                fill=(210, 185, 140))
    person(d, x + w * 0.50, y + h * 0.55, h / 34, (20, 40, 90))
    d.line([x + w * 0.53, y + h * 0.55, x + w * 0.62, y + h * 0.75],
           fill=(200, 170, 120), width=3)
    person(d, x + w * 0.80, y + h * 0.42, h / 34, (200, 200, 200))
    d.ellipse([x + w * 0.12, y + h * 0.30, x + w * 0.18, y + h * 0.36],
              fill=(250, 250, 250))

def scene_gaza(d, x, y, w, h):
    # Desert road, aid truck, dust.
    vgrad(d, (x, y, x + w, y + h), (215, 190, 150), (170, 140, 105))
    sun(d, x + w * 0.80, y + h * 0.18, r=max(6, int(h * 0.08)))
    d.rectangle([x, y + h * 0.70, x + w, y + h], fill=(150, 120, 85))
    d.rectangle([x + w * 0.10, y + h * 0.42, x + w * 0.55, y + h * 0.70],
                fill=(240, 240, 235))
    d.rectangle([x + w * 0.55, y + h * 0.50, x + w * 0.72, y + h * 0.70],
                fill=(200, 60, 40))
    d.ellipse([x + w * 0.18, y + h * 0.66, x + w * 0.30, y + h * 0.78],
              fill=(25, 25, 28))
    d.ellipse([x + w * 0.58, y + h * 0.66, x + w * 0.70, y + h * 0.78],
              fill=(25, 25, 28))
    smoke(d, x + w * 0.78, y + h * 0.40, n=3, seed=11, top=y)

def scene_nigeria(d, x, y, w, h):
    # River, capsized boat, rescue canoe.
    vgrad(d, (x, y, x + w, y + h), (90, 140, 180), (30, 70, 110))
    d.ellipse([x + w * 0.30, y + h * 0.55, x + w * 0.70, y + h * 0.75],
              fill=(70, 120, 160))
    d.polygon([(x + w * 0.18, y + h * 0.62), (x + w * 0.45, y + h * 0.62),
               (x + w * 0.40, y + h * 0.72), (x + w * 0.23, y + h * 0.72)],
              fill=(120, 70, 40))
    d.polygon([(x + w * 0.30, y + h * 0.62), (x + w * 0.32, y + h * 0.42),
               (x + w * 0.34, y + h * 0.62)], fill=(240, 235, 220))
    person(d, x + w * 0.62, y + h * 0.60, h / 36, (30, 60, 110))
    d.ellipse([x + w * 0.75, y + h * 0.68, x + w * 0.82, y + h * 0.72],
              fill=(250, 140, 30))

def scene_nvidia(d, x, y, w, h):
    # Office tower + falling chart.
    vgrad(d, (x, y, x + w, y + h), (200, 210, 225), (150, 165, 185))
    d.rectangle([x + w * 0.10, y + h * 0.30, x + w * 0.32, y + h * 0.95],
                fill=(60, 70, 85))
    for wy in range(4):
        for wx in range(2):
            d.rectangle([x + w * (0.13 + wx * 0.09), y + h * (0.36 + wy * 0.14),
                         x + w * (0.19 + wx * 0.09), y + h * (0.44 + wy * 0.14)],
                        fill=(180, 200, 220))
    pts = [(x + w * 0.42, y + h * 0.35), (x + w * 0.58, y + h * 0.45),
           (x + w * 0.72, y + h * 0.40), (x + w * 0.88, y + h * 0.70)]
    d.line(pts, fill=(200, 40, 30), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(200, 40, 30))
    d.polygon([(x + w * 0.82, y + h * 0.70), (x + w * 0.88, y + h * 0.70),
               (x + w * 0.85, y + h * 0.78)], fill=(200, 40, 30))

def scene_f1(d, x, y, w, h):
    # Night street circuit: neon, car, skyline.
    vgrad(d, (x, y, x + w, y + h), (30, 25, 55), (10, 10, 20))
    stars(d, (x + 4, y + 4, x + w - 4, y + h * 0.4), n=12, seed=12)
    for i, bh in enumerate([0.45, 0.60, 0.50]):
        bx = x + w * (0.08 + 0.30 * i)
        d.rectangle([bx, y + h * (0.75 - bh), bx + w * 0.16, y + h * 0.75],
                    fill=(50, 45, 70))
        for wy in range(3):
            d.rectangle([bx + w * 0.03, y + h * (0.75 - bh) + h * 0.05 + wy * h * 0.14,
                         bx + w * 0.13, y + h * (0.75 - bh) + h * 0.10 + wy * h * 0.14],
                        fill=(250, 210, 90))
    d.rectangle([x, y + h * 0.75, x + w, y + h], fill=(35, 35, 40))
    d.line([(x, y + h * 0.88), (x + w, y + h * 0.88)], fill=(250, 210, 90), width=2)
    car(d, x + w * 0.30, y + h * 0.78, w * 0.40, h * 0.10, body=(30, 60, 180))

def scene_sinaloa(d, x, y, w, h):
    # Desert highway, convoy, helicopter.
    vgrad(d, (x, y, x + w, y + h), (220, 195, 150), (170, 135, 95))
    sun(d, x + w * 0.80, y + h * 0.18, r=max(6, int(h * 0.08)))
    d.polygon([(x, y + h * 0.62), (x + w * 0.35, y + h * 0.30),
               (x + w * 0.65, y + h * 0.62)], fill=(140, 110, 80))
    d.polygon([(x + w * 0.55, y + h * 0.62), (x + w * 0.85, y + h * 0.38),
               (x + w, y + h * 0.62)], fill=(120, 95, 70))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(90, 75, 55))
    car(d, x + w * 0.12, y + h * 0.70, w * 0.24, h * 0.12, body=(40, 45, 55))
    car(d, x + w * 0.45, y + h * 0.70, w * 0.24, h * 0.12, body=(120, 30, 30))
    d.ellipse([x + w * 0.70, y + h * 0.18, x + w * 0.80, y + h * 0.24],
              fill=(60, 60, 65))
    d.line([x + w * 0.66, y + h * 0.21, x + w * 0.84, y + h * 0.21],
           fill=(60, 60, 65), width=2)

def scene_basra(d, x, y, w, h):
    # Power plant at dusk, flames, smoke.
    vgrad(d, (x, y, x + w, y + h), (90, 70, 60), (40, 30, 28))
    d.rectangle([x + w * 0.10, y + h * 0.35, x + w * 0.45, y + h * 0.85],
                fill=(70, 65, 60))
    for i in range(2):
        d.rectangle([x + w * (0.52 + 0.16 * i), y + h * 0.22,
                     x + w * (0.58 + 0.16 * i), y + h * 0.85],
                    fill=(85, 80, 75))
    flames(d, x + w * 0.15, y + h * 0.85, w * 0.5, h * 0.28, seed=13)
    smoke(d, x + w * 0.40, y + h * 0.30, n=4, seed=14, top=y)
    d.rectangle([x, y + h * 0.85, x + w, y + h], fill=(30, 28, 26))

def scene_hormuz(d, x, y, w, h):
    # Strait at dawn, two tankers, smoke column.
    vgrad(d, (x, y, x + w, y + h), (200, 170, 130), (120, 110, 100))
    sun(d, x + w * 0.50, y + h * 0.22, r=max(6, int(h * 0.09)))
    d.rectangle([x, y + h * 0.60, x + w, y + h], fill=(70, 95, 120))
    d.rectangle([x + w * 0.08, y + h * 0.42, x + w * 0.38, y + h * 0.60],
                fill=(140, 40, 35))
    d.rectangle([x + w * 0.55, y + h * 0.45, x + w * 0.85, y + h * 0.60],
                fill=(60, 60, 70))
    smoke(d, x + w * 0.22, y + h * 0.28, n=3, seed=15, top=y)
    d.ellipse([x + w * 0.42, y + h * 0.66, x + w * 0.50, y + h * 0.70],
              fill=(240, 235, 225))

# ---------- map polygons (lon/lat, coarse, proven in r2/r3) ----------
POLYS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-80, 73),
     (-65, 62), (-55, 52), (-65, 45), (-75, 35), (-80, 26), (-85, 30),
     (-95, 29), (-105, 22), (-115, 30), (-125, 40), (-125, 49), (-140, 60),
     (-155, 58), (-168, 66)],
    [(-170, 66), (-155, 71), (-135, 69), (-125, 71), (-140, 70), (-165, 68)],
    [(-10, 37), (-9, 43), (-2, 44), (0, 46), (3, 43), (8, 44), (12, 44),
     (15, 40), (19, 42), (23, 40), (28, 41), (30, 36), (26, 36), (23, 36),
     (19, 41), (15, 44), (10, 45), (5, 43), (-1, 38), (-6, 36), (-10, 37)],
    [(30, 36), (36, 36), (40, 40), (44, 39), (48, 38), (50, 30), (44, 29),
     (40, 31), (36, 33), (32, 31), (28, 36), (30, 36)],
    [(55, 26), (60, 25), (65, 25), (70, 20), (72, 21), (77, 8), (80, 7),
     (80, 13), (85, 20), (89, 22), (92, 21), (95, 16), (98, 16), (100, 13),
     (101, 8), (104, 2), (103, 1), (100, 8), (98, 10), (95, 15), (92, 21),
     (88, 22), (80, 15), (77, 10), (74, 20), (70, 22), (66, 25), (61, 25),
     (57, 26), (55, 26)],
    [(100, 15), (104, 9), (106, 10), (109, 13), (108, 18), (105, 20),
     (100, 15)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (129, -32), (132, -32),
     (135, -35), (138, -35), (140, -38), (145, -38), (150, -37), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (135, -15), (132, -11),
     (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
    [(129, 32), (132, 33), (135, 34), (137, 35), (139, 38), (141, 41),
     (140, 44), (137, 41), (134, 38), (131, 34), (129, 32)],
    [(95, 65), (105, 68), (115, 70), (125, 72), (135, 71), (145, 72),
     (155, 70), (165, 66), (175, 66), (178, 65), (170, 60), (160, 60),
     (150, 59), (140, 55), (130, 50), (120, 50), (110, 55), (100, 60),
     (95, 65)],
    [(95, 5), (100, 5), (104, 1), (105, -2), (102, -4), (98, -2), (95, 2),
     (95, 5)],
    [(-10, 15), (-17, 15), (-17, 21), (-12, 28), (-6, 35), (0, 36), (10, 37),
     (11, 34), (20, 32), (32, 31), (35, 28), (38, 22), (43, 12), (48, 11),
     (51, 12), (48, 15), (43, 15), (40, 10), (36, 5), (33, -1), (30, -5),
     (28, -10), (26, -15), (22, -18), (18, -20), (16, -25), (14, -30),
     (12, -32), (18, -34), (20, -30), (25, -33), (28, -32), (32, -28),
     (35, -25), (35, -20), (36, -15), (40, -12), (40, -5), (42, 0), (44, 5),
     (48, 10), (43, 12), (40, 18), (35, 22), (32, 28), (30, 31), (25, 32),
     (20, 35), (15, 37), (10, 37), (5, 35), (0, 30), (-5, 25), (-10, 20),
     (-10, 15)],
    [(-58, -34), (-65, -41), (-68, -50), (-70, -54), (-66, -55), (-62, -45),
     (-58, -40), (-52, -33), (-48, -28), (-41, -23), (-39, -15), (-35, -8),
     (-35, -5), (-40, -3), (-44, -3), (-50, 0), (-52, 4), (-58, 2), (-62, -5),
     (-65, -10), (-70, -18), (-72, -25), (-70, -30), (-65, -35), (-58, -34)],
    [(-70, 18), (-75, 20), (-80, 25), (-85, 28), (-90, 21), (-95, 19),
     (-97, 16), (-95, 15), (-90, 14), (-85, 12), (-80, 9), (-78, 7),
     (-75, 10), (-72, 12), (-70, 18)],
    [(-100, 20), (-105, 20), (-110, 24), (-105, 30), (-100, 32), (-95, 29),
     (-90, 21), (-95, 16), (-100, 20)],
    [(-75, 10), (-80, 8), (-83, 9), (-80, 2), (-77, 4), (-72, 11), (-70, 12),
     (-75, 10)],
    [(68, 75), (75, 72), (85, 68), (95, 70), (105, 72), (115, 74), (125, 72),
     (135, 70), (145, 72), (155, 70), (165, 68), (175, 65), (178, 64),
     (170, 60), (160, 60), (150, 58), (140, 55), (130, 52), (120, 50),
     (110, 55), (100, 60), (90, 62), (80, 68), (68, 75)],
    [(140, -45), (150, -42), (160, -45), (170, -42), (175, -45), (165, -48),
     (155, -48), (145, -46), (140, -45)],
]

PINS = [  # (lon, lat) — same coordinates as r2/r3, verified geographically
    (37.7, 36.9),    # 1 COP31 Antalya
    (33.4, 48.0),    # 2 Kryvyi Rih
    (50.6, 26.2),    # 3 Bahrain
    (9.5, 59.5),     # 4 Sparta II, Gulf of Finland
    (114.2, 22.3),   # 5 Hong Kong
    (91.7, 26.1),    # 6 Guwahati, India
    (34.5, 31.4),    # 7 Gaza
    (5.0, 13.0),     # 8 Sokoto, Nigeria
    (-74.0, 40.7),   # 9 New York (Nvidia)
    (-115.2, 36.2),  # 10 Las Vegas
    (-107.4, 24.8),  # 11 Sinaloa
    (47.8, 30.5),    # 12 Basra
    (56.3, 26.5),    # 13 Hormuz
]

# ---------- data (spec v2 + §8 verification record, binding) ----------
CLOCK = ("BY THE CLOCK — 01:58 BTC $60,112 · 05:30 Verstappen wins · "
         "06:00 COP31 approval · 16:30 Liverpool v Utd » · 17:00 ATP final »")

STRIP = [  # (number, label line 1, label line 2)
    ("~200", "NATIONS AT", "COP31 TALKS"),
    ("03:00", "GMT OBJECTION", "DEADLINE"),
    ("400+", "DRONES FIRED", "AT UKRAINE"),
    ("110", "MISSILES, SAME", "NIGHT"),
    ("2", "US BASES HIT", "IN BAHRAIN"),
    ("16", "CREW RESCUED", "FROM SPARTA II"),
]

REGIONS = [  # (label, count, color, width)
    ("EUROPE 9", 9, (40, 90, 160), 236),
    ("MIDDLE EAST 8", 8, (178, 50, 40), 208),
    ("ASIA-PACIFIC 7", 7, (200, 120, 30), 185),
    ("AMERICAS 6", 6, (40, 130, 70), 160),
    ("AFRICA 2", 2, (130, 90, 50), 72),
    ("OCEANIA 2", 2, (30, 130, 130), 72),
    ("WORLD 1", 1, (110, 70, 160), 75),
]

LEADS = [
    dict(num=1, scene=scene_cop31, source="REUTERS", status="ONGOING",
         dateline="ANTALYA, TÜRKIYE · CLIMATE",
         headline="COP31 nears a final deal",
         sub="Text tabled · no fossil-fuel line"),
    dict(num=2, scene=scene_kryvyi, source="AP", status="REPORTED",
         dateline="KRYVYI RIH, UKRAINE · WAR",
         headline="Russia's overnight drones kill two in Zelenskyy's home city",
         sub="148 drones, 3 missiles · 60 hurt"),
    dict(num=3, scene=scene_bahrain, source="AL JAZEERA", status="CLAIM · IRAN SAYS",
         dateline="MANAMA, BAHRAIN · IRAN WAR",
         headline="Iran strikes US bases in Bahrain",
         sub="2 Patriot radars hit, Iran claims"),
]

MEDIUMS = [
    dict(num=4, scene=scene_sparta, source="REUTERS", status="REPORTED",
         banner="SHIP ABLAZE", dateline="GULF OF FINLAND · WAR AT SEA",
         headline="Russian ship still burning off Finland",
         sub="16 rescued · tow promised"),
    dict(num=5, scene=scene_hk, source="AP", status="REPORTED",
         banner="VOTE", dateline="HONG KONG · CHINA VOTE",
         headline="Hong Kong votes for its Election Committee",
         sub="856 run for 723 seats"),
    dict(num=6, scene=scene_cricket, source="BBC", status="REPORTED",
         banner="RECORD", dateline="GUWAHATI, INDIA · TEST",
         headline="India post record Test total in NZ",
         sub="Pant 128 · Rahul 136"),
    dict(num=7, scene=scene_gaza, source="AFP", status="CLAIM",
         banner="STRIKE", dateline="GAZA · AID",
         headline="Strike hits food aid vehicle",
         sub="3 killed in air attack"),
    dict(num=8, scene=scene_nigeria, source="AP", status="REPORTED",
         banner="SINKING", dateline="SOKOTO, NIGERIA · ACCIDENT",
         headline="Nigeria boat sinks, 24 dead",
         sub="24 rescued · toll rising"),
    dict(num=9, scene=scene_nvidia, source="BLOOMBERG", status="REPORTED",
         banner="PROBE", dateline="NEW YORK · MARKETS",
         headline="Nvidia faces US accounting probe",
         sub="$500bn wiped in a day"),
    dict(num=10, scene=scene_f1, source="SKY SPORTS", status="REPORTED",
         banner="F1 WIN", dateline="LAS VEGAS · F1",
         headline="Verstappen wins in Vegas",
         sub="Norris 2nd · Piastri 3rd"),
    dict(num=11, scene=scene_sinaloa, source="AP", status="REPORTED",
         banner="ARREST", dateline="SINALOA, MEXICO · CARTEL",
         headline="'El Chapo Isidro' captured",
         sub="11 killed in Guasave raid"),
    dict(num=12, scene=scene_basra, source="AP", status="REPORTED",
         banner="FIRE", dateline="BASRA, IRAQ · ENERGY",
         headline="Basra power plant fire kills four",
         sub="35 hurt · pipeline blaze"),
    dict(num=13, scene=scene_hormuz, source="AP", status="CLAIM",
         banner="TANKERS HIT", dateline="STRAIT OF HORMUZ · TANKERS",
         headline="Two tankers hit near Hormuz",
         sub="No casualties reported"),
]

BRIEFS = [  # (num, text, source, day tag) — verbatim from spec v2 / r3, §8 KEPT
    (14, "Estonia shuts Russia border", "Reuters", "FRI"),
    (15, "Bolsonaro in ICU, stable in Brasília", "AP", "SAT"),
    (16, "Modi opens 9.76 km Nitish Setu bridge", "PIB", "SAT"),
    (17, "UNIFIL gap: France offers troops", "WaPo", "FRI"),
    (18, "France 45–17 Argentina, into final", "Reuters", "SAT"),
    (19, "Iran power rationing, 2 hrs/day", "RFE/RL", "SUN"),
    (20, "Bitcoin back above $60,000", "Reuters", "SUN"),
    (21, "Eisenkot invites Likud to talks", "Fr24", "SUN"),
    (22, "Marles hits back on AUKUS row", "Reuters", "SUN"),
    (23, "Akvan: 14 flights axed at Ranchi", "IMD", "FRI"),
    (24, "Kerch Bridge arch down 227 m", "BBC", "MON–TUE"),
    (25, "EU–Indonesia deal signed", "Reuters", "SAT"),
    (26, "Denmark expels Russian attaché", "WSJ", "FRI"),
    (27, "50+ homes torched in Narail", "bdnews24", "FRI"),
    (28, "Nepal PM Shah lands in Delhi", "MOFA", "SUN"),
    (29, "FBI probes hack of its crime database", "CNN", "SAT"),
    (30, "Teen gamer helps FBI rescue a girl", "BBC", "SUN"),
    (31, "Saudi downs 3 Houthi missiles", "Reuters", "SAT"),
    (32, "Lisbon march over living costs", "Reuters", "SAT"),
    (33, "Fred Nile dies aged 92", "ABC", "SUN"),
    (34, "70 yrs since Melbourne 1956 Games", "ABC", "SUN"),
    (35, "Sudan landmine kills 22", "Darfur24", "SUN"),
]
assert len(BRIEFS) == 22 and BRIEFS[0][0] == 14 and BRIEFS[-1][0] == 35

DATE_CHECK_BODY = (
    "Wires read up to 07:10 UTC, Sun 22 Nov 2026: every story here happened, "
    "or was first reported, on 22 November in at least one time zone. "
    "Sparta II burned late Saturday; Bahrain's aftermath still developing Sunday. "
    "Left out: Peru quake (Fri 20 Nov), Kerch Bridge strikes, Shenzhen summit "
    "(Thu 19 Nov), Oreshnik strike (Wed 18 Nov). "
    "Not yet happened: COP31 approval, Liverpool, the ATP champion."
)

DATE_CHECK_FOOTER = (
    "Sources: Reuters, BBC, Al Jazeera, AP, AFP, Guardian · Labels: REPORTED = "
    "confirmed · CLAIM = one side's claim · FORECAST = scheduled · ONE PAGE"
)

# ---------- canvas ----------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 8
RIGHT = W - MX  # 1016

# ---------- 1. MASTHEAD (0–104) ----------
d.text((MX, 5), "THE WORLD IN ONE DAY", font=font(SFB, 15), fill=RED)
rk = "35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
assert_fit(d, rk, font(SFB, 13), RIGHT - MX, "masthead kicker right")
d.text((RIGHT - tw(d, rk, font(SFB, 13)), 6), rk, font=font(SFB, 13), fill=GREY)
title = "Sunday 22 November 2026"
tf = font(SFB, 54)
assert_fit(d, title, tf, RIGHT - MX, "masthead title")
d.text(((W - tw(d, title, tf)) / 2, 22), title, font=tf, fill=INK)
deck = ("COP31 nears a deal in Antalya · Iran strikes US bases in Bahrain · "
        "Russia's drones kill two in Kryvyi Rih")
df, dsize = fit_font(d, deck, SFI, [22, 20, 18, 16], RIGHT - MX)
d.text(((W - tw(d, deck, df)) / 2, 80), deck, font=df, fill=RED_D)
d.line([(MX, 102), (RIGHT, 102)], fill=INK, width=2)

# ---------- 2. STRIP (104–188) ----------
d.rectangle([MX, 104, RIGHT, 188], fill=PAPER2)
d.line([(MX, 104), (RIGHT, 104)], fill=INK, width=1)
d.line([(MX, 188), (RIGHT, 188)], fill=INK, width=1)
cell_w = (RIGHT - MX) / 6
for i, (num, l1, l2) in enumerate(STRIP):
    cx = MX + i * cell_w
    nf = font(SFB, 52)
    assert_fit(d, num, nf, cell_w - 8, f"strip num {num}")
    d.text((cx + (cell_w - tw(d, num, nf)) / 2, 108), num, font=nf, fill=INK)
    lf = font(SFB, 12)
    for j, lab in enumerate((l1, l2)):
        assert_fit(d, lab, lf, cell_w - 8, f"strip label {lab}")
        d.text((cx + (cell_w - tw(d, lab, lf)) / 2, 164 + j * 13), lab,
               font=lf, fill=GREY)
    if i:
        d.line([(cx, 112), (cx, 180)], fill=GREY_L, width=1)

# ---------- 3. REGION BAR (188–220) ----------
rx = MX
for label, count, color, wseg in REGIONS:
    d.rectangle([rx, 188, rx + wseg, 220], fill=color)
    rf = font(SSB, 13)
    if tw(d, label, rf) > wseg - 6:
        rf = font(SSB, 12)
    assert_fit(d, label, rf, wseg - 4, f"region {label}")
    d.text((rx + (wseg - tw(d, label, rf)) / 2, 197), label, font=rf, fill=WHITE)
    rx += wseg
assert rx == RIGHT, f"region bar width {rx} != {RIGHT}"

# ---------- 4. CLOCK (220–250) ----------
d.rectangle([MX, 220, RIGHT, 250], fill=BLACK)
cf, csize = fit_font(d, CLOCK, SFB, [16, 15, 14], RIGHT - MX - 16)
d.text((MX + 8, 229), CLOCK, font=cf, fill=GOLD)

# ---------- 5. LEADS (250–520) ----------
lead_w, lead_gap = 330, 9
for i, L in enumerate(LEADS):
    x = MX + i * (lead_w + lead_gap)
    y = 250
    # red tag band
    d.rectangle([x, y, x + lead_w, y + 20], fill=RED)
    bf = font(SSB, 12)
    d.text((x + 8, y + 4), f"{L['num']} · LEAD", font=bf, fill=WHITE)
    sf = font(SSB, 11)
    st = L["status"]
    assert_fit(d, st, sf, lead_w - 90, f"lead status {st}")
    d.text((x + lead_w - tw(d, st, sf) - 8, y + 5), st, font=sf, fill=WHITE)
    # scene 150px
    L["scene"](d, x, y + 20, lead_w, 150)
    d.rectangle([x, y + 20, x + lead_w, y + 170], outline=INK, width=1)
    tag_chip(d, x + 6, y + 20 + 150 - 22, L["source"], size=10)
    # dateline
    dy = y + 174
    df2 = font(SFB, 13)
    assert_fit(d, L["dateline"], df2, lead_w - 4, f"lead dateline {L['num']}")
    d.text((x + 2, dy), L["dateline"], font=df2, fill=RED)
    # headline (serif bold, <=2 lines)
    hf, hsize, hlines = headline_lines(d, L["headline"], lead_w - 4)
    hy = dy + 16
    for ln in hlines:
        d.text((x + 2, hy), ln, font=hf, fill=INK)
        hy += hsize + 1
    # sub (1 line, serif 16)
    subf = font(SF, 16)
    assert_fit(d, L["sub"], subf, lead_w - 4, f"lead sub {L['num']}")
    sy = hy
    d.text((x + 2, sy), L["sub"], font=subf, fill=GREY)
    assert sy + 17 <= y + 270, f"lead {L['num']} overflows card: {sy + 17} > {y + 270}"

# ---------- 6. MEDIUMS (520–770) ----------
med_w, med_gap = 196, 6
med_h = 125
for idx, M in enumerate(MEDIUMS):
    col, row = idx % 5, idx // 5
    x = MX + 2 + col * (med_w + med_gap)
    y = 520 + row * med_h
    # scene 56px (banner overlays its top edge)
    M["scene"](d, x, y, med_w, 56)
    d.rectangle([x, y, x + med_w, y + 56], outline=INK, width=1)
    # red banner tag (full width, over scene top)
    d.rectangle([x, y, x + med_w, y + 14], fill=RED)
    bf = font(SSB, 11)
    btxt = f"{M['num']} · {M['banner']}"
    assert_fit(d, btxt, bf, med_w - 60, f"medium banner {M['num']}")
    d.text((x + 5, y + 2), btxt, font=bf, fill=WHITE)
    sf = font(SSB, 10)
    st = M["status"]
    assert_fit(d, st, sf, 56, f"medium status {M['num']}")
    d.text((x + med_w - tw(d, st, sf) - 5, y + 3), st, font=sf, fill=WHITE)
    tag_chip(d, x + med_w - 62, y + 56 - 20, M["source"], size=9)
    # dateline
    dy = y + 57
    df3 = font(SFB, 10)
    assert_fit(d, M["dateline"], df3, med_w - 4, f"medium dateline {M['num']}")
    d.text((x + 2, dy), M["dateline"], font=df3, fill=RED)
    # headline (serif bold 20px, <=2 lines)
    hf, hsize, hlines = headline_lines(d, M["headline"], med_w - 4,
                                       sizes=(20, 19, 18))
    hy = dy + 10
    for ln in hlines:
        d.text((x + 2, hy), ln, font=hf, fill=INK)
        hy += hsize
    # sub (1 line, serif 14)
    subf = font(SF, 14)
    assert_fit(d, M["sub"], subf, med_w - 4, f"medium sub {M['num']}")
    sy = hy
    d.text((x + 2, sy), M["sub"], font=subf, fill=GREY)
    assert sy + 14 <= y + med_h, f"medium {M['num']} overflows: {sy + 14} > {y + med_h}"

# ---------- 7. MAP + BRIEFS (770–940) ----------
# map (left): light dotted world map on cream, red pins
map_x, map_y, map_w, map_h = MX, 786, 322, 112
d.text((MX, 772), "WHERE IT HAPPENED — PINS 1–13", font=font(SFB, 13), fill=INK)
d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(240, 234, 220),
            outline=INK, width=1)
def lonlat_to_xy(lon, lat):
    px = map_x + (lon + 180) / 360 * map_w
    py = map_y + (75 - lat) / 135 * map_h
    return px, py
for poly in POLYS:
    pts = [lonlat_to_xy(lon, lat) for lon, lat in poly]
    d.polygon(pts, fill=(175, 160, 130))
for i, (lon, lat) in enumerate(PINS, start=1):
    px, py = lonlat_to_xy(lon, lat)
    d.ellipse([px - 6, py - 6, px + 6, py + 6], fill=RED, outline=WHITE, width=1)
    nf = font(SSB, 8)
    d.text((px - tw(d, str(i), nf) / 2, py - 4), str(i), font=nf, fill=WHITE)
# pin index (3 lines, 9px serif)
idx_lines = [
    "1 COP31 · 2 Kryvyi Rih · 3 Bahrain · 4 Sparta II · 5 Hong Kong",
    "6 India · 7 Gaza · 8 Nigeria · 9 Nvidia · 10 Vegas",
    "11 Sinaloa · 12 Basra · 13 Hormuz",
]
for j, line in enumerate(idx_lines):
    assert_fit(d, line, font(SF, 9), map_w - 4, f"pin index {j}")
    d.text((map_x + 2, map_y + map_h + 4 + j * 11), line, font=font(SF, 9), fill=INK)

# briefs (right): 2 cols x 11 rows
d.text((340, 772), "ALSO ON — 22 BRIEFS", font=font(SFB, 13), fill=INK)
bf_font = font(SF, 11)
col_w = 338
for i, (num, text, src, tag) in enumerate(BRIEFS):
    col, row = i % 2, i // 2
    bx = 340 + col * col_w
    by = 788 + row * 14
    line = f"{num}  {text} ({src}, {tag})"
    assert_fit(d, line, bf_font, col_w - 8, f"brief {num}")
    d.text((bx, by), line, font=bf_font, fill=INK)

# ---------- 8. DATE CHECK (940–1024) ----------
d.rectangle([MX, 942, RIGHT, 1022], outline=RED, width=2)
d.text((MX + 8, 946), "DATE CHECK", font=font(SFB, 13), fill=RED)
body_font = font(SF, 13)
body_lines = wrap_text(d, DATE_CHECK_BODY, body_font, RIGHT - MX - 16)
assert len(body_lines) <= 3, f"DATE CHECK needs {len(body_lines)} lines: {body_lines}"
by = 962
for ln in body_lines:
    d.text((MX + 8, by), ln, font=body_font, fill=INK)
    by += 15
foot_font = font(SF, 10)
assert_fit(d, DATE_CHECK_FOOTER, foot_font, RIGHT - MX - 16, "DATE CHECK footer")
d.text((MX + 8, 1008), DATE_CHECK_FOOTER, font=foot_font, fill=GREY)

# ---------- save + report ----------
img.save(OUT)
print("saved", OUT)
print("DATE CHECK body chars:", len(DATE_CHECK_BODY),
      "lines:", len(body_lines))
print("DATE CHECK body:", DATE_CHECK_BODY)
print("region counts sum:", sum(c for _, c, _, _ in REGIONS),
      "stories:", 3 + len(MEDIUMS) + len(BRIEFS))
print("strip numbers:", [s[0] for s in STRIP])
print("lead headlines:", [L["headline"] for L in LEADS])
