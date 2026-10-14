"""Validate raw source records against SCHEMA.md. Usage: python scripts/validate_raw.py [repo_root]"""
import hashlib, json, pathlib, re, sys, urllib.error, urllib.request

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent)
REGISTERED = {"articles", "notebooklm", "papers", "transcripts", "web", "youtube"}
PAPER_FIELDS = ["title", "authors", "year", "doi", "url", "zotero_key", "captured", "sha256"]
zotero_up = True
fails = 0

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
            fm[k.strip()] = v.strip()
        if fm.get("sha256") != hashlib.sha256(b[m.end():]).hexdigest(): errs.append("sha256 mismatch")
        if rel.startswith("raw/papers/"):
            errs += [f"missing {f}" for f in PAPER_FIELDS if not fm.get(f)]
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm.get("captured", "")): errs.append("bad captured date")
            z = zotero(fm.get("zotero_key", "")) if zotero_up and fm.get("zotero_key") else None
            if z and "_error" in z: errs.append(f"zotero lookup failed: {z['_error']}")
            elif z:
                if fm.get("title") and json.loads(fm["title"]) != z.get("title"): errs.append("title != Zotero")
                if fm.get("doi") and json.loads(fm["doi"]) != z.get("DOI"): errs.append("doi != Zotero")
    fails += bool(errs)
    print(("FAIL " if errs else "OK   ") + rel + ("  -> " + ", ".join(errs) if errs else ""))

if not zotero_up:
    print("\nWARN Zotero local API unreachable; Zotero cross-check skipped. Start Zotero and rerun.")
print(f"\n{fails} failing record(s)")
sys.exit(1 if fails else 0)
