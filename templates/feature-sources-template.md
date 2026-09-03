# 当前 Feature 来源

> 这里只记录当前 Feature 实际使用到的来源。完整元数据统一保存在 `.specify/provenance/sources.md`。

## 需求来源

<!-- 示例：
- [SRC-001] 用户登录 PRD — 登录流程和验证码需求
-->

## 设计来源

<!-- 示例：
- [SRC-002] 登录页 Figma — 页面布局、Loading 和错误状态
-->

## 技术参考

<!-- 示例：
- [SRC-003] Auth API — `POST /v2/auth/login`
-->

## 说明

- 即使底层 URI 发生变化，也必须保持 Source ID 稳定。
- 不要在这里重复完整的注册表元数据。
- Source ID 后优先使用可读名称，不要只保留 `[SRC-xxx] https://...` 这种难以理解的形式。
- 当来源由用户在当前对话中提供时，项目级注册表应保留其 `Origin`、`Introduced during` 和 `Context`。
