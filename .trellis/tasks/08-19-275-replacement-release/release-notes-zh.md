# v0.6.5-guru.10 发布说明（草案）

## 修复内容

- 修复 `v0.6.5-guru.9` Throwaway closeout 中，Finalizer 已完成 archive、Ready PR 与 terminal cleanup 后 public invoke 错误返回 `finalization_stale` 的回归。
- terminal projection 只接受精确 retired owner locator，并重新校验 durable archive identity 与当前 local/remote/PR/scope facts；真实 stale 行为继续 fail closed。
- Throwaway verifier 的 active package、command 与 complete-package inventory 改为从 canonical registry/interface validation 派生，不再维护固定数量。
- 修复 installed `finish-work.sh` 的 managed runtime import path，并同步 Shared/Codex/Claude/Cursor 投影与 executable mode。

## 版本与升级

- repo tag：`v0.6.5-guru.10`
- Guru Team extension revision：`0.6.5-guru.36`
- official Trellis CLI target：`0.6.5`
- workflow/preset source：同一 immutable `v0.6.5-guru.10` tag

升级时使用 pinned marketplace/workflow source，执行 official Trellis update 后重新 apply Guru preset，并核对 canonical/installed/platform inventory、ownership、mode、overlay drift 与递归零 sidecar。

## 验证与边界

发布前必须完成 current-HEAD independent review 与 exact-candidate clean install、existing `v0.6.5-guru.9` upgrade、workflow preview/switch、official update、preset reapply 和完整 closeout。合并后才创建 annotated tag；随后验证 peeled commit、manifest identity、tag-pinned fresh smoke、非 draft/非 prerelease GitHub Release 与 `castbox/k8s-infra#28` live consumer gate。

本 Issue 不承担 #260 的完整多平台 upgrade/update matrix，也不承担 #267 的最终累计 release authority。预期 Release 不携带额外 assets。

## 安全与部署

不包含 secret、credential、客户数据或业务仓手工 patch；不修改历史 tag/Release、Trellis upstream、全局 npm 或系统 Python。
