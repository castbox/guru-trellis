# #466 最小必要复杂度贡献

状态：implementation candidate draft / non-current；source：[Issue #466](https://github.com/castbox/guru-trellis/issues/466)；TaskId：`466-no-speculative-extension` / generation 0。

## Authority binding

Guru public contract：`guru-maintain-architecture-baseline:2.0`；expected-current Architecture/RDT：`current-main-0.6.17-guru.76` / active；baseline locator：`docs/architecture/README.md`；constitution：`docs/architecture/00-foundation/design-constitution.md` / `guru-trellis-design-constitution-v1` / current；change contract：`guru-trellis-architecture-change-contract-v1`；concern set：`guru-trellis-architecture-change-concerns-v1`。

本文记录 task 的适用结论与晋升职责，不拥有原则正文。五 identity/short name不变，实际命中 `minimum-necessary-complexity` 与 `cohesion-change-isolation`；无原则例外。

## Concern applicability

| Concern | 适用性与当前设计依据 |
| --- | --- |
| authority-binding | applicable：读取上述四 authority；规划与 proposed amendment 不能冒充 current。 |
| constitution-binding | applicable：只在唯一 authority 内强化既有原则；公共包/fixture/spec 不复制正文。 |
| boundary-and-decision | applicable：R466-01..06、C466-01..06；唯一 `target_native` path，复用原 semantic/route boundaries。 |
| owner-and-single-writer | applicable：Architecture owner判断与晋升；原 Planning/qualification/Check/Review owners 消费；runtime只验证事实。 |
| compatibility-and-exit | not_applicable：本任务不新增或删除生产兼容层。当前兼容/迁移是语义示例审查对象，现有真实 support/owner/exit 不变。 |
| gap-and-deviation | applicable：解决当前原则解释/消费缺口；不新建或重开 GAP，不扩大已记录历史 debt。 |
| parallel-scope | applicable：task文件、贡献、candidate、canonical包在隔离worktree中修改；禁止并行直接写 shared current/GAP/owner。 |
| evidence-and-freshness | applicable：Planning绑定当前source；Phase2审candidate，Branch Review审完整committed范围；Test contribution持有实际结果。 |
| review-and-promotion | applicable：独立review后expected-current promotion；current推进则sync_required；晋升diff执行fresh gates。 |

## Before / candidate after

Before：当前原则举例覆盖窄，必要性证据与污染 Requirement 的回程解释不完整；authority、五 identity、现有 stage/owner/routes 均已存在。

Candidate after：三个 canonical package contract 已消费完整新增能力与既有回程；Check/Branch Review 薄入口同步。六类案例集中在 [proposed amendment](./466-no-speculative-extension-proposed-amendment.md)，只承载待晋升增量，不是 current authority。RDT contribution 已闭合 R466 -> D466 -> C466/Test。实际验证只由唯一 Test contribution 持有；candidate 不证明独立 committed review 或 promotion 已完成。

Change path：`target_native`。ADR：不需要，原因是强化现有原则适用解释，不改变architecture decision、原则tradeoff/exception、GAP lifecycle、owner、single writer或compatibility exit；实际发现这些变化时回Planning。

## 检查与晋升

Project-check：`guru-trellis-architecture-convergence@1`，descriptor `guru-trellis-architecture-convergence:repository:1`，entrypoint `docs/architecture/06-governance/change-contract.md`；rule `ARCH-GOV-006..009`，decision `ADR-005/ADR-009`，GAP `ARCH-GAP-006/ARCH-GAP-008`。Planning结果只判断本计划满足current边界，未执行候选/安装测试；后续stage每次重新绑定current候选。

Review：pending；promotion：未执行。独立committed review范围与promoted identity只能在实际完成后记录，不预填passed。expected current变动时重读authority、对齐同一task与contribution并重审；不覆盖其它任务的新current。

RDT/test consumer： `docs/requirements-design-test-contributions/466-no-speculative-extension/traceability.md` 与唯一 `test.md`；promotion消费proposed amendment后删除候选副本，长期事实由本贡献、唯一current与Git历史承接。
