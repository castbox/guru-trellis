# D2 实际整合后的 bounded continuity 对象读取

Direct Source：https://github.com/castbox/guru-trellis/issues/589 第3.3第二项、第5–8节；整体accepted scope见Task根prd.md。D1已交付PR#593，不重复其收益。

本批改进原guru-review-branch tree_identity：同一调用内相同blob只请求/计算内容hash一次，按原路径顺序保留每条摘要贡献；预先完成普通文件request，以单向stdout pipe和不大于1MiB分块处理内容、普通文件stderr保留错误，避免整批内容常驻及response整批落盘后重读；消除record及同进程validate对同一不可变tree/同规则摘要重复计算。保留gitlink、symlink、文件mode原语义、正常缺失/读取失败以及每份输入独立检查。复用绑定真实repo与immutable tree，仅调用内；独立recorder/checker/invoke各次重新确认。

实施前由原正式schema2 bounded continuity链完成1000/10000路径高重复与10000 unique（含16MiB对象）before，两次同口径，固定耗时和RSS标准后再改生产。验证record/check/invoke及原consumer，保留实际整合后当前Check与完整BranchReview义务，不把bounded结果当完整Review。覆盖新旧摘要一致、调用内去重/复用、相邻可变输入刷新、正常错误和受管安装投影。

本批独立交付后仍剩D3生命周期/全流程计数与联合回归、官方Task创建和重复hash上游前置；不能关闭#589，不执行完整Release矩阵。
