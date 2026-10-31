# PROJECT KNOWLEDGE BASE

**Generated:** 
**Commit:** 
**Branch:** main

## OVERVIEW

- Markdown/Obsidian second-brain template using an evidence-first LLM wiki model.
- The repository root is the wiki root; no database, service, or build system exists.
- `SCHEMA.md` is the operational contract. `README.md` covers optional tool setup
  but describes a generic PARA layout that is not the current repository structure.
- Current curated state: 25 raw paper records (local only) and 23 canonical pages.
- Daily automation (Hermes cron, this machine): `collect-evidence` at 10:00
  (script-only, Gate A) and `compile-wiki` at 11:00 (agent with `llm-wiki`,
  Gate B, commits to a `wiki/compile-<date>` branch).
- Human-in-the-Loop: a coding agent reviews each compile branch with
  `scripts/review_compile_prompt.md` and reports; the branch is merged and
  pushed, or discarded, only after the user approves or rejects. Never merge
  AI-generated knowledge without that decision.
- Discovery is manual: the NotebookLM notebook holds the raw records, and the
  UA knowledge graph (`.ua/`) is built from canonical pages. Both produce
  hypotheses, never evidence.

## START HERE

1. Read `SCHEMA.md` completely.
2. Read `index.md` to find existing canonical subjects and avoid duplicates.
3. Read the newest entries in append-only `log.md` before changing the wiki.
4. Resolve every path relative to this repository root.

## STRUCTURE

```text
./
├── inbox/                 # Temporary intake; neither evidence nor canonical
├── raw/                   # Gitignored except .gitkeep: source text stays local
│   ├── articles/          # Immutable captured article Markdown
│   ├── notebooklm/        # Immutable NotebookLM-imported source records
│   ├── papers/            # Immutable captured paper Markdown (Zotero metadata + full text)
│   │   └── files/         # Optional paper attachments, created only when needed
│   ├── transcripts/       # Immutable captured transcript Markdown
│   ├── web/               # Importer-preserved web captures
│   ├── youtube/           # Importer-preserved video transcript captures
│   └── assets/            # Local assets referenced by raw records
├── entities/              # Canonical type: entity
├── concepts/              # Canonical type: concept
├── comparisons/           # Canonical type: comparison
├── queries/               # Canonical type: query
├── docs/
│   ├── architecture/      # Narrative architecture plus rendered exports
│   ├── tech-stack/        # Editable and rendered technology-stack diagram
│   └── workflow/          # Editable and rendered workflow diagram
├── scripts/
│   ├── collect_evidence.py  # Gate A: Zotero collection -> raw/papers/, validate, inbox candidates
│   ├── collect_config.json  # Collection name, search keywords, candidate limits
│   ├── compile_wiki_prompt.md  # Gate B task the compile-wiki cron agent follows
│   ├── lint_canonical.py  # Canonical-page and index.md checker
│   ├── review_compile_prompt.md  # HITL review procedure for compile branches
│   └── validate_raw.py    # Raw-record integrity checker; run after every ingest
├── SCHEMA.md              # Authoritative content and integrity contract
├── index.md               # Complete active canonical catalog
└── log.md                 # Append-only wiki operation history
```

`raw/papers/files/`, `templates/`, and `_archive/` are schema-defined, on-demand
paths. `.obsidian/` is shared editor configuration; ignored `.ua/` is derived
knowledge-graph state, never canonical evidence.

## WHERE TO LOOK

| Task | Location | Notes |
| --- | --- | --- |
| Learn the rules | `SCHEMA.md` | Wins over README examples |
| Install optional tools | `README.md` | Obsidian, Zotero, MCP, CLI, and agent skills |
| Find existing knowledge | `index.md` | Count must equal active canonical files |
| Understand recent work | `log.md` | Read the tail; never rewrite history |
| Stage unclassified input | `inbox/` | Capture properly before canonical use |
| Preserve source evidence | Registered source directories under `raw/` | Body integrity boundary; preserve importer paths |
| Curate reusable knowledge | `entities/`, `concepts/`, `comparisons/`, `queries/` | Folder and frontmatter `type` must agree |
| Inspect architecture and diagrams | `docs/` | Deliverables only; not raw or canonical evidence |
| Inspect editor behavior | `.obsidian/` | Wikilinks enabled; attachments use `raw/assets` |

## CONTENT CONTRACT

- Canonical filenames are lowercase kebab-case and end in `.md`.
- Canonical frontmatter starts at byte zero and contains `title`, `created`,
  `updated`, `type`, `tags`, `sources`, `confidence`, `contested`, and `contradictions`.
- Preserve `created`; bump `updated` whenever content or metadata changes.
- Register tags in the `SCHEMA.md` taxonomy before use; 14 tags currently exist.
- Use `confidence: high` only when multiple sources support the content.
- When `contested` is true, record dated, sourced unresolved positions in the body;
  `contradictions` lists conflicting canonical slugs or is empty.
- Replace or remove every `<angle-bracket>` token before promoting a template copy
  to a raw record or canonical page.
- Create a page only for a source's central subject or a subject repeated across
  at least two sources. Update an existing subject instead of creating a synonym.
- Split pages near 200 lines while preserving provenance and useful links.
- Every canonical page needs two distinct, resolvable, non-self `[[wikilinks]]`
  to active canonical pages; one- and two-page canonical sets are invalid.

## RAW INTEGRITY AND PROVENANCE

- Treat captured raw bodies as immutable.
- Compute raw `sha256` over the exact post-frontmatter body bytes.
- Preserve byte-identical legacy imports with missing `sha256` or final LF;
  report coverage/format gaps instead of normalizing paths, frontmatter, or EOF.
- Only the Zotero metadata-repair and NotebookLM frontmatter-mapping operations
  defined in `SCHEMA.md` may mutate a raw record; follow their byte-preservation
  requirements exactly.
- Put corrections and interpretation in canonical pages, never in captured text.
- Canonical `sources` entries must be exact, existing repository-relative raw
  Markdown paths under a source directory registered in `SCHEMA.md`. Assets and
  attachments do not qualify as sources.
- A claim-level `^[raw/...md]` marker must resolve and already appear in that
  page's `sources` list.

## TRANSACTIONAL WIKI UPDATES

For every canonical create, update, filed query, archive, or delete:

1. Keep `index.md` alphabetic, type-correct, unique, and count-accurate.
2. Append one `log.md` entry using an allowed action and list every affected path.
3. Archive only fully superseded pages; repair active links and remove them from
   the index.

Never index raw records, docs, templates, archived pages, or generated outputs as
active canonical pages.
Log headings use `## [YYYY-MM-DD] <action> | <subject>`; actions are `ingest`,
`create`, `update`, `query`, `lint`, `archive`, `delete`, `map`, and `repair`.
Rotate after 500 entries without changing the completed log. Split an index section
after 50 entries and add thematic navigation after 200 total entries.

## COMMANDS AND VALIDATION

This repository is public, and its root is the wiki root. Captured source text
may be copyrighted, so `.gitignore` excludes everything under `raw/` except the
`.gitkeep` placeholders. Canonical pages, `SCHEMA.md`, `index.md`, and `log.md`
are original work and are committed. Never `git add -f` anything under `raw/`,
and never quote long passages of a source into a canonical page.

Raw records have one executable checker: `python scripts/validate_raw.py`
(registered directory, UTF-8/LF/no BOM/final LF, byte-zero frontmatter, `sha256`,
required paper fields, and title/DOI against the Zotero local API when Zotero is
running). Run it after every `ingest`, fix or report each `FAIL` before compiling
canonical pages, and record the outcome as a `lint` entry in `log.md`. A Zotero
`WARN` means the cross-check was skipped; rerun with Zotero open.

`python scripts/collect_evidence.py` is the Gate A collector (Hermes cron runs it
daily, script-only). It captures new parent items of the Zotero `2nd-brain`
collection into `raw/papers/` (PDF `.zotero-ft-cache` text, never overwriting an
existing record), runs `validate_raw.py`, appends `ingest`/`lint` log entries
when it captured something, and writes Semantic Scholar (most cited; keyless
OpenAlex fallback when it is rate-limited) and arXiv (newest) candidates to
gitignored `inbox/candidates-*.md`. Candidates are not
evidence: the user adds chosen papers to the Zotero collection. Exit 1 means a
Zotero or validation failure; `WARN` lines are candidate-search failures only.

Canonical pages have one executable checker: `python scripts/lint_canonical.py`
(frontmatter fields and values, registered tags, type-directory fit, existing
sources and `^[raw/...]` markers, two valid outbound links, broken links,
orphans, the 200-line limit, and `index.md` entries, sections, order, and
total). Run it after every canonical create, update, filed query, archive, or
delete. There is no build, test, or CI. Validate the rest of the contract
directly:

- UTF-8, LF, no BOM, final newline, and correct leading frontmatter; documented
  byte-identical legacy raw imports may retain their original missing final LF.
- Required fields, date/enumeration values, registered tags, and type-directory fit.
- Existing source paths and valid claim-level provenance markers.
- Two valid outbound canonical links per page and no broken canonical links.
- Filesystem canonical count equals `index.md`; each active page appears once.
- Raw hashes still match exact post-frontmatter bytes.
- Obsidian JSON remains parseable after shared setting changes.
- Before graph generation, lint canonical state; afterward verify `kind: knowledge`,
  complete batches, freshness, required node fields, and no dangling edges.

## ANTI-PATTERNS

- Do not use README's PARA tree, optional metadata/free tags, or Markdown-link
  guidance for canonical work; the active `SCHEMA.md` contract wins.
- Do not edit raw bodies, invent provenance paths, or treat attachments as evidence.
- Do not create passing-mention, isolated, free-form-tag, or duplicate canonical pages.
- Do not rewrite prior `log.md` entries or silently omit index/log synchronization.
- Do not treat `docs/` or `.ua/` as evidence, auto-promote graph output, or
  overwrite canonical Markdown from graph hypotheses; verify against raw sources.
- Do not commit credentials, personal data, Obsidian workspace state, local plugins,
  automation tokens/log URLs, copied assets, `.ua/`, `output/`, or QA artifacts.

## NOTES

- Markdown is the durable asset; Obsidian is an optional editing and graph UI.
- `templates/` and `_archive/` should be created only when their workflows require
  them, not merely to fill the tree.
- No code-symbol map exists. Even explicit project-path Codegraph queries return
  ancestor/global cache data, and no Markdown LSP is active; reject both as evidence.
