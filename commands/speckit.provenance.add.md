---
description: 登记外部来源并分配稳定的 SRC 标识符
---

# 登记来源

将 `$ARGUMENTS` 中提供的来源登记到 `.specify/provenance/sources.md`。

## 规则

1. 接受 URL、本地文档路径、代码仓库引用，或“简短说明 + 来源位置”。
2. 不要把来源正文复制进注册表，只记录来源元数据。
3. 创建来源前先检查注册表；当规范化后的 URI 已存在时，复用已有来源。
4. 按 `SRC-001`、`SRC-002`……的形式分配下一个稳定标识符。已有 Source ID 永远不要重新编号。
5. 注册表必须保证人在 GitHub 中直接浏览时也能读懂。
6. 如果来源来自当前用户对话，应尽可能记录 `Origin: user`、`Introduced during` 和简短的 `Context`。

## 仅提供 URL 时

用户只提供一个 URL 也是合法输入，但最终不能只保存成一条无法理解的裸链接。

当只有 URL 时：

- 根据主机名和有意义的路径片段生成可读的临时显示名称；
- 当信息明显时推断 `Provider`，例如 `figma`、`github`、`notion`、`confluence`、`swagger`；
- 只有在置信度较高时才推断 `Type`，否则使用 `other`；
- 如果不知道真实文档标题或用途，将 `Status` 设为 `needs-review`；
- 填写真实且保守的摘要，例如“用户在需求讨论中提供的外部参考，标题和具体用途待确认”；
- 保留足够的 URI 信息，确保后续仍可访问该来源。

例如：

`https://docs.example.com/auth/api-v2`

应显示为类似：

`docs.example.com — auth / api-v2`

而不是只显示原始 URL。

## 安全要求

不得把秘密信息持久化到 URI。应移除看起来包含 token、API Key、签名、凭据或临时认证信息的 query 参数。如果移除后 URL 无法直接使用，则保存安全的基础地址，并注明需要认证访问。

## 输出

报告：

- 新分配或复用的 Source ID；
- 可读显示名称；
- 类型；
- URI；
- 状态；
- 对话来源信息（若存在）。

如果该来源属于当前 Feature，同时在该 Feature 的 `sources.md` 中加入简洁引用，不要复制完整注册表元数据。
