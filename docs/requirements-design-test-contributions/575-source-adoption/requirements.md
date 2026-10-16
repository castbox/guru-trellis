# #575 S1：正式来源采用需求

本贡献只承接 #575 Stage 1 的来源采用切片。整体 Task 继续拥有工具/任务原生切换、最终 `.4`、全部投影与定向验证；本切片不关闭发布 Issue，不表示整个准备任务完成。当前 RDT `.99/active`、Architecture `.93/active` 作为前驱 authority，本候选未晋升 shared current。

| Identity | 必须满足的行为 | 设计 / 测试 |
| --- | --- | --- |
| R575-S1-01 / BEH575-S1-01 | canonical 来源记录固定同一个正式 Fork commit/tree/ordered parents/成功 CI、CLI/Core 与 package manager；实际 checkout/build/API 必须匹配，版本字符串不能替代来源 | D575-S1-01 / T575-S1-01、02 |
| R575-S1-02 / BEH575-S1-02 | 当前公开文档区分已发布稳定 `.3`、本次未发布 `.4` 目标和 S1 暂留 `.3` manifest 的源码；稳定 tag/provider 与其原锁保持，不混搭新锁与旧 Guru 源码 | D575-S1-02 / T575-S1-03 |
| R575-S1-03 / BEH575-S1-03 | 构建准备通过来源记录选择正式源码，正常失败时不继续运行或补写构建 marker；同版本 stale build 必须诊断，不回退全局 CLI | D575-S1-01 / T575-S1-02、03 |
| R575-S1-04 / BEH575-S1-04 | 首切片只交付 source/doc 增量；旧完整 installed 图保留到原维护 owners 的真实切换，所有 M/S2 剩余工作与证明层次明确 | D575-S1-03 / T575-S1-03、04 |
| R575-S1-05 / BEH575-S1-05 | 历史 #495/#503/#566/#40/#43 证据保持原来源，候选贡献只由原 owners 晋升；不生成动态发布状态、第二 owner 或当前通过的替代证明 | D575-S1-02、03 / T575-S1-04 |

本贡献不新增业务功能、公共 Skill/schema/exit、兼容 runtime、版本支持族或升级算法。M、S2、最终 main candidate/tag/Release、真实业务安装与完整平台矩阵都不属于本切片的已交付声明。
