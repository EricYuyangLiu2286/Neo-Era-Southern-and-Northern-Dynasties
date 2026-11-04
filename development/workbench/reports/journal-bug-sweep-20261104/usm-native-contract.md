# USM战后整合与“西省行政”日志：原生接口合同

2026-11-04；Victoria 3 **1.13.11 / Steam build 24799966**。本轮`catalog.py status`为`CURRENT / changed_count=0`。只读当前GAME/MOD与本机引擎文档，不沿用旧任务对玩法的假定；未改脚本、未启动游戏。状态：`SOURCE_RESEARCH / ENGINE_NOT_RUN`。

## 可以直接使用的符号

| 用户对象 | 当前MOD实际键 | 来源 |
| --- | --- | --- |
| 成都 | `STATE_SICHUAN` | [州名:456](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/map/ce_states_l_simp_chinese.yml:456>)；[地图定义:36](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/map_data/state_regions/11_east_asia.txt:36>) |
| 襄阳 | `STATE_XIANGYANG` | [州名:6](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/nesnd_editor_l_simp_chinese.yml:6>)；地图同文件1834 |
| 桂北 | `STATE_GUILIN` | [州名:8](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/nesnd_editor_l_simp_chinese.yml:8>)；地图同文件1867。不要误用`STATE_GUANGXI`。 |
| 荆楚 | `cu:ce_chu` | [文化定义:1480](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/cultures/CE_cultures.txt:1480>)；[文化本地化:21](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/localization/simp_chinese/replace/ce_cultures_l_simp_chinese.yml:21>) |
| 西南 | `cu:ce_xinan` | 同文化定义1648、本地化24 |
| 客家 | `cu:hakka` | 文化定义628，`REPLACE:hakka` |
| 粤 | `cu:yue` | 文化定义978，`REPLACE:yue` |

当前历史三州分别由SIH/HNA/GNG拥有：[00_states.txt:7070、9493、9508](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/history/states/00_states.txt:9493>)。这个初始归属不能代替运行时检查。

## 三项存续debuff的量纲与边界

| 需求 | 已核原生键 | scope/数值 | 结论 |
| --- | --- | --- | --- |
| 整合速度−50% | `state_incorporation_speed_mult` | state类型修正，可由country/JE向本国州传播；候选`-0.5` | 精确对应。修正是加到整合速度倍率上的−50%，不是把当前剩余时间固定乘1.5；无其他修正时速度减半、耗时约翻倍。 |
| 机构行政力成本+15% | `country_bureaucracy_investment_cost_factor_mult` | country；候选`0.15` | 精确对应每个机构投入等级的行政力费用倍率。不是`country_bureaucracy_cost_add`固定花费，也不是全国人口基础行政成本。 |
| 生活水平变化产生的激进派+10% | 本机只有 `state_radicals_and_loyalists_from_sol_change_mult` | state；`0.1`会同时影响SoL变化产生的激进派**和效忠派** | **没有查到只增加SoL激进派的独立原生modifier。不能把这个双向键冒充单向debuff。** |

来源：[引擎modifiers.log:447–450](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/modifiers.log:447>)机构成本；1739–1742整合速度；1875–1878双向SoL。原生实际应用：[00_bureaucracy.txt:186–188](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/laws/00_bureaucracy.txt:186>)用机构成本−15%；[02_event_modifiers.txt:2010–2019](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/02_event_modifiers.txt:2010>)混合country合法性与state整合速度；[天保危机修正:1–7](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/static_modifiers/00_ep2_02_modifiers.txt:1>)的SoL双向+10%由[07_tenpo_crisis.txt:9–11](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/07_tenpo_crisis.txt:9>)作为日志存续修正应用。

**SoL项必须让主任务明确选择：**原生双向+10%可以精确实施但与本次用户“只增加激进派”不完全一致；若坚持单向，当前未证实可精确实现的直接modifier。本轮不擅自替换成政治运动激进派、低SoL固定月增激进派、全国固定增加10%激进派，也不以月度平均SoL差值模型伪称逐次SoL变化的准确增益。双向项是对对应变化产生的人数乘数，不是每月全国人口直接+10%激进派。

## 吞并后整合：state scope及地域约束

原生`set_state_type = incorporated`作用于**state**，不是state_region或country。文档：[effects.log:37157–37159](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:37157>)。完整实际参考为原生[00_victoria_scripted_effects.txt:26–39](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_scripted_effects.txt:26>)：遍历owner-state，`set_state_owner=c:TPG`后`set_state_type=incorporated`；美国内战重建[acw_je_events.txt:202–225](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/american_civil_war/acw_je_events.txt:202>)使用同一接口把明确筛选的州改成未整合。

USM当前镇压成功标记为`usm_government_winner_civilwar`，JE入口[ce_usm_the_last_days_of_ming.txt:345–350](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/ce_usm_the_last_days_of_ming.txt:345>)；当前吞并来源至少有`usm_civilwar.5`、其他战后接受/吞并选项和战争目标原生结算，不能只改一个按钮后宣称所有镇压吞并都覆盖。具体合入应由主任务锁定本轮完整调用集合。

建议在**实际领土转入USM之后**从USM遍历其现有owner-states，筛选批准的大陆中国地区集合，并排除三州，再设置incorporated。不要把“原败方全部州”直接整合：日本、东南亚、远南等外国领地必须保持原状态。对领土转移后可能合并/失效的旧state scope，重新从USM取当前state比继续持有旧scope可靠。

当前可参考的地理白名单是[nesnd_south_chinese_state:1–54](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_politics.txt:1>)，但它**不是严格“大陆”定义**：包含台湾`STATE_FORMOSA`、海南，以及本项目设定下的东北/西域等地。不能凭函数名直接认为满足本次地理范围；应取用户意图对应的明确子集，保留架空地理，不照现代国界新造筛选。已有当地外资、人口文化与建筑不在`set_state_type`这项请求的改动范围。

**例外不等于反整合。**“自动整合除成都/襄阳/桂北外的州”只要求跳过它们，不能自行加`set_state_type=unincorporated`。吞并后三州若已经整合，新JE会马上满足目标；要强制产生三州重建过程必须明确改变既有整合状态，属于额外设计。引擎[annex_as_civil_war文档:552–556](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:552>)仅说继承内战胜利效果，没有公开全部州整合继承规则；不要预先假定这三州一定变成未整合。另有`annex_with_incorporation`明确继承整合，但用它替换当前吞并会改变其他继承语义，不为本目标擅换。

## JE完成条件与修正自动清理

完成需要分别验证三州**全地区归USM**，以及USM对应owner-state已经整合：

- country使用`owns_entire_state_region = STATE_SICHUAN`（其他两州相同）；[triggers.log:13453–13457](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:13453>)。
- state使用`is_incorporated = yes`；[triggers.log:11904–11908](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log:11904>)。应先在独立分支确认`s:STATE_SICHUAN.region_state:USM`存在，再读取；或遍历USM州做相同地区匹配，避免无州时解析空scope。
- 仅`any_scope_state={state_region=... is_incorporated=yes}`不能证明整个地区归属（拆分州可能部分属于外国）；所有权条件不可省。
- 三州失去一个时应继续未完成，直到期限；用户未要求失地即取消，不应通过invalid把debuff免掉。

静态修正定义放`common/static_modifiers`，JE用`modifiers_while_active={ 新修正键 }`。官方[JE文档:348–352](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/journal_entries.md:348>)明确修正应用到JE并传播到country；在JE结束后不再存续。原版[00_impose_law.txt:14–22](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_impose_law.txt:14>)甚至先清同名国家直接modifier，再把它交给JE存续；其complete/invalid处理没有手动移除该存续modifier。[00_reunify_china.txt:8–10](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/00_reunify_china.txt:8>)也用同形字段。

因此不要同时在`immediate`给USM永久`add_modifier`同一debuff，再试图分别在成功/失败/失效清理；那会产生重复或残留。国家灭亡/日志失效时JE承载修正随实例退出；本轮只有源码合同，实际旧档刷新时机仍为ENGINE_NOT_RUN。

## 1850失败：全国四文化各25%，唯一提交点

当前原生country effect：

```text
add_radicals = { culture = cu:ce_chu   value = 0.25 }
add_radicals = { culture = cu:ce_xinan value = 0.25 }
add_radicals = { culture = cu:hakka    value = 0.25 }
add_radicals = { culture = cu:yue      value = 0.25 }
```

这四行应在USM国家scope执行。引擎[effects.log:367–380](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log:367>)说明value是**每个匹配Pop向激进化移动的比例**，culture可用`cu:key`。原版[德国统一:218–225](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/german_unification.txt:218>)在同一国家连续对南德、北德分别调用；[原版global:1098–1100](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/history/global/00_global.txt:1098>)使用明确数值与`cu:han`。

适用范围是USM境内四文化的全部匹配Pop，不限三州/整合州/文化家园，也不遍历其他国家；同一个Pop只有一种culture，四项不会对同一个Pop重复命中。**不是**全国总人口25%平均分给四文化，不是把四文化最终激进派占比设置成25%，也不能保证已高度激进/有效忠派的Pop最终净激进人数都严格增加25个百分点；引擎描述是“更趋激进”，底层忠诚度与上限转换由引擎处理。原生提示同样表述“become more radical”，见[effects_l_english.yml:584–586](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/effects_l_english.yml:584>)。

截止日应使用绝对`game_date >= 1850.1.1`，不要用固定天数timeout冒充1850。当前原版JE日期比较实例：[04_sikh_empire.txt:88](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/04_sikh_empire.txt:88>)。解释按“1850年到来时仍未完成就失败”；若主任务决定包含1850整年，应统一改成1851.1.1，不能模糊两种含义。

唯一实际扣罚入口放`on_fail`里的受保护effect：先检查无`failure_applied`和无成功标记，**先写一次锁，再执行四条效果**；失败通知事件只负责说明，不再执行一次处罚。on_complete/on_fail都写终态，入口/possible排除两个终态，禁止旧档月度补入口再次创建。不要在on_timeout、on_invalid和通知选项重复放四条add_radicals。

成功/失败条件应互斥，并在实际效果再次验终态。若坚持“必须在1850之前完成”，complete同时限制截止日前，fail于截止日后且未已完成；不要让1850后刚整合完的状态与失败同时为真而依赖引擎求值顺序。若日志直到1850后才因晚镇压启动，绝对期限意味着立即面对失败；不能擅自再给相对15年。国家失效出口不发文化处罚。

## 必需的定向检查

- 地理：国内普通州被整合；三例外原状态不被无授权反整合；JAP/南洋/外国区域不变；拆分地区不能假完成。
- 完成：三州完整拥有＋已整合才通过；缺一/部分拥有/整合进行中均不完成；不存在owner-state时安全false。
- 生命周期：只活跃期间有机构成本与整合速度修正；成功、失败、失效后无JE修正残留，且没有第二份country永久modifier。
- 时间：1849.12.31、1850.1.1、晚启动、同日完成边界；成功/失败不双提交。
- 处罚：四文化每项恰一次、非目标文化不变；无该文化时自然无匹配Pop；重复回调/重新add JE/读档不再处罚。
- SoL项：若用双向原生键必须准确说明效忠派副作用；单向精确实现当前未证，不能以静态检查掩盖语义差异。

本报告只给当前原版和MOD来源合同，不将上述检查列为已执行的游戏验收，也不创建新的玩法文件。
