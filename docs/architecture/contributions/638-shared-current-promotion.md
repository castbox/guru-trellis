# #638 共享知识身份与最终整合晋升架构贡献

状态：`proposed`，尚未晋升。change_path：`target_native`。TaskId=`638-shared-current-promotion`，generation=0，Delivery=`30c417c5-d86b-40cc-89e9-7068af782aaf`。唯一详细方案为所选Delivery的design.md。本文是本Task贡献，不是共享CURRENT或正式gate结果。

## 适用来源与实际变化

固定before authority：Git `9cec623833b61814f1175f31acde4fa81334cdb0:docs/architecture/`，Architecture `.105`、RDT `.114`、constitution `guru-trellis-design-constitution-v1`、project contract `guru-trellis-architecture-change-contract-v1`。首次独立candidate_assessment实际为architecture_impact/target_native，尚待Wording-current final_plan。

当前runtime要求普通promotion写总入口并产生不同successor，现有质量链要求先实际晋升。本候选将稳定单元identity与Git精确正文快照分开；Task隔离贡献及完整proposed正文先接受原独立Architecture和原Check完整候选检查。随后在同Delivery最终整合边界由两原maintenance owners读取真实命中target，保留全部有效条件，合成并写唯一current，最终Check/commit/完整Review覆盖实际变化。

原Check新增candidate-only入口和candidate_checked输出，不写最终public Check gate。RDT candidate_ready定位已审proposed内容，不称shared authority已更新。Arch5.0/Delivery3.0、RDT命中impact/promotion2.0和Check6.0连同受控consumer迁移，Planning、官方Task/Delivery模型和原最终质量职责保持。旧完整安装固定或成套切换，同key由原owner恢复，不新增长期双读。

公共状态通过原owners承接：implementation首次begin_check进入checking，原Check完成候选判断并合法rework回implementation；原maintenance owners在implementing完成最终写入，implementation以同固定B及实际HEAD/全部after差额重建candidate并begin_check，最终Check在checking校验新content_ref并记录gate进入reviewing。写后旧candidate不能复用；不改官方API或直接写控制态，既有真实覆盖仅供适用性判断。

## Required concerns

| Concern | 适用性与具体承接 |
| --- | --- |
| authority-binding | applicable：上述B和独立候选输出绑定当前Planning；新运行合同与项目条款通过原owner实际评估/晋升，不以新current自证旧约束 |
| constitution-binding | applicable：完整单元/状态/直接consumer清楚；减少全局写入和重复authority；无需队列、锁、全仓hash inventory或审批链 |
| boundary-and-decision | applicable：时机和identity真实改变。必要ADR候选窄替代ADR-030的提前晋升及全局入口successor义务；ADR-028/034仍有效 |
| owner-and-single-writer | applicable：Author只写规划及本Task贡献；Architecture/RDT各自原owner单写shared target，原Check/Review作质量判断，脚本不合成语义 |
| compatibility-and-exit | applicable：当前受控入口直接演进，旧shape只属固定旧安装/历史资产；matching切换后三类在途对象原owner重入，不借旧pass或创建第二current |
| gap-and-deviation | applicable：不声明关闭ARCH-GAP-006/008，不扩并行writer；缺覆盖、来源或不清楚组合影响仍回原owner，不因优化删检查 |
| parallel-scope | applicable：允许本Task canonical和隔离贡献；禁止写其它Task贡献或在初次候选检查前竞争shared current。无关目标推进保留原现状 |
| evidence-and-freshness | applicable：Git commit/locator精确来源，局部target/candidate一致性由原validator验证；实际语义、工程、安装和远端证据分层，不建永久账本 |
| review-and-promotion | applicable：首次完整候选及拟写审查；最终target合成后按#637覆盖全差额和未改消费者；原owner写入读回，再最终Check和独立committed Review，Ready/Finish只接受真实promoted或no_change |

## 正文、关系与历史

本Task实施时形成完整拟写正文，定位于本贡献同名目录及RDT贡献目录的proposed/；尚未形成的正文不声称完成。命中知识维护和生命周期条款，以及Architecture CURRENT/DOMAIN/INTEGRATION/GOV与change-contract。根导航切换为稳定authority identity，仅保留定位、状态和必要关系；真实API/schema版本不被抹去。未命中单元和历史归档不批量改写。

必要ADR候选位于[adr-final-integration.md](./638-shared-current-promotion/adr-final-integration.md)，预定最终identity为ADR-KNOWLEDGE-FINAL-INTEGRATION。原Architecture final_plan决定当前设计/贡献/ADR的适用性，原promotion才写shared authority。RDT完整trace为R638/BEH638→D638/CON638→T638/SCN638；唯一实际结果位于本Task RDT test.md，实施时形成，不复制旧结果。

## 恢复与未验证边界

真实命中target变化先由原owner合成；需求前提推翻回scope/Planning，行为/接口/验证义务变化回原质量owner。部分写入或输出丢失沿同一明确intent恢复，不引入新状态机。没有知识变化时不制造空ADR/贡献/导航。

实现、完整拟写正文、当前final_plan、实际Agent双Task样本、matching installed #636/#637组合、reapply/dogfood、最终Check/Review与交付均尚未验证。既有suite/reapply/source-lock记录只作线索，当前fresh归因。本文不证明软件Release、业务采用、Task Completion、Closure、Finish或Cleanup。

## 实施发现：在途 local-clone receipt

原 tools preview 在写前实际拒绝本 Task 旧安装。正常 installer 将当时 source checkout 的 origin 原样写入 source.repo；该 origin 是本机 #637 clone 路径。路径已删除，但 receipt 的精确旧提交 fd16444370c3eceed68c02dc1fc344114bc2ae7e 在本仓对象和 GitHub 均可读，其 Guru/CLI metadata 与旧安装匹配。原 maintenance consumer 只接受 GitHub transport，因此无法开始本批 R638-06/07 的 tools 切换。没有修改 receipt 或把后续 dirty 状态当首次失败。

拟在原安装维护 owner 内补齐这个正常输入：保留 receipt，不把其中路径当旧源码 authority，也不要求旧本机目录继续存在。由原 caller 显式提供本轮已选完整 Guru source；consumer 从其 Git 对象读取 recorded exact old commit，先核对旧 Guru/CLI metadata，再沿原逐路径 source/preimage 规则恢复缺失 hashes。不可读或不匹配仍在写前停止；不以当前 HEAD 代替旧来源。已有 GitHub transport 保留原义。该修正不增加 public DTO、持久来源记录、Task 转换或兼容 parser，也不改 Task/session/archive。

该差额归原 producer/consumer 的来源判定及其共享直接 callers，详细方案由 Delivery design 的 D638-06 单写。原 caller 的完整 source 提供 receipt exact old object；clean metadata mismatch 或对象缺失写前停止，dirty receipt 仍仅作原逐路径来源。原 GitHub 和 unknown-preimage 语义不扩张。实施与定向验证由 implement I638-06a/T05a 承接，不新增 ADR、公共来源 DTO 或第二维护 owner。本节不表示新规划已激活、修复已实施或安装已成功。
