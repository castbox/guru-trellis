# #694 双向追踪与替代边界

适用 Git `2dbaf308e6d5137bf640cfe546a078497c1c713a`，authority `guru-trellis-rdt`；Architecture `docs/architecture/README.md / guru-trellis-architecture / active`。proposed 镜像最终路径，内部相对链接按目标路径解释。

| 整体 accepted scope | requirement | design | test |
| --- | --- | --- | --- |
| R694-01/02/03/05；AC01/02 | R694-01，保 R679-02 | D694-01 | T694-01/02 |
| R694-04/06；AC03/04 | R694-02，保 R679 其他职责 | D694-02 | T694-02/03 |
| R694-07；AC05 | R694-02 | D694-02 | T694-04 |

只替代 R679-01/D679-01/T679-01 中独立 final_plan 一律先持久绑定/选择的部分。正常执行、其他 Architecture stage/purpose、原 writers、首失败、scope/freshness、独立读序和所有其他条件保持；没有 public schema、DTO 或持久格式变化。完整 proposed 供原候选 Architecture/Check；原 RDT promotion 才写 shared current 并读回，实施重绑 actual candidate 后最终 Check/Review。
