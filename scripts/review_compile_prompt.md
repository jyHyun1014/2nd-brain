# review (Human-in-the-Loop gate) task

Review AI-generated knowledge before it enters the Second Brain (`main`). This
covers `wiki/compile-<date>` branches and new knowledge from NotebookLM Q&A or
the knowledge graph (proposed as `queries/` or page updates on a branch).
Claude Code does the whole review; the user only approves or rejects.

1. On `main` with a clean tree, list the branch's changes:
   `git diff --stat main <branch>`.
2. For every created or changed canonical page, read the branch version
   (`git show <branch>:<path>`) and check each number, table row, comparison,
   and named dataset/model against the raw records in its `sources`. Confirm
   what the source table compares, not only that the number appears.
   Unsupported values (counts, dates, totals) are errors. Graph or NotebookLM
   output is never evidence: every claim must trace to `raw/`.
3. Also check: no synonym of an existing page, sensible links, Korean prose,
   no long quotations.
4. Fix errors on the branch, run `python scripts/lint_canonical.py` until
   `0 issues`, append a `repair` entry to `log.md` (LF line endings) listing
   each fix and each page reviewed without changes, and commit on the branch.
5. Stop. Do not merge. Report to the user in Korean, written for a reader who
   has not read the papers:
   - each page in 2-3 plain sentences (what it says, why it is useful);
   - errors found and fixed, with the raw location as evidence;
   - open issues that remain, if any;
   - a recommendation: 승인 or 반려, with the reason.
6. On the user's decision only:
   - 승인: `git switch main`, `git merge --ff-only <branch>`, lint again,
     `git push origin main`, `git branch -d <branch>`.
   - 반려: `git switch main`, `git branch -D <branch>`, and append a
     `lint` entry to `log.md` recording the rejection and reason.
