#!/usr/bin/env python3
"""Minimal Git-native source registry helper for Spec Kit Provenance v0.1.

The Markdown registry remains the source of truth. This helper intentionally
implements only deterministic operations that are safe to automate:
URL sanitization, readable label inference, duplicate detection, ID allocation,
add/list and basic lint.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

ID_RE = re.compile(r"^## (SRC-(\d+)) — (.+)$", re.M)
SECRET_KEYS = {"token", "access_token", "api_key", "key", "signature", "sig", "auth"}


def sanitize_url(raw: str) -> str:
    parsed = urlparse(raw.strip())
    if parsed.scheme not in {"http", "https"}:
        return raw.strip()
    safe_query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
                  if k.lower() not in SECRET_KEYS]
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", urlencode(safe_query), ""))


def infer_provider(uri: str) -> str:
    host = urlparse(uri).netloc.lower()
    providers = {
        "figma.com": "figma", "github.com": "github", "notion.so": "notion",
        "notion.site": "notion", "atlassian.net": "confluence/jira",
        "docs.google.com": "google-docs", "swagger.io": "swagger",
    }
    for suffix, provider in providers.items():
        if host == suffix or host.endswith("." + suffix):
            return provider
    return "web" if host else "local-file"


def infer_type(uri: str, provider: str) -> str:
    lower = uri.lower()
    if provider == "figma":
        return "design"
    if "swagger" in lower or "openapi" in lower or "/api" in lower:
        return "api"
    if "issue" in lower or "/issues/" in lower:
        return "issue"
    if provider == "github":
        return "code"
    if "wiki" in lower or provider == "confluence/jira":
        return "wiki"
    return "other"


def readable_label(uri: str) -> str:
    parsed = urlparse(uri)
    if not parsed.netloc:
        return Path(uri).name or uri
    segments = [s for s in parsed.path.split("/") if s]
    useful = " / ".join(segments[-2:]) if segments else "home"
    return f"{parsed.netloc} — {useful}"


def ensure_registry(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Source Registry\n\n> Canonical external source registry. Sources are referenced, not copied.\n\n", encoding="utf-8")


def entries(text: str):
    matches = list(ID_RE.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[match.start():end]
        yield match.group(1), int(match.group(2)), match.group(3).strip(), block


def field(block: str, name: str) -> str | None:
    m = re.search(rf"^- \*\*{re.escape(name)}\*\*:\s*(.*)$", block, re.M)
    return m.group(1).strip() if m else None


def add(registry: Path, raw_uri: str, title: str | None, source_type: str | None, summary: str | None) -> int:
    ensure_registry(registry)
    uri = sanitize_url(raw_uri)
    text = registry.read_text(encoding="utf-8")
    existing = list(entries(text))
    for sid, _, label, block in existing:
        if field(block, "URI") == uri:
            print(f"REUSED {sid} — {label}\n{uri}")
            return 0

    next_num = max((num for _, num, _, _ in existing), default=0) + 1
    sid = f"SRC-{next_num:03d}"
    provider = infer_provider(uri)
    inferred_type = source_type or infer_type(uri, provider)
    label = title or readable_label(uri)
    status = "active" if title else "needs-review"
    desc = summary or ("External reference; title and purpose need review." if not title else "Registered external source.")
    today = dt.date.today().isoformat()
    block = (
        f"\n## {sid} — {label}\n\n"
        f"- **Type**: {inferred_type}\n"
        f"- **Provider**: {provider}\n"
        f"- **URI**: {uri}\n"
        f"- **Status**: {status}\n"
        f"- **Accessed**: {today}\n"
        f"- **Display**: {label}\n"
        f"- **Locator**: —\n"
        f"- **Summary**: {desc}\n"
        f"- **Used by**: —\n"
        f"- **Superseded by**: —\n"
    )
    registry.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
    print(f"ADDED {sid} — {label}\n{uri}\nstatus={status}")
    return 0


def list_sources(registry: Path) -> int:
    if not registry.exists():
        print("No source registry found.")
        return 0
    for sid, _, label, block in entries(registry.read_text(encoding="utf-8")):
        print(f"{sid}\t{label}\t{field(block, 'Type') or '-'}\t{field(block, 'Status') or '-'}\t{field(block, 'URI') or '-'}")
    return 0


def lint(registry: Path) -> int:
    if not registry.exists():
        print("ERROR registry missing")
        return 1
    text = registry.read_text(encoding="utf-8")
    seen_ids, seen_uris, issues = set(), {}, []
    for sid, _, label, block in entries(text):
        if sid in seen_ids:
            issues.append(("ERROR", sid, "duplicate source ID"))
        seen_ids.add(sid)
        uri = field(block, "URI")
        status = field(block, "Status")
        summary = field(block, "Summary")
        if not uri or uri == "—":
            issues.append(("ERROR", sid, "missing URI/reference"))
        elif uri in seen_uris:
            issues.append(("WARN", sid, f"duplicate URI also used by {seen_uris[uri]}"))
        else:
            seen_uris[uri] = sid
        if status == "needs-review":
            issues.append(("WARN", sid, "source metadata needs human review"))
        if not label or label.startswith("http"):
            issues.append(("WARN", sid, "human-readable display label missing"))
        if not summary or summary == "—":
            issues.append(("WARN", sid, "summary/purpose missing"))
        if uri and any(re.search(rf"[?&]{re.escape(k)}=", uri, re.I) for k in SECRET_KEYS):
            issues.append(("ERROR", sid, "URI may contain secret query material"))
    if not issues:
        print("OK provenance registry")
        return 0
    for severity, sid, message in issues:
        print(f"{severity} {sid}: {message}")
    return 1 if any(x[0] == "ERROR" for x in issues) else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=".specify/provenance/sources.md")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add")
    p_add.add_argument("uri")
    p_add.add_argument("--title")
    p_add.add_argument("--type")
    p_add.add_argument("--summary")
    sub.add_parser("list")
    sub.add_parser("lint")
    args = parser.parse_args()
    registry = Path(args.registry)
    if args.command == "add":
        return add(registry, args.uri, args.title, args.type, args.summary)
    if args.command == "list":
        return list_sources(registry)
    return lint(registry)


if __name__ == "__main__":
    raise SystemExit(main())
