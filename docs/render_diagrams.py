"""Generate the three current-state 2nd-brain diagrams as SVG."""
import pathlib, sys
from html import escape

OUT = pathlib.Path(sys.argv[1])
FONT = "font-family=\"'Segoe UI','Malgun Gothic',Arial,sans-serif\""
C = {"ink": "#1f2937", "muted": "#6b7280", "line": "#475569",
     "ev": ("#eef6ff", "#3b82f6"), "can": ("#ecfdf5", "#10b981"),
     "dis": ("#fff7ed", "#f59e0b"), "dec": ("#fdf2f8", "#db2777"),
     "ctl": ("#f5f3ff", "#7c3aed"), "gray": ("#f8fafc", "#94a3b8")}


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT}>'
            '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{C["line"]}"/></marker></defs>'
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>'
            f'<text x="30" y="42" font-size="24" font-weight="700" fill="{C["ink"]}">{escape(title)}</text>'
            + "".join(body) + "</svg>")


def box(x, y, w, h, pal, head, lines, sub=None):
    fill, stroke = C[pal]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>']
    ty = y + 26
    if sub:
        out.append(f'<text x="{x+12}" y="{ty}" font-size="12" font-weight="600" fill="{stroke}">{escape(sub)}</text>')
        ty += 20
    out.append(f'<text x="{x+12}" y="{ty}" font-size="16" font-weight="700" fill="{C["ink"]}">{escape(head)}</text>')
    for i, ln in enumerate(lines):
        out.append(f'<text x="{x+12}" y="{ty+22+i*19}" font-size="13" fill="{C["ink"]}">{escape(ln)}</text>')
    return "".join(out)


def arrow(pts, dash=False):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    extra = ' stroke-dasharray="6 5"' if dash else ""
    return f'<path d="{d}" fill="none" stroke="{C["line"]}" stroke-width="2"{extra} marker-end="url(#a)"/>'


def note(x, y, text, size=13, color=None, weight=400):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{color or C["muted"]}">{escape(text)}</text>'


def chips(x, y, items, pal):
    fill, stroke = C[pal]
    out = []
    for t in items:
        w = int(len(t) * 7.6) + 24
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="15" fill="#ffffff" stroke="{stroke}" stroke-width="1.5"/>'
                   f'<text x="{x+12}" y="{y+20}" font-size="13" fill="{C["ink"]}">{escape(t)}</text>')
        x += w + 10
    return "".join(out)


# 1. Workflow
B, W_, Y = 175, 172, 80
xs = [30 + i * (W_ + 22) for i in range(6)]
row1 = [
    ("gray", "Capture", ["Add paper to Zotero", "'2nd-brain' collection"], "Manual"),
    ("ev", "Gate A: collect", ["collect_evidence.py", "→ raw/papers/ + sha256", "validate_raw.py", "candidates → inbox/"], "Daily 10:00 · Hermes script"),
    ("can", "Gate B: compile", ["Hermes agent + llm-wiki", "→ wiki/compile-<date>", "self-check vs raw/", "lint_canonical.py"], "Daily 11:00 · Hermes agent"),
    ("ctl", "Review", ["Claude Code", "review prompt (scripts/)", "re-check every claim", "report + recommendation"], "On request"),
    ("dec", "Human decision", ["Approve → merge + push", "Reject → discard branch", "(user decides only)"], "Human-in-the-Loop"),
    ("can", "Second Brain", ["main branch:", "canonical pages,", "index.md, log.md"], "Durable memory"),
]
body = [box(x, Y, W_, B, p, h, l, s) for x, (p, h, l, s) in zip(xs, row1)]
for i in range(5):
    body.append(arrow([(xs[i] + W_, Y + B / 2), (xs[i + 1] - 2, Y + B / 2)]))
Y2 = 330
body += [
    box(xs[2], Y2, W_, 115, "dis", "New knowledge", ["candidates", "(hypotheses only)"]),
    box(xs[3], Y2, W_, 115, "dis", "NotebookLM", ["Q&A over raw/", "paper records"]),
    box(xs[4], Y2, W_, 115, "dis", "UA graph", ["Understand Anything,", "from canonical pages"]),
    box(xs[5], Y2, W_, 115, "gray", "Obsidian", ["read, edit,", "graph view"]),
    arrow([(xs[5] + W_ / 2, Y + B), (xs[5] + W_ / 2, Y2 - 2)]),
    arrow([(xs[5], Y2 + 57), (xs[4] + W_ + 2, Y2 + 57)]),
    arrow([(xs[3], Y2 + 57), (xs[2] + W_ + 2, Y2 + 57)]),
    arrow([(xs[4] + W_ / 2, Y2 + 115), (xs[4] + W_ / 2, Y2 + 140), (xs[2] + W_ / 2, Y2 + 140), (xs[2] + W_ / 2, Y2 + 117)]),
    arrow([(xs[2] + W_ / 2, Y2), (xs[2] + W_ / 2, Y2 - 40), (xs[3] + W_ / 2, Y2 - 40), (xs[3] + W_ / 2, Y + B + 2)], dash=True),
    note(xs[2] + W_ / 2 + 8, Y2 - 48, "verify against raw/ first"),
    note(30, 530, "Rules: raw/ bodies are immutable · every claim traces to raw/ · discovery output is never evidence · nothing reaches main without the user's decision", 13, C["ink"]),
    note(30, 554, "Hermes runs locally; its model provider and API keys live in the Hermes data directory, never in this repository. Not yet automated: graph rebuild, review step."),
]
(OUT / "workflow/second-brain-workflow-current.svg").write_text(
    svg(1200, 580, body, "2nd-Brain operating workflow (current, 2026-11)"), encoding="utf-8")

# 2. Architecture
bands = [
    ("ev", "1. Evidence", "raw/ — immutable source bodies, Zotero metadata, sha256", ["Zotero", "raw/papers/", "validate_raw.py", "gitignored (local only)"]),
    ("can", "2. Canonical Memory", "Compiled, sourced Markdown with frontmatter and wikilinks", ["entities/ concepts/", "comparisons/ queries/", "index.md · log.md", "SCHEMA.md", "lint_canonical.py"]),
    ("dis", "3. Discovery", "Focused Q&A and graph analysis → hypotheses, not evidence", ["NotebookLM (raw records)", "Understand Anything (.ua/)", "Obsidian graph"]),
    ("dec", "4. Human Decision", "Claude Code verifies and reports; the user approves or rejects", ["review_compile_prompt.md", "approve → merge + push", "reject → discard"]),
]
body, bx, bw, bh = [], 50, 840, 115
for i, (p, head, desc, items) in enumerate(bands):
    y = 80 + i * 145
    fill, stroke = C[p]
    body += [f'<rect x="{bx}" y="{y}" width="{bw}" height="{bh}" rx="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
             note(bx + 18, y + 32, head, 18, C["ink"], 700), note(bx + 18, y + 56, desc, 13, C["ink"]),
             chips(bx + 18, y + 72, items, p)]
    if i < 3:
        body.append(arrow([(470, y + bh), (470, y + 143)]))
labels = ["compile (Gate B)", "explore", "candidates"]
for i, t in enumerate(labels):
    body.append(note(480, 80 + i * 145 + bh + 20, t))
body.append(arrow([(bx, 80 + 3 * 145 + 57), (25, 80 + 3 * 145 + 57), (25, 80 + 145 + 57), (bx - 2, 80 + 145 + 57)]))
body.append(note(30, 80 + 2 * 145 + 140, "approved", 12))
cx, cy, cw, ch = 920, 80, 250, 550
body += [f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="12" fill="{C["ctl"][0]}" stroke="{C["ctl"][1]}" stroke-width="2"/>',
         note(cx + 16, cy + 32, "Automation Control Plane", 17, C["ink"], 700),
         note(cx + 16, cy + 54, "Hermes Agent (local cron)", 13, C["ctl"][1], 600)]
ctl = [("10:00 collect-evidence", "script only → Evidence"), ("11:00 compile-wiki", "agent + llm-wiki → branch"),
       ("Guardrails", "deny push / merge / rm raw"), ("Model provider", "OpenAI-compatible API"),
       ("Planned", "UA graph rebuild, review run")]
for i, (h, d) in enumerate(ctl):
    y = cy + 80 + i * 92
    body += [f'<rect x="{cx+14}" y="{y}" width="{cw-28}" height="76" rx="8" fill="#ffffff" stroke="{C["ctl"][1]}" stroke-width="1.2"{" stroke-dasharray=\"5 4\"" if h == "Planned" else ""}/>',
             note(cx + 26, y + 30, h, 14, C["ink"], 700), note(cx + 26, y + 54, d, 13)]
body += [arrow([(cx, 80 + 57), (bx + bw + 2, 80 + 57)]), arrow([(cx, 225 + 57), (bx + bw + 2, 225 + 57)])]
body.append(note(30, 680, "Core assets are open formats (Markdown, YAML frontmatter, raw text + sha256) and Git history; every tool above is replaceable."))
(OUT / "architecture/second-brain-pkm-architecture-current.svg").write_text(
    svg(1200, 700, body, "2nd-Brain architecture (current, 2026-11)"), encoding="utf-8")

# 3. Tech stack
rows = [
    ("dec", "Review & decision", ["Claude Code", "review_compile_prompt.md", "GitHub (main)"]),
    ("dis", "Discovery", ["NotebookLM", "notebooklm-py CLI", "Understand Anything", "Obsidian graph view"]),
    ("can", "Compile & validate", ["Hermes Agent cron", "llm-wiki skill", "OpenAI-compatible model API", "lint_canonical.py"]),
    ("ev", "Capture", ["Zotero + Connector", "Zotero local API / MCP", "Obsidian Web Clipper", "collect_evidence.py", "validate_raw.py"]),
    ("gray", "Durable assets", ["raw/ text + sha256", "Markdown + YAML frontmatter", "[[wikilinks]]", "index.md · log.md", "Git history"]),
]
body = []
for i, (p, head, items) in enumerate(rows):
    y = 75 + i * 92
    fill, stroke = C[p]
    body += [f'<rect x="30" y="{y}" width="1140" height="78" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
             note(48, y + 44, head, 16, C["ink"], 700), chips(240, y + 24, items, p)]
body.append(note(30, 555, "Bottom layer is what lasts; upper layers are replaceable tools. Obsidian is the editing surface over the same Markdown files."))
(OUT / "tech-stack/second-brain-technology-stack-current.svg").write_text(
    svg(1200, 580, body, "2nd-Brain technology stack (current, 2026-11)"), encoding="utf-8")
print("ok")
