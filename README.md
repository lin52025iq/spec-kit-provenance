# Spec Kit 来源追溯扩展

为 [Spec Kit](https://github.com/github/spec-kit) 提供 Git-native 的来源、证据与追溯管理能力。

> **最低兼容版本：`specify 1.0.5.dev0`。** 本扩展的开发、测试和后续功能设计均以 `1.0.5.dev0` 及更高版本为基线。

它主要回答一个问题：

> 这条需求、设计约束、API 决策或研究结论，到底来自哪里？

## 一键安装

先确保当前项目已经通过 `specify init` 初始化，并且当前 `specify` 版本不低于 `1.0.5.dev0`。

然后直接从 GitHub 安装当前版本：

```bash
specify extension add provenance --from https://github.com/lin52025iq/spec-kit-provenance/archive/refs/heads/master.zip
```

安装完成后查看状态：

```bash
specify extension list
specify extension info provenance
```

如果已经安装过，希望直接用仓库最新内容覆盖更新：

```bash
specify extension add provenance --from https://github.com/lin52025iq/spec-kit-provenance/archive/refs/heads/master.zip --force
```

也可以移除后重新安装：

```bash
specify extension remove provenance
specify extension add provenance --from https://github.com/lin52025iq/spec-kit-provenance/archive/refs/heads/master.zip
```

安装成功后，配置模板应自动生成到：

```text
.specify/extensions/provenance/provenance-config.yml
```

如果升级前曾看到 `Config templates not scaffolded: provenance-config`，请使用上面的 `--force` 命令重新安装；`v0.1.1` 已修正配置目标文件名。

> `master.zip` 适合当前快速迭代阶段。后续发布正式版本后，推荐改为固定 Release Tag 的 ZIP 地址，以获得可重复安装能力。

## 核心场景：管理用户对话中提供的来源

这个扩展首先管理的是**用户在 Spec Kit 对话中主动提供的信息**，而不仅仅是扫描已经生成的 Markdown。

当用户在 `/speckit.specify`、`/speckit.clarify`、`/speckit.plan` 或后续讨论中提供参考资料时，应在对话上下文消失之前保存其来源信息。

典型输入包括：

```text
需求参考：https://docs.example.com/prd/login
UI 看这个：https://figma.com/design/...
接口定义：https://api.example.com/openapi.json
这个 Issue 可以参考：https://github.com/org/repo/issues/123
```

即使用户只发送了：

```text
https://docs.example.com/auth/api-v2
```

只要当前上下文明显是在提供参考资料，也可以作为合法来源捕获。

对来自对话的来源，注册表会尽量保存：

```text
Origin: user
Introduced during: specify | clarify | plan
Context: 登录需求参考 / UI 设计稿 / 认证接口定义
```

不会把完整聊天记录复制进仓库。

## 设计原则

1. **用户提供的资料是一等来源。** 优先从当前对话捕获，再检查生成文档。
2. **来源只引用，不复制。** PRD、Figma、API 文档等仍留在原位置。
3. **Source ID 稳定。** URL 可以变化，`SRC-xxx` 不应变化。
4. **优先可读性。** 不打开 URL 也应该大致知道某个 Source 是什么。
5. **裸 URL 可以输入，但不能成为最终唯一展示。** 不知道真实标题时生成临时可读名称，并标记 `needs-review`。
6. **核心与 Provider 解耦。** Figma、Notion、GitHub、Confluence、Swagger、普通网页统一使用 Source 模型。
7. **默认 Git-native。** Markdown 是唯一事实来源，不要求外部数据库。

## 命令

```text
/speckit.provenance.add <url-or-reference>
/speckit.provenance.list
/speckit.provenance.show SRC-001
/speckit.provenance.capture
/speckit.provenance.lint
```

### `add`

显式登记一个来源，并分配或复用稳定 `SRC-xxx`。

### `list`

以可读索引查看来源，而不是直接输出一大段裸 URL。

### `show`

查看单个来源，包括它是什么、为什么被记录、在哪个阶段引入、哪些 Feature 正在使用它。

### `capture`

从当前用户对话、命令参数以及当前 Feature Artifact 中捕获来源。

### `lint`

检查重复来源、失效引用、不可读来源、秘密 URL、未登记外部证据等问题。

## 自动捕获

扩展声明了以下可选生命周期 Hook：

```text
after_specify
after_clarify
after_plan
```

它们都会调用：

```text
speckit.provenance.capture
```

捕获优先顺序：

```text
用户对话
   ↓
当前命令参数 / Hook 上下文
   ↓
当前 Feature 文档
   ↓
来源注册表
   ↓
Feature sources.md
   ↓
必要时写入 [SRC-xxx] 引用
```

重点是：如果用户已经在对话里明确给了来源，不需要等链接之后出现在 `spec.md` 或 `plan.md` 才登记。

## 存储位置

### 项目级来源注册表

```text
.specify/provenance/sources.md
```

这里保存完整、唯一的 Source 元数据。

### Feature 来源清单

```text
specs/<feature>/sources.md
```

这里只保存当前 Feature 实际使用到的来源及其用途，不复制完整元数据。

## 裸 URL 示例

用户只提供：

```text
https://www.figma.com/design/abc123/login
```

不会只保存成一条裸链接，而会形成类似：

```markdown
## SRC-001 — www.figma.com — abc123 / login

- **Type**: design
- **Provider**: figma
- **URI**: https://www.figma.com/design/abc123/login
- **Status**: needs-review
- **Display**: www.figma.com — abc123 / login
- **Summary**: 外部参考来源；真实标题和具体用途待确认。
- **Origin**: user
- **Introduced during**: specify
- **Context**: 用户在需求讨论中提供的 UI 参考
```

后续知道真实标题后，可以完善：

```text
Display: 登录页面设计稿
Status: active
```

但 `SRC-001` 保持不变。

## 引用方式

需求可以写：

```markdown
- **FR-006**：验证码发送后 60 秒内不得重复发送。  
  **来源**：[SRC-003 §4.2]
```

Plan / Research 中可以写：

```markdown
采用 `POST /v2/auth/login`。**来源**：[SRC-009 POST /v2/auth/login]
```

解析时真正稳定的机器部分只有 `SRC-xxx`，Locator 保持人类可读自由文本。

## 来源类型

以下值属于机器协议，保持英文：

```text
requirement
design
api
architecture
standard
research
issue
code
wiki
document
other
```

## 来源状态

```text
active         当前有效
needs-review   已安全登记，但元数据仍需要确认
superseded     已被新来源替代
stale          仍可访问，但可能已经过期
unavailable    当前无法访问
```

## 对话来源元数据

主要字段：

```text
Origin
Introduced during
Context
```

例如：

```text
Origin: user
Introduced during: plan
Context: 用户指定的登录接口参考
```

`Origin` 表示来源如何进入当前工作流，不代表外部文档作者是谁。

## 安全

不要把以下内容写入 Git：

- signed URL；
- token；
- API Key；
- Cookie；
- credential；
- 临时认证参数。

自带 Python helper 会在写入 URL 前移除常见敏感 query 参数。

## Python 辅助工具

Markdown 注册表仍然是唯一事实来源。Python helper 只处理适合自动化的确定性操作：

```bash
python scripts/python/provenance.py add https://example.com/docs/api

python scripts/python/provenance.py add https://example.com/docs/api \
  --origin user \
  --phase plan \
  --context "登录接口参考"

python scripts/python/provenance.py list
python scripts/python/provenance.py lint
```

是否应该把一个链接视为真正的“需求依据”、它与哪个 Requirement 或 Decision 关联，仍由 Agent 根据当前对话上下文判断。

## 与中文 Preset 配合

可以和 [`spec-kit-preset-zh-cn`](https://github.com/lin52025iq/spec-kit-preset-zh-cn) 同时使用：

```bash
specify preset add --from https://github.com/lin52025iq/spec-kit-preset-zh-cn/archive/refs/heads/master.zip
specify extension add provenance --from https://github.com/lin52025iq/spec-kit-provenance/archive/refs/heads/master.zip
```

两者职责不同：

```text
spec-kit-preset-zh-cn
→ 中文模板、中文文档、中文工作流展示

spec-kit-provenance
→ 来源捕获、来源登记、来源引用、来源追溯
```

## 当前版本

`0.1.1`

兼容基线：

- `specify >= 1.0.5.dev0`

当前能力：

- 用户对话优先的来源捕获；
- 稳定 `SRC-xxx`；
- 裸 URL 可读化；
- `Origin / Introduced during / Context` 对话来源元数据；
- `add / list / show / capture / lint`；
- `after_specify / after_clarify / after_plan` 可选 Hook；
- URL 清理和基础来源质量检查；
- 项目级 Registry 与 Feature 级来源清单；
- 修复普通 ZIP 安装时 `provenance-config.yml` 未自动 scaffold 的问题。

## 后续方向

- 更完整的 Requirement / Decision 来源关系图；
- Figma、Notion、GitHub、OpenAPI 等 Provider Adapter；
- 来源元数据自动刷新；
- 来源变化后的影响分析；
- 与 `spec-kit-wiki` 的可选集成；
- 正式 Release Tag 与社区 Catalog 发布。
