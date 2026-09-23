# #454 C4 Branch Association Test Contribution

状态：`contribution_candidate`。以下是 C4 focused acceptance；它们不构成 promotion-created diff 的 Phase 2、Branch Review、Publication、
production activation 或 Release Gate 证明。

- `T454-C4-01`（R454-C4-01/02）：Draft 2020-12 与 runtime 同时验证 five-field binding、revision 0、strict
  increment、stale/no-op rejection，以及 path/HEAD/session/ownership/binding-epoch/refs namespace/reserved ref rejection。
- `T454-C4-02`（R454-C4-03/05）：隔离 Git fixtures 覆盖 binding+ownership 均存在、仅 binding、仅 ownership、
  两侧均缺失四象限；断言已有一侧不被改写，缺失 ownership 保守投影 caller-owned。
- `T454-C4-03`（R454-C4-04）：覆盖 unique、zero、multiple candidate，registered/local branch 去重，exact task
  artifact/status/generation、wrong repository、registration mismatch、other-task binding 与 unresolved incarnation；
  unique local-only branch 在 provision 前返回 `checkout_acquisition_required`。
- `T454-C4-04`（R454-C4-06）：dirty same-checkout fixture 同时包含 staged、tracked dirty 与 binary untracked bytes；
  换绑前后 HEAD、真实 index hash、worktree hash、status hash 与逐文件 bytes 必须相等。
- `T454-C4-05`（R454-C4-06/07）：existing-target 覆盖 clean exact artifact 与 ancestor-compatible success；artifact
  mismatch 阻塞，不相关历史返回 `rebind_reconcile_required`。
- `T454-C4-06`（R454-C4-08）：target ref 存在 unresolved resource incarnation 时，candidate/prepare 均拒绝复用。
- `T454-C4-07`（R454-C4-09）：post-mutation failure 恢复 checkout branch、target ref absence、binding bytes 与
  ownership snapshot；caller-owned existing target 保持不变。
- `T454-C4-08`（R454-C4-09）：establishment/rebind output-loss recovery 可重复只读调用，结果 revision 不再次递增，
  ownership mutation 调用次数不增加。
- `T454-C4-09`（R454-C4-10）：canonical ownership 与 preset tests 断言 32 active + 3 planned，两个新 ID 无
  package/interface/active graph/installed/platform projection。
- `T454-C4-10`（R454-C4-01..10）：完整 lifecycle runtime、两个 schema/registry/manifest JSON parse、Python compile、
  preset focused suite、task validation、`git diff --check` 与 touched non-generated file 3000-line check 构成 focused evidence。

完整 installer/upgrade/workflow-switch/multi-platform Release matrix 保持 deferred；broader suite 的既有失败必须
如实报告，不得通过越权同步 installed/platform bytes 将 C4 宣称为 production-ready。

当前 candidate focused evidence：task-lifecycle runtime `72/72`，planned-ID ownership `3/3`，installed
extension manifest 定向用例 `1/1`；两个 schema、registry、extension manifest JSON parse、Python compile、task
validation、tracked/untracked `git diff --check` 与 touched-file line limit 均通过。Preset Python suite 为 `85/86`：
唯一错误是 raw apply clean-fixture 检测到 E434 前故意未同步的 installed task-lifecycle README/schema/registry
sidecars，未命中 C4 branch runtime。该 suite 不声明通过，也不授权同步 installed/platform projection。

RDT 与 Architecture current 仍为 `.61/active`，serialized promotion 尚未执行；后续 promotion-created diff
必须 fresh 重走 Phase 2、Task Commit 与完整 Branch Review。C5-C7、D443、D436、E434、#434 activation 与完整
Release matrix 保持未验证。
