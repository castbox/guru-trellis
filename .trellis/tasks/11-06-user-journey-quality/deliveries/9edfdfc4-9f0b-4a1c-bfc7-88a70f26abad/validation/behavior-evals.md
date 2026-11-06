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
