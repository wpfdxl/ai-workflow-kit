# Python + FastAPI（示例规范）

> 示意用。默认 `PROJECT.md` 指向本 profile，便于演示。

## 1. 技术栈

- 语言与版本：Python 3.10+（按目标仓）
- 框架与版本：FastAPI
- 运行时/包管理：poetry / pip / uv（以目标仓为准）
- 类型：优先类型注解；Pydantic 做入参/出参模型

## 2. 仓库与目录

- 建议：`app/api`（路由）、`app/schemas`、`app/services`、`app/repositories`、`app/models`、`app/core`
- 配置：settings 模块 + 环境变量
- 测试：`tests/`

## 3. 分层架构

| 层 | 职责 | 允许依赖 | 禁止 |
|---|---|---|---|
| API Router | 路径、Depends、调 Service | Service、Schema | 直连 DB Session 堆业务 |
| Service | 业务 | Repository | 操作 Request 对象细节 |
| Repository | 持久化 | Session/Engine | 业务规则 |
| Schema | 请求/响应模型 | Pydantic | 副作用 |

- 事务：Service 或依赖注入的 unit-of-work，全项目一致
- 跨模块：Service 对外

## 4. 命名规范

- 模块/文件：snake_case
- 类：PascalCase；函数/变量：snake_case
- 常量：UPPER_SNAKE
- 路由：清晰资源路径；版本可 `/api/v1`

## 5. API 约定

- OpenAPI 由 FastAPI 生成；业务字段与 Schema 一致
- 统一错误：HTTPException 或自定义 handler → `{ code, message, data }`
- 分页：`limit`/`offset` 或 `page`/`page_size`，全项目统一一种

## 6. 数据访问

- SQLAlchemy / 仓内既有；异步或同步与仓内一致
- 防 N+1；参数绑定
- Alembic 或约定迁移目录

## 7. 缓存（如有）

- redis 客户端封装；key 前缀；TTL；写失效

## 8. 日志与可观测

- logging/structlog；请求 id
- 不打密钥

## 9. 代码风格与禁止项

- ruff/black/isort 跟随仓内
- 禁止裸 `except:`；禁止在路由函数写长业务
- 新代码带类型注解

## 10. 修改原则

- 最小修改；Schema 与实现同步改

## 11. 编码顺序（摘要）

models/schemas → repository → service → api router → tests/doc

## 12. Review 关注点

- Schema 与文档一致；依赖注入；事务边界；类型
