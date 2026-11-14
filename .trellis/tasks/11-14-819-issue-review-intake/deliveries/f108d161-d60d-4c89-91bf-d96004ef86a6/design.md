# D1 Issue 审核评论与 Intake 分流设计

## 1. 设计目标、需求承接与内容基线

本批覆盖本目录 PRD 的 D1-R1–R7、D1-SC01–07 和整体 R1–R7。评论生产、已有 Issue 复核和三个局部返回共同交付；没有前序 Delivery。开发基线 B=4f2adef1f7b099f78bb8429e8b8facd66dce3bfc，来源为本 Task 明确选择的 origin/main；Planning H0 同 B。B 是后续内容范围起点，PR target=main 是集成目标，二者不随无关目标前进相互替代。

当前架构来源为 docs/architecture/README.md（guru-trellis-architecture / active）、00-foundation/design-constitution.md（guru-trellis-design-constitution-v1 / current）和 06-governance/change-contract.md。独立 candidate_assessment 实际返回 baseline_current、architecture_impact、target_native，decision_refs=[ADR-ISSUE-REVIEW-INTAKE]。它要求真实隔离贡献和 ADR；不代表 final_plan、实施、安装或外部验收通过。整体 accepted_scope 及本批 key 以 PRD 第1节和公开 Delivery 记录为准。

## 2. 当前系统、边界与目标差额

现有 selector→Sync→Discovery→Clarify→Wording→Readiness 只允许本轮完整链。Readiness current_issue 的 invoke/runtime 要求 wording_current transition；ready 输出复制完整 context/clarity/wording digest 及 target。Discovery 和 Clarify 的普通出口默认继续下一审核，无法合法完成局部返回。Create Issue 已有 issue attempt marker、正式内容读回与 recover，但没有评论动作；created 只有 repo_ref/number/url。Clarify 已有 AI-owned repo-bound gh source_actions 和 readback，能写 Issue/comment。

目标是在原 workflow 加一个薄入口分流：Sync 后已有 Issue 先进入原 Readiness；其他标准对象继续完整链。Readiness 亲自读取当前依据，直接 ready 或请求最早缺口。局部原 owners 完成后交回同次复核。Create 顺序扩展到评论读回后才 created；Clarify 在实际获准发布/修订路径写准确评论。历史自然语言评论同样可采用。Task identity、checkout/acquisition、scope接受、Delivery及其后续门禁不变。

实现源为 trellis/skills/guru-team/packages、trellis/workflows/guru-team、trellis/presets/guru-team；安装投影不是唯一源头。不修改上游 Trellis、全局包、node_modules、hooks 或 Task 生命周期模型，不新增复核 Skill、长期 coverage ledger、固定审核资格或期限。

## 3. 来源设计处置（唯一）

| 来源/承诺 | 处置与本批落点 | 理由、影响及上游处置 |
| --- | --- | --- |
| SRC819 行为一：Create 完整草稿审核→创建→正式内容读回→评论 | retain；§4评论owner、§6.3、§7恢复 | 评论完成属于原创建结果，不能提前 created。输入显式迁移，不复制草稿 pass 为正式 Issue pass。 |
| SRC819 行为一：Clarify准确覆盖、只读不写、共用正文 | retain；§4、§5.4、§6.4 | 复用原 source_actions；不新增第二评论执行器或评论审核authority。 |
| SRC819 行为二：Sync后原Readiness六类分叉 | retain；§5.1–5.3、§6.1 | 原 semantic owner 作路线判断；新profile不要求伪造前序transition。 |
| SRC819 局部返回与多缺口顺序 | retain；§5.2、§6.2 | 每次回同Issue/base/continuation；只补最早仍必要项，不自动串剩余链。 |
| SRC819 基线失效及适用性 | retain；§6.1、§7 | 原Sync刷新只用于真实基线失效；丢失调用期材料先恢复原读取，不以换Agent/时间/无关HEAD判失效。 |
| SRC819 无Issue、草稿/仅创建终点、no_issue | retain；§5.3、§6.5 | 完整草稿方法和原no_issue保持；创建并开工消费正式对象和实际评论。 |
| SRC819 公共I/O、恢复及分发 | retain；§5、§7–8 | 新profile/出口与真实consumer同批直接迁移，原owner恢复；不开长期兼容层。 |
| 当前 workflow Phase0及原Readiness receipts前置 | change，仅已有Issue先行及局部profile；完整链、资格确认路径仍保其本来用途 | 它是本项明确改变的原机制。MIGRATION-819说明适用边界，RDT原owner窄替代命中条件；不改旧历史。 |
| #692 local-fix-intake R692-02 / BEH692-REUSE、D692-01 / CON692-OWNERS | retain事实适用性、原调查/诊断方法；change固定全链限制 | 事实复用不是新放行凭证；真实完整current由原RDT整合，见implement唯一Docs Plan。 |
| #818 issue-content完整内容方法 | retain；两生产者与各审核owner继续读原正文 | 新评论规则独立于完整Issue内容方法，不重复或削弱其正文要求。 |
| Architecture change contract / subtraction-first | retain；§7及隔离贡献 | 原owner、九concerns、单写、直接迁移与一次提交后独立Review保持。不需要额外需求选择。 |
| 当前Create Task SKILL、public-delivery-task-creation-input-2.0、共享task-creation-input-3.0及MIGRATION-813 | retain；§5.1、§5.3、§7及V819-01/02/06 | 新路径须承接真实来源类型、精确commit、独立集成目标及原创建/恢复条件。旧1.0 schema仅为历史验证资产，不作为本批consumer依据；不重做#813的实现。 |

## 4. 模块、职责与设计取舍

1. **workflow及routing**：trellis/workflows/guru-team/workflow.md、references/routing.md 与对应graph/Interface声明拥有显式调用和唯一consumer。增加 `guru-issue-intake-base-router`（薄router，不是Skill）：只按caller已经确定的对象kind分支。已有Issue进入原Readiness；draft/standalone进入原Discovery；已有资格确认context_request仍回原Discovery。同步两README和真实受影响平台launcher的入口描述，入口不复制审核算法。
2. **Readiness**：guru-review-change-request 新 `existing_issue_intake` 和 `issue_review_return`。AI对完整live标题/正文、有效讨论/评论、必要前置交付及相关代码差额作当前判断，选择§5出口。原record/check只保存其相邻invoke所需最小结论和客观对象事实；不检查“是否已跑本轮全链”来代替覆盖判断。current_issue/proposed_draft/standalone_request原完整方法保留。
3. **局部owners**：Discovery、Clarify、Wording各增加 `issue_readiness_supplement` profile，调用自己原完整适用方法；缺口只指定本次目的，不能让它们跳过必要事实或完整正文一致性。局部成功唯一回Readiness，不落普通默认consumer。Clarify仍拥有需求、source角色、独立交付单位及必要选择；Wording不作产品选择。
4. **评论正文**：在原Clarify package的 references/issue-review-comment.md 单写可复用规则，Create/Clarify引用它。正文只写实际对象/范围、结论、影响开工的未决项/前置，基线仅在相关时说明；无固定模板或机器pass标识要求。旧清楚评论无需重写。
5. **评论副作用**：Create原runtime执行自己的创建后POST/readback；Clarify复用原source_actions中的repo-bound gh动作，不引入新持久执行器。AI先检查精确评论正文及发布/更新对象，再进入原副作用预览。真正写入仍由原owner控制；单纯局部补审不自带写权限。
6. **分发**：原guru-upgrade-tools负责已有checkout的matching工具/workflow/Skill投影；canonical installer及其元数据负责新安装。registry、production manifest、Interface版本、schema引用、examples和测试入口成套变更。

先行Readiness直接复核是最短可行路径。新复核Skill会重复同一判断，完整receipt重跑违背按缺口补审，长期ledger则引入无必要共享写与维护。调用期只携带当前对象和局部结果；缺失时从原公开producer或live来源恢复，不建立跨Skill的digest链。评论恢复所需单次attempt定位只服务已成功对象，不成为评论资格或覆盖authority。无新增保护机制、并发协议或性能指标。

## 5. 接口与数据

### 5.1 已有Issue入口及逐出口

以下均为本项新profile的独立schema；不把旧transition总包扩成全optional对象。`issue`仅为 `{repo_ref,number}`；`base_source`为闭合的 `{kind,selected_ref,commit}`，kind为git_object或synced_branch，commit为完整40位commit OID。它保留审核来源，selected_ref不表示Task集成分支。repo执行位置由原调用参数提供。`continuation_id`指向同次Readiness，不是授权或通过token。

输入 `existing_issue_intake` 必填 profile/mode/issue/base_source/continuation_id/source_exit；source_exit来自实际baseline_ready或synced。实际Sync read输出的base.kind=git_object时，薄router原样复制kind/selected_ref/commit；实际Sync同步成功时，设kind=synced_branch，selected_ref取标准化的原selected_base，commit复制原decision_head。不能从read、当前HEAD或邻近字段推断同步事实。Issue来自明确caller；缺真实来源或对象回原producer，不制造前序结果或从目录猜对象。

| 新profile出口 | 最小output与直接consumer |
| --- | --- |
| ready | 新独立ready变体：exit_id/mode/issue/base_source/continuation_id/source_selection；唯一consumer仍guru-task-intake-router，再到原Create Task |
| supplement_context | exit_id/mode/issue/base_source/continuation_id/gap；原Discovery局部profile |
| supplement_requirements | 同上；原Clarify局部profile |
| supplement_wording | 同上；原Wording局部profile |
| full_intake_required | exit_id/mode/issue/base_source/continuation_id；原Discovery pre_task，完整链终点仍原Readiness current_issue |
| refresh_issue_baseline | exit_id/mode/issue/continuation_id/base_source；原Sync按来源kind和当前真实操作意图恢复或刷新，实际结果回本入口 |
| blocked | 原blocked最小出口；当前对话说明具体缺口、恢复条件和受影响owner，唯一fail-closed stop |

`gap`是指明当前缺失事实、需求或措辞的非空描述；它不封装全量覆盖历史。`source_selection`沿既有locator/section/authority_kind形状，供Task后续原Clarify/Author使用。Readiness只采用仍适用的原来源角色结论；没有引入来源时为[]。来源角色或规范性约束有真实歧义时必须走Clarify，不能靠评论解析器推断。

ready→原Create Task当前consumer按以下三项分别承接：

- Issue身份进入reviewed_source={kind:"issue",repo_ref,number,disposition}；disposition仍由原Create Task审核为exact_source或reference_only，不增加relation字段或改变关闭责任。
- base_source的kind/selected_ref/commit仅原样投影为creation.reviewed_base_source。原Create Task核同仓精确对象确为commit，并核acquisition.decision_head=该commit。git_object的selected_ref只定位已采用来源，不重新解析其后来值，不比较本地main与固定commit，也不因read要求primary clean。原checkout/acquisition其余资格保持。
- creation.selected_base_ref由原Create Task独立审核为Task集成branch，供官方task.py --base-branch；delivery_target另保未来交付仓库/branch。本Task二者为main，来源仍为固定B；从来源selected_ref、remote ref或commit字符串推导任一目标均不合法。新Readiness不拥有分支选择，故不把这两个目标复制到各局部DTO；原Create Task在原副作用预览中核定它们。

synced_branch的来源selected_ref必须与selected_base_ref表示同一标准化branch；该来源身份关系属于新建/恢复共用检查。只有新建前额外要求该本地branch HEAD等于来源commit；已完成结果恢复沿原来源/acquisition和成功事实，不因后来branch前进失效。当前目标合同是原package的schemas/public-delivery-task-creation-input-2.0.schema.json和共享contracts/task-lifecycle/task-creation-input-3.0.schema.json；不重新引入其已移除的reviewed_base_head公共输入。不得用新ready补造旧readiness_current transition。

字段级例子如下，假定上游真实read已经返回所示固定来源。此片段只说明投影，不是完整创建输入，不会再次创建本Task；acquisition其余字段仍由原owner审查。

```json
{
  "ready_base_source": {
    "kind": "git_object",
    "selected_ref": "origin/main",
    "commit": "4f2adef1f7b099f78bb8429e8b8facd66dce3bfc"
  },
  "creation_projection": {
    "reviewed_base_source": {
      "kind": "git_object",
      "selected_ref": "origin/main",
      "commit": "4f2adef1f7b099f78bb8429e8b8facd66dce3bfc"
    },
    "selected_base_ref": "main",
    "delivery_target": {"repo_ref": "castbox/guru-trellis", "branch_ref": "main"}
  },
  "acquisition_projection": {"decision_head": "4f2adef1f7b099f78bb8429e8b8facd66dce3bfc"}
}
```

旧ready完整链变体保持自己的独立schema及真实前序；新aggregate按实际profile选择。guru-task-intake-router明确识别两类合法producer结果；新分支直接薄投影到原Create Task，旧draft仍到原Create Issue，standalone仍走原no_issue。Create Task无需更改生命周期DTO，只更新其Skill中ready字段投影和对应example/validator的入口消费要求。

### 5.2 三类局部补审与回判

三个owner分别拥有自己的输入schema，均为 profile=issue_readiness_supplement、source_exit=相应supplement_*、mode/issue/base_source/continuation_id/gap。输入、supplemented、Clarify事实往返和Wording requirements_gap均保持§5.1完整base_source三字段；不能丢kind、换commit、重新解析selected_ref或把它改成集成branch。不能要求当前context_current或clarity_current。各自读取live对象及仍适用依据，履行自己原semantic review、必要交互和record/check。新的 `supplemented` 出口只交Readiness `issue_review_return`：共同字段exit_id/mode/issue/base_source/continuation_id，另带该owner的非空 `result_summary` 和必要 `source_refs`（可空数组，不装全量历史）；Clarify结果另有实际source_selection。Readiness返回输入分别以 context_result、requirements_result、wording_result 三种闭合变体承接真实producer结果，不接受一个总optional结果对象。

Discovery只提供事实及影响，不替Readiness决定ready。Clarify需事实时沿原needs_context→Discovery context_request→Clarify往返，增加局部return identity适用分支，保持Issue/base/continuation和实际待解决gap；结束才supplemented。Clarify必要正文/评论mutation及readback仍在自身原合同，之后回判。Wording使用原完整Issue标题/正文scanner和保义方法；等义修改及实际结果回判，若发现真正需求问题用新 `requirements_gap` 出口薄投影回Readiness，再由其选择supplement_requirements。只读而确需修改仍用原blocked/revision语义，不能假称补审完成。

Wording的requirements_gap独立output必填exit_id/mode/issue/base_source/continuation_id/gap/source_refs，只交Readiness；issue_review_return为它增加requirements_gap这一闭合输入变体。Readiness根据真实需求缺口选择原Clarify，不把该输出当作wording通过。局部Clarify的needs_context沿原context_request接口增加resume_profile=issue_readiness_supplement的独立return变体，保同Issue/base/continuation/gap；Discovery的context_ready仅交回该Clarify，不能提前交Readiness或原标准Clarify。

局部owner若实际缺事实则回原context producer；已证实基线失效用Readiness刷新路线，不把查事实变成Sync。未知出口、同Issue/base/continuation错配、缺真实producer结果均停止或回原producer；脚本只校验这些客观关系。Readiness重新读取改变对象及结果，判断哪些原覆盖仍有效；不凭结果摘要自动放行。

### 5.3 原完整链和Sync

Sync current输出的唯一consumer由“固定Discovery”显式迁移为上述薄base router。非已有Issue及原confirmation context_request逐字段保留原projection。新refresh route新增专用return identity（Issue/continuation及既定返回目的），不得借normal/solution confirmation profile承载。Sync只读Git事实、保留已选来源和已给返回identity，不决定Intake路线。

full_intake_required用本次真实Sync结果构造原Discovery pre_task输入和真实change_input=该Issue。原完整transition保留其真实read或sync来源；不能把base_source三字段反拼成带虚构provenance/digest的完整transition。调用期原baseline输出丢失时回原producer恢复：固定对象read使用同selected_ref及固定commit；同步结果先恢复原操作结果，不把它改成read再继续宣称synced_branch。拿不到真实同步结果时由原Sync按实际意图重新执行，Readiness重判受影响覆盖；不凭局部字段补造。完整链的existing_issue及standalone_request出口继续消费原真实ready，并按当前#813合同进入Create Task；draft仍进原Create Issue。

refresh_issue_baseline保原base_source给原Sync识别来源种类：git_object走原read来源合同，synced_branch只有真实同步操作才产同步来源。缺失调用期依据只恢复同一结果；真实来源失效才由原Sync产生新事实，再回Readiness。此返回不从固定selected_ref设置Task集成branch，不借normal/solution确认profile，不把时间或无关HEAD变化当刷新原因。原资格确认、reviewed_plan_intake和合法no_issue保其原用途，不新增双reader。

### 5.4 评论输入与结果

Create Issue input升级到独立2.0，保留现有draft/reviewed_target/labels/原create或recover action，新增必填 `review_comment_body`：AI实际已审的正文。评论正文与草稿审核结果的语义对应由AI检查，executor只验证非空和正式Issue读回，不能自行生成结论。created仍仅返回exit_id/repo_ref/number/url；其新完成语义由Interface迁移明确为“内容一致且评论发布/读回完成”，不新增无人消费comment hash/metadata。下次Readiness直接读取live评论。

Clarify沿已有source_actions和当前对话执行精确 `POST repos/{owner}/{repo}/issues/{number}/comments` 或 `PATCH repos/{owner}/{repo}/issues/comments/{comment_id}`，更新仅限已明确的本次评论。正式Issue和comment各GET读回，比较实际正文/所属Issue；写失败不声称完成。原source action readback消费真实comment_id/url，不要求把该元数据扩入其他public DTO。

## 6. 状态、顺序、正常与失败流程

### 6.1 Readiness

已有Issue→真实Sync→existing_issue_intake。先读完整Issue和讨论/评论，核必要前置及相关代码，再判断覆盖是否充分和当前仍适用。充分且前置满足→ready；依次选择最早仍必要的事实、需求、措辞补审；影响不可界定或原覆盖不足→full_intake_required；已确认必要前置/真实选择/证据无法取得→blocked。无评论本身不阻塞，清楚旧评论也不是自动pass。

只在选定来源实际不可用/不再适用时refresh_issue_baseline；时间、会话、Agent或无关HEAD变化不触发。blocked恢复条件满足后回受影响owner或本Readiness，采用仍有效覆盖。AI说明判断依据与剩余边界，脚本不从labels、评论格式或时间算路线。

### 6.2 局部返回

supplement_*→原owner→真实supplemented→同Issue/base/continuation的issue_review_return。事实无变化可直接ready；需求改变则复核受影响正文，只有措辞覆盖受影响才补Wording；多缺口每次回判，不能自动继续所有后续步骤。Readiness调用期依据丢失时读live材料并向原producer恢复必要结果，无法取得则明确缺口；不拼接旧receipt或建立持久coverage缓存。

### 6.3 Create及恢复

完整草稿→Wording→Readiness proposed_draft真实ready→原Create AI审查精确Issue和评论payload→同次副作用预览→原executor创建Issue→GET正式title/body核一致→POST评论→GET评论和所属Issue核一致→created。正式内容已变则refresh_review，不发布与当前对象不符的评论。评论失败不另建Issue，也不提前created。

原attempt identity继续定位本次已创建Issue，并派生仅供这个executor定位其评论的恢复标记；标记不要求历史评论采用，也不被Readiness作为充分性判据。recover先查原Issue，再查该Issue本次attempt评论；唯一已成功对象读回后恢复结果；确认未执行才补剩余动作；零/多候选但执行结果不明则停止查明，不盲目再POST。普通请求错误、部分完成和输出丢失按原操作恢复；不设计并发锁、attack或crash压力协议。

### 6.4 Clarify

用户主动复审→AI审实际范围→只读则仅返回结论；存在明确评论发布或修订范围时，AI准备准确完整/局部结论，原source_action发布或更新，并live读回。更新用已明确comment_id；未知结果先查Issue下本次原动作的实际评论与正文，找回唯一对象，不因新Agent直接重发；无法唯一确定则blocked并说明已有成功事实和缺口。原private checkpoint仅在确有原恢复consumer时保存最小不可重推内容，消费后退役，不存用户授权。

### 6.5 讨论、创建和no_issue

没有Issue时沿Sync→Discovery→Clarify。仅讨论或草稿在对应结果结束；需要创建则完整Wording→Readiness→Create及评论读回；仅创建在created结束。还要求开工则将created正式Issue送Sync→existing_issue_intake，读取实际评论；仍适用时直接ready。原意图由当前对话caller携带，不新增持久授权/intent ledger。no_issue继续完整standalone_request审核及原Task创建，不要求空壳Issue或评论。

## 7. 恢复、兼容、迁移与集成

新增 MIGRATION-819.md，逐项列旧/新profile、schema $id、Interface/registry/manifest消费者版本和唯一route；不全体无差别升版。重点迁移Sync基线consumer、Readiness独立新ready、三个局部返回及Clarify context返回、Create2.0输入/完成语义、Task intake字段投影、examples与受影响ordinary runner/validator。旧已发布schema/example字节可保留作固定旧安装验证资产，不作当前runtime fallback。

切换必须用完整matching provider和原tools owner，保Task/session、用户修改、mode和sidecar。旧未完成create/comment动作先由匹配旧provider恢复已有Issue事实；新安装重新完成必要语义审查，再按同一Issue明确补评论动作，不重新创建对象或把旧created自动升级。旧Readiness/局部receipt不转换成新pass；重新读取当前对象进入适用owner。历史Task与资格确认仍按其真实阶段/固定安装合同恢复，不重置Task或扩大迁移。

Create Task当前aggregate2.0→profile2.0→共享creation3.0的选择由其Interface确定，canonical与installed已一致；旧未带版本后缀的profile1.0仅是历史验证资产。本项只为新ready增加到这个当前consumer的薄投影及匹配例子，不改回旧输入、增kind推断或重写原Creation内部同名字段。已成功的旧Task创建结果仍沿MIGRATION-813由固定原provider恢复，活动Task按当前Identity/Ensure/session/Delivery续接；本Task身份、gen0、D1和固定B均保持。

实施期在本Task隔离贡献中形成完整Architecture/RDT拟写。原maintenance owners在真实实施和工程自检后final_integration读取live expected-current、保留仍有效条件、整合/readback。TaskCommit纳入全部after；固定B/H的committed candidate/begin_check后，由新的独立reviewer完成同一次Architecture before/after与完整Review。当前Planning不晋升共享authority，不产生额外提交前candidate Check。

## 8. 验证设计

| ID / 对应 | 层、入口和输入 | 独立观察与边界 |
| --- | --- | --- |
| V819-01 / AC2、R2–4 | 生产public wrappers及workflow消费者；真实baseline输出→existing_issue_intake→ready→当前Create Task；采用充分、事实缺口、需求缺口、措辞缺口、依据不足、必要阻塞场景 | 路线来自实际AI判断；确定性fixture验证真实kind/selected_ref/commit经新投影可被原Creation2.0/3.0消费，固定对象与集成目标独立、acquisition匹配；实际同步路径保原branch/新建HEAD条件，不要求旧前序transition。只做schema不能证明AI覆盖判断。 |
| V819-02 / AC2、R3–4 | 各原局部profile公开入口；实际局部结果回同Readiness；含事实不变、需求改变影响措辞、多缺口、阻塞解除、真实基线失效 | 观察每次回判及仅必要owner被调用；三类局部、Clarify事实往返与刷新均保真实source kind和精确对象；最终ready仍进入当前Creation。必要全链使用真实Sync transition，不以fixture构造supplemented或反拼transition取代producer。 |
| V819-03 / AC1、R1/R7 | 原Create invoke及repo-bound gh测试边界；草稿完整审核输出、正式readback、评论POST/GET及原recover | 断言动作顺序和created终点；普通评论失败、已成功输出丢失恢复同Issue/comment，原无评论时不重复Issue。隔离HTTP替身仅证明executor，不证明live写入。 |
| V819-04 / AC1、R1 | 原Clarify主动review/source_actions与readback；完整/局部/只读及更新对象 | 实际AI评论语义范围准确；只读无mutation；POST/PATCH及GET对象一致；未知结果找回原动作。不机械比较固定模板。 |
| V819-05 / AC3、R5–6 | 实际Agent从讨论→草稿→创建→开工；讨论/草稿/仅创建终点及原no_issue | 正式Issue入口读实际评论；无重复产品问答/完整链；原Task/acquisition和后续门禁保留。真实外部动作需原owner的精确对象与payload，未执行则AC1/AC3外部部分仍未验证。 |
| V819-06 / AC4、R7 | 受影响package/runtime、public examples/graph/Interface、真实installed消费者；原tools更新及定向reapply | canonical/installed/声明平台投影一致、无未知出口；preserve Task/session及用户内容，mode/sidecar正确，drift脚本通过。分发事实不代替行为验收。 |
| V819-07 / AC5、全部 | 原知识整合/readback→TaskCommit→独立committed Review→Delivery/Task原收尾 | 真实after覆盖完整要求。当前只规划，未执行任何后续结果。 |

采用已有test_intake_profile_integration的完整链、source_selection和qualification返回；其对新先行入口/局部返回没有覆盖，补生产wrapper集成用例。采用test_issue_content_distribution的正文共享分发/reapply，扩展新评论正文引用与实际安装；它不能证明评论语义或外部写入。Create本次无评论旧测试保持草稿/Issue基线价值，新评论终点另补。长期测试只覆盖不同可观察分支；临时Agent观察或外部回读按实际入口报告，不为固定案例数或计时造系统。

先做profile/路由确定性检查，再做实际Agent分流/评论内容与真实外部动作观察，最后必要安装采用验证及原质量链。该顺序让普通接口错误先被低成本检查发现；没有惯例红绿/回退要求。行为条件、动作和结果为断言来源，不把实现常量或自己生成fixture当预期。证据充分后停止；新增实验仅解决具体未决缺口。完整多平台Throwaway、release、生产效果不在本项验证范围。

## 9. Canonical 引用、本轮差额与实际未决项

完整RDT来源是 docs/{requirements,design,test}/current/local-fix-intake.md、issue-content.md，authority为guru-trellis-rdt/active。前者保留原reuse事实方法并窄替代固定全链；后者保留内容方法，补评论生产/消费。拟完整current由原RDT owner按delta_first在final_integration维护，不在这里写第二套定义。

Architecture隔离贡献位于 docs/architecture/contributions/819-issue-review-intake/contribution.md，必要ADR候选为同目录issue-review-intake.md，decision identity=ADR-ISSUE-REVIEW-INTAKE。拟共享target为03-domains/issue-review-intake.md和adr/issue-review-intake.md；Planning只写隔离候选，不向root/system/ownership/ADR index登记。project descriptor/check/result继续原change-contract的既有identity。九concerns由贡献逐项展开并交原独立final_plan判断。

没有未解决产品选择或必须新增兼容例外。具体public版本号在实施时按当前registry/Interface合法successor分配，但本节规定的形状、consumer和直接迁移为本批设计责任，不能省略。真实Agent、评论外部动作、工具采用和工程验证尚未执行；后续缺少精确外部验收对象时由原owner展示，不把fixture成功当作live验收。最终Approval只判规划可实施，当前停止在Activation/实施之前。

