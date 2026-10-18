# #331 当前有效知识迁移

## 1. 采用边界与唯一维护方

本迁移把按历史增量拼接的日常查询，收敛为按能力或职责读取完整当前单元。
RDT 和 Architecture 仍分别由原 `guru-maintain-requirements-design-test-ssot`
与 `guru-maintain-architecture-baseline` 维护。共享读写规则唯一位于 RDT package
的 [current-knowledge.md](../../skills/guru-team/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md)。
Architecture 在完整安装中读取同一文件。公共 Skill id、profiles、输入、schema、
typed exits 和 runtime 不变；本迁移不创建知识服务、解析器或新审批步骤。

本仓库的实际采用入口为 `docs/{requirements,design,test}/README.md` 与
`docs/architecture/README.md`。各 README 指定适用版本与正文位置；软件版本号
不能替代知识版本。其他仓库必须由原维护方选择自己的真实来源和迁移范围，
不能将本仓库的三组单元、版本或栈选择直接复制成业务 authority。

## 2. 本仓库来源与迁移清单

迁移前内容基线为 Git `bdb5185c673c91b2fb5cfc66ffbb33849904a69c`，RDT
`current-main-0.6.17-guru.109`，Architecture `current-main-0.6.17-guru.100`。
切换目标为经原 owner 审查晋升的 RDT `.110` 与 Architecture `.101`。
这些是知识身份，不是软件发布或业务安装结果。是否生效须读取实际共享入口，
不能仅凭本迁移文件或候选目录判断。

| 迁移对象 | 旧完整来源边界 | 新正文与必要关系入口 |
| --- | --- | --- |
| Task/Delivery 生命周期 | 三层 `.109` 版本页指向的前驱与 reviewed contributions，含 Task/Delivery 生命周期后继 | 三层 `current/task-delivery-lifecycle.md`，由各 `current/README.md` 定位稳定身份及关系 |
| Completion/Closure/Finish | 同一适用三层 authority 中整体完成、源处置和归档的现行定义 | 三层 `current/completion-closure.md`，保留整体 Task 与切片结果的区别 |
| 知识维护 | 同一三层 authority 中 RDT/Architecture 贡献、晋升、适用性及本轮差额 | 三层 `current/knowledge-maintenance.md`，本轮贡献在 `docs/requirements-design-test-contributions/331-current-effective-knowledge/` |
| Architecture 晋升治理 | `.100` 对应的 `06-governance/rules.md`、`change-contract.md` 及 ADR-028/030；旧措辞仅在后继替代范围内退出 | 原 governance 正文位置，保留 ARCH-GOV 身份及仍有效条件；ADR/Git 承载历史原因 |
| 通用技术栈与项目选择 | 由原 Architecture owner 审查的真实通用源与项目差异 | `trellis/knowledge/technology-baselines/trellis-extension/versions/1.0/baseline.md` 与 `docs/architecture/00-foundation/stack-selection.md` |

逐条 predecessor locator、stable identity、后继和 R/D/T 关系由实际单元、导航及
本轮 contribution 的 `traceability.md` 承载；上表不另写一份业务摘要。单元的
来源说明须足以核对全部仍有效条件，不能只引用旧版本号声称内容已完整吸收。

这不是全历史语料迁移。除上表已核对单元外，其他能力仍按各层导航中的 legacy
范围读取 `.109` 及其原完整来源。未迁移条目必须说明该范围与拼接边界，不能
因为 README 可打开便标为已迁移。本次不改写旧 `versions/`、历史贡献或归档。

## 3. 切换、修订和恢复

原 owners 先读取固定前驱和完整候选，再核对条件、否定、例外、顺序、替代范围、
必要关系、稳定 ID 及实际验证。新单元必须提供本能力的完整定义；接口规格保留其
原唯一正文，不将目录或摘要当作完整知识。正常查询从适用导航进入这些正文，
只有解释历史原因、旧版本或未迁移范围时才展开历史。

并行 Task 继续各写隔离贡献。原 promotion owner 读取 live target、核对
expected-current，并把实际 delta 合入完整当前定义；其他已晋升变化不得丢失。
结构调整保留存续身份，新增含义分配新身份，删除/替换/拆分/合并保留前驱后继。
历史贡献成为来源，不再充当已迁移单元的日常拼接链。

Architecture 由独立 Phase 2 先审完整候选及 proposed targets。原 owner 晋升并核对
实际写入适用性后，最终 Check、Task Commit、独立 committed full-diff Review
覆盖实际结果。共享入口只能在原维护门禁满足后切换。晋升不代表后续交付、整体
Completion 或 Release 通过。

缺必要来源、断链、冲突或迁移未完成时，说明受影响对象和不能支持的结论，
进入原 repair/Clarify/blocked 路由。切换前保留旧入口，候选保持 proposed；不要
用推断补成 current。切换后的普通纠错走原 repair 或受审 successor，不覆盖固定
旧快照。实际 promotion 的 partial/output-loss 恢复继续使用原 owner 合同。

## 4. 旧 Task 使用方与退出

真实旧读 consumer 是仍绑定旧 RDT/Architecture 版本的在途 planning、candidate
及 gate。它们继续使用相应 immutable version 或上述 Git authority；无关共享
CURRENT 推进不使其失效，不强制重写贡献或重做业务门禁。真实需求、依赖、方案
变化或明确适用规则变化仍回原判断和修订路径。

兼容范围只有旧知识读取。新变化写新 current，不同时维护两套 current 正文。
旧普通读取在该 Task Finish、合法 Reactivate 后重新选版，或原 owner 因真实
依赖变化改选适用版本时退出。原维护 owner 负责该适用性判断及去除失去 consumer
的旧日常入口；历史版本/Git 继续保留以供追溯。这不是永久双写或新 runtime
legacy reader，也不改变已存在的旧完整安装适用边界。

## 5. 完整安装与 matching update/reapply

公共共享正文通过现有递归 package 分发进入
`.trellis/guru-team/skills/packages/guru-maintain-requirements-design-test-ssot/references/current-knowledge.md`。
公共 managed spec 是 `spec/workflow/requirements-design-test-ssot.md`，由原
MANAGED_SPEC_PATHS 安装到同名 `.trellis/spec/workflow/` 路径。项目内
`.trellis/spec/docs/requirements-design-test-ssot.md`、
`.trellis/spec/architecture/baseline-usage.md` 和
`.trellis/spec/workflow/architecture-baseline.md` 是项目投影，由项目原 owner
按实际 authority 更新；本迁移不为它们新增公共模板或 installer 路径。

采用者须先读取目标 matching source 的安装合同。workflow marketplace 与完整
preset 使用同一真实版本/ref，不能只复制一个新 Skill。已有安装在 Trellis
update/upgrade 后，按官方 marketplace `--create-new` 预览 `.trellis/workflow.md.new`，
核对当前文件、用户修改与来源，再从同一 provider 显式 `--force` 应用 workflow。
然后从该匹配源码执行：

```bash
bash trellis/presets/guru-team/scripts/bash/apply.sh --repo <target>
```

保留用户内容，按原 managed hashes 和冲突规则逐个处理 `.new`/`.bak`；未解决的
sidecar 不算成功。reapply 后核对真实 installed package 正文、两 Skills 引用、
workflow、所选平台投影和 managed spec，再验证重复 reapply 与 drift。源码仓库
dogfood 使用 `check-dogfood-overlay-drift.sh`；它不替代业务 target 的实际安装
validator。public discovery、source/installed closure 与正文可读分别检查。

reapply 不选择 Task/Delivery、不晋升知识，也不自动迁移其他业务文档。包和投影
一致只证明分发。真实 Agent 正确读写、同问题多次 old/new 成本对照、迁移完整性、
一个代表性 clean/update/reapply 和未覆盖项由本轮唯一 Test 记录。完整多平台
Upgrade/Release 矩阵与生产业务采用仍归其专门 owner，不从本迁移推定通过。
