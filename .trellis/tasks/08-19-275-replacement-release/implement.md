# 实施计划

- 复现 exact-tag `verify_installed_closeout.py` 归档后 public invoke 回归。
- 修复 canonical `guru-finalize-task` runtime/contract/schema/tests，同步所有声明平台副本。
- 修复 `verify-throwaway-install.sh` inventory 派生和相关测试/文档。
- 运行 focused package/runtime/closeout、source/dogfood/installed drift 与模式检查。
- 推进 canonical extension revision 到 `0.6.5-guru.36`，准备 `v0.6.5-guru.10` public mapping 与 release notes，不预填未知 peeled commit。
- 执行 exact candidate cumulative Release Gate；在独立 review 与用户确认后才提交、合并、打 annotated tag/Release，并做 tag-pinned smoke/downstream gate。
