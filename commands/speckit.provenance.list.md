---
description: List registered provenance sources in a readable index
---

# Provenance List

Read `.specify/provenance/sources.md` and present a compact, human-readable source index.

For each source show:

- stable ID;
- readable display name;
- type and provider when available;
- status;
- a shortened but recognizable URI;
- active feature usage when known.

Prioritize readability over dumping raw registry text. A person should be able to answer "what is SRC-012?" without opening the URL.

If a source is `needs-review`, make that obvious and explain what metadata is missing, such as title, purpose, type, or locator.

Support filters from `$ARGUMENTS` when obvious, for example `type=api`, `status=active`, `provider=figma`, or `feature=001-login`.
