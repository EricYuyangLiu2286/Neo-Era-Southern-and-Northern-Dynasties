# 52 日本国政之争显示修复与朝鲜子方案

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: root
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [检查、差异与方案](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/jp-politics-ui-20261107/>)

## 现象与期望
进度悬停只有“当前无进度”，方针效果为空，冷却和费用不明，变量与国家条件重复。作者确认保留目标/数值，三个方针常显，已选也显示下一步，改换代价明确；不开游戏。

## 原因
命名script value中的内部条件不进入1.15进度明细；月结变量与条各有写入。按钮整段效果由可用条件if包裹，冷却时预览分支为空。资格展开显示内部变量和国家枚举。

## 改了什么
- common/journal_entries/nesnd_jp_politics.txt：入口国家和资格各一句，失败条件改可读提示。
- common/scripted_buttons/nesnd_jp_politics.txt：方针常显；当前/未选if-else提示独立于隐藏执行守卫；冷却、费用、清零与下一步常显。
- common/scripted_progress_bars/nesnd_jp_politics.txt：四项原生progress_condition；条是唯一月增量写入者。
- common/scripted_effects/nesnd_jp_politics.txt：月结只回读条到既有变量，保留12个月达标检查。
- common/script_values/nesnd_jp_politics.txt：增加分开的战争/激进派读数。
- localization中英nesnd_japan文件：零值也显示的四来源、状态、费用、下一步及冷却文本；BOM与键集合核对通过。

## 怎么复测
关闭并重新启动游戏后，可先读原观察者存档检查显示；主验收用新开局（不新增旧档迁移）。未选时三按钮效果都有路线收益/目标；已选按钮灰显且写当前方针；其他按钮冷却期间灰显，约N个月与清空进度明确；冷却结束付费改换只扣一次、进度和连续达标月数归零。条悬停四来源含0，行政+0.5、全目标+2.5、战争−0.5、激进派≥25%−0.5；月界只结算一次。

## 遗留问题
实际UI排版、月份公式及月界/保存重载未经引擎验证。月份为到期剩余天数÷30的一位小数近似值，沿用原12月到期变量。Tiger为1.13.5检查器，不能识别1.15 progress_condition；依据本机1.15文档使用，不能称Tiger零报错。任务31政治内容厚度、朝鲜既有常驻治理缺少阶段结局仅记录，不本轮扩改。
