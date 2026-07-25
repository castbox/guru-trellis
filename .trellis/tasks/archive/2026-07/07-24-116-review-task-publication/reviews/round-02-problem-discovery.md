# #116 Branch Review 第 2 轮问题发现连续性报告

## 审查身份与结论

- 审查角色：独立 `问题发现审查代理`
- 审查代理：`/root/issue116_branch_review_round1`
- 审查轮次：`round-02`
- 连续性来源：[round-01-final-release.md](./round-01-final-release.md)
- 结论：`implementation_required`
- 问题数量：`1`（P0=`0`，P1=`0`，P2=`1`，P3=`0`）
- 目的：将 round 1 已发现并完成资格审查的 current-scope finding，按问题发现 owner 的 logical role 留下可供 finding lifecycle 消费的原始证据；本报告不覆盖、不重写 round 1。

## 审查绑定

- GitHub issue：`castbox/guru-trellis#116`
- 工作树：`/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/116-review-task-publication`
- 基线：`origin/main`
- 基线 HEAD：`bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- 审查范围：`origin/main...aacb6e02e5386578bfe3d046511a0002a51cb581`
- 审查 HEAD：`aacb6e02e5386578bfe3d046511a0002a51cb581`
- HEAD 连续性：本轮重新执行 `git rev-parse HEAD`，仍为上述 SHA；round 1 之后没有新的 committed implementation diff。
- 工作区边界：boundary validator 为 `status=ok`，expected workspace 与 actual repo root 均为上述 task worktree，source checkout 干净，`suspicious_source_artifacts=[]`。
- Round 1 证据身份：SHA-256 `e1935435de055e1be8a452d6564c90ee8e9557dea2de444ab72d4beabe84a314`，大小 `13286` bytes。

## 复用证据范围

本轮不重复 full-range diff 阅读和全量测试，复用 round 1 已完成并记录的以下证据：

- 完整 330-file `origin/main...HEAD` committed diff 审查；
- live issue、官方 Trellis 文档、`prd.md` / `design.md` / `implement.md`、planning approval、Phase 2、Docs SSOT、Issue Scope Ledger 与完整 implementation handoff；
- runtime 570/570（13 skipped）、Skill package 174/174、preset 45/45、ownership 9/9；
- source/installed publication contract 16/16 × 2、Branch Review contract 8/8 × 2、wrapper eval 7/7 × 2；
- fresh throwaway install/update/reapply exit 0，source/installed/platform、ownership、dogfood drift 与 marketplace sample 验证通过；
- Docs SSOT `ssot_first` 的 16 个 durable path 与 handoff digest 一致。

这些证据均绑定同一审查 HEAD，本轮只重新核对 HEAD、finding 代码路径、合同依据、正常路径 reproduction 与 qualification。

## 问题发现

### P2：Publication checker 把任意 task-local working-tree 文件当作允许的 metadata tail

- Finding ref：`BR116-R02-P2-01`
- Round 1 原始 ref：`BR116-R01-P2-01`
- 场景分类：`normal_required_behavior`
- Qualification：`qualified_current_finding`
- Severity：`P2`
- Status：`open`
- Route：`implementation_required`
- 位置：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json:30`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:14085-14115`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py:14943-14956`
- 合同依据：
  - PRD R3 要求 Branch Review 后出现非 allowlisted metadata drift 时失败关闭；
  - PRD R4 的 `metadata_tail_integrity` 要求仅有 allowlisted task metadata tail；
  - design 要求非 allowlisted tail 停在 entry gate，并由 contract closed allowlist 管理 metadata revision；
  - approved implement Step 4 要求只接受 contract 指定 publication metadata paths，并覆盖 `non-allowlisted tail` 负例；
  - public Interface 将 `review_range_and_working_tree` 绑定定义为 `reviewed HEAD plus contract allowlist only`。
- 代码事实：repository binding 记录除 `pr-readiness.json` 外的全部 Git status path；checker 随后只把“不在当前 task prefix 且不在 `.trellis/.runtime/`”的路径视为非 metadata drift。整个 task prefix 被豁免，没有按 publication contract 的 closed allowlist 逐项验证。
- 本轮正常路径复核：在新的隔离临时 Git repo 建立已提交 baseline 与 `origin/main`，执行普通误操作新增 `.trellis/tasks/fixture/debug-note.md`，调用当前 runtime 后得到：

  ```json
  {
    "status_paths": [".trellis/tasks/fixture/debug-note.md"],
    "checker_non_metadata_status": [],
    "unexpected_task_local_file_is_rejected": false
  }
  ```

- 资格判断：该复现不修改既有 artifact/hash/state，不需要恶意 actor、故意伪造、并发、TOCTOU 或 fault injection。普通 task-local 临时文件即可进入受支持正常路径，因此属于 `normal_required_behavior` 下的 current acceptance violation，可以进入 P0-P3。
- 影响：honest-but-fallible reviewer 若漏看该路径，deterministic checker 不会兑现 exact allowlist 的 fail-closed entry contract，仍可在意外 task-local tail 存在时记录或接受 `ready`。
- 修复要求：
  1. 定义并复用精确的 publication task metadata/runtime-input allowlist；
  2. recorder/checker 对 `status_paths` 每项做 allowlist 校验，非白名单 task-local path 在 `ready` 路径必须失败；
  3. 增加 source/installed/runtime 负例与已批准 metadata 正路径回归；
  4. 同步 canonical、dogfood、selected-platform copies，并重新执行 Phase 2、task commit 与完整 Branch Review。

## 被拒绝候选

### Phase 2 首次 clean throwaway 的一次空响应

- 场景分类：`normal_required_behavior`
- Qualification：`rejected_candidate`
- 依据：同一 fixture 后续 7/7 eval 通过，Phase 2 第二次 clean run exit 0；round 1 fresh throwaway install/update/reapply 也 exit 0 且未出现空响应。
- 结论：没有在当前正常路径独立复现，不计 finding。通过并发/TOCTOU/fault injection 压力重造 transient response 属于 `out_of_scope`，不得进入 P0-P3。

## 验证结果

- HEAD/边界复核：通过。
- P2 隔离正常路径复现：通过，结果与 round 1 一致。
- Lint/TypeCheck/全量 tests：本连续性 follow-up 未重复运行；复用同一 HEAD 的 round 1 完整证据。
- Recorder/Gate：未运行。
- Commit/Push/PR：未执行。

## Docs SSOT 与影响

- Round 1 已确认 durable Docs SSOT、task artifacts、code/test 除本 finding 外整体一致；exact allowlist wording已存在于 approved planning、Interface 与 durable contract，问题在 runtime 未兑现，而不是缺少需求授权。
- 本轮没有修改 durable docs、task plan、Phase 2、implementation handoff、assignment、review gate 或实现文件。
- 安全/部署判断沿用 round 1：无 secret 泄漏，无 CI/CD、容器、K8s/Helm、DB migration、Makefile、依赖 manifest 或生产服务部署变更；本 finding 是正常 correctness/fail-closed 缺口。

## 结论

`BR116-R02-P2-01` 已由 `问题发现审查代理` 在同一 HEAD 上完成正常路径复现、current-scope qualification 与 P2 定级，状态为 `open`。当前分支应进入 `implementation_required`，不得记录 Branch Review pass、finish-work、push、PR 或 close issue；修复后由问题闭环审查与新的最终放行审查继续处理。
