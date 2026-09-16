# #417 技术设计

## 1. 边界

需求与验收见 [prd.md](./prd.md) R1-R6。复用既有 semantic_authoring eval 模式，为 Phase 2 增加事实 staging、公开读取集合与正式调用承接，不建设通用多 owner 编排框架。
保留 post_owner 作为确定性路由测试，不宣称其证明模型完成语义审查。

## 2. 生产合同

canonical Skill/contract 明确当前 AI 的六步顺序，并列出原 recorder authoring 字段。
AI 编写语义内容；原 recorder 派生 task/content identity；原 checker 验证结构和 freshness；原 wrapper 输出唯一出口。
保持 public input 2.0、private result 5.0、四出口及 consumer、wrapper argv 不变。
owner 尚未执行时当前 AI 继续；真实 authority/验证缺失按原路由处理；校验错误结束当前 invocation，fresh reread 后重新审查；不得把 worker 缺失当作平台能力缺失。

## 3. Native 验证

新增 case id native-owner-clean 和 native-owner-finding，显式声明 semantic_authoring、Codex adapter 和沿用既有 authoring case 的模型配置。
使用真实 installed fixture，提供 task、三份 approved planning、Docs、实现、测试、live diff/dirty paths 和实际验证输出。
finding fixture 使用最小业务无关函数：需求规定上界包含，错误实现在边界排除，运行测试复现失败；clean 使用满足同一需求的实现。
Architecture 上游公开结果由对应 AI owner 审查和正式 wrapper 形成，不用 host 伪造 pass。fixture 不包含用户业务数据。

owner_staging.py 仅准备 Phase 2 事实，不调用 check-passed 或 check-implementation-required recipe 生成 owner result。
native_adapter.py 按当前 skill 使用专属 required-read 集合；不按 case id 决定出口。expected exit、评分配置、示例结果、eval control 不进入模型可读投影。
模型完成九维判断后 author 原 recorder 所需语义字段；boundary 原样转发给真实 installed recorder/checker/wrapper，不补维度、finding、reason 或出口。
content token 从真实 fixture 派生，不从模型投影目录或人工摘要派生。

结构测试验证输入/输出边界、required reads、正式调用顺序和无 host 预置。真实 native 验证还需 AI 阅读 transcript，核验九维结论及 finding 的实际证据。
fake-native、关键词和 host 预填 grading 只能用于驱动结构测试，不能替代真实 native 验收。
扩展只覆盖本次 accepted path，不增加防攻击、锁或进程身份 authority。

## 4. Architecture Alignment

绑定 guru-maintain-architecture-baseline:2.0、active baseline current-main-0.6.17-guru.52、constitution guru-trellis-design-constitution-v1、change contract guru-trellis-architecture-change-contract-v1。
authority locators 为 docs/architecture/README.md、docs/architecture/00-foundation/design-constitution.md、docs/architecture/06-governance/change-contract.md。
规划判断 no_architecture_impact：生产 sole owner、public I/O、状态生命周期、single writer 和相邻 consumer 不变，只修正执行说明和既有 eval 承接。
不创建 contribution/ADR、不修改 shared current/GAP。若实现需要新生产状态、owner、公开合同或跨层 authority，先 fresh Planning Architecture，不沿用此结论。
对应 EVO-004 唯一 owner、EVO-005 去除错误等待、EVO-007 投影一致；EVO-001/002/003 既有 authority 保留，EVO-006 生命周期重构不进入范围。

## 5. 安装与文档

Docs SSOT Plan 仅见 PRD 第 4 节。canonical 改动经原 preset installer 同步，不手改生成副本作为唯一来源。
最多一个代表性 clean installed fixture，复用运行两个 native cases；全平台 parity 不等于全平台 native 模型通过。完整矩阵仍由 #410 负责。
保持 Architecture authoring 和 post_owner 的原行为；不新增兼容 wrapper、旧 schema reader 或无人消费的 metadata。
