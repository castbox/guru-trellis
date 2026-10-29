# #687 固定来源采用：Architecture 差额

本贡献属于 Task `687-adopt-castbox6`、generation 0、Delivery `c973480b-ade3-4b54-85c2-59c63c25fc54`。要求来源为 [#687](https://github.com/castbox/guru-trellis/issues/687)；对应实际方案位于该 Delivery 的 `design.md`。本文件供原 final_plan、候选 Architecture/Check、final_integration 和 committed Review 消费；拟写 shared-current 正文位于同名目录的 `proposed/`，当前尚未晋升。

## Authority、before 与差额

适用 authority 为 `guru-trellis-architecture`，constitution 为 `guru-trellis-design-constitution-v1`，change contract 为 `guru-trellis-architecture-change-contract-v1`，concern set 为 `guru-trellis-architecture-change-concerns-v1`。晋升前完整定义由 Git `7718d129bcb2055d77c7f43d0e4edca9aee313ea` 的命中正文定位；原owner在实际写入前另读live target和expected-current。

Before：ARCH-STACK-TOOLS-001、ARCH-INT-014已将框架来源唯一归canonical source lock；ARCH-CUR-074、ARCH-DOM-057、ARCH-INT-060仍把`.5`直接写成当前来源。采用17015f98/.6后，这三处正文需要与来源责任一致。

Target：原source lock继续选择精确Fork/CLI/Core；三个完整当前单元引用该唯一选择，保留#630当时`.5`与7f050fa的历史观察、原installer/LF/raw/用户编辑/上游所有权条件。#687 Test单写新来源采用与installed停止回归的实际观察，不回写#630历史结果。没有新增owner、公共API、状态、兼容层、GAP或架构决策；change_path=target_native，无需新ADR。

## 完整拟写单元与职责

| 目标 | 本轮差额与必须保留的条件 |
| --- | --- |
| `docs/architecture/01-current/system.md` / ARCH-CUR-074 | 去掉当前固定`.5`，明确source lock拥有精确pair；保留Path/URI/Bash/UTF8、hook/index、LF/raw/用户保护及native/Windows/Release证据边界；分开630与687观察owner。 |
| `docs/architecture/03-domains/ownership.md` / ARCH-DOM-057 | 原source owner消费canonical lock精确pair；installer/TaskCommit原owner、ADR-032与上游entry所有权保持，630历史观察不变。 |
| `docs/architecture/04-integrations/distribution.md` / ARCH-INT-060 | 当前pair从lock读取，630的`.5`/7f050fa明确为历史；保留实际build/目标采用、raw/sidecar、upstream边界和原update/maintain/recovery/reapply验收路径。 |

同名目录保存每个目标文件的完整proposed内容。Author只写隔离候选；独立Architecture审查完整差额与未改消费者。原Check候选检查通过后，原Architecture owner在final_integration读取实际live目标、组合已审差额、写入并读回。implementation重建候选，最终Architecture/Check、TaskCommit和完整B..HEAD独立Review覆盖实际写入。RDT贡献与晋升归原RDT owner。

## Required concerns

| Concern | 适用性与本轮承接 |
| --- | --- |
| authority-binding | applicable；上述固定Git正文与current lock、实际candidate分别绑定，不以新CURRENT证明旧约束。 |
| constitution-binding | applicable；官方扩展面、唯一语义owner和最小必要文档修订符合原宪法；不复制原则或制造评分。 |
| boundary-and-decision | applicable；目标是修正三个当前定义的来源选择表达，无新决定；引用ARCH-STACK-TOOLS-001、ARCH-CUR-074、ARCH-DOM-057、ARCH-INT-014/060/063与ADR-032。 |
| owner-and-single-writer | applicable；canonical lock原source owner、生命周期原Core/Python owner、隔离Author与shared-current晋升owner保持分离。 |
| compatibility-and-exit | applicable；直接修改当前说明，保留合法历史观察，无runtime双读或兼容新路径。 |
| gap-and-deviation | applicable；没有新GAP、owner或宪法例外；闭合本轮采用会造成的当前来源说明偏移。 |
| parallel-scope | applicable；仅隔离贡献与proposed写作并行，禁止实施worker直接写shared-current三目标。 |
| evidence-and-freshness | applicable；方案、source/build、真实tools-only采用、installed停止、业务采用及Release分层。实际观察由687 Test拥有，当前贡献不预填执行成功。 |
| review-and-promotion | applicable；final_plan审实际贡献；候选Check后原owner晋升完整单元并判断写后适用性，再回最终质量链。 |

## 验证与边界

本轮实际验证由Delivery方案V1–V5及687 Test承接：严格匹配来源、单个隔离source_locked采用、Task/session/用户内容/peer保留、两种旧profile的installed公开stop与重试、source/installed/ownership/reapply/drift/sidecar。贡献和知识晋升均不证明这些执行已发生。完整累计平台矩阵、远端marketplace安装、新Guru软件Release与真实业务项目采用不在本Task范围。
