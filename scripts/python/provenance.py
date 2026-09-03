#!/usr/bin/env python3
"""Spec Kit Provenance v0.1 的最小 Git-native 来源注册辅助工具。

Markdown 注册表始终是唯一事实来源。该脚本只负责适合自动化的确定性操作：
URL 清理、可读名称推断、重复检测、ID 分配、登记、列表和基础检查。
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
    safe_query = [
        (k, v)
        for k, v in parse_qsl(parsed.query, keep_blank_values=True)
        if k.lower() not in SECRET_KEYS
    ]
    path = parsed.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunparse(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, "", urlencode(safe_query), "")
    )


def infer_provider(uri: str) -> str:
    host = urlparse(uri).netloc.lower()
    providers = {
        "figma.com": "figma",
        "github.com": "github",
        "notion.so": "notion",
        "notion.site": "notion",
        "atlassian.net": "confluence/jira",
        "docs.google.com": "google-docs",
        "swagger.io": "swagger",
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
    useful = " / ".join(segments[-2:]) if segments else "首页"
    return f"{parsed.netloc} — {useful}"


def ensure_registry(path: Path) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# 来源注册表\n\n"
        "> Spec Kit 项目使用的外部来源统一登记在这里。来源只建立引用，不复制原文。\n\n",
        encoding="utf-8",
    )


def entries(text: str):
    matches = list(ID_RE.finditer(text))
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[match.start():end]
        yield match.group(1), int(match.group(2)), match.group(3).strip(), block


def field(block: str, name: str) -> str | None:
    m = re.search(rf"^- \*\*{re.escape(name)}\*\*:\s*(.*)$", block, re.M)
    return m.group(1).strip() if m else None


def add(
    registry: Path,
    raw_uri: str,
    title: str | None,
    source_type: str | None,
    summary: str | None,
    origin: str = "manual",
    phase: str = "manual",
    context: str | None = None,
) -> int:
    ensure_registry(registry)
    uri = sanitize_url(raw_uri)
    text = registry.read_text(encoding="utf-8")
    existing = list(entries(text))
    for sid, _, label, block in existing:
        if field(block, "URI") == uri:
            print(f"复用 {sid} — {label}\n{uri}")
            return 0

    next_num = max((num for _, num, _, _ in existing), default=0) + 1
    sid = f"SRC-{next_num:03d}"
    provider = infer_provider(uri)
    inferred_type = source_type or infer_type(uri, provider)
    label = title or readable_label(uri)
    status = "active" if title else "needs-review"
    desc = summary or (
        "外部参考来源；真实标题和具体用途待确认。"
        if not title
        else "已登记的外部来源。"
    )
    context_value = context or "—"
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
        f"- **Origin**: {origin}\n"
        f"- **Introduced during**: {phase}\n"
        f"- **Context**: {context_value}\n"
        f"- **Used by**: —\n"
        f"- **Superseded by**: —\n"
    )
    registry.write_text(text.rstrip() + "\n" + block, encoding="utf-8")
    print(
        f"已登记 {sid} — {label}\n{uri}\n"
        f"status={status}\norigin={origin}\nphase={phase}"
    )
    return 0


def list_sources(registry: Path) -> int:
    if not registry.exists():
        print("尚未找到来源注册表。")
        return 0
    for sid, _, label, block in entries(registry.read_text(encoding="utf-8")):
        print(
            f"{sid}\t{label}\t{field(block, 'Type') or '-'}\t"
            f"{field(block, 'Status') or '-'}\t{field(block, 'Origin') or '-'}\t"
            f"{field(block, 'URI') or '-'}"
        )
    return 0


def lint(registry: Path) -> int:
    if not registry.exists():
        print("ERROR：来源注册表不存在")
        return 1
    text = registry.read_text(encoding="utf-8")
    seen_ids, seen_uris, issues = set(), {}, []
    for sid, _, label, block in entries(text):
        if sid in seen_ids:
            issues.append(("ERROR", sid, "Source ID 重复"))
        seen_ids.add(sid)
        uri = field(block, "URI")
        status = field(block, "Status")
        summary = field(block, "Summary")
        origin = field(block, "Origin")
        phase = field(block, "Introduced during")
        if not uri or uri == "—":
            issues.append(("ERROR", sid, "缺少 URI 或其他来源位置"))
        elif uri in seen_uris:
            issues.append(("WARN", sid, f"URI 与 {seen_uris[uri]} 重复"))
        else:
            seen_uris[uri] = sid
        if status == "needs-review":
            issues.append(("WARN", sid, "来源元数据仍需要人工确认"))
        if not label or label.startswith("http"):
            issues.append(("WARN", sid, "缺少可读显示名称"))
        if not summary or summary == "—":
            issues.append(("WARN", sid, "缺少来源摘要或用途"))
        if not origin:
            issues.append(("WARN", sid, "缺少 Origin 元数据"))
        if not phase:
            issues.append(("WARN", sid, "缺少 Introduced during 元数据"))
        if uri and any(
            re.search(rf"[?&]{re.escape(k)}=", uri, re.I) for k in SECRET_KEYS
        ):
            issues.append(("ERROR", sid, "URI 可能包含敏感 query 参数"))
    if not issues:
        print("OK：来源注册表检查通过")
        return 0
    for severity, sid, message in issues:
        print(f"{severity} {sid}: {message}")
    return 1 if any(x[0] == "ERROR" for x in issues) else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Spec Kit 来源注册表辅助工具")
    parser.add_argument("--registry", default=".specify/provenance/sources.md")
    sub = parser.add_subparsers(dest="command", required=True)
    p_add = sub.add_parser("add", help="登记来源")
    p_add.add_argument("uri")
    p_add.add_argument("--title")
    p_add.add_argument("--type")
    p_add.add_argument("--summary")
    p_add.add_argument("--origin", default="manual")
    p_add.add_argument("--phase", default="manual")
    p_add.add_argument("--context")
    sub.add_parser("list", help="列出来源")
    sub.add_parser("lint", help="检查来源注册表")
    args = parser.parse_args()
    registry = Path(args.registry)
    if args.command == "add":
        return add(
            registry,
            args.uri,
            args.title,
            args.type,
            args.summary,
            args.origin,
            args.phase,
            args.context,
        )
    if args.command == "list":
        return list_sources(registry)
    return lint(registry)


if __name__ == "__main__":
    raise SystemExit(main())
