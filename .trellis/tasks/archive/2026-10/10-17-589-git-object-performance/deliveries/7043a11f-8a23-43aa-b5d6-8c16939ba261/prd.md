# D8 正式工具采用与最终集成验证

原 Task `589-git-object-performance` / generation 0 继续当前 #589 accepted scope。D1–D7 实际交付保留；D7 已通过 PR604 合入 main，候选 `1cee58a6db1b9837054c6ce8582fb6c0bf9e55b8`，merge `9a10cb54c4a7eb8016d52b9bd5c3c2ec7de31807`。本批不再修改性能机制，不以预设耗时或RSS数字驱动优化。

本批消费 D7 clean committed canonical source，经原 `guru-upgrade-tools` 的 `source_locked` 操作，分别更新原 Task checkout 与正式代表 `/tmp/guru-589-installed-20261017`。来源必须匹配 Fork `9f40ec70914f98fce2619560274cc1d0619f2f7e` 和 CLI/Core `0.7.0-castbox.4` 的完整配对。维护只写 tools/workflow/Guru投影及checkout-local Python pointer，保留 Task、规划、archive、session、workspace 和 peer/common pointer；不 patch 上游脚本或迁移历史 Task。

必须取得两个目标各自的实际 receipt、CLI/Core/source/API、native 和适用平台/mode/reapply/drift/sidecar 证据。代表candidate或源码fixture不代替最终目标采用。D7 的同输入16cell before/after 与历史失败按实际代码和依赖适用后承接，不重复无影响矩阵、不挑样或把旧FAIL改为PASS。

本批发布真实 Refs-only PR 后，按已审核的同一 merge 方法完成真实手动合并；首次通过原 `delivery_merged_recovery` 记录该未记录的实际结果，并检查 stdout 丢失后的同结果恢复。随后通过 query2 验证当前 Task 的全部实际 Delivery、固定截点及无重复事实。不得用正常merge owner已记录的短路恢复冒充新手动入口。

最后收敛完整优化/保留清单及全部AC证据，原 Completion 重新判断整体。PR合并不代表Task完成；只有整体通过后才Closure/Finish和适用收尾。#575完整Release矩阵、Guru版本发布、npm发布和业务仓采用不在本批范围。
