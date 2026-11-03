# ADR-KNOWLEDGE-NAVIGATION-ISOLATION：独立知识单元的发现与写入

Identity：`ADR-KNOWLEDGE-NAVIGATION-ISOLATION`；状态：`accepted`。适用范围：已完成 `knowledge-navigation-1` 文档切换的 RDT/Architecture 单元及其导航维护。来源为 [Issue #711](https://github.com/castbox/guru-trellis/issues/711) 和 [原隔离贡献](../contributions/711-knowledge-navigation-isolation.md)；精确内容由包含本文的完整 Git revision 与 locator 定位。独立评估和实际晋升由原 Architecture owner 合同承接；本文的 proposed 副本在晋升前不是已接受 authority。

## 背景与必要性

原规则已要求稳定身份、完整能力单元、隔离贡献和原 owner 晋升，但仍允许独立主题晋升时向共享根或下级 README 登记。两个业务正文互不相交的正常 Task 因而共同修改导航文件。Issue 的 backend PR #997 三方合并证据仅绑定其固定基线与候选；它说明共享写入的成因，不代表该 PR 当前状态或所有文档都会冲突。

当前需要解除独立主题对集中登记的依赖，同时保留完整知识的可发现、唯一、适用性和跨层关系。问题不属于 Git 合并算法，也不要求解决同一能力的真实语义重叠。

## 决定与责任

根入口保存体系稳定 identity、scope/status、职责/当前目录范围、真实公共版本、历史与未迁移边界及发现方法。完整单元按稳定能力或职责划分，在自身正文或自身目录内保留 identity/aliases、原 semantic owner、状态、适用来源、晋升依据、完整定义、必要关系与替代范围。一个 Issue 不自动对应一个新的 current 单元。

普通 Task 新增或修改语义独立单元时，只维护该单元、自身目录内的局部导航及真实受影响引用。不向根、下级共享 README、统一 index/manifest、system/ownership 汇总、共享 metadata 或生成需提交索引逐项登记；不递增无关全局版本，也不追加合并历史。入口自身的身份、适用状态、位置、发现合同或必要跨体系关系实际变化，仍由原 owner 修改该入口。

Agent 从本阶段适用的稳定入口取得目录范围，以文件列表和限定 ID/alias/概念检索定位，再读取完整单元并核原 owner 晋升事实、适用来源、状态和必要关系。搜索只定位，不拥有 authority；目录、文件存在、排序、日期或更大版本均不能单独放行。CURRENT、accepted target、未晋升 contribution、历史和 superseded 定义保持各自含义。缺完整来源、晋升依据、引用或存在重复 current 时，由原 repair/澄清处理，不能用搜索摘要填缺。

RDT 与 Architecture 原 owners 分别拥有自身语义和晋升。新/改名/替换/删除单元时维护真实受影响的引用；旧引用须仍能定位其历史意义和转换，不保留第二活动完整正文。两个 Task 共同修改同一能力或有效关系时，原 owner 比较适用 base、双方完整 proposal、实际 target 和受影响消费者，保留仍有效条件。文本自动合并可用，但不能替代该语义整合；不得复制关系或只取一侧来制造隔离。

## 代价与替代

读取端承担限定发现、核状态和必要关系的工作；维护端承担单元自身 metadata 与受影响引用的同步。该职责由已有 Markdown、文件工具、rg 与原 AI owners 完成，不新增 registry、服务、schema、缓存、锁或进程协调。共享生成索引仍需各 PR 提交，不能解除共同写入；把总表移到下一级同样无效。强制全部 Task 串行会限制原本独立的工作，因此不采用。

## 迁移、兼容与退出

[迁移合同](../../../trellis/presets/guru-team/MIGRATION-711.md)拥有匹配规则安装和项目文档切换的执行步骤。切换前固定旧完整来源、稳定引用、目标范围和未迁移范围，验证完整定义、关系及适用发现；未达条件保原 authority，候选 proposed，不声明消除共享索引写入。达条件后，新任务采用本写入合同，不双写旧索引。

在途 Task 仍读取其阶段适用版本；最终集成触及已迁移单元时，原 owner 重读真实目标，整合到当前完整单元，不把旧读兼容解释为旧索引写权限。Task Finish、合法 Reactivate 重选或真实依赖变化按原合同结束旧普通读取。切换前失败保原入口；切换后由原 repair 或受审 successor 修正；不可变历史、版本和原始失败证据不改。

本决定窄化 ADR-031 和既有规则中独立主题仍可触发共享导航登记的范围，保留完整知识、稳定身份、必要关系、未迁移完整来源和两层技术基线职责。ADR-KNOWLEDGE-FINAL-INTEGRATION 的隔离候选、完整候选 Check、原 owners final integration/readback、actual after 重绑、最终 Check 与独立完整 committed Review 全部保持。公共 Skill I/O、真实 API 版本、GAP lifecycle 和业务项目采用责任不变。

## 重审条件与证据边界

目录发现无法定位完整适用定义、current 判定缺必要来源、稳定引用语义丢失、单元边界变化或新的真实共同关系出现时，原 owner 重审受影响范围。语义正确性不能由无文本冲突或目录结构证明。确定性组合、实际 Agent 读写、分发/安装、文档迁移与业务项目采用分别提供其真实证据；知识接受本身不证明全部验证、Task 完成或软件 Release。
