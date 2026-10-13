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
BASE_CSS = (
    f".s{{font-family:{SANS}}}.m{{font-family:{MONO}}}"
    "@keyframes blink{50%{opacity:.25}}.blink{animation:blink 1.4s steps(1) infinite}"
    "@keyframes pulse{from{transform:scale(1);opacity:.9}to{transform:scale(2.3);opacity:0}}"
    ".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}"
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
    out = mark + text(84, 50, title, 25, weight=700)
    if note:
        out += text(width - 40, 48, note, 12, "m", INK_3, anchor="end", spacing=1)
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


def train(path, dur, color, begin="0s", length=20):
    """A lit carriage running along a path, fading in and out at the ends."""
    h = length * 0.375
    return (
        f'<g class="train" opacity="0">'
        f'<rect x="{-length / 2:g}" y="{-h / 2:g}" width="{length}" height="{h:g}" rx="{h / 2:g}" '
        f'fill="{color}" filter="url(#glow)"/>'
        f'<animateMotion path="{path}" dur="{dur}" begin="{begin}" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.05;.95;1" dur="{dur}" '
        f'begin="{begin}" repeatCount="indefinite"/></g>'
    )


def line(x, y1, y2, color):
    """A vertical line diagram running down the left of a panel."""
    return f'<path d="M{x} {y1}V{y2}" stroke="{color}" stroke-width="8" stroke-linecap="round"/>'


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


def chip(x, cy, name, key, color):
    """A tool: its logo and name in a rounded box. Returns markup and width."""
    width = 46 + text_width(name, 15, bold=True) + 16
    return (
        f'<rect x="{x:g}" y="{cy - 19}" width="{width:g}" height="38" rx="19" fill="{CHIP}" '
        f'stroke="{EDGE_HI}"/>'
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

    body = [
        f'<g clip-path="url(#board)"><rect width="{width}" height="{height}" fill="{PANEL}"/>'
        f'<rect width="{width}" height="12" fill="{led}"/></g>'
        f'<rect x="0.75" y="0.75" width="{width - 1.5}" height="{height - 1.5}" rx="18" fill="none" '
        f'stroke="{EDGE}" stroke-width="1.5"/>'
    ]
    body.append(text(52, 66, ROLE, 13, "m", led, weight=700, spacing=3))
    body.append(
        f'<text class="m" x="{width - 52}" y="66" font-size="11" fill="{INK_3}" text-anchor="end" '
        f'letter-spacing="1.5"><tspan fill="{VERDE}">●</tspan> <tspan fill="{LARANJA}">●</tspan>  '
        f"{escape(LOCATION)}</text>"
    )
    body.append(text(46, 152, NAME, 80, weight=800, spacing=-2))
    body.append(text(50, 192, TAGLINE, 18, fill=INK_2))

    body.append(f'<path d="M60 {y}H{width - 60}" stroke="{led}" stroke-width="8" stroke-linecap="round"/>')
    body.append(train(f"M60,{y} H{width - 60}", "7s", INK, begin="0.6s"))
    for x, (what, tools) in zip(xs, FOCUS):
        body.append(station(x, y))
        body.append(text(x, y + 42, what, 16.5, weight=700, anchor="middle"))
        body.append(text(x, y + 64, tools, 12, "m", led, anchor="middle"))

    label = f"{NAME}, Java backend developer in Brasília, Brazil. {TAGLINE} " + "; ".join(
        f"{what}: {tools}" for what, tools in FOCUS
    ) + "."
    defs = f'<clipPath id="board"><rect width="{width}" height="{height}" rx="18"/></clipPath>' + glow()
    return document(width, height, label, body, defs=defs)


def right_now(theme):
    led = theme["led"]
    width = 1000
    top, step = 132, 58
    height = top + step * (len(NOW) - 1) + 56
    body = [panel(width, height), header(bullet("1", [led]), "Right now")]
    body.append(line(64, top, top + step * (len(NOW) - 1), led))
    for i, (label, sentence) in enumerate(NOW):
        y = top + i * step
        body.append(station(64, y, current=led if i == 0 else None))
        body.append(text(98, y - 6, label, 11.5, "m", led, weight=700, spacing=2))
        body.append(text(98, y + 16, sentence, 16))
    label = "Right now. " + " ".join(f"{label.capitalize()}: {sentence}" for label, sentence in NOW)
    return document(width, height, label, body)


def stack(theme):
    led = theme["led"]
    width = 1000
    top, step = 134, 58
    height = top + step * (len(STACK) - 1) + 52
    body = [panel(width, height), header(bullet("2", [VERDE]), "Tech stack")]
    body.append(line(64, top, top + step * (len(STACK) - 1), VERDE))
    for i, (group, tools) in enumerate(STACK):
        y = top + i * step
        body.append(station(64, y))
        body.append(text(98, y + 4, group, 11.5, "m", INK_2, weight=700, spacing=1.5))
        x = 320
        for name, key in tools:
            markup, w = chip(x, y, name, key, led)
            body.append(markup)
            x += w + 12
    label = "Tech stack. " + " ".join(
        f"{group.capitalize()}: {', '.join(name for name, _ in tools)}." for group, tools in STACK
    )
    return document(width, height, label, body)


def modernization(theme):
    width = 1000
    top, step = 138, 58
    height = top + step * (len(CHANGES) - 1) + 56
    body = [panel(width, height), header(bullet("3", [LARANJA, VERDE]), "Legacy modernization",
                                         f"{len(CHANGES)} MIGRATIONS")]
    for i, (old, new, where, badge) in enumerate(CHANGES):
        y = top + i * step
        cy = y - 5
        body.append(closed_station(64, cy))
        body.append(text(88, y, old, 16, fill=INK_3, extra=' text-decoration="line-through"'))
        body.append(
            f'<path d="M300 {cy}H546" stroke="{INK_3}" stroke-opacity=".45" stroke-width="2" '
            'stroke-dasharray="2 7" stroke-linecap="round"/>'
        )
        body.append(train(f"M300,{cy} H546", "2.8s", VERDE, begin=f"{i * 0.5:.1f}s", length=18))
        body.append(
            f'<path d="M553 {cy - 6}L559 {cy}L553 {cy + 6}" fill="none" stroke="{VERDE}" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="584" cy="{cy}" r="9" fill="{INK}" stroke="{VERDE}" stroke-width="4"/>'
        )
        body.append(text(606, y, new, 16.5, weight=700))
        body.append(text(606, y + 20, where, 11.5, "m", INK_3))
        if badge:
            ongoing = badge == "ongoing"
            body.append(pill(width - 44, cy, badge, LARANJA if ongoing else VERDE, dot=ongoing))

    label = "Legacy modernization: " + "; ".join(
        f"{old} to {new} ({where}{', ' + badge if badge else ''})" for old, new, where, badge in CHANGES
    ) + "."
    return document(width, height, label, body, defs=glow())


def contact(theme):
    led = theme["led"]
    width, height = 1000, 240
    cy, sx = 120, 880
    title, sentence = CONTACT
    body = [panel(width, height)]
    body.append(text(52, 66, "CONTACT", 13, "m", led, weight=700, spacing=3))
    body.append(text(48, 124, title, 52, weight=800, spacing=-1))
    body.append(text(52, 160, sentence, 17, fill=INK_2))
    body.append(f'<rect x="52" y="180" width="160" height="40" rx="20" fill="{led}"/>')
    body.append(text(132, 205.5, "LinkedIn ↗", 15.5, weight=700, fill=BG, anchor="middle"))

    body.append(f'<path d="M640 {cy}H{sx}" stroke="{led}" stroke-width="8" stroke-linecap="round"/>')
    body.append(train(f"M640,{cy} H{sx - 24}", "3.6s", INK))
    body.append(station(sx, cy, current=led))
    body.append(text(sx, cy + 44, "LINKEDIN", 11, "m", INK_3, anchor="middle", spacing=1.5))
    label = f"Contact. {title} {sentence} Find me on LinkedIn."
    return document(width, height, label, body, defs=glow())


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


DRAWINGS = {
    "hero.svg": hero,
    "right-now.svg": right_now,
    "stack.svg": stack,
    "modernization.svg": modernization,
    "contact.svg": contact,
    "linkedin.svg": linkedin_button,
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
