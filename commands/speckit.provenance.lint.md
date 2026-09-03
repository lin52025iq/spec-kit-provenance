---
description: Validate provenance registry, citations, and source quality
---

# Provenance Lint

Validate `.specify/provenance/sources.md` and feature-level source references.

## Errors

Report as errors:

- malformed or duplicate `SRC-xxx` identifiers;
- citations to source IDs that do not exist;
- source entries without a usable URI/path/reference;
- unsafe persisted URIs containing obvious credentials or secret query parameters.

## Warnings

Report as warnings:

- duplicate or obviously equivalent URIs;
- `needs-review` sources that still lack a meaningful title, type, purpose, or locator;
- `superseded` sources still cited by active artifacts;
- `stale` or `unavailable` sources supporting active requirements/decisions;
- orphan sources not used by any feature;
- raw external URLs in feature artifacts that appear to be evidence but are not registered;
- feature `sources.md` labels that are unreadable or contain only a source ID and bare URL.

## Readability Check

Every registered source should be understandable without opening it. At minimum, a reviewer should see a readable display name and a short purpose/summary. Bare URLs are allowed as input, not as the final human-facing representation.

## Output

Group findings by severity and source ID. Provide concrete repair suggestions. Do not mutate files unless the user explicitly asks for fixes.
