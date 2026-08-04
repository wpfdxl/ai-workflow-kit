# Node.js + Express（示例规范）

> 示意用。可按真实项目改目录与响应格式。

## 1. 技术栈

- 语言与版本：Node.js LTS（在 PROJECT/本文件写明具体主版本）
- 框架与版本：Express 4.x 风格
- 运行时/包管理：npm 或 pnpm（以目标仓为准）
- 主要依赖约定：不擅自加重大依赖，先搜仓内已有库

## 2. 仓库与目录

- 建议：`src/routes` / `src/controllers` / `src/services` / `src/repositories` / `src/middlewares`
- 配置：`config/` 或环境变量
- 测试：`test/` 或 `*.test.js`

## 3. 分层架构

| 层 | 职责 | 允许依赖 | 禁止 |
|---|---|---|---|
| Route | 挂载路径、中间件 | Controller | 写业务 |
| Controller | 解析请求、调 Service、写响应 | Service | 直连 DB |
| Service | 业务规则 | Repository、其他 Service | 操作 req/res |
| Repository | 数据访问 | DB 客户端 | 业务分支 |

- 事务：Service 层协调
- 跨模块：通过 Service 导出，不互相挖 Repository

## 4. 命名规范

- 文件：kebab-case 或目标仓既有风格，保持一致
- 函数：camelCase
- 常量：UPPER_SNAKE 或目标仓风格
- 路由：小写、名词复数资源风格（或目标仓既有）

## 5. API 约定

- JSON body；统一 `{ code, message, data }`（可改，但全项目一致）
- 鉴权：middleware
- 分页：`page` / `pageSize`
- HTTP 状态码与业务 code 分工写清

## 6. 数据访问

- 使用仓内已有 ORM/查询库
- 防 N+1；参数化查询，禁止字符串拼 SQL
- 迁移脚本进约定目录

## 7. 缓存（如有）

- key 前缀常量；TTL 明确；写路径失效

## 8. 日志与可观测

- 请求 id / 错误栈按仓内 logger
- 不打密钥

## 9. 代码风格与禁止项

- ESLint/Prettier 跟随仓内
- 禁止未处理的 Promise；async 错误要传到错误中间件
- 禁止在 Controller 堆 SQL

## 10. 修改原则

- 最小修改；新文件对齐邻域风格

## 11. 编码顺序（摘要）

Repository → Service → Controller → Route → 测试/文档

## 12. Review 关注点

- 分层穿层；错误处理；输入校验；SQL 注入面
