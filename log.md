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

## [2026-10-19] update | Align concept pages with the llm-wiki skill

Installed the mentor `llm-wiki` skill under `.claude/skills/llm-wiki/`
(gitignored: `ains-lab/harness` has no license, so it is not redistributed).
Following its concept-page structure, each concept page gained an open-questions
section built only from limitations its source papers state, plus a
related-concepts list. Lint now also checks inbound links: 7 pages, 24 outbound
links, at least 2 inbound per page, 0 issues. The Zotero metadata backfill of
the raw paper records is pending because Zotero was not running.

- Updated:
  - concepts/chain-of-thought-prompting.md
  - concepts/in-context-learning.md
  - concepts/language-model-scaling.md
  - concepts/masked-language-modeling.md
  - concepts/retrieval-augmented-generation.md
  - concepts/transformer.md
  - .gitignore
  - log.md

## [2026-10-19] repair | Zotero metadata backfill to the llm-wiki schema

Backfilled the six paper records to the `llm-wiki` Zotero schema using the
Zotero local API: parent item metadata, BibTeX citation key, and children
(attachment keys only; the child note was not ingested). Only the frontmatter and
the readable block before `## Extracted Text` changed. Every extracted-text
suffix is byte-identical to its pre-backfill copy, and `sha256` was recomputed
over the new body. Paths were kept, as the skill's backfill rules require, so
no canonical `sources` changed. All six records are `metadata_status: complete`.
`SCHEMA.md` now states the Zotero record fields, `scripts/validate_raw.py`
checks them, and the Transformer page's note now names the renamed `published`
field.

- Updated (local only, gitignored):
  - raw/papers/brown-2020-language-models-are-few-shot.md
  - raw/papers/devlin-2019-bert-pre-training-of-deep.md
  - raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md
  - raw/papers/redmon-2016-you-only-look-once-unified.md
  - raw/papers/vaswani-2023-attention-is-all-you-need.md
  - raw/papers/wei-2023-chain-of-thought-prompting-elicits.md
- Updated:
  - SCHEMA.md
  - concepts/transformer.md
  - scripts/validate_raw.py
  - log.md

## [2026-10-19] lint | 0 issues found

- Raw: 6 of 6 Zotero records pass `scripts/validate_raw.py`, including required
  fields, parent-key check, duplicate-key check, and title/DOI against Zotero.
- Canonical: 7 pages, 24 outbound links, at least 2 inbound links per page,
  0 orphans, 0 broken links, index matches the filesystem.

## [2026-10-19] query | How RAG and in-context learning supply knowledge

Question: how do RAG and in-context learning supply factual knowledge, and how
do they compare on the same tasks? Answered from the RAG, in-context-learning,
and fine-tuning comparison pages, then checked against the papers. The GPT-3
paper's closed-book QA section places RAG and GPT-3 on the same open-domain QA
benchmarks, which the existing pages did not yet cover. Filed as a query page
because that cross-paper comparison would be painful to re-derive. The RAG and
in-context-learning pages now link to it.

- Created:
  - queries/rag-vs-in-context-learning-knowledge-supply.md
- Updated:
  - concepts/in-context-learning.md
  - concepts/retrieval-augmented-generation.md
  - index.md
  - log.md

## [2026-10-19] query | NotebookLM cross-check of RAG vs GPT-3 open-domain QA

Created the NotebookLM notebook "LLM 기초" (`8bb21020-1405-4bdd-b9e2-4f04f6a45cba`)
with `notebooklm-py` 0.8.5. Its sources are the five NLP paper records, each
titled with its local path so cited source IDs map back to raw records. One
question (conversation `59f5970d-1fe4-4b72-8e3c-f44077d3c093`) cited only
`raw/papers/brown-2020-language-models-are-few-shot.md` and
`raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md`.

- Adopted after checking RAG Table 1: TriviaQA has a standard test split
  (RAG-Sequence 56.8) and a Wiki split (68.0). GPT-3's comparison uses the Wiki
  split, and RAG reports a TriviaQA state of the art only on that split. GPT-3's
  RAG row takes the better of RAG-Sequence and RAG-Token per dataset.
- Not adopted: the answer's claim that trivia knowledge is "densely distributed"
  in GPT-3's pre-training corpus. Neither paper states it.
- Updated:
  - queries/rag-vs-in-context-learning-knowledge-supply.md
  - log.md

## [2026-10-20] repair | Rename paper records to the llm-wiki naming rule

Renamed the six raw paper records to the skill's `raw/papers/YYYY-MM-title-slug.md`
rule (Zotero `published` year-month plus the full title slug) at the user's request.
File bytes are unchanged, so every `sha256` still matches. Earlier log entries keep
the old paths as history; the mapping is:

- raw/papers/brown-2020-language-models-are-few-shot.md -> raw/papers/2020-07-language-models-are-few-shot-learners.md
- raw/papers/devlin-2019-bert-pre-training-of-deep.md -> raw/papers/2019-05-bert-pre-training-of-deep-bidirectional-transformers-for-language-understanding.md
- raw/papers/lewis-2021-retrieval-augmented-generation-for-knowledge.md -> raw/papers/2021-04-retrieval-augmented-generation-for-knowledge-intensive-nlp-tasks.md
- raw/papers/redmon-2016-you-only-look-once-unified.md -> raw/papers/2016-05-you-only-look-once-unified-real-time-object-detection.md
- raw/papers/vaswani-2023-attention-is-all-you-need.md -> raw/papers/2023-08-attention-is-all-you-need.md
- raw/papers/wei-2023-chain-of-thought-prompting-elicits.md -> raw/papers/2023-01-chain-of-thought-prompting-elicits-reasoning-in-large-language-models.md
- Updated `sources` and provenance markers:
  - comparisons/fine-tuning-vs-in-context-learning.md
  - concepts/chain-of-thought-prompting.md
  - concepts/in-context-learning.md
  - concepts/language-model-scaling.md
  - concepts/masked-language-modeling.md
  - concepts/retrieval-augmented-generation.md
  - concepts/transformer.md
  - queries/rag-vs-in-context-learning-knowledge-supply.md
  - log.md

## [2026-10-21] ingest | Zotero collection 2nd-brain (1 records)

Captured by `scripts/collect_evidence.py`: Zotero local API metadata plus the PDF
attachment's `.zotero-ft-cache` text. `sha256` covers the exact post-frontmatter body.

- raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md

## [2026-10-21] lint | Raw paper records

`python scripts/validate_raw.py`: 0 failing record(s).

## [2026-10-21] create | Vision Transformer (compile of 1 raw record)

Compiled `raw/papers/2021-06-an-image-is-worth-16x16-words-transformers-for-image-recognition-at-scale.md`. Created one concept page and linked it from
related pages. Validate/lint result for canonical pages is clean (links, tags,
sources/markers, index count).

- Created:
  - concepts/vision-transformer.md
- Updated:
  - concepts/transformer.md
  - concepts/masked-language-modeling.md
  - index.md
  - log.md

## [2026-10-21] lint | Compile deferred: 1 raw records

- `raw/papers/2016-05-you-only-look-once-unified-real-time-object-detection.md`: YOLO is a single-source subject (object detection with a CNN) and no
  registered tag in `SCHEMA.md` covers computer vision. The only existing canonical
  link target is the [[vision-transformer]] page, which mentions detection merely as a
  future challenge, so a page would be isolated or force-linked. Revisit when a second
  vision or detection source or a registered tag exists.

## [2026-10-22] ingest | Zotero collection 2nd-brain (13 records)

Captured by `scripts/collect_evidence.py`: Zotero local API metadata plus the PDF
attachment's `.zotero-ft-cache` text. `sha256` covers the exact post-frontmatter body.

- raw/papers/2025-10-agentbench-evaluating-llms-as-agents.md
- raw/papers/2023-03-self-consistency-improves-chain-of-thought-reasoning-in-language-models.md
- raw/papers/2024-06-sglang-efficient-execution-of-structured-language-model-programs.md
- raw/papers/2023-07-llama-2-open-foundation-and-fine-tuned-chat-models.md
- raw/papers/2026-10-the-explainability-illusion-must-vits-exhibit-patch-decoding-interpretability.md
- raw/papers/2021-08-swin-transformer-hierarchical-vision-transformer-using-shifted-windows.md
- raw/papers/2023-09-the-rise-and-potential-of-large-language-model-based-agents-a-survey.md
- raw/papers/2025-02-from-local-to-global-a-graph-rag-approach-to-query-focused-summarization.md
- raw/papers/2026-10-recurrent-vision-transformers-for-event-based-spacecraft-pose-estimation-under-slow-relative-motions.md
- raw/papers/2023-10-self-rag-learning-to-retrieve-generate-and-critique-through-self-reflection.md
- raw/papers/2021-10-lora-low-rank-adaptation-of-large-language-models.md
- raw/papers/2024-03-retrieval-augmented-generation-for-large-language-models-a-survey.md
- raw/papers/2022-03-training-language-models-to-follow-instructions-with-human-feedback.md

## [2026-10-22] lint | Raw paper records

`python scripts/validate_raw.py`: 0 failing record(s).

## [2026-10-22] create | Compile 13 Zotero papers into canonical pages

Compiled from the 13 raw records captured in the `ingest` entry above (all cited via
`^[raw/...]` markers). New pages (9): concepts/graph-rag.md, concepts/llm-based-agents.md,
concepts/lora.md, concepts/reinforcement-learning-from-human-feedback.md,
concepts/self-consistency.md, concepts/self-rag.md, concepts/sglang.md,
concepts/swin-transformer.md, entities/llama-2.md.

- Created: 9 pages (listed above).
- Raw coverage: swin -> swin-transformer; lora -> lora; instructgpt -> reinforcement-learning-from-human-feedback;
  self-consistency -> self-consistency; llama-2 -> llama-2; agents survey + agentbench -> llm-based-agents;
  self-rag -> self-rag; rag survey -> retrieval-augmented-generation (update); sglang -> sglang;
  graphrag -> graph-rag; the two 2026-10 ViT papers -> vision-transformer (update).

## [2026-10-22] update | Existing pages extended with the new sources

- concepts/retrieval-augmented-generation.md (RAG survey: Naive/Advanced/Modular, evaluation; confidence medium -> high)
- concepts/vision-transformer.md (Swin link, event-based RVT, patch-decoding explainability)
- concepts/chain-of-thought-prompting.md (links to self-consistency, llm-based-agents)
- comparisons/fine-tuning-vs-in-context-learning.md (LoRA as parameter-efficient fine-tuning)
- index.md (9 -> 18 active pages)

## [2026-10-22] lint | Post-compile check

`python scripts/validate_raw.py`: 0 failing record(s). All wikilinks in canonical pages resolve to
active pages; index.md lists 18 pages and the filesystem holds 18; every page has at least two
distinct outbound links and uses only registered tags.

## [2026-10-23] ingest | Zotero collection 2nd-brain (5 records)

Captured by `scripts/collect_evidence.py`: Zotero local API metadata plus the PDF
attachment's `.zotero-ft-cache` text. `sha256` covers the exact post-frontmatter body.

- raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md
- raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md
- raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md
- raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md
- raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md

## [2026-10-23] lint | Raw paper records

`python scripts/validate_raw.py`: 0 failing record(s).

## [2026-10-30] ingest | Zotero collection 2nd-brain (5 records compiled)

Compiled the 5 records captured on 2026-10-23 into canonical pages. Raw bodies unchanged.

- raw/papers/2021-05-emerging-properties-in-self-supervised-vision-transformers.md (DINO)
- raw/papers/2023-03-react-synergizing-reasoning-and-acting-in-language-models.md (ReAct)
- raw/papers/2024-06-chatdev-communicative-agents-for-software-development.md (ChatDev)
- raw/papers/2025-04-ragas-automated-evaluation-of-retrieval-augmented-generation.md (RAGAS)
- raw/papers/2026-10-learning-marginal-viewpoint-utility-for-budgeted-evidence-selection-in-rag.md (LMVU)

## [2026-10-30] create | 5 canonical pages from 5 pending records

- concepts/self-supervised-vision-pretraining.md (DINO: self-distillation, centering/sharpening, k-NN)
- concepts/react.md (thought-action-observation loop; HotpotQA/FEVER/ALFWorld/WebShop)
- concepts/multi-agent-software-development.md (ChatDev chat chain, dehallucination, dual agreement)
- concepts/ragas.md (faithfulness, answer relevance, context relevance)
- concepts/marginal-viewpoint-utility.md (token-budgeted evidence selection by marginal gain)

## [2026-10-30] update | Cross-references for the 5 pending records

- concepts/vision-transformer.md (DINO source, self-supervised pretraining link)
- concepts/retrieval-augmented-generation.md (RAGAS, LMVU sources and sections)
- concepts/llm-based-agents.md (ReAct, ChatDev sources and sections)
- concepts/chain-of-thought-prompting.md (ReAct source, "reasoning + action" section)
- concepts/self-rag.md (links to ragas, marginal-viewpoint-utility)
- index.md (18 -> 23 active pages)

## [2026-10-30] lint | Post-compile check

`python scripts/lint_canonical.py`: 0 issues (23 pages, 96 valid outbound links, minimum 1 inbound).
`python scripts/validate_raw.py`: 0 failing record(s); Zotero local API was unreachable so the
title/DOI cross-check was skipped (WARN, not a failure).

## [2026-10-30] repair | DINO page claims checked against raw
- concepts/self-supervised-vision-pretraining.md: removed image counts absent from the source; corrected Table 10 comparison (DINO ViT-S vs DINO ResNet-50, not supervised ViT-S).
- Reviewed concepts/react.md numbers against raw; no changes needed.

