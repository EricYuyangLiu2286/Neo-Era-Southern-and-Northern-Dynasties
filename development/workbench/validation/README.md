# NESND 全局检查入口

这是源码检查、真实 MCP 查询和已采集原生证据的编排器。它不模拟 Clausewitz，不启动游戏、不按键、不改候选、不重置人口基准。

```powershell
& 'D:/ProgramData/anaconda3/python.exe' -X utf8 `
  'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/tools/global_validation_runner.py' `
  --candidate 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/debug-naval-20261031-e1' `
  --baseline 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/exports/integrated-preview-20261031-c5' `
  --runtime-run 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/runtime/20261031T230637Z/run.json' `
  --engine-collector 'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/plans/two-empires/evidence/batch-probe-e1-existing-manifest-check.json'
```

默认在 `WORK/validation/runs/<UTC>-<candidate>/` 写唯一新目录。退出码0=全部要求检查PASS；1=有FAIL；2=没有FAIL但仍有要求项NOT_RUN。流程完成可以返回1，不能把“跑通”改成“全部通过”。每项记录执行状态、PASS/FAIL/NOT_RUN、STATIC/MCP/ENGINE_EVIDENCE层次、用时、报告SHA和能力边界；`progress.json`在每项完成后落盘，可从中恢复断点。

默认要求简中本地化。若本轮明确要求英语，一并传 `--language simp_chinese --language english`；不暗中把补完英语翻译当成debug要求。MCP默认实际运行，`--no-mcp`会明确NOT_RUN。没有实际engine collector时，原生探针NOT_RUN，绝不自动打开游戏。

当前工具链已冻结在 `toolchain-frozen-current.json`（19项）。runner启动会核该清单，结束还会核整轮工具SHA是否变化；修改中的checker不能被当作一次可复算的通过记录。新的工具修正须先局部回归、明确重建冻结清单，再跑最终整合候选；不并行反复重跑各个仍在修改的分支。

## 复用入口与覆盖边界

|检查|复用代码/适配器|可证明与不可证明|
|---|---|---|
|版本指纹|skill scripts/catalog.py status|当前安装版本和源索引是否变动；不自动refresh或更新Steam|
|有序语法/历史/PM|skill scripts/pdx.py、audit.py|保留重复块，历史归属、显式PM与建筑组匹配；不计算运行经济|
|全定义生产/资源|tools/validate_production_links.py|补全未被开局选用的建筑→PM组→PM，以及地图资源/traits的字面引用|
|固定人口边界|tools/population_envelope_audit.py|作者原MOD+冻结原版的固定781地区±25%；新州按原地理合计，不能新键绕限制|
|依赖图|tools/dependency_graph.py|源码影响路线与来源行号；不是谓词可满足性或全部剧情的可执行图|
|事件/JE/button/loc/media|tools/validate_content_closure.py|有定义的字面闭包；动态scope、运行时参数、声音/授权范围另列待验|
|地图全域|audit_global_naval_exits.py、map_transport_preflight.py|全出口编号/真实像素边界/网络结构；显式保留已审本体视觉例外，不假称全世界舰队实测|
|Tiger|tools/tiger-1.19.0/vic3-tiger.exe|实际执行，基线差异与窄范围源码/原生反证；未知告警不因未增加而豁免|
|语义缺口登记|validation/review-register.json|已审P1按相关源SHA绑定；代码变动后变为NOT_RUN待复核，不自动清绿|
|MCP|mcp_candidate_probe.py + 已有stdio server|实际initialize/list_tools/init_game(vic3)/get_structure；不会执行游戏事件|
|原生批量探针|qa_batch_probe.py collect + classify_batch_probe_evidence.py|只认精确候选/挂载probe/实际run/完整日志周期绑定；旧PASS不能认证新候选|

没有调用那些会直接写候选、改技能或复制发布包的旧专项 `validate_integrated_*` 脚本。专项历史证据仍有用途，但其硬编码父版本和副作用不能直接当通用只读检查。

Tiger为每轮在报告目录生成独立`.conf`：主语言检查、`load_mod`按只读绝对路径加载共同开启的EAC、保留loaded-mod诊断。实际stderr、命令、配置及SHA写进报告；没有把素材复制到候选。`line/from=null`是已实测的Tiger JSON合法情况，适配器已用真实985条/11个nullable记录做局部回归。

历史132次省色重赋与4投资人重复已按**精确源码SHA+E1原生证据**分类：38条本体同类顺序覆盖、94条保留作者最终结果的非阻断备注、4项同身份覆盖冗余。它们不是实际双属或应相加的15级建筑。原生四楼实际合7级；不改历史凑绿。来源漂移或新重复不会自动继承这项分类，会转NOT_RUN复核。

## 发现错误后的流程

先集中阅读源文件及图关系，给每项确定影响闭包；批量修独立候选，再跑本入口。先处理语法、丢失引用、人口超界和已证语义BUG，再做针对性实机；实际新错误回写源码/门禁反例后重跑。MCP和Python输出不替代首次hover、事件选择、走时、舰队到达、战争与存读档。

`review-register.json`的一次性E1登记保存已审地图例外和已知发布阻断的原始证据副本。不得重复运行initializer把新候选当原始基准，也不能把某条告警类整体加入忽略列表。新审查必须更新具体来源SHA、原因和证据；人口基准属于另一套固定审计，始终不随本登记变化。
