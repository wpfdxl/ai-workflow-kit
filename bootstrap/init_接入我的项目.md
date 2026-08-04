# Init Prompt：接入我的工程并清理示例

> **用法（推荐）**：把本仓库放进/旁挂到你的业务工程后，用 Cursor（或其它 AI）打开本 kit 目录，把下面「给 AI 的整段」复制粘贴，再填好「我的项目信息」。  
> AI 会：生成你的 profile → 改 `PROJECT.md` → **删除不相关的示例 profile / 示例需求 / 示例 doc** → 清空 INDEX。

---

## 给 AI 的整段（直接复制）

你正在 **AI Workflow Kit** 仓库中，帮我完成「接入真实工程」的初始化。

### 必读

1. `bootstrap/RULES_TEMPLATE.md`
2. `bootstrap/step0_生成项目规范.md`（生成规范的规则）
3. `profiles/README.md`
4. 根目录 `PROJECT.md`
5. `docs/哪些可以删.md`（清理范围以该文件为准）

### 任务（按顺序做完）

1. **生成规范包**  
   根据下方「我的项目信息」创建 `profiles/<profile_id>/`：
   - `RULES.md`（严格按 RULES_TEMPLATE 章节）
   - `coding_order.md`
   - `checklist_编码自检.md`  
   `profile_id`：小写+连字符，能体现语言/框架，如 `acme-go-kratos`、`shop-java-spring`。

2. **更新 `PROJECT.md`**  
   - `active_profile` / `rules_path` 指向新 profile  
   - `code_root` 写成我给出的业务代码路径  
   - 删掉仍指向 `*-sample` 的说明，改成我的 profile

3. **清理开箱示例（必须执行，除非我明确说「保留示例」）**  
   按 `docs/哪些可以删.md` 删除：
   - 所有 `profiles/*-sample/`（以及其它非我新建的 profile）
   - `workspace/_example_*/` 全部示例需求目录
   - `doc/` 下除 Viewer 与 archive 外的示例需求目录（如 `健康检查摘要/`、`用户资料查询/`）  
   然后：
   - 重写 `workspace/INDEX.md`：在跑/已归档表清空，只留表头与命名约定说明
   - 更新 `profiles/README.md`：只列出我的 profile
   - 更新 `doc/README.md`：去掉已删示例的配对说明

4. **可选**  
   若我说了「写入 Cursor rules」：生成 `.cursor/rules/<profile_id>.mdc` 摘要，`alwaysApply` 按我要求。

5. **收尾**  
   用几条 bullet 告诉我：新建了哪些路径、删了哪些路径、下一步如何开第一个需求（复制 `_templates` 或空目录 + 填 `00_需求.md`）。

### 禁止

- 不要删：`workspace/_templates` / `_prompts` / `_checklists`、`bootstrap/`、`doc/sbdoc_web.py`、`doc/hfdoc_config.json`、`doc/archive/`、`archive/`、`docs/`、`.cursor/rules/workflow.mdc`、根目录说明与 LICENSE
- 不要把业务仓源码拷进本 kit
- 不要保留未使用的 `*-sample` profile（除非我写了「保留示例」）

### 我的项目信息

```
业务仓路径（code_root）：
语言与版本：
框架与版本：
分层/架构（如 DDD、MVC、三层…）：
目录习惯（关键路径）：
API 风格（HTTP/gRPC/响应包装）：
DB / 缓存约定：
禁止项 / 代码风格：
是否写入 Cursor rules：（是/否）
是否保留开箱示例：（否 / 是）
其它约束：
```

（把上面填空后发给 AI。）
