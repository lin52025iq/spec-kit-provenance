# Source Registry

> Canonical registry for external sources used by Spec Kit artifacts. Sources are referenced, not copied.
>
> **Human-readable rule:** even when only a URL is known, give the source a stable ID and a readable display name. If the real title is unknown, derive a temporary title from the host/path and mark it as `needs-review` rather than leaving a bare URL.
>
> **Conversation rule:** when a source was supplied by the user during a Spec Kit conversation, retain concise metadata explaining who introduced it, during which workflow phase, and why it was provided.

## Source Types

`requirement` · `design` · `api` · `architecture` · `standard` · `research` · `issue` · `code` · `wiki` · `document` · `other`

## Status Values

`active` · `superseded` · `stale` · `unavailable` · `needs-review`

## Origin Values

Common values: `user` · `agent` · `artifact` · `import`.

Use `user` for a source intentionally supplied in conversation. Origin describes **where the source entered the workflow**, not who authored the external document.

---

<!-- Example only. Remove or replace when the first real source is registered.
## SRC-001 — User Login PRD

- **Type**: requirement
- **Provider**: notion
- **URI**: https://example.com/login-prd
- **Status**: active
- **Accessed**: 2026-09-03
- **Display**: User Login PRD
- **Locator**: §4.2 Verification code rules
- **Summary**: Product requirements for login and verification-code behavior.
- **Origin**: user
- **Introduced during**: specify
- **Context**: 用户提供的登录功能需求依据
- **Used by**: specs/001-login
- **Superseded by**: —
-->
