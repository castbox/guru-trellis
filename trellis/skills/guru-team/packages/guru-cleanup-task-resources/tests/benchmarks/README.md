# Cleanup 原公开链测量

这些source-private工具复现#589 D4固定合同，不进入安装inventory。需要选定同一个Python3.14环境、pytest，以及完整matching Fork source checkout；本批固定Fork 2a6f10b/0.7.0-castbox.3。不要使用业务Task或真实资源：工具只删除它创建的临时Git fixture分支。

单组：

```bash
python benchmark_cleanup.py --source /path/to/guru-source --fork /path/to/trellis-fork --output /path/to/new-output --count 10 --mode timing
```

mode为timing/profile/rss/volume；RSS依赖macOS BSD time。加--installed通过原preset installer产生本组代表安装，安装准备在timer外；10/100两档固定唯一head/Task路径数。完整16组：

```bash
python run_benchmarks.py /path/to/guru-source /path/to/new-output /path/to/trellis-fork
python analyze_volume.py /path/to/new-output
```

每组两轮fresh等价fixture，preview、原确认删除及same-input恢复分别计时/计数。无主动预热、warm OS cache、串行执行；不同时运行其他测试/安装。timing包含原launcher和全部客观检查；profile、volume、RSS独立pass。GitHub网络为0，fixture语义不代表nativeAI或远端效果。RSS为wrapper调用单进程峰值与各Git峰值，不是同时进程组总和。

volume保留原始post-delete probe；已删除ref的成功show通过trace退出码与操作前记录的精确Task blob OID/大小补正，见resolved-volume.json，不改timing或输入。其他对象按原OIDprobe。原始/tmp测量工具与本便携版只在Fork/helper定位参数上变化，正文运行及计时方法保持；#589实际before/after使用冻结原工具hash。

失败输出保留，不计通过；解决具体环境/实现错误后使用新输出目录或显式保留旧失败目录。完成结果和阈值由Task performance-contract/results拥有，工具不判断semantic pass。
