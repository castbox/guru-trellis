# 标量缓存消费者设计

采用 app/service.py、app/cache_proxy.py、app/scalar_cache.py 和 app/generated_client.py 的现有调用链。schema/ 标识生成输入，版本备注见 observed/release-note.md。本地行为观察见 frozen/ 和 local-observation.json。没有新增接口或持久化方案。
