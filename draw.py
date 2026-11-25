"""Draw the entry image for make.fun bounty news-image-20261124.

A newspaper front page summing up Tuesday 24 November 2026, drawn with
Pillow. Stories were verified against news reports of that day:
  - Huawei found guilty of trade-secret theft and bank fraud by a US jury
    (acquitted of racketeering)
  - Four tankers hit by mines in the Strait of Hormuz (IRGC statement)
  - Ukrainian naval drones hit Russian ships in the Gulf of Finland and
    off Libya
  - Nvidia reinstates Jensen Huang as CEO; shares swing
  - China launches Shenzhou 24 with the first Pakistani astronaut aboard
  - Senegal's 2025 Africa Cup of Nations title restored on appeal (CAS)
  - Also: Cartagena supermarket hostages, Houthis near Aden, US tariff
    threat, Nepal 5.6 quake, Trump honours Giuliani
Output: entry.png, 1024x1024, well under 1 MiB.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 246, 238)
NAVY = (15, 42, 74)
NAVY_LT = (28, 64, 104)
GOLD = (232, 184, 75)
RED = (178, 34, 34)
INK = (24, 24, 24)
GREY = (92, 92, 92)
WHITE = (255, 255, 255)
TEAL = (18, 110, 130)
SEA = (46, 111, 151)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def serif_b(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSerif-Bold.ttf", size)


def serif(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSerif.ttf", size)


def sans_b(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans-Bold.ttf", size)


def sans(size):
    return ImageFont.truetype(FONT_DIR + "DejaVuSans.ttf", size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, font, max_w, fill, leading=None):
    lines = wrap(draw, text, font, max_w)
    lh = leading or int(font.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y, len(lines)


def fit_text(draw, text, font_fn, max_w, max_lines, start_size):
    """Shrink font until text fits in max_lines at max_w. Returns (font, lines)."""
    size = start_size
    while size > 12:
        font = font_fn(size)
        lines = wrap(draw, text, font, max_w)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = font_fn(size)
    return font, wrap(draw, text, font, max_w)


def panel(draw, box, fill=WHITE, outline=(200, 192, 176), width=2):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


def kicker_headline_body(draw, x, y, w, kicker, kicker_color, headline,
                         headline_size, body, body_size, head_lines=2,
                         body_lines=3):
    draw.text((x, y), kicker, font=sans_b(15), fill=kicker_color)
    y += 22
    font, lines = fit_text(draw, headline, serif_b, w, head_lines, headline_size)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=INK)
        y += int(font.size * 1.12)
    y += 4
    font, lines = fit_text(draw, body, sans, w, body_lines, body_size)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=(60, 60, 60))
        y += int(font.size * 1.28)
    return y


# ---------- illustration helpers ----------

def illu_huawei(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(24, 52, 88))
    # gavel, fully visible on the left of the phone
    draw.line([(x0 + 58, y1 - 52), (x0 + 112, y0 + 88)], fill=(214, 164, 96), width=14)
    draw.rectangle([x0 + 20, y1 - 74, x0 + 70, y1 - 38], fill=(140, 96, 52))
    draw.rectangle([x0 + 104, y0 + 76, x0 + 124, y0 + 100], fill=(140, 96, 52))
    # phone with chip
    px0, py0, px1, py1 = x0 + 118, y0 + 22, x1 - 26, y1 - 24
    draw.rounded_rectangle([px0, py0, px1, py1], radius=14, fill=(16, 20, 28),
                           outline=(120, 140, 170), width=3)
    cx, cy = (px0 + px1) // 2, (py0 + py1) // 2 + 6
    draw.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(34, 110, 88),
                   outline=GOLD, width=3)
    for dx in (-46, -23, 0, 23, 46):
        draw.line([(cx + dx, cy - 46), (cx + dx, cy - 34)], fill=GOLD, width=3)
        draw.line([(cx + dx, cy + 34), (cx + dx, cy + 46)], fill=GOLD, width=3)
    draw.text((cx - 62, py0 + 12), "HUAWEI", font=sans_b(15), fill=(180, 200, 220))
    draw.text((cx - 62, py1 - 30), "GUILTY", font=sans_b(17), fill=GOLD)


def illu_tanker(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(126, 190, 214))
    draw.rectangle([x0, y0 + 78, x1, y1], fill=(24, 84, 122))
    # tanker hull + containers
    draw.polygon([(x0 + 28, y0 + 62), (x1 - 28, y0 + 62), (x1 - 52, y0 + 96),
                  (x0 + 52, y0 + 96)], fill=(40, 44, 52))
    for i, c in enumerate([(178, 52, 44), (232, 184, 75), (46, 120, 80)]):
        draw.rectangle([x0 + 52 + i * 52, y0 + 30, x0 + 98 + i * 52, y0 + 62],
                       fill=c, outline=(30, 30, 30), width=2)
    # mine: spiky black circle
    mx, my = x1 - 62, y0 + 34
    for a in range(0, 360, 30):
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        draw.line([(mx + dx * 10, my + dy * 10), (mx + dx * 20, my + dy * 20)],
                  fill=(20, 20, 20), width=4)
    draw.ellipse([mx - 11, my - 11, mx + 11, my + 11], fill=(20, 20, 20))
    # explosion burst
    ex, ey = x0 + 46, y0 + 30
    for a in range(0, 360, 45):
        import math
        dx, dy = math.cos(math.radians(a)), math.sin(math.radians(a))
        draw.line([(ex, ey), (ex + dx * 22, ey + dy * 22)], fill=(232, 120, 30),
                  width=5)
    draw.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], fill=(255, 200, 60))


def illu_drone_ship(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(150, 178, 196))
    draw.rectangle([x0, y0 + 82, x1, y1], fill=(38, 84, 116))
    # warship silhouette
    draw.polygon([(x0 + 24, y0 + 66), (x1 - 24, y0 + 66), (x1 - 48, y0 + 96),
                  (x0 + 48, y0 + 96)], fill=(52, 58, 66))
    draw.rectangle([x0 + 92, y0 + 40, x0 + 150, y0 + 66], fill=(52, 58, 66))
    draw.line([(x0 + 120, y0 + 40), (x0 + 120, y0 + 22)], fill=(52, 58, 66), width=4)
    # drone quadcopter
    dx, dy = x1 - 66, y0 + 32
    draw.ellipse([dx - 22, dy - 6, dx - 6, dy + 6], fill=(30, 30, 30))
    draw.ellipse([dx + 6, dy - 6, dx + 22, dy + 6], fill=(30, 30, 30))
    draw.rectangle([dx - 8, dy - 4, dx + 8, dy + 4], fill=(30, 30, 30))
    draw.line([(dx, dy + 4), (dx, dy + 14)], fill=(30, 30, 30), width=3)
    # burst on ship
    bx, by = x0 + 60, y0 + 52
    for a in range(0, 360, 45):
        import math
        ddx, ddy = math.cos(math.radians(a)), math.sin(math.radians(a))
        draw.line([(bx, by), (bx + ddx * 18, by + ddy * 18)], fill=(232, 120, 30),
                  width=4)
    draw.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=(255, 200, 60))


def illu_nvidia(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 66, 32))
    # chip
    cx, cy = (x0 + x1) // 2 - 30, (y0 + y1) // 2
    draw.rectangle([cx - 34, cy - 34, cx + 34, cy + 34], fill=(24, 24, 24),
                   outline=(118, 200, 90), width=3)
    for d in (-22, 0, 22):
        draw.line([(cx + d, cy - 46), (cx + d, cy - 34)], fill=(118, 200, 90), width=3)
        draw.line([(cx + d, cy + 34), (cx + d, cy + 46)], fill=(118, 200, 90), width=3)
    draw.text((cx - 20, cy - 12), "NV", font=sans_b(20), fill=(118, 200, 90))
    # rising chart arrow
    ax, ay = x0 + 168, y1 - 26
    pts = [(ax, ay), (ax + 26, ay - 26), (ax + 52, ay - 14), (ax + 78, ay - 44),
           (ax + 104, ay - 58)]
    draw.line(pts, fill=(140, 220, 110), width=5, joint="curve")
    draw.polygon([(ax + 104, ay - 58), (ax + 88, ay - 56), (ax + 102, ay - 40)],
                 fill=(140, 220, 110))


def illu_rocket(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(12, 24, 58))
    import random
    rnd = random.Random(24)
    for _ in range(26):
        sx, sy = rnd.randint(x0 + 6, x1 - 6), rnd.randint(y0 + 6, y1 - 6)
        draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=WHITE)
    # small Earth, fully inside the illustration box, bottom right
    ex, ey, er = x1 - 34, y1 - 30, 22
    draw.ellipse([ex - er, ey - er, ex + er, ey + er], fill=(52, 120, 180),
                 outline=(120, 190, 230), width=2)
    draw.ellipse([ex - er + 6, ey - er + 4, ex - er + 16, ey - er + 12],
                 fill=(70, 160, 90))
    # rocket
    rx, ry = (x0 + x1) // 2, (y0 + y1) // 2 - 6
    draw.polygon([(rx, ry - 42), (rx - 16, ry - 6), (rx + 16, ry - 6)], fill=RED)
    draw.rectangle([rx - 16, ry - 6, rx + 16, ry + 34], fill=WHITE)
    draw.polygon([(rx - 16, ry + 34), (rx - 30, ry + 52), (rx - 16, ry + 44)],
                 fill=RED)
    draw.polygon([(rx + 16, ry + 34), (rx + 30, ry + 52), (rx + 16, ry + 44)],
                 fill=RED)
    draw.polygon([(rx - 7, ry + 34), (rx + 7, ry + 34), (rx, ry + 58)],
                 fill=(255, 170, 40))
    draw.ellipse([rx - 6, ry - 22, rx + 6, ry - 10], fill=(120, 190, 230))


def illu_trophy(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(18, 96, 58))
    # flag stripes top
    for i, c in enumerate([(0, 148, 64), (252, 210, 0), (220, 40, 40)]):
        draw.rectangle([x0 + i * (x1 - x0) // 3, y0,
                        x0 + (i + 1) * (x1 - x0) // 3, y0 + 10], fill=c)
    # trophy
    cx, cy = (x0 + x1) // 2 - 34, (y0 + y1) // 2 + 4
    draw.ellipse([cx - 30, cy - 34, cx + 30, cy + 10], fill=GOLD)
    draw.rectangle([cx - 30, cy - 34, cx + 30, cy - 6], fill=GOLD)
    draw.arc([cx - 48, cy - 30, cx - 18, cy + 6], 90, 270, fill=GOLD, width=7)
    draw.arc([cx + 18, cy - 30, cx + 48, cy + 6], -90, 90, fill=GOLD, width=7)
    draw.rectangle([cx - 6, cy + 10, cx + 6, cy + 26], fill=GOLD)
    draw.rectangle([cx - 22, cy + 26, cx + 22, cy + 36], fill=GOLD)
    # football
    fx, fy = x1 - 52, y1 - 42
    draw.ellipse([fx - 24, fy - 24, fx + 24, fy + 24], fill=WHITE,
                 outline=(30, 30, 30), width=2)
    draw.polygon([(fx, fy - 10), (fx + 9, fy - 3), (fx + 6, fy + 8),
                  (fx - 6, fy + 8), (fx - 9, fy - 3)], fill=(20, 20, 20))
    for dx, dy in ((-20, -8), (20, -8), (0, 20)):
        draw.ellipse([fx + dx - 4, fy + dy - 4, fx + dx + 4, fy + dy + 4],
                     fill=(20, 20, 20))


# ---------- page ----------

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle([0, 0, W, 128], fill=NAVY)
    title = "THE WORLD IN ONE DAY"
    tf = serif_b(54)
    d.text(((W - d.textlength(title, font=tf)) / 2, 16), title, font=tf, fill=WHITE)
    date = "TUESDAY  ·  24 NOVEMBER 2026"
    df = sans_b(27)
    d.text(((W - d.textlength(date, font=df)) / 2, 82), date, font=df, fill=GOLD)
    d.rectangle([0, 128, W, 134], fill=GOLD)

    # --- lead story: Huawei ---
    panel(d, (28, 150, 996, 424))
    illu_huawei(d, (44, 166, 372, 408))
    kicker_headline_body(
        d, 396, 170, 584,
        "UNITED STATES  ·  TECH ON TRIAL", RED,
        "HUAWEI FOUND GUILTY IN U.S. TRIAL", 40,
        "A federal jury convicts the Chinese telecom giant of stealing "
        "trade secrets and bank fraud — but acquits it of the more serious "
        "racketeering charge.", 20)

    # --- row 2: two panels ---
    panel(d, (28, 440, 500, 700))
    illu_tanker(d, (44, 456, 484, 560))
    kicker_headline_body(
        d, 44, 570, 440,
        "STRAIT OF HORMUZ  ·  MIDDLE EAST", TEAL,
        "FOUR TANKERS HIT BY MINES", 26,
        "Iran's Revolutionary Guard says four oil tankers struck naval "
        "mines in the strait.", 17, body_lines=2)

    panel(d, (524, 440, 996, 700))
    illu_drone_ship(d, (540, 456, 980, 560))
    kicker_headline_body(
        d, 540, 570, 440,
        "UKRAINE  ·  WAR AT SEA", NAVY_LT,
        "DRONES HIT RUSSIAN SHIPS", 26,
        "Kyiv says its naval drones struck a Russian cargo ship in the "
        "Gulf of Finland — and another off Libya.", 17, body_lines=2)

    # --- row 3: three panels ---
    boxes = [(28, 716, 340, 940), (356, 716, 668, 940), (684, 716, 996, 940)]
    illus = [illu_nvidia, illu_rocket, illu_trophy]
    stories = [
        ("BUSINESS  ·  MARKETS", (16, 96, 40),
         "NVIDIA BRINGS BACK ITS CHIEF",
         "Jensen Huang is reinstated as CEO; shares soar, then slide 6%."),
        ("SPACE  ·  CHINA", (90, 60, 140),
         "SHENZHOU 24 LIFTS OFF",
         "China launches two Chinese and the first Pakistani astronaut to "
         "Tiangong."),
        ("SPORT  ·  AFRICA", (150, 90, 20),
         "SENEGAL'S TITLE RESTORED",
         "CAS hands Senegal the 2025 Africa Cup crown back after an appeal."),
    ]
    for (bx0, by0, bx1, by1), illu, (kick, kcol, head, body) in zip(boxes, illus, stories):
        panel(d, (bx0, by0, bx1, by1))
        illu(d, (bx0 + 14, by0 + 12, bx1 - 14, by0 + 104))
        kicker_headline_body(d, bx0 + 14, by0 + 116, bx1 - bx0 - 28,
                             kick, kcol, head, 20, body, 15,
                             head_lines=2, body_lines=2)

    # --- footer ticker ---
    d.rectangle([0, 952, W, H], fill=NAVY)
    ticker = ("ALSO ON 24 NOVEMBER  —  Hostages seized at a Cartagena supermarket  •  "
              "Houthi fighters close on Aden  •  U.S. weighs tariffs on China and the EU  •  "
              "5.6 quake shakes Nepal  •  Trump awards Giuliani the Medal of Freedom")
    tf2 = sans(17)
    _, n = draw_wrapped(d, 28, 962, ticker, tf2, W - 56, (220, 225, 230))
    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
