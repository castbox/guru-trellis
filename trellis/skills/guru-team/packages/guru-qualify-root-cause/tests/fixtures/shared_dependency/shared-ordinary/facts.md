# 行为合同

继续当前标量缓存消费者交付。调用入口是 app/service.py 的 lookup_twice，重复标量查询只加载一次。当前 app/ 与 schema/ 是已提交内容。observed/release-note.md 是提供的版本备注，代码和生成链没有差额。

frozen/ 是当前入口、SDK、生成物与输入的副本。local-observation.json 是本次宿主实际执行 frozen/run.py 的命令、环境及结果。该观察使用与当前相同的 pure Python client、输入 pear 和重复查询行为，未调用网络。当前下一步需要由实施 owner 判断。
