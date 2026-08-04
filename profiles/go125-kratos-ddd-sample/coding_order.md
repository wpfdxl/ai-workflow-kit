# 编码顺序（go125-kratos-ddd-sample）

1. `api/**/*.proto`（若契约有变）并生成代码
2. `internal/biz`：实体/值对象、Repo 接口、usecase
3. `internal/data`：Repo 实现、装配
4. `internal/service`：实现 proto Service，做 DTO 转换
5. `internal/server`：注册 HTTP/gRPC 路由（若需）
6. wire / 依赖注入更新
7. 单测（优先 biz）
8. 接口文档 json（workspace/doc，若需要给人联调）
9. 跑 checklist + 通用自检
