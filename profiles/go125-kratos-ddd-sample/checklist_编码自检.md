# 编码自检（go125-kratos-ddd-sample）

- [ ] 依赖方向：server→service→biz←data，无 biz import data 实现细节
- [ ] 跨服务未 import 对方 `internal`
- [ ] DB/Redis 仅出现在 `internal/data`
- [ ] proto 已重新生成；未手改生成文件
- [ ] 业务错误使用 Kratos errors，非随意字符串
- [ ] 关键 error 未静默丢弃
- [ ] 通过 gofmt；Go 版本声明与 go.mod 一致（1.25）
- [ ] 缓存/密钥未进日志
