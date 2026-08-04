# Go 1.25 + Kratos + DDD（示例规范）

> 示意用。面向 go-kratos 微服务 + DDD 分层；非某公司业务规范。

## 1. 技术栈

- 语言与版本：Go 1.25
- 框架与版本：Kratos（HTTP/gRPC，protobuf API）
- 运行时/包管理：Go modules
- 主要依赖：google.golang.org/protobuf、Kratos 组件（config/log/transport）；ORM/缓存以目标仓为准

## 2. 仓库与目录

典型单服务布局（可按 monorepo 调整）：

```
cmd/<service>/main.go
api/<service>/v1/*.proto          # 对外契约
internal/conf                     # 配置结构
internal/server                   # HTTP/gRPC Server 装配
internal/service                  # 应用层：实现 proto 生成的 Service 接口
internal/biz                      # 领域层：usecase、领域对象、repo 接口
internal/data                     # 基础设施：repo 实现、DB/缓存/RPC 客户端
internal/pkg                      # 仅本服务可复用小工具（慎用）
```

- 配置：`configs/` + Kratos config
- 测试：`internal/.../*_test.go`；优先测 biz

## 3. 分层架构（DDD）

| 层 | 目录 | 职责 | 允许依赖 | 禁止 |
|---|---|---|---|---|
| API | `api/` | protobuf 契约 | 无业务代码 | 写逻辑 |
| Interface/Server | `internal/server` | 传输层装配、中间件 | service | 业务规则 |
| Application | `internal/service` | DTO↔领域转换、编排 usecase | biz | 直连 DB |
| Domain | `internal/biz` | 实体/值对象、usecase、Repo **接口** | 标准库、领域纯依赖 | 依赖 data/驱动细节 |
| Infrastructure | `internal/data` | Repo 实现、外部系统 | biz 接口、驱动 | 领域规则堆砌 |

依赖方向（强制）：

```
server → service → biz ← data
                 （data 实现 biz 定义的接口，经 wire 注入）
```

- 跨服务：只通过 `api` proto / 客户端，不 import 对方 `internal`
- 事务：在 biz usecase 或 data 的 UnitOfWork 中明确一种，全服务一致
- 领域事件（如有）：在 biz 定义，data/outbox 投递

## 4. 命名规范

- 包名：小写单词；目录与包一致
- 导出：大写；未导出小写
- proto：`package api.<service>.v1`；RPC/消息 PascalCase
- usecase 方法：动词短语，如 `GetUserProfile`
- Repo 接口：`UserRepo`，实现放 data 包私有结构体

## 5. API 约定

- 对外以 protobuf 为准；HTTP 由 proto HTTP annotations / Kratos 生成
- 错误：`github.com/go-kratos/kratos/v2/errors` 业务错误码；勿裸 `fmt.Errorf` 直出给调用方
- 分页：统一 `page`/`page_size` 或 cursor，全服务一种
- 鉴权：transport middleware；biz 只接收已解析的身份值对象

## 6. 数据访问

- 仅 `internal/data` 接触 DB/Redis/MQ
- biz 只依赖 Repo 接口；禁止 data 类型泄漏进 service/biz 导出 API
- SQL 参数化；防 N+1
- 迁移：独立 migrate 目录或工具，评审后执行

## 7. 缓存（如有）

- 实现放 data；key 前缀常量；TTL 与失效写在 usecase 或 repo 注释
- 缓存不能破坏领域不变量；写路径主动失效或版本号

## 8. 日志与可观测

- Kratos log + trace id；关键业务失败打 Warn/Error
- 禁止日志输出 token、密码、证件号明文

## 9. 代码风格与禁止项

- `gofmt` / `goimports`；`golangci-lint` 跟随仓内
- 禁止：service/biz 直接 import 驱动；循环依赖；跨服务 import internal
- 禁止：丢掉 error（`_ = err`）于关键路径
- proto 变更需同步生成代码，生成物勿手改

## 10. 修改原则

- 最小修改；先改 proto/契约再改实现（若 API 变更）
- 新代码走 DDD 边界；改旧代码不强行大拆，除非任务要求

## 11. 编码顺序（摘要）

proto/api → biz（实体+接口+usecase）→ data 实现 → service → server 注册 → 测试/文档

## 12. Review 关注点

- 依赖方向是否反转；领域逻辑是否漏到 data；错误码；proto 与实现一致
