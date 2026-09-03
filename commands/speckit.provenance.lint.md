---
description: 检查来源注册表、引用关系和来源质量
---

# 来源检查

检查 `.specify/provenance/sources.md` 以及 Feature 级来源引用是否一致、可读和安全。

## 错误

以下情况应报告为错误：

- `SRC-xxx` 标识格式错误或重复；
- 文档引用了不存在的 Source ID；
- 来源没有可用的 URI、路径或其他可解析位置；
- 已持久化 URI 中明显包含凭据、token、API Key 或其他秘密参数。

## 警告

以下情况应报告为警告：

- URI 重复或明显等价；
- `needs-review` 来源仍缺少有意义的标题、用途、类型或 Locator；
- `superseded` 来源仍被当前 Artifact 引用；
- `stale` 或 `unavailable` 来源仍支撑当前需求或决策；
- 来源没有被任何 Feature 使用；
- Feature 文档中出现明显作为证据使用的外部 URL，但没有登记成 Source；
- Feature 的 `sources.md` 只包含 Source ID 和裸 URL，没有可读名称；
- 来自用户对话的来源缺少足以理解其用途的 `Context`。

## 可读性检查

每个来源都应该做到：**无需打开原始链接，审阅者也能大致理解它是什么以及为什么会被记录。**

至少应能看到：

- 可读的 `Display`；
- 简短的 `Summary` 或 `Context`；
- 稳定 Source ID；
- URI；
- 状态。

裸 URL 可以作为输入，但不应该成为最终唯一的人类可读表示。

## 输出

按严重程度和 Source ID 分组输出问题，并给出具体修复建议。

除非用户明确要求自动修复，否则检查命令只报告问题，不直接修改文件。
