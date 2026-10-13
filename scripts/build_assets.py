"""Draws the profile README in the style of Brasília's metro signage.

Brasília's metro runs two lines, green and orange, and the profile borrows its
look: a station name board on top, then line diagrams for what I'm working on,
my stack and the legacy systems I've modernized.

Run from the repository root:

    python scripts/build_assets.py                # orange signs
    python scripts/build_assets.py --theme musgo  # neon moss signs
"""
import argparse
import json
from pathlib import Path
from xml.sax.saxutils import escape

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
ICONS = json.loads((HERE / "icons.json").read_text(encoding="utf-8"))

THEME = "laranja"  # laranja | musgo: colour of the signs and highlights

# ---------------------------------------------------------------- content ---

NAME = "Eduardo Alecrim"
ROLE = "JAVA BACKEND DEVELOPER"
TAGLINE = "I build backend services and modernize the legacy systems behind them."
LOCATION = "BRASÍLIA, BRAZIL"

# Stations on the name board's line: (what, with what).
FOCUS = [
    ("REST APIs", "Spring Boot · Quarkus"),
    ("Event-driven", "Apache Kafka"),
    ("Cloud-native", "OpenShift"),
    ("Legacy modernization", "SOAP → REST · .NET → Java"),
]

# Right now: (label, sentence).
NOW = [
    ("WORKING ON", "Backend services at CASSI, one of Brazil's largest self-managed health plans."),
    ("BUILDING WITH", "Spring Boot, Quarkus and Apache Kafka, deployed on OpenShift."),
    ("LEARNING", "DDD, Clean Architecture and TDD, in a postgrad in Agile Software Engineering."),
    ("PREVIOUSLY", "CAST group, where I went from junior to senior developer in 15 months."),
]

# Tech stack: (group, [(name, icon)]). An icon is a key of icons.json or GLYPHS,
# or else a short monogram drawn as text.
STACK = [
    ("LANGUAGES & FRAMEWORKS", [("Java", "openjdk"), ("Spring Boot", "springboot"), ("Quarkus", "quarkus")]),
    ("MESSAGING & APIS", [("Apache Kafka", "apachekafka"), ("REST", "api"), ("SOAP", "api")]),
    ("PLATFORM & DATA", [("OpenShift", "redhatopenshift"), ("SQL Server", "database"), ("Oracle", "database")]),
    ("FRONT END & .NET", [("React", "react"), ("C#", "C#"), ("ASP.NET MVC", "dotnet")]),
]

# Legacy modernization: (legacy, replacement, where and when, badge).
CHANGES = [
    ("ASP.NET Web Forms", "ASP.NET MVC", "CAST group · 2022", None),
    ("Apache Camel", "Spring Boot", "CAST group · 2022–23", None),
    ("Oracle SOA · SOAP", "Spring Boot · REST APIs", "CAST group · 2023–24", "all services"),
    ("ASP.NET MVC 4.6", "Java + React", "CASSI · 2024 →", "ongoing"),
    ("OpenShift 3", "OpenShift 4", "CASSI · 2024 →", "ongoing"),
]

CONTACT = ("Let's talk.", "Happy to chat about backend, event-driven systems and legacy modernization.")

# ---------------------------------------------------------------- palette ---

BG = "#08090A"
PANEL = "#0D0E10"
CHIP = "#131417"
EDGE = "#1F2125"
EDGE_HI = "#2C2F35"
INK = "#F2F3EF"
INK_2 = "#A9ACB2"
INK_3 = "#7C8089"
VERDE = "#B4F03C"    # Brasília's Green line, as neon moss
LARANJA = "#FF8A1F"  # Brasília's Orange line

THEMES = {  # colour of the signs and highlights
    "laranja": {"led": LARANJA},
    "musgo": {"led": VERDE},
}

GLYPHS = {  # stroked 24x24 drawings for tools without a Simple Icons logo
    "api": "M9 4C7 4 6 5 6 7v2c0 1.6-1 2.6-2.5 3C5 12.4 6 13.4 6 15v2c0 2 1 3 3 3"
           "M15 4c2 0 3 1 3 3v2c0 1.6 1 2.6 2.5 3-1.5.4-2.5 1.4-2.5 3v2c0 2-1 3-3 3",
    "database": "M4 6c0-1.7 3.6-3 8-3s8 1.3 8 3-3.6 3-8 3-8-1.3-8-3zM4 6v12c0 1.7 3.6 3 8 3s8-1.3 8-3V6"
                "M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3",
}

SANS = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Mono',Consolas,'SFMono-Regular',Menlo,'Liberation Mono',monospace"
# Entrances play once on load (pop, rise, draw, type); the rest loops. Every
# entrance animates *from* hidden, so with reduced motion everything just shows.
BASE_CSS = (
    f".s{{font-family:{SANS}}}.m{{font-family:{MONO}}}"
    "@keyframes blink{50%{opacity:.25}}.blink{animation:blink 1.4s steps(1) infinite}"
    "@keyframes pulse{from{transform:scale(1);opacity:.9}to{transform:scale(2.3);opacity:0}}"
    ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}"
    "@keyframes pop{from{transform:scale(0);opacity:0}}"
    ".pop{transform-box:fill-box;transform-origin:center;animation:pop .5s cubic-bezier(.34,1.56,.64,1) both}"
    "@keyframes rise{from{opacity:0;transform:translateY(10px)}}.rise{animation:rise .6s ease-out both}"
    "@keyframes draw{from{stroke-dashoffset:1}}.draw{animation:draw 1.2s cubic-bezier(.65,0,.35,1) both}"
    "@keyframes type{from{fill-opacity:0}to{fill-opacity:1}}.type{animation:type .01s steps(1) both}"
    "@keyframes flicker{0%,86%,89%,93%,100%{opacity:1}87%{opacity:.3}91%{opacity:.55}}"
    ".flicker{animation:flicker 6s linear infinite}"
    "@keyframes sweep{0%{transform:translateX(0)}50%,100%{transform:translateX(1400px)}}"
    ".sweep{animation:sweep 5s ease-in-out 1.5s infinite}"
    "@keyframes breathe{from{opacity:.04}to{opacity:.14}}.breathe{animation:breathe 4s ease-in-out infinite alternate}"
    "@keyframes uncover{from{transform:scaleX(1)}}"
    ".uncover{transform-box:fill-box;transform-origin:right;transform:scaleX(0);"
    "animation:uncover 1s cubic-bezier(.65,0,.35,1) both}"
    ".scan{opacity:0;animation:scan 1s cubic-bezier(.65,0,.35,1) both}"
    "@keyframes ring{from{transform:scale(1);opacity:.7}to{transform:scale(1.15,1.6);opacity:0}}"
    ".ring{transform-box:fill-box;transform-origin:center;animation:ring 2.4s ease-out infinite}"
    "@media (prefers-reduced-motion:reduce){*{animation:none!important}.train{display:none}}"
)

# ---------------------------------------------------------------- helpers ---


def attr(value):
    return escape(str(value), {'"': "&quot;"})


def text(x, y, content, size, cls="s", fill=INK, weight=None, anchor=None, spacing=None, extra=""):
    attrs = [f'class="{cls}"', f'x="{x:g}"', f'y="{y:g}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}{extra}>{escape(content)}</text>'


def text_width(content, size, bold=False):
    """A generous estimate, so boxes fit the widest of the fallback fonts."""
    em = sum(
        0.3 if ch in "ijlI.,:;'|! ·" else 0.86 if ch in "MWmw@" else 0.64 if ch.isupper() or ch.isdigit() else 0.55
        for ch in content
    )
    return em * size * (1.06 if bold else 1)


def document(width, height, label, body, css="", defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{attr(label)}">'
        f"<title>{escape(label)}</title><defs><style>{BASE_CSS}{css}</style>{defs}</defs>"
        f"{''.join(body)}</svg>\n"
    )


def glow(fid="glow", blur=2.5):
    return (
        f'<filter id="{fid}" x="-50%" y="-50%" width="200%" height="200%">'
        f'<feGaussianBlur stdDeviation="{blur}" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    )


def panel(width, height):
    return (
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="18" '
        f'fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
    )


def bullet(label, colors, cx=52, cy=42, r=17):
    """The coloured disc that names a line on the signs; two colours if shared."""
    if len(colors) == 1:
        disc = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{colors[0]}"/>'
    else:
        disc = (
            f'<path d="M{cx} {cy - r}A{r} {r} 0 0 0 {cx} {cy + r}Z" fill="{colors[0]}"/>'
            f'<path d="M{cx} {cy - r}A{r} {r} 0 0 1 {cx} {cy + r}Z" fill="{colors[1]}"/>'
        )
    return disc + text(cx, cy + 6.5, label, 18, weight=800, fill=BG, anchor="middle")


def header(mark, title, note="", width=1000):
    out = appear(mark, "pop", 0.05) + appear(text(84, 50, title, 25, weight=700), "rise", 0.15)
    if note:
        out += appear(text(width - 40, 48, note, 12, "m", INK_3, anchor="end", spacing=1), "rise", 0.3)
    return out + f'<line x1="24" y1="80" x2="{width - 24}" y2="80" stroke="{EDGE}"/>'


def station(x, y, current=None):
    """A station; the current one carries a pulse in the given colour."""
    if current:
        return (
            f'<circle class="pulse" cx="{x:g}" cy="{y:g}" r="13" fill="none" stroke="{current}" stroke-width="2"/>'
            f'<circle cx="{x:g}" cy="{y:g}" r="14" fill="{INK}" stroke="{PANEL}" stroke-width="4"/>'
            f'<circle cx="{x:g}" cy="{y:g}" r="5" fill="{current}"/>'
        )
    return f'<circle cx="{x:g}" cy="{y:g}" r="10.5" fill="{INK}" stroke="{PANEL}" stroke-width="4"/>'


def closed_station(x, y):
    return (
        f'<circle cx="{x}" cy="{y}" r="9" fill="{PANEL}" stroke="{INK_3}" stroke-width="2.5" '
        'stroke-dasharray="3.2 2.6"/>'
        f'<path d="M{x - 5} {y + 5}L{x + 5} {y - 5}" stroke="{LARANJA}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def train(path, dur, color, begin=0, length=20):
    """A lit carriage running along a path at a steady speed, fading in and out at the ends."""
    h = length * 0.375
    timing = f'dur="{dur:g}s" begin="{begin:g}s" repeatCount="indefinite"'
    return (
        f'<g class="train" opacity="0">'
        f'<rect x="{-length / 2:g}" y="{-h / 2:g}" width="{length}" height="{h:g}" rx="{h / 2:g}" '
        f'fill="{color}" filter="url(#glow)"/>'
        f'<animateMotion path="{path}" rotate="auto" {timing}/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.95;1" {timing}/></g>'
    )


def flash(x, y, color, begin, dur, r0=11, r1=30):
    """A ring that bursts from a station every time a train reaches it.

    It repeats with the train's period, so start it when the train first arrives.
    """
    burst = min(0.9, 1.1 / dur)
    timing = f'keyTimes="0;{burst:.3f};1" dur="{dur:g}s" begin="{begin:.2f}s" repeatCount="indefinite"'
    return (
        f'<circle cx="{x:g}" cy="{y:g}" r="{r0}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0">'
        f'<animate attributeName="r" values="{r0};{r1};{r1}" {timing}/>'
        f'<animate attributeName="opacity" values="1;0;0" {timing}/></circle>'
        f'<circle cx="{x:g}" cy="{y:g}" r="5.5" fill="{color}" opacity="0">'
        f'<animate attributeName="opacity" values="1;0;0" {timing}/></circle>'
    )


def appear(markup, cls, at):
    """Wraps markup in an entrance (pop or rise) that starts `at` seconds in."""
    return f'<g class="{cls}" style="animation-delay:{at:.2f}s">{markup}</g>'


def drawn(d, color, at, dur=1.2, width=8):
    """A line that draws itself from its first point to its last."""
    return (
        f'<path class="draw" d="{d}" pathLength="1" stroke-dasharray="1" fill="none" stroke="{color}" '
        f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '
        f'style="animation-delay:{at:.2f}s;animation-duration:{dur:g}s"/>'
    )


def typed(x, y, content, size, start, step=0.028, fill=INK_2):
    """Text that types itself in, one character at a time."""
    spans = "".join(
        f'<tspan class="type" style="animation-delay:{start + i * step:.3f}s">{escape(ch)}</tspan>'
        for i, ch in enumerate(content)
    )
    return f'<text class="s" x="{x}" y="{y}" font-size="{size}" fill="{fill}" style="white-space:pre">{spans}</text>'


def wiped(markup, box, color, at, dur=1.0):
    """Reveals markup left to right behind a bright bar, like a sign being lit.

    A panel-coloured cover shrinks away to the right while the bar sweeps across.
    `box` is (x, y, width, height) of the area to reveal; returns (css, body).
    """
    x, y, w, h = box
    timing = f'style="animation-delay:{at:g}s;animation-duration:{dur:g}s"'
    css = (
        f"@keyframes scan{{0%{{opacity:1;transform:translateX(0)}}85%{{opacity:1}}"
        f"100%{{opacity:0;transform:translateX({w:g}px)}}}}"
    )
    body = (
        markup
        + f'<rect class="uncover" x="{x}" y="{y}" width="{w:g}" height="{h}" fill="{PANEL}" {timing}/>'
        + f'<rect class="scan" x="{x}" y="{y + 8}" width="4" height="{h - 16}" rx="2" fill="{color}" '
        f'filter="url(#glow)" {timing}/>'
    )
    return css, body


def pill(right, cy, label, color, dot=False):
    label = label.upper()
    width = len(label) * 7.9 + 24 + (14 if dot else 0)
    x = right - width
    out = (
        f'<rect x="{x:g}" y="{cy - 12}" width="{width:g}" height="24" rx="12" fill="{color}" '
        f'fill-opacity=".08" stroke="{color}" stroke-opacity=".7"/>'
    )
    if dot:
        out += f'<circle class="blink" cx="{x + 14:g}" cy="{cy}" r="3.5" fill="{color}"/>'
    return out + text(x + 12 + (14 if dot else 0), cy + 4, label, 11.5, "m", color, weight=700, spacing=1)


def icon(key, x, y, color, size=20):
    scale = f"translate({x:g} {y:g}) scale({size / 24:g})"
    if key in ICONS:
        return f'<path transform="{scale}" d="{ICONS[key]}" fill="{color}"/>'
    if key in GLYPHS:
        return (
            f'<path transform="{scale}" d="{GLYPHS[key]}" fill="none" stroke="{color}" stroke-width="2.2" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    return text(x + size / 2, y + size * 0.74, key, size * 0.66, weight=800, fill=color, anchor="middle")


def chip(x, cy, name, key, color, lit=None):
    """A tool: its logo and name in a rounded box. Returns markup and width.

    `lit` is (begin, period): the border lights up then, once per period.
    """
    width = 46 + text_width(name, 15, bold=True) + 16
    glow_up = ""
    if lit:
        begin, period = lit
        glow_up = (
            f'<animate attributeName="stroke" values="{color};{EDGE_HI};{EDGE_HI}" '
            f'keyTimes="0;{min(0.9, 1.2 / period):.3f};1" dur="{period:g}s" begin="{begin:.2f}s" '
            'repeatCount="indefinite"/>'
        )
    return (
        f'<rect x="{x:g}" y="{cy - 19}" width="{width:g}" height="38" rx="19" fill="{CHIP}" '
        f'stroke="{EDGE_HI}">{glow_up}</rect>'
        + icon(key, x + 15, cy - 10, color)
        + text(x + 46, cy + 5, name, 15, weight=700)
    ), width


# --------------------------------------------------------------- drawings ---


def hero(theme):
    """A station name board: my name, and a line through what I work on."""
    led = theme["led"]
    width, height = 1000, 366
    y = 264
    xs = [150 + (850 - 150) * i / (len(FOCUS) - 1) for i in range(len(FOCUS))]
    line_at, line_dur = 1.0, 1.2           # the line draws itself...
    run_at, run_dur = 2.6, 7.0             # ...then a train keeps running along it

    name_w = min(text_width(NAME, 80, bold=True) + 24, width - 80)
    wipe_css, name = wiped(text(46, 152, NAME, 80, weight=800, spacing=-2), (40, 70, name_w, 104), led, 0.15)

    body = [
        f'<g clip-path="url(#board)"><rect width="{width}" height="{height}" fill="{PANEL}"/>'
        f'<circle class="breathe" cx="{width - 120}" cy="40" r="320" fill="url(#halo)" opacity=".09"/>'
        f'<rect width="{width}" height="12" fill="{led}"/>'
        '<rect class="sweep" x="-220" width="220" height="12" fill="url(#sheen)"/></g>'
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="18" fill="none" '
        f'stroke="{EDGE}" stroke-width="1.5"/>'
    ]
    body.append(appear(text(52, 66, ROLE, 13, "m", led, weight=700, spacing=3), "rise", 0))
    body.append(appear(
        f'<text class="m" x="{width - 52}" y="66" font-size="11" fill="{INK_3}" text-anchor="end" '
        f'letter-spacing="1.5"><tspan fill="{VERDE}">●</tspan> <tspan fill="{LARANJA}">●</tspan>  '
        f"{escape(LOCATION)}</text>", "rise", 0.1))
    body.append(name)
    body.append(typed(50, 192, TAGLINE, 18, start=1.0))

    body.append(drawn(f"M60 {y}H{width - 60}", led, line_at, line_dur))
    labels = []
    for x, (what, tools) in zip(xs, FOCUS):
        reach = (x - 60) / (width - 120)
        body.append(appear(station(x, y), "pop", line_at + reach * line_dur))
        labels.append(flash(x, y, led, run_at + reach * run_dur, run_dur))
        labels.append(appear(
            text(x, y + 42, what, 16.5, weight=700, anchor="middle")
            + text(x, y + 64, tools, 12, "m", led, anchor="middle"),
            "rise", line_at + reach * line_dur + 0.15))
    body.append(train(f"M60,{y} H{width - 60}", run_dur, INK, begin=run_at))
    body += labels

    label = f"{NAME}, Java backend developer in Brasília, Brazil. {TAGLINE} " + "; ".join(
        f"{what}: {tools}" for what, tools in FOCUS
    ) + "."
    defs = (
        f'<clipPath id="board"><rect width="{width}" height="{height}" rx="18"/></clipPath>'
        f'<radialGradient id="halo"><stop offset="0" stop-color="{led}"/>'
        f'<stop offset="1" stop-color="{led}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="sheen"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        "</linearGradient>"
        + glow()
    )
    return document(width, height, label, body, wipe_css, defs)


def right_now(theme):
    led = theme["led"]
    width = 1000
    top, step = 132, 58
    bottom = top + step * (len(NOW) - 1)
    height = bottom + 56
    run_at, run_dur = 2.2, 4.0
    body = [panel(width, height), header(bullet("1", [led]), "Right now")]
    body.append(drawn(f"M64 {top}V{bottom}", led, 0.3, 1.0))
    body.append(train(f"M64,{top} V{bottom}", run_dur, INK, begin=run_at))
    for i, (label, sentence) in enumerate(NOW):
        y = top + i * step
        reach = (y - top) / (bottom - top)
        body.append(appear(station(64, y, current=led if i == 0 else None), "pop", 0.3 + reach))
        body.append(flash(64, y, led, run_at + reach * run_dur, run_dur))
        body.append(appear(
            text(98, y - 6, label, 11.5, "m", led, weight=700, spacing=2) + text(98, y + 16, sentence, 16),
            "rise", 0.45 + i * 0.18))
    label = "Right now. " + " ".join(f"{label.capitalize()}: {sentence}" for label, sentence in NOW)
    return document(width, height, label, body, defs=glow())


def stack(theme):
    led = theme["led"]
    width = 1000
    top, step = 134, 58
    bottom = top + step * (len(STACK) - 1)
    height = bottom + 52
    run_at, run_dur = 2.6, 4.4
    body = [panel(width, height), header(bullet("2", [VERDE]), "Tech stack")]
    body.append(drawn(f"M64 {top}V{bottom}", VERDE, 0.3, 1.0))
    body.append(train(f"M64,{top} V{bottom}", run_dur, INK, begin=run_at))
    for i, (group, tools) in enumerate(STACK):
        y = top + i * step
        reach = (y - top) / (bottom - top)
        passes = run_at + reach * run_dur
        body.append(appear(station(64, y), "pop", 0.3 + reach))
        body.append(flash(64, y, VERDE, passes, run_dur))
        body.append(appear(text(98, y + 4, group, 11.5, "m", INK_2, weight=700, spacing=1.5), "rise", 0.45 + i * 0.15))
        x = 320
        for j, (name, key) in enumerate(tools):  # the chips light up as the train passes their row
            markup, w = chip(x, y, name, key, led, lit=(passes + 0.1 + j * 0.12, run_dur))
            body.append(appear(markup, "pop", 0.6 + i * 0.15 + j * 0.08))
            x += w + 12
    label = "Tech stack. " + " ".join(
        f"{group.capitalize()}: {', '.join(name for name, _ in tools)}." for group, tools in STACK
    )
    return document(width, height, label, body, defs=glow())


def modernization(theme):
    width = 1000
    top, step = 138, 58
    height = top + step * (len(CHANGES) - 1) + 56
    run_dur = 2.8
    body = [panel(width, height), header(bullet("3", [LARANJA, VERDE]), "Legacy modernization",
                                         f"{len(CHANGES)} MIGRATIONS")]
    for i, (old, new, where, badge) in enumerate(CHANGES):
        y = top + i * step
        cy = y - 5
        enter = 0.2 + i * 0.12
        run_at = 1.2 + i * 0.5
        legacy = closed_station(64, cy) + text(88, y, old, 16, fill=INK_3, extra=' text-decoration="line-through"')
        body.append(appear(f'<g class="flicker" style="animation-delay:{i * 1.3:.1f}s">{legacy}</g>', "rise", enter))
        body.append(
            f'<path d="M300 {cy}H546" stroke="{INK_3}" stroke-opacity=".45" stroke-width="2" '
            'stroke-dasharray="2 7" stroke-linecap="round"/>'
        )
        body.append(train(f"M300,{cy} H546", run_dur, VERDE, begin=run_at, length=18))
        body.append(appear(
            f'<path d="M553 {cy - 6}L559 {cy}L553 {cy + 6}" fill="none" stroke="{VERDE}" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="584" cy="{cy}" r="9" fill="{INK}" stroke="{VERDE}" stroke-width="4"/>'
            + text(606, y, new, 16.5, weight=700) + text(606, y + 20, where, 11.5, "m", INK_3),
            "rise", enter + 0.1))
        body.append(flash(584, cy, VERDE, run_at + 0.95 * run_dur, run_dur, r0=9, r1=24))
        if badge:
            ongoing = badge == "ongoing"
            body.append(appear(pill(width - 44, cy, badge, LARANJA if ongoing else VERDE, dot=ongoing), "pop",
                               enter + 0.3))

    label = "Legacy modernization: " + "; ".join(
        f"{old} to {new} ({where}{', ' + badge if badge else ''})" for old, new, where, badge in CHANGES
    ) + "."
    return document(width, height, label, body, defs=glow())


def contact(theme):
    led = theme["led"]
    width, height = 1000, 240
    cy, sx = 120, 880
    run_at, run_dur = 2.0, 3.6
    title, sentence = CONTACT
    wipe_css, heading = wiped(text(48, 124, title, 52, weight=800, spacing=-1),
                               (44, 72, text_width(title, 52, bold=True) + 20, 70), led, 0.3, 0.8)
    body = [panel(width, height)]
    body.append(appear(text(52, 66, "CONTACT", 13, "m", led, weight=700, spacing=3), "rise", 0))
    body.append(heading)
    body.append(appear(text(52, 160, sentence, 17, fill=INK_2), "rise", 0.9))
    body.append(appear(
        f'<rect class="ring" x="52" y="180" width="160" height="40" rx="20" fill="none" stroke="{led}" stroke-width="2"/>'
        f'<rect x="52" y="180" width="160" height="40" rx="20" fill="{led}"/>'
        + text(132, 205.5, "LinkedIn ↗", 15.5, weight=700, fill=BG, anchor="middle"),
        "pop", 1.1))

    body.append(drawn(f"M640 {cy}H{sx}", led, 0.6, 1.0))
    body.append(train(f"M640,{cy} H{sx - 24}", run_dur, INK, begin=run_at))
    body.append(appear(station(sx, cy, current=led), "pop", 1.5))
    body.append(flash(sx, cy, led, run_at + 0.95 * run_dur, run_dur, r0=14, r1=34))
    body.append(appear(text(sx, cy + 44, "LINKEDIN", 11, "m", INK_3, anchor="middle", spacing=1.5), "rise", 1.6))
    label = f"Contact. {title} {sentence} Find me on LinkedIn."
    return document(width, height, label, body, wipe_css, defs=glow())


def linkedin_button(theme):
    led = theme["led"]
    width, height = 292, 48
    body = [
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="23.25" fill="{PANEL}" '
        f'stroke="{EDGE_HI}" stroke-width="1.5"/>',
        f'<circle cx="24" cy="24" r="15" fill="{led}"/>',
        text(24, 29.5, "in", 15, weight=800, fill=BG, anchor="middle"),
        f'<text class="s" x="50" y="29.5" font-size="15.5"><tspan font-weight="700" fill="{INK}">LinkedIn</tspan>'
        f'<tspan class="m" dx="9" font-size="12" fill="{INK_3}">/in/eduardosantosalm</tspan></text>',
    ]
    return document(width, height, "LinkedIn: eduardosantosalm", body)


def portfolio_button(theme):
    led = theme["led"]
    width, height = 332, 48
    body = [
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="23.25" fill="{PANEL}" '
        f'stroke="{EDGE_HI}" stroke-width="1.5"/>',
        f'<circle cx="24" cy="24" r="15" fill="{led}"/>',
        f'<path d="M18.5 29.5 29 19M21.5 18.5H29.5V26.5" fill="none" stroke="{BG}" stroke-width="2.6" '
        'stroke-linecap="round" stroke-linejoin="round"/>',
        f'<text class="s" x="50" y="29.5" font-size="15.5"><tspan font-weight="700" fill="{INK}">Portfolio</tspan>'
        f'<tspan class="m" dx="9" font-size="12" fill="{INK_3}">eduardo-alecrim.github.io</tspan></text>',
    ]
    return document(width, height, "Portfolio: eduardo-alecrim.github.io", body)


DRAWINGS = {
    "hero.svg": hero,
    "right-now.svg": right_now,
    "stack.svg": stack,
    "modernization.svg": modernization,
    "contact.svg": contact,
    "linkedin.svg": linkedin_button,
    "portfolio.svg": portfolio_button,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--theme", choices=THEMES, default=THEME, help="colour of the signs and highlights")
    parser.add_argument("--out", type=Path, default=ASSETS, help="where to write the SVGs")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, draw in DRAWINGS.items():
        (args.out / name).write_text(draw(THEMES[args.theme]), encoding="utf-8")
        print(f"wrote {args.out / name}")


if __name__ == "__main__":
    main()
