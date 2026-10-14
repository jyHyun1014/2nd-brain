# Wiki Log

> Chronological record of wiki actions. This file is append-only: add entries at
> the end and never rewrite or remove an earlier entry.
>
> Entry heading format: `## [YYYY-MM-DD] <action> | <subject>`
>
> Allowed actions: `ingest`, `create`, `update`, `query`, `lint`, `archive`,
> `delete`, `map`, and `repair`.
>
> Each entry lists every affected repository-relative path. After 500 entries,
> rotate the completed file to `log-YYYY.md` and begin a new `log.md`; preserve the
> completed file unchanged.

## [2026-10-08] ingest | Zotero papers (6 records)

Captured from the local Zotero library: bibliographic metadata from
`zotero.sqlite` plus PDF text from each attachment's `.zotero-ft-cache`.
`sha256` covers the exact post-frontmatter body; all six verified after write.

- raw/papers/brown-2020-language-models-are-few-shot.md
- raw/papers/devlin-2019-bert-pre-training-of-deep.md
- raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md
- raw/papers/redmon-2016-you-only-look-once-unified.md
- raw/papers/vaswani-2023-attention-is-all-you-need.md
- raw/papers/wei-2023-chain-of-thought-prompting-elicits.md

## [2026-10-08] lint | Raw paper records

Checked every `raw/**/*.md`: registered source directory, UTF-8 without BOM, LF
only, final LF, byte-zero frontmatter, `sha256` against post-frontmatter bytes,
required paper fields, and title/DOI against the live Zotero item. 6 of 6 pass;
no files renamed or modified.

- raw/papers/brown-2020-language-models-are-few-shot.md
- raw/papers/devlin-2019-bert-pre-training-of-deep.md
- raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md
- raw/papers/redmon-2016-you-only-look-once-unified.md
- raw/papers/vaswani-2023-attention-is-all-you-need.md
- raw/papers/wei-2023-chain-of-thought-prompting-elicits.md

## [2026-10-13] ingest | Relocate paper records to the gitignored wiki

The public repository must keep `raw/` empty, so the six records moved to
`wiki/`, which `.gitignore` excludes. All six are byte-identical to their
previous copies; `scripts/validate_raw.py wiki` passes 6 of 6, including the
Zotero title/DOI cross-check. The two entries above were carried over unchanged.

- raw/papers/brown-2020-language-models-are-few-shot.md
- raw/papers/devlin-2019-bert-pre-training-of-deep.md
- raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md
- raw/papers/redmon-2016-you-only-look-once-unified.md
- raw/papers/vaswani-2023-attention-is-all-you-need.md
- raw/papers/wei-2023-chain-of-thought-prompting-elicits.md

## [2026-10-13] create | LLM paper canonical core

Compiled the five NLP/LLM paper records into six concepts and one comparison.
Claims were checked against the captured text; claim-level markers cite the
supporting record. Tags `llm`, `nlp`, `pretraining`, `prompting`, and
`retrieval` were registered in `SCHEMA.md` before use. The YOLO record is
captured but not compiled: it is the only computer-vision source and has no two
supported links to other canonical pages yet.

- Created:
  - concepts/chain-of-thought-prompting.md
  - concepts/in-context-learning.md
  - concepts/language-model-scaling.md
  - concepts/masked-language-modeling.md
  - concepts/retrieval-augmented-generation.md
  - concepts/transformer.md
  - comparisons/fine-tuning-vs-in-context-learning.md
- Updated:
  - SCHEMA.md
  - index.md
  - log.md

## [2026-10-13] lint | 0 issues found

- Canonical pages: 7 (6 concepts, 1 comparison); required fields, types,
  dates, confidence, contested/contradictions, and registered tags valid.
- Navigation: 7 alphabetical index entries matching the filesystem, 24 valid
  outbound canonical links, at least 2 per page, 0 broken links.
- Provenance: every source exists under `raw/papers/`; every `^[raw/...]`
  marker appears in its page's `sources`.
- Raw integrity: `scripts/validate_raw.py wiki` passes 6 of 6.

## [2026-10-14] ingest | Move the wiki back to the repository root

The `wiki/` subfolder duplicated the root layout and conflicted with the
mentor `llm-wiki` rule that the project root is the wiki root, so its content
moved back to the root and `wiki/` was removed. `.gitignore` now excludes
everything under `raw/` except `.gitkeep`, so captured source text stays local;
canonical pages, `SCHEMA.md`, `index.md`, and `log.md` are committed. Every file
is byte-identical to its `wiki/` copy. `scripts/validate_raw.py` passes 6 of 6
(Zotero closed, so the Zotero cross-check was skipped) and the canonical lint
reports 0 issues.

- Moved (local only, gitignored):
  - raw/papers/brown-2020-language-models-are-few-shot.md
  - raw/papers/devlin-2019-bert-pre-training-of-deep.md
  - raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md
  - raw/papers/redmon-2016-you-only-look-once-unified.md
  - raw/papers/vaswani-2023-attention-is-all-you-need.md
  - raw/papers/wei-2023-chain-of-thought-prompting-elicits.md
- Moved (committed):
  - concepts/chain-of-thought-prompting.md
  - concepts/in-context-learning.md
  - concepts/language-model-scaling.md
  - concepts/masked-language-modeling.md
  - concepts/retrieval-augmented-generation.md
  - concepts/transformer.md
  - comparisons/fine-tuning-vs-in-context-learning.md
- Updated:
  - SCHEMA.md
  - index.md
  - log.md
