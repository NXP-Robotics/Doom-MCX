#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-or-later
"""Generate the startup splash tile as a C array of RGB565 pixels.

The tile is a starburst of rays fanning out from the middle of the left edge
with a text label rendered on top using a built-in 5x7 font.
"""

import argparse
import math
import struct
import sys
import zlib

# 5x7 glyphs, one line per character: key, then 7 rows of 5 columns.
# "_" is the key for the space character. Leftmost column is the most
# significant bit when a row is treated as 5 bits.
_GLYPHS = """
A .###. #...# #...# ##### #...# #...# #...#
B ####. #...# #...# ####. #...# #...# ####.
C .###. #...# #.... #.... #.... #...# .###.
D ####. #...# #...# #...# #...# #...# ####.
E ##### #.... #.... ####. #.... #.... #####
F ##### #.... #.... ####. #.... #.... #....
G .###. #...# #.... #.### #...# #...# .###.
H #...# #...# #...# ##### #...# #...# #...#
I .###. ..#.. ..#.. ..#.. ..#.. ..#.. .###.
J ..### ...#. ...#. ...#. ...#. #..#. .##..
K #...# #..#. #.#.. ##... #.#.. #..#. #...#
L #.... #.... #.... #.... #.... #.... #####
M #...# ##.## #.#.# #.#.# #...# #...# #...#
N #...# ##..# ##..# #.#.# #..## #..## #...#
O .###. #...# #...# #...# #...# #...# .###.
P ####. #...# #...# ####. #.... #.... #....
Q .###. #...# #...# #...# #.#.# #..#. .##.#
R ####. #...# #...# ####. #.#.. #..#. #...#
S .#### #.... #.... .###. ....# ....# ####.
T ##### ..#.. ..#.. ..#.. ..#.. ..#.. ..#..
U #...# #...# #...# #...# #...# #...# .###.
V #...# #...# #...# #...# #...# .#.#. ..#..
W #...# #...# #...# #.#.# #.#.# ##.## #...#
X #...# #...# .#.#. ..#.. .#.#. #...# #...#
Y #...# #...# .#.#. ..#.. ..#.. ..#.. ..#..
Z ##### ....# ...#. ..#.. .#... #.... #####
0 .###. #...# #..## #.#.# ##..# #...# .###.
1 ..#.. .##.. ..#.. ..#.. ..#.. ..#.. .###.
2 .###. #...# ....# ...#. ..#.. .#... #####
3 ##### ...#. ..##. ....# ....# #...# .###.
4 ...#. ..##. .#.#. #..#. ##### ...#. ...#.
5 ##### #.... ####. ....# ....# #...# .###.
6 ..##. .#... #.... ####. #...# #...# .###.
7 ##### ....# ...#. ..#.. .#... .#... .#...
8 .###. #...# #...# .###. #...# #...# .###.
9 .###. #...# #...# .#### ....# ...#. .##..
- ..... ..... ..... ##### ..... ..... .....
. ..... ..... ..... ..... ..... .##.. .##..
_ ..... ..... ..... ..... ..... ..... .....
"""

FONT = {}
for _line in _GLYPHS.split("\n"):
    _tok = _line.split()
    if _tok:
        FONT[" " if _tok[0] == "_" else _tok[0]] = _tok[1:]

GLYPH_W, GLYPH_H = 5, 7

# Ray palettes, upper half then lower half, as RGB888.
UPPER = [0x9FD531, 0x2EB25C, 0x1AACA9, 0x38B9E8]
LOWER = [0xF2C200, 0xF28C00, 0xE05A00]
NRAYS = 28


def rgb565(rgb):
    r, g, b = rgb >> 16, (rgb >> 8) & 0xFF, rgb & 0xFF
    return (r >> 3) << 11 | (g >> 2) << 5 | (b >> 3)


def unrgb565(v):
    r, g, b = v >> 11, (v >> 5) & 0x3F, v & 0x1F
    return bytes((r << 3 | r >> 2, g << 2 | g >> 4, b << 3 | b >> 2))


def darken(rgb, f):
    return sum(int(((rgb >> s) & 0xFF) * f) << s for s in (16, 8, 0))


def rays(width, height):
    """Background: NRAYS wedges fanning out from (0, height / 2)."""
    pix = []
    for y in range(height):
        for x in range(width):
            a = math.atan2(y - height / 2 + 0.5, x + 0.5)
            i = min(NRAYS - 1, int((a + math.pi / 2) / math.pi * NRAYS))
            pal = UPPER if a < 0 else LOWER
            c = pal[i % len(pal)]
            pix.append(rgb565(darken(c, 0.85) if i % 2 else c))
    return pix


def text_scale(text, width, height):
    """Largest integer scale that keeps the label inside the tile."""
    cells = (GLYPH_W + 1) * len(text) - 1
    s = 1
    while cells * (s + 1) <= width - 8 and GLYPH_H * (s + 1) <= height / 4:
        s += 1
    return s


def draw_text(pix, width, height, text, color=0xFFFF):
    s = text_scale(text, width, height)
    tw = ((GLYPH_W + 1) * len(text) - 1) * s
    x0, y0 = (width - tw) // 2, height // 2 - (GLYPH_H * s) // 2
    for i, ch in enumerate(text):
        rows = FONT.get(ch, FONT[" "])
        for ry, row in enumerate(rows):
            for rx, c in enumerate(row):
                if c != "#":
                    continue
                for dy in range(s):
                    for dx in range(s):
                        x = x0 + (i * (GLYPH_W + 1) + rx) * s + dx
                        y = y0 + ry * s + dy
                        if 0 <= x < width and 0 <= y < height:
                            pix[y * width + x] = color


def render(width, height, text):
    pix = rays(width, height)
    if text:
        draw_text(pix, width, height, text)
    return pix


def ascii_art(text):
    rows = [FONT.get(c, FONT[" "]) for c in text]
    return "\n".join(" ".join(g[r] for g in rows) for r in range(GLYPH_H))


def write_png(path, width, height, pix):
    raw = b"".join(
        b"\0" + b"".join(unrgb565(v) for v in pix[y * width:(y + 1) * width])
        for y in range(height)
    )

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)))
        f.write(chunk(b"IDAT", zlib.compress(raw, 9)))
        f.write(chunk(b"IEND", b""))


def write_c(path, width, height, pix, swap):
    vals = [(v >> 8) | (v << 8) & 0xFF00 for v in pix] if swap else pix
    with open(path, "w") as f:
        f.write("/* SPDX-License-Identifier: Apache-2.0 OR GPL-2.0-or-later */\n")
        f.write("/* Generated by scripts/gen_splash.py, do not edit. */\n\n")
        f.write("const unsigned int doom_splash_width = %d;\n" % width)
        f.write("const unsigned int doom_splash_height = %d;\n\n" % height)
        f.write("const unsigned short doom_splash[%d * %d] = {\n" % (width, height))
        for i in range(0, len(vals), 16):
            f.write("  " + " ".join("0x%04x," % v for v in vals[i:i + 16]) + "\n")
        f.write("};\n")


def selftest():
    text = "NXP 0123456789 ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    print(ascii_art(text))
    for ch, rows in FONT.items():
        assert len(rows) == GLYPH_H, "glyph %r has %d rows" % (ch, len(rows))
        assert all(len(r) == GLYPH_W and set(r) <= set(".#") for r in rows), "bad glyph %r" % ch
    for name in "-.":
        assert name in FONT, "missing glyph %r" % name
    w, h = 80, 320
    pix = render(w, h, "NXP")
    assert len(pix) == w * h, "tile is %d pixels, expected %d" % (len(pix), w * h)
    assert all(0 <= v <= 0xFFFF for v in pix), "pixel value out of 16-bit range"
    assert 0xFFFF in pix, "text was not drawn"
    assert text_scale("NXP", w, h) == 4, "unexpected text scale"
    print("selftest OK")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--width", type=int, default=80)
    p.add_argument("--height", type=int, default=320)
    p.add_argument("--text", default="NXP")
    p.add_argument("--swap", action="store_true", help="byte-swap each RGB565 value")
    p.add_argument("--png", help="also write the tile as a PNG for inspection")
    p.add_argument("--ascii", action="store_true", help="print the text as ASCII art")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--out", help="C file to write")
    a = p.parse_args()

    if a.selftest:
        selftest()
        return
    if a.width < GLYPH_W or a.height < 4 * GLYPH_H:
        p.error("width/height too small for the font")

    text = a.text.upper()
    if a.ascii:
        print(ascii_art(text))
    if not a.out and not a.png:
        return
    pix = render(a.width, a.height, text)
    if a.png:
        write_png(a.png, a.width, a.height, pix)
    if a.out:
        write_c(a.out, a.width, a.height, pix, a.swap)


if __name__ == "__main__":
    sys.exit(main())
