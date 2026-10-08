# #503 设计

## 根因与职责
唯一性只需合法id/ref，却复用完整current/legacy分类。按consumer拆分读取，不扩大白名单、不新增索引或持久状态。

- D503-CLASSIFY：复用JSON/object/canonical locator与id normalization，提供仅含id/ref的reservation投影。占用不读取source/generation/status语义；坏活动身份具体拒绝，archive/branch缺损保留既有策略。
- D503-RESERVE：composition保留worktrees/branch history/ledger扫描范围；先比较身份与唯一性，selected resolution再严格current校验。task_inventory与upgrade inventory/disposition保留完整分类。创建后完整校验不变。
- D503-DIAGNOSTIC：保留旧候选中有独立价值的最小blocked/invalid_task_state locator/remediation，同一stop consumer解释当前失败；不保存扫描历史、授权、session identity或恢复状态。旧最小输出与created/refresh_review兼容。
- D503-DISTRIBUTION：正式Fork lock集成5c760463680ffc10a3f26957b330c57a4b0c3ff8，fresh核对parents/tree和成功main CI 37735554354；CLI/package manager轴不变。必要pin文档、dogfood官方投影、apply、compatibility matrix和实际clean安装一致。
- D503-EXIT：Guru shared identity/composition独占本地substrate；Fork writer已由#29修复。完整migration分类保持其owner与退出条件；不新增迁移器或历史写入。旧classifier有inventory/migration消费者则保留原合同，仅删除已无消费者的占用分类。

## 架构与取舍
承接design constitution v1的职责内聚、最小必要复杂度与债务收敛，以target_native consumer读取分离实现。ARCH-CUR-049/ARCH-DOM-034/ADR-017/018的current-only与单写责任不变；task贡献由正式Architecture owner重审，无新增无消费者ADR。

扩大白名单仍耦合无关字段且无法解除Fork第二层；吞异常丢失占用；全量迁移扩大业务写入，因此不采用。canonical是长期源头，不patch Backend安装或node_modules。

## 验证边界
合法id只改变非身份字段时占用不变，直接选择无效目标仍拒绝。正式source/installed create/ensure/bind证明根因解除；资源无半创建、历史bytes/modes保全。完整Release和Backend升级/部署另属各owner。
