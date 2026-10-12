# #535：两个 Review owner 的真实零候选承接

## 来源与目标

Direct Source：castbox/guru-trellis#535，完整正文的目标与范围及验收；创建后 fresh Intake 读取 live body（含原创建标记）与 updatedAt。#292 是缺口发现现场，不是本 Task 来源；#532 只拥有 Check、#530 只拥有 postcommit ingress、#531 只拥有生命周期迁移。

目标：完整独立语义审查没有真实缺陷候选时，Branch Review 与 Delivery Review 如实以 `candidate_classifications=[]` 走完原 recorder/checker/public invoke；空数组本身不选择 pass/ready。

## Accepted scope

- R1：两个 Review owners 定义真实空候选与实际非空候选分支。空集合不调用三个 nonempty qualifier；实际候选按 normal→solution→eligible root 现有顺序承接。受审文件、业务功能和 no-defect 占位项不是缺陷候选。
- R2：current Branch gate7 与 archived gate1、共同 validator、Delivery semantic result1 接受空列表，保留元素类型、unique refs 与每个 finding/proposal/disposition 的真实引用校验。历史 pinned Branch gate5/6 不重写。
- R3：完整 Review 维度、live requirements、Docs/RDT/Architecture、完整 committed range、freshness、真实来源、route invariants、checkpoint 生命周期及 public I/O 保持。缺必需证据或正常 stale 不因空集通过。
- R4：共享 Branch validator 的 current `branch_review(initial_review|fresh_final_review)`、`base_continuity`、`archived_review` 都按实际 consumer 验证。Delivery 的 ready 与原 implementation/planning/scope/blocked routes 保持；三个 qualifier 合同不变。
- R5：同步 canonical、regular dogfood 与一个代表性 installed 全 preset 环境，示例去除虚构无缺陷候选；保留实际非空 rejected 及有效 finding 场景。执行定向 package/runtime、apply/reapply、drift、sidecar、mode 验证。

## 可观察验收

| ID | 入口/场景 | 预期观察 |
| --- | --- | --- |
| AC1 | current active full-range Branch 原 recorder→checker→invoke，真实零候选 | 完整前置与AI实际结论下正式 passed；数组为空、checkpoint正常消费 |
| AC2 | Delivery 原公共 invocation，真实零候选 | 十维、conclusions、policy、Refs-only payload充分时正式 ready；未凭空集推导结论 |
| AC3 | 实际非空候选全部 rejected | 分类/witness保留，合法无findings；与AC1/AC2分开证明 |
| AC4 | 正常可复现 qualified finding | 原implementation/revision/block route与真实candidate binding有效，不能因允许空集丢弃候选 |
| AC5 | 必需证据缺失及正常 content/base drift | 原检查拒绝或owner回程；不修改hash/checkpoint制造案例 |
| AC6 | current bounded continuity、archived read-only | 各自原范围、出口、只读和freshness保持；不扩大为full-review成功 |
| AC7 | canonical/dogfood/一个完整installed及apply/reapply | 原wrapper结果一致；无未处理sidecar/overlay drift；historical5/6字节不变 |
| AC8 | 独立完整语义结果及分层报告 | 单元/contract、实际原公开链路、投影安装、未验证边界分别报告 |

## Delivery policy 与非目标

一个完整Delivery slice覆盖R1–R5/AC1–AC8，无Task内部剩余切片；独立交付不依赖#531或#530完成。#292原owner在merge、base整合、正规安装和fresh gates后恢复其fixture，不能由本task改写。

不改Task/Delivery生命周期、不新增Skill/exit/DTO字段/ledger/授权存储、不改qualifier非空输入、不跳Check/Commit/Architecture/Review、不改upstream或全局包、不扩大攻击/伪造/竞态/crash范围、不执行完整多平台Release矩阵、不做业务部署或原#292验收、不隐含清理。

## Docs SSOT Plan

`ssot_first`：两个canonical Skill/contract是step-local行为来源，Python只校验客观值域和引用。regular dogfood由preset生成；platform薄入口不拥有第二份内循环。

RDT 使用 `docs/requirements-design-test-contributions/535-review-zero-candidates/` requirement/design/test/traceability，test.md唯一记录实际验证层级与首次失败/剩余边界。共享current仅经原RDT promotion owner的expected-current-bound路径晋升；历史版本保持。Architecture impact/path由fresh独立owner实际执行，不预填no-impact或制造贡献/ADR。Planning不是长期运行authority或验收证明。
