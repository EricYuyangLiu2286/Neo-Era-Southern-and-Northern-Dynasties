# CNE 原版来源、实际结算与文本对读

本机1.13.11/build24799966，catalog CURRENT/0 changed。

- 年龄复用 `common/scripted_effects/nesnd_crisis_effects.txt` 的 nesnd_land_months：仅缺值时初始化0，主JE活跃月度+1，暂缓子改革不暂停这个时间。主日志终局关闭，信心yearly按programs_live关闭；既有11个月/1000终档不改。
- 原生 `GAME/common/script_values/command_values.txt:211` 使用floor=yes；嵌套value/min/divide/floor/multiply遵循当前script_value算术。`min`是下限（技能numeric-scale-contract已记录实证），因此负月份按0处理。时间额外扣减与bar使用同一script_value。
- 主日志现有失败：失君主制、信心0、成功政变、原生革命/分离战争、极端危机。极端危机需要样本>=15、失序>=90、连续坏月>=12、动乱>40%、合法性<25，且战争或破产。失序100本身不是独立失败。小于4州为失效。未另造硬到期或修改这些出口。
- 年度账本是源码算术示例，不是引擎时序模拟：假设12/24/...月年结，无战争/项目/事件/暂缓；无执政恢复约第17次结算耗尽，即使每年恢复40也约第25次耗尽。实际会受共和国起义、战争、建设、破产、完成和退出影响，不能把这些年份写成固定死亡日期。

## 文本对读

作者原始样本：`WORK/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:8` 的“推动地权革命”；当前已定进度来源名“革命热情消退”。本轮只补一个短原因标签，不改正文、制度设定或故事。

|条目|候选|检查|
|---|---|---|
|信心额外年耗|改革久拖未成 / Reform left unfinished|直接说明迟滞与扣减，无开发叙事；实际数字由原生yearly_progress显示，不另写长提示。通过。|
|海战当前舰船|进攻方／防御方＋现有舰船数量模板；Attacking/Defending＋同模板|沿原版角色与数量，不显示不可用的PP占位；不是军事能力削弱。通过。|
|海战初始舰船中文|保持原中文句子，UnitsDesc替换为ShipsDesc|与原版英文实际接口及导出一致；没有改写历史文本。通过。|

MCP的false会返回布尔False，验证按工具实际表示读取。按钮ai_chance采用本体 `00_colonial_administration_buttons.txt:40–41` 的value形式；旧Markdown写base与当前实例/Tiger不符，已据实际源码修正。


## 逐键审校补记

作者样本键：`flavorCNE.1.t`，上述原始备份文件第8行“推动地权革命”；文件SHA256 `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`。这是行动/改革主题用语的样本，不将既有AI标签冒称作者原文。海战字段本轮仅修接口并保留原生简短舰船描述，以GAME本身为文本样本。

|语言／键|原文|候选|结论|
|---|---|---|---|
|simp_chinese / `nesnd_cne_conf_delay_desc`|新增进度来源；参考作者“推动地权革命”及现有进度明细|改革久拖未成|通过：简短、作用对应、无开发过程文案。|
|simp_chinese / `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER`|$BATTLE_SHIPS_BREAKDOWN_HEADER$ Attacking with [NAVAL_BATTLE.CalcCurrentAttackerPowerProjection\|*1v] #todo PP#!|进攻方：$BATTLE_SHIPS_BREAKDOWN_HEADER$|通过：简短、作用对应、无开发过程文案。|
|simp_chinese / `BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER`|$BATTLE_SHIPS_BREAKDOWN_HEADER$ Defending with [NAVAL_BATTLE.CalcCurrentDefenderPowerProjection\|*1v] #todo PP#!|防御方：$BATTLE_SHIPS_BREAKDOWN_HEADER$|通过：简短、作用对应、无开发过程文案。|
|simp_chinese / `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER_START_OF_BATTLE`|[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetAttackerNumWantedUnitsDesc, '\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$进攻|[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetAttackerNumWantedShipsDesc, '\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$进攻|通过：简短、作用对应、无开发过程文案。|
|simp_chinese / `BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER_START_OF_BATTLE`|[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetDefenderNumWantedUnitsDesc, '\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$防御|[ConcatIfNeitherEmpty( NAVAL_BATTLE.GetDefenderNumWantedShipsDesc, '\n' )]战斗开始时有$BATTLE_SHIPS_BREAKDOWN_HEADER$防御|通过：简短、作用对应、无开发过程文案。|
|english / `nesnd_cne_conf_delay_desc`|新增进度来源；参考作者“推动地权革命”及现有进度明细|Reform left unfinished|通过：简短、作用对应、无开发过程文案。|
|english / `BATTLE_SHIPS_BREAKDOWN_HEADER_ATTACKER`|$BATTLE_SHIPS_BREAKDOWN_HEADER$ Attacking with [NAVAL_BATTLE.CalcCurrentAttackerPowerProjection\|*1v] #todo PP#!|Attacking: $BATTLE_SHIPS_BREAKDOWN_HEADER$|通过：简短、作用对应、无开发过程文案。|
|english / `BATTLE_SHIPS_BREAKDOWN_HEADER_DEFENDER`|$BATTLE_SHIPS_BREAKDOWN_HEADER$ Defending with [NAVAL_BATTLE.CalcCurrentDefenderPowerProjection\|*1v] #todo PP#!|Defending: $BATTLE_SHIPS_BREAKDOWN_HEADER$|通过：简短、作用对应、无开发过程文案。|

原版 simp_chinese 海战文本SHA256：`ac47ad2ee1692b298946856782ed5ad6d633ea9f0955c8a76d9b6f184cb065e9`。

原版 english 海战文本SHA256：`7644e8ffd6cb62962cd2a41971ef8dbd06adc1ddebf4c2c5d05c762b1257c275`。
