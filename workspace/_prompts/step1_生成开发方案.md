# Step1 Prompt：生成开发方案

> 用法：复制下面整段给 AI，并附上 `workspace/<需求>/00_需求.md`。  
> 产出：`workspace/<需求>/01_开发方案.md`（结构见 `_templates/01_开发方案模板.md`）

---

你正在 **AI Workflow Kit** 中协助生成开发方案。

## 必读

1. 根目录 `PROJECT.md`（active_profile、code_root、rules_path）
2. 该 profile 的 `RULES.md` 与 `coding_order.md`
3. `workspace/_templates/01_开发方案模板.md`

## 必须遵守

1. **只**遵守当前 active profile 的规范；不要套用其他 sample 或其他业务仓规则
2. 先在 `code_root` 内搜索类似实现再写方案，禁止凭空臆造已有封装 API
3. 方案第 9 节 Task 顺序对齐 `coding_order.md`，每个 Task 可独立验证
4. 不确定处放入第 10 节「待人肉确认」，不要瞎填
5. 接口清单写清方法/路径/鉴权/端

## 输出要求

- 严格按模板章节顺序
- 核心流程覆盖分支、异常、边界
- 若有缓存/跨服务，写清策略

## 需求内容

<把 00_需求.md 内容贴这里>
