# D1 精简 legacy 正式归档恢复设计

## 1. 设计目标、需求承接与内容基线

承接本批 R1–R7、S1–S5、AC1–AC6。development baseline B=main@3a4b65ab08cdfe05d97f68e7f2e7512254d728f1，来源为本次 Sync 的明确 main Git object；Planning H0 相同，PR 目标 main。内容范围为固定 B...最终 H，不把目标后续推进当作内容基线变化。

独立 candidate_assessment 已正式返回 baseline_current/no_architecture_impact。authority 为 guru-trellis-architecture、constitution guru-trellis-design-constitution-v1、change-contract guru-trellis-architecture-change-contract-v1。ARCH-DOM-060 与 ARCH-INT-063 已定义公共格式/增代及 Guru 历史核验的责任；本批只收敛现存消费者，不新增架构机制。该结果不替代 Wording 后 final_plan。

## 2. 当前系统、边界与目标差额

无前序 Delivery。shared_finish.read_shared_archive 以 raw generation 和无人员字段限制 schema1；_successor_at_checkout/find_successor 及 invoke.acquire_incarnation 仅让 schema1 进入公共正式恢复。identity._archived_lifecycle_candidates 比较原始 generation/source，不能处理保留 compact 前驱的已归档后继。

改动这些直接消费者，使用 fixed CLI/Core 公共 family/key/关系判断。schema2 reopen、人工 archive_resume、未完 Finish 路由保留。全局 workflow 顺序和公开输入/typed exit 不改；调用者仍给准确 archived_lifecycle，AI 在原公共 inspection 取得其实际值。

## 3. 来源设计处置（唯一）

| 来源承诺 | 处置与具体落点 | 理由、影响与上游 |
| --- | --- | --- |
| #712“公共家族与身份”：Trellis 拥有格式/generation，Guru 不复制算法 | retain；第4/5节从 locator 公共 inspect，native 关系校验 | 公共 #64/PR#65 已交付；本批不修改上游 |
| #712“原 owner 接线”：历史审核与 acquisition/binding/session 各归原 owner | retain；第4/6节沿现有 operation/control 代码 | 不建第二恢复状态机 |
| #712“来源与历史投影”：规范旧 scope，原档只读，不增加关闭权限 | retain；第5节原 task_source 提供语义来源，公共 projection 校验关系 | 实际样本原形保留，scope owner 继续整体范围 |
| #712“完成边界”：applied、本地控制、native/下一 scope 消费及再次归档读取分别验证 | retain；第8节 V1–V5 | 避免 producer 成功替代 consumer 可用性 |
| #712“工具与分发”：原工具 owner 采用固定 source/build/API | retain；第7节 matching tools 与 dogfood 同步 | local_candidate 只作隔离证明，正式 source_locked 限界保留 |

## 4. 模块、职责与设计取舍

shared_finish 接收 source_ref（原语义输入），从精确已核 Git archive 对应的工作树 locator 调用 inspectTaskTarget，取得 public classification/key；核其与显式 key 一致，并按公共 capability 确认正式支持的家族。schema2 继续公共 schema2 parser。对原档不在工作树、bytes 与精确 Git 版本不一致的情况保持具体缺口，不从别的版本分类。

Guru 历史准入仍核 summary2、generator/path/status、原活动移除、准确 introducing merged PR 与目标可达性；AI 另读原安装合同、PRD 范围和历史，脚本不判充分性。known_legacy 和 schema1 都进入原 formal_inspection/prepare/apply/recover；public inspection 不承担正式资格审查。

identity 的保留前驱消歧复用目标安装公开 native task_utils 的 TaskId 唯一性/前驱关系读取，通过现有 installed-module loader；保留 Guru 所需精确 Git/retained bytes 关系核验。仅在正式 provenance 分支消费，不放宽普通 current parser。避免直接调用下划线 helper、复制 legacy 判断或从缺字段补0。若公共入口无法提供所需关系，回公共 owner，而非新增 Guru parser。

原 tests 扩展 compact fixture；native setup helper 只造合法客观前史/provider/seeds，不生成 semantic pass。RDT、工具采用和安装同步仍分别由原 owners 执行。

## 5. 接口与数据

不改变公开 Reactivate profile/DTO/exit。内部 shared reader 可新增可选 source 参数，现存 schema2 caller 不受影响；正式旧家族必须提供 matching source。

公共 inspectTaskTarget 输入 root/task_ref/original_task_ref，不要求先给旧档补 key；结果 classification/key 用于准确比对。formal archive inspection 继续转发原 key、精确 commit/target、summary AuthorityRef；prepare projection 为公共 Task2，保留 id/source/历史 scope，generation 由 public 校验严格+1。

旧 scope 来源由现有 task_source 解释；projection source 不得升级关闭权限，public source relation 必须验证。creator/assignee 不投影到当前 Task2，旧原字节保留在原档及公共 source snapshot。无新增持久状态；原 operation checkpoint 只供原恢复 consumer。

## 6. 状态、顺序、正常与失败流程

1. AI 核历史资格和当前 scope；选择准确 source、前驱 key/anchor 和 acquisition。
2. 读取共享 Git/PR 事实及公共家族/key；发现真实后继优先，核关系/阶段。
3. 无后继时原 acquisition 获得目标；目标 native 采用校验通过后 prepare 一次 formal operation。
4. pending 保留原 transaction，recover/resume 同 plan；不输出 active key。
5. applied 真实 key/ref 后原 C4/C5 建控制，原 Bind/continuation 接手。绑定中断继续原 transaction。
6. 丢失 private result 先核真实后继，不重复 prepare；已归档后继进入其实际 archive/Continuation owner。

source、Git、PR、capability、目标采用或后继关系失配给原具体诊断，保留现场。已核共享终态不依赖原机 seal/Cleanup；不取得别的 clone 资源权限。

## 7. 恢复、兼容、迁移与集成

保持 transaction2/3、旧 profiles 与 existing implementation 的独立语义。新增正式 family 进入原 operation 恢复，不能用人工保代恢复替代增代。当前严格 Task2 reader 不双读任意旧档。

固定两包 source=619133c62d1487c5fbecbf9e00cea9e3f5ea52a6，release issue-64-candidate-619133c62d14；同名 .6 必须校验实际 pair digest。目标 native 模板来自该 pair，Guru 更新由 guru-upgrade-tools 完整源执行，不覆盖 Task/session。dogfood 也用该 owner 同步 managed assets。隔离 local_candidate 明确 formal_fork_source_lock 未验证；不修改正式 source lock 或发布。

需要一个代表性完整隔离安装，随后原工具 owner 更新目标并核 native；不跑多平台累计矩阵。不操作来源业务仓库。

## 8. 验证设计

| ID | 入口与输入 | 独立可观察结果及限界 |
| --- | --- | --- |
| V1/AC1 | formal archive tests + actual matching SDK，原样十字段/source scope/人员字段、真实 Git 和受控 PR | public known_legacy/key，Guru 准入，实际+1且原档 bytes 不变；不能先转换旧 fixture |
| V2/AC2/3 | 同测试的 pending、applied后控制中断、丢失结果/真实后继 | 同 operation/后继，不重复 prepare/generation/resources；只证明确定性本地集成 |
| V3/AC3/4 | 后继合法再次归档代表状态，native TS/Python identity 与 Guru/Reactivate；原 schema1/schema2/人工/未完定向回归 | 保留 compact 前驱不碰撞；source/历史普通不一致准确停止。再次归档 reader fixture 不声称完整第二生命周期 |
| V4/AC5 | 一个完整安装目标，实际 AI 读历史合同/PRD/provider，调用 installed Reactivate→Identity→Ensure/Bind→get_context continuation→原 scope owner | 分别记录 applied、控制、native 续接与 scope 实际消费；无空 Delivery；受控 provider 不证明真实 GitHub/业务生产 |
| V5/AC6 | package/runtime targeted、syntax、schema、dogfood reapply/drift、platform projections、sidecar/diff check | 真实源/安装一致；完整 Release/多平台 upgrade matrix 明确未覆盖 |

已有正式 recovery 测试继续证明仍适用路径，新增断言针对 compact 必经失败点与 consumer。由原问题输入/代码因果分析加 post-change 观察判修复，不惯例重复回退。必要行为证据充分后停止扩展；设施失败先定位其层，不冒充产品失败或通过。

## 9. Canonical 引用、本轮差额与实际未决项

RDT completion-closure 三层完整单元由原 guru-maintain-requirements-design-test-ssot 准备 delta、在最终 Phase2 前整合，限定 family 和消费者变化。原 Skill/README 同步 formal 家族说明。Architecture 当前无需 contribution/ADR/shared 写；实际发现机制/owner 扩大时重入原 assessment。当前无必要未决范围问题，public capability 或 native 缺口阻塞其真实验收。
