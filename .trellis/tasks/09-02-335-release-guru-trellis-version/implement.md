# 实施计划

1. 建立 `.agents/skills/release-guru-trellis-version/` 的短入口和显式链接的 release contract，定义 repo-private identity、最小输入、fresh preflight、两阶段 lifecycle、owner composition、stale/recovery、禁止持久化和终态报告。
2. 同步 Shared/Codex/Claude/Cursor 的 Agent 可读 Skill 文件，保持字节一致；不增加 command/prompt、公共 interface/schema/runtime、marketplace、preset、overlay 或 installed projection。
3. 增加 repo-private contract tests 与 honest-path integration fixture，覆盖单次完整 Branch Review、Publication/Finalizer metadata 不自指、delivery drift stale、private runtime identity stability、独立副作用确认及 public inventory 隔离；补充 Finalizer package 的正常 base 前进回归，并仅在现有 planless route 校验阻断时修复 canonical/current-checkout validator，不改变 public I/O 或 transaction。
4. 更新根 `README.md` 的仓库维护者发布入口，并按 RDT/Architecture owners 创建最小 task-owned contributions；仅在 live owner 判断要求时 promotion shared current authority。
5. 运行 Skill/frontmatter、投影 byte equality、public inventory isolation、reviewed-content identity、honest-path、task context、source/current-checkout drift 与 residue 定向验证；不执行完整累计多平台 Release Gate 矩阵，不创建真实发布副作用。
6. 执行 Phase 2 semantic check；完成最终内容 commit 后执行一次独立完整 Branch Review，再进入 Publication 和 Finalizer。task commit、push、PR create、Finalizer mutation、merge、tag、smoke、Release、Issue closure 和 cleanup 分别展示，且只在取得对应独立确认后执行。
