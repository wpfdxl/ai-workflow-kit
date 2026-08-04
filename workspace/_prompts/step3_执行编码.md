# Step3 Prompt：执行编码

> 用法：接口文档定稿后，准备好 `03_编码任务.md` 的 @ 引用，复制下面整段给 AI。

---

你正在 **AI Workflow Kit** 中执行编码。

## 执行规则

1. 先读 `workspace/<需求>/03_编码任务.md` 及其 @ 引用（方案、接口、PROJECT、RULES、coding_order）
2. 规范**仅**来自 active profile；禁止套用未激活的 sample 或其他仓规则
3. 按 coding_order 与 Task 清单逐项做；动手前在 `code_root` search 类似实现
4. 最小修改；不自由发挥字段/路径；不格式化无关代码
5. 每完成 Task：勾选并简述文件
6. 全部完成后跑：
   - `workspace/_checklists/编码完成自检清单.md`
   - `profiles/<active>/checklist_编码自检.md`

## 禁止

- 跳过方案/接口文档自己定字段
- 违反 profile 禁止项
- 扩大需求外重构

## 开始

读 `workspace/<需求名>/03_编码任务.md`，从 Task1 开始。
