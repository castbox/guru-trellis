# 实施与验证计划

1. 为runtime locator、完整identity、common-dir default/worktree override pointer、用户cache与迁移增加测试。
2. 重构canonical `bootstrap.py`，统一路径计算、bootstrap、activate、validate与错误payload。
3. 简化 `resolve-python.sh`，通过bootstrap只读resolve入口执行受管解释器。
4. 更新preset installer的prepared/active interpreter解析，消除repo-local路径假设。
5. 更新README与workflow/preset spec，并同步canonical到dogfood managed copies。
6. 运行runtime与preset targeted tests、source/installed validation、apply/reapply、dogfood drift和sidecar扫描。
7. 在隔离临时repo中执行main checkout apply -> linked worktree wrapper lifecycle，重放 `EXT-222-001`；并验证两个linked checkout顺序apply不同identity后仍分别解析自身runtime。
8. 验证runtime unit suite只写临时repo pointer，current checkout wrapper不继承测试cache override，且suite前后caller pointer bytes不变。
9. 执行 `guru-check-task`、创建reviewed commit、Branch Review、publication、PR与merge。
10. 合并后更新#222 prerequisite并从fresh `origin/main`重新冻结candidate；旧发布证据全部作废。

任何正式验证失败均停止后续PR/merge或#222 tag动作。
