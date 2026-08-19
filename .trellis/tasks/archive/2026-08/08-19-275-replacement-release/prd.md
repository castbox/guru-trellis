# #275 修复 v0.6.5-guru.9 Throwaway closeout 回归并发布 replacement release

## Goal

GitHub issue: https://github.com/castbox/guru-trellis/issues/275

## Requirements

- 修复 Finalizer 归档后 `ready_for_merge` public projection，以 terminal authority 投影 DTO；真实 plan/content/head/branch/PR/archive/marker 漂移仍 fail closed。
- 将 Throwaway verifier active package/command inventory 改为 canonical registry/interface 派生，保留 id、command、planned-id 和 source/installed equality 校验。
- 同步 canonical、dogfood、installed、Claude/Codex/Cursor 投影、manifest、schema、contract、eval 与测试，并保持 executable mode。
- 完成 focused validation 与 exact-candidate cumulative Release Gate；仅在独立 review 和全部 release identity/smoke/downstream gate 通过后发布新 immutable annotated tag/Release。

## Acceptance Criteria

- [ ] exact `v0.6.5-guru.9` 回归可复现且修复后归档终态 public invoke 返回 schema-valid `ready_for_merge`。
- [ ] Finalizer/Publication/Merge/closeout focused tests、source/dogfood/installed drift 和 executable mode 检查通过。
- [ ] verifier 不含 `18/65/18` 等固定 inventory，且 canonical registry/interface validation 与 installed projection 一致。
- [ ] 新 tag/release 的 peeled commit、manifest/version identity、tag-pinned smoke 和 `castbox/k8s-infra#28` gate 通过后才关闭 Issue。

## Notes

不修改历史 tag/Release，不吸收 #260/#267 或 broad Phase refactor；完整多平台矩阵由后续 release/upgrade Issue 负责。
