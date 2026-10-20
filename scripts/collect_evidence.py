"""Gate A collect-evidence: capture new papers from one Zotero collection into raw/papers/,
validate raw records, and list Semantic Scholar (most cited) and arXiv (newest) candidates in inbox/.
Settings: scripts/collect_config.json. Usage: python scripts/collect_evidence.py [repo_root]"""
import datetime, hashlib, json, os, pathlib, re, subprocess, sys, time, urllib.error, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
cfg = json.loads((root / "scripts/collect_config.json").read_text(encoding="utf-8"))
ZOTERO = "http://localhost:23119/api/users/0/"
STORAGE = pathlib.Path(os.environ.get("ZOTERO_DATA_DIR", pathlib.Path.home() / "Zotero")) / "storage"
HEADERS = {"User-Agent": "2nd-brain-collect-evidence/1.0 (personal research wiki)"}
today = datetime.date.today().isoformat()
problems = []  # Gate A failures: Zotero capture or raw validation -> exit 1
warnings = []  # candidate search failures: reported, do not fail the gate

def fetch(url, as_json=True, timeout=30):
    headers = dict(HEADERS)
    if url.startswith("https://api.semanticscholar.org/") and os.environ.get("SEMANTIC_SCHOLAR_API_KEY"):
        headers["x-api-key"] = os.environ["SEMANTIC_SCHOLAR_API_KEY"]
    for wait in (10, 30, None):  # keyless Semantic Scholar shares one rate-limit pool: back off on 429/5xx
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                data = r.read()
            return json.loads(data) if as_json else data.decode("utf-8")
        except urllib.error.HTTPError as e:
            if wait is None or (e.code != 429 and e.code < 500):
                raise
            time.sleep(wait)

def zotero_all(path):
    out = []
    while True:
        page = fetch(f"{ZOTERO}{path}?format=json&limit=100&start={len(out)}", timeout=10)
        out += page
        if len(page) < 100:
            return out

def norm(title):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", title.lower()).split())

# --- 1. Zotero collection -> raw/papers/ -------------------------------------------------------
def build_record(d, key):
    children = fetch(f"{ZOTERO}items/{key}/children?format=json", timeout=10)
    attach = sorted(c["key"] for c in children if c["data"]["itemType"] == "attachment")
    pdfs = [c["key"] for c in children if c["data"].get("contentType") == "application/pdf"]
    cache = next((STORAGE / k / ".zotero-ft-cache" for k in pdfs if (STORAGE / k / ".zotero-ft-cache").exists()), None)
    if not cache:
        return None, "no indexed PDF text yet"
    text = cache.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n").rstrip(b"\n") + b"\n"
    text.decode("utf-8")
    bib = fetch(f"{ZOTERO}items/{key}?format=bibtex", as_json=False, timeout=10)
    cite = re.search(r"@\w+\{([^,]+),", bib).group(1)
    authors = [f"{c['lastName']}, {c['firstName']}".strip(", ") if "lastName" in c else c["name"]
               for c in d["creators"] if c["creatorType"] == "author"]
    tags = [t["tag"] for t in d.get("tags", [])]
    publisher = d.get("repository") or d.get("publisher") or d.get("publicationTitle", "")
    missing = [n for n, v in [("title", d.get("title")), ("authors", authors), ("published", d.get("date")),
               ("item_type", d.get("itemType")), ("doi_or_url", d.get("DOI") or d.get("url"))] if not v]
    fm = [("source_type", "zotero"), ("zotero_item_key", key), ("zotero_attachment_keys", attach),
          ("item_type", d["itemType"]), ("title", d["title"]), ("authors", authors),
          ("published", d.get("date")), ("publisher", publisher), ("archive_id", d.get("archiveID")),
          ("doi", d.get("DOI")), ("url", d.get("url")), ("language", d.get("language")),
          ("citation_key", cite), ("zotero_tags", tags), ("zotero_collections", d.get("collections")),
          ("ingested", today), ("metadata_status", "incomplete" if missing else "complete")]
    if missing:
        fm.append(("metadata_missing", missing))
    lines = [f"{k}: {v if k in ('published', 'ingested', 'zotero_item_key') else json.dumps(v, ensure_ascii=False)}"
             for k, v in fm if v not in (None, "", [])]
    block = [f"# {d['title']}", "", "## Zotero Metadata", "",
             f"- Zotero Item Key: {key}", f"- Item Type: {d['itemType']}", f"- Citation Key: {cite}",
             f"- Authors: {'; '.join(authors)}", f"- Published: {d.get('date', '')}"]
    for label, v in [("Publisher", publisher), ("Archive ID", d.get("archiveID")), ("DOI", d.get("DOI")),
                     ("URL", d.get("url")), ("Language", d.get("language"))]:
        if v:
            block.append(f"- {label}: {v}")
    block.append(f"- Attachment Keys: {', '.join(attach)}")
    if tags:
        block.append(f"- Tags: {'; '.join(tags)}")
    if d.get("collections"):
        block.append(f"- Collections: {', '.join(d['collections'])}")
    block += ["", "## Abstract", "", d.get("abstractNote", "").strip(), "", ""]
    body = "\n".join(block).encode("utf-8") + b"## Extracted Text\n\n" + text
    sha = hashlib.sha256(body).hexdigest()
    return ("---\n" + "\n".join(lines) + f"\nsha256: {sha}\n---\n").encode("utf-8") + body, authors

def file_name(d):
    """llm-wiki rule: raw/papers/YYYY-MM-title-slug.md from the most precise publication year/month."""
    date = re.match(r"(\d{4})(?:-(\d{2}))?", d.get("date", ""))
    prefix = [x for x in date.groups() if x] if date else ["undated"]
    return "-".join(prefix + norm(d["title"]).split()) + ".md"

papers = root / "raw/papers"
have = {}
for p in papers.glob("*.md"):
    m = re.search(rb"^zotero_item_key: (\S+)$", p.read_bytes(), re.M)
    if m:
        have[m.group(1).decode()] = p.name
new, pending, skipped, library = [], [], [], []
try:
    library = zotero_all("items/top")
    coll = next((c for c in zotero_all("collections") if c["data"]["name"] == cfg["zotero_collection"]), None)
    if not coll:
        problems.append(f"Zotero collection '{cfg['zotero_collection']}' not found")
    for item in zotero_all(f"collections/{coll['key']}/items/top") if coll else []:
        d, key = item["data"], item["key"]
        if key in have:
            continue
        if d["itemType"] in ("attachment", "note", "annotation"):
            skipped.append(f"{key} ({d['itemType']})")
            continue
        record, authors = build_record(d, key)
        if record is None:
            pending.append(f"{key} {d.get('title', '')[:50]}: {authors}")
            continue
        target = papers / file_name(d)
        if target.exists():
            target = target.with_name(f"{target.stem}-{key.lower()}.md")
        target.write_bytes(record)
        new.append(target.relative_to(root).as_posix())
except (OSError, ValueError) as e:
    problems.append(f"Zotero local API unreachable or failed ({type(e).__name__}); start Zotero and rerun")

val = subprocess.run([sys.executable, str(root / "scripts/validate_raw.py"), str(root)],
                     capture_output=True, text=True, encoding="utf-8")
fails = [l for l in val.stdout.splitlines() if l.startswith("FAIL")]
if val.returncode:
    problems += fails or [f"validate_raw.py exited {val.returncode}"]
if new:
    with open(root / "log.md", "a", encoding="utf-8", newline="\n") as log:
        log.write(f"\n## [{today}] ingest | Zotero collection {cfg['zotero_collection']} ({len(new)} records)\n\n"
                  "Captured by `scripts/collect_evidence.py`: Zotero local API metadata plus the PDF\n"
                  "attachment's `.zotero-ft-cache` text. `sha256` covers the exact post-frontmatter body.\n\n"
                  + "".join(f"- {p}\n" for p in new)
                  + f"\n## [{today}] lint | Raw paper records\n\n"
                  f"`python scripts/validate_raw.py`: {len(fails)} failing record(s)"
                  + ("; Zotero cross-check skipped.\n" if "WARN" in val.stdout else ".\n"))

# --- 2. Candidates -> inbox/ ------------------------------------------------------------------
inbox = root / "inbox"
seen = {norm(i["data"].get("title", "")) for i in library}
seen |= {norm(t) for f in inbox.glob("candidates-*.md")
         for t in re.findall(r"^- \[(.+?)\]\(", f.read_text(encoding="utf-8"), re.M)}

def semantic_scholar(kw):
    q = urllib.parse.urlencode({"query": f'"{kw}"', "sort": "citationCount:desc",
                                "fields": "title,year,citationCount,externalIds,authors,url"})
    for p in fetch(f"https://api.semanticscholar.org/graph/v1/paper/search/bulk?{q}").get("data") or []:
        arxiv = (p.get("externalIds") or {}).get("ArXiv")
        yield {"title": p["title"], "year": p.get("year"), "who": [a["name"] for a in p.get("authors") or []],
               "url": f"https://arxiv.org/abs/{arxiv}" if arxiv else p["url"],
               "note": f"인용 {p.get('citationCount') or 0:,} · Semantic Scholar"}

def arxiv(kw):
    q = urllib.parse.urlencode({"search_query": f'all:"{kw}"', "sortBy": "submittedDate",
                                "sortOrder": "descending", "max_results": 20})
    ns = {"a": "http://www.w3.org/2005/Atom"}
    for e in ET.fromstring(fetch(f"https://export.arxiv.org/api/query?{q}", as_json=False)).findall("a:entry", ns):
        yield {"title": " ".join(e.find("a:title", ns).text.split()), "year": e.find("a:published", ns).text[:4],
               "who": [a.find("a:name", ns).text for a in e.findall("a:author", ns)],
               "url": e.find("a:id", ns).text.replace("http://", "https://"), "note": "최신 · arXiv"}

start = datetime.date.today().toordinal() % len(cfg["keywords"])
keywords = cfg["keywords"][start:] + cfg["keywords"][:start]  # rotate daily so every keyword gets the first slot

def pick(source, slots, pause):
    results = {}
    for kw in keywords:
        try:
            results[kw] = list(source(kw))
        except (OSError, ValueError, ET.ParseError) as e:
            warnings.append(f"{source.__name__} '{kw}' failed ({getattr(e, 'code', type(e).__name__)})")
            results[kw] = []
        time.sleep(pause)
    chosen = []
    while len(chosen) < slots and any(results.values()):
        for kw in keywords:
            while results[kw] and len(chosen) < slots:
                c = results[kw].pop(0)
                if c["title"] and norm(c["title"]) not in seen:
                    seen.add(norm(c["title"]))
                    chosen.append((kw, c))
                    break
    return chosen

slots = cfg["max_candidates"]
picked = pick(semantic_scholar, slots - cfg["arxiv_slots"], 5)
picked += pick(arxiv, slots - len(picked), 3)
out = inbox / f"candidates-{today}.md"
if picked:
    with open(out, "a", encoding="utf-8", newline="\n") as f:
        if f.tell() == 0:
            f.write(f"# 수집 후보 {today}\n\n고른 논문만 Zotero `{cfg['zotero_collection']}` 컬렉션에 추가한다. "
                    "후보 목록일 뿐 evidence가 아니다.\n\n")
        for kw, c in picked:
            who = c["who"][0] + (" 외" if len(c["who"]) > 1 else "") if c["who"] else "저자 미상"
            f.write(f"- [{c['title']}]({c['url']}) — {who}, {c['year'] or '연도 미상'} · {c['note']} · `{kw}`\n")

# --- Report (Hermes delivers stdout verbatim: counts and paths only) ---------------------------
print(f"collect-evidence {today}")
print(f"zotero: new {len(new)}, already captured {len(have)}, pending {len(pending)}, skipped {len(skipped)}")
for line in new + [f"pending {p}" for p in pending] + [f"skipped {s}" for s in skipped]:
    print(f"  {line}")
print(f"validate_raw: {'OK' if not val.returncode else 'FAIL'} ({len(fails)} failing)")
print(f"candidates: {len(picked)}" + (f" -> {out.relative_to(root).as_posix()}" if picked else ""))
for w in warnings:
    print(f"WARN {w}")
for p in problems:
    print(f"PROBLEM {p}")
sys.exit(1 if problems else 0)
