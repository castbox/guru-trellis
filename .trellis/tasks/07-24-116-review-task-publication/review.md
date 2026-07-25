# Issue #116 Branch Review 汇总

## 审查范围

- Base：`origin/main@bdc8f50bcd1e325aed331d4b01107b83ed8ee940`
- Reviewed HEAD：`aacb6e02e5386578bfe3d046511a0002a51cb581`
- 完整范围：`origin/main...aacb6e02e5386578bfe3d046511a0002a51cb581`
- Issue scope：close `[116]`；related `[115,131,144,146]`；follow-up `[81,117,118,119,132]`
- Docs SSOT：`ssot_first`，Phase 2 记录的 16 个 durable paths 已同步

## 审查轮次

- [Round 01：完整范围独立审查，发现 1 个 P2](reviews/round-01-final-release.md)
- [Round 02：同身份问题发现 owner 归属与正常路径复现](reviews/round-02-problem-discovery.md)

Round 01 使用此前未参与实现、Phase 2 或 Branch Review 的独立 technical
identity 完成 330-file committed diff、live issue、规划、Docs SSOT、
runtime/package/preset/platform、安装升级、安全部署和完整测试审查。由于该轮发现
finding，不能作为最终放行依据。Round 02 不重复全量测试，仅在相同 HEAD 上复核
finding 的正常路径 reproduction、current-scope qualification 与 owner role 绑定。

## 当前问题

### BR116-R02-P2-01：publication checker 未按 closed allowlist 拒绝意外 task-local 文件

- Severity：`P2`
- Scenario：`normal_required_behavior`
- Status：`open`
- Owner round：`2`
- 影响路径：
  - `trellis/skills/guru-team/packages/guru-review-task-publication/interface.json`
  - `trellis/workflows/guru-team/scripts/python/guru_team_trellis.py`
- 合同依据：PRD R3/R4/R6、批准 design/implement、public Interface
  `review_range_and_working_tree=reviewed HEAD plus contract allowlist only`
- 正常路径复现：在隔离普通 Git repo 新增
  `.trellis/tasks/fixture/debug-note.md` 后，repository binding 的
  `status_paths` 包含该文件，但 checker 得出 `non_metadata_status=[]` 且未拒绝。
- 影响：honest-but-fallible 流程可能在非白名单 task-local tail 存在时记录或接受
  `ready`，未兑现确定性 fail-closed entry contract。

## 被拒绝候选

- Phase 2 首次 throwaway 的空 response 在同 fixture 7/7、第二次 clean
  throwaway exit 0 和本轮 fresh throwaway exit 0 中均未复现。该候选保留为
  `rejected_candidate`，不带 severity，也不通过并发、TOCTOU 或 fault injection
  扩大当前范围。

## 验证证据

- Runtime：570/570，13 skipped
- Skill packages：174/174
- Preset：45/45
- Ownership：9/9
- Source/installed publication contract：16/16 × 2
- Source/installed wrapper eval：7/7 × 2
- Fresh throwaway install/update/reapply：exit 0
- Workspace boundary、task/planning/Phase 2、overlay drift、source checkout：通过

## Docs SSOT、安全与部署

Durable docs、task artifacts、code/tests 除当前 finding 外保持一致；现有合同已经
要求 exact allowlist，缺口位于 runtime 兑现。未发现 secret、credential、私钥、
签名 URL、`.env`、客户数据或敏感原始记录泄漏。无 CI/CD、容器、Kubernetes、
Helm、DB migration、Makefile、依赖 manifest 或生产服务部署变更。

## 结论

当前存在 1 个正常路径可复现的 current-scope P2 finding，无 P0/P1/P3。
Branch Review Gate 的合法出口是 `implementation_required`，不得进入 publication
review、push、PR、Issue close、archive 或 finalize。修复后必须重新执行完整 Phase 2、
task commit、问题闭环审查，并由新的最终放行审查代理覆盖完整最终 range。
