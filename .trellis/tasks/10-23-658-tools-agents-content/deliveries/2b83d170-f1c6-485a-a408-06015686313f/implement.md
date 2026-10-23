# D1：AGENTS 维护实施与验证计划

## 1. 输入与引用

读取整体../../prd.md、本批prd.md及design.md第3节唯一处置。实现依据为#658、Fork#57、原tools owner与preset renderer合同；.trellis/spec/preset/installer.md、upstream-ownership.md、workflow/quality-guidelines.md和clear-technical-writing.md定义写集、分发、验证与写作边界。无前序Delivery。

## 2. 有依赖顺序的步骤与文件责任

1. Fork原owner交付#57的新源码与CI；协调#656来源约束。原发布制品不变。
2. Guru实现子Agent只修改tools_owner.py、对应tests、canonical Skill/references及必要安装说明：显式custom输入在prepare前合成；缺能力/错误最终target写前诊断。原updater、恢复算法与状态不改。
3. 主会话采用实际Fork commit/tree/parents/CI到source lock；通过原preset installer同步受影响dogfood/平台副本，处理本次生成且可确认来源的sidecar，保留并行内容。
4. 运行V1–V3/V5，原Check对完整候选审查；缺陷回原实现owner。需要Docs delta时先形成完整隔离候选，经candidate Check后才由原RDT/Architecture owner最终整合。
5. 真实业务安装前从原来源合法处置原失败操作；展示精确目标、来源、工具写集后执行V4，不修改业务任务或其它checkout。
6. 完整Check、TaskCommit、完整固定B-to-HEAD独立Review、Delivery Review及发布合并；整体Completion另核验全部AC，再Closure/Finish与精确资源Cleanup。

## 3. 验证入口、输入与预期观察

- V1：GURU_UPSTREAM_DELIVERY_CLI=<固定匹配CLI> 配合原managed Python运行guru-upgrade-tools/tests/test_agents_target.py。观察真实prepare/apply/recover/resume/rollback及权限/正文行为，不能只运行mock。
- V2：原package tests/test_recovery.py及必要真实组合样本；普通中断/后续编辑保持原恢复语义。
- V3：原tests/test_native_install.py配真实原writer生成的旧安装fixture和匹配candidate，执行完整wrapper/preset重应用，读取目标自身runtime及Task/peer快照。
- V4：原业务dev读取原checkpoint/公开记录/数据快照，原owner合法处置后从source_locked修复来源安装，运行实际installed/native，复核3698历史Task/workspace文件及非目标指针。数量为原现场样本事实，最终仍以实际内容/mode比较为准。
- V5：运行原source/installed validators、apply.sh --repo .、check-dogfood-overlay-drift.sh、受影响package/runtime测试、git diff --check及sidecar检查；声明平台投影一致，不把它当真实多平台native发布矩阵。

## 4. 停止条件与适用回退点

缺Fork能力、固定来源/CI不匹配或真实测试失败时停止依赖工作，继续独立可做的规划/修复，不声明完成。原checkpoint/目标出现来源或后续工作冲突时交原维护owner，不手改冻结状态，不reset业务分支。实现机制变化回原Architecture/Author；范围变化回Clarify。

未执行软件发布或Task数据迁移，因此不新增对应回滚协议。业务工具回退仅走原source的工具恢复合同并保护业务数据。保留其它任务与工作树。

## 5. Delivery Policy（唯一）

full：本批覆盖整体R1–R8及AC01–AC07；代码、合同分发、固定依赖、原失败处置和真实目标验证齐备后才可完成。无延期责任或后继空切片。PR合并、安装成功与Task Completion分别判断；不把正式Release列入本Task完成。

## 6. Docs SSOT Plan（唯一）

strategy=no_docs_update_needed：既有#566 Requirements/Design/Test和ARCH-DOM-047已要求正确最终内容、原公共writer及两层恢复，本次修复实现对现有合同的违背，不增加业务行为或架构决策。历史测试贡献保留实际旧来源与限制，不追写成新通过。

本次必改的步骤说明由原canonical guru-upgrade-tools Skill/references独占，必要安装提示按现有README分工同步；它们属于执行接口源码，不在RDT中复制正文。原RDT owner在Phase2复核这一no-change判断；若完整候选证明有实际当前定义差额，改为delta_first并由原owner形成隔离完整候选，在最终Phase2前完成整合。Architecture沿真实no-impact结论复核，不制造空贡献。
