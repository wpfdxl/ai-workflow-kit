# Step0 Prompt：生成项目规范

> 用法：把下面整段复制给 AI，再附上你对目标项目的描述（语言、框架、分层、禁止项、目录习惯等）。  
> 产出：`profiles/<新id>/RULES.md` + `coding_order.md` + `checklist_编码自检.md`，并更新根目录 `PROJECT.md`。

---

你正在 **AI Workflow Kit** 中工作。请根据用户给出的技术栈与约束，生成一套**可挂接工作流**的项目规范包。

## 必读

1. `bootstrap/RULES_TEMPLATE.md` — `RULES.md` 必须按该模板章节顺序输出
2. `profiles/README.md` — profile 目录约定
3. 可参考（仅作结构参考，**不要**照抄内容到新 profile，除非用户要求同一栈）：
   - `profiles/go125-kratos-ddd-sample/`
   - `profiles/python-fastapi-sample/`
   - `profiles/go-gin-sample/`
   - `profiles/node-express-sample/`
   - `profiles/php55-thinkphp-sample/`

## 任务

1. 与用户确认或自行拟定合法的 `profile_id`：小写 + 连字符，如 `acme-java-spring`、`myapp-django`
2. 创建目录 `profiles/<profile_id>/`，写入：
   - `RULES.md`（完整规范，按模板章节）
   - `coding_order.md`（推荐编码 Task 顺序，可独立验证）
   - `checklist_编码自检.md`（该栈专用勾选清单）
3. 更新根目录 `PROJECT.md`：`active_profile`、`rules_path`，并提示用户核对 `code_root`
4. 若用户明确要求「写入 Cursor rules」：再生成 `.cursor/rules/<profile_id>.mdc` 摘要（alwaysApply 按用户意愿），正文仍以 profile `RULES.md` 为准

## 必须遵守

1. **不要**写入某个公司的私有业务表名、密钥或未公开 URL，除非用户描述里明确要求写入其自有项目规范
2. 规范要可执行：禁止项写清楚，分层依赖写清楚
3. 不确定处用 ❓ 标在 RULES 对应节，不要瞎编框架 API
4. `coding_order.md` 的顺序必须与 RULES 第 3、11 节一致
5. `checklist_编码自检.md` 每条可勾选、可验证

## 用户描述

<把用户对语言/框架/分层/目录/DB/缓存/禁止项/响应格式等要求贴这里>
