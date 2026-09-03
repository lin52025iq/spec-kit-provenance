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
- `Origin`: where the source entered the Spec Kit workflow. Common values: `user`, `agent`, `artifact`, `import`.
- `Introduced during`: workflow phase in which it first appeared, such as `specify`, `clarify`, `plan`, or `manual`.
- `Context`: concise human-readable reason the source was supplied or registered. This should capture intent such as `登录需求参考`, `UI 设计稿`, or `认证接口定义`, not a transcript of the conversation.
- `Used by`: feature identifiers/paths that rely on the source.
- `Superseded by`: replacement source when status is `superseded`.

## Conversational provenance

User conversation is a first-class source surface.

When a user intentionally supplies external material during `/speckit.specify`, `/speckit.clarify`, `/speckit.plan`, or follow-up discussion, Provenance should register or reuse that source even if the generated artifact has not yet copied the URL into Markdown.

Example user message:

```text
登录接口参考这个：https://docs.example.com/auth/api-v2
```

A resulting registry record may retain:

```text
Origin: user
Introduced during: plan
Context: 登录接口参考
```

Do not store the full user message. The registry is provenance metadata, not a conversation archive.

If the same source is later supplied again, reuse its stable ID and update usage/context only when doing so adds useful information.

## Bare URL normalization

Bare URLs are common during conversational workflows. They MUST be accepted without forcing the user to provide metadata first.

However, the registry must not degrade into a bookmark dump. Therefore:

1. derive a readable provisional `Display` from hostname and meaningful path segments;
2. infer provider and type only when reasonably confident;
3. use nearby conversational wording as `Context` when available;
4. set `Status: needs-review` if actual title/purpose is unknown;
5. give the source a generic but truthful summary rather than fabricating document contents;
6. preserve the stable source ID when metadata is later improved.

Example:

```text
Input: https://docs.example.com/platform/authentication/api-v2
Display: docs.example.com — authentication / api-v2
Status: needs-review
Origin: user
Context: API 参考
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
