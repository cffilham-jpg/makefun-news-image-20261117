#!/usr/bin/env python3
"""news-image-20261117 (v2): generate a 1024x1024 editorial infographic
summing up Tuesday 17 November 2026 in four large illustrated panels.

Design goal: legibility at ~300px. Four stories only, each with a big
illustration, a coloured section tag, a condensed extra-bold headline
(40-48px, two lines max) and one short subline. All text is overlaid with
PIL; the illustrations themselves contain no text, so nothing can garble.

Deterministic: fixed layout, fixed fonts, no randomness, no timestamps.
Writes entry.png into $MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
import sys
from collections import namedtuple

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

# --- canvas -----------------------------------------------------------------
W, H = 1024, 1024
PAPER = (247, 244, 236)      # warm off-white page
CARD = (255, 255, 255)
INK = (26, 26, 26)
GREY = (85, 85, 85)
FAINT = (120, 116, 104)
RULE = (216, 210, 196)
NAVY = (20, 33, 61)
GOLD = (224, 165, 38)
MASTHEAD_SUB = (200, 205, 215)

# --- fonts ------------------------------------------------------------------
FONT_DIR = "/usr/share/fonts/truetype"
FONTS = {
    "sans": os.path.join(FONT_DIR, "liberation/LiberationSans-Regular.ttf"),
    "sans_bold": os.path.join(FONT_DIR, "liberation/LiberationSans-Bold.ttf"),
    "serif_bold": os.path.join(FONT_DIR, "liberation/LiberationSerif-Bold.ttf"),
    "cond_xb": os.path.join(FONT_DIR, "noto/NotoSans-CondensedExtraBold.ttf"),
}


def font(name, size):
    return ImageFont.truetype(FONTS[name], size)


# --- stories -----------------------------------------------------------------
Story = namedtuple("Story", "asset focus tag colour headline subline")

STORIES = [
    Story("media-generation-bridge-0-ed8bf139-49aa-4c15-b663-746b200c6929.webp",
          0.62, "EUROPE \u00b7 WAR", (179, 38, 30),
          "UKRAINE STRIKES CRIMEA BRIDGE AGAIN",
          "Road span collapses in second hit in 24 hours"),
    Story("media-generation-drones-0-e3291ee7-59d9-4d0f-9483-db863e473a42.webp",
          0.42, "MIDDLE EAST \u00b7 WAR", (179, 38, 30),
          "IRAN DRONES TARGET U.S. RADAR, BAHRAIN",
          "Bahrain intercepts the attack; no damage"),
    Story("media-generation-summit-0-31f920f4-b6b1-407b-ad2d-f1235300dcfa.webp",
          0.44, "ASIA \u00b7 DIPLOMACY", (29, 95, 168),
          "TRUMP IN MANILA FOR ASEAN SUMMIT",
          "Arrives for talks with Xi and Putin Thursday"),
    Story("media-generation-chips-0-7308380a-5fe7-4140-b73f-88d99f78a843.webp",
          0.55, "TECH \u00b7 TRADE", (14, 124, 123),
          "CHINA CONDEMNS U.S. AI CHIP CURBS",
          "Beijing hits back at new rules on remote access"),
]

FOOTER = "Sources: BBC  \u00b7  AP  \u00b7  Reuters  \u00b7  Al Jazeera"


# --- text helpers -----------------------------------------------------------
def tracked_width(draw, text, fnt, tracking):
    """Width of `text` drawn with `tracking` px between letters."""
    total = sum(draw.textlength(ch, font=fnt) for ch in text)
    return total + tracking * max(0, len(text) - 1)


def draw_tracked(draw, x, y, text, fnt, fill, tracking):
    """Draw `text` one letter at a time with fixed letter spacing."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking


def draw_centered_tracked(draw, cx, y, text, fnt, fill, tracking):
    width = tracked_width(draw, text, fnt, tracking)
    draw_tracked(draw, cx - width // 2, y, text, fnt, fill, tracking)


def wrap_words(draw, text, fnt, max_width):
    """Greedy word wrap into lines no wider than max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = "%s %s" % (current, word) if current else word
        if draw.textlength(trial, font=fnt) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def choose_headline(draw, text, max_width):
    """Biggest condensed font (48 down to 40) whose wrap fits two lines."""
    for size in (48, 46, 44, 42, 40):
        fnt = font("cond_xb", size)
        lines = wrap_words(draw, text, fnt, max_width)
        if len(lines) <= 2:
            return fnt, lines
    fnt = font("cond_xb", 40)
    return fnt, wrap_words(draw, text, fnt, max_width)[:2]


def fit_one_line(draw, text, max_width, start=21, minimum=16):
    """Largest regular-sans size (start down to minimum) fitting one line."""
    for size in range(start, minimum - 1, -1):
        fnt = font("sans", size)
        if draw.textlength(text, font=fnt) <= max_width:
            return fnt
    return font("sans", minimum)


# --- image helpers ----------------------------------------------------------
def cover_fit(image, width, height, focus_y):
    """Crop to the target aspect around a vertical focus, then resize."""
    src_w, src_h = image.size
    crop_h = int(src_w * height / width)
    centre = int(src_h * focus_y)
    top = max(0, min(src_h - crop_h, centre - crop_h // 2))
    return image.crop((0, top, src_w, top + crop_h)).resize(
        (width, height), Image.LANCZOS)


# --- layout -----------------------------------------------------------------
MASTHEAD_H = 158
MARGIN = 18
GAP = 14
PANEL_W = (W - 2 * MARGIN - GAP) // 2       # 487
PANEL_H = 396
ART_H = 214
TEXT_PAD = 18
HEAD_GAP = 30   # tag line to first headline line (was 28: block sat high)
SUB_GAP = 8     # headline block to subline (was 4: too tight under 2-line heads)


def draw_masthead(draw):
    draw.rectangle([0, 0, W, MASTHEAD_H], fill=NAVY)
    draw_centered_tracked(draw, W // 2, 16, "THE WORLD IN ONE IMAGE",
                          font("sans_bold", 22), GOLD, tracking=3)
    date = "TUESDAY 17 NOVEMBER 2026"
    date_font = font("serif_bold", 66)
    date_w = draw.textlength(date, font=date_font)
    draw.text(((W - date_w) // 2, 46), date, font=date_font, fill=(255, 255, 255))
    draw_centered_tracked(draw, W // 2, 126, "FOUR STORIES THAT DEFINED THE DAY",
                          font("sans_bold", 20), MASTHEAD_SUB, tracking=3)
    draw.line([24, MASTHEAD_H - 1, W - 24, MASTHEAD_H - 1], fill=GOLD, width=2)


def draw_story(canvas, draw, story, col, row):
    x0 = MARGIN + col * (PANEL_W + GAP)
    y0 = MASTHEAD_H + MARGIN + row * (PANEL_H + GAP)
    draw.rectangle([x0, y0, x0 + PANEL_W, y0 + PANEL_H],
                   fill=CARD, outline=RULE, width=1)

    art = Image.open(os.path.join(ASSETS, story.asset)).convert("RGB")
    art = cover_fit(art, PANEL_W - 2, ART_H, story.focus)
    canvas.paste(art, (x0 + 1, y0 + 1))
    draw.line([x0, y0 + ART_H + 1, x0 + PANEL_W, y0 + ART_H + 1],
              fill=RULE, width=1)

    tx = x0 + TEXT_PAD
    text_w = PANEL_W - 2 * TEXT_PAD
    tag_y = y0 + ART_H + 11
    draw_tracked(draw, tx, tag_y, story.tag, font("sans_bold", 20),
                 story.colour, tracking=1)

    head_font, lines = choose_headline(draw, story.headline, text_w)
    line_h = head_font.size + 4
    hy = tag_y + HEAD_GAP
    for line in lines:
        draw.text((tx, hy), line, font=head_font, fill=INK)
        hy += line_h

    sub_font = fit_one_line(draw, story.subline, text_w)
    draw.text((tx, tag_y + HEAD_GAP + 2 * line_h + SUB_GAP), story.subline,
              font=sub_font, fill=GREY)


def draw_footer(draw):
    foot_font = font("sans", 16)
    foot_w = draw.textlength(FOOTER, font=foot_font)
    draw.text(((W - foot_w) // 2, H - 26), FOOTER, font=foot_font, fill=FAINT)


def build():
    canvas = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(canvas)
    draw_masthead(draw)
    for index, story in enumerate(STORIES):
        draw_story(canvas, draw, story, col=index % 2, row=index // 2)
    draw_footer(draw)
    return canvas


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    image = build()
    dest = os.path.join(out_dir, "entry.png")
    image.save(dest, "PNG", optimize=True)
    size = os.path.getsize(dest)
    print("wrote %s (%dx%d, %d bytes)" % (dest, W, H, size))
    if size > 1048576:
        print("ERROR: output exceeds 1 MiB", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
