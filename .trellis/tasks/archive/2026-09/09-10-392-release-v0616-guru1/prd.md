# #392 发布 v0.6.16-guru.1

## Goal

将固定使用 `castbox/Trellis@ad332e3fe5a19d7274cb03e7c2f3e2128f8de291`
和 Trellis CLI `0.6.16` 的 Guru Team extension 正式发布为 repository annotated
tag / GitHub Release `v0.6.16-guru.1`，并将 extension revision 提升到
`0.6.16-guru.41`。

## Background And Current Facts

- 当前 `main` 起点为 `96c441e4e961e47447c73b57d5d2efae57355742` 的后继
  `96c441e4e961e47447c73b57d5b565099ce45dfe`，包含 #378 / PR #391 的固定
  Fork 来源与会话隔离交付。
- `trellis/presets/guru-team/source/trellis-source.json` 已固定 Fork full SHA 和
  CLI `0.6.16`，canonical manifest 仍为 extension `0.6.15-guru.40`。
- 当前正式 predecessor 为 annotated tag / GitHub Release `v0.6.15-guru.6`，其
  peeled commit 为 `be70390f5eca1dfadf5bf792d5d2efae57355742`。
- `v0.6.16-guru.1` tag 与 GitHub Release 尚不存在；release-facing 文档、fixture
  和 current Architecture/RDT authority 仍包含 predecessor 映射或 #378 过渡状态。
- #378 的验证只证明 fixed Fork 接入，不能替代本次 fresh exact-candidate Release
  Gate。

## Requirements

- `REQ-392-01`：canonical、dogfood、installed manifest 必须一致声明 extension
  `0.6.16-guru.41`，target/required/tested Trellis CLI 保持 `0.6.16`。
- `REQ-392-02`：README、workflow/preset 文档、fixture、schema、validator 和稳定安装
  入口必须使用唯一 current mapping：`v0.6.16-guru.1` /
  `0.6.16-guru.41` / CLI `0.6.16` / fixed Fork full SHA。
- `REQ-392-03`：移除 current surfaces 中旧 target、旧候选状态和
  “`v0.6.15-guru.6` 尚未发布”这三类过期陈述；历史文件继续保留当时事实。
- `REQ-392-04`：从 `.47` 派生新的 Requirements、Design、Test 与 Architecture
  current authority，记录 #392 version/publication contract，并将 `.47` 标记为
  immutable superseded evidence。
- `REQ-392-05`：repository-private release orchestration 必须支持 preparation delivery
  在 serialized Architecture/RDT promotion 前后各完成一次 fresh Phase 2、task commit 和覆盖
  `origin/main...HEAD` 的独立 Branch Review；每次 P0-P3 open findings 必须为零，且
  promotion-created diff 未复核时不得进入 Publication/Finish。
- `REQ-392-06`：准备 PR 合并后重新 fetch `origin/main`，冻结一个 commit/tree
  exact candidate；准备分支 HEAD、#378 evidence 或其他 SHA 的结果不得复用。
- `REQ-392-07`：exact candidate 必须完成 Issue #392 与 release contract 指定的
  source/installed、四平台投影、ownership、dogfood drift、clean/existing install、
  update、workflow preview/switch、preset reapply、Fork source/build、代表性业务仓库
  installed smoke、secret scan 和递归 residue 验证。
- `REQ-392-08`：task commit、push、PR、merge、annotated tag、tag-pinned smoke、
  GitHub Release、Issue close 和 cleanup 各自使用当前 live authority 与独立确认。
- `REQ-392-09`：发布流程不得创建 task-local release notes、Release body handoff、
  动态发布 checklist 或 tracked lifecycle 状态。

## Acceptance Criteria

- `AC-392-01`：所有 current release-facing surfaces 对四个版本/来源轴无冲突，且
  source lock 使用完整 SHA，不以版本号替代构建来源证明。
- `AC-392-02`：新的 Architecture/RDT authority 成为唯一 active current identity，
  `.47` 及更早版本保持 immutable/superseded；traceability 覆盖本任务 requirement、
  design、test 和 Architecture contribution。
- `AC-392-03`：canonical、dogfood、installed package 检查、managed byte/mode parity、
  overlay reapply 和 drift 检查通过，无未处理 `.new`、`.bak` 或未知 sidecar。
- `AC-392-04`：pre-promotion delivery 与 promotion-created delivery diff 分别通过 fresh
  Phase 2、task commit 和独立完整 Branch Review，P0-P3 open findings 均为零；
  repository-private release skill 四平台投影与合同测试覆盖该顺序，局部或历史验证不会被
  表述为本次发布通过。
- `AC-392-05`：合并后的同一 exact candidate 通过全部 Release Gate；任何 `FAIL`、
  `SKIP`、stale、cross-SHA、unknown/multiple/unmapped exit 都阻止 tag 创建。
- `AC-392-06`：经独立确认创建并 push annotated tag `v0.6.16-guru.1`，live 回读
  tag object、peeled commit 和 candidate 一致，tag-pinned smoke 通过。
- `AC-392-07`：经后续独立确认创建非 draft、非 prerelease 的 GitHub Release，live
  latest stable 属性与 tag 一致；再单独完成 Issue #392 closeout。
- `AC-392-08`：不发布 npm package，不重写历史 tag/Release/main，不隐式升级或部署
  业务仓库、数据库、容器、Kubernetes 或生产基础设施，不泄露 secret 或本机路径。

## Out Of Scope

- 发布或修改 `@mindfoldhq/trellis` npm package。
- 移动、删除、重建历史 tag、Release 或 main history。
- 为业务仓库执行升级、部署或生产写操作；代表性 installed smoke 只验证安装消费。
- 新增公共 Skill、typed exit、schema API 或与本版本发布无直接 consumer 的兼容层。
- 恶意伪造、并发压力、TOCTOU、锁、异常 crash consistency 或跨 OS 加固。

## Open Questions

无。Issue #392、当前仓库事实和 repository-private release contract 已确定发布轴、
验证范围、兼容边界与独立副作用确认规则。
