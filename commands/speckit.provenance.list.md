---
description: 以可读索引形式列出已登记的来源
---

# 来源列表

读取 `.specify/provenance/sources.md`，以紧凑、便于人工理解的方式展示来源索引。

每个来源至少展示：

- 稳定 Source ID；
- 可读显示名称；
- `Type` 和 `Provider`（如果已知）；
- `Status`；
- 缩短但仍可辨识的 URI；
- 已关联的 Feature（如果已知）；
- 来源阶段和上下文（如果有助于理解）。

优先保证可读性，不要直接倾倒完整注册表文本。查看者应当无需打开 URL，就能回答“`SRC-012` 是什么、为什么会存在”。

如果某个来源为 `needs-review`，应明确标出，并说明缺少哪些信息，例如真实标题、用途、类型或 Locator。

当 `$ARGUMENTS` 中存在明显过滤条件时支持过滤，例如：

- `type=api`
- `status=active`
- `provider=figma`
- `feature=001-login`
- `origin=user`
- `phase=plan`
