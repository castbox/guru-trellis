# 准备 v0.7.0-guru.8 正式发布：整体需求

## 1. 来源与术语

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| https://github.com/castbox/guru-trellis/issues/746 | 准备任务、目标与背景、范围边界 | Direct Source，reference_only；后续发布仍由 Issue 承担。 |
| .agents/skills/release-guru-trellis-version/references/contract.md | Stage 1、版本轴、freshness | 规范性设计约束：双阶段、原 owner、两次独立完整 Branch Review、真实 dogfood。 |
| .trellis/workflow.md | Phase 1–3 | 当前 Task/Delivery 生命周期与 gate 权威。 |

extension revision 是公共扩展版本；Fork CLI/Core 是固定 Trellis 依赖。dogfood 是本仓库实际受管安装。

## 2. 背景与问题

main 的 canonical extension 仍为 0.7.0-guru.7，公开文档仍把 .6 称为稳定版、.7 称为未发布。真实前驱已是 v0.7.0-guru.7。准备目标为 0.7.0-guru.8，沿用 Fork CLI/Core 0.7.0-castbox.6 及 source lock 17015f987166f4106034f115d23212446f16d536。

Codex 公共 Skill 已迁移至 .agents/skills；私有发布合同仍要求旧 .codex/skills 核对。必须对齐当前受管清单，不能恢复退休副本或把缺失当作通过。

## 3. 目标与非目标

交付可进入 post-merge exact-candidate Gate 的版本、公开说明和真实 dogfood 安装，完成 Docs/Architecture/RDT 收敛与 Task 正常终态。

本 Task 不承担 tag、Release、post-merge smoke、发布后主仓安装收尾或 #746 关闭。这些仍由发布 Issue 承担。不实现其它 Issue、不改上游或全局包、不转换历史 Task、不升级业务仓库或生产环境。

## 4. 真实调用方、场景与流程

| 场景 | 调用方与前置 | 动作与处理 | 可观察结果 |
| --- | --- | --- | --- |
| S1 版本准备 | 发布 Agent，main 基线 | 更新 canonical、maintenance/schema/断言及公开说明 | 版本映射唯一，前驱与候选状态真实 |
| S2 入口核对 | 当前平台与 installer | 对齐公共与私有 Skill 实际投影 | 退休公共目录不再作为要求，有效入口保留 |
| S3 实际安装 | 原 tools owner，完整干净已提交来源 | source_locked 更新 Task checkout dogfood | extension、CLI、来源、全部 managed bytes 和 lock 可验证 |
| S4 交付收尾 | 原 Check/Review/Publish/Finish owners | 晋升前后分别 Check、提交、完整独立 Review，Refs-only PR 与归档 | Task 正常终态，#746 保持开放 |

## 5. 行为要求

- R1：extension 为 0.7.0-guru.8，tag 为 v0.7.0-guru.8。保持 Fork 0.7.0-castbox.6 和固定 lock；同步当前版本约束与必要断言，不改历史归档。
- R2：公开文档区分已发布前驱 .7、准备候选 .8 和真实依赖。marketplace 与 preset 使用相同 immutable source，不提前宣称发布或验证成功。
- R3：按 Codex .agents/skills 迁移语义修正私有 release 合同与实际发现投影；私有 release Skill 不进入公共 registry/manifest/package/安装清单。
- R4：原 guru-upgrade-tools 由完整干净已提交来源使用 source_locked 实际更新 dogfood；throwaway 不代替本地安装。保留 Task/archive/workspace/session、用户配置、peer tools 和 common runtime 指针，不转换历史记录。
- R5：形成稳定规划和 Docs Plan。晋升前 Phase 2、原 TaskCommit、独立完整 Branch Review 均完成且零开放 P0–P3 finding 后，才串行晋升。晋升后重新 Check、原提交和第二次完整独立 Review。
- R6：原 Delivery Review/Publish/Merge 交付中文 Refs-only PR。Completion 覆盖全部准备范围，Closure 为 no_mutation。原 Finish 完成归档及独立 bookkeeping，原 Cleanup 处理精确资源。
- R7：不创建 task-local release notes、PR/Release body handoff、动态 implement checklist、release-status commit 或发布 ledger。结论限于实际证据。

## 6. 约束与依赖

Markdown 拥有流程与 AI 判断，脚本仅执行事实。main 是开发基线及 PR 目标。canonical 修改后由原 owner 同步 dogfood，验证 source/installed、平台投影、ownership 和 drift。

本 Task 不伪造 Stage 2 的 fresh candidate pass；只执行 accepted scope 所需验证。没有业务字段或外部 API 变化，因此不涉及数据迁移或生产部署。公共 API 和迁移边界必须保持。

## 7. 可观察验收与验证方式

| 验收 | 要求/场景 | 入口与预期结果 |
| --- | --- | --- |
| AC1 | R1–R2/S1 | 核对 canonical、maintenance、schema、README 和适用断言；版本/前驱/依赖一致，未提前声称发布。 |
| AC2 | R3/S2 | source/platform validators、私有 Skill 字节与 registry 核对；有效平台一致，私有 Skill 不分发。 |
| AC3 | R4/S3 | 原 tools preview/prepare/invoke、实际 target validation；版本、CLI、全部受管字节、来源和 lock 匹配，保留内容无损。 |
| AC4 | R5/S4 | 原 Check、两次独立完整 Branch Review、串行 Architecture/RDT；晋升差额重新验证。 |
| AC5 | R6–R7/S4 | public Delivery/PR/merge 与原 Completion/Closure/Finish/Cleanup；终态归档可在 main 验证，#746 不提前关闭。 |

以上是待执行验收，不以文件存在、脚本返回或单次 PR 合并代替完整语义判断。

## 8. 实际未决项

整体准备需求没有必要未决选择。具体版本文件、平台投影与安装入口由 Author/Architecture 从 live source 细化。完整累计多平台矩阵、所有 native host 和真实业务升级不在本 Task；最终保留其未验证边界。
