# doc — 接口文档

进行中：`doc/<需求名>/<需求名>接口文档.json`  
归档：`doc/archive/<需求名>/`

**命名约定**：`<需求名>` 与 `workspace/` 下需求目录一致。  
示例目录在 workspace 侧加 `_example_` 前缀，去掉前缀后与 doc 同名：

| workspace | doc |
|---|---|
| `_example_健康检查摘要/` | `健康检查摘要/` |
| `_example_用户资料查询/` | `用户资料查询/` |

## 预览

```bash
cd doc
python3 sbdoc_web.py --port 9122
```

配置：`hfdoc_config.json`。
