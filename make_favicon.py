#!/usr/bin/env python3
"""Draw favicon.ico — the same mark as the inline SVG icon in index.html.

The app's icon is an inline SVG data URI, which every current browser prefers.
favicon.ico is the fallback: it's what a browser fetches from the site root on
its own, what older ones use, and what a bookmark or a search result shows. The
two have to be the same picture, so this draws the SVG's geometry with Pillow
rather than hand-editing a binary nobody can review in a diff.

    python3 make_favicon.py

The mark is the sprint itself — a cycle that comes round again — with the
commitment point marked where it closes. It's the family shape: the midnight
page as a rounded tile, the soft disc in the bottom-left corner, and one
gradient stroke in the accent, exactly as Money Map and PAPTrack wear it. Flow
Metrics is its sibling and carries the same tile under a bar chart; if the
family's shared parts change, change them in both.

Everything is drawn at 8x and reduced with Lanczos, which is what gives the
16px version clean edges. Keep the shapes here in step with the SVG in
index.html if that ever changes.
"""

import math

from PIL import Image, ImageDraw

# The mark, in the SVG's own 64x64 coordinates.
BG = (10, 14, 26, 255)          # #0a0e1a — midnight, the default theme's page
GLOW = (20, 28, 51, 255)        # #141c33 — the darker disc in the corner
GRAD_FROM = (129, 140, 248)     # #818cf8 — midnight's accent
GRAD_TO = (165, 180, 252)       # #a5b4fc
GRAD_AXIS = ((10, 52), (54, 12))                  # where the gradient runs

RING = (32, 32, 17)             # the sprint cycle: centre x, centre y, radius
RING_FROM = 50                  # degrees, counter-clockwise from east
RING_SWEEP = 295                # ...swept clockwise, leaving a gap at the top
RING_WIDTH = 6

SCALE = 8                       # supersample, then reduce
SIZES = [16, 32, 48, 64, 128, 256]


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient_at(point):
    """Colour for a point, projected onto the gradient's axis."""
    (x0, y0), (x1, y1) = GRAD_AXIS
    dx, dy = x1 - x0, y1 - y0
    span = dx * dx + dy * dy
    t = ((point[0] - x0) * dx + (point[1] - y0) * dy) / span
    return lerp(GRAD_FROM, GRAD_TO, min(1.0, max(0.0, t)))


def stamp(d, pts, width):
    """A gradient stroke, drawn by stamping a circle at every step.

    Round caps and joins come free that way: a polyline drawn in coloured
    pieces would otherwise show a notch wherever two pieces meet.
    """
    r = width / 2
    for x, y in pts:
        d.ellipse([(x - r) * SCALE, (y - r) * SCALE,
                   (x + r) * SCALE, (y + r) * SCALE],
                  fill=gradient_at((x, y)) + (255,))


def arc_points(cx, cy, r, start_deg, sweep_deg, steps=900):
    """Points along an arc, swept CLOCKWISE on screen from start_deg.

    Angles are the ordinary maths ones — counter-clockwise from east — and the
    y axis points down on screen, so subtracting the angle walks clockwise.
    """
    pts = []
    for s in range(steps + 1):
        a = math.radians(start_deg - sweep_deg * s / steps)
        pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
    return pts


def build():
    n = 64 * SCALE
    img = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, n, n], fill=BG)
    # the soft disc bottom-left, the way the SVG has it
    d.ellipse([(14 - 20) * SCALE, (52 - 20) * SCALE,
               (14 + 20) * SCALE, (52 + 20) * SCALE], fill=GLOW)

    cx, cy, r = RING
    stamp(d, arc_points(cx, cy, r, RING_FROM, RING_SWEEP), RING_WIDTH)

    # The commitment point, where the cycle opens: the same ringed dot Money
    # Map puts at the end of its line, so the two read as one family.
    a = math.radians(RING_FROM)
    mx, my = cx + r * math.cos(a), cy - r * math.sin(a)
    d.ellipse([(mx - 6.5) * SCALE, (my - 6.5) * SCALE,
               (mx + 6.5) * SCALE, (my + 6.5) * SCALE], fill=GRAD_TO + (255,))
    d.ellipse([(mx - 2.4) * SCALE, (my - 2.4) * SCALE,
               (mx + 2.4) * SCALE, (my + 2.4) * SCALE], fill=BG)

    # Round the corners with an alpha mask. The SVG leaves the disc square at
    # the edges; an icon reads better rounded, and this is the file that ends
    # up on a bookmarks bar.
    mask = Image.new('L', (n, n), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, n - 1, n - 1],
                                           radius=14 * SCALE, fill=255)
    img.putalpha(mask)
    return img


def main():
    art = build()
    frames = [art.resize((s, s), Image.LANCZOS) for s in SIZES]
    frames[-1].save('favicon.ico', format='ICO',
                    sizes=[(s, s) for s in SIZES])
    print('favicon.ico written at ' + ', '.join(f'{s}px' for s in SIZES))
    print('Now bump the ?v= on both favicon.ico references in index.html — '
          'browsers cache an icon for a long time and will keep showing the old '
          'one otherwise.')


if __name__ == '__main__':
    main()
