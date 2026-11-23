#!/usr/bin/env python3
"""Rebuild entry.png for the make.fun bounty news-image-20261122.

The entry is a newspaper front page for Sunday 22 November 2026: a navy
masthead, an AI-painted hero (a stormy globe, missile trails above tankers,
a plunging market chart — no words in the artwork itself), and six story
cards carrying the day's headlines. The hero illustration lives in assets/;
everything else — masthead, cards, footer — is drawn here with Pillow so
the text stays razor sharp at 1024x1024.

Usage:  python3 compose.py        # writes entry.png beside this file
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
HERO_FILE = HERE / "assets" / "media-generation-hero-globe-20261122-0-c93eb9f6-db47-4037-b516-14a1ca7f812f.webp"
OUT_FILE = HERE / "entry.png"

PAGE_W, PAGE_H = 1024, 1024

# Palette
NAVY = (18, 30, 55)
GOLD = (201, 162, 39)
GOLD_LIGHT = (216, 178, 74)
CREAM = (247, 243, 234)
PAPER = (255, 253, 247)
CARD_LINE = (210, 205, 190)
INK = (24, 28, 38)
GREY = (90, 96, 110)
WHITE = (255, 255, 255)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
SERIF_BOLD = FONT_DIR / "DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
SANS_PLAIN = FONT_DIR / "DejaVuSans.ttf"

MASTHEAD = "THE WORLD IN ONE DAY"
DATELINE = "SUNDAY · 22 NOVEMBER 2026"
FOOTER = "Six stories that defined the day — reported 22 November 2026 · AP · Reuters · AFP"

# (kicker, accent colour, headline, deck) — two columns, three rows.
STORIES = [
    (
        "CLIMATE · ANTALYA",
        (46, 110, 58),
        "COP31 COLLAPSES",
        "Climate summit ends with no deal after the EU rejects a draft "
        "that never mentions fossil fuels.",
    ),
    (
        "CONFLICT · BAHRAIN",
        (176, 60, 24),
        "IRAN STRIKES BAHRAIN",
        "Missiles and drones hit an industrial site, injuring two; "
        "tankers struck near the Strait of Hormuz.",
    ),
    (
        "JUSTICE · MEXICO",
        (31, 93, 140),
        "EL CHAPO ISIDRO CAUGHT",
        "Special forces capture cartel boss Fausto Isidro Meza Flores; "
        "11 killed in the Sinaloa raid.",
    ),
    (
        "WAR · KYIV REGION",
        (122, 63, 84),
        "DRONE HITS FLATS",
        "Russian drone hits a five-storey block in Dymer; 14 missing. "
        "Missile kills two in Kryvyi Rih.",
    ),
    (
        "MARKETS · NEW YORK",
        (140, 30, 30),
        "STOCKS IN CORRECTION",
        "S&P 500 falls 3.7% and Nasdaq 5.3% as the AI sell-off spreads "
        "to Japan and Korea.",
    ),
    (
        "JUSTICE · THE HAGUE",
        (90, 60, 120),
        "GENOCIDE RULING",
        "World Court finds Myanmar guilty of genocide against the "
        "Rohingya — a first for a state.",
    ),
]


def load(size, path=SANS_PLAIN):
    """One TrueType font at the requested size."""
    return ImageFont.truetype(str(path), size)


def centred(draw, y, text, font, colour):
    """Draw text horizontally centred on the page at height y."""
    x = (PAGE_W - draw.textlength(text, font=font)) / 2
    draw.text((x, y), text, font=font, fill=colour)


def flow(draw, text, font, width):
    """Greedy word wrap: the longest lines that still fit in width."""
    lines = []
    current = ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paint_masthead(draw):
    draw.rectangle([0, 0, PAGE_W, 96], fill=NAVY)
    draw.rectangle([0, 96, PAGE_W, 100], fill=GOLD)
    centred(draw, 10, MASTHEAD, load(46, SERIF_BOLD), CREAM)
    centred(draw, 62, DATELINE, load(25, SANS_BOLD), GOLD_LIGHT)


def cover(image, width, height):
    """Centre-crop to the target aspect, then scale — no squashing."""
    src_w, src_h = image.size
    target = width / height
    if src_w / src_h > target:
        crop_w = int(src_h * target)
        left = (src_w - crop_w) // 2
        image = image.crop((left, 0, left + crop_w, src_h))
    else:
        crop_h = int(src_w / target)
        top = (src_h - crop_h) // 2
        image = image.crop((0, top, src_w, top + crop_h))
    return image.resize((width, height), Image.LANCZOS)


def paint_hero(page):
    """Hero banner: the AI illustration, cropped to fill the full width."""
    hero = Image.open(HERO_FILE).convert("RGB")
    hero = cover(hero, PAGE_W, 341)
    page.paste(hero, (0, 100))
    draw = ImageDraw.Draw(page)
    draw.rectangle([0, 437, PAGE_W, 441], fill=GOLD)
    return draw


def paint_card(draw, index, story):
    kicker, accent, headline, deck = story
    margin, gutter = 24, 16
    card_w = (PAGE_W - 2 * margin - gutter) // 2
    card_h = 162
    col, row = index % 2, index // 2
    x = margin + col * (card_w + gutter)
    y = 454 + row * (card_h + 12)

    draw.rounded_rectangle(
        [x, y, x + card_w, y + card_h],
        radius=10, fill=PAPER, outline=CARD_LINE, width=1,
    )
    # Accent spine on the left edge of the card.
    draw.rectangle([x, y + 8, x + 6, y + card_h - 8], fill=accent)

    text_x = x + 20
    inner_w = card_w - 40

    # Numbered badge, top right.
    badge = (x + card_w - 42, y + 12, x + card_w - 12, y + 42)
    draw.ellipse(badge, fill=accent)
    digits = load(18, SANS_BOLD)
    label = str(index + 1)
    draw.text(
        (x + card_w - 27 - draw.textlength(label, font=digits) / 2, y + 15),
        label, font=digits, fill=WHITE,
    )

    draw.text((text_x, y + 12), kicker, font=load(15, SANS_BOLD), fill=accent)

    headline_font = load(25, SANS_BOLD)
    cursor = y + 38
    for line in flow(draw, headline, headline_font, inner_w)[:2]:
        draw.text((text_x, cursor), line, font=headline_font, fill=INK)
        cursor += 30

    deck_font = load(17, SANS_PLAIN)
    cursor += 4
    for line in flow(draw, deck, deck_font, inner_w)[:2]:
        draw.text((text_x, cursor), line, font=deck_font, fill=GREY)
        cursor += 23


def paint_footer(draw):
    centred(draw, 990, FOOTER, load(15, SANS_PLAIN), GREY)


def build():
    page = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    draw = ImageDraw.Draw(page)
    paint_masthead(draw)
    draw = paint_hero(page)
    for index, story in enumerate(STORIES):
        paint_card(draw, index, story)
    paint_footer(draw)
    page.save(OUT_FILE, optimize=True)
    print(f"wrote {OUT_FILE} {page.size}")


if __name__ == "__main__":
    build()
