"""
Diagram engine for the Siraj documentation set.

A tiny, dependency-free SVG layout library. It exists so that every diagram in
`docs/diagrams/` shares one visual language: the same type scale, the same node
anatomy, the same connector geometry and the same colour semantics.

Design rules encoded here
-------------------------
* Square corners everywhere. Nothing is rounded.
* A node is never a bare shape: it carries a category spine, a kicker, a title
  and optional detail lines, so the picture survives without a key.
* Colour is semantic, not decorative - each palette entry means one kind of
  participant (client, service, retrieval, model, store, note).
* Connectors are orthogonal and labelled; a label always sits on an opaque
  plate so it never collides with the line it annotates.
"""

from __future__ import annotations

from dataclasses import dataclass
from xml.sax.saxutils import escape

# --------------------------------------------------------------------------
# Typography
# --------------------------------------------------------------------------

SANS = "Inter, 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'Cascadia Code', 'SF Mono', Consolas, monospace"

# --------------------------------------------------------------------------
# Palette
# --------------------------------------------------------------------------

INK = "#0B1220"
BODY = "#334155"
MUTED = "#6B7A90"
FAINT = "#94A3B8"
HAIRLINE = "#DCE3ED"
RULE = "#C4CEDC"
PAPER = "#FFFFFF"
PANEL = "#F6F8FC"
BRAND = "#0E8F6E"


@dataclass(frozen=True)
class Style:
    """Border, fill, spine and text colours for one category of node."""

    line: str
    fill: str
    spine: str
    title: str = INK
    detail: str = MUTED
    kick: str = MUTED


CLIENT = Style(line="#B9CBF0", fill="#F2F6FE", spine="#2557D6", kick="#2557D6")
SERVICE = Style(
    line="#0B1220",
    fill="#0B1220",
    spine="#38BDF8",
    title="#FFFFFF",
    detail="#AEBCCE",
    kick="#7DD3FC",
)
RETRIEVE = Style(line="#A8DCCB", fill="#EFFBF5", spine="#0E8F6E", kick="#0B7A5E")
MODEL = Style(line="#EBD2A6", fill="#FEF8EC", spine="#B0740E", kick="#96630C")
STORE = Style(line="#CFC4EE", fill="#F6F3FE", spine="#6234C4", kick="#5A2FB4")
NOTE = Style(line="#D7DEE9", fill="#F7F9FC", spine="#7C8CA3", kick="#7C8CA3")
ALERT = Style(line="#EFC0BC", fill="#FEF4F3", spine="#C0392B", kick="#B03225")

LEGEND = [
    ("Client surface", CLIENT),
    ("Application service", SERVICE),
    ("Retrieval step", RETRIEVE),
    ("Model provider", MODEL),
    ("Store / artefact", STORE),
]

# --------------------------------------------------------------------------
# Text metrics (approximate, good enough for plate sizing)
# --------------------------------------------------------------------------

_FACTOR = {400: 0.515, 500: 0.525, 600: 0.538, 700: 0.550}


def text_width(s: str, size: float, weight: int = 400) -> float:
    return len(s) * size * _FACTOR.get(weight, 0.52)


def wrap(s: str, size: float, max_width: float, weight: int = 400) -> list:
    words, lines, cur = s.split(), [], ""
    for word in words:
        probe = (cur + " " + word).strip()
        if cur and text_width(probe, size, weight) > max_width:
            lines.append(cur)
            cur = word
        else:
            cur = probe
    if cur:
        lines.append(cur)
    return lines


# --------------------------------------------------------------------------
# Primitives
# --------------------------------------------------------------------------


def tx(x, y, s, size=12, weight=400, fill=BODY, anchor="start", family=SANS,
       spacing=None, opacity=None):
    extra = ""
    if spacing:
        extra += ' letter-spacing="%s"' % spacing
    if opacity is not None:
        extra += ' opacity="%s"' % opacity
    return (
        '<text x="%.1f" y="%.1f" font-family="%s" font-size="%s" font-weight="%s" '
        'fill="%s" text-anchor="%s"%s>%s</text>'
        % (x, y, family, size, weight, fill, anchor, extra, escape(s))
    )


def kicker(x, y, s, fill, anchor="start", size=8.5):
    return tx(x, y, s.upper(), size=size, weight=700, fill=fill, anchor=anchor, spacing=1.1)


def rect(x, y, w, h, fill=PAPER, stroke=HAIRLINE, sw=1.4, dash=None, shadow=False,
         opacity=None):
    extra = ""
    if dash:
        extra += ' stroke-dasharray="%s"' % dash
    if shadow:
        extra += ' filter="url(#lift)"'
    if opacity is not None:
        extra += ' opacity="%s"' % opacity
    return (
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" '
        'stroke-width="%s"%s/>' % (x, y, w, h, fill, stroke, sw, extra)
    )


def line(x1, y1, x2, y2, stroke=RULE, sw=1.4, dash=None):
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    return (
        '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
        % (x1, y1, x2, y2, stroke, sw, extra)
    )


class Node(object):
    """A rectangular participant with a spine, kicker, title and details."""

    def __init__(self, x, y, w, h, style, title, detail="", tag="", mono=False,
                 badge=""):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.style, self.title, self.tag, self.badge = style, title, tag, badge
        detail = [detail] if isinstance(detail, str) else list(detail)
        self.detail = [d for d in detail if d]
        self.mono = mono

    @property
    def cx(self):
        return self.x + self.w / 2.0

    @property
    def cy(self):
        return self.y + self.h / 2.0

    @property
    def right(self):
        return (self.x + self.w, self.cy)

    @property
    def left(self):
        return (self.x, self.cy)

    @property
    def top(self):
        return (self.cx, self.y)

    @property
    def bottom(self):
        return (self.cx, self.y + self.h)

    def port(self, side, t=0.5):
        """A point along one edge; t runs 0..1 top-to-bottom or left-to-right."""
        if side == "l":
            return (self.x, self.y + self.h * t)
        if side == "r":
            return (self.x + self.w, self.y + self.h * t)
        if side == "t":
            return (self.x + self.w * t, self.y)
        return (self.x + self.w * t, self.y + self.h)

    def svg(self):
        s, out = self.style, []
        out.append(rect(self.x, self.y, self.w, self.h, fill=s.fill, stroke=s.line,
                        sw=1.4, shadow=True))
        out.append('<rect x="%.1f" y="%.1f" width="4" height="%.1f" fill="%s"/>'
                   % (self.x, self.y, self.h, s.spine))
        px = self.x + 18
        cy = self.y + 21
        if self.tag:
            out.append(kicker(px, cy, self.tag, s.kick))
            cy += 17
        else:
            cy = self.y + 27
        for ln in wrap(self.title, 13.5, self.w - 34, 600):
            out.append(tx(px, cy + 4, ln, size=13.5, weight=600, fill=s.title))
            cy += 18
        if self.detail:
            cy += 2
            fam = MONO if self.mono else SANS
            size = 10.4 if self.mono else 11.2
            for d in self.detail:
                for ln in wrap(d, size, self.w - 34, 400):
                    out.append(tx(px, cy + 3, ln, size=size, fill=s.detail, family=fam))
                    cy += 14.5
        if self.badge:
            bw = text_width(self.badge, 9.5, 700) + 16
            out.append(rect(self.x + self.w - bw - 12, self.y + 11, bw, 17,
                            fill=PAPER, stroke=s.line, sw=1))
            out.append(tx(self.x + self.w - bw / 2 - 12, self.y + 23, self.badge,
                          size=9.5, weight=700, fill=s.kick, anchor="middle"))
        return "".join(out)


def cylinder(x, y, w, h, style, title, detail="", tag=""):
    """A store rendered as a squat cylinder - the one curve the set allows."""
    ry = 13.0
    out = [
        '<path d="M%.1f,%.1f a%.1f,%s 0 0 1 %.1f,0 v%.1f a%.1f,%s 0 0 1 %.1f,0 z" '
        'fill="%s" stroke="%s" stroke-width="1.4" filter="url(#lift)"/>'
        % (x, y + ry, w / 2, ry, w, h - 2 * ry, w / 2, ry, -w, style.fill, style.line),
        '<path d="M%.1f,%.1f a%.1f,%s 0 0 1 %.1f,0" fill="none" stroke="%s" '
        'stroke-width="1.4"/>' % (x, y + ry, w / 2, ry, w, style.line),
        '<path d="M%.1f,%.1f a%.1f,%s 0 0 0 %.1f,0" fill="none" stroke="%s" '
        'stroke-width="1.4"/>' % (x, y + ry, w / 2, ry, w, style.line),
    ]
    mid = y + h / 2.0
    if tag:
        out.append(kicker(x + w / 2, y + ry + 26, tag, style.kick, anchor="middle"))
    out.append(tx(x + w / 2, mid + 8, title, size=13, weight=600, fill=style.title,
                  anchor="middle"))
    if detail:
        out.append(tx(x + w / 2, mid + 25, detail, size=10.6, fill=style.detail,
                      anchor="middle"))
    return "".join(out)


def diamond(cx, cy, w, h, label, sub=""):
    pts = "%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" % (
        cx, cy - h / 2, cx + w / 2, cy, cx, cy + h / 2, cx - w / 2, cy)
    out = ['<polygon points="%s" fill="#FEF8EC" stroke="#D8A44C" stroke-width="1.5" '
           'filter="url(#lift)"/>' % pts]
    if sub:
        out.append(tx(cx, cy - 1, label, size=12.2, weight=600, fill=INK, anchor="middle"))
        out.append(tx(cx, cy + 15, sub, size=10.4, fill="#8A6316", anchor="middle"))
    else:
        out.append(tx(cx, cy + 4, label, size=12.2, weight=600, fill=INK, anchor="middle"))
    return "".join(out)


def actor(cx, cy, label, sub=""):
    c = "#44546B"
    out = [
        '<circle cx="%s" cy="%s" r="9.5" fill="none" stroke="%s" stroke-width="1.7"/>'
        % (cx, cy - 20, c),
        '<path d="M%s,%s v-8 a14,14 0 0 1 28,0 v8" fill="none" stroke="%s" '
        'stroke-width="1.7"/>' % (cx - 14, cy + 16, c),
        tx(cx, cy + 36, label, size=12, weight=600, fill=INK, anchor="middle"),
    ]
    if sub:
        out.append(tx(cx, cy + 51, sub, size=10.4, fill=MUTED, anchor="middle"))
    return "".join(out)


def plate(cx, cy, label, size=10.2, weight=600, fill=INK, bg=PAPER, border=None):
    w = text_width(label, size, weight) + 14
    h = size + 10
    return (
        '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" stroke="%s" '
        'stroke-width="1"/>' % (cx - w / 2, cy - h / 2, w, h, bg, border or "none")
        + tx(cx, cy + size * 0.36, label, size=size, weight=weight, fill=fill,
             anchor="middle")
    )


def path(points, stroke="#57647A", sw=1.7, dash=None, head=True, tail=False,
         marker="head"):
    d = "M" + " L".join("%.1f,%.1f" % (x, y) for x, y in points)
    extra = ""
    if dash:
        extra += ' stroke-dasharray="%s"' % dash
    if head:
        extra += ' marker-end="url(#%s)"' % marker
    if tail:
        extra += ' marker-start="url(#%s-back)"' % marker
    return ('<path d="%s" fill="none" stroke="%s" stroke-width="%s" '
            'stroke-linejoin="miter" stroke-linecap="butt"%s/>' % (d, stroke, sw, extra))


def connect(a, b, label="", stroke="#57647A", dash=None, mid=None, axis="h",
            at=0.5, sw=1.7, marker="head", tail=False, label_dx=0.0, label_dy=0.0):
    """Orthogonal connector. `axis` picks which leg is drawn first."""
    (x1, y1), (x2, y2) = a, b
    if abs(y1 - y2) < 0.6 or abs(x1 - x2) < 0.6:
        pts = [(x1, y1), (x2, y2)]
        lx = x1 + (x2 - x1) * at
        ly = y1 + (y2 - y1) * at
    elif axis == "h":
        m = mid if mid is not None else (x1 + x2) / 2.0
        pts = [(x1, y1), (m, y1), (m, y2), (x2, y2)]
        lx, ly = m, y1 + (y2 - y1) * at
    else:
        m = mid if mid is not None else (y1 + y2) / 2.0
        pts = [(x1, y1), (x1, m), (x2, m), (x2, y2)]
        lx, ly = x1 + (x2 - x1) * at, m
    out = [path(pts, stroke=stroke, dash=dash, sw=sw, marker=marker, tail=tail)]
    if label:
        out.append(plate(lx + label_dx, ly + label_dy, label))
    return "".join(out)


def step(n, cx, cy, tone=BRAND):
    """A numbered sequence pip."""
    return ('<circle cx="%.1f" cy="%.1f" r="10.5" fill="%s"/>' % (cx, cy, tone)
            + tx(cx, cy + 3.8, str(n), size=11, weight=700, fill=PAPER, anchor="middle"))


# --------------------------------------------------------------------------
# Frames, rails and page chrome
# --------------------------------------------------------------------------


def frame(x, y, w, h, title, fill="none", stroke="#B7C2D2", dash=None, tone=INK):
    """A titled container - the label interrupts the top border."""
    lbl_w = text_width(title.upper(), 8.5, 700) + 1.1 * len(title) + 22
    out = [rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, dash=dash)]
    out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="17" fill="%s"/>'
               % (x + 22, y - 8.5, lbl_w, PAPER))
    out.append(kicker(x + 32, y - 1.5, title, tone))
    return "".join(out)


def rail(x, y, w, h, title, sub="", tone="#8595AC"):
    """A band label down the left edge of a layered diagram."""
    out = [rect(x, y, w, h, fill=PANEL, stroke=HAIRLINE, sw=1.2)]
    out.append('<rect x="%.1f" y="%.1f" width="3" height="%.1f" fill="%s"/>'
               % (x, y, h, tone))
    out.append(kicker(x + 16, y + 27, title, tone))
    if sub:
        cy = y + 45
        for ln in wrap(sub, 10.6, w - 32):
            out.append(tx(x + 16, cy, ln, size=10.6, fill=MUTED))
            cy += 14
    return "".join(out)


def callout(x, y, w, title, lines, style=NOTE):
    """A side note block; height is derived from the content."""
    body = []
    for ln in lines:
        body.extend(wrap(ln, 11, w - 36))
    h = 46 + 15 * len(body)
    out = [rect(x, y, w, h, fill=style.fill, stroke=style.line, sw=1.2, dash="4 3")]
    out.append('<rect x="%.1f" y="%.1f" width="3" height="%.1f" fill="%s"/>'
               % (x, y, h, style.spine))
    out.append(kicker(x + 16, y + 24, title, style.kick))
    cy = y + 44
    for ln in body:
        out.append(tx(x + 16, cy, ln, size=11, fill=MUTED))
        cy += 15
    return "".join(out), h


def columns(x0, x1, n, gap):
    w = (x1 - x0 - gap * (n - 1)) / float(n)
    return [(x0 + i * (w + gap), w) for i in range(n)]


class Diagram(object):
    def __init__(self, width, height, title, subtitle="",
                 eyebrow="SIRAJ - ISLAMIC RAG CHATBOT"):
        self.w, self.h = width, height
        self.title, self.subtitle, self.eyebrow = title, subtitle, eyebrow
        self.body = []

    def add(self, *chunks):
        self.body.extend([c for c in chunks if c])
        return self

    def legend(self, items, x, y, gap=176):
        out = []
        for i, (label, style) in enumerate(items):
            cx = x + i * gap
            out.append(rect(cx, y - 9, 26, 13, fill=style.fill, stroke=style.line, sw=1.2))
            out.append('<rect x="%.1f" y="%.1f" width="3" height="13" fill="%s"/>'
                       % (cx, y - 9, style.spine))
            out.append(tx(cx + 34, y + 1.5, label, size=10.6, fill=MUTED))
        return self.add(*out)

    def render(self):
        w, h = self.w, self.h
        head = [
            '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" '
            'viewBox="0 0 %s %s" role="img" aria-label="%s">' % (w, h, w, h, escape(self.title)),
            "<title>%s</title>" % escape(self.title),
            "<defs>",
            '<marker id="head" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="7.5" '
            'markerHeight="7.5" orient="auto-start-reverse">'
            '<path d="M0.5,0.8 L9.5,5 L0.5,9.2 z" fill="#57647A"/></marker>',
            '<marker id="head-back" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="7.5" '
            'markerHeight="7.5" orient="auto-start-reverse">'
            '<path d="M0.5,0.8 L9.5,5 L0.5,9.2 z" fill="#57647A"/></marker>',
            '<marker id="soft" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0.5,0.8 L9.5,5 L0.5,9.2 z" fill="#93A2B7"/></marker>',
            '<marker id="soft-back" viewBox="0 0 10 10" refX="9.2" refY="5" markerWidth="7" '
            'markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0.5,0.8 L9.5,5 L0.5,9.2 z" fill="#93A2B7"/></marker>',
            '<filter id="lift" x="-14%" y="-16%" width="130%" height="136%">'
            '<feDropShadow dx="0" dy="1.5" stdDeviation="2.4" flood-color="#0B1220" '
            'flood-opacity="0.07"/></filter>',
            '<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">'
            '<path d="M28,0 L0,0 L0,28" fill="none" stroke="#EDF1F7" stroke-width="1"/>'
            "</pattern>",
            "</defs>",
            '<rect width="%s" height="%s" fill="%s"/>' % (w, h, PAPER),
            '<rect width="%s" height="%s" fill="url(#grid)"/>' % (w, h),
            '<rect x="0.75" y="0.75" width="%.1f" height="%.1f" fill="none" '
            'stroke="#D3DBE6" stroke-width="1.5"/>' % (w - 1.5, h - 1.5),
            '<rect x="0" y="0" width="%s" height="4" fill="%s"/>' % (w, BRAND),
            kicker(40, 47, self.eyebrow, BRAND),
            tx(40, 76, self.title, size=22, weight=700, fill=INK),
        ]
        if self.subtitle:
            head.append(tx(40, 97, self.subtitle, size=12.4, fill=MUTED))
        foot = [
            line(40, h - 46, w - 40, h - 46, stroke=HAIRLINE, sw=1),
            tx(40, h - 26, "docs/diagrams - regenerate with python docs/diagrams/generate_diagrams.py",
               size=10, fill=FAINT),
            tx(w - 40, h - 26, "Siraj", size=10, fill=FAINT, anchor="end"),
        ]
        return "\n".join(head + self.body + foot + ["</svg>"]) + "\n"

    def save(self, dest):
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(self.render())
        print("wrote %s" % dest)
