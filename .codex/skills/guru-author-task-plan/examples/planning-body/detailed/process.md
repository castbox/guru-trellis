# 详细来源的调查、成文、切片与修订

本目录是去敏、合成的教学材料，不是真实会话、用户答复或测试结果。下面描述示范推理及预期 owner 行为；不能将这些正文或预设修订当作 V1–V7 的实际 Agent 行为证据。

## 输入与调查

先完整读 [source.md 第1节](source.md#1-当前要求)，再读第2节的事实快照、第3节 authority 和第4节的来源角色。Discovery 在实际仓库应查 cli.main、入口、现有 tests 和依赖；示例已明确给出这些教学事实，未声称真的执行过调查。

Clarify 的来源选择保留 R1–R4 为要求、D-A/D-B 为约定设计。C1 是建议，H1 是历史，E1 是证据摘录。H1 与 R2 的处理不同，但它没有当前规范效力，因此不是待用户决定的产品冲突。当前输入已明确调用方、范围和失败语义，无需制造澄清。如何校验字段和构造 CheckResult 属于 Author/Architecture 的技术细化，不要求用户设计。

如果实际新来源要求“缺失后立即停止”，Clarify 应调查它是否意图变更 R2；真正产品选择未答前停止相关 requirements_ready，不能依文本较新直接覆盖。此条件分支没有虚构用户答案，也不改变本目录 final 正文的输入。

## 四类完整正文

1. [task-prd.md](task-prd.md) 承载整体需求，原 Clarify 复核后才 accept_scope。这里不先要求 Delivery 设计。
2. [delivery-prd.md](delivery-prd.md) 展开全量 D1 的起点、范围和全部本批行为，requirements_ready 前收敛。
3. [delivery-design.md](delivery-design.md) 在候选独立评估后展开引擎、adapter、字段、状态/流程和唯一来源设计处置。
4. [delivery-implement.md](delivery-implement.md) 安排文件、依赖、命令、输入与观察，以及 full Policy 和 Docs Plan。

本目录没有真的调用 wrappers 或接受任何规划。正文展示的是各阶段需要形成的内容，未预填 semantic pass。

## 一次具体审核与修改

初稿 design 第6节曾写：“逐项检查文件；缺失项记 missing_file 后继续。”这遗漏了 R1/D-B 的“完整格式校验先于任何文件检查”，也没有落实 R2 的 disabled 不访问。对应 implement 初稿只安排合法/缺失两类测试。

原 Approval 在其充分性范围内应指出：合法第一项之后跟一个重复 id 时，初稿可能先访问第一项文件；disabled 路径也可能被探测。这里是正常规划遗漏，不是人为篡改已接受事实。revision_actions 返回原 Author 的 requirements/design 修订，保留 R1/R2，不要求用户重新选择。

最终 [design 第5、6节](delivery-design.md#6-状态顺序正常与失败流程) 明确完整字段校验→重复 id 校验→disabled 分支→文件存在判断。最终 [implement I1/V2/V4](delivery-implement.md#3-验证入口输入与预期观察) 增加 reader 调用观察和“先合法项后坏项”用例；前者验证 disabled 不调用，后者验证格式错误时零文件检查。这是可核对的前后变化说明，测试仍是计划，不伪称已运行。机制细化重新进入原候选评估，随后由原 owners 重审实际最终稿。

## 部分与后续切片

[slices.md](slices.md) 给出另一种教学切片：P1 先交纯引擎，P2 后接 CLI。它与本目录 full D1 是互斥的教学安排，不能同时当作实际 Delivery 历史。两批各有完整 PRD/design/implement，P2 输入的前序事实也明确标为教学前提。实际流程必须由原 Creation 和 Delivery owner 产生真实身份/结果，不能宿主手写 delivered 后计入验收。

## 来源更新和恢复

如果实际来源把 JSON 输出增为另一个字段，Clarify 先判断是否是整体要求变更，发布当前整体 scope 后再修订受影响 Delivery。旧输出和旧验收保持历史身份。恢复会话通过原 Bind/Selection 解析同一 Task/Delivery，重新读当前模板、完整相关来源、必要 canonical 引用和前序结果，不能将本目录的示例基线当 live identity。
