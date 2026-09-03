# 来源注册表

> Spec Kit 项目使用的外部来源统一登记在这里。**来源只建立引用，不复制原文。**
>
> **可读性规则：** 即使当前只知道一个 URL，也必须分配稳定 Source ID，并生成一个人在 GitHub 中能够识别的显示名称。如果不知道真实标题，则根据 host/path 生成临时名称，并标记为 `needs-review`，不要只留下裸 URL。
>
> **对话来源规则：** 当来源由用户在 Spec Kit 对话中主动提供时，应保留简洁元数据，说明它由谁引入、在哪个工作流阶段引入，以及用户为什么提供它。

## 来源类型

机器值保持稳定：

`requirement` · `design` · `api` · `architecture` · `standard` · `research` · `issue` · `code` · `wiki` · `document` · `other`

## 来源状态

机器值保持稳定：

`active` · `superseded` · `stale` · `unavailable` · `needs-review`

## 来源入口

常用 `Origin` 值：`user` · `agent` · `artifact` · `import`。

用户在对话中主动提供的来源使用 `user`。`Origin` 表示“来源如何进入当前工作流”，并不表示外部文档的作者是谁。

## 字段说明

- **Type**：来源的语义类型。
- **Provider**：来源所在系统，例如 `figma`、`github`、`notion`、`web`。
- **URI**：可以重新定位来源的地址、路径或引用。
- **Status**：来源当前状态。
- **Accessed**：最近有意识查看该来源的日期。
- **Display**：列表和 Feature 清单中使用的可读名称。
- **Locator**：来源内部的具体位置，例如章节、Figma Frame、API Operation。
- **Summary**：来源是什么、主要提供什么信息。
- **Origin**：来源如何进入工作流。
- **Introduced during**：来源在哪个 Spec Kit 阶段首次引入，例如 `specify`、`clarify`、`plan`。
- **Context**：用户当时为什么提供该来源的简短说明。
- **Used by**：哪些 Feature 使用该来源。
- **Superseded by**：该来源被哪个新来源替代。

---

<!-- 仅为示例；登记第一个真实来源时删除或替换。
## SRC-001 — 用户登录 PRD

- **Type**: requirement
- **Provider**: notion
- **URI**: https://example.com/login-prd
- **Status**: active
- **Accessed**: 2026-09-03
- **Display**: 用户登录 PRD
- **Locator**: §4.2 验证码规则
- **Summary**: 登录流程和验证码行为的产品需求来源。
- **Origin**: user
- **Introduced during**: specify
- **Context**: 用户在需求讨论中指定的主要 PRD
- **Used by**: specs/001-login
- **Superseded by**: —
-->
