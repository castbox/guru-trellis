# Guru Team 清晰技术写作规范 / Clear Technical Writing

本规范供当前输出 Agent、写作 owner、原范围审核 owner 和独立子 Agent 使用。准确表达优先于简短。中文采用清晰表达原则；英文有限参考下述 ASD-STE100 来源。

Use this specification when writing or changing natural language. Preserve meaning before shortening text. The Chinese guidance adapts clarity principles; the English guidance uses only the verified ASD-STE100 material listed below.

## 来源与采用边界 / Sources and adoption limits

英文参考版本为 **ASD-STE100 Simplified Technical English, Issue 9, 2025-01-15**。正式来源是 ASD Simplified Technical English Maintenance Group（STEMG）官网。以下公开页面已于 2026-10-17 核对；FAQ 的定位使用页面问题标题，不是标准条款编号。

The English reference is **ASD-STE100 Issue 9 (January 15, 2025)**. The official source is the ASD Simplified Technical English Maintenance Group. The public pages below were checked on October 17, 2026. FAQ question titles identify the verified material; they are not numbered clauses of the standard.

| 来源 / Source | 已核对内容 / Verified material | 本项目采用 / Project use |
| --- | --- | --- |
| [STEMG 首页](https://www.asd-ste100.org/) | Issue 9 的名称和发布日期 / Issue name and publication date | 固定英文参考版本 / Pin the English reference version |
| [About STE](https://www.asd-ste100.org/about_STE.html)：Today、How does STE work?、What's new in Issue 9 | 写作规则和受控词典是不同部分；可使用项目技术名词和动词 / Writing rules, controlled dictionary, and project technical terms | GTW-005 的术语一致原则；不声称实施完整词典 / Terminology consistency, without adopting the full dictionary |
| [FAQ](https://www.asd-ste100.org/STE_faq.html)：Who needs to write in STE? | STE 面向技术维护文档；其他场景可采用短句、单一主题和主动语态原则 / Maintenance-document scope; transferable clarity principles | GTW-002、GTW-011；适用范围和强度由本项目定义 / This project defines applicability and strength |
| 同一 FAQ：Do conditional clauses always need to precede the main clause? | 读者必须先知道的工作条件应置于操作前 / Put a necessary work condition before the step | GTW-004 的条件与结果关系 / Explicit conditions and results |
| 同一 FAQ：Why can't I use passive sentences? | 操作使用祈使句；描述中执行者未知时可用被动语态 / Imperative instructions; passive descriptions when the agent is unknown | GTW-003、GTW-011，保留未知执行者事实 / Clear instructions without inventing an actor |
| 同一 FAQ：What is ASD-STE100 Simplified Technical English (STE?) | 通用受控词的含义和词性一致；允许技术词汇 / Consistent meanings and parts of speech; technical terms | GTW-005 的项目术语原则 / Consistent project terminology |
| 同一 FAQ：Will STE change the meaning of technical texts? | 正确使用须保留含义，依赖技术和语言理解 / Preserve meaning through technical and linguistic understanding | GTW-001 的语义优先原则 / Meaning takes priority |
| 同一 FAQ：Is a language checking tool necessary to write in STE? | 工具不能替代标准；不为商业工具认证合规 / Tools do not replace the standard or establish certified compliance | GTW-010 的 AI 语义判断与机械检查边界 / Separate semantic review from mechanical checks |
| [Downloads](https://www.asd-ste100.org/STE_downloads.html) | 当前正式 PDF 通过申请表提供 / The current PDF is available by request | 说明未取得范围 / State what has not been obtained |

本次核对未取得完整 Issue 9 PDF、编号条款或完整词典，故不标为已采用。不得从旧版推断 Issue 9 条款，也不得把 FAQ 标题当作条款编号。GTW 编号是项目规则编号。会话范围、义务强度、literal、证据、加载与 owner 职责是项目规则，不是已经核对的 ASD 条款。

The full Issue 9 PDF, numbered clauses, and complete dictionary were not obtained or adopted in this work. Do not infer current clauses from older editions. GTW identifiers belong to this project. Rules for conversations, modality, literals, evidence, loading, and owners are project rules, not verified ASD clauses.

**不得宣称中文符合 ASD-STE100，也不得宣称英文已完整实施或取得 ASD-STE100 认证。** / **Do not claim ASD-STE100 compliance for Chinese, full implementation for English, or ASD-STE100 certification.**

## 内容范围 / Content scope

规则适用于 Agent 新写或修改的全部自然语言：会话回复、文档、workflow、skill、prompt、代码注释、面向用户的提示、Issue、PR、模板中的文字，以及 Agent 编写的程序提示文本。修改文件时，只检查本次变更及理解它所需的上下文。历史归档、旧证据和不可变版本不追溯润色。

Apply the rules to all natural language the Agent writes or changes: replies, documents, workflows, skills, prompts, code comments, user messages, Issues, PRs, template prose, and program prompts authored by the Agent. Review the changed text and the context needed to understand it. Do not rewrite historical archives, old evidence, or immutable versions for style.

用户明确指定的原文、格式和输出用途，以及既有功能和兼容合同，决定规则是否适用。保留准确表达；不得把写作偏好新增为业务条件。下表的逐规则例外与 GTW-007、GTW-008 共同适用。

Explicit user requirements for original text, format, and purpose, together with existing functional and compatibility contracts, determine applicability. Keep accurate wording. Do not turn a writing preference into a business condition. Apply each rule's exceptions together with GTW-007 and GTW-008.

## 稳定规则 / Stable rules

“强制 / Required”只在该规则的适用条件成立时要求修订。“建议 / Advisory”用于改善表达，不能单独成为阻塞条件。编号保持稳定，不按 ASD 条款编号解释。

Required rules apply only under their stated conditions. Advisory rules guide improvement and cannot alone block work. Keep GTW identifiers stable; they do not identify ASD clauses.

| 编号、强度 / ID and strength | 规则与适用内容 / Rule and applicable content | 例外 / Exceptions | 来源 / Basis |
| --- | --- | --- | --- |
| **GTW-001 强制 / Required** | 所有改写保留含义、义务强度、完整条件、否定、例外、顺序和兼容边界；不添加来源没有的事实。/ Preserve meaning, obligation strength, conditions, negation, exceptions, order, and compatibility limits in every rewrite. Do not add facts. | 无法简化而保持原意时，保留准确表达；经授权的功能修改按原变更合同执行，不伪装成等义润色。/ Keep accurate text if simplification loses meaning. Apply authorized functional changes under their original change contract. | 意义保留 FAQ 原则 + 项目语义要求 / Meaning-preservation principle plus project requirements |
| **GTW-002 强制 / Required** | 新写或修改的说明一句表达一个主要意思；将互不依赖的动作或事实分句。/ Express one main idea per sentence in new or changed explanations. Separate independent actions or facts. | 为准确表达同一主要意思所需的复合条件、因果关系、必要术语及限定可保留在同句；用户指定固定格式时保留格式。不为拆句丢失关联或精度。/ Keep combined conditions, causes, necessary terms, and qualifications together when they express one main idea accurately. Preserve user-required fixed formats. Do not lose relations or precision to split a sentence. | Who needs to write in STE? 的有限改编；强度由项目定义 / Limited adaptation; strength defined by this project |
| **GTW-003 强制 / Required** | 操作指令明确执行者、动作和对象，使读者能确定谁做什么。多 owner 时写出责任人。/ Make the actor, action, and object clear in instructions. Name the responsible owner when several owners participate. | 祈使句可省略明确的当前执行者；不适用于未知执行者的事实描述。不得猜测执行者。/ Imperatives may omit an unambiguous actor. Unknown actors in factual descriptions must remain unknown. | Why can't I use passive sentences? + 项目职责 / FAQ principle plus project ownership |
| **GTW-004 强制 / Required** | 条件行为写明触发条件及结果；执行前必须知道的条件放在动作前。/ State the trigger and result of conditional behavior. Put a condition needed before execution before the action. | 后置条件同样明确且不影响执行理解时可保留；纯描述无需改成条件句；保留 AND/OR 分组、否定和例外。/ A clear trailing condition may remain if it does not affect execution. Descriptions need no artificial condition. Preserve logical grouping, negation, and exceptions. | 条件 FAQ 原则 + 项目完整性 / Conditional-order principle plus completeness |
| **GTW-005 强制 / Required** | 同一概念使用同一术语，不同概念保留区别；项目用语见下表。/ Use one term consistently for a concept. Keep distinct concepts distinct. Use the project terms below. | 不改公共名称、引用或精确字面内容；解释同义词时可并列并明确对应。/ Preserve public names, quotations, and exact literals. Synonyms may be shown to explain their mapping. | About / What is ASD-STE100…? 的术语原则 + 项目术语 / Terminology principles plus project vocabulary |
| **GTW-006 强制 / Required** | 在要求、建议、事实、计划和未验证结论之间明确区分；结论限于证据覆盖范围。/ Distinguish requirements, advice, facts, plans, and unverified conclusions. Limit claims to the available evidence. | 不把引用中的原有强度改成项目要求；可使用同样清晰的其它措辞，无固定关键词门禁。/ Quoted modality does not become a project requirement. Equally clear wording is valid; no fixed keyword is required. | 项目规则 / Project rule |
| **GTW-007 强制 / Required** | 仅润色时保留命令、路径、代码标识符、schema 字段、公共 API 名称、typed exit 和精确匹配的接口消息；保留外部引用及用户指定原文、格式、用途。/ For style-only edits, preserve commands, paths, identifiers, schema fields, public API names, typed exits, exact interface messages, external quotations, and user-required text, format, and purpose. | 功能需求已授权修改接口或标识符时，按该需求及兼容合同修改；本规范不授权也不阻止该变更。脱敏呈现按 GTW-008。/ An authorized functional change follows its requirement and compatibility contract. This rule neither authorizes nor blocks that change. Apply GTW-008 to redaction. | 项目 literal 与用户合同 / Project literal and user contracts |
| **GTW-008 强制 / Required** | 原始日志和证据本体保持原样，新增说明遵守规则。呈现内容继续遵守脱敏、权限和敏感数据保护规则；脱敏摘录标明省略或替换，不回写原始本体。/ Preserve original logs and evidence. Apply these rules to new explanations. Follow existing redaction, permission, and sensitive-data rules. Label omissions or replacements in excerpts; do not write them back to the original evidence. | 保留本体不要求复制、公开或取得无权限的原始记录；脱敏摘录可不保留敏感字面内容。/ Preserving originals does not require copying, publishing, or accessing restricted records. Redacted excerpts may replace sensitive literals. | 项目证据与敏感数据边界 / Project evidence and sensitive-data boundaries |
| **GTW-009 强制 / Required** | 所有入口在首次实质输出前完整读取本规范；恢复和子 Agent 的适用条件见加载合同。/ Read this complete specification before the first substantive output through any entry. Follow the loading contract for resumed sessions and child Agents. | 完整读取前仅可给出短句加载进度或具体缺失诊断，明确动作或缺失项，不作未验证断言；读取失败时暂停受影响正文，恢复读取后继续原请求，无新增审批。/ Before loading, only brief loading progress or a specific missing-dependency diagnostic is allowed. State the action or missing item without unverified claims. Pause affected prose on failure; after a successful read, continue the same request without new approval. | 项目加载合同 / Project loading contract |
| **GTW-010 强制 / Required** | 写作 owner 输出前自检；审核 owner 在原审核范围内判断清晰度与语义。AI 负责判断，脚本只检查分发、引用、投影和已定义机械条件。/ Writers check their output. Reviewers assess clarity and meaning within their existing scope. AI makes semantic judgments; scripts check distribution, references, projections, and defined mechanical conditions. | 会话由当前 Agent 自检；同样清晰的表达或仅违反建议不阻塞。不新增通用语言审核 owner；保留原门禁范围与 typed exits。/ The current Agent checks replies. Equally clear wording or advice-only differences do not block. Add no general language-review owner; preserve existing gate scope and typed exits. | 工具 FAQ 原则 + 项目职责 / Tool principle plus project responsibilities |
| **GTW-011 建议 / Advisory** | 在不损失准确性的前提下使用短句、常用词和主动语态。/ Prefer short sentences, familiar words, and active voice when they preserve accuracy. | 术语、精确引用、未知执行者的被动描述、必要限定和用户格式可保留；不设强制句长或词表扫描门禁。/ Keep technical terms, exact quotations, passive descriptions with unknown actors, necessary qualifications, and required formats. No sentence-length or word-list scan is a compliance gate. | Who needs to write in STE? / Why can't I use passive sentences? 的有限改编 / Limited adaptation |
| **GTW-012 强制 / Required** | 保留当前仓库语言政策和用户明确语言要求。Guru Team 默认业务仓库的持久文档、任务人类可读内容及审查报告使用中文；公共扩展源码按既有分工可用英文或双语。/ Preserve repository language policy and explicit user language requirements. Guru Team defaults to Chinese for durable business-repository documents, human-readable task content, and review reports. Public extension sources may use English or both languages under their existing policy. | literal、外部引用、用户指定原文及既有源码语言分工保留；不因本规范统一改用英文或翻译历史内容。/ Preserve literals, quotations, user-required originals, and existing source-language divisions. This specification does not require switching to English or translating history. | 既有中文政策与项目适用边界 / Existing language policy and project scope |

## 项目术语 / Project terms

| 术语 / Term | 含义与边界 / Meaning and boundary |
| --- | --- |
| Task | 整体 accepted scope 的任务身份与生命周期；不能用一次切片交付替代整体完成。/ The identity and lifecycle for the whole accepted scope. One slice does not establish whole-task completion. |
| Delivery | Task 内一个选定的交付切片及其结果；Delivery 合并不等于 Task Completion。/ A selected delivery slice and its result within a Task. Its merge does not establish Task Completion. |
| Check | 对当前 task scope 的完整质量检查，由原 Check owner 执行。/ The complete quality check of current task scope, owned by the existing Check owner. |
| Review | 原审核 owner 针对其声明范围的独立语义审核；按具体用途写明 Branch Review、Delivery Review 等。/ An independent semantic assessment within the review owner's declared scope. Name the specific review when needed. |
| 强制 / Required | 适用条件成立时必须满足的要求；不能改写为可选。/ An obligation when applicable; do not rewrite it as optional. |
| 建议 / Advisory | 可改善表达的偏好；不是业务前置或独立阻塞理由。/ A preference that can improve wording; not a business prerequisite or an independent blocker. |
| literal | 需要精确保留的字面内容；其外部解释仍受本规范约束。/ Content that must remain exact; surrounding explanations still follow this specification. |

这些含义用于写作，不替代当前 workflow、Skill Interface 或业务需求中的权威定义。公共名称保持原字面，例如 `guru-review-contract-wording`、`passed`；不要为语言统一重命名它们。

These meanings guide writing and do not replace authoritative workflow, Skill Interface, or business definitions. Preserve public names such as `guru-review-contract-wording` and `passed` exactly.

## 加载与现有职责 / Loading and existing responsibilities

唯一 canonical 正文为 `trellis/presets/guru-team/spec/workflow/clear-technical-writing.md`，通过现有 managed-spec 安装到 `.trellis/spec/workflow/clear-technical-writing.md`。运行 Agent 读取安装正文。workflow、平台入口、Guru Skill 和 docs 只定位同一正文，不另写规则副本。

The canonical body is `trellis/presets/guru-team/spec/workflow/clear-technical-writing.md`. The existing managed-spec mechanism installs it at `.trellis/spec/workflow/clear-technical-writing.md`. Runtime Agents read the installed body. Workflows, platform entries, Guru Skills, and docs reference this body rather than maintain separate rules.

无 Task、正式 Task、task-free、独立 Git/GitHub 操作以及新建会话，均在首次实质输出前完整读取正文。实质输出包括需求、方案、代码说明、审查结论、Issue、PR 和任务答复正文。读取前，进度或缺失提示只使用短句，说明当前动作或具体缺失项，不作未验证结论，也不声称已执行完整规范。

For sessions without a Task, formal Tasks, task-free work, independent Git/GitHub operations, and new sessions, read the full body before substantive output. Such output includes requirements, plans, code explanations, review conclusions, Issues, PRs, and task answers. Before loading, use only brief progress or missing-item messages. State the current action or exact missing item. Do not make unverified claims or claim to have applied the full specification.

恢复或上下文压缩后，确认完整且当前的正文仍可用；若丢失、截断、版本不确定或仅保留摘要，在生成正文前重新读取。子 Agent 不假设继承主会话内容：只有可确认完整且未截断的原生注入可直接使用；未注入、截断或不确定时，由子 Agent 自行完整读取安装路径。dispatch 与实际 Task context manifest 引用同一安装正文，不用复制全文替代加载。

After resume or context compaction, confirm that the complete current body remains available. Reread it before substantive output if it was lost, truncated, reduced to a summary, or is of uncertain version. Child Agents must not assume inheritance. They may use verified complete, untruncated native injection. Otherwise, they must read the full installed file themselves. Dispatch and applicable Task context manifests reference the same installed body.

文件缺失或读取失败时，仅报告具体缺口，暂停依赖该规范的实质文本。通过原安装或恢复路径修复后，完整读取并继续原请求；此恢复不新增审批。已有 Git/GitHub 副作用和业务权限规则继续由原 owner 执行。

If the file is missing or cannot be read, report the specific gap and pause affected substantive text. After recovery through the existing installation or recovery path, read the whole file and continue the original request. This recovery adds no approval step. Existing Git/GitHub side-effect and business-permission rules remain with their original owners.

写作 owner 输出前比较改写与原需求、证据和用途。审核 owner 只审其原有范围：歧义改变行为、遗漏必要条件或弱化义务，按 correctness 问题处理；违反适用强制规则时要求修订。仅建议差异或另一种同样清晰的表达不构成阻塞 finding。`guru-review-contract-wording` 的固定范围、前置条件和 typed exits 保持不变，不承担通用语言审核。

Before output, the writer compares the text with the original requirements, evidence, and purpose. Reviewers stay within their existing scope. Treat ambiguity that changes behavior, missing conditions, or weakened obligations as correctness issues. Require revision for an applicable required-rule violation. Advice-only differences and equally clear alternatives are not blocking findings. Keep the fixed scope, preconditions, and typed exits of `guru-review-contract-wording`; it is not a general language reviewer.

AI 判断语义与清晰度，句长、关键词和扫描结果不能独立证明合规。安装投影一致也不能证明 Agent 实际读取或写作行为。源码修改不代表已有安装已更新；已有项目按匹配版本更新 workflow 并 reapply 完整 preset，沿原机制保留用户指令、处理冲突及 `.new`/`.bak`，再验证实际安装。

AI assesses meaning and clarity. Sentence length, keywords, and scans cannot establish compliance alone. Projection parity does not prove actual loading or writing behavior. A source change does not update an existing installation. Existing projects use matching workflow and full-preset reapply paths, preserve user instructions, resolve conflicts and `.new`/`.bak` through existing mechanisms, and verify the installed result.

## 双语示例与逐例理由 / Bilingual examples and reasons

每例先给出业务或证据前提。反例是该前提下应修订的表达；正例不新增事实、权限或前置条件。“建议”示例只说明可读性改进，不把原表达列为阻塞。

Each example states its requirement or evidence first. The poor wording needs revision only under that premise. The clear wording adds no fact, permission, or prerequisite. Advisory examples show readability improvements and do not establish blockers.

### E1 指令 / Instructions — GTW-003、GTW-011

前提 / Premise：执行者是 installer，写入对象是目标安装文件。/ The installer writes the target installation file.

- 反例 / Poor：进行相关内容的处理。/ The relevant content is to be handled.
- 正例 / Clear：installer 将规范安装到 `.trellis/spec/workflow/clear-technical-writing.md`。/ The installer installs the specification at `.trellis/spec/workflow/clear-technical-writing.md`.
- 理由 / Reason：指明已有执行者、动作和对象，没有增加步骤。执行者明确时也可写“读取安装文件。/ Read the installed file.”，无需重复 actor。/ Names the known actor, action, and object without adding a step. An imperative may omit an unambiguous actor.

### E2 条件与结果 / Conditions and results — GTW-004

前提 / Premise：规范缺失时暂停正文；文件可读时完整读取后继续。/ Pause substantive text when the specification is missing. Read the complete file before continuing when it is available.

- 反例 / Poor：继续写正文，文件缺失时再处理。/ Continue writing and handle the missing file later.
- 正例 / Clear：如果规范文件缺失，报告缺失路径并暂停正文。文件恢复后，完整读取，再继续原请求。/ If the specification is missing, report its path and pause substantive text. After recovery, read the full file, then continue the original request.
- 理由 / Reason：将执行前必须知道的条件放在前面，并保留暂停和恢复顺序；没有增加确认步骤。/ Places the necessary condition before execution and preserves pause and recovery order without adding confirmation.

### E3 术语 / Terminology — GTW-005

前提 / Premise：某 Delivery 已合并，Task Completion 尚未审核。/ A Delivery has merged; Task Completion has not been reviewed.

- 反例 / Poor：任务交付完成，所以 Task 已完成。/ The delivery is done, so the Task is complete.
- 正例 / Clear：Delivery 已合并。Task Completion 尚未审核。/ The Delivery has merged. Task Completion has not been reviewed.
- 理由 / Reason：保留切片结果与整体完成的区别，不把合并事实扩张为未发生的审核。Check 和 Review 也不能互换。/ Keeps the slice result distinct from whole-task completion. A merge does not imply an unperformed review; Check and Review are also distinct.

### E4 要求与建议 / Requirements and advice — GTW-006、GTW-011

前提 / Premise：保留完整条件是强制要求；短句只是建议。/ Complete conditions are required; short sentences are advisory.

- 反例 / Poor：建议保留条件；长句必须拆分才可通过。/ You may keep the conditions; every long sentence must be split to pass.
- 正例 / Clear：必须保留完整条件。建议在不损失条件关系时使用短句。/ Preserve every required condition. Prefer short sentences when they retain the relationship between conditions.
- 理由 / Reason：恢复已有义务强度；不把句长偏好升级为 gate。没有固定字数阈值。/ Restores obligation strength without turning sentence length into a gate. No word-count limit is implied.

### E5 事实、计划与未验证结论 / Facts, plans, and unverified claims — GTW-001、GTW-006

前提 / Premise：仅源码检查通过；计划下一步做安装验证；实际平台行为未验证。/ Source checks passed. Installation validation is planned next. Actual platform behavior is unverified.

- 反例 / Poor：所有平台已可用。/ All platforms work.
- 正例 / Clear：源码检查通过。下一步计划验证安装。实际平台行为尚未验证。/ Source checks passed. Installation validation is planned next. Actual platform behavior remains unverified.
- 理由 / Reason：分别说明已知事实、后续计划和证据边界，不以静态结果替代行为证明。/ Separates facts, plans, and evidence limits. Static checks do not establish behavior.

### E6 复合条件、否定与例外 / Combined conditions, negation, and exceptions — GTW-001、GTW-004

前提 / Premise：只有 A、B 都满足才执行 X；出现 C 时不得执行，D 是 C 的明确例外。A/B/C/D 是既有条件标签。/ Run X only when both A and B hold. Do not run it when C holds, except when D applies. A/B/C/D label existing conditions.

- 反例 / Poor：A 或 B 满足即可执行 X。/ Run X when A or B holds.
- 正例 / Clear：仅当 A 和 B 都满足，且满足“C 不成立或 D 例外适用”这一条件时，执行 X。/ Run X only when A and B both hold and either C does not hold or exception D applies.
- 理由 / Reason：保留 `A AND B AND (NOT C OR D)`。反例改变 AND、删除否定和例外。正例可保留为一句，不能为拆句改变分组。/ Preserves the complete logical relation. The poor wording changes AND to OR and drops negation and exception. One sentence is appropriate here.

### E7 执行顺序 / Execution order — GTW-001、GTW-002

前提 / Premise：必须先读取原始记录，再生成脱敏摘录，最后输出说明。/ First read the original record, then create a redacted excerpt, then output the explanation.

- 反例 / Poor：输出说明后读取记录并脱敏。/ Output the explanation, then read and redact the record.
- 正例 / Clear：先读取原始记录，再生成脱敏摘录。最后输出说明。/ Read the original record first. Then create a redacted excerpt. Output the explanation last.
- 理由 / Reason：按原顺序拆句；不把顺序依赖改为可并行步骤。/ Splits the steps while preserving order; no parallel execution is implied.

### E8 字面保留与授权功能修改 / Literals and authorized functional changes — GTW-001、GTW-007

前提 / Premise：仅润色时须保留 `passed`。另一个功能需求已明确授权将字段 `old_name` 改为 `new_name`，并保留其原兼容计划。/ A style-only edit must retain `passed`. A separate functional requirement authorizes renaming `old_name` to `new_name` under its existing compatibility plan.

- 反例 / Poor：为统一中文，将 `passed` 改为“通过”；写作规范禁止字段重命名。/ Translate `passed` for consistency; the writing specification forbids the field rename.
- 正例 / Clear：仅润色时保留 `passed`。按已授权功能需求及原兼容计划，将 `old_name` 改为 `new_name`。/ Retain `passed` in style-only edits. Rename `old_name` to `new_name` under the authorized functional requirement and its compatibility plan.
- 理由 / Reason：前者保护接口字面值；后者由功能需求授权。本规范既不阻止已授权变更，也不新增授权。/ Protects the literal for style edits while leaving functional authority and compatibility with their original contract.

### E9 用户原文、格式与用途 / User originals, format, and purpose — GTW-007、GTW-012

前提 / Premise：用户要求仅返回一行原文“Task / Delivery”，供精确匹配。/ The user requests exactly one line, `Task / Delivery`, for exact matching.

- 反例 / Poor：任务和交付是不同概念。/ A Task and a Delivery are different concepts.
- 正例 / Clear：`Task / Delivery`（实际输出仅含该行文字，不添加反引号或解释。）/ `Task / Delivery` (The actual output contains only that line, without backticks or explanation.)
- 理由 / Reason：示例注释不进入实际输出。用户的字面和格式要求适用；不能因清晰度建议新增说明或翻译。/ The explanatory note is not part of the requested output. Do not add explanation or translation where exact text and format are required.

### E10 原始证据与脱敏摘录 / Original evidence and redacted excerpts — GTW-007、GTW-008

前提 / Premise：原记录含敏感值，只允许对外展示脱敏摘录。以下全部为示例占位内容，不是真实敏感记录。/ The original contains sensitive values; only a redacted excerpt may be shared. All content here is illustrative placeholder text.

- 反例 / Poor：为保留原文，对外复制全部原始记录；再把脱敏文字写回本体。/ Publish the full original to preserve its wording, then replace the original with the redacted text.
- 正例 / Clear：脱敏摘录：`request_id=[已替换 / REDACTED] … [已省略 / OMITTED]`。原始证据本体保持原样，不在此公开。/ Redacted excerpt: `request_id=[REDACTED] … [OMITTED]`. Preserve the original evidence without publishing it here.
- 理由 / Reason：明确摘录中的替换和省略，避免误称逐字原始证据；保留本体不等于公开本体。/ Labels replacements and omissions. The excerpt is not presented as verbatim original evidence. Preservation does not require publication.

### E11 准确性与被动语态 / Accuracy and passive voice — GTW-002、GTW-003、GTW-011

前提 / Premise：事实只有“文件已删除”，执行者未知；用户需要准确状态。/ The only known fact is that the file was deleted. The actor is unknown; the user needs an accurate status.

- 反例 / Poor：Agent 已删除文件。/ The Agent deleted the file.
- 正例 / Clear：文件已删除。执行者未知。/ The file was deleted. The actor is unknown.
- 理由 / Reason：为改主动语态而猜测 actor 会新增事实。描述中的被动语态适用，不违反操作指令规则。复杂但准确的句子也不能仅因长度被阻塞。/ Active voice would invent an actor. Passive voice is appropriate in this description. An accurate complex sentence cannot be blocked for length alone.

### E12 加载、恢复与审核职责 / Loading, recovery, and review ownership — GTW-009、GTW-010

前提 / Premise：安装正文当前缺失；恢复后可完整读取；尚未开始实质写作。/ The installed body is missing. It can be read in full after recovery. Substantive writing has not started.

- 反例 / Poor：规范已执行，方案如下……恢复后请重新批准写作。/ The specification is applied; here is the plan… Approve writing again after recovery.
- 正例 / Clear：缺少 `.trellis/spec/workflow/clear-technical-writing.md`，暂停方案正文。恢复并完整读取后，继续原请求。/ `.trellis/spec/workflow/clear-technical-writing.md` is missing. Pause the plan text. After recovery and a complete read, continue the original request.
- 理由 / Reason：缺失诊断不假称已读，不提前写正文，不新增审批。写作 Agent 负责自检；原审核 owner 不因本规范扩大范围或改变 typed exits。/ Reports the gap without claiming a read, generating substantive text, or adding approval. Writing and review remain with their existing owners and scope.

### E13 单一主要意思 / One main idea — GTW-002

前提 / Premise：源码检查通过；另一件独立事实是某文档仍待修订，两者没有因果或执行依赖。/ Source checks passed. An unrelated document still needs revision. These facts have no causal or execution dependency.

- 反例 / Poor：源码检查通过且另一文档待修订。/ Source checks passed and an unrelated document needs revision.
- 正例 / Clear：源码检查通过。另一文档仍待修订。/ Source checks passed. The other document still needs revision.
- 理由 / Reason：将互不依赖的事实分句，保持两项状态。E6 的复合条件共同定义同一动作，属于明确例外；不能为执行本规则改变条件关系。/ Separates independent facts without changing either status. The combined conditions in E6 define one action and fit the stated exception. Splitting must not change their relationship.
