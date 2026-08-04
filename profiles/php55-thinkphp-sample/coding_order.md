# 编码顺序（php55-thinkphp-sample）

按 Task 拆分，每步可独立验证。

1. Constants（如有新增常量/错误码）
2. Table（Single；含 JOIN 的单独说明）
3. Logic（业务 + 事务）
4. Cache（如有）
5. Controller / 对外入口
6. 接口文档 json（如本需求需要）
7. 跑 `checklist_编码自检.md` + 通用编码自检
