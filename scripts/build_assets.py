"""Generates the SVG images used by the profile README.

Run from the repository root:  python scripts/build_assets.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

BG = "#0D1117"
PANEL = "#161B22"
BORDER = "#30363D"
DOT = "#21262D"
TEXT = "#E6EDF3"
SUB = "#C9D1D9"
MUTED = "#8B949E"

JAVA = "#F89820"
SPRING = "#6DB33F"
KAFKA = "#58A6FF"
DOTNET = "#A371F7"
OPENSHIFT = "#F85149"
AMBER = "#D29922"
GREEN = "#3FB950"

STYLE = """<style>
.sans{font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}
.mono{font-family:'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace}
@keyframes flow{to{stroke-dashoffset:-28}}
.flow{stroke-dasharray:4 10;animation:flow 1s linear infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.3}}
.pulse{animation:pulse 1.6s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){.flow,.pulse{animation:none}}
</style>"""

DOTS = (
    '<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">'
    f'<circle cx="2" cy="2" r="1.2" fill="{DOT}"/></pattern>'
)


def svg(width, height, label, body, extra_defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(label)}">'
        f"<defs>{STYLE}{DOTS}{extra_defs}</defs>{''.join(body)}</svg>"
    )


def packets(path, color, dur, count, r=3.5):
    """Message dots travelling along a path, evenly spaced in time."""
    return "".join(
        f'<circle r="{r}" fill="{color}"><animateMotion dur="{dur}s" '
        f'begin="-{dur * i / count:.2f}s" repeatCount="indefinite" path="{path}"/></circle>'
        for i in range(count)
    )


def link(path, color, dur, count, r=3.5):
    return (
        f'<path d="{path}" stroke="{BORDER}" stroke-width="2.5" stroke-linecap="round"/>'
        f'<path class="flow" d="{path}" stroke="{color}" stroke-width="2.5" '
        f'stroke-linecap="round" stroke-opacity="0.8"/>' + packets(path, color, dur, count, r)
    )


def icon(x, y, size, tag, color):
    font = 15 if len(tag) <= 2 else 12
    return (
        f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="10" fill="{color}" '
        f'fill-opacity="0.15" stroke="{color}" stroke-opacity="0.6"/>'
        f'<text class="mono" x="{x + size / 2}" y="{y + size / 2 + font / 3}" text-anchor="middle" '
        f'font-size="{font}" font-weight="700" fill="{color}">{escape(tag)}</text>'
    )


def hero():
    w, h = 1200, 420
    glows = (
        '<radialGradient id="glowA" cx="0.88" cy="0.12" r="0.5">'
        f'<stop offset="0" stop-color="{JAVA}" stop-opacity="0.18"/>'
        f'<stop offset="1" stop-color="{JAVA}" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="glowB" cx="0.05" cy="0.95" r="0.45">'
        f'<stop offset="0" stop-color="{KAFKA}" stop-opacity="0.12"/>'
        f'<stop offset="1" stop-color="{KAFKA}" stop-opacity="0"/></radialGradient>'
    )
    body = [
        f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>',
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>',
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#glowA)"/>',
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#glowB)"/>',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{BORDER}"/>',
        # Terminal-style title bar
        f'<path d="M0,16 a16,16 0 0 1 16,-16 H{w - 16} a16,16 0 0 1 16,16 V52 H0 Z" fill="{PANEL}"/>',
        f'<line x1="0" y1="52" x2="{w}" y2="52" stroke="{BORDER}"/>',
        *(f'<circle cx="{28 + i * 20}" cy="26" r="6" fill="{c}"/>' for i, c in enumerate((OPENSHIFT, AMBER, GREEN))),
        f'<text class="mono" x="100" y="31" font-size="14" fill="{MUTED}">$ kafka-console-consumer --topic '
        f'<tspan fill="{SUB}">eduardo.profile</tspan> --from-beginning</text>',
        f'<circle class="pulse" cx="1080" cy="26" r="5" fill="{GREEN}"/>',
        f'<text class="mono" x="1092" y="31" font-size="13" fill="{SUB}">streaming</text>',
        # Name and headline
        f'<text class="sans" x="60" y="146" font-size="60" font-weight="800" fill="{TEXT}" '
        f'letter-spacing="-1">Eduardo <tspan fill="{JAVA}">Alecrim</tspan></text>',
        f'<text class="sans" x="62" y="188" font-size="22" font-weight="500" fill="{SUB}">'
        "Java Backend Developer · Spring Boot · Quarkus · Kafka</text>",
        f'<text class="mono" x="62" y="220" font-size="14" fill="{MUTED}">'
        "// modernizing legacy systems into event-driven services</text>",
    ]

    bx, by = 780, 82
    body += [
        f'<rect x="{bx}" y="{by}" width="360" height="140" rx="10" fill="{JAVA}" fill-opacity="0.07" '
        f'stroke="{JAVA}" stroke-opacity="0.35"/>',
        f'<text class="mono" x="{bx + 20}" y="{by + 28}" font-size="12" font-weight="700" fill="{JAVA}" '
        'letter-spacing="1.5">CURRENTLY @ CASSI</text>',
    ]
    for i, line in enumerate(("Event-driven services · Kafka", "ASP.NET MVC → Java + React", "OpenShift 3 → OpenShift 4")):
        body.append(f'<text class="mono" x="{bx + 20}" y="{by + 56 + i * 24}" font-size="14" fill="{SUB}">{escape(line)}</text>')
    body.append(f'<text class="mono" x="{bx + 20}" y="{by + 126}" font-size="12" fill="{MUTED}">supplementary healthcare · Brasília</text>')

    # Pipeline: legacy in, event-driven services out
    nodes = (
        ("SOA", "Legacy", "Oracle SOA · ASP.NET", DOTNET),
        ("SB", "Spring Boot", "Quarkus · REST · SOAP", SPRING),
        ("K", "Apache Kafka", "event-driven · topics", KAFKA),
        ("OS", "OpenShift", "containers · deploy", OPENSHIFT),
    )
    node_w, node_h, ny = 228, 76, 262
    xs = (60, 344, 628, 912)
    mid = ny + node_h // 2
    for i in range(len(xs) - 1):
        body.append(link(f"M{xs[i] + node_w},{mid} L{xs[i + 1]},{mid}", nodes[i + 1][3], dur=1.4, count=1))
    for x, (tag, title, sub, color) in zip(xs, nodes):
        body += [
            f'<rect x="{x}" y="{ny}" width="{node_w}" height="{node_h}" rx="14" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>',
            icon(x + 14, ny + 16, 44, tag, color),
            f'<text class="sans" x="{x + 72}" y="{ny + 34}" font-size="16" font-weight="700" fill="{TEXT}">{escape(title)}</text>',
            f'<text class="mono" x="{x + 72}" y="{ny + 54}" font-size="11" fill="{MUTED}">{escape(sub)}</text>',
            f'<circle cx="{x}" cy="{mid}" r="5" fill="{BG}" stroke="{MUTED}" stroke-width="1.5"/>',
            f'<circle cx="{x + node_w}" cy="{mid}" r="5" fill="{MUTED}"/>',
        ]

    body += [
        f'<text class="mono" x="60" y="392" font-size="12" fill="{MUTED}"><tspan fill="{GREEN}">●</tspan> '
        "4+ years in Java · CAST group → CASSI</text>",
        f'<text class="mono" x="1140" y="392" text-anchor="end" font-size="12" fill="{MUTED}">Brasília, Brazil</text>',
    ]
    return svg(w, h, "Eduardo Alecrim, Java Backend Developer: Spring Boot, Quarkus, Kafka, OpenShift", body, glows)


def section(number, title, color):
    w, h, pill = 1200, 64, 230
    body = [
        f'<rect x="1" y="8" width="{pill}" height="48" rx="12" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<rect x="10" y="16" width="32" height="32" rx="8" fill="{color}" fill-opacity="0.15" stroke="{color}" stroke-opacity="0.6"/>',
        f'<text class="mono" x="26" y="37" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">{number}</text>',
        f'<text class="sans" x="56" y="38" font-size="17" font-weight="700" fill="{TEXT}" letter-spacing="2">{escape(title)}</text>',
        f'<circle cx="{pill + 1}" cy="32" r="4.5" fill="{MUTED}"/>',
        link(f"M{pill + 1},32 L1188,32", color, dur=7, count=3, r=4),
        f'<circle cx="1188" cy="32" r="6" fill="{BG}" stroke="{color}" stroke-width="2"/>',
    ]
    return svg(w, h, title, body)


def card(tag, title, meta, description, status, status_color, tags, color, live=False):
    w, h = 400, 220
    body = [
        f'<rect width="{w}" height="{h}" rx="16" fill="{PANEL}"/>',
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>',
        f'<rect x="0.75" y="0.75" width="{w - 1.5}" height="{h - 1.5}" rx="16" fill="none" stroke="{BORDER}" stroke-width="1.5"/>',
        f'<path d="M18,1.5 H{w - 18}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>',
        icon(22, 26, 44, tag, color),
        f'<text class="sans" x="80" y="46" font-size="19" font-weight="700" fill="{TEXT}">{escape(title)}</text>',
        f'<text class="mono" x="80" y="67" font-size="12" fill="{MUTED}">{escape(meta)}</text>',
        *(
            f'<text class="sans" x="24" y="{104 + i * 21}" font-size="15" fill="{SUB}">{escape(line)}</text>'
            for i, line in enumerate(description)
        ),
        f'<line x1="22" y1="168" x2="{w - 22}" y2="168" stroke="{BORDER}"/>',
        f'<circle{" class=\"pulse\"" if live else ""} cx="28" cy="192" r="4" fill="{status_color}"/>',
        f'<text class="mono" x="40" y="196" font-size="12" fill="{MUTED}">{escape(status)}</text>',
        f'<text class="mono" x="{w - 24}" y="196" text-anchor="end" font-size="12" font-weight="700" fill="{color}">{escape(tags)}</text>',
    ]
    return svg(w, h, f"{title}: {' '.join(description)}", body)


def areas():
    """Four panels summarizing what I work with."""
    w, h, gap = 1200, 232, 20
    panel_w = (w - 3 * gap) // 4
    columns = (
        ("JV", "BACKEND", JAVA, ("Java", "Spring Boot", "Quarkus", "REST · SOAP")),
        ("EV", "INTEGRATION", KAFKA, ("Apache Kafka", "Apache Camel", "Oracle SOA", "SOAP → REST")),
        ("DB", "DATA", AMBER, ("SQL Server", "Oracle", "Data modeling")),
        ("OS", "PLATFORM", OPENSHIFT, ("OpenShift", "Containers", "React", "ASP.NET MVC · C#")),
    )
    body = []
    for i, (tag, title, color, items) in enumerate(columns):
        x = i * (panel_w + gap)
        body += [
            f'<rect x="{x + 0.75}" y="0.75" width="{panel_w - 1.5}" height="{h - 1.5}" rx="16" fill="{PANEL}" stroke="{BORDER}" stroke-width="1.5"/>',
            f'<rect x="{x}" y="0" width="{panel_w}" height="{h}" rx="16" fill="url(#dots)"/>',
            f'<path d="M{x + 18},1.5 H{x + panel_w - 18}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>',
            icon(x + 20, 22, 44, tag, color),
            f'<text class="sans" x="{x + 78}" y="50" font-size="17" font-weight="700" fill="{TEXT}" letter-spacing="1.5">{title}</text>',
            *(
                f'<text class="mono" x="{x + 24}" y="{108 + j * 30}" font-size="16" fill="{SUB}">'
                f'<tspan fill="{color}">▸</tspan> {escape(item)}</text>'
                for j, item in enumerate(items)
            ),
        ]
    return svg(w, h, "Backend, integration, data and platform skills", body)


def footer():
    w, h = 1200, 100
    body = [
        f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>',
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#dots)"/>',
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="none" stroke="{BORDER}"/>',
        link("M40,52 L410,52", JAVA, dur=4, count=2),
        link("M790,52 L1160,52", JAVA, dur=4, count=2),
        f'<circle cx="40" cy="52" r="5" fill="{MUTED}"/>',
        f'<circle cx="1160" cy="52" r="6" fill="{BG}" stroke="{JAVA}" stroke-width="2"/>',
        f'<text class="mono" x="600" y="50" text-anchor="middle" font-size="14" fill="{SUB}"># end of stream · thanks for stopping by</text>',
        f'<text class="mono" x="600" y="72" text-anchor="middle" font-size="12" fill="{MUTED}">fim do stream · obrigado pela visita</text>',
    ]
    return svg(w, h, "End of stream, thanks for stopping by", body)


CARDS = {
    "card-oracle-soa": card(
        "SOA", "Oracle SOA → Spring Boot", "CAST group · 2023 – 2024",
        ("Migrated every SOAP service from the Oracle", "SOA platform to Spring Boot apps, turning", "SOAP services into REST APIs."),
        "shipped", GREEN, "Spring Boot · REST · OpenShift", SPRING,
    ),
    "card-kafka": card(
        "K", "Event-driven services", "CASSI · 2024 – present",
        ("Backend services with Spring Boot and", "Quarkus, plus event-driven applications", "built on Apache Kafka."),
        "active", GREEN, "Kafka · Quarkus · Spring Boot", KAFKA, live=True,
    ),
    "card-aspnet-react": card(
        "NET", "ASP.NET MVC → Java + React", "CASSI · 2024 – present",
        ("Migrating legacy ASP.NET MVC 4.6 projects", "to a new architecture with a Java backend", "and a React frontend."),
        "in progress", AMBER, "Java · React", DOTNET, live=True,
    ),
    "card-openshift": card(
        "OS", "OpenShift 3 → 4", "CASSI · 2024 – present",
        ("Migrating legacy applications from", "OpenShift 3 to OpenShift 4."),
        "in progress", AMBER, "OpenShift · Containers", OPENSHIFT, live=True,
    ),
    "card-camel": card(
        "CML", "Apache Camel → Spring Boot", "CAST group · 2022 – 2023",
        ("Migrated legacy Apache Camel projects to", "Spring Boot, modernizing the integration", "architecture."),
        "shipped", GREEN, "Camel · Spring Boot", JAVA,
    ),
    "card-data-modeling": card(
        "DB", "Data modeling", "CASSI · SQL Server",
        ("Designing SQL Server databases for new", "applications: data structures and entity", "relationships."),
        "active", GREEN, "SQL Server", AMBER, live=True,
    ),
}


def main():
    ASSETS.mkdir(exist_ok=True)
    files = {
        "hero": hero(),
        "areas": areas(),
        "sec-about": section("01", "ABOUT ME", JAVA),
        "sec-stack": section("02", "TECH STACK", SPRING),
        "sec-highlights": section("03", "HIGHLIGHTS", KAFKA),
        "sec-connect": section("04", "CONNECT", OPENSHIFT),
        "footer": footer(),
        **CARDS,
    }
    for name, content in files.items():
        (ASSETS / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(files)} files to {ASSETS}")


if __name__ == "__main__":
    main()
