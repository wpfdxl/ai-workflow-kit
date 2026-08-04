# 编码自检（php55-thinkphp-sample）

- [ ] Controller 未直接调 Table/Cache
- [ ] Table 方法以 `Db` 结尾，Cache 方法以 `Cache` 结尾
- [ ] 无 PHP >5.5 语法
- [ ] 无三目、无花括号 if、无业务动态调用
- [ ] 新常量进 Constants，未硬编码散落魔法数（状态类）
- [ ] 跨库/关键写失败有日志
- [ ] 缓存 key 有常量前缀；写路径有失效策略
- [ ] DDL/字段未用保留字滥竽充数
