# 拷到其他工程

本目录是一套文件契约，不是业务代码。任意语言仓库都可以整夹复制。

## 1. 放哪

任选一种：

```text
<your-repo>/ai-dev-workflow/     # 推荐，和业务代码并列
<your-repo>/docs/ai-workflow/    # 若希望藏在 docs 下
```

不要把历史 `workspace/<真实需求>`、`archive/`、业务源码路径拷进去。

## 2. 填本工程信息

编辑 `project.local.md`：

- 语言 / 运行时
- 默认对比分支（main / master / develop）
- 规范文件路径（CONTRIBUTING、AGENTS.md、linter、架构说明）
- 业务代码根目录（如 `src/`、`app/`）——**只写在这一份里**，不要写回 templates/prompts

## 3. 让模型看得到

Cursor / Claude Code / 其它 Agent：

- 把 `AGENTS.md` 复制到目标仓根，或在规则里写「编码流程以 `ai-dev-workflow/README.md` 为准」
- 对话里 `@ai-dev-workflow/README.md`

## 4. 接口文档格式

阶段③不强制 OpenAPI 或某家平台。`docs/<需求名>/` 用本工程已经在用的格式即可：OpenAPI、Proto、Markdown 表格、内部 JSON。在 `project.local.md` 写一句「本工程接口文件长什么样」。

没有对外 API 的需求：`02` 写「无独立接口」，INDEX 注明即可。

## 5. 不要改的

- `templates/` `prompts/` `checklists/` 保持语言无关
- 语言禁令（例如某语言不能用三目、方法必须以 Xxx 结尾）写进 **目标仓自己的规范**，不要写进本套模板
