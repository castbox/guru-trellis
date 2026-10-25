# #669 已有实现分支恢复：Architecture contribution

状态：accepted；来源为 #669 及实际独立 Planning candidate assessment。适用前驱为 Git `83512901506409f59016121aebc2d0b0bbe98059` 的 `docs/architecture/03-domains/ownership.md`（ARCH-DOM-060/shared lifecycle）、`docs/architecture/adr/portable-shared-lifecycle.md`。完整职责定义已整合到 `docs/architecture/03-domains/ownership.md`；实现与后续质量结果按实际证据和原公共结果判断。

## 当前差额和决定

原 Reactivate 的 shared-archive入口要求base HEAD上的clean checkout；#669明确要求既有实现HEAD和已审本地改动的准确接续。选择target_native：在同一个Reactivate owner提供独立闭合profile/schema，原C3 acquisition承接准确既有checkout，public Task writer仍唯一增代，C4/C5/Bind与正式Delivery gates仍归原owners。

新路径分别核准确base、实际实现HEAD、完整已审本地内容、原Draft PR repository/base/head及原资源责任。逻辑内容比较使用index entries而非raw index缓存字节，同时包含worktree/untracked内容、类型和执行位。当前rebind及raw-index snapshot保持原义。所有比较只服务普通版本绑定和stale检测，不是授权或对抗边界。

同操作优先继续实际公共后继，不因receipt缺失重新增代。恢复自身合法写入的Task metadata与原已审核工作区以精确前后状态区分；不整体忽略.trellis，不覆盖未审/冲突内容。旧入口仍服务当前clean-base消费者；独立新增入口不伪装成旧schema扩义。必要交易新版本有直接same-owner恢复consumer，不增加第二状态authority或全链digest。

## 唯一职责与晋升目标

AI读取authority、范围、前驱、PR和实际内容并判断充分性；只读observer提供Git/gh事实，确定性executor执行原公共operation。公开handoff只保留原真实key/ref/route，无快照审查历史或授权。恢复不自动commit/push/create/merge PR、关闭Issue或Cleanup。旧Completion/Closure保持历史身份，不转为当前通过。

拟维护完整单元为 `docs/architecture/03-domains/ownership.md` 的ARCH-DOM-060及其Reactivate段落：保留原shared archive/legacy/Finish/public successor与local-resource约束，并加入准确已有实现状态的独立入口和上述单写边界。该单元完整拟写在实现形成后交独立Phase2和candidate Check；原Architecture owner在final_integration实际写入并核对after。RDT三个completion-closure正文由原RDT owner分别整合，不在Planning提前晋升shared current。

## 原则、GAP和证据界限

当前命中最小必要复杂度、职责内聚及语义完整性：不增加通用allow_dirty、迁移framework或跨owner账本；旧入口、原公共writer及本地ownership保留明确职责。没有新的GAP、宪法例外或需要独立ADR的架构决定；ADR-PORTABLE-SHARED-LIFECYCLE继续承接。

验证按D1 design V1–V6。代表完整安装中的实际AI已读取installed入口，审核真实Git/受控provider事实并调用原公开Reactivate；返回同TaskId的generation1，原内容保留，同操作重试不再增代。安装、恢复和后续质量门禁分别记录在RDT贡献的test.md；该结果不证明真实GitHub、backend #802恢复、业务生产效果或最终Check/Review通过。

## 完整拟写与写前来源

目标 `docs/architecture/03-domains/ownership.md` 的完整拟后正文在 `669-existing-implementation-reactivation/proposed/ownership.md`，固定前驱为 B 的同 target。该拟写只在 ARCH-DOM-060/shared lifecycle 的原 Reactivate 与 Closure 之间加入已接受的新路径条件，原全部其它职责和关系保留。链接按最终 target 位置解释。独立 Phase2/candidate Check 覆盖这个完整拟写；原 Architecture owner 只在 final_integration 核真实 expected-current 后写入。
