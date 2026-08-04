# Profiles（项目规范包）

每个子目录是一套可切换的技术栈规范。工作流本身不绑定语言。

## 目录约定

```
profiles/<profile_id>/
├── RULES.md                 # 完整规范（给人 / AI）
├── coding_order.md          # 推荐编码顺序
└── checklist_编码自检.md    # 栈专用自检
```

`profile_id`：小写字母、数字、连字符。

## 切换

1. 改根目录 `PROJECT.md` 的 `active_profile` 与 `rules_path`
2. 确认 `code_root` 指向真实业务仓

## 新增

- 拷贝最接近的 sample 改名修改，或
- 用 `bootstrap/step0_生成项目规范.md` / `bootstrap/init_接入我的项目.md` 让 AI 生成  

接入工程并清理开箱示例：见 `docs/示例对话_初始化.md`、`docs/哪些可以删.md`。

## 内置示例（示意用，非某公司业务规范）

| id | 说明 |
|---|---|
| `go125-kratos-ddd-sample` | Go 1.25 + Kratos 微服务 + DDD（默认 PROJECT 指向） |
| `php55-thinkphp-sample` | PHP 5.5 + ThinkPHP 风格分层示意 |
| `node-express-sample` | Node.js + Express |
| `go-gin-sample` | Go + Gin |
| `python-fastapi-sample` | Python + FastAPI |

配套需求示例（与 doc 同名）：

- `workspace/_example_用户资料查询/` ↔ `doc/用户资料查询/`
- `workspace/_example_健康检查摘要/` ↔ `doc/健康检查摘要/`
