# #332 Original-entry correction Design contribution

## Entry And Runtime Model

- `D332-ENTRY-01`：四个原 `scripts/invoke.sh` 是唯一平台 public wrapper，并分别固定绑定
  `invoke-guru-create-task-commit`、`invoke-guru-review-task-publication`、
  `invoke-guru-finalize-task`、`invoke-task-pr-merge`。
- `D332-ENTRY-02`：每个原 command 的 arguments 定义 Happy Path 与 compatibility 的 closed union；
  package-local `runtime/invoke.py` 在入口处按互斥参数选择单一路径，公共 wrapper 只定位 managed
  dispatcher、绑定 command id 并透传 argv。
- `D332-ENTRY-03`：Happy Path 复用 invocation-local facts，在 mutation boundary 与 post-mutation proof
  执行必要 fresh read；compatibility branch 只在旧参数出现时运行，不成为 Happy Path 前置链。
- `D332-ENTRY-04`：PR #341 的 transaction/recovery primitives 迁入或保留在原 command 直接消费的
  package runtime；只服务第二 public command 的 facade adapter、schema、example、fixture 和 projection
  在确认无 consumer 后删除。

## Distribution And Generic Consumers

- `D332-ENTRY-05`：Interface 是 wrapper path 的唯一公共 authority。通用消费者读取 exact declared
  wrapper，校验 canonical/installed/platform bytes、executable mode 与 private-script leak；文件名不参与
  public/private 判定。
- `D332-ENTRY-06`：`runtime/validate.py` 将 managed-launcher fallback 校验应用于 Interface-declared
  public wrapper；qualification-only helper 可保留其 package-local 固定路径，但不得扩散到 generic
  runtime 或 eval。
- `D332-ENTRY-07`：preset apply 负责删除 managed facade projection、同步 canonical/dogfood/installed 与
  Shared/Codex/Claude/Cursor；不得手工在共享 scripts 目录建立转发层。
- `D332-ENTRY-08`：`guru-restore-archived-task` 的 `restore-archived-task.sh` 覆盖 generic source、installed、
  platform、actual-load 与 eval 回归，证明 Interface-driven selection 可处理任意安全相对 wrapper path。

## Authority Lifecycle

- `D332-ENTRY-09`：本 task 只写独立 RDT/Architecture contribution，shared `.44` 保持 immutable；两个
  serialized owner 在 implementation candidate 完成独立 committed review 后，绑定 expected `.44`
  生成唯一 `.45`。
- `D332-ENTRY-10`：`.45` 修订 #330 的 current RDT/Architecture 语义、`DES-019`、distribution evidence
  与 live-derived 23 / 97 / 77 graph；promotion-created diff 重新进入 Phase 2、task commit 与独立完整
  Branch Review。
- `D332-ENTRY-11`：本任务使用 `dedicated_refactor_slice`，因为外部行为和既有 public identity 保持不变，
  只把错误的双入口实现收敛回一个 owner/entry。compatibility owner 是各原 command，退出条件是已声明
  旧 caller 全部迁移；在退出前也不得形成第二 public wrapper。
- `D332-ENTRY-12`：不创建 ADR。本次恢复 design constitution 已有的最小必要复杂度、变化隔离和技术债务
  单向收敛，不引入新的长期 architecture decision 或原则例外。

## Preserved Boundaries

- 各 semantic owner、typed exits、consumer、独立确认和 fail-closed route 不变。
- 低层 package-private 命令可测试、诊断和恢复，但不成为 Agent 正常编排步骤。
- 历史 #330/#341 和 `.44` authority 保留为 before-state；不改写历史 PR、tag、Release 或旧 candidate。
