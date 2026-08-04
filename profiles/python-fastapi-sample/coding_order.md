# 编码顺序（python-fastapi-sample）

1. models（如需表/实体）
2. schemas（请求/响应）
3. repository
4. service
5. api router + Depends
6. 测试（若任务要求）
7. 接口文档 json（若需要；亦可依赖 OpenAPI 导出说明）
8. 跑 checklist + 通用自检
