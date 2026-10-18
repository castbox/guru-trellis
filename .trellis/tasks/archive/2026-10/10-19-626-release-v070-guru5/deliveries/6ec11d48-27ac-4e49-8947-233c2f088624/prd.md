# D1 v0.7.0-guru.5 及内部版本准备需求

## 1. 整体来源与术语

整体 accepted_scope 为 Task 根 prd.md 的实际 sha256 AuthorityRef，由公共 Task 记录持有。本批 scope_ref 包含 AC1–AC6；planning_root 为 deliveries/6ec11d48-27ac-4e49-8947-233c2f088624。

| 来源 | 角色与用途 |
| --- | --- |
| https://github.com/castbox/guru-trellis/issues/626 / 版本与来源、准备与发布行为 | 当前要求；本批只承接 Stage1 |
| .agents/skills/release-guru-trellis-version/references/contract.md / Two-Stage Lifecycle | 约定设计；晋升前后审查、Refs-only 与独立 Stage2 |
| Task 根 prd.md 第5–7节 | 当前整体要求与 AC；本批全量覆盖 |
| docs/{requirements,design,test}/README.md、docs/architecture/README.md | 当前知识及架构 identity 与完整正文导航 |

软件 tag、extension、Fork、内部知识版本独立。历史身份不因新的 current 版本而改写。

## 2. 整体与本批目标、非目标

本批是准备 Task 的完整单一 Delivery。完成 extension/maintenance .5、公开版本说明、内部 RDT .7.0-guru.111 / Architecture .7.0-guru.102 后继和投影、定向验证。当前 .4 manifest、旧 README 与旧内部前缀是起点。排除 Stage2 exact-candidate/tag/smoke/Release/Issue closure；排除其它 Open Issue、Fork 修改、真实业务升级和生产部署。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，无前序 Delivery。起点 main 为 33f18a768c9c8d901f34b899934ac40c3d97cc5b。匹配 Fork lock 7bcbeaad31380e7a29c97898cb947c6120a61775、CLI-Core 0.7.0-castbox.4 不变。原 Architecture/RDT owners 管理后继及适用晋升。Delivery 合并后 Task 仍需整体 Completion、reference-only Closure 与 Finish；发布 Issue 仍需 Stage2，不能因本批交付关闭。

## 4. 本批调用方、场景与流程

- DS1：发布准备 caller 读取 .4/tag 与 main，更新 .5 的 canonical 版本及维护 consumer。安装/升级入口读取一致目标；错误版本或 stale 来源仍由原 owner 拒绝。
- DS2：知识 reader 从 RDT/Architecture README 进入 .7.0 后继，读取相同完整单元；旧 task 使用原 immutable 版本/Git，不跟随新 current 解释旧身份。
- DS3：Check/Review/Delivery owners 检查准备内容、投影和边界；完成 Refs-only PR 合并。Completion 与 Finish 后把源代码和终态归档交给 release caller，后者重新验证 exact candidate。

## 5. 完整行为、条件与约束

- DR1（R1/DS1）：extension 与 maintenance target 均为 0.7.0-guru.5，repository 目标 v0.7.0-guru.5；真实前驱为 v0.7.0-guru.4。维护 runtime、output const/schema/consumer、示例及其定向测试同步目标；Fork source/CLI/Core/package-manager 不变。
- DR2（R2/DS1）：三 README 和 public-docs 区分 .4 已发布、.5 准备、历史 .3；准备时稳定安装仍使用真实 .4，试用只允许真实远端完整 candidate SHA。不以版本号相同替代匹配 Fork source/build。
- DR3（R3/DS2）：RDT current-main-0.6.17-guru.110 → current-main-0.7.0-guru.111；Architecture current-main-0.6.17-guru.101 → current-main-0.7.0-guru.102。新旧关系、三层导航/版本页、完整 current 单元与必要引用一致；旧快照、归档和未迁移范围保留。
- DR4（R4/R5/DS1–3）：canonical 修改后通过 apply 生成 dogfood 与声明平台；定向 source/installed/parity/ownership/drift/tests 及 residue/diff hygiene 验证。FAIL/SKIP 不视为通过；实质范围变化回原 owner。
- DR5（R6/DS3）：source reference_only，PR 只 Refs #626。原语义审查与晋升顺序见本批 design 第3节唯一处置。无授权记录、动态 release checklist、task-local release notes 或 body handoff。

## 6. 本批验收、验证方式与未决项

- DAC1：对 manifest/source lock、maintenance runtime/schema/consumer 执行目标版本定向测试，观察全部 .5 与 unchanged Fork .4 对齐（AC1）。
- DAC2：全文审核三 README/public-docs，核对 live .4 stable、.5 candidate、历史来源/验证边界（AC2）。
- DAC3：通过原知识 owners 核对新旧 authority、三层关系/链接和 current 完整单元，观察 .111/.102 及正确前驱（AC3）。
- DAC4：运行 source/installed validators、Shared/Codex/Claude/Cursor parity、ownership/apply/reapply/dogfood drift 和变更定向 tests，观察无未解决 sidecar/bytecode/意外 dirty（AC4）。
- DAC5：原 owners 完成完整 Check、提交、独立 review 与 Refs-only Delivery；Task 整体审查/Finish 正常，#626 OPEN。后续 caller 获得 fresh main 的准备内容与归档，不继承最终 release pass（AC5/AC6）。

本 requirements 阶段没有必要未决产品或范围问题。技术方案待独立 candidate_assessment 后由 Author 写 design/implement，不能提前当作完成。

## 7. Canonical 引用与本轮差额

RDT requirement/design/test 的 current knowledge-maintenance 单元和 Architecture FOUNDATION/ARCH-GOV-001..012 是必要依据。版本后继只承接本批映射和新文档边界，不改原 Task/Delivery 或知识行为。public API 的完整规格继续归 canonical packages；本轮只调整 maintenance target 发行 const。历史未迁移范围按 .110 当前入口保留原完整来源。对知识版本/导航的具体写入由原 owners 在适用晋升阶段处理，Planning 不直接编辑共享入口。
