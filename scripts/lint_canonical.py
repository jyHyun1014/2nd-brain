"""Lint canonical pages against SCHEMA.md: frontmatter, tags, sources and ^[raw/...] markers,
>=2 valid outbound wikilinks, orphans, 200-line limit, and index.md entries/sections/order/total.
Usage: python scripts/lint_canonical.py [repo_root]"""
import json, pathlib, re, sys

sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
DIRS = {"entities": "entity", "concepts": "concept", "comparisons": "comparison", "queries": "query"}
REQ = ["title", "created", "updated", "type", "tags", "sources", "confidence", "contested", "contradictions"]
tags_ok = set(re.findall(r"^- `([a-z0-9-]+)`:", (root / "SCHEMA.md").read_text(encoding="utf-8"), re.M))
pages = {p.stem: p for d in DIRS for p in (root / d).glob("*.md")}
errs, links_total = [], 0
inbound = {s: set() for s in pages}

for slug, p in sorted(pages.items()):
    b = p.read_bytes()
    e = lambda m: errs.append(f"{p.relative_to(root).as_posix()}: {m}")
    if b.startswith(b"\xef\xbb\xbf") or b"\r" in b or not b.endswith(b"\n"): e("encoding/EOL")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", slug): e("filename not kebab-case")
    m = re.match(r"---\n(.*?)\n---\n", b.decode("utf-8"), re.S)
    if not m: e("no byte-zero frontmatter"); continue
    fm = {k.strip(): json.loads(v) for k, _, v in (l.partition(":") for l in m.group(1).splitlines())}
    body = b.decode("utf-8")[m.end():]
    for f in REQ:
        if f not in fm: e(f"missing {f}")
    if fm.get("type") != DIRS[p.parent.name]: e("type != directory")
    for f in ("created", "updated"):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(fm.get(f, ""))): e(f"bad {f}")
    if fm.get("confidence") not in ("high", "medium", "low"): e("bad confidence")
    if fm.get("confidence") == "high" and len(fm.get("sources", [])) < 2: e("high confidence with <2 sources")
    if not isinstance(fm.get("contested"), bool): e("contested not boolean")
    if fm.get("contested") is False and fm.get("contradictions"): e("contradictions while not contested")
    for t in fm.get("tags", []):
        if t not in tags_ok: e(f"unregistered tag {t}")
    srcs = fm.get("sources", [])
    if not srcs: e("no sources")
    for s in srcs:
        if not re.match(r"raw/(articles|notebooklm|papers|transcripts|web|youtube)/.+\.md$", s) or not (root / s).is_file():
            e(f"bad source {s}")
    for mk in re.findall(r"\^\[(raw/[^\]]+)\]", body):
        if mk not in srcs: e(f"marker not in sources {mk}")
    targets = set(re.findall(r"\[\[([^\]|#]+)", body))
    for t in targets:
        if t not in pages: e(f"broken link [[{t}]]")
    valid = {t for t in targets if t in pages and t != slug}
    links_total += len(valid)
    for t in valid: inbound[t].add(slug)
    if len(valid) < 2: e(f"only {len(valid)} valid outbound links")
    if len(body.splitlines()) > 200: e("over 200 lines")

for s, src in inbound.items():
    if not src: errs.append(f"orphan page (no inbound links): {s}")

idx = (root / "index.md").read_text(encoding="utf-8")
listed = re.findall(r"^- \[\[([^\]]+)\]\]", idx, re.M)
if sorted(listed) != sorted(pages): errs.append(f"index entries {sorted(listed)} != pages {sorted(pages)}")
if len(set(listed)) != len(listed): errs.append("duplicate index entries")
for sec in re.split(r"^## ", idx, flags=re.M)[1:]:
    names = re.findall(r"^- \[\[([^\]]+)\]\]", sec, re.M)
    if names != sorted(names): errs.append(f"index section not alphabetical: {sec.splitlines()[0]}")
    want = {"Entities": "entities", "Concepts": "concepts", "Comparisons": "comparisons", "Queries": "queries"}[sec.splitlines()[0].strip()]
    for n in names:
        if pages[n].parent.name != want: errs.append(f"{n} listed under wrong section")
total = re.search(r"Total pages: (\d+)", idx)
if not total or int(total.group(1)) != len(pages): errs.append("index total != page count")

print(f"pages {len(pages)}, valid outbound links {links_total}, min inbound {min(map(len, inbound.values()))}")
print("\n".join(errs) or "0 issues")
sys.exit(1 if errs else 0)
