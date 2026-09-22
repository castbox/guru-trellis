# TARGET

- `ARCH-TGT-001`（accepted direction）：RDT 与 Architecture authority 通过 task impact/contribution/promotion 持续维护，`.trellis/spec` 始终是最小 projection。
- `ARCH-TGT-002`（accepted release target, `unverified`）：独立的重构前稳定版 Release Issue 在 exact frozen `origin/main` 上发布 tag `v0.6.15-guru.1`、extension `.37`、Trellis `0.6.15` immutable stable tag 与 GitHub Release；#267 与下一阶段重构链明确排除。
- `ARCH-TGT-003`（accepted release direction, `unverified`）：tag-pinned clean install、upgrade/update、consumer 与 release smoke 必须重验，不以 #260 的 `public_plus_local_candidate` 证据替代。
- `ARCH-TGT-004`（accepted direction）：Guru Trellis 下一阶段产品进化以
  [`EVO-001..007`](../../requirements/evolution/requirement-main.md)
  为唯一目标 authority。Architecture TARGET、Issue、task planning 和 Release
  只引用 goal identity、具体 delta 与证据，不复制目标正文；该 accepted target
  不表示 CURRENT 已实现或已授权执行。
- `ARCH-TGT-005`（accepted direction）：统一 task lifecycle 以 immutable TaskId、mutable TaskRef、
  lifecycle generation、portable source/Delivery identity、live checkout/branch resolution 与 owner-scoped
  resource cleanup 为一个封闭模型。`.59` 只实现 C2 shared kernel 与 D0 stage-evidence correction；完整方向
  继续由 #454 task design 承接，C3-C7、D443、D436 与 E434 尚未实现或激活。

TARGET 不表示已实现、已测试、已发布或已授权执行。
