# Go + Gin（示例规范）

> 示意用。按真实模块路径调整。

## 1. 技术栈

- 语言与版本：Go 1.20+（写明目标仓 go.mod 版本）
- 框架与版本：Gin
- 运行时/包管理：Go modules
- 主要依赖：优先仓内已有；新增需说明

## 2. 仓库与目录

- 建议：`cmd/`、`internal/handler`、`internal/service`、`internal/repository`、`internal/model`、`pkg/`
- 配置：env / yaml
- 测试：`*_test.go`

## 3. 分层架构

| 层 | 职责 | 允许依赖 | 禁止 |
|---|---|---|---|
| Handler | 绑定参数、调 Service、写 JSON | Service | 直连 DB |
| Service | 业务 | Repository | 依赖 gin.Context 业务逻辑 |
| Repository | DB/缓存访问 | driver/client | 业务规则 |

- 事务：Service 或 Repository 明确一种，全项目一致
- 跨包：通过接口注入，避免循环依赖

## 4. 命名规范

- 包名：小写单词
- 导出：大写开头；未导出小写
- 文件：小写下划线或小写
- HTTP：RESTful 或目标仓既有

## 5. API 约定

- 统一 JSON：`{ "code": 0, "message": "ok", "data": {} }`（可改）
- 鉴权：middleware
- 错误：error 上抛，Handler 映射 code

## 6. 数据访问

- database/sql 或仓内 ORM
- context 贯穿；超时可取消
- 禁止字符串拼 SQL；用参数占位

## 7. 缓存（如有）

- key 常量；TTL；失败降级策略写清

## 8. 日志与可观测

- slog/zap 等仓内方案；带 request id
- 不打密钥

## 9. 代码风格与禁止项

- gofmt / goimports
- 检查 error；禁止 `_ = err` 吞掉关键错误
- 避免过大函数；接口小而专

## 10. 修改原则

- 最小修改；保持包边界

## 11. 编码顺序（摘要）

model/repository → service → handler → router → test/doc

## 12. Review 关注点

- error 处理；context；分层；并发安全
