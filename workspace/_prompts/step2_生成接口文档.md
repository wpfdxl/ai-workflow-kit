# Step2 Prompt：生成接口文档

> 用法：`01_开发方案.md` 人肉定稿后，复制下面整段给 AI。  
> 产出：`workspace/<需求>/02_接口文档.md` + `doc/<需求>/<需求>接口文档.json`

---

你正在 **AI Workflow Kit** 中生成接口文档。

## 必读

1. 定稿的 `01_开发方案.md`
2. `PROJECT.md` 与 active profile 的 API 约定（响应包装、路径风格）
3. `workspace/_templates/02_接口文档模板.md`

## 任务

1. 按模板写 `02_接口文档.md`
2. 同步写 `doc/<需求名>/<需求名>接口文档.json`（SBDoc 风格即可：含 name、data 接口数组；字段含 type/name/remark）

## 必须遵守

1. 每个接口：请求、参数表、业务规则、返回字段、正常/空态/错误示例
2. 类型与枚举写清；每个字段 **remark 必填**（含嵌套）
3. 路径与命名遵守当前 profile，不套用其他栈习惯
4. 顶层包装与 profile「统一响应」一致，业务字段放在约定的 data 区

## 开发方案内容

<把定稿的 01_开发方案.md 贴这里>
