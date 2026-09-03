# ADR-008 Candidate: Solution Mechanism Qualification

状态：`candidate_pending_independent_review`；本文件在 Architecture
promotion 前不是 accepted ADR，也不是 CURRENT authority。

## Context

Guru Team 已有 `guru-qualify-normal-scenario`，但它只判断问题场景是否
进入后续流程。Issue #240 新增公共 `guru-qualify-solution-mechanism`
semantic owner，用于判断拟采用的机制是否把业务 authority 下沉到 OS、
kernel、process 或 descriptor 原语。

## Decision Candidate

采用两个独立的 qualification owner：normal-scenario owner 判断问题场景，
solution-mechanism owner 判断解决机制。机制 owner 直接读取 requirement、
Architecture/spec authority、dependency/caller graph、diff 和 tests，AI
负责语义判断；recorder/validator 只验证 shape、identity、freshness 和
consumer binding。

OS lock、`/proc`、PID/PGID/SID、process tree、FD identity、signal/kill 及
同类原语在承接业务正确性、身份、fencing、monitor、inspection、cancel、
recovery、publication 或 evidence authority 时不合格。普通文件/目录仍可
作为 state、artifact、日志、配置和 cache 使用，但其存在性、inode、FD 或
打开状态不得成为业务 authority。

命中禁止机制时，机制 owner 返回 `mechanism_revision_required` 并回到
原调用方删除或替换后 fresh 重跑；缺少完整 live authority、dependency
graph 或 candidate set 时返回 `blocked`。该 owner 不承担场景 qualification、
severity、implementation route 或 publication readiness。

## Alternatives Rejected

- 将机制判断合并进 normal-scenario qualification，造成两个语义 owner
  互相替代。
- 用关键词/import/命令名/path scanner 或测试通过结果替代 AI 语义判断。
- 通过 lock/process adapter、fail-closed 或 race/TOCTOU 叙述继续让 OS
  原语承接业务 authority。

## Consequences

公共图谱新增一个 semantic owner，caller 需要提交 profile-specific
candidate set；workflow、registry、preset 和三平台投影必须保持同一
public identity。该变化走 `target_native`，不保留 legacy dual-read、
compatibility adapter 或业务仓迁移。Architecture shared current 仍由
现有 promotion owner 单写，task-owned contribution 在独立 committed
full-diff Branch Review 前保持隔离。

## Acceptance Condition

本 candidate 只有在独立 Branch Review、serialized Architecture promotion
以及 promotion 后 fresh Phase 2、Task Commit 和 Branch Review 均通过后，
才能成为 accepted/current architecture decision。#260/#267 的完整
throwaway、upgrade 和 release matrix 不由本 ADR candidate 声称覆盖。
