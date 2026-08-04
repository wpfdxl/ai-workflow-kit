# 当前项目配置

> 人填。step1~3 与编码任务**只**认这里的指针。

## active_profile

```
go125-kratos-ddd-sample
```

可选示例：`go125-kratos-ddd-sample` / `php55-thinkphp-sample` / `node-express-sample` / `go-gin-sample` / `python-fastapi-sample`  
或 step0 生成的自定义 id。

对应目录：`profiles/<active_profile>/`

## rules_path

```
profiles/go125-kratos-ddd-sample/RULES.md
```

编码顺序：`profiles/<active_profile>/coding_order.md`  
栈专用自检：`profiles/<active_profile>/checklist_编码自检.md`

## code_root

> 真实业务代码路径（相对本仓库或绝对路径）。

```
../   # e.g. ../../user-service
```

## 说明

- **接入工程**：把 `bootstrap/init_接入我的项目.md` 发给 AI（填技术栈 + code_root），会生成规范并清理示例；见 `docs/示例对话_初始化.md`
- 切换栈：改 `active_profile` + `rules_path`
- 只生成规范：`bootstrap/step0_生成项目规范.md`
- 可删清单：`docs/哪些可以删.md`
- 可选 Cursor 规则摘要：

```
# .cursor/rules/<id>.mdc
```
