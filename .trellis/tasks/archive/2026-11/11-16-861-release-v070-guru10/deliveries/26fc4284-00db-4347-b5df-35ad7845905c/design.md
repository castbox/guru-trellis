# D2：准备 checkout 的正式工具采用设计

## 1. 设计目标、需求承接与内容基线

本批承接 [PRD](prd.md) D2-R1～R5、SC1～SC4、AC1～AC4。整体范围见 [Task PRD](../../prd.md)，本批 scope_ref 为 R3、R4、R5、AC2、AC3、AC4。目标是交付真实工具安装 after，不再次交付 D1 canonical 源。

开发基线 B 为 `b3525d4b052f79f7d9cb4a18f827ff7c990f1983`：它是当前 HEAD 的唯一最近实际前序 delivered head，来自 D1 `delivery:dc300d26ed638d97a303753958f85eaa645f2067`，不是先前 Task 起点 `f52...`。Planning H0 同为 B；最终 H 由安装、工程、知识及原 TaskCommit 形成。PR 目标仍为 main；原 constructor 优先恢复该前序基线，纳入全部真实 installed 差额，不重复 D1。后续 main 推进本身不改 B，实际集成走原 owner。

独立 Architecture candidate_assessment 实际返回 `baseline_current/no_architecture_impact`，baseline `guru-trellis-architecture`、constitution `guru-trellis-design-constitution-v1/current`。方案复用 ARCH-INT-006/014/015 的既有责任，没有新 owner/状态/迁移机制；本 design 完成后仍需独立 final_plan 和原 Approval。

## 2. 当前系统、边界与目标差额

原 tools preview 使用完整 canonical D1 source 执行，source_locked 配对检查成功；实际安装尚未执行。目标仍为 `.9`，source provenance 为 `9697e04d66cf5958f507f340116b4aa3b6ab2f39 / dirty`。其历史身份保持，不回写成 `.10`。

实际 manifest 选择 Claude/Codex/Cursor；public Core 对应 `claude-code/codex/cursor`，Guru 选择是 `claude/codex/cursor`。preview 读取了 9,992 个旧受管路径及 832 项 peer/runtime 观察；没有旧受管本地编辑或现存 Guru sidecar。目标 gitdir 的原 tools-upgrade 事务目录没有待处理 operation。执行前仍复核相交公共维护事务和 live 状态，不把本次观察当永远有效。

本轮明确差额为升级 owner 的私有 runtime、shared consumer、schema/example，以及三发现根的对应 public schema/example/consumer。manifest 由 installer 生成 `.10`，source commit/ref 指向 immutable D1 H，canonical `trellis/**` 保持干净。原 source_provenance 用整个 worktree 的 Git status 记录 tree_state；Task 规划或 installed after 使其为 dirty 时如实保留，不能伪写 clean，也不要求为此另建来源或提交。workflow 和大部分工具已匹配，仍由完整原安装过程维护，不能只复制差额。`.trellis/config.yaml` 被 public inspection 标为非 required conflict：保留当前 `task_auto_commit:false`、channel 与 Codex 配置；`.trellis/guru-team/config.yml` 是目标配置，虽与 raw template 不同，由原 owner 作为非受管用户配置自动保留，不写 guru_decisions，也不以 raw template hash 要求覆盖。AGENTS 保留用户正文，原 renderer 只更新 Guru block。

## 3. 来源设计处置（唯一）

| 来源与原承诺 | 处置 | 本批落点、理由与影响 | 上游处置 |
| --- | --- | --- | --- |
| release / Complete Source Before Actual Adoption：D1 完整源 delivered 后才建 D2 | retain | §1/2；真实 D1 公共结果已成立，D2 使用其 H 和 clean canonical，不用样本/未交付提交 | 原 Completion/Creation 已执行 |
| 同节：D2 独立 Planning/Activation、source_locked、全部 installed after 完整交付 | retain | §4/6/8；本目标真实采用，不能把原 .9 观察当通过 | 原 tools、TaskCommit、Review、readiness/Publish/Merge |
| tools / Forward behavior：匹配 CLI/Core、目标 exact selection、custom workflow、AGENTS custom renderer、prepare 一次 | retain | §4/5；复用原 API1.0 和安装器；不新增脚本/替代 renderer | 无偏离 |
| tools / Gate、Execution：Task/session/user/peer/common 保留、未知修改/sidecar 阻塞 | retain | §2/6/7；public config 显式 preserve、Guru 用户配置原生保留、单目标写集与原 preimages 校验 | 原 tools owner |
| tools / Same-operation resume/rollback：原 ref、plan/preimages 不刷新 | retain | §7；部分失败续同 operation，回退另审，不 reset Git | 原 recovery owner |
| release / Whole Preparation Completion、Stage2、Independent Mutation Confirmations | retain | §6/7；本批 Refs-only；不执行 Finish/正式发布/主目录安装/close | 原后继 owners；当前不执行 |
| R724/D724：共享发现根、目标选择、旧受管退出和证据分层 | retain | §4/8；公共 Codex 根为 .agents；完整集合/字节/mode 与实际入口分别验证 | 不改变该能力或重写其历史结果 |

没有来源设计偏离或要求上游另作产品选择。PRD/implement 只引用此矩阵。

## 4. 模块、职责与设计取舍

唯一 source 与 target 均为本 Task checkout；source HEAD 固定 B，`trellis/**` clean，Task 规划/runtime dirty 合法且不进入 canonical token。原 tools launcher 从 `trellis/skills/guru-team/packages/guru-upgrade-tools/` 执行，绝不借旧 target dispatcher 安装。固定 Fork 为 `/Users/wumengye/Documents/GoProjects/Trellis@e3793251fad8bd261d0c370d408c7675b9f6a140`，复用其现成 clean、匹配 build；CLI/Core 都是 `.6`。原 transport 验真实包 bytes/mode 和 lock/build，不复制 dist 或改全局包。

原 public maintenance 拥有上游工具、AGENTS 和 workflow 的最终写入；workflow 选择 install，template `guru-team`，provider `gh:castbox/guru-trellis/trellis#b3525d4b052f79f7d9cb4a18f827ff7c990f1983`，ownership custom，content 是完整 canonical workflow。AGENTS 必须恰好一个 action=custom，source 为原 inspection snapshot，content 为目标原全文，由原纯 renderer 合成。public `.trellis/config.yaml` 冲突 action=preserve；原 skip/required 规则保持。

Guru 原 installer 拥有 `.trellis/guru-team/**`、managed specs、shared/Claude/Cursor Skills、平台 overlays、manifest 和目标 checkout-local Python pointer。原 `guru_owned` 明确排除 `.trellis/guru-team/config.yml`：它不在退休集合和 guru_decisions 允许集合内，原 installer 在其已存在时保持不写。当前无受管本地编辑，因此 guru_decisions 为空；其它已知未改受管路径用原 previous hashes 更新，不做逐文件手工覆盖。832 项 peer/runtime 观察只由原 tools consumer 冻结和校验，不写 Task 文档或公共输出。

直接原 tools 更新是最小已有路径。普通 full apply 会触及历史 Task preflight，完整 installation conversion 改变业务资料，手抄文件缺维护 provenance；这三条都不满足当前单目标保留合同。成本是原 preview/prepare 对完整资产和 peers 的检查，不为降低成本削减原门禁或新增增量安装器。

## 5. 接口与数据

没有新增公共字段或生命周期。本次沿原 `install` 输入：source_ref=B、dependency_mode=source_locked、checkout=当前绝对目标。source descriptor 指向 Fork `packages/cli` 和实际配对 Core，携带真实 package identities、Guru/Fork source roots；只供本 tools operation，不进入 planning DTO。

原 preview 的 intermediate receipt `result` 是 inventory。原 prepare 消费 private-prepare，返回 `result.plan`，其中 public upstream operation/plan 不修改；原 invoke 消费该 frozen plan。`tools_upgraded` 只证明目标工具状态，`resume_required` 返回同 owner，`blocked` 停止；不会直接写 Delivery Check、Completion 或升级 Task schema。

文件主要落在既有 `.trellis/guru-team/`、`.trellis/spec/`、`.agents/skills/`、`.claude/skills/`、`.cursor/skills/` 和对应平台入口；实际增删由 prepare 的完整固定集合决定。保护范围为 Task/archive/workspace/session/public facts、用户正文和配置、其它 checkout、common runtime。允许原 owner 的 Git-private恢复状态及目标自身 runtime pointer；不新增 ledger、授权字段或 tracked status。

## 6. 状态、顺序、正常与失败流程

1. Author plan_ready → 独立 final_plan → Approval；展示完整本计划，停在 workflow 接受/Activation 边界。当前不 prepare、不安装。
2. 接受并 Activation 后，原 tools owner 复核 D1 result/source/Fork/build、目标状态、事务和保存项；刷新只读 preview。真实新增冲突先审查，不默认覆盖。
3. 按 §4 构造 private-prepare，调用 prepare 一次；消费完整 frozen plan，核 AGENTS renderer 幂等、配置 preserve、平台、workflow/provider、全部 writes/deletions 及隔离。显示精确目标/source/命令/写删集合后，停在独立安装确认边界。
4. 安装确认后，原 invoke 执行 public maintenance → Guru assets/manifest → target validation/preservation。部分失败从真实 recovery_ref 续接，不新 prepare。
5. 实施 owner 验真实 after、原 reapply/drift、目标 native 和保存项。原 RDT/Architecture 处理真实知识差额，原 TaskCommit 后 constructor/begin_check 固定完整 B..H，新独立 reviewer 同次完成 Architecture/Check/full Review，随后 readiness/Publish/Merge 各守边界。

source/API/lock 不符、未完相交事务、未知修改、sidecar、验证失败停在原 tools/实施 owner；真实 authority/机制变化回 Clarify/Author/Architecture。preview 或安装返回值不替代任何语义审核。

## 7. 恢复、兼容、迁移与集成

不转换历史 Task/schema，也不热改在途操作 provider。本批尚无 frozen operation；prepare 只在 Activation 后对最终确定输入调用一次。install 输出丢失时，原 tools owner 使用相同 ref/plan/source 和真实 phase 恢复；业务 metadata 后续变化不能被重新吸入 rollback anchors。rollback 仅原兼容检查通过后按同 preimages，另行审查其实际副作用。

reapply 由同 tools owner 在原 installer 的 `tools_only=true` 模式，消费该 operation 的同一 public source/plan/recovery_ref；不重新 prepare，也不使用普通 apply 绕开历史 Task guard。若公开能力不足以合法完成所需再应用，保留该验证缺口并回原 owner，不伪称 reapply pass。

D1 旧观察和原失败保持历史含义；本批实测 after 支持当前采用。D2 实际 delivered 后原 Completion 才重评全体范围；Closure no_mutation、Finish 和 Stage2 最新 main 各有后继责任，不由本批安装或合并隐含完成。

## 8. 验证设计

| 验证 | 要求/验收 | 原入口与独立观察 | 边界 |
| --- | --- | --- | --- |
| V1 来源/计划 | R1/R2，AC1 | 原 source_locked preview/prepare；实际 H/canonical status、Fork lock/build/API、target exact selection、AGENTS/workflow/config 与完整 plan | 只读 preview 不证明安装 |
| V2 原安装 | R2/R3，AC2 | 原 invoke 真实 tools_upgraded、unverified=[]；实际 manifest/source revision `.10`、CLI/lock 和 public tools postvalidation | 不从 exit0 替代目标内容 |
| V3 目标可用 | R4，AC3 | target own resolver、installed validator、get_context continuation 和原公开 Identity/Ensure 入口；同 Task/gen/D2 原状态仍可接续 | 脚本/native 观察不宣称客户端真实 Agent/生产效果 |
| V4 完整资产 | R2/R4，AC3 | 原 managed_source_projections 完整 expected 集与目标 bytes/mode、manifest 库存，声明三 roots；workflow/lock/source、ownership/drift、同 operation tools-only reapply、零未解决 sidecar | config 按原保留/renderer，非所有 raw template 等同；不扩 Release 矩阵 |
| V5 保留 | R3，AC3 | 原 public/Guru before/after 与 actual peer/common 校验；安装区间 Task/session/user bytes 及原 D2 key/planning accepted 读回 | 基线在安装前由原 owner 冻结，不从规划阶段长期缓存 |
| V6 独立交付 | R5，AC4 | 原 TaskCommit、完整 B..H Review 两槽、readiness、Refs-only Publish/Merge | 不能替代整体 Completion/Stage2 |

已有 D1 source/package/三平台样本结果对未变 canonical 的适用范围保持，不重复同源码全套测试。V1～V5 必须在本真实目标执行；不新增长期测试、固定版本字面断言或 installer副本。实际覆盖足够即停止追加实验；发现原入口/API或设施缺口，保留其证据并返回原 owner。

## 9. Canonical 引用、本轮差额与实际未决项

R724/D724/T724 的完整 `docs/{requirements,design,test}/current/codex-skill-distribution.md` 保持共享根、选择、保留与证据职责；本轮不更改这些规则。Architecture authority/constitution/change-contract 与 ARCH-INT-006/014/015 及当前原 tools 合同承接采用路径。无新增机制/authority/compatibility，故不计划共享知识写入；真正出现规范差额时先回 Author 更新唯一 Docs Plan，再由原 RDT/Architecture owners 整合/readback。

没有未决产品问题。真实安装写删集合、公共维护事务及 current per-path 决策在 Activation 后原 prepare 门禁固定；当前只读 preview 不是未来写集的批准或安装通过。
