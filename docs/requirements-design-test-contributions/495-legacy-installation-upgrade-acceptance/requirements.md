# #495 最终验收需求增量

状态：隔离 successor candidate，expected current `.72`，拟晋升 `.73`；尚未 promotion。完整继承 [`.72` Requirements](../../requirements/versions/current-main-0.6.17-guru.72/requirement-main.md) 的 `R495-01..08`，仅下述 `R495-05 / MIG-495-06` 样本来源由 [live 范围说明](https://github.com/castbox/guru-trellis/issues/495#issuecomment-6028281048) 明确调整。其它 MIG-495-01..09 的验收和无人员/current-only 边界不变。

`R495-05`：原始旧在途事务不可取得时，允许固定 core `0.6.16` / Guru `0.6.16-guru.41`、旧 source `a32ffdca61f432bc6c3e0557fe68486c1422d08f` 的隔离构造代表样本。通过正式旧 native task 入口与 canonical Finalizer harness，在正常执行中只读保存正式 writer 已写出的非 terminal 状态，原路径继续正常完成。不得手填 transaction/checkpoint/hash/gate，不改生产控制流，不故意失败。

构造 provider 仅为明确的 test double，不证明真实 GitHub 发布或业务原始在途。新固定来源的 public migration 必须识别、诊断并原字节/模式保留旧任务及事务，给出 pinned-old/manual 处置；不复用旧 gate，不重复 commit/push/PR/merge。已有 PR 与已合并交付继续单列真实 live facts，不能用构造 provider 替代。证据类型与执行结果见 [test.md](./test.md)。

知识晋升只更新 reviewed accepted scope 和验证事实；独立 committed full-diff review、expected-current promotion 及 promotion 后 fresh gates 完成前不进入最终 merge/Completion。固定验收来源不是软件 Release；真实业务升级与完整累计多平台矩阵仍是独立边界。
