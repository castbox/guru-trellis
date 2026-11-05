# D1 精简 legacy 正式归档恢复需求

## 1. 整体来源与术语

本批 accepted_scope 为 Task 根 prd.md 当前公开版本，scope_ref 选择 AC1、AC2、AC3、AC4、AC5、AC6。整体定义见 ../../prd.md。Direct Source 为 https://github.com/castbox/guru-trellis/issues/712 全文，角色为要求与两仓职责约束；Trellis #64 / PR #65 为公共前置交付事实；研究 compact-formal-reactivation.md 为代码事实而非门禁结论。正式 legacy 仍须完整历史资格判断。

## 2. 整体与本批目标、非目标

D1 是首个且全量切片：使原样十字段正式归档进入公共转换、Guru 获取/绑定、目标 native 续接及下一 scope owner。覆盖 R1–R7，旧原档只读，TaskId/source 保留，generation 由公共解释决定并增代一次。完整来源 Issue 的业务未交付部分不因恢复变成已完成。

不新增公共模型、旧格式解析器、人员体系或任意旧格式框架；不操作真实业务 Task，不实施 Opening V4，不增加攻击/锁/并发压力范围。

## 3. 本批起点、前序结果、依赖与剩余责任

无前序 Delivery。起点 main@3a4b65ab08cdfe05d97f68e7f2e7512254d728f1 的 shared_finish/raw identity 仍拒绝 compact 形状。已取得 Trellis source 619133c62d1487c5fbecbf9e00cea9e3f5ea52a6 固定成对包、API1.0，hash 和隔离 capability 已核；尚未证明 Guru 目标安装及续接。

本批剩余责任包括实现、原工具 owner 采用、历史审核、实际 native 联合验证、文档整合、完整质量与交付。D1 合并不代替整体 Completion。

## 4. 本批调用方、场景与流程

S1：AI Reactivate 读取精确归档、旧安装/Finish、PRD、summary 和 PR/Git；只对正式历史调用公共检查和转换，观察相同 TaskId 的新代与原档不变。
S2：公共 pending 或 applied 后绑定中断时，原入口续接同 operation，按真实 key/ref 建立控制，不重复 prepare/增代。
S3：私有结果丢失时读取真实后继，核关系后续接其阶段；后继再次归档后 native TS/Python 与 Guru 仍正确消歧保留前驱。
S4：source、历史、PR/Git 或后继不一致时返回具体诊断，保护原档/其他任务。
S5：原 schema1/schema2、人工 archive_resume 和未完 Finish 维持原出口。

## 5. 完整行为、条件与约束

R1/R2：公共 inspect 从精确 archive locator 返回受支持 family/key，历史 AI 核验独立进行；不先补字段或删人员字段。缺 generation 不通用补0。单个 parser/status/PR 或本机 receipt 不能替代资格。
R3：共享 reader、正式转换选择、后继发现及归档前驱关系消费者采用同一公共家族解释。规范旧 scope 可由原 source owner 投影，不回写原档；普通 current reader 仍严格。
R4：保持原 TaskId、source、历史 scope/交付/bytes，旧 gates 不复用。下一 scope owner 实际读取当前关系，历史 BASE-01～05 不扩大到完整 #130。
R5：仅 applied 后绑定，pending 继续原操作。已有合法后继优先，receipt 丢失不再增代；后继已归档回其实际 owner。
R6：目标自身 native Identity/Bind/continuation 和下一 scope owner 必须实际消费，外部新工具代执行和静态 DTO 不够。再次归档用合法代表状态补定向读证据，不要求第二次真实增代或空 Delivery。
R7：原 tools owner 核 fixed source/build/API，canonical 和 dogfood/平台投影同步。配置、其他任务与会话保持。实现阶段分别说明安装、转换、本地控制、续接和业务范围状态。

## 6. 本批验收、验证方式与未决项

AC1：原样 compact fixture、真实 Git 和受控 PR facts，经 installed 公共分类/Guru 准入/实际转换，观察 TaskId 不变、generation+1、archive bytes 不变。
AC2：pending、绑定中断，原操作恢复后只有一个后继/资源。
AC3：移除已消费私有结果后，已有实际后继续接；再次归档 native TS/Python/Guru 正确解析。
AC4：普通 source/历史/后继错误准确诊断；原正式/人工/未完路径回归。
AC5：固定包的完整代表安装中，AI 原 owners 实际执行 Identity、Bind、continuation 和下一 scope owner；受控 provider 仅证明本地集成，不宣称真实 GitHub/业务生产。
AC6：定向 package/runtime、canonical/dogfood/installed、reapply/drift/sidecar/diff-check。最多一个必要 clean throwaway；不跑完整多平台升级/Release 矩阵。

当前无待用户决定的范围问题。验收尚未执行，不预填 pass。

## 7. Canonical 引用与本轮差额

docs/requirements/current/completion-closure.md 的“跨 clone 的 Closure 输入与共享终态”须扩展显式支持的正式 compact 家族，保留 #635/#669 边界。
docs/design/current/completion-closure.md 的“最小共享 Closure 载体与恢复”须让公共正式 owner 和前驱消费者一致，保留单写与原机资源边界。
docs/test/current/completion-closure.md 的 T635/T669 须增加 compact 和 native 联合路径，旧结果不外推。
Architecture 由独立 owner 读取 docs/architecture/README.md 定位 ARCH-DOM-060/shared lifecycle 与适用完整单元，判断本轮影响；本 PRD 不预定其结论。
