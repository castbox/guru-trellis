# #147 Guru Skill 行为评测合同、Runner 与跨 Agent Adapter 基础设施

## 1. 目标

建立版本化、package-local、跨 Agent 共用的 Guru Skill 行为评测基础设施，使评测系统能够从 Interface 1.3 发现并实际执行 public invocation，识别 actual typed exit，按对应的 per-exit output schema 和确定性断言验证行为，同时把 semantic judgment 与 human feedback 留在独立边界。

本任务只交付横向基础设施与 representative semantic/deterministic packages，不迁移九个 production Skills，也不完成 active Skill coverage closure。

## 2. 权威来源

- 产品需求：GitHub issue <https://github.com/castbox/guru-trellis/issues/147>，当前无评论冲突。
- 直接前置：closed #144 交付的 `guru-team-skill-interface-1.3`、exact public invocation、per-exit output schema、consumer contract 与 public/private 边界。
- Durable contract：`.trellis/spec/workflow/skill-package-contract.md`。
- 仓库约束：`AGENTS.md`，包括 Markdown/AI 判断与确定性脚本分层、honest-but-fallible 场景边界、canonical/dogfood/platform 同步及安装升级门禁。
- 官方扩展边界：Trellis custom workflow 与 spec template marketplace 文档；本任务不修改 Trellis upstream、全局 npm 或 `node_modules`。
- 参考而非兼容目标：`castbox/guru-codex-plugin-skill-factory` 的 `resources/skill/skill-evals.schema.json` 与 package-local `evals/evals.json`。
- Issue 处置：`issue-scope-ledger.json`，Close 仅 #147；Related 为 #127、#125、#130；Follow-up 为 #145、#146。

## 3. 当前差距

当前仓库已能发现 Interface 1.3 public contract，并通过 representative wrappers 实际验证单次 public invocation，但没有以下能力：

1. package-local、版本化、closed 的 eval corpus schema；
2. 面向 eval corpus 的稳定 discovery/run public commands；
3. actual typed exit、per-exit schema 与 case assertions 的统一运行结果；
4. deterministic assertions、semantic assertions 与 human feedback 的独立边界；
5. shared、Codex、Claude Code、Cursor 四个薄 adapter；
6. package/repo tracked tree 之外的临时 transcript、grading、timing、comparison 与 feedback evidence；
7. source/installed/dogfood/platform/throwaway/update-reapply 的完整 eval 分发门禁。

Factory 现有 schema 接受 integer id、`expectations` 字符串和未知字段，只验证结构与数量，不能直接作为 Guru 公共合同。

## 4. 功能需求

### R1. Eval corpus 身份与位置

- Canonical corpus 路径固定为 Skill root 下的 `evals/evals.json`。
- 新 schema 使用独立稳定 id 和 `schema_version`；顶层必须包含 exact `skill_name` 与非空 `evals[]`。
- Case `id` 必须是 package 内唯一且稳定的字符串，不得依赖数组下标或排序。
- Schema 与 runtime 对未知字段、`null`、重复 id 和版本/skill identity mismatch fail closed。

### R2. Case 输入与 expected contract

- 每个 case 必须声明 `id`、`prompt`、`expected_exit` 和人类可读 `expected_output`。
- `expected_output` 不参与自动 pass/fail。
- Case 声明 `input_profile_id` 时，该值必须 exact-ref Interface 1.3 拥有的 structured profile id；case 不复制 profile schema。
- `files` 只有非空时才出现；每个路径必须是 normalized Skill-root-relative 路径，且目标 regular file 位于 package 的 `evals/files/` 下。
- `assertions` 只有非空时才出现，并在结构上分离 deterministic 与 semantic assertions。

### R3. Assertion 与 legacy migration

- Deterministic assertion kind 使用 closed discriminator，首批覆盖 JSON value/path、schema/exit invariant、file outcome 与 public-invocation trace invariant；任意表达式或脚本一律拒绝。
- Semantic assertion 只声明待审查标准和 evidence selector，不得由 Python/shell 生成 pass。
- Human feedback 是独立输入/结果，不得伪装成 deterministic assertion。
- Canonical writer 只写 `assertions`。Legacy `expectations` 仅作为单向 adapter/migration test 的输入；canonical corpus 同时出现 `assertions` 与 `expectations` 必须失败。

### R4. Eval discovery public command

- Extension public API 注册 exact `discover-skill-evals` command，并提供 source/installed stable help。
- Discovery 必须先验证 registry、Interface、package、corpus schema、case identity、fixture path 和 assertion refs，再返回 closed discovery DTO。
- 无 corpus、legacy Skill、未知 Skill、版本 mismatch、缺失 fixture 与 installed drift 返回稳定 `code`、`field_path`、`remediation`。

### R5. Eval run public command

- Extension public API 注册 exact `run-skill-evals` command，并提供 source/installed stable help。
- Runner 必须从 Interface 1.3 解析 exact public invocation、input profile、declared exits 与 per-exit output schema；case 不携带 schema path、consumer projection 或 private artifact locator。
- 每个 case 必须实际执行 public invocation。只检查 JSON shape、case 数量、static example 或 fixture 文件存在不构成通过。
- Runner 独立记录 actual typed exit；以 `expected_exit` 选择对应 output schema 并验证 stdout DTO。
- Runner 不读取/import `guru_team_trellis.py` 或其它 private runtime source 来构造 public input 或解释 public output；它只调用已发布 wrapper/command。

### R6. 运行状态与错误分类

- Run status 闭集为 `passed`、`evaluation_failed`、`execution_error`、`unsupported`。
- Behavior mismatch、断言失败或缺少必需的外部 semantic grading 归入 `evaluation_failed`。
- Adapter/CLI 启动失败、无合法 typed output 或 runner 自身执行失败归入 `execution_error`。
- 平台不具备声明能力时返回 `unsupported`，不得改写 corpus 或跳过要求来伪造通过。
- 预期 refresh、re-entry、blocked 或 stop exit 在 exit/schema/assertions 全部通过时返回 `passed`，不得被归类为基础设施失败。

### R7. Grader 边界

- JSON/schema/exit/files/public-invocation assertions 由 deterministic grader 机械判定。
- Semantic assertion 结果必须来自显式 semantic grader 或 human review 输入；runner 只校验、绑定和汇总外部结果，不生成 semantic pass。
- 缺失、重复、未知、case/assertion identity mismatch 或不完整的 semantic result fail closed。
- Human feedback 与 semantic grading 分开记录；feedback 本身不得覆盖 deterministic failure。

### R8. 四个薄 Adapter

- 提供 `shared`、`codex`、`claude`、`cursor` 四个稳定 adapter id。
- Adapter 只负责创建隔离 execution context、加载指定 Skill、传递 prompt/files、收集 public output 和 trace。
- Adapter 不复制 Skill 行为、corpus、Interface schema、consumer projection、semantic judgment 或 grader policy。
- 四个 adapter 必须消费同一 canonical corpus bytes；byte identity mismatch 直接失败。
- Native CLI 不可用或能力不支持时返回 `unsupported`。

### R9. Comparison mode

- 新 Skill comparison 接受 caller 已解析的 with-skill/without-skill exact package identity。
- 既有 Skill comparison 接受 caller 已解析的 current/comparison exact package identity。
- 两个 package 参数必须成对出现；runner 不解释 `latest`、`previous`、branch、tag 或其它浮动 ref。
- Comparison 共享同一 corpus bytes 和 assertion contract，结果保持两侧执行/grade/timing 可区分。

### R10. Runner evidence

- 单次运行的所有可写结果必须位于显式隔离临时 workspace，且该 workspace 位于 package/repo tracked tree 之外。
- Closed evidence 仅记录排障和比较需要的 case id、corpus/schema version、Skill/Interface version、platform、adapter、comparison version、actual exit、assertion results、run status、transcript locator、timing 和 feedback。
- Evidence 不是 public Skill I/O、typed handoff、gate artifact、checkpoint、审计链或发布证明；不得新增 eval 专用签名、checksum、provenance、release 或防伪字段。

### R11. 正常运行零影响

- 正常 workflow/standalone invocation 不读取 `evals/evals.json`、eval fixtures、adapter descriptors 或 runner evidence。
- Eval corpus 不进入 prompt context，也不增加普通 Skill invocation 的 runtime payload。
- Production Skill 的 public I/O、typed exits、consumer route 与现有九个 `legacy` 状态保持不变。

### R12. 分发、文档与升级

- Canonical schema、runtime commands、adapters、representative fixtures、tests 与 extension inventory 先在 `trellis/` 下实现。
- Preset 安装到 `.trellis/guru-team/`，并把含 corpus 的 package byte-identical 分发到 shared、Codex、Claude、Cursor selected-platform roots。
- 同步 dogfood 安装副本；执行 preset apply 和 overlay drift 检查。
- Durable spec、requirements docs、workflow/preset/root README 必须同步 eval contract、public commands、边界、验证命令和 #145/#146 migration 关系。
- Fresh install、`trellis update`、preset reapply 后必须重新通过 source/installed/eval/platform checks，最终递归扫描无 `.new`/`.bak`。

## 5. 场景矩阵

### 5.1 必须通过

- Semantic representative package：normal case 与 refresh/re-entry/blocked family case。
- Deterministic representative package：normal case 与 blocked/refresh family case。
- Expected non-success exit 与 actual exit 一致，且 schema/assertions 通过。
- 四 adapter 对相同 corpus bytes 的 normal execution；缺少 native CLI 时为 `unsupported`。
- 具有完整外部 semantic grading 的 semantic case。
- Explicit comparison package pair。
- Legacy `expectations` 单向读取/迁移 test，不写入 canonical corpus。

### 5.2 必须拒绝

- 未知字段/assertion kind、`null`、重复或不稳定 id、空 `evals[]`。
- 绝对/越界/非 normalized file path、`evals/files/` 外目标、缺失或 symlink fixture。
- 未知 input profile、expected exit 或 output schema；case 自带 schema/private locator。
- Canonical corpus 使用 `expectations` 或同时出现 `expectations`/`assertions`。
- Adapter corpus bytes 不一致、平台 fork、漏传 prompt/files 或改写 expected contract。
- Semantic assertion 无外部 grading 却声明 pass；human feedback 覆盖 deterministic failure。
- 浮动 comparison ref、单边 comparison package、repo 内 evidence workspace。
- 普通 invocation 读取 eval corpus/private runtime source。

## 6. 非功能与安全边界

- 只处理 honest-but-fallible 正常执行、普通错误、stale/mismatch、平台兼容和行为回归。
- 不增加恶意 actor、对抗性输入、anti-tamper、防伪、锁、TOCTOU、压力、额外 fault injection、crash consistency 或跨 OS 原子性机制和测试。
- 输出和 fixture 不得包含 secret、token、private key、`.env`、signed URL、客户数据或敏感原始记录。
- Wrapper 保持薄；shared runtime 只执行确定性 parsing、validation、dispatch、grading aggregation 与 evidence serialization。

## 7. Issue 处置与非目标

### 7.1 Issue 处置

- Close：#147。
- Related：#127、#125、#130，只保留引用。
- Follow-up：#145、#146，不在本任务迁移或关闭。

### 7.2 非目标

- 不迁移任何 production Skill public I/O 或业务 payload。
- 不为九个 active Skills 编写完整 corpus 或 coverage manifest。
- 不把 evals 当作 public input/output schema、consumer projection、gate artifact、checkpoint 或审计记录。
- 不替代 Interface、per-exit schema/example、recorder、validator、executor 或 unit tests。
- 不采用 factory 的 `codex-skill-package-v1`、release notes、checksum 或 provenance 字段。
- 不要求四个平台使用同一个原生 eval engine；统一的是 corpus、adapter protocol 和 Guru runner contract。
- 不修改 Trellis upstream、全局 npm 包或 `node_modules`。

## 8. Docs 状态

- Docs state：`complete_docs`。
- Strategy：`ssot_first`。
- Requirements impact：本任务新增长期的 eval schema、public commands、adapter protocol、evidence boundary、distribution 与 upgrade contract，必须同步 durable spec、requirements docs 和 public README。
- 权威 Docs SSOT Plan：`design.md` 的“Docs SSOT Plan”章节。

## 9. 验收标准

- [ ] AC1：Closed eval schema 固定 package-local path、version、string case id、required fields、optional non-empty fields 和 unknown/null rejection。
- [ ] AC2：Input profile、expected exit、files 与 assertions 都 exact-ref Interface/package ownership，所有 path 负例有稳定 error code/field path/remediation。
- [ ] AC3：Canonical `assertions`、legacy `expectations` 单向 migration、deterministic/semantic/human 三类边界均有正负例。
- [ ] AC4：`discover-skill-evals` 与 `run-skill-evals` 进入 extension public API、wrapper inventory、stable help 和 source/installed validation。
- [ ] AC5：Runner 对每个 case 实际调用 Interface 1.3 public invocation，记录 actual exit，并使用该 exit 独立 output schema 复验。
- [ ] AC6：Run status 准确区分 behavior failure、execution failure、unsupported；预期 refresh/re-entry/blocked/stop 不被误判。
- [ ] AC7：Deterministic grader 不做 semantic judgment；semantic pass 只能来自绑定完整的外部 grader/human review 输入。
- [ ] AC8：Shared、Codex、Claude、Cursor adapter 保持薄且执行 byte-identical corpus；平台 fork 被拒绝。
- [ ] AC9：Comparison 只接受 caller-resolved exact package pair，不解析浮动 refs。
- [ ] AC10：Runner evidence 仅写 repo/package 外临时 workspace，字段闭集不包含 public handoff、gate/checkpoint、审计或发布链信息。
- [ ] AC11：Normal workflow/standalone transcript 与 runner trace 证明普通 invocation 不加载 evals，公开调用不读取/import private runtime source。
- [ ] AC12：Representative semantic/deterministic packages 均覆盖 normal 与 refresh/re-entry/blocked family；production Skills 与 active coverage 不迁移。
- [ ] AC13：Canonical、installed、dogfood、shared/Codex/Claude/Cursor copies 的 corpus/schema/wrapper bytes 与 executable mode 一致。
- [ ] AC14：Targeted unit/integration/negative tests、source/installed validation、preset apply、dogfood drift、clean throwaway install/update/reapply 全部通过。
- [ ] AC15：最终递归扫描无 `.new`/`.bak`，README 命令可执行且不依赖本机隐藏状态。

## 10. 完成条件

只有 AC1-AC15 全部获得测试或命令证据，Phase 2 semantic check 无未解决 finding，Docs SSOT reconciliation 完成，Branch Review 覆盖 `origin/main...HEAD` 完整 diff，PR readiness 仍只关闭 #147 时，本任务才可进入 finish/publish。
