---
description: Show one source and its provenance relationships
---

# Provenance Show

Resolve the `SRC-xxx` identifier from `$ARGUMENTS` against `.specify/provenance/sources.md`.

Show the source in a form optimized for human review:

- ID and readable display name;
- type, provider, status;
- URI;
- accessed date;
- locator, if available;
- summary/purpose;
- features/artifacts that reference it;
- supersession information, if any.

If the source has only a generated display label and is marked `needs-review`, explicitly say that the label is provisional and show which metadata should be improved.

Also search active feature artifacts for citations such as `[SRC-012]` and report the relevant artifact names and nearby requirement/decision identifiers when practical.
