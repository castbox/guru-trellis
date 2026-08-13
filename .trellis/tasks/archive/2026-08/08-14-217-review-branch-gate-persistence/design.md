# #217 技术设计

## 问题根因

当前 Branch Review 三阶段并未共享一个真实 owner-private state contract：

1. recorder 组装并校验 gate 后只返回完整 gate object；
2. checker要求调用者提供一个 JSON文件路径；
3. invoke要求调用者在 envelope中提供完整 `owner_result`；
4. package test手工把 recorder返回值写成临时文件，并把同一对象直接传给 invoke。

因此命令声明中的 `runtime_write` 与 Skill文档中的 `review-gate.json`/retirement生命周期没有实现依据。修复必须让公开 wrappers成为唯一正常入口，而不是为测试增加另一个辅助写文件步骤。

## Owner-Private Checkpoint

### 路径

在 package-local `common.py` 建立单一 resolver，生成 repo内 gitignored路径：

```text
.trellis/.runtime/guru-team/review-branch/<task-owner-key>/review-gate.json
```

最终相对布局以现有 private-state命名规范和安全path helpers为准，但必须满足：

- task locator与owner package共同决定唯一位置；
- caller不能传入任意输出路径；
- 每个现有父组件和目标文件都通过 lexical containment、`lstat`/symlink与regular-file检查；
- 不把绝对路径写入public DTO、tracked task artifact或manifest。

### 内容与 stdout

checkpoint内容继续使用 current `review-gate-4.0` compact gate，不新增授权、过程或完整scan字段。recorder在完整validate之后写regular JSON，再输出最小receipt，例如 task、typed exit和checkpoint identity所需字段；具体stdout schema应只满足 checker/invoke直接consumer。

写入采用普通normal-operation边界；本Issue不扩展锁、并发、TOCTOU或跨OS原子性。symlink与unsafe ancestor必须在写前fail closed。

## Wrapper 数据流

```text
AI semantic review
  -> review-branch wrapper
     -> validate public input + semantic result
     -> write exact owner-private review-gate.json
     -> minimal recorder receipt
  -> check-review-gate wrapper
     -> resolve exact checkpoint from task identity
     -> validate schema, facts, task/base/head/content freshness
     -> minimal checked receipt
  -> invoke-guru-review-branch wrapper
     -> resolve and rerun checker against exact checkpoint
     -> derive typed exit and project current public DTO
     -> retire or retain checkpoint per exit lifecycle
```

invoke envelope只携带current public input/identity，不接受完整caller-authored gate作为normal authority。compatibility-only旧locator若必须保留，应明确隔离且不得成为测试正向路径。

## 生命周期矩阵

| 场景 | Checkpoint结果 |
| --- | --- |
| `passed` check失败 | 保留，供同owner修复 |
| `passed` invoke投影失败 | 保留 |
| `passed` invoke成功 | 退休 |
| 非终态 `implementation_required`（首选覆盖）invoke成功 | 保留供finding/fix re-entry，具体consumer由现行合同决定 |
| 重复record同identity | 确定性覆盖同一精确checkpoint或返回稳定duplicate结果，不产生第二份文件 |
| 重复invoke已退休terminal checkpoint | fail closed |
| stale/mismatch/unsafe/symlink | fail closed且不得错误删除有效regular checkpoint |

若现行consumer证据表明另一个非终态route更适合retain测试，则实现可选择该route，但必须在测试名和合同文档中明确唯一生命周期。

## 兼容性边界

- 不修改 current gate schema 4.0的semantic字段、五个external exits、consumer mapping或public output schemas，除非为最小recorder/checker receipt建立非public command schema；public跨Skill DTO不得扩大。
- canonical package拥有private runtime；`.agents/.codex/.claude/.cursor`只接收public projection，不复制private Python runtime。
- `.trellis/guru-team/skills/packages/guru-review-branch` installed runtime与canonical byte-equal；preset manifest/inventory同步更新。
- shared kernel只在至少两个真实consumer语义完全相同时扩展，否则path/lifecycle helper留在Branch Review package。

## 测试设计

新增真实shell wrapper fixture，在临时Git repo与完整installed runtime中：

1. 通过 `review-branch.sh` record，断言stdout为最小JSON且checkpoint自动产生；
2. 通过 `check-review-gate.sh` check精确checkpoint；
3. 通过 `invoke.sh` invoke，不传手工owner result；
4. 对terminal/non-terminal断言retire/retain；
5. 对stale content、错误task/base/head、unsafe/symlink、duplicate与retired状态逐项断言稳定fail closed。

测试禁止调用private Python `record.run`来模拟公开生命周期，禁止测试代码写gate文件，禁止用预制checker-passed owner result直接invoke。package内部纯函数的schema/identity单测可保留，但不能替代wrapper-level acceptance。

## 验证与发布边界

实现后运行受影响package/runtime/integration tests、source/installed与四平台projection equality、targeted all-platform apply/reapply、managed inventory、dogfood drift和recursive sidecar scan。完整verifier、marketplace、official update、全平台throwaway、业务仓库upgrade与release/tag全部由#222或后续流程承担。

## 风险与回滚

- `common.py` path resolver与invoke retirement影响Branch Review所有 exits，是最高风险点；错误时应优先保留checkpoint并fail closed。
- 修改 `commands.json`/wrappers必须与interface、installed manifest和tests同批同步，避免mixed package activation。
- preset apply会刷新dogfood manifest provenance；只提交与当前实现对应的managed bytes，不把本机时间/路径或无关installed provenance纳入task提交。
