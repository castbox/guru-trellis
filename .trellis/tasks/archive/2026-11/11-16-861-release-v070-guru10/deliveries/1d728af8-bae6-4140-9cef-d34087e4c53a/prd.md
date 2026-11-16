# #861 后继：组合交付源正式采用与前驱升级验证

## 1. 整体来源与术语

整体权威为 `../../prd.md`，accepted_scope 为 `sha256:287ca06d18f878e858c70b703c39ef3643084e5aca9df1e41409f842c2e6869d`。当前 Task `744a637b-a044-46cd-8cdd-77ddd85ded8e` / gen1，Delivery `1d728af8-bae6-4140-9cef-d34087e4c53a`，选择 R3/R4/R5/R11、AC2/AC3/AC7/AC9。整体 R6/R7 的交付及收尾顺序仍适用。

| 来源/章节 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/861 全文 | 要求：真实准备、最新 main 最终候选、无其它 Issue 状态前置 |
| `.agents/skills/release-guru-trellis-version/references/contract.md` Stage1/Complete Source Before Actual Adoption/Stage2 | 设计约束：source delivered 后才创建采用切片；本批不进入正式发布 |
| `.agents/skills/guru-upgrade-tools/references/contract.md` 全文 | 设计约束：完整 source_locked、单目标、保留、prepare一次及同操作恢复 |
| 前序 `../178264f4-24da-4e14-b56e-02c6c3d42701/{prd,design,implement}.md` | 原切片与后继责任：本批接实际采用及完整 existing，不重复源修复 |
| PR #871 merge `79c25b5eaafdbcf415393535a16a7b1c0d281284` | 已交付事实：含本批修复及 main 的 #868/#872；这两项是已存在的源事实，不是新增 Issue 依赖 |
| `docs/architecture/04-integrations/distribution.md` ARCH-INT-006/014/015；RDT current/codex-skill-distribution、native-compatibility | 现行约束：来源/CLI轴、平台选择、目标保留与证据分层 |

正式采用指唯一准备目标的原 tools source_locked 安装。existing 指原 verifier 从真实 `v0.7.0-guru.9` 到组合交付源的完整单平台升级验证，不是当前目标的 reapply，也不是累计矩阵。

## 2. 整体与本批目标、非目标

本批独立目标是正式采用已交付完整组合源，消除新 canonical manifest 与准备目标 installed 的实际差额，并完成 AC7/AC9 所需完整 existing。目标仅 `/Users/wumengye/Documents/GoProjects/guru-trellis-worktrees/861-release-v070-guru10-repair`。目标版本 `0.7.0-guru.10`，固定 Fork CLI/Core `0.7.0-castbox.6`，lock `e3793251fad8bd261d0c370d408c7675b9f6a140`。

本批允许对原完整 existing verifier 及其直接回归作必要修复，使其承接原 public tools writer 正常更新的 AGENTS template baseline；不改变 installer、template hash 或受管正文生成规则。不改 canonical 业务行为、schema/selector、Fork或lock；不重做 #868/#872，不转换历史 Task，不安装主目录或peer，不创建新Task/branch/worktree，不执行Finish/tag/smoke/Release/Issue关闭/Cleanup，不扩完整多平台矩阵。

## 3. 本批起点、前序结果、依赖与剩余责任

gen0 #865/#866/#867 保留历史身份。gen1 source Delivery `178264f4-24da-4e14-b56e-02c6c3d42701` 已 delivered，结果 `delivery:79c25b5eaafdbcf415393535a16a7b1c0d281284`，reviewed H `f09afb891cfae105ee808c137301e182804b6092`；merge 的 first parent `434b207fe2d5df75a75ed9552cf17c02a9504527` 已含 #868/#872。原 Completion 实际返回 additional_delivery_required，不能把本工作记为 evidence_pending。

采用源须为包含以上合并结果的完整干净 matching Git source，当前选定 immutable C 为 `79c25b5eaafdbcf415393535a16a7b1c0d281284`。仅 H 的旧 canonical 不含 #868/#872，不能代替 C。源的取得和实际root、canonical clean、目标完整性须由原owner核对；首次规划观察的主目录为434b；该起点不代表后续live source状态。未执行的同步/安装保留原独立边界；已成功操作消费实际原结果，不重复。前驱 `.9` 的 CLI/Fork 从其自身manifest/lock推导，不拿当前值填充。

本批全部installed after及验证经过完整质量/交付后，原Completion才重评整体；no_mutation Closure/Finish和Stage2另有原边界。Stage2仍从届时最新main重新冻结，不沿用b85或本批来源作为最终发布pass。

## 4. 本批调用方、场景与流程

| 场景 | 条件、动作与可观察结果 |
| --- | --- |
| A1 来源准备 | 本批Planning接受后，原source/sync owner取得C完整干净源；版本、CLI/lock、#868/#872源正文及11项清单修正共同存在 |
| A2 正式采用 | 原tools从C的完整canonical launcher预览单目标、一次prepare，独立展示并确认真实写集后invoke；真实manifest由installer产生 |
| A3 目标验证 | 目标自身resolver/installed/native与完整集合bytes/modes、workflow/lock/provenance/current清单一致；Task/session/user/peer保持 |
| A4 前驱验证 | 从真实`.9`安装用原existing入口升级C；完整matrix结果、退役资产、AGENTS合法变换、平台集合及零sidecar成立 |
| A5 正常失败 | 冲突/stale/部分操作失败保留事实，原owner同operation恢复；新source缺陷回原规划，不手改manifest或弱化exact比较 |
| A6 升级阶段前像 | 原完整 existing 在真实 `.9` 安装后调用 public tools writer；verifier 必须用与当前 template baseline 对应的该次正常维护前像判断原 renderer 的精确 after，不能继续把 init 前像当作维护阶段前像 |

## 5. 完整行为、条件与约束

- **A-R1 来源完整性**：source_locked绑定C及其实际HEAD、干净canonical tree和精确Fork build/API；保完整#868/#872正文/投影及本修复，不按版本号或部分文件判等。来源root改变或并行内容变化时原owner刷新判断。
- **A-R2 单目标采用**：平台来自目标exact selection；完整维护workflow、Skills、spec、平台overlay与manifest。AGENTS由原renderer保块外用户正文；配置和未知修改按原preserve/replace及sidecar规则，不直接复制受管副本。
- **A-R3 保留与恢复**：Task/archive/workspace/session/public facts、用户配置、peer tools/common pointers保留。新事务前检查实际相交未完成操作。一次prepare只绑定一个计划；invoke失败沿原ref恢复，不重prepare、不刷新rollback anchors、不普通apply绕过历史guard。
- **A-R4 目标验收**：实际tools_upgraded及正式source-lock成立，并由目标自身入口证明可用；完整expected map/bytes/modes/current API/lock/workflow/provenance和同operation reapply/drift、零sidecar核实。投影/native脚本不宣称真实客户端或生产通过。
- **A-R5 完整existing**：真实前驱`.9`的immutable tag、manifest/lock/CLI/build与C经原existing入口执行完整单Codex cell，保最早失败；tools_upgraded或focused不能替代。原 verifier 必须正确承接 init、前驱 preset、public tools 维护和当前 reapply 各阶段的真实前像。仅接受 baseline 对应的合法原 writer 输入到原 renderer 精确 after；区块外用户内容保留，未知编辑仍失败。不得改写 hash、跳过 unknown drift 或从当前 after 反推并伪造前像。没有必要重复未变source所有tests或累计矩阵。
- **A-R6 交付边界**：全部实际installed after、稳定规划及必要知识整合纳入原TaskCommit与固定B..H完整Review/readiness/Refs-only交付；合并不是whole Completion。本轮返工方案接受前不实施driver修复；已完成操作只消费原结果，后续Git动作保留原独立边界。

## 6. 本批验收、验证方式与未决项

| 验收 | 入口、输入和预期观察 |
| --- | --- |
| A-AC1 | 原source_locked preview/prepare从C完整源与锁定Fork检查单目标；无未解决相交事务/冲突，实际source包含三项交付事实 |
| A-AC2 | 原invoke真实tools_upgraded且formal_fork_source_lock无缺口；目标实际清单及完整资产来自C，Task/session/user/peer保持 |
| A-AC3 | 目标自身resolver/installed/native、完整bytes/modes/manifest/workflow/lock、合法reapply/drift及零sidecar；不以source验证代替目标 |
| A-AC4 | 原existing入口从真实`.9`到完整组合资产及本批必要 verifier 修复执行完整结果，退役资产/AGENTS hash/平台规则成立；回归实际覆盖 public tools writer 改变 baseline 后的阶段承接，并保留未知内容拒绝。这是原AC7/AC9承诺 |
| A-AC5 | 全部after经原完整质量与actual delivered，原Completion再评整体；不关闭#861或预称发布完成 |

无未决产品选择。实际来源取得、目标冲突及prepare写删集合属后续原owner的执行事实，必须执行前复核；不预填成功。未完成的真实采用或完整existing属于实施责任，不是仅待外部证据。

## 7. Canonical 引用与本轮差额

沿原R724/D724/T724的共享root、selection及用户保留合同，R630/D630/T630的正常文本维护/验证层次，data-contracts current清单合同及MIGRATION-861历史schema边界。Architecture baseline/constitution/change-contract与distribution ARCH-INT-006/014/015承接source与采用分层。本轮必要差额仅为完整 existing verifier 对原 public writer 的阶段前像承接及直接回归；真实安装源C、matching Fork、fixed B与整体 accepted_scope 不因该修复被替换。没有新公共语义，原RDT/Architecture仍在实施后复核真实after；必要变更沿原writer整合/readback，无差额不建空contribution或ADR。
