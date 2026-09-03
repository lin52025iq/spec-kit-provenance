---
description: 查看单个来源及其追溯关系
---

# 查看来源

从 `$ARGUMENTS` 中取得 `SRC-xxx`，并在 `.specify/provenance/sources.md` 中解析对应来源。

以方便人工审阅的形式展示：

- Source ID 与可读显示名称；
- `Type`、`Provider`、`Status`；
- URI；
- 最近访问日期；
- `Locator`（如果存在）；
- 摘要和用途；
- `Origin`、`Introduced during`、`Context`；
- 哪些 Feature / Artifact 正在引用该来源；
- 是否已经被其他来源替代。

如果来源只有自动生成的临时名称，并且状态为 `needs-review`，必须明确说明该名称是临时的，并指出还应该完善哪些信息，例如真实标题、用途、类型或具体定位。

同时在当前 Feature 的产物中查找 `[SRC-012]` 这类引用。在条件允许时，报告引用它的文档名称以及附近的 Requirement / Decision 标识，例如 `FR-003`、`D-002`。

目标是让使用者无需打开原始链接，就能先理解“这个来源是什么、为什么被记录、在哪里被使用”。
