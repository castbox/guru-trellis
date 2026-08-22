# 技术设计：统一临时对象生命周期

## Architecture Boundary

canonical ownership 放在 `trellis/presets/guru-team/` 与 `trellis/skills/guru-team/` 的公共源；`.trellis/guru-team/`、平台目录和安装目标只是 projection。确定性脚本负责 root/prefix 解析、对象登记、信号/退出清理、stale 判定、删除/保留 disposition、schema/hash 校验；语义 ownership 仍由 inventory contract 和 AI review gate 决定。

新增一个 package-local lifecycle module（由 shared runtime 复用稳定的 root/path helpers），并由以下 owner 通过薄 adapter 接入：preset apply/verify、extension verification、task commit、Phase 2/installed verifier。不得把业务判断塞进 shell/Python executor。

## Inventory Contract

登记五类现有前缀：`guru-team-preset-stage-*`、`guru-trellis-install.*`、`guru-extension-verification-*`、`guru-task-commit-input.*`、`guru-phase2-input.*`。每行包含 owner、kind、controlled root resolver、prefix、created_by、live/in-use probe、stale predicate、normal cleanup、next-run recovery 和 diagnostic owner。`guru283wording.*`、显式 `WORK_DIR`、未登记 `guru*` 不进入 inventory。

每次 auto-created run 取得一个 run handle，记录对象 path、owner、root、prefix、creation marker/live marker。`try/finally` 与 SIGINT/SIGTERM handler 调用同一 cleanup；SIGKILL 仅由下一次 reaper 处理。删除动作先做 lexical/realpath root containment 和 exact prefix 检查，再判断 stale/non-live；target resolution 失败返回 fail-closed disposition。

## Data Flow

1. resolver 解析 controlled root；错误立即阻断宽泛扫描。
2. creator 通过 inventory entry 创建对象并登记 run handle；caller path 不登记为 auto-created。
3. primary operation 返回时，cleanup runner 逐项删除并生成 `deleted`、`retained_live`、`retained_non_stale`、`deletion_failed` 或 `deletion_unverified`。
4. next-run reaper 读取登记 root，按 prefix + stale predicate 逐项输出 candidate evidence；不跨 root、不递归清理未知对象。
5. adapters 将 cleanup disposition 合并到既有结果，不覆盖 primary result；测试读取结构化结果而非日志字符串。

## Projection and Compatibility

canonical inventory/schema、runtime module、tests、preset installer manifest 和平台 projections 一起更新；执行 `apply.sh --repo .` 同步 dogfood，并执行 drift/sidecar checks。保持现有 command argv、显式 `WORK_DIR` 保留语义和所有既有 atomic Guru capabilities；旧调用方若不使用 auto-created handle，继续走 caller-owned 保留路径。

## Failure and Security Boundaries

删除 policy 被本地拒绝时不绕过 policy，返回 `deletion_unverified`；CI/isolated fixture 才能证明 actual delete。路径 resolution、symlink/unsafe target、unknown prefix 和 live/in-use 一律保留或 fail closed。该设计不引入攻击者模型、锁或跨 OS 原子协议。

## Rollback

变更按 canonical module、adapter、inventory/schema、projection 和测试分层提交；若 runtime integration 失败，可回退 adapter 接入而保留无副作用 inventory/test contract。不得通过恢复 broad deletion 作为回滚。
