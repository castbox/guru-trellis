# #916 基线复现记录

Guru 基线为 `8604558695dfd9d8ea2181406a87ece70d9eea63`。测试使用项目锁定 Trellis Fork `e3793251fad8bd261d0c370d408c7675b9f6a140`。三个隔离工作区从同一临时仓库提交 `86ab7d539b31c3c530b382b0c6e0c8fc724a2ac4` 启动，均走原 `delivery_promotion` 入口。

| 样本 | 实际观察 |
| --- | --- |
| A，Job Search 增加来源索引 | 原 owner 在首次实际写入前移除只追加版本摘要的根目标。实际修改所属单元和 export 关系，根 README 字节和稳定身份与基点一致。两份文件各多一个末尾空行。 |
| B，Backup Recovery 报告保留校验状态 | 原 owner 写入完整能力和报告关系并读回。根 README 字节和稳定身份与基点一致。 |
| C，新增实际职责发现范围 | 原 owner 将新的查找范围写入根 README，写入所属单元并读回。正式入口首次返回 `baseline_current / integrated_pending_review`，稳定根身份保留。 |

A、B 首次 wrapper 返回 `stale_identity/candidate`。后续恢复获得 `baseline_current / integrated_pending_review`，恢复过程使用内层重建逻辑或同一算法。保留两轮结果。候选绑定出错没有造成 #916 所述根误写。匹配 Fork 的原 promotion 套件执行 16 项，全部通过。

另一份诊断向正式 wrapper 提交 fixture 已写入的版本摘要目标。它仍返回 `baseline_current`。这个结果覆盖写后客观绑定。实际语义决定由已安装的原 Architecture owner 在写入前作出。普通、合法例外和部分写入恢复仍由同一 owner 承接。核对 canonical、dogfood 和声明平台后，本任务相关的 Skill 与 contract 文件内容一致。

## 重跑材料

本机隔离样本目录为 `/tmp/guru-916-native.ulfa2Y`。在该目录运行 `bash replay-case.sh a`、`b` 或 `c`。脚本从保留的 fixture 提交重新克隆，生成新的独立运行目录。A 的触发输入是 `normal-proposal.json`。B、C 的触发输入是各自目录的 `proposal.json`。记录各自的 `observations.json`、`architecture.diff` 和 `native.events.jsonl`。写后诊断在 `/tmp/guru-916-baseline.OhJWtY` 下保存了起点、输入、差异和正式 stdout。

当前样本没有复现独立单元误写共享根入口。没有发现可归属本 Issue 的具体当前修复点。正式实施需要受支持的失败入口、触发输入和实际误写结果。后续若出现上述证据，由同一 Delivery 的原 Author 更新修复点和验证方式。
