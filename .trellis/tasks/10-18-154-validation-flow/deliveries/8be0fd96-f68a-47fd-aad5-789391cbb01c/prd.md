# D1：pack 输出目录帮助需求

## 1. 整体来源与术语

整体 authority 为 `.trellis/tasks/10-18-154-validation-flow/prd.md`，revision `sha256:81b7e22d328f03a46b9844a63c8c7477df39a420f2a07818302b36e1bb61ed76`，由公共 accepted_scope 持有。当前 DeliveryKey 为 `8be0fd96-f68a-47fd-aad5-789391cbb01c`，scope_ref anchors 为 R1、R3、R4、AC1、AC4、AC5；planning_root 为 `deliveries/8be0fd96-f68a-47fd-aad5-789391cbb01c`。

| 来源 | 章节 | 角色与用途 |
| --- | --- | --- |
| Task 根 prd.md | §1–8 | 整体要求与 Completion，实际加载 |
| validation-fixture/source-a.md | 全文 | requirement；帮助、dry-run、不覆盖保留，改 build 不采用 |
| validation-fixture/source-b.md | 全文 | requirement；保留 dist 与共同承诺 |
| validation-fixture/docs/usage.md | 全文 | 当前行为证据 |
| validation-fixture/sandbox/pack.py | build_parser/build/main | 当前解析与构建边界 |
| validation-fixture/tests/test_pack.py | 三个现有用例 | 当前兼容基线 |

本批帮助指 argparse 的 --help 输出；默认值指未传 --output 时使用的 dist。

## 2. 整体与本批目标、非目标

整体目标为帮助展示与 dry-run。本批独立目标是让 CLI 调用者在 --help 看见已支持的 --output DIR、目录用途与真实默认 dist。只承担 R1，并保持 R3 与 R4 的切片边界。

D1 不新增 --dry-run、不改变 main/build 的普通构建流程、不改默认 dist、不改变目标已有时返回 2 和不覆盖语义。不涉及远程服务、安装器、打包格式或并发机制。

## 3. 本批起点、前序结果、依赖与剩余责任

首次 D1，没有前序 delivered 结果。当前 build_parser 用 argparse.SUPPRESS 隐藏 --output；普通构建已支持默认 dist、自定义目录和已有目标拒绝。D1 从该实现出发，不依赖 D2。

剩余 R2 由后续 D2 实现默认/显式目标的零写入 dry-run，包括新增来源 C 要求的已存在目标预演（整体 AC3E），并回归本批帮助与普通构建。D2 尚未创建或交付。本批只形成 partial 交付；整个 Task Completion 仍须 AC1–5 及 AC3E 的完整证据，由原 Completion 处理，不能以 D1 合并替代。C 只补充 D2 的条件；其 JSON 输出建议不进入本批或 D2 要求。

## 4. 本批调用方、场景与流程

- D1-S1：本地 CLI 调用者运行 --help。argparse 输出参数说明并返回 0，不调用 build，不创建目标目录或 package.txt。
- D1-S2：现有调用者无参数或 --output artifacts 普通构建。解析仍传同一 output 给 build，成功行为不变。
- D1-S3：目标已存在时普通构建。stderr 说明目标已存在，返回 2，已有内容及文件集合不变。

本批改变参数的帮助展示，不改变上述普通构建分支和顺序。

## 5. 完整行为、条件与约束

D1-R1（整体 R1）：--help 必须显示 --output DIR、说明其用途是选择输出目录，并显示 dist 为未指定时的实际默认值。不能把 build 写成默认值。
D1-R2（整体 R3）：保留 output 的默认值 dist 与显式 DIR 输入语义，保留现有构建 stdout/stderr 和返回值。
D1-R3（整体 R4）：不新增 dry-run 实现。其整个要求完整保留在根 PRD 与本批 §3，不得标为 delivered。
D1-R4：帮助路径不得触发目录或文件创建；--output 的帮助展示必须引用实际参数默认值，避免另建第二份默认权威。

来源仅约定产品行为，没有规范性技术设计；具体判断见本批 design §3，不能把来源当实现方案。

## 6. 本批验收、验证方式与未决项

| AC | 场景/要求 | 输入与入口 | 预期观察 |
| --- | --- | --- | --- |
| D1-AC1 | S1/R1 | Python CLI --help | 返回 0，stdout 含 --output、DIR、目录用途和 dist，stderr 空 |
| D1-AC2 | S1/R4 | 在受控空目录运行 --help | 文件集合前后相同，不创建 dist 或 package.txt |
| D1-AC3 | S2/R2 | 现有默认与显式 output 测试 | 仍在 dist/artifacts 写 package.txt，返回 0 |
| D1-AC4 | S3/R2 | 现有目标拒绝测试 | 返回 2、stderr 包含目标已存在、原内容和集合不变 |

这些是后续实施验证目标，不是通过结论。本批完成支持整体 AC1、AC4、AC5，整体 AC2/3 仍留 D2。需求没有必要未决项；技术细化进入原 Architecture candidate_assessment 后由 Author 完成。

## 7. Canonical 引用与本轮差额

requirement/behavior：根 PRD §5/7 和 fixture usage 全文；本批差额为帮助从隐藏变为可见。
design：pack.py build_parser/build/main 是当前设计事实；本批只改变 build_parser 帮助元数据。
test：test_pack.py 三例是现有回归；需增加帮助内容和零写入观察，后续实施才写测试。
Architecture：docs/architecture/00-foundation/baseline.md、design-constitution.md 与 docs/architecture/06-governance/change-contract.md，由原独立 Architecture owner 按自己的顺序读取和判断；本批不预填架构结果、不改共享导航。
