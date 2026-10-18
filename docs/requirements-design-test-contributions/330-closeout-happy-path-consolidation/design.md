# #330 Design contribution

- `DES-026`：保留四个 package-local semantic Skill，分别增加 recommended facade；workflow
  只路由 stable Skill/exit，不吸收 step-local recorder/checker/executor 或 recovery 规则。
- `DES-027`：Publication、Finalizer 与 Merge facade 使用 process-local checked context 复用
  同一 authority identity 下且 mutation 前未变化的 facts。跨 invocation、跨 Skill 或 mutation
  boundary 必须重新读取；context 不进入 tracked artifact 或 public DTO。
- `DES-028`：Commit facade 消费 prepared candidate locator，并以 ignored minimal success receipt
  绑定 exact candidate/ref/commit identity；成功 mutation 的 stdout-loss recovery 不重复 commit
  或 ref update，正常 terminal consumption 删除 receipt/candidate 和已消费 checkpoint。
- `DES-029`：Finalizer facade 只自动消费 package contract 已声明且 semantic plan 未变化的
  mapped reprepare/recovery。dialogue-local confirmation 只以 current preview identity 作为调用参数，
  不写入 checkpoint、artifact 或 DTO。
- `DES-030`：Merge watcher 独立返回 checks succeeded/failed/pending/head-changed facts，不判断
  readiness。Merge facade 在 expected-head mutation 两侧各捕获一次完整 snapshot，并以 live
  merged state 恢复 mutation-output loss；terminal projection 后清理临时状态并立即停止。
- `DES-031`：normalized operation counters 是结构性收敛 evidence；wall-clock envelope 分为
  Agent orchestration、deterministic command、GitHub API、external CI wait，不能替代 correctness。
- `DES-032`：legacy command IDs 与 schemas 不删除；recommended command 的 package registry、
  Interface、wrapper、canonical/dogfood/installed projection 一致切换，失败时可回退旧路径。

Architecture Baseline 判定为 `no_architecture_impact`：本 contribution 没有改变 owner、跨 Skill
boundary、single-writer、durable authority 或发布职责，只收敛现有 package 内确定性调用面。
