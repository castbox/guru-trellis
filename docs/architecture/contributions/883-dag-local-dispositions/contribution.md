# #883 DAG 局部处置：Architecture 贡献

Identity：`architecture-contribution-883-dag-local-dispositions-v1`。状态：`proposed`。归属 Task `883-issue-dag-local-confirmation`、generation 0、Delivery `a700dbf6-0310-4c4f-b8e3-ed0c5bc44eac`。本文件是隔离候选。

- Direct Source：[Issue #883](https://github.com/castbox/guru-trellis/issues/883)，2026-11-19T07:01:56Z。固定 before：`8b92022d6cdf8f9debda09ed68602f1d137e3629`，目标 `main`。基线 `guru-trellis-architecture`，宪法 `guru-trellis-design-constitution-v1`，变更合同 `guru-trellis-architecture-change-contract-v1`。
- 独立候选选择 `target_native`。承接 ARCH-FND-002、ARCH-FND-005、ARCH-DOM-ISSUE-REVIEW-INTAKE、ADR-ISSUE-REVIEW-INTAKE。必要决定见 [ADR 拟案](proposed/docs/architecture/adr/dag-local-dispositions.md)，职责定义见 [领域拟案](proposed/docs/architecture/03-domains/dag-local-dispositions.md)。真实晋升目标为 `docs/architecture/adr/dag-local-dispositions.md` 和 `docs/architecture/03-domains/dag-local-dispositions.md`。相对引用按拟晋升位置解释。
- Before：共享方法持有语义，DAG 维持本地依赖及终局；确认和继续观察之间的同轮衔接未落实，两项指定例外无完整协调规则。After：共享 Markdown 对 DAG 单写处置规则，DAG 入口引用，原 Git 执行者与 Issue 审核/写入 owner 仍读写各自事实；无新 API、调度器或状态。

| 原 concern | 适用性与本批落点 |
| --- | --- |
| authority-binding | 适用。固定 before，规划候选与 final 各走原 3.0；实际提交及晋升由后续原阶段绑定。 |
| constitution-binding | 适用。以仓库宪法处理职责内聚、最小复杂度与兼容。工具事实不获得授权判断，授权不持久化。 |
| boundary-and-decision | 适用。选择 target_native 和 ADR；同轮观察及两项例外的执行定义单写在共享方法。 |
| owner-and-single-writer | 适用。协调者只安排原 owner；RDT、Architecture、安装各保留其原单写职责。既有直接真人确认仍约束协调者。 |
| compatibility-and-exit | 适用。成套安装采用；无新旧 dual-read、兼容层或公开接口迁移。Sequence 不获得两项例外。 |
| gap-and-deviation | 适用。修复 #883 的同轮退出及局部解阻规则缺口；实际候选证明前不标已关闭，无新增可接受偏移。 |
| parallel-scope | 适用。规划只写本 Task/D1 与本隔离贡献；仅原写入 owner 可在实施后按真实差额整合共享 current。 |
| evidence-and-freshness | 适用。V1 复用固定旧版隔离复现和独立载体证据；V2、V5、V6 由真实候选执行。定向安装与原生 App 的证据独立报告。 |
| review-and-promotion | 适用。Planning final 绑定实际设计和本贡献。实现与工程证据后，原 owner 核对实际 targets、before/expected-current、写入并回读。提交后原独立 Review 才核证晋升语义。 |

不移除既有资源、不改共享导航。实际目标在晋升前发生变化时，由原维护方评估影响并整合仍有效条件；普通冲突或权限改变回原 owner。项目检查沿现有 `guru-trellis-architecture-convergence@1`。不以本文件预填实施、安装或晋升结果。
