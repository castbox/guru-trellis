# Codex Skill 分发与迁移验证

Identity：RDT-TST-CODEX-DISCOVERY；关系：RDT-REQ-CODEX-DISCOVERY → RDT-DES-CODEX-DISCOVERY。
以下定义验收策略，执行结果由原 Task/D1 validation 及正式公共结果/Git事实提供。

| 验证 | 需求/设计 | 入口、输入和可观察结果 |
| --- | --- | --- |
| T724-01 / SC724-INSTALL | R724-01/02/06 → D724-01 | 一个代表性Codex clean安装；公共集合、内容、mode、专属包元数据正确，无旧受管根/私有资产。non-codex和含codex多平台用定向测试核适用性和去重。 |
| T724-02 / SC724-UPGRADE | R724-03/04 → D724-02/03 | 合法旧source/provenance经正式维护入口；目标完整后才移除未修改旧文件，manifest及removals匹配磁盘。 |
| T724-03 / SC724-CONFLICT | R724-04 → D724-02 | 旧/新两端用户修改及未知文件保留；目标冲突时旧副本仍在；原冲突处置和恢复后正常重试，不以双投影或未解决sidecar报成功。 |
| T724-04 / SC724-SELECTION | R724-02/06 → D724-01/03 | 增加和移除codex的实际installer路径；专属包安装/退出，共享包、其它平台副本、用户文件及其它.codex职责保留，manifest/conflicts/removals一致。 |
| T724-05 / SC724-NATIVE | R724-05 → D724-04 | 真实CLI0.162.1在目标无旧Skill副本时按名称发现并实际调用公共包和专属包；trace定位共享投影，原公开入口和前置产生合法出口，保留真实宿主/版本/结果。 |

同clean样本继续reapply并核不恢复退役根；canonical/dogfood/installed、声明平台、ownership/drift、mode和递归sidecar定向检查保留。真实来源必须由原合法producer形成，不能手改manifest/hash伪造迁移前态。原installer机械抽取须保原行为，不能用常量或文件存在自证功能。

原生能力不足的专属dry-run出口与真实业务编排成功分开；源码扫描、模型预加载package、本聊天清单均非native发现证据。只有本项义务都完成才允许整体完成，知识晋升或合并不能代替。

完整多平台Throwaway/Release矩阵、其它客户端UI、正式source-lock、业务采用和生产效果按实际未验证边界报告，不从定向检查推断。实际证据定位为 TaskId724-codex-shared-skills/gen0、DeliveryIda831ddba-681c-480a-9eb9-1e350f48a43d 的 validation；活动或归档位置由原Task身份解析。
