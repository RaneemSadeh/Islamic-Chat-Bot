"""
Diagram engine for the Siraj documentation set.

A small, dependency-free SVG layout library. Everything in `docs/diagrams/`
is drawn with it, so the whole set shares one visual language.

The style, in one paragraph: a thin framed figure with its title sitting on the
top border; compact flat-coloured boxes with short labels; stick figures for
people; page glyphs for documents; a cylinder for a store; thin black arrows
carrying small captions. Light, airy, and readable at a glance - the picture
carries the shape of the system, and the prose around it carries the detail.
"""

from __future__ import annotations

from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# Typography
# --------------------------------------------------------------------------

SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', Consolas, monospace"

INK = "#1A1A1A"
LINE = "#1F1F1F"
CAPTION = "#4A4A4A"
FAINT = "#8A8A8A"
PAPER = "#FFFFFF"

# --------------------------------------------------------------------------
# Palette - (fill, border, text). Flat colours, one meaning each.
# --------------------------------------------------------------------------

BLUE = ("#A4C2F4", "#6D9EEB", INK)      # client surface
DARK = ("#1F1F1F", "#1F1F1F", "#FFFFFF")  # application service
GREEN = ("#B6D7A8", "#82B366", INK)      # retrieval / store
YELLOW = ("#FFE599", "#D6B656", INK)     # model provider
ORANGE = ("#F9CB9C", "#E69138", INK)     # output
GRAY = ("#EFEFEF", "#B7B7B7", INK)       # neutral / absent
RED = ("#F4CCCC", "#CC7C7C", INK)        # limitation
WHITE = ("#FFFFFF", "#9E9E9E", INK)

R = 5  # corner radius, matching the reference figures

_W = {400: 0.512, 500: 0.522, 600: 0.536, 700: 0.548}


def text_width(s: str, size: float, weight: int = 400) -> float:
    return len(s) * size * _W.get(weight, 0.52)


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------


def tx(x, y, s, size=11, weight=400, fill=INK, anchor="middle", family=SANS,
       spacing=None):
    extra = ' letter-spacing="%s"' % spacing if spacing else ""
    return ('<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" font-weight="%s" '
            'fill="%s" text-anchor="%s"%s>%s</text>'
            % (x, y, family, size, weight, fill, anchor, extra, escape(s)))


def rect(x, y, w, h, fill=PAPER, stroke=LINE, sw=1.2, r=R, dash=None):
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" ry="%s" '
            'fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, r, fill, stroke, sw, extra))


def line(x1, y1, x2, y2, stroke=LINE, sw=1.1, dash=None):
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
            'stroke-width="%s"%s/>' % (x1, y1, x2, y2, stroke, sw, extra))


# --------------------------------------------------------------------------
# Figures
# --------------------------------------------------------------------------


class Box(object):
    """A compact labelled box. Title centred, optional small lines beneath."""

    def __init__(self, x, y, w, h, style, title, subs=(), port="", mono_subs=False,
                 title_size=11.5):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.style, self.title, self.port = style, title, port
        self.subs = [s for s in (subs if not isinstance(subs, str) else [subs]) if s]
        self.mono_subs = mono_subs
        self.title_size = title_size

    @property
    def cx(self):
        return self.x + self.w / 2.0

    @property
    def cy(self):
        return self.y + self.h / 2.0

    @property
    def left(self):
        return (self.x, self.cy)

    @property
    def right(self):
        return (self.x + self.w, self.cy)

    @property
    def top(self):
        return (self.cx, self.y)

    @property
    def bottom(self):
        return (self.cx, self.y + self.h)

    def port_at(self, side, t=0.5):
        if side == "l":
            return (self.x, self.y + self.h * t)
        if side == "r":
            return (self.x + self.w, self.y + self.h * t)
        if side == "t":
            return (self.x + self.w * t, self.y)
        return (self.x + self.w * t, self.y + self.h)

    def svg(self):
        fill, border, colour = self.style
        out = [rect(self.x, self.y, self.w, self.h, fill=fill, stroke=border, sw=1.2)]
        n = len(self.subs)
        if n == 0:
            base = self.cy + self.title_size * 0.36
        else:
            base = self.cy - (n * 10.0) / 2.0 + 1
        out.append(tx(self.cx, base, self.title, size=self.title_size, weight=600, fill=colour))
        cy = base + 12.5
        sub_colour = "#D4D4D4" if colour == "#FFFFFF" else "#3C3C3C"
        for s in self.subs:
            out.append(tx(self.cx, cy, s, size=8.4, fill=sub_colour,
                          family=MONO if self.mono_subs else SANS))
            cy += 10.5
        if self.port:
            out.append(tx(self.cx, self.y + self.h + 12, self.port, size=8.4, fill=FAINT,
                          family=MONO))
        return "".join(out)


class Cylinder(object):
    """A store."""

    def __init__(self, x, y, w, h, style, title, subs=()):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.style, self.title = style, title
        self.subs = [s for s in (subs if not isinstance(subs, str) else [subs]) if s]

    @property
    def cx(self):
        return self.x + self.w / 2.0

    @property
    def cy(self):
        return self.y + self.h / 2.0

    @property
    def top(self):
        return (self.cx, self.y)

    @property
    def bottom(self):
        return (self.cx, self.y + self.h)

    @property
    def left(self):
        return (self.x, self.cy)

    @property
    def right(self):
        return (self.x + self.w, self.cy)

    def svg(self):
        fill, border, colour = self.style
        x, y, w, h = self.x, self.y, self.w, self.h
        ry = 9.0
        out = [
            '<path d="M%.1f,%.1f a%.1f,%s 0 0 1 %.1f,0 v%.1f a%.1f,%s 0 0 1 %.1f,0 z" '
            'fill="%s" stroke="%s" stroke-width="1.2"/>'
            % (x, y + ry, w / 2, ry, w, h - 2 * ry, w / 2, ry, -w, fill, border),
            '<path d="M%.1f,%.1f a%.1f,%s 0 0 0 %.1f,0" fill="none" stroke="%s" '
            'stroke-width="1.2"/>' % (x, y + ry, w / 2, ry, w, border),
        ]
        n = len(self.subs)
        base = self.cy + (4 if n == 0 else -(n * 10.0) / 2.0 + 3)
        out.append(tx(self.cx, base, self.title, size=11.5, weight=600, fill=colour))
        cy = base + 12
        for s in self.subs:
            out.append(tx(self.cx, cy, s, size=8.4, fill="#3C3C3C"))
            cy += 10.5
        return "".join(out)


def actor(cx, cy, label, sub=""):
    """A person. `cy` is the centre of the glyph, the label sits below it."""
    out = [
        '<circle cx="%.1f" cy="%.1f" r="7.5" fill="none" stroke="%s" stroke-width="1.3"/>'
        % (cx, cy - 15, LINE),
        '<path d="M%.1f,%.1f v-6 a11,11 0 0 1 22,0 v6" fill="none" stroke="%s" '
        'stroke-width="1.3"/>' % (cx - 11, cy + 14, LINE),
        tx(cx, cy + 30, label, size=9.5, weight=600, fill=INK),
    ]
    if sub:
        out.append(tx(cx, cy + 42, sub, size=8.2, fill=FAINT))
    return "".join(out)


def page(cx, cy, label="", sub="", w=34, h=42):
    """A document glyph - a page with a wavy bottom edge."""
    x, y = cx - w / 2.0, cy - h / 2.0
    q = w / 4.0
    d = ("M%.1f,%.1f h%.1f v%.1f q%.1f,7 %.1f,0 q%.1f,-7 %.1f,0 z"
         % (x, y, w, h - 7, -q, -(w / 2), -q, -(w / 2)))
    out = ['<path d="%s" fill="%s" stroke="%s" stroke-width="1.2"/>' % (d, PAPER, LINE)]
    for i in range(3):
        out.append(line(x + 6, y + 10 + i * 7, x + w - 6, y + 10 + i * 7,
                        stroke="#C4C4C4", sw=1))
    if label:
        out.append(tx(cx, y + h + 13, label, size=9.2, weight=600, fill=INK))
    if sub:
        out.append(tx(cx, y + h + 24, sub, size=8.2, fill=FAINT))
    return "".join(out)


def dot(cx, cy, style=GREEN, r=9):
    """The small junction node used before a provider call."""
    fill, border, _ = style
    return ('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" stroke="%s" stroke-width="1.2"/>'
            % (cx, cy, r, fill, border))


def brace(x, y0, y1, depth=9, flip=False):
    """A curly brace grouping a column of things."""
    s = -1 if flip else 1
    mid = (y0 + y1) / 2.0
    d = ("M%.1f,%.1f q%.1f,0 %.1f,%.1f v%.1f q0,%.1f %.1f,%.1f "
         "q%.1f,0 %.1f,%.1f v%.1f q0,%.1f %.1f,%.1f"
         % (x, y0, s * depth * 0.1, s * depth * 0.5, depth * 0.45,
            (mid - y0) - depth * 1.2, depth * 0.6, s * depth * 0.5, depth * 0.6,
            -s * depth * 0.5, -s * depth * 0.5, depth * 0.6,
            (y1 - mid) - depth * 1.2, depth * 0.6, s * depth * 0.5, depth * 0.6))
    return '<path d="%s" fill="none" stroke="%s" stroke-width="1.2"/>' % (d, LINE)


# --------------------------------------------------------------------------
# Connectors
# --------------------------------------------------------------------------


def arrow(a, b, label="", below="", dashed=False, bidir=False, route="straight",
          mid=None, stroke=LINE, label_dy=-7, sw=1.1, head=True, pts=None):
    """A thin connector. `route` is straight, 'h' (across first) or 'v' (down first).

    Pass `pts` to route it by hand when neither elbow reads well.
    """
    (x1, y1), (x2, y2) = a, b
    if pts is not None:
        pts = list(pts)
    elif route == "straight" or abs(y1 - y2) < 0.6 or abs(x1 - x2) < 0.6:
        pts = [(x1, y1), (x2, y2)]
    elif route == "h":
        m = mid if mid is not None else (x1 + x2) / 2.0
        pts = [(x1, y1), (m, y1), (m, y2), (x2, y2)]
    else:
        m = mid if mid is not None else (y1 + y2) / 2.0
        pts = [(x1, y1), (x1, m), (x2, m), (x2, y2)]

    d = "M" + " L".join("%.1f,%.1f" % p for p in pts)
    extra = ""
    if dashed:
        extra += ' stroke-dasharray="4 3"'
    if head:
        extra += ' marker-end="url(#tip)"'
    if bidir:
        extra += ' marker-start="url(#tip-back)"'
    out = ['<path d="%s" fill="none" stroke="%s" stroke-width="%s" '
           'stroke-linejoin="round"%s/>' % (d, stroke, sw, extra)]

    if label or below:
        if len(pts) == 2:
            lx, ly = (pts[0][0] + pts[1][0]) / 2.0, (pts[0][1] + pts[1][1]) / 2.0
        else:
            lx = (pts[0][0] + pts[1][0]) / 2.0
            ly = (pts[0][1] + pts[1][1]) / 2.0
        vertical = abs(pts[-1][1] - pts[0][1]) > abs(pts[-1][0] - pts[0][0]) and len(pts) == 2
        if label:
            if vertical:
                out.append(tx(lx + 6, ly, label, size=8.4, fill=CAPTION, anchor="start"))
            else:
                out.append(tx(lx, ly + label_dy, label, size=8.4, fill=CAPTION))
        if below:
            out.append(tx(lx, ly + 14, below, size=8.4, fill=FAINT))
    return "".join(out)


def caption(cx, cy, lines, anchor="middle", size=8.4, fill=FAINT, gap=11):
    """Free-floating small print - the grey annotations in the reference figures."""
    out = []
    for i, ln in enumerate(lines if not isinstance(lines, str) else [lines]):
        out.append(tx(cx, cy + i * gap, ln, size=size, fill=fill, anchor=anchor))
    return "".join(out)


def frame(x, y, w, h, title, dash=None):
    """The outer container: thin border with the title sitting on the top edge."""
    tw = text_width(title, 13, 700) + 22
    return (rect(x, y, w, h, fill="none", stroke=LINE, sw=1.3, r=6, dash=dash)
            + '<rect x="%.1f" y="%.1f" width="%.1f" height="18" fill="%s"/>'
              % (x + w / 2 - tw / 2, y - 9, tw, PAPER)
            + tx(x + w / 2, y + 4.5, title, size=13, weight=700, fill=INK))


def panel(x, y, w, h, title="", dash="5 4", stroke="#B4B4B4"):
    """A dashed sub-grouping inside a frame, titled at its top-left."""
    out = [rect(x, y, w, h, fill="none", stroke=stroke, sw=1.1, r=4, dash=dash)]
    if title:
        tw = text_width(title, 9.5, 600) + 14
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="14" fill="%s"/>'
                   % (x + 14, y - 7, tw, PAPER))
        out.append(tx(x + 14 + tw / 2, y - 2.5, title, size=9.5, weight=600, fill="#5A5A5A"))
    return "".join(out)


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------


class Diagram(object):
    def __init__(self, width, height):
        self.w, self.h = width, height
        self.body = []

    def add(self, *chunks):
        self.body.extend([c for c in chunks if c])
        return self

    def legend(self, items, cx, y):
        """A single centred row of swatches."""
        widths = [26 + 6 + text_width(label, 8.6) + 22 for label, _ in items]
        total = sum(widths) - 22
        x = cx - total / 2.0
        out = []
        for (label, style), width in zip(items, widths):
            fill, border, _ = style
            out.append(rect(x, y - 8, 22, 12, fill=fill, stroke=border, sw=1, r=2))
            out.append(tx(x + 28, y + 1.5, label, size=8.6, fill=CAPTION, anchor="start"))
            x += width
        return self.add(*out)

    def render(self):
        head = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" '
            'viewBox="0 0 %s %s">' % (self.w, self.h, self.w, self.h),
            "<defs>",
            '<marker id="tip" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.5" '
            'markerHeight="6.5" orient="auto-start-reverse">'
            '<path d="M0.8,1.2 L9,5 L0.8,8.8 z" fill="%s"/></marker>' % LINE,
            '<marker id="tip-back" viewBox="0 0 10 10" refX="8.6" refY="5" markerWidth="6.5" '
            'markerHeight="6.5" orient="auto-start-reverse">'
            '<path d="M0.8,1.2 L9,5 L0.8,8.8 z" fill="%s"/></marker>' % LINE,
            "</defs>",
            '<rect width="%s" height="%s" fill="%s"/>' % (self.w, self.h, PAPER),
        ]
        return "\n".join(head + self.body + ["</svg>"]) + "\n"

    def save(self, dest):
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(self.render())
        print("wrote %s" % dest)


def row(x0, x1, n, gap):
    """n equal slots between x0 and x1."""
    w = (x1 - x0 - gap * (n - 1)) / float(n)
    return [(x0 + i * (w + gap), w) for i in range(n)]
