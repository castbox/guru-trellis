# Codex 公共投影与旧根退出设计

导航别名：`R724/D724/T724`；`Codex Skill共享目录`。原知识状态：`current`（继承上述旧入口的原 current 条目，不表示实现通过）。原语义 owner：`guru-maintain-requirements-design-test-ssot`。这些检索别名继承自 Git `f75f0f5dd078a0c2c4c9a54ac861383774162806:docs/design/current/README.md` 的原 current 条目；该来源定位原晋升状态及所属完整正文，不将知识状态扩大为实现/安装通过。原定义、来源与关系保持。

Identity：RDT-DES-CODEX-DISCOVERY；需求：RDT-REQ-CODEX-DISCOVERY；测试：RDT-TST-CODEX-DISCOVERY。
Architecture：guru-trellis-architecture，ARCH-INT-006、ARCH-DOM-020、ADR-CODEX-SHARED-SKILLS。

## D724-01 / CON724-PROJECT：原 owner 的单一投影

Guru preset owns current 平台 descriptors；pinned upstream identity/cliFlag 不变。Codex root 是 .agents/skills，原 selected_skill_roots 去重；每包 supported_platforms 与目标 exact selection 决定是否进入该根。专属包公共元数据沿既有 allowlist 投影，私有资产保持原安装位置。其它平台原 root 和 Codex 非 Skill 配置不迁移。

## D724-02 / CON724-RETIRE：有界 predecessor retirement

原 installer/maintenance owner 读取具体旧受管记录，先形成完整目标公共集合，再退出符合 previous managed hash 的旧文件。旧根仅用于迁移识别，不继续成为 current inventory 或长期兼容路径。只清理由具体已移除路径派生的空目录，保留用户和第三方内容。

目标 public bytes/mode 不完整或有未解决冲突时，保留对应旧副本并沿原 staged activation/recovery 阻塞成功。两端修改和未知来源文件沿原 provenance conflict/sidecar 处置。既有 files/removals/conflicts/sidecars 与磁盘一致，不新增持久迁移台账或第二 writer。

## D724-03 / CON724-MAINTAIN：目标选择与安装隔离

已有 checkout 的 tools-only 更新从完整目标 source 的 guru-upgrade-tools 进入；完整旧安装仍由 guru-upgrade-installation 承接。目标选择来自目标 manifest/provenance，不从 source selection 推断。保留 Task/session、其它 checkout 和用户修改。普通 full apply 的 current-only 前置不授权无关历史转换。

选择加入 codex 安装专属包；退出 codex 移除其未修改专属受管投影，保留其它平台仍消费的共享包。迁移完成后的 reapply 只维护 current 根。代码维护在原 owner 内作必要机械抽取，保持每个 touched non-generated 文件 <=3000行，不引入新通用框架。

## D724-04：发现证据与能力边界

官方 Codex Skills 合同说明 repo .agents/skills scanner、同名不合并和元数据策略。本项按本 Task 规划选择 CLI0.162.1 为同机制代表，真实 native trace 核发现根和打开的公共包；专属包经显式 dry-run 保留原 native chat/async 工具检查。合法 blocked 只证明当前门禁结果，不声明真实业务编排、桌面 UI 或所有版本已验证。

实施/公开API、投影一致、真实安装、native调用、正式source-lock及发布矩阵分别记录。代码和三层current定义在同一最终Delivery中交付；隔离proposed先经独立Architecture和candidate Check，再由原owners final_integration读前像/写回/读回，随后实际候选重绑和最终质量链。
