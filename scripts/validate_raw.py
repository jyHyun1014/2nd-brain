"""Validate raw source records against SCHEMA.md and the llm-wiki Zotero schema. Usage: python scripts/validate_raw.py [repo_root]"""
import hashlib, json, pathlib, re, sys, urllib.error, urllib.request

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
REGISTERED = {"articles", "notebooklm", "papers", "transcripts", "web", "youtube"}
ZOTERO_REQUIRED = ["zotero_item_key", "item_type", "title", "authors", "published", "ingested", "metadata_status", "sha256"]
zotero_up = True
fails = 0
keys = {}

def zotero(key):
    global zotero_up
    try:
        with urllib.request.urlopen(f"http://localhost:23119/api/users/0/items/{key}", timeout=5) as r:
            return json.load(r)["data"]
    except urllib.error.HTTPError as e:
        return {"_error": f"HTTP {e.code}"}
    except OSError:
        zotero_up = False
        return None

def value(v):
    try: return json.loads(v)
    except ValueError: return v

for p in sorted(root.glob("raw/**/*.md")):
    rel = p.relative_to(root).as_posix()
    b = p.read_bytes()
    errs = []
    if rel.split("/")[1] not in REGISTERED: errs.append("unregistered source dir")
    if b.startswith(b"\xef\xbb\xbf"): errs.append("BOM")
    if b"\r" in b: errs.append("CR")
    if not b.endswith(b"\n"): errs.append("no final LF")
    try: b.decode("utf-8")
    except UnicodeDecodeError: errs.append("not UTF-8")
    m = re.match(rb"---\n(.*?)\n---\n", b, re.S)
    if not m:
        errs.append("no byte-zero frontmatter")
    else:
        fm = {}
        for line in m.group(1).decode(errors="replace").splitlines():
            k, _, v = line.partition(":")
            fm[k.strip()] = value(v.strip())
        body = b[m.end():]
        if fm.get("sha256") != hashlib.sha256(body).hexdigest(): errs.append("sha256 mismatch")
        if fm.get("source_type") == "zotero":
            missing = [f for f in ZOTERO_REQUIRED if not fm.get(f)]
            if not (fm.get("doi") or fm.get("url")): missing.append("doi_or_url")
            errs += [f"missing {f}" for f in missing]
            if fm.get("metadata_status") not in ("complete", "incomplete"): errs.append("bad metadata_status")
            if fm.get("metadata_status") == "complete" and missing: errs.append("complete despite missing fields")
            if not isinstance(fm.get("authors"), list): errs.append("authors not a list")
            for f in ("published", "ingested"):
                if not re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", str(fm.get(f, ""))): errs.append(f"bad {f} date")
            if b"\n## Zotero Metadata\n" not in body: errs.append("no ## Zotero Metadata")
            if b"\n## Extracted Text\n" not in body: errs.append("no ## Extracted Text")
            key = str(fm.get("zotero_item_key", ""))
            if key in keys: errs.append(f"duplicate zotero_item_key with {keys[key]}")
            keys.setdefault(key, rel)
            z = zotero(key) if zotero_up and key else None
            if z and "_error" in z: errs.append(f"zotero lookup failed: {z['_error']}")
            elif z:
                if z.get("itemType") in ("attachment", "note", "annotation"): errs.append("zotero_item_key is not a parent item")
                if fm.get("title") != z.get("title"): errs.append("title != Zotero")
                if fm.get("doi") and fm.get("doi") != z.get("DOI"): errs.append("doi != Zotero")
        elif rel.startswith("raw/papers/"):
            errs.append("paper record without source_type: zotero")
    fails += bool(errs)
    print(("FAIL " if errs else "OK   ") + rel + ("  -> " + ", ".join(errs) if errs else ""))

if not zotero_up:
    print("\nWARN Zotero local API unreachable; Zotero cross-check skipped. Start Zotero and rerun.")
print(f"\n{fails} failing record(s)")
sys.exit(1 if fails else 0)
