# D1 真实 Agent 方法观察

## 对象、输入与边界

本观察对应本 Delivery design §8 的 V1—V4、JQ-AC1—6/8。使用实际 `codex-cli 0.166.0`，经 `codex exec --ephemeral --json` 执行四组独立只读材料；没有指定模型覆盖。外部 collector 复用 #735 的完整 provider 复制和原生进程采集方式，只记录输入、工具、输出及退出事实，不按关键词或退出码判语义通过。

输入及 prompt 在运行前冻结于 `/tmp/guru-747-behavior/inputs/v1` 至 `v4`；独立预期位于模型工作区外的 `/tmp/guru-747-behavior/host/expectations.json`，冻结记录为同目录 `frozen-inputs.json`。模型读取独立虚构项目事实和当前完整 canonical provider；provider 不含 tests/evals、host 预期或本 Task 的验收答案。六个方法正文的实际字节记录在 `host/tested-methods.json`，四个运行各有 `provider-snapshot.json`；核对确认四份 provider 对应同一方法版本，冻结输入未变。

这些是原 Clarify/Author、Phase 2 派工和独立审核职责的方法执行观察。没有运行正式公开 owner 的完整生命周期调用或 formal Check/Branch Review，没有构造或宣称其通过结果。材料中的产品事实是虚构 fixture；未构建、操作或测试真实业务应用，也不证明 QA 缺陷率或执行成本下降。

## 实际观察

| 观察 | 实际入口与结果 | 原始结果位置 |
| --- | --- | --- |
| V1 | Clarify/Author 方法只读推导；原生退出 0，306.30 秒 | `/tmp/guru-747-behavior/runs/v1/native.jsonl`、`native-final.txt`、`collection.json` |
| V2 | Phase 2 实施派工方法只读评估；原生退出 0，83.76 秒 | `/tmp/guru-747-behavior/runs/v2/native.jsonl`、`native-final.txt`、`collection.json` |
| V3 | 独立审核方法只读审查；原生退出 0，217.36 秒 | `/tmp/guru-747-behavior/runs/v3/native.jsonl`、`native-final.txt`、`collection.json` |
| V4 | 纯函数验证选择对照；原生退出 0，247.08 秒 | `/tmp/guru-747-behavior/runs/v4/native.jsonl`、`native-final.txt`、`collection.json` |

退出 0 只说明原生执行完成。以下结论由观察 owner 阅读完整原始输出与实际工具记录，对照预先冻结的独立预期判断。

### V1 连续操作、交接与真实选择

Agent 区分编辑页确定、上传完成、草稿可靠保留和服务器保存。它根据“最后一个引用释放即删除”及 `closeEditor()` 先于 `confirm(value)` 的顺序，识别没有 upload 引用时的正常引用空档；提出表单先持有再释放编辑页引用。它也识别上传回调仍持有旧 editor 对象，当前可见对象及改选结果可能无法正确更新，并要求结果归属具体选择。

验证安排涵盖上传期间改选、局部确定后退出/恢复、失败重试或移除、最终保存一致性。它保留系统返回交互这个真实未决选择，并另外识别材料未规定“上传未完成时保存”的可见行为；所给处理建议明确未确认。引用和回调机制由 Author 解决，没有要求产品提供事务代码。

### V2 旅程优先与局部测试边界

Agent 将直接 `pasteText`、直接 `confirm`、替换整段媒体路由和保存同实例 fake 的证明范围分别限定为局部逻辑；没有据此推定长按菜单、真实页面交接/焦点、持久化保存重入或丢弃行为已通过。

在应用、服务与设备已具备的事实下，它优先安排真实长按粘贴至媒体确认、焦点、保存重入的一条最小完整旅程，再补具有独立价值的参数组合。它单列显式丢弃验收，保留既有边界测试，没有用一条旅程替代其余必要验收。

### V3 独立问题、实际构建与替身语义

原始工具记录显示：Agent 先读取 `facts.md` 和方法 authority，发出基于已接受行为的审查问题，再执行 `cat candidate.md`。这些问题包括两组已接受媒体组合、草稿往返、URL/到期时间更新和下一帧可用性；没有由实施总结决定范围。

对照候选后，它识别开发机 full ffmpeg 与应用 min 包的能力差异，以及 H264/AAC MOV 单样本无法支持 HEVC/PCM 的应用结论。它没有因 `h264_metadata` 缺失就另立缺陷：材料未证明该路径依赖它。它指出 JSON 生成新对象而 UI 依赖对象身份的冲突、同实例 fake 对持久化恢复证明不足，以及 URL 非空/cache hit 无法证明冷缓存解码就绪。

所选补充观察仅覆盖已接受的两组编码、真实持久化/更新消费者及轮播帧状态，没有要求默认全格式或设备矩阵。输出明确材料没有可执行源码、测试体或构建结果，因此此处不是实际应用实现覆盖或架构适配结论。

### V4 低成本纯函数对照

Agent 为 trim-only 函数选择直接廉价单元测试，预期包括两端空白移除、内部空格和大小写保留、空及全空白输入返回空串。它沿用已存在的 `strip()` 候选，没有为制造失败要求删除实现或固定回退红绿，也没有追加 UI、设备、I/O 或 E2E 旅程。所提测试尚未执行，未宣称正式批准、测试通过或 Check 完成。

## 适用结论与未验证项

这四组观察支持当前方法在本组中性材料下能推导正常连续操作和交接、辨别真实产品选择、限制测试证据并按风险裁剪验证。原始工具记录没有读取 host 预期、父目录或其它业务仓库，也没有产品/Task 写入和正式门禁调用。运行后教学例子的来源前提澄清不属于四组模型输入；六个方法正文未变，现有观察仍适用。

本报告不证明四组正式公开 owner 链、真实业务验收、已安装 dogfood 行为、多平台发布或统计收益。分发、reapply/drift、工具维护及最终质量结论由 V5/V6 和原 owner 的实际结果承接，不能从本报告推定。外部临时日志用于本次检查，长期结论保留本正文即可，不复制转录或新增长期行为账本。


## 本轮新旧对照及收敛验证（追加，旧 V1—V4 观察保持）

### 原 A/B：局部收益，未证明全面改善

旧 B 基线为 3a4b65ab08cdfe05d97f68e7f2e7512254d728f1，当前 H 为 7b14b6f83f274bd3b08e2721be8624516374b73d。四组各一对、共八次原生方法执行均退出0；独立评价先冻结标准，再阅读匿名完整答案和读取顺序，固定盲评后解盲。该退出事实不证明语义通过。

原报告支持 V2 的真实旅程优先有局部改善。V1 核心交接诊断相当，旧版普通最终服务器保存断言更完整；新版零引用删除因果更直接并识别上传中保存未决。V3 核心证据问题相当，外显独立问题先于候选读取未改善；早期带顺序提示的正向观察不能证明去掉提示仍自然执行。V4 两侧均选便宜单测，新版却增加正式流程加载/说明开销，不能宣称简单任务减负或整体成本下降。

原材料、标准和结果保持不变。完整比较及资源限界见 `/tmp/guru-747-ab/comparison-report.md`；冻结输入和源映射见同目录 `host/`，八次实际运行见 `runs/`，独立盲评见 `/tmp/guru-747-ab-evaluation/`。本正文不复制逐轮日志或成本表。原 V1 直接提供候选释放顺序及旧 editor 回调，主要观察已给缺陷识别，不能据此证明从分散来源发现未知问题。

### E1：加载方式对照没有单向优胜

同一当前 H provider、原冻结 V1 事实与标准下，pairA 为自主检索，pairB 为提前提供完整适用方法单元。盲评冻结后按 `/tmp/guru-747-convergence/host/e1-mapping.json` 解盲。自主检索组普通最终保存断言更明确；完整 upfront 组已确认要求与技术职责区分更稳，却未独立展开正常服务器保存观察。两侧都识别引用空档与旧对象结果归属。

读取不完整是原轨迹中的事实，但不是已证明的唯一原因。既有来源保真和自检规则本来存在；完整材料可见性也不等于模型完整消费。E1 不能分离检索/注意力成本、内容可见性与模型波动，不支持“完整加载即可消除遗漏”。盲评及精确限界见 `/tmp/guru-747-convergence/evaluation/reviews/e1-blind.md`，实际两组输出和读取顺序见同目录上级 `e1/pairA/`、`e1/pairB/`。

### E2：新领域三产物对照仍有遗漏和 candidate 收窄

仓储调拨事实由三份分散来源和两份 current 文件构成。双方实际生成 PRD、design、implement 三份正文；A 为当前 H baseline，B 为正式激活后实施的修订 candidate。评价者先读冻结来源/预期和双方六份完整产物，再读 native-final/read-order；final 的运行路径暴露 baseline/candidate 身份。因此这是产物先盲读、最终路径后暴露身份的部分盲化评价，不能称全程严格盲评。未重跑或修改原标准。

双方均保留普通有效匹配预留的最终成功主线，pending-back 未决仅阻塞依赖分支。candidate 的 discard 缺合同声明及原职责安排更明确，轨迹中也有通读三产物后修正映射的实际自检。但 candidate 在恢复场景前置和设计中将“已确认内容保留/重开”收窄为“已由 saveDraft 成功持久化”的内容。PRD 表格仍列原要求不能抵消该收窄；未手动保存的已确认内容接管机制与验收没有闭合。

双方还未完整展开当前内容与 save 返回 revision 在 reserve 前的匹配，以及 pending 修改后再次申请前的保存/版本衔接。已提交记录重开只读所需的状态/结果读取合同也未明确补齐责任和阻塞范围。独立 discard API/失败合同仍有缺口，candidate 一处“现有 discard 能力”不能视为该能力已证实存在。这些是规划表达和合同连续性缺口，不是已运行产品故障；双方没有服务/库存实测。

本样本不支持 candidate 全面优于 baseline，也不证明方法已消除义务遗漏。局部改进与 candidate 失败均保留，不把本次结果回写为旧 V1 通过证据。完整冻结评价和定位行号见 `/tmp/guru-747-convergence/evaluation/reviews/e2-blind.md`；实际产物见 `/tmp/guru-747-convergence/evaluation/e2/pairA/outputs/` 与 `pairB/outputs/`；冻结来源和预期见同目录 `inputs/`、`expectations.json`。一次配对、部分盲化及方法 fixture 均不足以证明稳定因果、业务 QA、未知缺陷泛化或线上缺陷率收益。


## 本轮原 review 职责回归检出：启动失败，无法评价

在原 E2 结论保持不变的前提下，本轮只检验原 review 对同六份既有产物的检出能力，不再次生成规划。before 为当前 V2 工作树完整 provider，不是历史 H；修改前冻结两 canonical 原字节及2545份 provider 文件 hash，位于 `/tmp/guru-747-continuity/before/` 与 `provider-manifest.json`。after 仅含 Author planning-body 与 review-sufficiency 两方法正文差额；原 A/B、E1、E2 的来源、判据和结果不变。

预定最多两次 native review，实际 P/Q 均在启动阶段返回1、timeout=false，无 report、工具调用、材料读取或 usage，错误同为 `CPA: unknown provider for model gpt-6.1-sol`。CLI 内部 Reconnecting 事件不算新增完整实验。没有更换模型、覆盖配置或追加重试。两 run 的有效配置相同，但其配置 hash 已不同于 E2：本轮 current 为 cpa/gpt-6.1-sol、model_provider=magpie、effort=medium，argv 无 model override；变更原因未查明，不能说跨 E2 使用同配置。

独立评价冻结为不可评价：空报告不是“未发现缺陷”，启动错误不是方法或被审规划的业务失败，相同错误也不能证明前后效果相同。本轮没有取得条件收窄、版本连接或缺失读取合同的语义检出证据，既不验证也不否定方法修订，更不证明改善。原始记录见 `/tmp/guru-747-review-regression/runs/P/native.jsonl`、`runs/Q/native.jsonl`；实际冻结输入/provider映射见同目录 `host/`，独立结论见 `evaluation/reviews/unassessable.md`。本轮停止于该证据缺口，不为获得有利结果继续运行。


## 后续 attempt2：已知六产物的 review 检出回归

此前两次启动失败原样保留。本次单独 attempt2 两次均完成，冻结共同来源、current、六份旧产物、提示及判据相同，pair配置相同且未增改材料；5102份provider entry核验。独立评价先冻结结论再揭示版本：P 为 V2 before，Q 为 V3 after。双方实际读取来源及两组各三份产物，没有在中性报告/读取记录暴露可映射的运行身份路径。

双方均检出已确认内容保留被保存前置收窄、当前内容到保存 revision/匹配预留/最终成功的连接缺口，以及保存失败验证遗漏。共同检出不计为新增方法收益。Q 额外明确检出两组产物的已提交重开缺少状态/结果读取合同，P 没有将该独立缺口列出；Q 还指出本人申请范围的验证缺口。Q 的预留恢复建议与 full Policy 提示没有足够依据作为额外已证缺陷，不计效果。双方均保留 discard 缺合同与 pending-back 未决的原边界。

该观察支持本次 Q 多检出一个既有目标问题，不代表问题已修复。六产物已用于方法开发，不能据全新执行上下文消除样本适配；每条件一次不能建立稳定优越、广泛泛化、确定因果或产品改善。完整揭示前冻结评价位于 `/tmp/guru-747-review-regression/attempt2/evaluation/reviews/review-regression.md`。旧 A/B、E1、E2 未改善及退步结论均保持。

## 新维修预约领域：作者首稿 V3/V4 配对

本轮只将已有同对象推演明确前移到开始展开 design，并同时展开正常成功可达与不匹配结果不可采用。修改前冻结当前 V3 的完整2545文件 provider，位于 `/tmp/guru-747-design-entry/before/`；after V4 仅改 Author planning-body 一处 design 展开句。新维修预约来源与七条判据在运行前独立预审并冻结，未复用旧六产物作为待写答案。P→X 为 V3 before，Q→Y 为 V4 after。两 native 自然退出0、600秒内完成，pair配置相同、来源/提示相同，每侧实际生成 PRD、design、implement 三份正文，原字节保留；退出0不等于语义通过。

独立评价完整读六份正文并补读截断部分，再读中性 final/read-order 和执行事实，未读provider、版本映射或成本，结论在揭示版本前冻结。C1—C7 双方均充分保留业务承诺：普通批准成功、真实合同缺口及短信未决限制在三份正文对应，没有重现 E2 的保留条件实质收窄。双方都定位终态发现和批准历史的读取合同缺口，共同能力不能记作 V4 新收益。V4 的异步结果接纳更具体，包括同预约/请求关联、终态后旧 pending 不能覆盖、操作后重读及匹配事实未齐不拼成成功。V3 已有防旧页面响应及断言，不能因其机制概括就判为已证缺陷。没有全面单向优胜。

此实验不是严格密封：X 列实验父目录并以 rg-l 搜索，该搜索至少检查匹配文本以返回另一provider/run文件名；可见轨迹没有输出另一run正文、host判据或旧报告正文，不能进一步推断已读取答案正文。X 还读取自身 before hash 快照，Y 搜索全局 skill 入口。因此不能宣称完全未接触外部文本，也不能把隔离不足抹去。

这是一例新领域首稿迁移观察，每条件一次，文件路径探索及模型波动限制归因。可说本例双方保真和成功主线均好，V4 异步接纳局部更具体；不能证明普遍泛化、稳定收益或确定因果。缺合同分支仍未完成，未执行产品代码、服务验收、正式 Planning Approval 或 Check。完整冻结评价及产物行号位于 `/tmp/guru-747-author-transfer/evaluation/reviews/author-transfer.md`；实际执行与三产物由同目录实验根的 runs 和 evaluation 承接。原历史结果全部保留，本次没有追加运行。
