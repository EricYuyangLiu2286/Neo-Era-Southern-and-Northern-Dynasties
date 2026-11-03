# CNE 信心、暂缓改革与按钮说明研究

2026-11-03。研究对象为当前主 MOD；未修改主 MOD，未启动游戏。以下实现块是候选提案，不能称为游戏内验证。当前源码目录索引 `catalog.py status`：Victoria 3 **1.13.11 / build 24799966 / CURRENT / changed_count 0**。

目录缩写：

- M = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`
- G = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`
- W = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench`

## 结论与本次范围

1. 将信心的**负项**减半：基础 −50→−25；土地商品化 −10→−5；国家城市化 −10→−5；每省营产整顿 −10→−5；战争 −50→−25；激进派超过15% −40→−20；破产一次 −500→−250。四类执政集团各 +10 保留。保留信心上限1000、共和派500门槛、归零失败、已有进度和所有历史标记。
2. 添加信心日志中的一次性“暂缓诸项改革”：至少一项改革正在推行、信心不高于900时可用；停止现有土地、城市及营产改革，恢复100信心，并用六个月的原生到期变量禁止重启。永久领取标记防止反复开关刷取。六个月是本轮平衡选择，不是原版强制值。
3. 不把奖励接入 `nesnd_land_suspend`：它实际上打开**永久结束**地权革命的确认事件。该按钮条件中的“尚未结案”改成“地权革命仍在进行。”
4. 修复当前按钮预览的两条泄漏路径：`possible` 展开生命周期检查；`effect` 的 `if.limit` 再次展开同一完整检查。内部初始化、存档、终局守卫放 `hidden_trigger`，实际改动在保留执行检查的 `hidden_effect` 中进行；真正的技术、建筑、资金和暂缓期资格继续独立显示。

## 一、当前完整链条

### 信心的权威状态与结算

|来源|作用|
|---|---|
|M/common/script_values/nesnd_cne_confidence.txt:1–17|项目计数和全部年度信心公式；年度总量调用同一组单项值。|
|M/common/scripted_progress_bars/nesnd_cne_confidence.txt:1–21|原生0–1000进度条；`yearly_progress` 逐项调用同一组公式，提供悬停明细。|
|M/common/journal_entries/nesnd_cne_confidence.txt:8–10|初始化/同步；**本条JE**年度脉冲调用 `nesnd_cne_confidence_yearly`。|
|M/common/scripted_effects/nesnd_cne_confidence.txt:9–42|变量仅在不存在时初始化1000；年度更新国家变量；周度破产监视；clamp；绝对同步bar；500门槛。|
|M/common/journal_entries/ce_cne_land_draft.txt:33–39,58|父JE以信心耗尽/废除君主制/政变/原生内战/极端危机失败；周度调用信心监视。|
|M/common/scripted_effects/nesnd_cne_republic.txt:1–27|500触发调用仍须有适当地区、NRP不存在等资格；成功生成共和军后才设置 `nesnd_cne_republican_rose`，不反复起义。|

原生bar先执行年度增量，随后同一JE年度脉冲更新国家变量并绝对设定bar；不是把已增长的bar再次读回。减半单项 script_value 即同时影响实际年度结算与原生明细。**不要再改总量乘0.5，否则四项正收益也会缩减，并可能把负项重复减半。** 同期引擎实际调用顺序本轮未运行验证。

当前年度式，L/U 为是否开启土地/城市改革，C 为营产省数，W 为是否交战，R 为激进派人口占比严格大于15%，G 为四个指定执政集团的数量：

```text
旧 Δ/年 = -50 -10L -10U -10C -50W -40R +10G
新 Δ/年 = -25  -5L  -5U  -5C -25W -20R +10G
G ∈ {0,1,2,3,4}：知识分子、小市民、工会、实业家；只要求执政，当前公式不要求其支持度为正。
```

所有年度项以 `nesnd_cne_programs_live` 为守卫。全部改革暂停时，父JE/信心JE仍活动，基础消耗、战争、激进派和执政集团项继续结算。旧和平暂停最佳为 −50+40=−10/年，因而不可能自然净恢复；新和平暂停时三集团可 +5/年、四集团可 +15/年。如果正收益也减半，最佳仍为 −5/年，失去用户所需的恢复空间。

破产在 `nesnd_cne_confidence_watch` 中：有 `declared_bankruptcy` 且无 `nesnd_cne_bankruptcy_charged` 才扣一次；破产修正消失后才清除此防重复标记。因此是“每次破产惩罚持续期内一次”，不是每周扣，也不是全局只扣一次。旧档已扣的500不应退款、重算或清旗；新扣款改250即可。当前源码没有独立的“破产扣500”玩家本地化，不要误把起义500门槛也改成250。

### 改革速度和实际代价

M/common/scripted_effects/nesnd_crisis_effects.txt:1–3 初始进度25、失序20；:15–53 第4个月度样本起计进度；M/common/script_values/nesnd_cne_bar_values.txt:1–14,52 给出：

```text
月进度 = 0.25L +0.35U +0.05C
从25到100的纯进度期 ≈ 3个月预热 + ceil(75/月进度)个月
```

以下为**源码估算**。假设从开始始终维持同一组合、无随机事件增减、无项目被领土变更清除；年度门槛列为自1000起的年度扣款次数，而不是保证日期。共和国500是尝试生成门槛，实际还须通过地区资格。成功另须连续12个月健康条件，可以与积累进度重叠。

|恒定情形|月进度|纯进度月数含预热|旧年净值|新年净值|旧到500/0的年度次数|新到500/0的年度次数|
|---|---:|---:|---:|---:|---:|---:|
|和平，只土地，G=0|0.25|303（25.25年）|−60|−30|9 / 17|17 / 34|
|和平，土地+3省营产，G=0|0.40|191（15.92年）|−90|−45|6 / 12|12 / 23|
|截图：战争，土地+3省营产，G=0|0.40|191（15.92年）|−140|−70|4 / 8|8 / 15|
|和平，土地+城市+3省营产，G=0|0.75|103（8.58年）|−100|−50|5 / 10|10 / 20|
|和平，土地+城市+3省营产，G=2|0.75|103（8.58年）|−80|−30|7 / 13|17 / 34|
|和平，土地+城市+22省营产，G=0|1.70|48（4年）|−290|−145|2 / 4|4 / 7|
|战争且激进派超15%，土地+城市+22省，G=0|1.70|48（4年）|−380|−190|2 / 3|3 / 6|

截图的 −140 精确分解为 −50基础 −10土地 −30三省 −50战争；新值为−70。减半并不保证全程战争、低改革速度也能顺利成功：成功本来要求和平，战争结束后的−45及政府组合能进一步缓解。不能将表格当作实际游戏成功率。

土地/城市/营产目前没有开始时的直接国库扣款。其代价及收益见 M/common/static_modifiers/nesnd_cne_programs.txt:1–28 与 M/common/scripted_effects/nesnd_cne_programs.txt:24–40,495–498：

- 土地：地主支持−2、乡村支持−1，地主吸引力−15%、实业家吸引力+15%，立法成功+5百分点，最低工资+5%。
- 城市：教士支持−2、实业家支持−1，小市民吸引力+15%，立法成功+5百分点，最低工资+5%。
- 每省营产：该省农业/矿业吞吐+10%，税容/建造+10%；全国军队支持−1，每位在职陆海军将领忠诚−1。多省叠加，22省等于−22支持与−22忠诚，不能把最大进度当作无代价推荐。
- 所有营产停止函数都负责移除本省国家惩罚、州修正和登记名单中人物的对应惩罚。调用共用函数能保留当前所有权/人物清理逻辑。

主JE成功条件另见 M/common/journal_entries/ce_cne_land_draft.txt:14–31 和 common/scripted_triggers/nesnd_cne_reform.txt:16–49：至少4州、君主制、合法地权法、学校2、识字48%、非负政力、和平、无破产修正、就业/民生条件、进度100、12健康月、失序<50。此次**不改**这些条件、项目收益、月进度、起义/终局规则。

## 二、内部条件泄漏的根因

M/common/scripted_buttons/nesnd_cne_programs.txt:313,318 的土地/城市暂停按钮直接以 `possible = { nesnd_cne_programs_live = yes }` 显示条件。其展开链是：

```text
nesnd_cne_programs_live (triggers/nesnd_cne_programs.txt:1–9)
  → num_states、schema/running、父JE、terminal标记
  → nesnd_reform_active (nesnd_cne_reform.txt:10–15)
  → NOT nesnd_cne_reform_failed (nesnd_cne_confidence.txt:14–22)
      → extreme_crisis (nesnd_cne_reform.txt:103–112)
      → coup_has_succeeded (nesnd_cne_programs.txt:223–230)
      → monarchy / native_civil_war / confidence_exhausted
```

这正好包含用户所见的内部变量、`country_turmoil`、合法性、revolution/secession外交博弈等。`country_turmoil` 本身是有效的国家人口加权动乱触发器，见 W/references/engine-docs-1.13.11-20261031/triggers.log:9474–9479；不是为修UI而删除其机制。

此外48个项目启停按钮均有显式 `effect = { if = { limit = { nesnd_cne_programs_live... } ... } }`。隐藏possible并不会隐藏效果预览中的limit，调用的start effect又会再次展开ready。22个营产停止按钮的possible还直接显示本省active变量。必须覆盖两条路径；只给内部变量取中文名不是根治。

原生依据：

- G/localization/english/interfaces_l_english.yml:11457 的 `SCRIPTED_ACTION_TOOLTIP` 同时调用 `ScriptedButton.GetPossibleDesc` 和 `ScriptedButton.GetEffectDesc`。
- G/gui/journal_entry.gui:213–230 挂载按钮；:988–1019 使用该tooltip与执行入口；:246–260用 `GetPeriodicProgressBreakdown` 显示原生进度明细。
- G/common/journal_entries/05_balkan_wars.txt:6–13 挂载原生研究开始/停止按钮；G/common/scripted_buttons/00_balkan_wars_buttons.txt:144–173 的停止按钮把实际修正资格保留可见，把内部成员/JE标记放hidden_trigger，并给真实五年期限自定义提示；所移除修正定义在 common/static_modifiers/content_4_modifiers.txt:699，名称/条件分别在 localization/english/ip3_serbia_l_english.yml:272,281,416。
- 同一原生buttons文件:430–474 使用hidden_effect隐藏内部外交操作，再用custom_tooltip呈现必要后果；:295用 `set_variable = { name = ... months = 72 }`。
- W/references/engine-docs-1.13.11-20261031/effects.log:9693–9696 定义hidden_effect“效果不显示”；triggers.log:11002–11005定义hidden_trigger。它们都不是对象安全或短路保证。所有实际效果依然重新检查资格。
- G/common/scripted_progress_bars/scripted_progress_bars.md:20说明bar周期更新先于JE脉冲；G/common/scripted_progress_bars/00_great_game_progress_bars.txt:8–21 是年度具名变量增量；调用者 common/journal_entries/00_player_objectives_great_game.txt:9，变量维护 common/scripted_effects/00_victoria_great_game_scripted_effects.txt:199,330–332。原生未提供本MOD的恢复平衡方案；这里只借接口与显示链。

## 三、可直接实施的候选块

以下为完整候选定义/替换形状。应在根代理候选副本执行；现有文件编码和换行保留，新脚本用UTF-8 BOM。

### 3.1 数值

在 M/common/script_values/nesnd_cne_confidence.txt:8–13 只改对应常量：−50→−25，−10→−5，−40→−20；:14–17 四项+10不改。

在 common/scripted_effects/nesnd_cne_confidence.txt:17 把扣款改为 `add = -250`。**不改**:22 的500起义阈值，不改1000初始化/clamp。

中英文 `zzzzzz_nesnd_cne_programs_l_*.yml` 中 `nesnd_cne_land_start_tt`、`nesnd_cne_urban_start_tt`、`nesnd_cne_camp_start_tt` 的最后一句年度信心10改5；其他数值逐字保留。

### 3.2 安全谓词（加入confidence触发器文件）

```text
nesnd_cne_reforms_in_progress = {
 OR = {
  has_variable = nesnd_cne_land_program
  has_variable = nesnd_cne_urban_program
  nesnd_cne_active_camp_count > 0
 }
}
nesnd_cne_respite_confidence_ready = {
 trigger_if = {
  limit = { has_variable = nesnd_cne_confidence }
  var:nesnd_cne_confidence <= 900
 }
 trigger_else = { always = no }
}
nesnd_cne_respite_ready = {
 nesnd_cne_programs_live = yes
 nesnd_cne_reforms_in_progress = yes
 nesnd_cne_respite_confidence_ready = yes
 NOT = { has_variable = nesnd_cne_respite_used }
 NOT = { has_variable = nesnd_cne_respite_active }
}
```

`nesnd_cne_active_camp_count` 已有缺值0守卫，见 common/script_values/nesnd_cne_programs.txt:19。信心比较必须维持独立 `trigger_if/trigger_else`，不可改成并列 `has_variable` 与 `var:` 比较。

### 3.3 六个月重启锁（替换现有共同入口）

```text
nesnd_cne_program_can_start = {
 nesnd_cne_programs_live = yes
 NOT = { has_variable = nesnd_cne_respite_active }
 trigger_if = { limit = { is_ai = yes } nesnd_cne_ai_program_safe = yes }
}
```

现有land/urban start_ready及22个camp ready均调用该入口，实际start效果又调用ready，因此玩家按钮和维护中的AI都不能绕过。不得改 `nesnd_cne_programs_live` 来实现暂停，否则子JE会invalid，年度计分及历史恢复逻辑也会受影响。六个月后仅允许重启，不自动重开此前项目。

### 3.4 恢复effect（加入confidence效果文件）

```text
nesnd_cne_take_respite = {
 if = {
  limit = { nesnd_cne_respite_ready = yes }
  set_variable = nesnd_cne_respite_used
  set_variable = { name = nesnd_cne_respite_active months = 6 }
  nesnd_cne_stop_all_programs = yes
  change_variable = { name = nesnd_cne_confidence add = 100 }
  clamp_variable = { name = nesnd_cne_confidence min = 0 max = 1000 }
  nesnd_cne_confidence_sync = yes
  nesnd_refresh_land_display = yes
 }
}
```

直接复用 common/scripted_effects/nesnd_cne_programs.txt:499–525：先land_stop/urban_stop，随后22省camp_stop，最后refresh count。**不要**调用:526的programs_cleanup（会清running和拨款等）；也不要land_freeze/land_cleanup（永久完成锁）。新永久变量 `nesnd_cne_respite_used` 不在init、cleanup、终局或读档恢复中删除；新到期变量只由引擎六个月到期自然清除，不在每月重设。先设置used再发奖励。旧档现有confidence/进度/共和国/破产标记全部保留。

### 3.5 专用按钮（新增buttons文件或现有confidence按钮文件）

```text
nesnd_cne_respite_button = {
 name = nesnd_cne_respite_button
 desc = nesnd_cne_respite_button_desc
 visible = {
  nesnd_cne_programs_live = yes
  nesnd_cne_reforms_in_progress = yes
  nesnd_cne_respite_confidence_ready = yes
 }
 possible = {
  hidden_trigger = { nesnd_cne_programs_live = yes }
  custom_tooltip = {
   text = nesnd_cne_respite_unused_tt
   NOT = { has_variable = nesnd_cne_respite_used }
  }
  custom_tooltip = {
   text = nesnd_cne_respite_over_tt
   NOT = { has_variable = nesnd_cne_respite_active }
  }
  custom_tooltip = {
   text = nesnd_cne_respite_programs_tt
   nesnd_cne_reforms_in_progress = yes
  }
  custom_tooltip = {
   text = nesnd_cne_respite_confidence_tt
   nesnd_cne_respite_confidence_ready = yes
  }
 }
 ai_chance = { value = 0 }
 effect = {
  custom_tooltip = nesnd_cne_respite_effect_tt
  hidden_effect = { nesnd_cne_take_respite = yes }
 }
}
```

在 common/journal_entries/nesnd_cne_confidence.txt 的bar旁挂 `scripted_button = nesnd_cne_respite_button`。按钮点击后全部项目暂停，会因visible条件消失；重启后若信心≤900会显示已使用而不可点。若希望永久隐藏已使用按钮，可在visible加NOT used，不改变effect守卫。建议保持当前块以让玩家看到“本轮只能一次”的状态。

### 3.6 已有启停按钮最小显示改造

土地开始保留原生技术/农业用地资格；额外单独显示真实的六个月锁。生命周期和仅AI安全条件不展开；`hidden_effect`内调用原来带ready检查的实际effect。

```text
nesnd_cne_land_start_button = {
 name = nesnd_cne_land_start_button
 desc = nesnd_cne_land_start_button_desc
 visible = { nesnd_cne_programs_live = yes NOT = { has_variable = nesnd_cne_land_program } }
 possible = {
  nesnd_cne_land_foundation = yes
  custom_tooltip = {
   text = nesnd_cne_respite_over_tt
   NOT = { has_variable = nesnd_cne_respite_active }
  }
  hidden_trigger = { nesnd_cne_program_can_start = yes }
 }
 ai_chance = { value = 0 }
 effect = {
  custom_tooltip = nesnd_cne_land_start_tt
  hidden_effect = {
   if = {
    limit = { nesnd_cne_land_start_ready = yes NOT = { has_variable = nesnd_cne_land_program } }
    nesnd_cne_land_start = yes
   }
  }
 }
}
nesnd_cne_land_stop_button = {
 name = nesnd_cne_land_stop_button
 desc = nesnd_cne_land_stop_button_desc
 visible = { nesnd_cne_programs_live = yes has_variable = nesnd_cne_land_program }
 possible = {
  hidden_trigger = { nesnd_cne_programs_live = yes has_variable = nesnd_cne_land_program }
 }
 ai_chance = { value = 0 }
 effect = {
  custom_tooltip = nesnd_cne_land_stop_tt
  hidden_effect = {
   if = {
    limit = { nesnd_cne_programs_live = yes has_variable = nesnd_cne_land_program }
    nesnd_cne_land_stop = yes
   }
  }
 }
}
```

城市用同形替换，保留 `nesnd_cne_urban_foundation` 的每项原生建筑/科技/法律条件。22省营产start的possible在原hidden ready之外加入 `nesnd_cne_respite_over_tt`；stop的原active标记改为hidden_trigger中的live+active+存在性。两类effect均将现有guard和实际副作用整体包入hidden_effect，保留已有start/stop结果TT在外层。不要只隐藏scripted-effect调用而仍让最外层if.limit可见。

营产停止样例（逐州替换slug/state；保留真实ownership检查）：

```text
possible = {
 hidden_trigger = {
  nesnd_cne_programs_live = yes
  has_variable = nesnd_cne_camp_alxa_active
  exists = s:STATE_ALXA.region_state:CNE
 }
}
effect = {
 custom_tooltip = nesnd_cne_camp_stop_tt
 hidden_effect = {
  if = {
   limit = {
    nesnd_cne_programs_live = yes
    has_variable = nesnd_cne_camp_alxa_active
    exists = s:STATE_ALXA.region_state:CNE
   }
   nesnd_cne_camp_alxa_stop = yes
   nesnd_cne_refresh_camp_count = yes
  }
 }
}
```

营产开始仍调用原带ready和owner检查的start effect，refresh count保留。不能把信心奖励加到这些stop函数：它们也被终局、丢州与AI清理调用。

真实失败条件继续在父JE独立显示：信心耗尽、君主制改变、政变、原生内战、极端危机。当前已有各自custom_tooltip无需并成“可以改革”大条件。按钮的visible已经保证父运动活动，所以隐藏重复的生命周期守卫不会隐藏一个尚可操作的真实资格。新六个月锁必须独立可见。

## 四、实际有效文案及作者对读

本轮按nesnd-player-writing读取原始备份，而非将当前AI改稿视作作者样本。

|原始样本|原文特征与本轮用途|
|---|---|
|W/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml:15，`ce_cne_land_reform_reason`|“为了经济振兴、解放生产和发动底层农民、士兵……重新开启了这一运动。”把改革视为社会经济政治运动，不能写“结案”。|
|同文件:69，`flavorCNE.3.d`|土地法、劳动力摆脱宗族、进入城市、新秩序之间有因果；不将改革缩成文书手续。|
|同文件:79，`flavorCNE.4.d`|“地权革命是经济上的革新，同样也是一项冷酷的政治运动。”阶层利益和实际阻力支撑暂缓理由。|
|W/.../ce_french_empire_journals_l_simp_chinese.yml:236–237，保卫王朝按钮|名称为国家行动，desc表达政治目的；机制限制由条件/效果承担。|
|同法国文件:248，进度读数|指标直接显示当前/总量；本轮仍用原生年度明细，不写一段数值更新公告。|

样本SHA256：CNE文件 `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`；法国文件 `352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844`。制度采用技能 `references/north-south-institutions.md` 的六部/元老院/咨议局边界；不新增议会、民意机构或虚构史实。

|键/类别|当前问题或原文对照|候选中文|候选英文|编辑判断|
|---|---|---|---|---|
|`nesnd_land_suspend_requirements` 条件|原“地权革命正在进行，尚未结案。”将全国运动写成案件；EN已准确|地权革命仍在进行。|The land revolution is still underway.|通过；只改CN。|
|`nesnd_cne_respite_button` 行动|作者政治按钮以行动命名|暂缓诸项改革|Pause the Reform Programmes|通过；与永久议止区别明确。|
|`nesnd_cne_respite_button_desc` 理由|作者原文强调改革承担者及经济过程|朝廷暂缓土地商品化、国家城市化与各省营产改制，给地方留下安顿生计、平息争端的时日。|The court will suspend land, urban and military-estate reforms, giving the provinces time to restore livelihoods and settle disputes.|通过；不许诺实际SoL/动乱恢复。|
|`nesnd_cne_respite_unused_tt` 一次资格|必须呈现真实一次性限制|本轮地权革命尚未实行过全面暂缓。|We have not yet called a general pause during this land revolution.|通过；对应永久used变量。|
|`nesnd_cne_respite_over_tt` 暂缓期资格|原生到期限制应单独显示，不暴露变量|未处于改革暂缓期。|No general reform pause is in effect.|通过；数字在效果中给出，此条件在从未暂停时也真实。|
|`nesnd_cne_respite_programs_tt` 行动资格|至少一项真实项目被停才有代价|至少一项改革正在推行。|At least one reform programme is underway.|通过。|
|`nesnd_cne_respite_confidence_tt` 数值资格|≤900保证完整获得100，不浪费额度|人民的信心不高于#v 900#!。|Public confidence is no higher than #v 900#!.|通过。|
|`nesnd_cne_respite_effect_tt` 后果|临时停止+禁止即刻重开+一次恢复|暂停土地商品化、国家城市化与各省营产整顿，并撤回对应的临时修正。#v 6个月#!内不能重启这些改革；人民的信心#p +100#!。|Pause land commercialisation, urbanisation and all military-estate reforms, removing their temporary modifiers. These programmes cannot be restarted for #v 6 months#!. Public confidence #p +100#!.|通过；不称永久结束、不称暂停基础/战争消耗。|
|三项start_tt 数值更新|现有已完整说明收益成本，不需重写|仅末句“每年消耗人民的信心#n 10#!”改为“每年消耗人民的信心#n 5#!”|Only change “Costs #n 10#! public confidence per year.” to “Costs #n 5#! public confidence per year.”|通过；其余数值保留。|
|`nesnd_cne_camp_stop_tt` 停止结果|现有省停止提示漏写信心项目随之停止|停止本州营产整顿带来的进度增长和信心消耗，撤回农业、矿业、税收与建设收益，以及对应的军队支持和将领忠诚惩罚。|Stop this state's reform progress and confidence cost. Remove its production, taxation and construction benefits and the associated military approval and officer loyalty penalties.|通过；仅隐藏原生效果时应补全。|

这些是**编辑提案通过，未接入游戏**。无需新增无实际状态依据的常驻叙事；信心数值和年度明细沿用现有条。土地/城市stop TT 已说明进度、信心消耗、临时修正，原文可保留。终局事件/按钮正文不因本次暂缓改成可重开。

## 五、预期检查与边界

落库后应批量外部检查，不开游戏：

1. 精确比较七类负项与四类+10，bar和country年度公式一致；阈值500、上限1000未改。
2. 新1000、旧850/520/100、有无共和国历史、有无破产charged标记：不重置；未存在confidence的预览谓词false，不读缺变量。
3. 900+100=1000；901不可用；0/live失败不可用；重复调用第二次不增；全停不可用；land-only、urban-only、camp-only都停止正确对象。
4. 六个月锁期间24类start_ready全部false；stop仍可清理；到期只解锁；全局cleanup/丢州不会奖励，used永不清除；旧存档没有新flag即未领取。
5. 保持原ready效果检查，不以visible/possible/hidden_effect代替执行守卫。48个项目启停的possible及effect预览均不展开内部失败闭包；真实技术、建设、法律、资金和暂缓期各保留可判断的原生/定制条件。
6. 新按钮只挂信心JE一次；不改永久议止的effect；原生JE和条初始化不反向添加自己，不写进度0或信心1000迁移。
7. 中英文有效覆盖层无旧10残留于三项开工提示；`尚未结案`仅限CNE这个键改动，首辅案中的同词不做全局替换。

实机未覆盖：真实tooltip版式、变量到期日、月/年同日时序、加载旧档后的活动JE显示。外部源码/算术检查不得表述为这些场景已通过。

## 六、追加：最新实际存档的共和军问题

### 6.1 实际证据，不与推测混写

读取根代理保存的不可变副本 `runtime-evidence/latest_test_save.v3`，160,961,827字节，SHA256 `6d1563547bf2ec4368625e23e3aed25b06352fe90d03aa6cd43ee27ef97711ee`。存档游戏日期 **1844.7.13.18**。本报告同目录 `read_cne_revolt_save.py` 只读SAV文本，复用 W/tools/save_market_network.py 的sections/records和已有有序解析器；证据输出在 `runtime-evidence/cne-revolt/`。

确定事实：

- CNE现存country ID **731**；`nesnd_cne_confidence=180`、改革进度71.6、月度样本102、活动营产3省。`nesnd_cne_programs_running`、`flavorCNE_land_reform_value`、`nesnd_cne_republican_rose`均为true。见 `country-731.txt:744–920` 和 `extra.json.cne_variables`。数值型identity按原生定点数除100000解码。
- 父改革JE53347、信心JE53354、三个改革子JE53355–53357当前active=yes。CNE自己的共和军JE53358是开局预建的inactive对象，不是正在起义；不得把数据库中大量同类inactive JE当作已经触发。
- 现存国家数据库中没有NRP、CRP或QRC。当前唯一外交博弈/战争是中美洲的dp_revolution/war19，双方country16777559和16777588，非CNE共和战争。旧NRP、旧外交博弈与旧战争记录已被清走，dead对象表也没有保留这些历史。
- **NRP曾真实拥有领土**。存档原行3017819起的州813（STATE_SHENGJING）与3019058起的州815（STATE_SOUTHERN_MANCHURIA）都显示 `country=731`、`previous_country_definition="NRP"`、`previous_country=33554660`、`last_owner_change=1841.5.18.12`。两州的recently_conquered_state也始于同一时间。不是角色的前所属国字段。
- USERDATA/logs/debug.1.log:3434–3436记录共和军政党成立，以及 **1841年1月3日**开始选举。说明起义已于1841年初进入真实国家阶段，随后至少持续至两省在5月18日被帝国收回。
- 不可变error.1.log:28（墙钟01:13:45）明确记录 `大汉共和军 already has a journal entry of type nesnd_cne_republic_journal`。与M/common/scripted_effects/nesnd_cne_republic.txt:80的无守卫显式addJE对应。
- USERDATA/logs/error.2.log:53–54（同本次加载，00:36:09）记录共和军将领使用 `ideology_republican` 不是角色意识形态，create_character PostValidate失败。当前源码对应 common/scripted_effects/nesnd_cne_republic.txt:78。正确角色定义为 G/common/ideologies/01_character_ideologies.txt:852 的 `ideology_republican_leader`。

因此，“500阈值完全没有生成共和军”不符合该存档证据。**已证实的问题是初始化错误、以创建过外交博弈代替已发生战争的结算漏洞，以及现有rose标记使该存档不再重复触发。** 最新存档不足以判定1841年5月18日是一次真实短战争的失败，还是未实际开战便进入旧脚本的收回分支。不能把二者中的任何一种伪装成已证根因。

保留用户现有历史：不清除旧档rose，不重置信心，不自动重建已经消失的NRP。这样不会把一次可能已经赢下的旧战争重演。以下修复保护今后的完整链条；不声称重构了旧存档已丢失的战争过程。

### 6.2 精确的前向修复

当前start效果只要找到外交博弈就记 `nesnd_cne_republic_war_created`（M/common/scripted_effects/nesnd_cne_republic.txt:93–94）；watch在该标记存在时停止重试（:102）；NRP JEfail允许 `war_created OR war_seen`（common/journal_entries/nesnd_cne_republic.txt:18）。故“博弈存在过，随后消失，但从未确认实际战争”同样能触发失败吞并。**博弈已创建、实际在战、战后结束应分别判断。** 此逻辑缺口可从源码直接证明，不要求推断旧档究竟走了哪条分支。

维持当前create_diplomatic_play的双方、`war=yes`、`annex_as_civil_war=no`。不要依据过时effects.log中“当前scope为目标”的文字反转双方：当前原版 G/events/heavenly_kingdom_events.txt:506–511、events/british_raj_events.txt:276–280实际使用发起国scope+target_country；原生history/diplomatic_plays/00_carlist_war.txt:3–11包含war及annex_as_civil_war字段。相关文档差异已记入技能recipes.md，不能因接口文档陈旧臆造这次故障原因。

#### 初始化两处改动

```text
# common/scripted_effects/nesnd_cne_republic.txt, setup:
create_character = {
 first_name = nesnd_republic_commander_first
 last_name = nesnd_republic_commander_last
 is_general = yes
 interest_group = ig_armed_forces
 ideology = ideology_republican_leader
}
if = {
 limit = { NOT = { has_journal_entry = nesnd_cne_republic_journal } }
 add_journal_entry = { type = nesnd_cne_republic_journal }
}
```

同时把spawn后 `if.limit={ c:NRP ?= {has_variable=challenger} }` 改成先 `exists=c:NRP` 的外层if，再进入NRP检查challenger的内层if。`?=`允许不存在时跳过，不能作为成功创建的唯一证据。只有确实存在且有challenger标记才写rose/执行setup；既有记录不改。

#### 无回调的实际战争记录 helper

```text
# NRP country scope. Current CNE and NRP identities are checked before access.
nesnd_cne_republic_note_actual_war = {
 if = {
  limit = { exists = c:CNE exists = c:NRP }
  if = {
   limit = {
    c:NRP = this
    has_variable = nesnd_cne_republican_challenger
    has_war_with = c:CNE
   }
   set_variable = nesnd_cne_republic_war_seen
   c:CNE = { set_variable = nesnd_cne_republic_war_confirmed }
  }
 }
}
```

NRP本地war_seen用于结算；新增CNE持久war_confirmed仅记录今后真的观察到战争，便于NRP消失后仍能辨别。它不作为旧档迁移的补发理由，不重置或覆盖现有变量。

#### start与watch完整替换

```text
nesnd_cne_start_republic_war = {
 if = {
  limit = {
   c:CNE ?= this
   nesnd_cne_republic_target_available = yes
   NOT = { nesnd_cne_republic_has_play = yes }
  }
  end_truce = c:NRP
  create_diplomatic_play = {
   name = nesnd_cne_republic_war
   type = dp_nesnd_cne_republic
   target_country = c:NRP
   war = yes
   annex_as_civil_war = no
  }
  if = {
   limit = { nesnd_cne_republic_has_play = yes }
   c:NRP = { set_variable = nesnd_cne_republic_war_created }
  }
 }
 # Also observes an already-existing direct war, without recreating it.
 if = {
  limit = { exists = c:NRP }
  c:NRP = { nesnd_cne_republic_note_actual_war = yes }
 }
}
nesnd_cne_republic_watch = {
 if = {
  limit = { c:NRP ?= this has_variable = nesnd_cne_republican_challenger }
  nesnd_cne_republic_note_actual_war = yes
  if = {
   limit = {
    exists = c:CNE
    NOT = { has_variable = nesnd_cne_republic_war_seen }
    NOT = { nesnd_cne_republic_has_play = yes }
    NOT = { nesnd_cne_republic_at_war = yes }
   }
   c:CNE = { nesnd_cne_start_republic_war = yes }
  }
 }
}
```

当前country和NRP仍由原predicates保卫；`nesnd_cne_republic_has_play`全局检索同一类型及同一双方，不会因watch从NRP调用而改变检索集合（W/references/engine-docs-1.13.11-20261031/triggers.log:1873–1877明确any_diplomatic_play为全局迭代）。已有play/war时不重建；只有未曾观察到实际战争且当前也没有play/war才重试。旧war_created保留为已有历史数据，但不再充当实际战争证明或永久重试锁。

#### JEfail和defeat都重新检查真实前置条件

```text
# common/journal_entries/nesnd_cne_republic.txt
fail = {
 c:NRP ?= this
 exists = c:CNE
 has_variable = nesnd_cne_republic_war_seen
 NOT = { nesnd_cne_republic_at_war = yes }
 NOT = { nesnd_cne_republic_has_play = yes }
 NOT = { has_variable = nesnd_cne_republic_launch_grace }
}

# common/scripted_effects/nesnd_cne_republic.txt
nesnd_cne_republic_defeat = {
 if = {
  limit = { exists = c:CNE exists = c:NRP }
  if = {
   limit = {
    c:NRP = this
    has_variable = nesnd_cne_republican_challenger
    has_variable = nesnd_cne_republic_war_seen
    NOT = { nesnd_cne_republic_at_war = yes }
    NOT = { nesnd_cne_republic_has_play = yes }
    NOT = { has_variable = nesnd_cne_republic_launch_grace }
   }
   c:CNE = {
    set_variable = nesnd_cne_republic_settled
    annex_with_incorporation = prev
    trigger_event = { id = nesnd_cne_confidence.4 popup = yes }
   }
  }
 }
}
```

7天launch_grace仍是现有宽限；无需引入新计时器、延迟事件或新的战争回调。新settled标记只在确认过战争且play/war均结束的脚本收回路径写入；原生战目标直接吞并NRP时可能不经过此effect，CNE的war_confirmed仍提供实际战争已观察到的依据。没有把所有NRP消失都写成脚本结算。

观察边界：创建后立刻检查，加现有每周检查，覆盖通常的直接开战和持续战争。若引擎把战争创建延迟到后续tick，又在首次周度观察前结束，这个极短窗口仍不能仅凭静态代码确认；本次不为这一未实证窗口新添回调或改写旧历史。应在用户下一轮实际运行时核NRP、play、has_war_with和CNE持久war_confirmed，不能以源码修复冒充已经复现并通过整场内战。
