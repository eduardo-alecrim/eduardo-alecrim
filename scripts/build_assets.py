"""Draws the profile README as a set of blueprint sheets.

Sheet 01 is a general arrangement of the work I do: requests routed through a
facade while legacy systems are strangled and replaced by event-driven services.
Sheet 02 is my career as a drawing's revision history, and sheet 03 is my stack
as a bill of materials.

Run from the repository root:  python scripts/build_assets.py
"""
import math
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

PAPER = "#0F3460"
FILL = "#13406F"
GRID = "#1A4777"
GRID_MAJOR = "#23558B"
INK = "#EAF2FF"
INK_DIM = "#9FBBE0"
REDLINE = "#FF8A7A"
MARKER = "#FFD166"

STYLE = """<style>
.t{font-family:Bahnschrift,'DIN Alternate','Roboto Condensed','Arial Narrow',Arial,sans-serif}
.m{font-family:Consolas,'SFMono-Regular','JetBrains Mono','Liberation Mono',Menlo,monospace}
@keyframes ink{to{stroke-dashoffset:0}}
.ink{animation:ink 2.4s ease-out .5s forwards}
@media (prefers-reduced-motion:reduce){.ink{animation:none;stroke-dashoffset:0}}
</style>"""

DEFS = (
    '<pattern id="minor" x="30" y="30" width="20" height="20" patternUnits="userSpaceOnUse">'
    f'<path d="M20,0 H0 V20" fill="none" stroke="{GRID}" stroke-width="0.6"/></pattern>'
    '<pattern id="major" x="30" y="30" width="100" height="100" patternUnits="userSpaceOnUse">'
    f'<path d="M100,0 H0 V100" fill="none" stroke="{GRID_MAJOR}"/></pattern>'
    '<pattern id="hatch" width="10" height="10" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
    f'<line x1="0" y1="0" x2="0" y2="10" stroke="{INK_DIM}" stroke-opacity="0.35"/></pattern>'
    '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
    f'markerWidth="10" markerHeight="10" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{INK}"/></marker>'
    '<marker id="arrow-dim" viewBox="0 0 10 10" refX="9" refY="5" markerUnits="userSpaceOnUse" '
    f'markerWidth="10" markerHeight="10" orient="auto"><path d="M0,0 L10,5 L0,10 Z" fill="{INK_DIM}"/></marker>'
)


def text(x, y, content, size, *, mono=False, fill=INK, bold=False, anchor="start", spacing=0, extra=""):
    attrs = [f'class="{"m" if mono else "t"}"', f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"']
    if bold:
        attrs.append('font-weight="700"')
    if anchor != "start":
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}{extra}>{escape(content)}</text>'


def box(x, y, w, h, fill=FILL, stroke=INK, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"{extra}/>'


def sheet(w, h, label, body):
    """A drawing sheet: blueprint paper, grid, double border and zone markers."""
    parts = [
        f'<rect width="{w}" height="{h}" rx="6" fill="{PAPER}"/>',
        f'<rect x="30" y="30" width="{w - 60}" height="{h - 60}" fill="url(#minor)"/>',
        f'<rect x="30" y="30" width="{w - 60}" height="{h - 60}" fill="url(#major)"/>',
        f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" fill="none" stroke="{INK_DIM}"/>',
        f'<rect x="30" y="30" width="{w - 60}" height="{h - 60}" fill="none" stroke="{INK}" stroke-width="2"/>',
    ]
    columns, rows = 6, max(2, round((h - 60) / 200))
    zone_w, zone_h = (w - 60) / columns, (h - 60) / rows
    for i in range(columns):
        cx = 30 + zone_w * (i + 0.5)
        letter = "ABCDEF"[i]
        parts += [
            text(cx, 24, letter, 11, mono=True, fill=INK_DIM, anchor="middle"),
            text(cx, h - 16, letter, 11, mono=True, fill=INK_DIM, anchor="middle"),
        ]
        if i:
            x = 30 + zone_w * i
            parts.append(f'<path d="M{x},10 V30 M{x},{h - 30} V{h - 10}" stroke="{INK_DIM}"/>')
    for j in range(rows):
        cy = 30 + zone_h * (j + 0.5) + 4
        parts += [
            text(20, cy, str(j + 1), 11, mono=True, fill=INK_DIM, anchor="middle"),
            text(w - 20, cy, str(j + 1), 11, mono=True, fill=INK_DIM, anchor="middle"),
        ]
        if j:
            y = 30 + zone_h * j
            parts.append(f'<path d="M10,{y} H30 M{w - 30},{y} H{w - 10}" stroke="{INK_DIM}"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}"><defs>{STYLE}{DEFS}</defs>{"".join(parts)}{"".join(body)}</svg>'
    )


def cloud(x, y, w, h, bump):
    """Revision cloud around a rectangle, drawn clockwise. Returns the path and its length."""
    d, length = [f"M{x},{y}"], 0.0
    for dx, dy, side in ((1, 0, w), (0, 1, h), (-1, 0, w), (0, -1, h)):
        n = max(1, round(side / (2 * bump)))
        step = side / n
        d += [f"a{step / 2:.2f},{step / 2:.2f} 0 0 1 {dx * step:.2f},{dy * step:.2f}"] * n
        length += n * math.pi * step / 2
    return " ".join(d), length


def rev_tag(cx, cy, letter, size=13):
    """Drafting revision triangle."""
    points = f"{cx},{cy - size} {cx + size * 0.95},{cy + size * 0.6} {cx - size * 0.95},{cy + size * 0.6}"
    return f'<polygon points="{points}" fill="{PAPER}" stroke="{REDLINE}" stroke-width="1.6"/>' + text(
        cx, cy + size * 0.38, letter, size * 0.85, mono=True, fill=REDLINE, bold=True, anchor="middle"
    )


def callout(cx, cy, number, r=9):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{PAPER}" stroke="{MARKER}" stroke-width="1.5"/>' + text(
        cx, cy + 4, number, 11, mono=True, fill=MARKER, bold=True, anchor="middle"
    )


def travelling(path, color, dur, count, r=4, opacity=1):
    """Dots moving along a path: requests through the facade, events on the bus."""
    return "".join(
        f'<circle r="{r}" fill="{color}" fill-opacity="{opacity}"><animateMotion dur="{dur}s" '
        f'begin="-{dur * i / count:.2f}s" repeatCount="indefinite" path="{path}"/></circle>'
        for i in range(count)
    )


def north_arrow(cx, cy):
    return (
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{INK_DIM}"/>'
        f'<path d="M{cx},{cy - 16} L{cx + 7},{cy + 10} L{cx},{cy + 5} Z" fill="{INK}"/>'
        f'<path d="M{cx},{cy - 16} L{cx - 7},{cy + 10} L{cx},{cy + 5} Z" fill="none" stroke="{INK}"/>'
        + text(cx, cy - 26, "N", 12, bold=True, anchor="middle")
    )


def arrangement():
    w, h = 1200, 640
    b = [
        text(60, 102, "EDUARDO ALECRIM", 56, bold=True, spacing=4),
        text(62, 136, "JAVA BACKEND DEVELOPER · SPRING BOOT · QUARKUS · KAFKA", 18, fill=INK_DIM, spacing=2.5),
        text(62, 166, "GENERAL ARRANGEMENT — MODERNIZING LEGACY INTO EVENT-DRIVEN SERVICES", 13, mono=True, fill=MARKER, spacing=1),
        text(960, 78, "SITE", 10, mono=True, fill=INK_DIM, spacing=2),
        text(960, 100, "BRASÍLIA-DF", 18, bold=True, spacing=1.5),
        text(960, 120, "15°47′S 47°52′W", 11, mono=True, fill=INK_DIM),
        north_arrow(1122, 100),
    ]

    # Requests enter through a facade that routes them to legacy or new services
    b += [
        text(60, 318, "REQUESTS", 11, mono=True, fill=INK_DIM, spacing=1.5),
        f'<path d="M60,330 H138" stroke="{INK}" stroke-width="1.5" marker-end="url(#arrow)"/>',
        box(140, 200, 40, 270),
        text(160, 340, "FACADE · ROUTING", 12, mono=True, anchor="middle", spacing=2, extra=' transform="rotate(-90 160 335)"'),
        f'<path d="M180,245 H248" stroke="{INK_DIM}" stroke-width="1.5" stroke-dasharray="5 5" marker-end="url(#arrow-dim)"/>',
        f'<path d="M180,386 H273" stroke="{INK}" stroke-width="1.5" marker-end="url(#arrow)"/>',
    ]

    # Legacy: existing, to be removed
    b += [
        text(250, 192, "EXISTING — TO BE REMOVED", 11, mono=True, fill=INK_DIM, spacing=1.5),
        box(250, 200, 390, 90, fill="url(#hatch)", stroke=INK_DIM, extra=' stroke-dasharray="8 6"'),
        text(270, 234, "LEGACY", 20, bold=True, spacing=2),
        text(270, 258, "ORACLE SOA · APACHE CAMEL", 12, mono=True, fill=INK_DIM),
        text(270, 278, "ASP.NET MVC 4.6 · OPENSHIFT 3", 12, mono=True, fill=INK_DIM),
        callout(626, 214, "1"),
    ]

    notes = (
        "ORACLE SOA → SPRING BOOT, EVERY SOAP SERVICE · CAST GROUP",
        "ASP.NET MVC 4.6 → JAVA + REACT · CASSI",
        "OPENSHIFT 3 → OPENSHIFT 4 · CASSI",
    )
    b.append(text(680, 214, "NOTES", 12, mono=True, fill=INK_DIM, bold=True, spacing=2))
    for i, note in enumerate(notes):
        y = 240 + i * 22
        b += [callout(690, y - 4, str(i + 1)), text(708, y, note, 13, mono=True)]

    # New platform on OpenShift 4, with Kafka as the event bus
    b += [
        box(250, 318, 890, 152, fill="none"),
        text(266, 342, "NEW PLATFORM — OPENSHIFT 4", 14, bold=True, spacing=2),
        callout(548, 337, "3"),
    ]
    for i, (name, role) in enumerate((("SPRING BOOT", "SERVICES · REST APIs"), ("QUARKUS", "SERVICES"), ("REACT", "FRONTEND"))):
        x = 275 + i * 200
        b += [
            box(x, 356, 180, 60),
            text(x + 90, 382, name, 16, bold=True, anchor="middle", spacing=1.5),
            text(x + 90, 402, role, 12, mono=True, fill=INK_DIM, anchor="middle"),
        ]
    b.append(callout(855, 356, "2"))

    cx, top, bottom, rx, ry = 965, 362, 410, 90, 8
    b += [
        f'<path d="M{cx - rx},{top} V{bottom} A{rx},{ry} 0 0 0 {cx + rx},{bottom} V{top}" fill="{FILL}" stroke="{INK}" stroke-width="1.5"/>',
        f'<ellipse cx="{cx}" cy="{top}" rx="{rx}" ry="{ry}" fill="{FILL}" stroke="{INK}" stroke-width="1.5"/>',
        text(cx, 390, "SQL SERVER", 16, bold=True, anchor="middle", spacing=1.5),
        text(cx, 406, "DATA MODELING", 11, mono=True, fill=INK_DIM, anchor="middle"),
    ]

    bus = 446
    b += [
        f'<path d="M365,416 V{bus - 4} M565,416 V{bus - 4}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="3 3"/>',
        f'<circle cx="365" cy="{bus - 4}" r="3" fill="{INK}"/><circle cx="565" cy="{bus - 4}" r="3" fill="{INK}"/>',
        f'<path d="M275,{bus - 4} H1120 M275,{bus + 4} H1120" stroke="{INK}" stroke-width="1.5"/>',
        travelling(f"M275,{bus} H1120", MARKER, dur=6, count=4, r=3.5),
        box(880, bus - 11, 220, 22, fill=PAPER, stroke=INK),
        text(990, bus + 4, "APACHE KAFKA · EVENT BUS", 12, mono=True, bold=True, anchor="middle", spacing=1),
    ]

    # Traffic shifts from legacy to the new services
    b += [
        travelling("M60,330 H160 V386 H273", INK, dur=3, count=3),
        travelling("M60,330 H160 V245 H248", INK_DIM, dur=3, count=1, opacity=0.6),
    ]

    path, length = cloud(240, 308, 910, 172, bump=12)
    b += [
        f'<path class="ink" d="{path}" fill="none" stroke="{REDLINE}" stroke-width="1.6" stroke-linejoin="round" '
        f'stroke-dasharray="{length:.0f}" stroke-dashoffset="{length:.0f}"/>',
        rev_tag(1142, 302, "D", size=15),
    ]

    # Legend
    mini_cloud, _ = cloud(450, 538, 36, 14, bump=4)
    b += [
        text(60, 516, "LEGEND", 12, mono=True, fill=INK_DIM, bold=True, spacing=2),
        box(60, 536, 28, 16, fill="url(#hatch)", stroke=INK_DIM, extra=' stroke-dasharray="4 3"'),
        text(98, 549, "EXISTING · TO BE REMOVED", 12, mono=True),
        box(330, 536, 28, 16),
        text(368, 549, "NEW", 12, mono=True),
        f'<path d="{mini_cloud}" fill="none" stroke="{REDLINE}" stroke-width="1.4"/>',
        text(500, 549, "REVISION D — CASSI, 2024", 12, mono=True),
        f'<circle cx="74" cy="576" r="4" fill="{INK}"/>',
        text(98, 580, "REQUEST", 12, mono=True),
        f'<circle cx="344" cy="576" r="3.5" fill="{MARKER}"/>',
        text(368, 580, "EVENT", 12, mono=True),
        callout(468, 576, "1"),
        text(500, 580, "SEE NOTE", 12, mono=True),
    ]

    # Title block
    cells = (
        (800, 500, 370, 36, "PROJECT", "EDUARDO ALECRIM"),
        (800, 536, 230, 36, "ROLE", "JAVA BACKEND DEVELOPER"),
        (1030, 536, 140, 36, "EXPERIENCE", "4+ YEARS"),
        (800, 572, 150, 38, "ORGANIZATION", "CASSI"),
        (950, 572, 120, 38, "SHEET", "01 / 03"),
        (1070, 572, 100, 38, "REV", "E"),
    )
    for x, y, cw, ch, label, value in cells:
        b += [
            box(x, y, cw, ch, fill=PAPER),
            text(x + 8, y + 12, label, 9, mono=True, fill=INK_DIM, spacing=1.5),
            text(x + 8, y + 30, value, 15, bold=True, spacing=0.5),
        ]

    return sheet(w, h, "Sheet 01, general arrangement: legacy systems replaced by event-driven services", b)


def heading(title, subtitle, number):
    return [
        text(60, 88, title, 34, bold=True, spacing=3),
        text(62, 114, subtitle, 12, mono=True, fill=MARKER, spacing=1),
        text(1140, 84, f"SHEET {number} / 03", 16, bold=True, anchor="end", spacing=2),
        text(1140, 106, "EDUARDO ALECRIM", 11, mono=True, fill=INK_DIM, anchor="end", spacing=1.5),
    ]


def revisions():
    w, h = 1200, 540
    rows = (
        ("E", "2026-09", "POSTGRADUATE — AGILE SOFTWARE ENGINEERING", "DDD · CLEAN ARCHITECTURE · TDD", "UNIASSELVI", True),
        ("D", "2024-10", "JAVA BACKEND DEVELOPER", "SPRING BOOT · QUARKUS · KAFKA · ASP.NET MVC → JAVA + REACT · OPENSHIFT 3 → 4", "CASSI", True),
        ("C", "2023-07", "SENIOR DEVELOPER", "EVERY SOAP SERVICE OFF ORACLE SOA → SPRING BOOT · SOAP → REST · OPENSHIFT", "CAST GROUP", False),
        ("B", "2022-10", "MID-LEVEL DEVELOPER", "APACHE CAMEL → SPRING BOOT · REST APIs · SOAP SERVICES · ASP.NET MVC", "CAST GROUP", False),
        ("A", "2022-04", "JUNIOR DEVELOPER", "ASP.NET WEB FORMS → MVC · REST APIs · APACHE CAMEL BACKENDS", "CAST GROUP", False),
        ("0", "2021-07", "INITIAL ISSUE — B.SC. SYSTEMS ANALYSIS AND DEVELOPMENT", "2019 – 2021", "UNIPROJEÇÃO", False),
    )
    b = heading("REVISION HISTORY", "CAREER — EACH REVISION SUPERSEDES THE PREVIOUS ONE", "02")
    left, right, top, header_h, row_h = 60, 1140, 136, 34, 52
    columns = ((60, "REV"), (140, "DATE"), (270, "DESCRIPTION"), (930, "ORGANIZATION"))
    bottom = top + header_h + row_h * len(rows)

    b.append(box(left, top, right - left, header_h))
    for i, (rev, date, role, detail, org, active) in enumerate(rows):
        y = top + header_h + i * row_h
        if active:
            b.append(f'<rect x="{left}" y="{y}" width="{right - left}" height="{row_h}" fill="{MARKER}" fill-opacity="0.07"/>')
        b += [
            rev_tag(100, y + 30, rev),
            text(152, y + 31, date, 13, mono=True),
            text(282, y + 22, role, 15, bold=True, spacing=1),
            text(282, y + 41, detail, 12.5, mono=True, fill=INK_DIM),
            text(942, y + 24, org, 14, bold=True, spacing=1),
        ]
        if active:
            b.append(text(942, y + 41, "● ACTIVE", 10, mono=True, fill=MARKER, spacing=1.5))
        if i:
            b.append(f'<path d="M{left},{y} H{right}" stroke="{INK_DIM}" stroke-opacity="0.6"/>')
    for x, label in columns:
        b.append(text(x + 12, top + 22, label, 11, mono=True, fill=INK_DIM, bold=True, spacing=2))
        if x != left:
            b.append(f'<path d="M{x},{top} V{bottom}" stroke="{INK}" stroke-width="1.2"/>')
    b.append(f'<rect x="{left}" y="{top}" width="{right - left}" height="{bottom - top}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    return sheet(w, h, "Sheet 02, revision history: career from 2021 to 2026", b)


def materials():
    w, h = 1200, 500
    items = (
        ("JAVA", "CORE LANGUAGE · 4+ YEARS", False),
        ("SPRING BOOT", "SERVICES · REST APIs", False),
        ("QUARKUS", "BACKEND SERVICES", False),
        ("APACHE KAFKA", "EVENT-DRIVEN MESSAGING", False),
        ("REST · SOAP", "INTEGRATIONS · SOAP → REST", False),
        ("OPENSHIFT", "CONTAINER PLATFORM · 3 → 4", False),
        ("SQL SERVER", "DATA MODELING FOR NEW APPS", False),
        ("ORACLE DATABASE", "RELATIONAL DATABASE", False),
        ("REACT", "FRONTEND OF MIGRATED APPS", False),
        ("APACHE CAMEL", "INTEGRATION · MIGRATED TO SPRING BOOT", True),
        ("ORACLE SOA", "SOAP PLATFORM · MIGRATED TO SPRING BOOT", True),
        ("C# · ASP.NET MVC", "LEGACY WEB APPS · BEING MIGRATED", True),
    )
    b = heading("BILL OF MATERIALS", "STACK — HATCHED ITEMS ARE THE LEGACY I MIGRATE", "03")
    top, header_h, row_h, half = 136, 32, 40, len(items) // 2
    for t, left in enumerate((60, 610)):
        right = left + 530
        cols = ((left, "ITEM"), (left + 60, "COMPONENT"), (left + 245, "FUNCTION"))
        bottom = top + header_h + row_h * half
        b.append(box(left, top, 530, header_h))
        for i, (component, function, legacy) in enumerate(items[t * half:(t + 1) * half]):
            y = top + header_h + i * row_h
            if legacy:
                b.append(f'<rect x="{left}" y="{y}" width="530" height="{row_h}" fill="url(#hatch)"/>')
            b += [
                text(left + 14, y + 26, f"{t * half + i + 1:02d}", 13, mono=True, fill=INK_DIM),
                text(left + 72, y + 26, component, 15, bold=True, spacing=1, fill=INK_DIM if legacy else INK),
                text(left + 257, y + 25, function, 12, mono=True, fill=INK_DIM if legacy else INK),
            ]
            if i:
                b.append(f'<path d="M{left},{y} H{right}" stroke="{INK_DIM}" stroke-opacity="0.6"/>')
        for x, label in cols:
            b.append(text(x + 12, top + 21, label, 11, mono=True, fill=INK_DIM, bold=True, spacing=2))
            if x != left:
                b.append(f'<path d="M{x},{top} V{bottom}" stroke="{INK}" stroke-width="1.2"/>')
        b.append(f'<rect x="{left}" y="{top}" width="530" height="{bottom - top}" fill="none" stroke="{INK}" stroke-width="1.5"/>')
    b.append(text(600, 448, "END OF DRAWING SET · THANKS FOR STOPPING BY", 12, mono=True, fill=INK_DIM, anchor="middle", spacing=2))
    return sheet(w, h, "Sheet 03, bill of materials: the stack I work with", b)


def main():
    ASSETS.mkdir(exist_ok=True)
    files = {
        "sheet-01-arrangement": arrangement(),
        "sheet-02-revisions": revisions(),
        "sheet-03-materials": materials(),
    }
    for stale in ASSETS.glob("*.svg"):
        if stale.stem not in files:
            stale.unlink()
    for name, content in files.items():
        (ASSETS / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} sheets to {ASSETS}")


if __name__ == "__main__":
    main()
