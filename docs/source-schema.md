# Source Schema

A source is the stable provenance record for an external reference used by Spec Kit artifacts.

## Required concepts

| Field | Meaning |
|---|---|
| `ID` | Stable identifier such as `SRC-001` |
| `Display` | Human-readable label used in lists and feature manifests |
| `URI` | External URL, local path, repository reference, or other resolvable location |
| `Type` | Semantic category of the information |
| `Status` | Lifecycle/quality state |
| `Summary` | Short explanation of what the source is or why it matters |

## Recommended metadata

- `Provider`: system that hosts the source, such as `figma`, `github`, `notion`, `confluence`, `web`.
- `Accessed`: last date the source was intentionally consulted.
- `Locator`: human-readable location inside the source, such as a section, Figma frame, API operation, issue comment, file/line range, or page name.
- `Used by`: feature identifiers/paths that rely on the source.
- `Superseded by`: replacement source when status is `superseded`.

## Bare URL normalization

Bare URLs are common during conversational workflows. They MUST be accepted without forcing the user to provide metadata first.

However, the registry must not degrade into a bookmark dump. Therefore:

1. derive a readable provisional `Display` from hostname and meaningful path segments;
2. infer provider and type only when reasonably confident;
3. set `Status: needs-review` if actual title/purpose is unknown;
4. give the source a generic but truthful summary rather than fabricating document contents;
5. preserve the stable source ID when metadata is later improved.

Example:

```text
Input: https://docs.example.com/platform/authentication/api-v2
Display: docs.example.com — authentication / api-v2
Status: needs-review
```

## Locator examples

### Document

```text
§4.2 Verification code rules
```

### Figma

```text
Authentication / Login / Error State
```

### API

```text
POST /v2/auth/login
```

### GitHub

```text
src/auth/service.ts @ v2.4.0, lines 120-170
```

Locator syntax is deliberately free text in v0.1. The stable machine-readable part is the `SRC-xxx` identifier.
