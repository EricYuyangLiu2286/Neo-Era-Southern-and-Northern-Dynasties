# 鸦片出口事件的目标市场闭包

父：冻结 `integrated-gameplay-20261031-e`。候选：`opium-target-scope-20261031-a`。自然 run153444 16:17:27 的4条错误已证明 .1.b 访问未保存的 opium_addict_country，不是单纯静态警告。

## 根因与来源

MOD `REPLACE:je_opium` 完成要求外国市场 exports≥200，调用独立 namespace 的 `ce_opium_events.1`；后者 immediate 却筛 exports≥600。200–599时可以完成JE，却不能保存被引导消费的国家和文化。option b 无资格检查，AI可选，随后在 empty scope set_variable。

当前 GAME `common/journal_entries/00_opium.txt` 与 `events/opium_events.txt` 使用一致的 **imports≥200**；目标是消费进口鸦片的外国市场。本MOD没有覆盖同名 native event，`ce_opium_events`自成namespace，只将原 JE completion 改接自定义事件。错误是筛选条件漂移及进出口方向反转，不是未挂载本体事件。保留作者新增的目标国禁烟日志，不把它改回原版直接添加文化obsession。

## 实施

1. 独立脚本 trigger 统一目标市场：非root市场、imports≥200、市场主国存活、未经历本campaign、未有待处理/进行中的同campaign，至少一种主流文化尚无鸦片obsession。
2. JE complete 和事件 immediate 复用同一个市场trigger。事件保存实际 market、其owner和真实culture，杜绝200/600不同步。生产建筑条件保留原版/作者的盈利、配员、储备、级别门槛。
3. .1.b 的可用性及执行时再次核对已保存国家/市场仍匹配、市场进口/待处理状态仍合法。全部目标效果和出口奖励在同一个条件内执行；不把无目标操作包装成成功。不改成随机任何国家。
4. .1.a 生产路线保留。若事件展开后目标灭亡、换市场主或进口消失，出口诱导项不可用，玩家/AI仍可走生产路线。原事件duration/default option不改。
5. .2 仍发起作者禁烟JE，后续成功/失败/invalid和阶段事件保留。目标pending变量阻止多出口国同时重复发起同一campaign。

## 验证

静态：共享trigger只定义一份；complete/immediate同一调用；其余事件及本地化/地图/经济数据不改；新txt BOM。Tiger新增符号与scope检查。

实机：需有盈利配员达标的鸦片种植园和外国imports≥200，JE完成→.1→选b→目标一天后.2→真实JE出现且仅一次；199不完成/不选目标，200–599可完整执行，600以上仍可；.1.a生产正常。展开后目标灭亡/更换市场或进口下降时，只能选择仍有效的生产路线且无export奖励/empty scope。不同出口国同时选择同目标不得重复进禁烟JE。不能通过伪造scope变量当作真实市场测试。

Nov15 CNE存档单独提取，累计QA后财政变化不用于重平衡主参数；该存档为非自然互斥选项组合，clock fixture只改三个计时/进度变量，民生条件保持真实。
