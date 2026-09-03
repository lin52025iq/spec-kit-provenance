---
description: Capture user-provided and high-confidence external sources from the active Spec Kit conversation and feature context
---

# Provenance Capture

Capture external sources introduced during the active Spec Kit workflow, with **user-provided conversational input as the highest-priority source surface**.

The goal is not merely to scan generated Markdown. The goal is to preserve evidence that the user supplied during `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, or related follow-up conversation before that evidence disappears from working context.

## Capture Priority

Inspect source surfaces in this order:

1. **Current user input and recent workflow conversation**
   - URLs pasted by the user;
   - Markdown links;
   - references such as “需求文档在…”, “参考这个…”, “API 文档…”, “Figma…”, “这个 Issue…”, “见附件/文件…”;
   - local document paths or repository references explicitly supplied as evidence;
   - a URL supplied without explanation.
2. **Current command arguments (`$ARGUMENTS`) and hook context**.
3. **Active feature artifacts**: `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, and existing `sources.md`.

Do not wait for a source to appear in a generated artifact before registering it when it was already clearly supplied by the user.

## Conversation Source Rule

When the user intentionally provides a document, URL, file, design, API reference, issue, standard, repository location, or other external material to help define or plan the feature, treat it as provenance unless it is clearly incidental.

Examples that SHOULD be captured:

- “需求参考这个：https://docs.example.com/prd/login”
- “UI 看这个 Figma：https://figma.com/design/... ”
- “接口定义：https://api.example.com/openapi.json”
- “这里有个 GitHub issue 可以参考：https://github.com/org/repo/issues/123”
- a user message containing only `https://...` when the surrounding workflow makes it clear that it is being supplied as reference material;
- “需求文档在 docs/login-prd.md”;
- “以仓库里的 ADR-004 为准”。

Examples that SHOULD NOT be auto-registered:

- localhost/runtime endpoints used only as implementation examples;
- callback URLs, test data, package homepage metadata, or placeholder domains;
- a URL mentioned only as output the product should generate;
- arbitrary code paths with no indication that they are source material.

If confidence is low, report a **potential source** instead of silently registering it.

## Preserve User Intent

For every captured source, preserve what can be truthfully inferred from the user's message:

- **Origin**: normally `user` when introduced directly by the user;
- **Introduced during**: `specify`, `clarify`, `plan`, or the closest active workflow phase;
- **Context**: a short human-readable note describing why the user supplied it, for example `登录需求参考`, `UI 设计稿`, or `认证接口定义`;
- **Type** and **Provider** when reasonably inferable;
- **Display** title when supplied by the user.

Do not copy the full conversation into the registry. Store only concise provenance metadata needed to understand why the source exists.

## Bare URL Handling

A bare URL is valid source input.

When only a URL is known:

1. sanitize it before persistence;
2. derive a readable provisional display label from provider/host/path;
3. use surrounding user wording as `Context` when available;
4. mark metadata `needs-review` if the real title/purpose remains unknown;
5. NEVER invent a document title or contents;
6. preserve the same `SRC-xxx` when metadata is later enriched.

The registry must remain understandable even when many sources began life as bare URLs.

## Registration

For each high-confidence source:

1. Normalize the URI enough to detect exact/obvious duplicates.
2. Reuse an existing `SRC-xxx` when already registered.
3. Otherwise register it following `/speckit.provenance.add` rules.
4. Record conversational provenance metadata (`Origin`, `Introduced during`, `Context`).
5. Add/reconcile the active feature's `sources.md`, grouped under Requirements, Design, or Technical References.
6. Never copy full external document contents into the registry.

If an existing source is reused in a new feature or phase, update its usage metadata rather than creating another ID.

## Citations

When a source-derived relationship is clear, add concise citations such as `[SRC-003]` or `[SRC-003 §4.2]` to the relevant requirement, decision, or research conclusion.

Do not aggressively annotate every sentence. Capture meaningful provenance relationships.

## Output

Keep the report concise and actionable:

- newly registered sources;
- existing sources reused;
- sources captured from user conversation;
- sources marked `needs-review`;
- low-confidence potential sources not auto-registered.

Do not interrupt the normal Spec Kit workflow merely to ask the user for metadata that can safely remain `needs-review` and be enriched later.
