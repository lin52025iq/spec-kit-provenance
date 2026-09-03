# Spec Kit Provenance

Git-native source and evidence tracking for [Spec Kit](https://github.com/github/spec-kit).

`spec-kit-provenance` answers a simple question throughout specification-driven development:

> Where did this requirement, design constraint, API decision, or research conclusion come from?

## Principles

1. **Sources are referenced, not copied.** External documents remain at their original location.
2. **Source IDs are stable.** A URL may change; `SRC-xxx` should not.
3. **Human-readable first.** A registry must be understandable without opening every URL.
4. **Bare URLs are valid input, not valid final presentation.** The extension derives a readable label and marks uncertain metadata `needs-review`.
5. **Provider-agnostic core.** Figma, Notion, GitHub, Confluence, Swagger and plain web links all use the same source model.
6. **Git-native by default.** Markdown is the canonical store; no database is required.

## Installation

Development installation:

```bash
specify extension add provenance --dev /path/to/spec-kit-provenance
```

## Commands

```text
/speckit.provenance.add <url-or-reference>
/speckit.provenance.list
/speckit.provenance.show SRC-001
/speckit.provenance.capture
/speckit.provenance.lint
```

The extension declares optional `after_specify`, `after_clarify`, and `after_plan` capture hooks.

## Storage

Project registry:

```text
.specify/provenance/sources.md
```

Feature manifest:

```text
specs/<feature>/sources.md
```

The project registry contains canonical metadata. Feature manifests contain concise references only.

## Example

A user provides only:

```text
https://www.figma.com/design/abc123/login
```

That is still a valid source. Instead of storing a bare link, Provenance records something like:

```markdown
## SRC-001 — www.figma.com — abc123 / login

- **Type**: design
- **Provider**: figma
- **URI**: https://www.figma.com/design/abc123/login
- **Status**: needs-review
- **Display**: www.figma.com — abc123 / login
- **Summary**: External reference; title and purpose need review.
```

Once a human or agent learns the real title/purpose, the metadata can be improved without changing `SRC-001`.

## Citations

Use concise citations in Spec Kit artifacts:

```markdown
- **FR-006**: Verification codes cannot be resent within 60 seconds.  
  **Source**: [SRC-003 §4.2]
```

For an API decision:

```markdown
Use `POST /v2/auth/login`. **Source**: [SRC-009 POST /v2/auth/login]
```

The parser only needs the stable `SRC-xxx`; locator text remains intentionally human-readable.

## Source Types

`requirement`, `design`, `api`, `architecture`, `standard`, `research`, `issue`, `code`, `wiki`, `document`, `other`.

## Source Status

- `active` — currently valid
- `needs-review` — registered safely, but metadata still needs clarification
- `superseded` — replaced by a newer source
- `stale` — reachable but likely outdated
- `unavailable` — cannot currently be accessed

## Security

Do not persist signed URLs, tokens, API keys, cookies, or credentials. The included helper strips common secret-bearing query keys before writing a URL.

## Helper Script

The Markdown registry remains canonical. A small deterministic helper is included for safe mechanical operations:

```bash
python scripts/python/provenance.py add https://example.com/docs/api
python scripts/python/provenance.py list
python scripts/python/provenance.py lint
```

Agent commands remain responsible for contextual judgments such as whether a link is actually evidence and how it relates to a feature.

## Roadmap

### v0.1

- registry and stable IDs
- readable handling of bare URLs
- add/list/show/capture/lint commands
- optional lifecycle capture hooks
- basic URL sanitization and linting

### Later

- richer requirement/decision relationship graph
- provider adapters and metadata refresh
- source impact analysis
- optional integration with `spec-kit-wiki`
