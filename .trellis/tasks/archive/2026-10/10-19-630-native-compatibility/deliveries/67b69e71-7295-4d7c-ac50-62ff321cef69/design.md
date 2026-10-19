# D3 Python 与路径脚本验收收敛设计

## 1. 设计目标、需求承接与内容基线

承接本批 DR1–DR4、DA1–DA3，整体 AC7/AC10。Development baseline 沿 Task 的 main；本批内容 B=cf07d082c046b8e5e3c5050a603f22285821b215，来源为当前 HEAD 的最近已交付祖先 D2 head；规划 H0 同为该值。PR目标为 main，三者职责分开。

实际独立 candidate_assessment 已返回 baseline_current / no_architecture_impact，Architecture current-main-0.7.0-guru.103、constitution-v1 current。该结论只支持文档机制，不替代后续 final_plan 或 Check。

## 2. 当前系统、边界与目标差额

D1已交付产品跨系统修复，D2已交付会话采集器修正。当前 Issue 和根PRD已接受脚本验收范围；当前 native RDT 和 CI README 仍保留真实会话必需措辞。本批定向修改这些正文，并更新唯一 Test 的当前状态与实际结果。产品Python、工作流和采集器不变。

## 3. 来源设计处置（唯一）

| 来源及承诺 | 处置及落点 | 理由、影响与上游处理 |
| --- | --- | --- |
| 当前 Issue/根PRD：Python runtime、目录脚本及公开wrapper为验收范围 | retain：第4、8节逐文件同步 | 源Issue已实际回读；不新增模型义务 |
| D630-06：独立driver/target，保留首失败，不放宽matcher | retain：当前design原D630-06主体 | 既有脚本与事实边界未改变 |
| 旧R630-06/T630-08：Windows真实Codex为完成阻塞条件 | change：撤销当前义务，保留cf07d082的旧定义定位；T630-08标为已撤销 | 真实整体范围已由原Clarify接受；不把原失败改成通过 |
| D1/D2 implement的partial剩余Windows会话责任 | retain历史、由新整体scope替代当前义务：唯一Test记录范围边界 | 不修改历史Delivery或删除实际失败 |

## 4. 模块、职责与设计取舍

原RDT owner定向同步 docs/requirements/current/native-compatibility.md、docs/design/current/native-compatibility.md、docs/test/current/native-compatibility.md，维持三层完整定义和引用。仅这些当前单元新增本次revision与旧Git定位，不复制全局版本集，不改历史贡献的旧requirement/design。

CI README 说明原windows_codex_session手动入口仍为显式诊断能力，不是#630验收义务；保留已实现的隔离配置与600秒事实，不创建runner选择。

唯一贡献Test保持历史区及原始结果，顶部当前状态指向本轮范围；文末新增D2合并、真实Windows超时与采用边界。可读取旧事实，不以历史“待完成”覆盖当前scope。保留手动采集器有明确维护者诊断调用方，不移除其已交付实现。

## 5. 接口与数据

没有产品API、schema、Skill输入输出或Task数据模型变化。R630-06/BEH630-06、D630-06身份保持；T630-08当前行明确withdrawn，并链接旧Git定义，其余T630-01..07保持。旧引用仍解析到历史含义，不能偷偷赋予T630-08新的Python测试语义。

## 6. 状态、顺序、正常与失败流程

源Issue修订→整体PRD接受→同D3 scope修订已实际发生。接着完成规划、Wording、final_plan、Approval与Activation，再实施文档→RDT直接同步→Phase2→正式Check→提交与完整Review→PR交付。后续Completion独立复核所有AC及D1/D2/D3事实。

发现当前正文仍要求会话或把脚本成功称为Agent成功时，回原文档owner修正；不启动模型补证。

## 7. 恢复、兼容、迁移与集成

直接修改已有文档，保留旧Git版本和历史Delivery；没有双读、fallback或新兼容层。没有DB、运行配置或生产数据迁移。公共事务失败通过原owner同身份恢复，不重复提交或发布。真实Windows会话保持未完成，不由范围修订变成通过。

## 8. 验证设计

V1对应DA1：语义核对Issue、整体PRD及当前RDT三单元，确认必需验收为runtime/目录脚本，旧义务有历史边界。

V2对应DA2：核对唯一Test与原run报告。采用D1原生产品/安装/维护、D2三系统CI及14项直接回归；Windows run39285077678保持timed_out/600秒，不重跑。实际来源见唯一Test链接及其原始报告。

V3对应DA3：完整审查git diff，执行git diff --check及本地文档链接存在性检查；确认无Python/workflow/collector变更。纯文档变更不新增镜像测试、字符串镜像断言或模型验证。

## 9. Canonical 引用、本轮差额与实际未决项

R630-06/D630-06/T630-08及CI说明为全部差额；其余native能力、Architecture .103、installer与平台canonical保持。原RDT owner在Phase2前直接同步完整当前单元，原Architecture owner判断本轮无影响及实际写入适用性；不预建贡献或ADR。没有未决产品选择；本批工程检查和正式语义门禁尚须实际完成。
