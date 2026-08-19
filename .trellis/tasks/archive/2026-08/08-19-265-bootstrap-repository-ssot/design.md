# 设计：guru-bootstrap-repository-ssot

## 1. 公共合同

Skill 使用 `judgment_mode=semantic`、Interface 1.4，输入 discriminator 为
`new_repository`、`existing_repository`、`repair`。输入只包含 caller/mode、仓库与
bootstrap task identity、已有 authority locator、scope、continuation/freshness
token 及两个子 Skill 所需的最小 bootstrap projection；不跨边界传递 private artifact。

四个输出分别携带直接 consumer 所需的最小 DTO：

- `completed`：两套 SSOT locator/version/status、spec projection identity 和 freshness。
- `baseline_incomplete`：不完整状态、缺口 locator 和同一 Bootstrap/repair consumer。
- `repair_required`：stale/conflict projection、修复 scope 和 repair profile consumer。
- `blocked`：稳定阻塞码、受影响 authority identity 和 fail-closed stop consumer。

完整扫描、Git facts、review narrative、hash bundle、授权和 recorder state 保持
owner-private；runtime 只做 schema/identity/freshness/consumer 校验。

## 2. 编排与语义边界

forward behavior 依次执行 upstream `trellis-spec-bootstrap`、#263
`bootstrap_foundation`、#264 `bootstrap_foundation`，再由 Bootstrap AI 检查跨 SSOT
版本/适用范围、行为与架构约束、设计继承、测试覆盖、CURRENT/TARGET/GAP 与事实一致性，
以及重复 authority 的复用/迁移/引用化。#263 到 #264 的交接 payload 仅包含
thin locator/version/status projection。Bootstrap 不重新解释或重写两个子 Skill 的内部 authority 判断。

`.trellis/spec` projection 建立或复用 `docs` 与 `architecture` 入口，保留唯一 canonical
locator、status/version、traceability、读取顺序、Planning/Implementation/Check/Review/
Finish 更新规则和 `sync_required` 指定 route；不复制正文。普通并行 task 不直接写 shared index。

## 3. 安装与平台

canonical package、registry row、workflow markers、consumer schemas、preset inventory、
README 与 shared/Codex/Claude/Cursor copies 由现有 registry-driven installer 管理。dogfood
副本通过 preset apply/reapply 同步，不能成为唯一源头。安装、upgrade、update、workflow switch
只返回 bootstrap 状态/预计范围，不静默执行或 archive `00-bootstrap-guidelines`。

## 4. 验证模型

package contract/runtime/eval 覆盖三个 profile、四个 exits、最小 output、self-reentry、
stale/repair/incomplete、子 Skill typed projection 和 consumer identity。安装侧执行当前版本
定向 canonical/dogfood/installed/platform parity、reapply/drift、recursive zero `.new/.bak`、
executable mode、README 命令及一个代表性 clean throwaway；不执行 #260/#267 所有权范围内的
完整多平台或 exact-candidate release 矩阵。
