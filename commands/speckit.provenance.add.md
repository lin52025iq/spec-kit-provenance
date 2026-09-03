---
description: Register an external source and assign a stable SRC identifier
---

# Provenance Add

Register the source supplied in `$ARGUMENTS` in `.specify/provenance/sources.md`.

## Rules

1. Accept a URL, local document path, repository reference, or a short description plus location.
2. Never copy the source body into the registry. Record provenance metadata only.
3. Search the registry before creating a source. Reuse an existing source when the normalized URI already exists.
4. Allocate the next stable identifier in the form `SRC-001`, `SRC-002`, ... . Never renumber existing sources.
5. The registry must remain understandable to a person browsing GitHub.

## Bare URL Handling

A URL alone is valid input. Never store it as an unexplained bare link.

When only a URL is available:

- infer a readable display name from the hostname and meaningful path segments;
- infer a likely `provider` when obvious (`figma`, `github`, `notion`, `confluence`, `swagger`, etc.);
- infer `type` only when confidence is high; otherwise use `other`;
- set `status` to `needs-review` when the real document title or purpose is not known;
- add a short `Summary` such as `External reference provided during specification; title needs review.`;
- preserve enough URI information for the source to be opened later.

Example: `https://docs.example.com/auth/api-v2` should be displayed as something like `docs.example.com — auth / api-v2`, not merely as the raw URL.

## Security

Do not persist secrets in URIs. Remove query parameters that appear to contain tokens, API keys, signatures, credentials, or temporary authentication material. If removing them would make the URI unusable, record a safe base URI and note that authentication is required.

## Output

Report the assigned/reused source ID, readable display name, type, URI, and status. If the source belongs to the active feature, add a concise reference to that feature's `sources.md` without duplicating all metadata.
