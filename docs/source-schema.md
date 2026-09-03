# 来源数据模型

Source 是 Spec Kit Artifact 所引用外部资料的稳定追溯记录。

## 必需概念

| 字段 | 含义 |
|---|---|
| `ID` | 稳定标识，例如 `SRC-001` |
| `Display` | 列表和 Feature 来源清单中使用的可读名称 |
| `URI` | 外部 URL、本地路径、仓库引用或其他可重新定位的位置 |
| `Type` | 来源信息的语义类别 |
| `Status` | 生命周期 / 质量状态 |
| `Summary` | 简短说明这个来源是什么、为什么重要 |

## 推荐元数据

- `Provider`：承载来源的系统，例如 `figma`、`github`、`notion`、`confluence`、`web`。
- `Accessed`：最近有意识查看该来源的日期。
- `Locator`：来源内部的可读定位，例如章节、Figma Frame、API Operation、Issue Comment、文件/行号或页面名。
- `Origin`：来源如何进入 Spec Kit 工作流。常用值：`user`、`agent`、`artifact`、`import`。
- `Introduced during`：首次出现的工作流阶段，例如 `specify`、`clarify`、`plan`、`manual`。
- `Context`：来源被提供或登记的简短原因，例如“登录需求参考”“UI 设计稿”“认证接口定义”。不要保存整段对话。
- `Used by`：依赖该来源的 Feature 标识或路径。
- `Superseded by`：当状态为 `superseded` 时，记录替代它的新来源。

## 对话来源

用户对话是一级来源入口。

当用户在 `/speckit.specify`、`/speckit.clarify`、`/speckit.plan` 或后续讨论中主动提供外部资料时，即使生成的 Markdown 中还没有出现该 URL，也应该登记或复用对应 Source。

例如用户说：

```text
登录接口参考这个：https://docs.example.com/auth/api-v2
```

对应来源可以记录：

```text
Origin: user
Introduced during: plan
Context: 登录接口参考
```

不要保存完整用户消息。来源注册表用于保存 provenance 元数据，不是聊天归档。

如果同一个来源之后再次被提供，应继续复用稳定 Source ID；只有在新增信息确实有管理价值时，才更新使用关系或上下文。

## 裸 URL 处理

对话过程中只提供 URL 很常见。系统必须接受这种输入，不应强迫用户先补完整元数据。

但注册表也不能退化成书签列表，因此：

1. 根据 hostname 和有意义的路径片段生成临时 `Display`；
2. 只有在合理确定时推断 `Provider` 和 `Type`；
3. 如果附近对话文字能说明用途，将其保存为 `Context`；
4. 如果不知道真实标题或用途，使用 `Status: needs-review`；
5. `Summary` 必须真实保守，不得虚构外部文档内容；
6. 后续完善元数据时保持原 Source ID 不变。

示例：

```text
输入：https://docs.example.com/platform/authentication/api-v2
Display: docs.example.com — authentication / api-v2
Status: needs-review
Origin: user
Context: API 参考
```

## Locator 示例

### 普通文档

```text
§4.2 验证码规则
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

v0.1 中 `Locator` 故意保持自由文本。稳定的机器可读部分仍然只有 `SRC-xxx` 标识符。

## 兼容性原则

主要说明内容可以使用中文，但以下机器协议保持英文或原始形式：

- 字段名，例如 `Type`、`Status`、`Provider`、`Origin`；
- 类型值，例如 `requirement`、`design`、`api`；
- 状态值，例如 `active`、`needs-review`；
- Source ID，例如 `SRC-001`；
- URI、文件路径、API Path、代码标识符。
