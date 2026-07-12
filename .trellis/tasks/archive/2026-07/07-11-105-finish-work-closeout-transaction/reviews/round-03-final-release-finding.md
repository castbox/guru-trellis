# Issue #105 最终放行审查原始报告

## 审查身份

- 逻辑角色：最终放行审查代理
- technical agent：`/root/final_release_review_105`
- 独立性：未参与实现、Phase 2、Round 1 问题发现或 Round 2 闭环
- reviewed HEAD：`fda16ddf5fcef3179ff85eda8ad0a0e8f1e4ddce`
- diff range：`origin/main...HEAD`
- findings_count：`1`
- 结论：`fail`

## 范围与方法

已独立读取 live issue #105、`prd.md`、`design.md`、`implement.md`、planning approval、Phase 2 artifact、issue ledger、agent assignment、Round 1/2 raw reports及完整 47 文件 diff。

逐层审查了 closeout plan/schema、raw UTF-8 PR body、readiness、marketplace verifier、draft PR、final summary、archive blob continuity、partial recovery、13 阶段生产重入、canonical/dogfood workflow、durable specs、README、preset、overlay、五个平台入口和测试。另核对官方 Trellis workflow/marketplace 文档及本机 `gh` 的实际过滤语义。全程只读，未运行 recorder/validator，未修改或发布。

## 发现项

### P1-1：唯一 draft PR 未绑定 head repository，exact `repo/head/base` identity 合同未实现

证据：

- `guru_team_trellis.py:11190` 的查询只读取 `number,url,title,body,headRefName,baseRefName,headRefOid,isDraft`，未读取 `headRepository`、`headRepositoryOwner` 或 `isCrossRepository`。
- 同文件 `PR identity validator:11245` 校验 base repo URL、branch、SHA、title/body、draft 和 summary，但不校验 PR 的 head repository。
- 本机 `gh pr list --help` 明确说明 `--head` 不支持 `<owner>:<branch>`，因此 `--repo target --head branch` 不能把候选限制为 target repo 内的同名 branch。
- 当前测试 fake PR 仅提供 `headRefName/baseRefName/headRefOid`，没有 same-name fork PR 负向场景。
- 需求与 durable SSOT 明确要求同一 exact `repo/head/base`，见 `prd.md:53` 和 `workflow-contract.md:35`。

影响：

同名 fork draft 只要具有相同 SHA、title 和 body，就可作为唯一候选被复用并写入 final summary。archive commit 随后 push 到目标 repo branch，不会推进 fork PR head，三方 HEAD 检查将在 task 已归档后失败；summary 又绑定了该 PR number，普通重试无法改绑。这会重新形成 #105 要消除的 archived-but-unpublished 状态。若 fork head 被外部同步，还可能把错误 head repository 的 PR 转 ready。

建议：

查询并校验 `headRepository.nameWithOwner`、`headRepositoryOwner.login` 和 `isCrossRepository`；当前合同应要求 head repository 与 immutable `plan.git.repo` 相同。同步校验配置 remote URL 指向该 repo。候选筛选应先排除同名 fork，再执行 0/1/>1 判定。补 target/fork 同名、同 SHA、同 title/body，以及 archive 后 recovery 的真实状态测试。

## 问题生命周期

Round 1 的四项 P1 已真实闭环：raw body exact identity、archive blob continuity、旧 Docs SSOT 清理和 13 阶段真实 Git 重入均有实现及测试证据。Phase 2 首轮正确保留未闭环项，第二轮通过后，`b900a3c..fda16dd` 的 9 个非 metadata 文件与 `phase2-check.json.dirty_paths` 精确一致，相关 spec 哈希与最终 HEAD 一致。

本次 P1-1 是最终独立审查新发现，不属于 Round 1 四项的回退。

## 验证证据

独立复跑通过：

- canonical tests：`364/364`
- preset tests：`36/36`
- targeted closeout tests：`30/30`
- Python compile、Bash syntax、4 个 Draft 2020-12 schema、`git diff --check`
- overlay drift、10 组 canonical/dogfood/platform equality
- 旧 archive-first/empty-summary/post-tail 固定语义扫描无命中
- 当前 worktree 只剩允许的 task metadata tail

测试全部通过，但未覆盖本 finding 的 cross-repository head identity。

## Docs SSOT 与范围

Docs 内部事务顺序已收敛，旧合同已清除；但其 exact `repo/head/base` 声明强于当前实现，因此 Docs SSOT 对代码承接结论为 `fail`。

Issue ledger 分类正确：只关闭 #105；#53/#96/#97/#100 为 related；#98/#99/#101 为 follow-up。P1-1 属于 #105 当前范围，不能下沉为 follow-up。

## 部署与安全

未变更 CI/CD、容器、K8s/Kustomize、DB migration、Makefile 或部署资产。未发现 token、secret、私钥、`.env`、客户数据或签名 URL。发布安全仍因 P1-1 未通过。

## 未验证边界

当前分支尚未推送，remote marketplace verifier 和真实 GitHub closeout E2E 尚未执行。远端仍不存在 `v0.6.5-guru.3` tag，不得声称稳定 tag 安装路径已验证。现有 throwaway init/preview/switch/update/reapply 证据已审核，但本轮未重复长链路。

## 观察项

无。

## 后续候选

0。本 P1 属于 #105 当前范围。

## 结论

最终放行审查不通过。必须修复 head repository identity 绑定并补真实负向测试，重新执行 Phase 2、问题闭环和全新最终放行审查后，才能记录通过的 Branch Review Gate 或进入 finish-work。
