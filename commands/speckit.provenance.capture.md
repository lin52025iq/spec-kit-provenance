---
description: Capture high-confidence external sources from the active feature context
---

# Provenance Capture

Inspect the active feature context for external sources introduced during specification, clarification, or planning.

## Scope

Prefer the active feature artifacts only: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and existing `sources.md`, plus explicit URLs or document references present in the current command context.

Do not scan the entire repository by default.

## What Counts as a Source

High-confidence examples include:

- a URL explicitly introduced as a requirement, PRD, reference, documentation, API, Figma/design file, standard, issue, wiki, or research source;
- Markdown links in a source/reference section;
- GitHub issue/repository links used as evidence;
- local document paths explicitly described as requirements, design, API, architecture, or reference documentation.

Do not register incidental URLs such as localhost endpoints, example placeholders, package metadata links, generated callback URLs, or links that clearly do not support a project artifact.

## Registration

For each high-confidence source:

1. Normalize the URI enough to detect exact/obvious duplicates.
2. Reuse an existing `SRC-xxx` when the source is already registered.
3. Otherwise register it following the same rules as `/speckit.provenance.add`.
4. A bare URL is acceptable, but MUST receive a readable display label. If title/purpose cannot be determined, mark it `needs-review` rather than inventing facts.
5. Add/reconcile the active feature's `sources.md` grouped under Requirements, Design, or Technical References.
6. Never copy full external document contents into the registry.

## Citations

When a feature artifact already contains a source-derived claim and the relationship is clear, prefer a concise citation such as `[SRC-003]` or `[SRC-003 §4.2]`. Do not aggressively annotate every sentence.

## Output

Summarize only meaningful changes: newly registered sources, reused sources, sources needing review, and possible sources intentionally not auto-registered because confidence was low.
