# #260 Design contribution

- `DES-014`：matrix runner 以单 cell executor + compact aggregator 组成；每个
  cell 使用独立 repo、npm prefix 与 runtime root，并输出版本、平台、场景、
  inventory comparison、sidecar 和 installed-smoke 结论。runner 以 HEAD、tracked
  delta、untracked path/mode/content 与 isolated-index candidate tree 形成 source
  identity，并要求 matrix 前后 identity 不变。
- `DES-015`：平台集合由 canonical/installed manifest、ownership claims、overlay
  entries 与 registry destinations 交叉验证；任何集合漂移 fail closed。
- `DES-016`：capability projection 按 `distribution`、`skill_api`、`workflow`、
  `task_data`、`docs_authority` 排序比较；distribution 同时比较 Skill package、普通
  managed asset 与 overlay executable mode，Docs authority 冻结 recursive `docs/**`
  且四个 domain 都必须含 versioned body。只有真正的 version fields 可隔离比较，
  extension identity 漂移独立阻塞。
- `DES-017`：dogfood 先执行 official update，再 preview/switch workflow，最后
  reapply preset；`.new/.bak` 必须逐个审查并归零。
- `DES-018`：A/B lifecycle verification 是 compatibility harness，不新增
  Acceptance/cleanup public Skill 或 typed exit；真实 A provider evidence 与本地
  failure/reachability evidence分开记录。A archive 后必须通过 installed history
  preview 得到唯一 non-empty PR candidate，并绑定其 `finish-summary.json` locator。
- `DES-019`：`preview-change-context-history.sh` 是 package-private validator
  wrapper；平台 public projection 只发布 `scripts/invoke.sh`，并显式验证 private
  wrapper 不泄漏到 `.agents`、Codex、Claude、Cursor。
