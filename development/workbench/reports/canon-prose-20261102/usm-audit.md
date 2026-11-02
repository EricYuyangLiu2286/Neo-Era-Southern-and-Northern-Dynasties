# 南朝／吴明／湖广文案审查与双语修订提案

状态：EDITORIAL_PROPOSAL；未改主 MOD、未改候选、未改技能、未开游戏。源码核对不能称为引擎验收。版本为 1.13.11 / Steam build 24799966；本轮 `catalog.py status` 返回 CURRENT、changed_count=0。

本审查按当前主 MOD 的本地化覆盖顺序整理 683 个相关键，其中包含成熟作者原文、AI后覆盖、隐式日志字段和旧兼容键。有效层按普通本地化后 replace、文件名顺序归并；每层原文和SHA均留在 usm-inventory.json，未将此静态归并冒充引擎观测。作者本轮附件与主MOD英文文件中的中文修订均作为作者证据；不能把错放在英文槽中的中文当作已经完成的英译。

修订 JSON 为 `usm-proposals.json`，300键，逐键含 zh/en/reason/source/mechanic/current_zh/current_en/status。主键文本应写回实际覆盖它的各层，或移除冲突的旧覆盖；不要只修改 ce_usm 基础文件。本审查没有把所有“盟约”替换成“礼法”：中央国制是礼法，反吴军阀可结盟，外交通商和援助仍使用条约。

## 关键结论与作者原稿的机制差异

1. **作者修改的 federal_compact_button 不是现行按钮显示源。**旧同名按钮已指向 south_offer 名称与描述，且没有当前JE调用；真正被“南朝诸国”调用的是 `nesnd_south_offer_accord`。该动作发送改制提议，不能写成点击即召开大会、立即通过宪法或改变领土。
2. **事件10无当前调用者。**`nesnd_crisis.10`保留了旧清理与招抚效果，但当前和平结局走明20→22、吴21→23。因此将作者关于“礼法通过”的历史论说接入真实结局，保留旧10稿作为兼容文本，不复活其奖励。两路线已分别写；不共享一个拥明胜利段落。
3. **湖广旧三按钮已退役。**`nesnd_huguang_preparations` possible=no、shown=no、invalid=yes，清理旧存档。书院、粮运、老兵按钮当前无JE调用。作者稿精修为可追溯的闲置提案，不能宣称三项教育、政治动员或荆蜀协定已经上线。现行湖广内容为“脆弱的贸易”，只核大学、军营等建筑就业与供应、民生和联络条件。报告与JSON分别覆盖了现行条目。
4. **警卫旧事件11已隐藏。**作者拟定的大理寺公开调查／锦衣卫秘密调查没有现行选择效果。真实首辅按钮被 chen_security 最终层覆盖，走六个月护卫、留署、内应清查及死亡／负伤／脱险概率。已将作者保护改革领袖的动机移至这个真实面板；旧11稿保留，不宣称旧两选项可玩。
5. **明和平不吞并诸省，不调整其经济法律。**它保留实际朱氏君主和各成员政府，中央获得120个月 authority−15%、government_wages+10%的礼法约束。作者“统一完成、万世难改”的表述改为共同认可权责；不得据此虚构统一省法或新增立法机制。
6. **吴和平有实际整合与日本割地。**在全部既有门槛连续满足12个月后，设置吴统治者／旗标，将明确同意且安全控制的中国范围辖地并入；日本只转让自己持有的四国、九州。海外保留条件按现有代码，不写成全体海外已经同意或全部吞并。二元君主立宪是作者本轮设定在叙事中的表达；现有effect没有另行 enact_law，不能声称某一法律组因此自动改变。
7. **首辅去位旧AI后覆盖与实际触发冲突。**flavorUSM.6要求陈东阳已无在世人物，是死亡后续。改为“首辅身后”，不强断言遇刺，兼容自然死亡。其d1在当前≤1862事件触发与>1870描述条件下不由正常调用可达，保留成熟原稿，不扩大机制修复。
8. **crisis20可能发生在土改结束后。**作者稿无条件“地权改革仍在继续”改为“若尚未完成”。A旁观，B湖南援助36个月、仅改革活跃时失序+8，C干预60个月、仅改革活跃时+15并加入可用反吴对峙。保留北朝“伪朝禅代”的阵营立场；选项C为“联络襄樊大营，准备南下”。
9. **外国主体不固定为皇帝。**法国事件没有君主制守卫，改“政府”，不为显示标题额外引用可能不存在的君主。真正新礼法颁诏的明20、22和吴23有君主来源，使用动态title＋name。
10. **英文回退与异步旧文已完整扫清提案范围。**683键中原有161个尚未进入首批提案的英文槽含中文；300键修订合并后，范围内英文中文回退为0。供应规则EN补齐当前CN的50%商品价格、各国建筑类型，删Latest refresh、每次核验等更新说明。external全部67键完成英译／审查；供应全部相关字段完成双语对照。

## 原版完整链条及适用边界

### 脚本按钮动态描述

- 调用者：[common/journal_entries/06_cuba.txt:324](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/06_cuba.txt:324>) 的 `je_cuba_independencia`，343行 `scripted_button = je_cuba_promise_freedom`；同JE有icon/group/progress_bar。
- 实例：[common/scripted_buttons/00_cuba_scripted_buttons.txt:2](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/00_cuba_scripted_buttons.txt:2>)；name在3–20行、desc在21–36行均直接用`first_valid/triggered_desc`，同一country上下文以 `has_law_or_variant` 分支；visible/possible/selected/effect全部在同对象内。effect从82行起设置承诺变量并作用于奴隶起义运动，说明这里是有效行为入口而非纯示意。
- 本地化：[localization/english/ip4_cuba_l_english.yml:98](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/ip4_cuba_l_english.yml:98>)，99/105行对应两个desc，后者已使用ROOT.GetCountry；无需新增GUI或customizable_localization。
- 适用差异：NESND按当前阵营脚本值1/2选择文字，效果和条件仍沿用原发送函数。`tag_WUU_var`只在登基后设置，不能用于判断登基前已选择的拥吴路线。无立场时回退中性描述。
- 原版按钮SHA256：`b5db040f10018dcd3cdfc1f34db932570553359ae4096a462c6599f747d00c10`。

### 君主标题与姓名

- 原版[events/law_events/republic_laws.txt:174](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/events/law_events/republic_laws.txt:174>) 的 `republic_laws.3` 为country_event/placement ROOT，以君主制和正在立法为触发，description引用republic_laws.3.d；icon与event_image都由本体定义。
- 实际文案[localization/english/content_4_l_english.yml:272](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/content_4_l_english.yml:272>)同时使用 `[ROOT.GetCountry.GetRuler.GetPrimaryRoleTitle] [ROOT.GetCountry.GetRuler.GetFullName]`。[localization/english/agitators_2_l_english.yml:8](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/localization/english/agitators_2_l_english.yml:8>)还存在同一GetFullName/GetPrimaryRoleTitle组合。
- NESND明20触发须有在世合法朱氏君主，明22紧接commit_ming；吴23紧接install_wu_peacefully，该函数先转入/生成实际君主再通知。其余无君主保证的country主体仍可执行外交，但不强接ruler动态引用。没有把旧历史回忆中的郑昭改为现任君主。

### 当前项目调用与机制来源

- [common/journal_entries/nesnd_succession_board.txt:26](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_succession_board.txt:26>)；SHA256 `1b982e78ef114f25c67303cd0a498a14e38f6246e3ac461a94223e34cb26f5f2`。
- [common/scripted_buttons/nesnd_south_accords.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_south_accords.txt:1>)；SHA256 `adb68d86b95e5ccdd38ed3e08ca55ec068db1634b069d931bc7063557221ae7d`。
- [common/scripted_buttons/nesnd_crisis_buttons.txt:53](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_crisis_buttons.txt:53>)；SHA256 `590f782d644820d142c221b2e7bb62041927884bf147e387f2333b3da95b4e09`。
- [common/scripted_effects/nesnd_south_accords.txt:9](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_accords.txt:9>)；SHA256 `4d4a4ccaec2f32a11ce856debd23340ea19ede9e752301f00772b6099c5cda70`。
- [common/scripted_triggers/nesnd_south_politics.txt:179](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_south_politics.txt:179>)；SHA256 `7fdff14cc2498cf0a9c5f0feb74b5903c11db0612c9412fb352a3de16cf2b784`。
- [events/nesnd_south_accords.txt:3](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_south_accords.txt:3>)；SHA256 `2f89c5d4628c91daae630f40b52c762ade877f7686a9f3db3e68f8a89a04a1d6`。
- [events/nesnd_south_accords.txt:221](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_south_accords.txt:221>)；SHA256 `2f89c5d4628c91daae630f40b52c762ade877f7686a9f3db3e68f8a89a04a1d6`。
- [events/nesnd_south_accords.txt:262](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_south_accords.txt:262>)；SHA256 `2f89c5d4628c91daae630f40b52c762ade877f7686a9f3db3e68f8a89a04a1d6`。
- [common/scripted_effects/nesnd_south_peace.txt:403](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:403>)；SHA256 `f8278e3e99f07afa97b38f4b3fc774e4753e9344bf9baed07db24630dde49791`。
- [common/scripted_effects/nesnd_south_peace.txt:439](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_peace.txt:439>)；SHA256 `f8278e3e99f07afa97b38f4b3fc774e4753e9344bf9baed07db24630dde49791`。
- [common/journal_entries/nesnd_regional_preparations.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_regional_preparations.txt:2>)；SHA256 `0957ecd8bda5969c960a1df49d937a96149398ae5f6ed820f1c565c78668d3dd`。
- [events/nesnd_crisis_events.txt:126](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_crisis_events.txt:126>)；SHA256 `6aa40e18d2d64bf0dba33622aca4e4f9ffae141988c89c73344dd71d88f92b00`。
- [events/nesnd_chen_security.txt:2](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_chen_security.txt:2>)；SHA256 `9743da66aaef696b23ccf4ed97a91a52996d45ead0524f2a94b3a7a039da06c0`。
- [events/flavorUSM_ce.txt:806](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/flavorUSM_ce.txt:806>)；SHA256 `1c75e75b015394b9af4a75639d7db0c943e4aaf81834dfc177b6be2d3dbecd2c`。
- [common/scripted_effects/nesnd_chen_security.txt:147](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_chen_security.txt:147>)；SHA256 `2e37491a703fc8af4c4c1dfa225a2f5fc4abb5b351a44b50d56209c833b51a89`。
- [common/scripted_effects/nesnd_south_reconciliation.txt:26](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_south_reconciliation.txt:26>)；SHA256 `ee0f09c34972ee5914d82c4bdaea55be09067d851374bc48ca09bf93e4fb5dd4`。
- [events/nesnd_external_events.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/events/nesnd_external_events.txt:1>)；SHA256 `66a88ac04086284176a99ae1f81c06037b45cb985f98ea87f637ce07e74648dc`。
- [common/scripted_buttons/nesnd_external_buttons.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_buttons/nesnd_external_buttons.txt:1>)；SHA256 `6c362de3f1bb51ec56f10478895e2fafa1666c19088ed586415227ff430083d6`。
- [common/scripted_triggers/nesnd_supply_triggers.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_triggers/nesnd_supply_triggers.txt:1>)；SHA256 `620f10fbc185b30e94c5bd8425412ee1fda8e8ef0a40a75c8a00df311a07efd8`。
- [common/static_modifiers/nesnd_crisis_modifiers.txt:1](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/nesnd_crisis_modifiers.txt:1>)；SHA256 `817dfbf997a405976f92c52a647db1c23d59d316430f4a509ee7d0a7a7edafe6`。

## 最小代码改动

只更改显示分支；不新增权重、不恢复退役日志、不增加任何货物／金钱／政体效果。

1. `common/scripted_buttons/nesnd_south_accords.txt` 的现行按钮中，将单行 `desc = nesnd_south_offer_accord_desc` 替换为：

```text
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 1 }
            desc = nesnd_federal_compact_button_desc
        }
        triggered_desc = {
            trigger = { nesnd_board_stance_value = 2 }
            desc = nesnd_federal_compact_button_alt_desc
        }
        desc = nesnd_south_offer_accord_desc
    }
}
```

2. `common/scripted_buttons/nesnd_crisis_buttons.txt` 中旧 `nesnd_federal_compact_button` 若保留兼容定义，可同步使用相同desc块；它当前无JE调用，不必重新挂回JE。name保持现有 `nesnd_south_offer_accord`。新alt键原为注释，需在两种语言中成为真实键。
3. `nesnd_south_accords.20`、`.21` 的 `name = nesnd_south_accords.reconsider` 选项中，各添加 `custom_tooltip = nesnd_south_reconsider_tt`。实际重新开始12个月的效果不变；原选项里的开发式“重新计算”移至具体操作提示。
4. 明20/22、吴21/23本来就是四个独立事件，按JSON分别修订正文即可，无须为它们另造动态分支。`nesnd_crisis.10`无caller，保留旧兼容稿；不能仅替换它后宣称用户现在能看到礼法结果。
5. 每个改动键的所有定义路径见inventory附表与JSON all_zh/all_en。同键多层须统一或由应用者明确保留单一最终定义，不新增一个更深zz文件来继续堆旧解释。主MOD英文中用户中文修改的事实／立场已人工继承到提案，不能用旧候选覆盖其本意。

## 作者语体对读与本轮返工

作者基线只来自 pre-update-20261030T233944Z/mod；本轮作者附件为事实和修订意图来源，旧AI句不当作作者样本。已对读原版 ce_usm_events 的 flavorUSM.1.d／4.d／5.d／7.d／8.d／10.d、ce_usm_conflicts_within_reason、usm_civilwar.8.d／10.d、相关选项和引文。原稿允许政治论说、历史铺陈和有立场的选项；判断重点是具体人物、制度与行动的因果，不靠每段短句或装饰文言。

- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:30](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:30>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：西元1678年春，时为北明吴国公的大明南京留守使、南京礼部尚书的（吴武宗）郑昭在他在海内外的一系列军事胜利后，单方面向朝廷上书，准备进京觐见大明天子。当是时，在三十年前的大宪战争中大获全胜的天津燕主及其国势还如烈火烹油。……
  - 对读键 `nesnd_south_accords.23.d`；决定：郑昭的军事实绩、移民与集权变法相接；候选沿这种因果写郑氏权势如何成为国制，去交接印信簿册。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:118](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:118>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：明朝朱姓，还是吴国郑氏？这对于中国南朝有能力参预政治的国人来说，是一个每分每秒都要自问的难题。从川边乡校的讲习台到南京礼部的议会殿。争论、札子、散文、报道，各式各样体裁的文字都在对人们呼喊。却是问多于答，争大于论。……
  - 对读键 `nesnd_south_succession_board_reason`；决定：原文把论争放在乡校与议会；候选明确监生、学政、内阁及营伍，而不把全天下压成同一张案。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:86](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:86>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：南明政权后期，武装力量主要分为西府、南府两大部分。其中的西府军队没有南府郑氏这样独断的政治领袖，而实际上是一个由四川蜀藩、湖北楚藩、广西淮藩为首的松散联盟。曾几何时，郑雕锦正是其中那颗冉冉升起的明星——朱班博麾下最有力的……
  - 对读键 `nesnd_huguang_preparations_reason`；决定：原文从朱班博与郑雕锦关系讲西府政治；候选保留作者岳麓、共和派和南府排挤的具体链条。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:75](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:75>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：陈东阳（字满越）（1772-[Date.GetString|v]）是西秦大革命时期的国人主义共和思想的代表人物，也是短命的革命共和国的开国元勋。在被迫逃离自己建立的国家后，陈东阳与南方的进步派合作，以南明首辅的身份又成为……
  - 对读键 `nesnd_protect_chen_button_desc`；决定：原文写政治盟友转为相忌；现行按钮叙述改革触动谁、为什么应保护陈，不承诺护卫必然救活。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:233](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:233>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：由郑氏乱臣贼子所兴起的这场内乱，终于以我们这些正道之士的胜利落下帷幕。这个时代不是值得称道的时代。忠臣和忠臣之间相互杀戮，共和派和共和派相互攻讦。郑氏原本并不是旧日明廷中最腐朽的一帮人，但他们对于权力的渴望以及他们在旧国……
  - 对读键 `usm_civilwar.10.d`；决定：作者胜利不等于无争论；候选说明宗室、地方领袖与共和派各有主张，真实战争联盟仍称联盟。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:32](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:32>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：尧舜禅让，汤武革命。中国天命所衷不在一家一姓，上下分隔，而在于民有德，于人有功。……
  - 对读键 `nesnd_south_accords.21.a`；决定：作者选项是政治行动/立场；新选项用受禅与依礼法施政，不写代码进度。 改后为编辑提案通过，未接入游戏。
- 原文[localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:31](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml:31>)，SHA `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`：.吾常闻朱家天子受命于天，乃神龙降世。明太祖高皇帝以一乞儿之身，执长策，灭胡氛，恢复汉家中原。功在千古，更比青史石刻永恒。所以周德虽衰，天命未改。今日一见，朱家小子亦凡人尔。\n——郑昭……
  - 对读键 `flavorUSM.4.f`；决定：成熟作者引文原样保留中文并英译；crisis10/11等无出处新引文单独标为剧情拟写，不冒署古人。 改后为编辑提案通过，未接入游戏。

局部纠正规则已实际应用：把“中央的盟书”按实际职责改成礼法；省际军事协议和国家间条约不改。把“军校—算粮饷”重建为书院监生—礼议院考试—未来省代表。把“国家颁诏”改为在有君主保证的事件中显示真正的title/name；无保证时改写行动主体。上述规则先回读最新north-south-institutions，再完成第二轮重写。第一版的 Liyi Assembly 已按本轮一致译名统一为 Assembly of Rites。

## 提案静态复核与局限

- 所有300键均有完整中文与英文；两语言动态方括号引用集合逐键相等；英文无中文回退；提案中文无“原生／本日志／本项目／按原规则／快照”。
- 数字只据现有脚本或原有效提示保留；没有调整政治权重、定向立场概率、经济成本或HNA三按钮可达性。12个月重置提示属于已有代价的展示。
- 已识别原稿与效果的差异并写明：HNA闲置；crisis10无caller；crisis11隐藏；明结局不吞并；crisis20土改条件；flavorUSM6死亡；法国可能共和。
- `nesnd_wu_eastern_question_reason` 为日本开发交接项：当前中文仅写天皇／德川两方，英文写丰臣／德川／天皇三方。已通知主代理，由日本候选所有者统一；不以本南朝审查覆盖其正在变更的日本剧情。
- 原作者成熟历史事件中不属于本次AI修订的长文与强烈立场保留。它们列在清单中，保留结论不等于认证所有原版剧情、角色生命周期、历史日期或引用归属均正确。
- 仅在报告目录生成文件；没有运行游戏、没有自称ENGINE_PASS。正式应用后的覆盖键检查、BOM、Jomini解析和候选检查由主代理进行。

## 逐文件／逐键清单

`重写`=JSON有双语提案；`保留作者原文`=中文与成熟基线逐字相同，本轮不改；`通过`=当前文案在本轮制度/玩家表达范围内保留；`日本交接`=交由日本正在修改的候选负责。是否有直接引用仅用于定位，JE自动字段、modifier名与二级本地化引用也可能有效，不能以未检出直接引用擅删文本。

### localization/simp_chinese/nesnd_external_l_simp_chinese.yml

共67键；主MOD SHA256 `cc8520415df5b7477f0d5d497ae99a07c802c84ddae01bb610f0ad99830d1fb2`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_external_choose_wu`|2|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:6；common/scripted_buttons/nesnd_external_buttons.txt:1|
|`nesnd_external_choose_sih`|3|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:7；common/scripted_buttons/nesnd_external_buttons.txt:99|
|`nesnd_external_choose_hus`|4|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:8；common/scripted_buttons/nesnd_external_buttons.txt:170|
|`nesnd_external_choose_fra`|5|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:9；common/scripted_buttons/nesnd_external_buttons.txt:241|
|`nesnd_external_hus_title`|6|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_hus_desc`|7|重写|去国库/工厂各交账目的机械隐喻；具体独立战争记忆与现实财力约束。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_fra_title`|8|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_fra_desc`|9|重写|FRA可改共和政体，删固定“皇帝裁定”；事件无当前君主守卫，不添加不安全ruler引用。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_qe1_title`|10|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_qe1_desc`|11|重写|西秦外交当前可选SIH/反吴，写具体对象与代价；不捏造新国书动作。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_sha_title`|12|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_sha_desc`|13|重写|SHA当前请求HUS援助，不写无功能的运粮过冬与议事厅对举。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_bur_title`|14|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_bur_desc`|15|重写|国家不是亲自颁诏者，改为明确外部局势。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_mug_title`|16|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_mug_desc`|17|重写|事件无保证USM此刻仍有Mysore，使用条件句；法国援助不是无条件军事干预。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_gbr_title`|18|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_gbr_desc`|19|重写|删除商报账目装饰，以旧同盟→新贸易机会→援助代价为因果。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_rus_title`|20|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:5|
|`nesnd_external_rus_desc`|21|重写|删除笼统账册堆案和无对象总结，说明可做的外交行动。 来源：events/nesnd_external_events.txt:6|
|`nesnd_external_policy`|22|重写|日志标题不再以账册代替外交内容。 来源：common/decisions/nesnd_external_decisions.txt:4；common/journal_entries/nesnd_external_journal.txt:1|
|`nesnd_external_policy_reason`|23|重写|去一场政变分前程的无内容概括；保留真实外交条约。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_external_follow`|24|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:10|
|`nesnd_external_decline`|25|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:13|
|`nesnd_external_choose_desc`|26|重写|删除“本项目”开发口吻，保留一次援助限制。 来源：common/scripted_buttons/nesnd_external_buttons.txt:3；common/scripted_buttons/nesnd_external_buttons.txt:101|
|`nesnd_external_choose_opposition`|27|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:10；common/scripted_buttons/nesnd_external_buttons.txt:312|
|`nesnd_external_choose_opposition_desc`|28|重写|删“实际/真实”实现词。 来源：common/scripted_buttons/nesnd_external_buttons.txt:312|
|`nesnd_external_offer_money`|29|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:11；common/scripted_buttons/nesnd_external_buttons.txt:323|
|`nesnd_external_offer_money_desc`|30|重写|明确约束期不自动终止，删原生内部词；数字按现有trigger。 来源：common/scripted_buttons/nesnd_external_buttons.txt:325|
|`nesnd_external_offer_arms`|31|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:12；common/scripted_buttons/nesnd_external_buttons.txt:357|
|`nesnd_external_offer_arms_desc`|32|重写|保留商品单位与约束期，玩家不读原生一词。 来源：common/scripted_buttons/nesnd_external_buttons.txt:359|
|`nesnd_external_request_tt`|33|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_external_buttons.txt:352；common/scripted_buttons/nesnd_external_buttons.txt:386|
|`nesnd_external_status_choose`|34|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:32|
|`nesnd_external_status_selected`|35|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:31|
|`nesnd_external_status_pending`|36|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:30|
|`nesnd_external_status_committed`|37|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:29|
|`nesnd_external_money_title`|38|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:25|
|`nesnd_external_money_desc`|39|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:26|
|`nesnd_external_arms_title`|40|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:193|
|`nesnd_external_arms_desc`|41|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:194|
|`nesnd_external_accept`|42|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:34；events/nesnd_external_events.txt:202|
|`nesnd_external_refuse`|43|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:163；events/nesnd_external_events.txt:350|
|`nesnd_external_commitment_tt`|44|重写|保留重要期限界限，删除原生实现词。 来源：events/nesnd_external_events.txt:159；events/nesnd_external_events.txt:346|
|`nesnd_external_request_money`|45|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:13；common/scripted_buttons/nesnd_external_buttons.txt:391|
|`nesnd_external_request_money_desc`|46|重写|删“不反向”防御式重复，付款方向已明确。 来源：common/scripted_buttons/nesnd_external_buttons.txt:393|
|`nesnd_external_request_arms`|47|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:14；common/scripted_buttons/nesnd_external_buttons.txt:425|
|`nesnd_external_request_arms_desc`|48|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_external_buttons.txt:427|
|`nesnd_external_request_money_title`|49|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:386|
|`nesnd_external_request_money_event_desc`|50|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:387|
|`nesnd_external_request_arms_title`|51|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:564|
|`nesnd_external_request_arms_event_desc`|52|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:565|
|`nesnd_external_accept_request`|53|重写|此选项供金钱与军械共用，“拨款照准”只合钱支线。 来源：events/nesnd_external_events.txt:395；events/nesnd_external_events.txt:573|
|`nesnd_external_refuse_request`|54|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:534；events/nesnd_external_events.txt:731|
|`nesnd_external_reconsider`|55|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:18；common/scripted_buttons/nesnd_external_buttons.txt:542|
|`nesnd_external_reconsider_desc`|56|重写|按钮可用条件已禁止committed；删清除选择的技术口吻和重复领取。 来源：common/scripted_buttons/nesnd_external_buttons.txt:544|
|`nesnd_external_mysore`|57|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:15；common/scripted_buttons/nesnd_external_buttons.txt:459|
|`nesnd_external_mysore_desc`|58|重写|按钮验证USM持地，不验证已经吴朝；改南朝。 来源：common/scripted_buttons/nesnd_external_buttons.txt:461|
|`nesnd_external_mysore_tt`|59|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_external_buttons.txt:492|
|`nesnd_external_cancel_request`|60|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:16；common/scripted_buttons/nesnd_external_buttons.txt:496|
|`nesnd_external_cancel_request_desc`|61|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_external_buttons.txt:496|
|`nesnd_external_dismiss`|62|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_external_journal.txt:17；common/scripted_buttons/nesnd_external_buttons.txt:500|
|`nesnd_external_dismiss_desc`|63|重写|删本项目。 来源：common/scripted_buttons/nesnd_external_buttons.txt:502|
|`nesnd_external_resume`|64|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/decisions/nesnd_external_decisions.txt:1|
|`nesnd_external_resume_desc`|65|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_external_end_title`|66|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:372|
|`nesnd_external_end_desc`|67|重写|删除文书借据清单排比，不把外交承诺变成宪法。 来源：events/nesnd_external_events.txt:372|
|`nesnd_external_end_option`|68|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_external_events.txt:374|
### localization/simp_chinese/nesnd_supply_l_simp_chinese.yml

共58键；主MOD SHA256 `42c302976d90952cc592057524f2cdda342989648e9d8d9399a52519704c3afc`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_supply_preparations`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/decisions/nesnd_supply_decisions.txt:2；common/decisions/nesnd_supply_decisions.txt:4|
|`nesnd_supply_preparations_reason`|3|重写|学校不是培养粮饷小吏；保留此JE确实建筑/商品/就业条件，不给没有HNA限定的日志硬塞襄阳唯一背景。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_supply_status_war`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:49；common/journal_entries/nesnd_supply_journals.txt:198|
|`nesnd_supply_status_inputs`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:63；common/journal_entries/nesnd_supply_journals.txt:212|
|`nesnd_supply_status_jobs`|6|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:107；common/journal_entries/nesnd_supply_journals.txt:256|
|`nesnd_supply_status_livelihood`|7|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:115；common/journal_entries/nesnd_supply_journals.txt:264|
|`nesnd_supply_status_diplomacy`|8|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:123；common/journal_entries/nesnd_supply_journals.txt:272|
|`nesnd_supply_status_stable`|9|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:125；common/journal_entries/nesnd_supply_journals.txt:274|
|`nesnd_supply_readiness_bar`|10|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:23；common/journal_entries/nesnd_supply_journals.txt:172|
|`nesnd_supply_readiness_bar_desc`|11|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_supply_bars.txt:1|
|`nesnd_supply_continuity_bar`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:24；common/journal_entries/nesnd_supply_journals.txt:173|
|`nesnd_supply_continuity_bar_desc`|13|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_supply_bars.txt:2|
|`nesnd_supply_invite_desc`|14|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:3；common/scripted_buttons/nesnd_supply_buttons.txt:85|
|`nesnd_supply_invitation_tt`|15|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:77；common/scripted_buttons/nesnd_supply_buttons.txt:159|
|`nesnd_supply_accept_tt`|16|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_supply_events.txt:90|
|`nesnd_supply_self`|17|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:31；common/journal_entries/nesnd_supply_journals.txt:180|
|`nesnd_supply_self_desc`|18|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:490|
|`nesnd_supply_end_contact`|19|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:32；common/journal_entries/nesnd_supply_journals.txt:181|
|`nesnd_supply_end_contact_desc`|20|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:496|
|`nesnd_supply_end_contact_tt`|21|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:499|
|`nesnd_supply_trade`|22|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:33；common/journal_entries/nesnd_supply_journals.txt:182|
|`nesnd_supply_trade_desc`|23|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:503|
|`nesnd_supply_trade_request_tt`|24|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:567|
|`nesnd_supply_finish`|25|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:34；common/journal_entries/nesnd_supply_journals.txt:183|
|`nesnd_supply_finish_desc`|26|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:573|
|`nesnd_supply_dismiss`|27|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:37；common/journal_entries/nesnd_supply_journals.txt:186|
|`nesnd_supply_dismiss_desc`|28|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:591|
|`nesnd_supply_envoys`|29|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:65；common/scripted_buttons/nesnd_supply_buttons.txt:147|
|`nesnd_supply_verified`|30|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/static_modifiers/nesnd_supply_modifiers.txt:2；events/nesnd_supply_events.txt:260|
|`nesnd_supply_treaty`|31|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:210|
|`nesnd_supply_resume`|32|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/decisions/nesnd_supply_decisions.txt:1|
|`nesnd_supply_resume_desc`|33|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_supply.1.t`|34|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:6|
|`nesnd_supply.1.d`|35|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:7|
|`nesnd_supply.1.a`|36|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:16|
|`nesnd_supply.1.b`|37|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:93|
|`nesnd_supply.2.t`|38|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:114|
|`nesnd_supply.2.d`|39|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:115|
|`nesnd_supply.2.a`|40|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:124|
|`nesnd_supply.2.b`|41|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:237|
|`nesnd_supply.3.t`|42|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:255|
|`nesnd_supply.3.d`|43|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:255|
|`nesnd_supply.3.a`|44|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_supply_events.txt:258|
|`nesnd_supply_invite_hna`|45|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:25；common/journal_entries/nesnd_supply_journals.txt:174|
|`nesnd_supply_invite_sih`|46|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:26；common/journal_entries/nesnd_supply_journals.txt:175|
|`nesnd_supply_invite_gng`|47|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:27；common/journal_entries/nesnd_supply_journals.txt:176|
|`nesnd_supply_invite_yn1`|48|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:28；common/journal_entries/nesnd_supply_journals.txt:177|
|`nesnd_supply_invite_cne`|49|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:29；common/journal_entries/nesnd_supply_journals.txt:178|
|`nesnd_supply_invite_fra`|50|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:30；common/journal_entries/nesnd_supply_journals.txt:179|
|`nesnd_supply_hus_preparations`|51|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/decisions/nesnd_supply_decisions.txt:2；common/decisions/nesnd_supply_decisions.txt:4|
|`nesnd_supply_hus_preparations_reason`|52|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_supply_finish_shared`|53|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:35；common/journal_entries/nesnd_supply_journals.txt:184|
|`nesnd_supply_finish_shared_desc`|54|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:599|
|`nesnd_supply_finish_autonomous`|55|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/nesnd_supply_journals.txt:36；common/journal_entries/nesnd_supply_journals.txt:185|
|`nesnd_supply_finish_autonomous_desc`|56|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_supply_buttons.txt:621|
|`nesnd_supply_workforce_ready_tt`|58|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_triggers/nesnd_supply_triggers.txt:35|
|`nesnd_supply_rules_link`|59|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_supply_rules`|60|重写|现有EN遗漏纸张/工具/小武器50%及各国建筑类型，且保留Latestrefresh更新口吻；按当前CN完整译出。 来源：自动字段／本地化引用；无直接脚本文字命中|
### localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml

共251键；主MOD SHA256 `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`ce_cne_reform_limited_market_access`|124|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_cne_land_draft.txt:92|
|`ce_cne_war_with_western_qin`|125|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_cne_land_draft.txt:93|
|`ce_cne_war_with_usm`|126|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_cne_land_draft.txt:94|
|`ce_cne_technology_advantage`|127|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_cne_land_draft.txt:95|
|`ce_cne_reform_legal_system`|128|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_cne_land_draft.txt:96|
|`dp_leadership_china`|2|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_leadership_china_desc`|3|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_leadership_china_tooltip_desc`|4|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_usm_civil_war`|6|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/diplomatic_plays/ce_diplomatic_plays.txt:1；common/scripted_effects/nesnd_crisis_effects.txt:284|
|`dp_usm_civil_war_tooltip`|7|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_usm_civil_war_desc`|8|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_ce_unify_china`|10|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/country_formation/CE_major_formables.txt:8；common/diplomatic_plays/ce_diplomatic_plays.txt:43|
|`dp_ce_unify_china_tooltip`|11|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`dp_ce_unify_china_desc`|12|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`flavorUSM.1.t`|14|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/ce_fra_unrest_events.txt:2672；events/flavorUSM_ce.txt:20|
|`flavorUSM.1.d`|15|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/ce_fra_unrest_events.txt:2674；events/flavorUSM_ce.txt:22|
|`flavorUSM.1.f`|16|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/ce_fra_unrest_events.txt:2677；events/flavorUSM_ce.txt:24|
|`flavorUSM.1.1`|17|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:43|
|`flavorUSM.2.t`|19|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:60|
|`flavorUSM.2.d`|20|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:62|
|`flavorUSM.2.f`|21|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:65|
|`flavorUSM.2.1`|22|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:184|
|`flavorUSM.3.t`|24|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:246|
|`flavorUSM.3.d`|25|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:248|
|`flavorUSM.3.f`|26|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:251|
|`flavorUSM.3.1`|27|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:370|
|`USM_discriminated_provinces`|34|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:159；events/flavorUSM_ce.txt:197|
|`USM_change_of_time`|35|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:169；events/flavorUSM_ce.txt:399|
|`USM_conflict_invalid`|36|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:139；events/flavorUSM_ce.txt:373|
|`USM_looming_conflicts`|37|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:154；common/static_modifiers/ce_event_modifiers.txt:133|
|`USM_change_of_wind`|38|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:227；events/flavorUSM_ce.txt:770|
|`USM_loyal_subject`|39|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:177；events/usm_civilwar_events.txt:328|
|`USM_wuu_post_war_modifier`|40|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:183；events/usm_civilwar_events.txt:1281|
|`USM_not_wuu_post_war_modifier`|41|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:194；events/usm_civilwar_events.txt:1380|
|`USM_collapsed_dynasty`|42|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:215；events/usm_civilwar_events.txt:1326|
|`USM_not_wuu_post_war_rev_modifier`|43|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:203；events/usm_civilwar_events.txt:1430|
|`usm_civilwar.9.t.happened`|44|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`others_have_overthrown_usm`|45|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`become_who_have_overthrown_usm`|46|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`trigger_zone_no_valid_ce.tt`|47|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`you_are_here_because_you_are_usm_side_tt`|48|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`you_are_here_because_you_are_rebel_side_tt`|49|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`you_are_here_because_you_are_not_involved_tt`|50|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.sichuan_contoller_tooltip`|51|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.hubei_contoller_tooltip`|52|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.guangxi_contoller_tooltip`|53|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.luzon_contoller_tooltip`|54|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.yuannan_contoller_tooltip`|55|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.sumatra_contoller_tooltip`|56|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_cw.kyushu_contoller_tooltip`|57|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_won_the_civil_war_tt`|58|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`information_on_the_other_side_usm_cw.usm`|59|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`information_on_the_other_side_usm_cw.rebel`|60|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`paradox_you_are_stubid.tt.usm_cw`|61|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`future_concequences_ce.tt`|62|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`USM_jap_nothing_good`|63|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:232；events/usm_civilwar_events.txt:2371|
|`USM_pingwu_dagao`|64|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:222；events/usm_civilwar_events.txt:417|
|`ce_Wei`|65|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/character_templates/zz_historical_leaders_ce_asia.txt:893|
|`name_Jian`|66|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/character_templates/zz_historical_leaders_ce_asia.txt:892|
|`ce_nothing_happen_tt`|67|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`sih_shuwang_ran_off_tt`|68|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`USM_domination_over_ming`|69|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:145；events/usm_civilwar_events.txt:1407|
|`ce_oldman_s_healthy`|71|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_oldman_s_healthy_desc`|72|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`flavorUSM.5.t`|74|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:716|
|`flavorUSM.5.d`|75|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:725|
|`flavorUSM.5.f`|76|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:728|
|`flavorUSM.5.1`|77|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:761|
|`flavorUSM.6.d1`|81|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:819|
|`flavorUSM.6.f`|82|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:826|
|`flavorUSM.6.1`|83|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:848|
|`flavorUSM.7.t`|85|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:892|
|`flavorUSM.7.d`|86|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:894|
|`flavorUSM.7.f`|87|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:897|
|`flavorUSM.7.1`|88|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:922|
|`flavorUSM.8.t`|90|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:932|
|`flavorUSM.8.d`|91|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:934|
|`flavorUSM.8.f`|92|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:937|
|`flavorUSM.8.1`|93|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1004|
|`flavorUSM.9.t`|95|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1110|
|`flavorUSM.9.d`|96|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1112|
|`flavorUSM.9.f`|97|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1115|
|`flavorUSM.9.1`|98|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1175|
|`flavorUSM.10.t`|100|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1283|
|`flavorUSM.10.d`|101|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1285|
|`flavorUSM.10.f`|102|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1288|
|`flavorUSM.10.1`|103|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:1347|
|`increase_usm_conflicts_25`|105|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorUSM_ce.txt:763；events/flavorUSM_ce.txt:850|
|`give_100_chance_to_discover_zheng_diaojin.tt`|107|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_conflicts_invalid_tt_1`|108|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:125|
|`ce_usm_conflicts_invalid_tt_2`|109|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:134|
|`ce_usm_conflict_evoked_tt`|110|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:251|
|`ce_usm_conflict_fail_tt`|111|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:269|
|`modifier_new_found_dynasty_wuu`|112|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:258；common/static_modifiers/ce_event_modifiers.txt:111|
|`ce_usm_ruling_of_nanfu_modifier`|113|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:246；common/static_modifiers/ce_event_modifiers.txt:103|
|`ce_usm_lunzhan_modifier`|115|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:8；common/static_modifiers/ce_event_modifiers.txt:92|
|`ce_usm_conflicts_within`|116|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:1；common/journal_entries/ce_usm_the_last_days_of_ming.txt:237|
|`ce_usm_conflicts_within_remove`|117|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_conflicts_within_goal`|119|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_ruling_of_nanfu`|121|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:231|
|`ce_usm_ruling_of_nanfu_reason`|122|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_political_reason_ban.tt.USM.1`|130|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`is_opposition_usm.tt`|131|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar_play`|132|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/scripted_effects/nesnd_crisis_effects.txt:282|
|`ce_usm_civilwar_journal`|133|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:297；events/flavorUSM_ce.txt:685|
|`ce_usm_civilwar_journal_reason`|134|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_civilwar_journal_fail.tt`|136|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_civilwar_journal_invalid.t1`|137|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_civilwar_journal_invalid.t2`|138|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_suppress_rebellion`|140|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:339；events/usm_civilwar_events.txt:388|
|`ce_usm_suppress_rebellion_reason`|141|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_restoration_of_ming`|143|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:372；common/scripted_effects/nesnd_ming_court.txt:143|
|`ce_usm_restoration_of_ming_reason`|144|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_acheive_revolution`|146|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:432；events/usm_civilwar_events.txt:501|
|`ce_usm_acheive_revolution_reason`|147|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_cw_japanese_interest`|149|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:492；events/usm_civilwar_events.txt:2531|
|`usm_surrender_to_target_country.1`|152|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_surrender_to_target_country.2`|153|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`capture_enemy_capital_usm.1`|155|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.1`|156|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.2`|157|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.3`|158|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.4`|159|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.5`|160|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip.6`|161|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`not_an_opposition_usm_tooltip`|162|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.8.tt`|164|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1279|
|`lost_all_occupied_region_in_jap_usm`|165|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1714；events/usm_civilwar_events.txt:1783|
|`receive_all_occupied_state_jap_ce`|166|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2198|
|`lost_all_occupied_region_in_jap_but_usm_retaliate`|167|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1872|
|`usm_civilwar.1.t`|168|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:6|
|`usm_civilwar.1.f`|170|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:8|
|`usm_civilwar_participate`|174|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:119；events/usm_civilwar_events.txt:236|
|`SHA_gold_mines`|176|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:245；common/history/countries/SHA.txt:25|
|`USM_civilwar_buffer`|177|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:240|
|`usm_civilwar.2.d1`|180|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.2.d2`|181|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.2.f`|183|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2328|
|`RULER_TITLE_CE_TAISHI`|190|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/government_types/00_ce_government_types.txt:5；common/government_types/00_ce_government_types.txt:6|
|`RULER_TITLE_CE_FANWANG`|191|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/government_types/00_ce_government_types.txt:49；common/government_types/00_ce_government_types.txt:50|
|`usm_civilwar.3.d1`|195|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.3.f`|196|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.3.2`|198|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.4.t`|200|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:580；events/usm_civilwar_events.txt:866|
|`usm_civilwar.4.d`|201|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:584；events/usm_civilwar_events.txt:870|
|`usm_civilwar.4.d1`|202|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:590；events/usm_civilwar_events.txt:876|
|`usm_civilwar.4.d2`|203|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:596；events/usm_civilwar_events.txt:882|
|`usm_civilwar.4.d3`|204|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:602；events/usm_civilwar_events.txt:888|
|`usm_civilwar.4.d4`|205|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:608；events/usm_civilwar_events.txt:894|
|`usm_civilwar.4.d5`|206|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:614；events/usm_civilwar_events.txt:900|
|`usm_civilwar.4.f`|207|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:635；events/usm_civilwar_events.txt:921|
|`usm_civilwar.4.1`|208|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:661|
|`usm_civilwar.4.2`|209|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:684|
|`usm_civilwar.6.t`|211|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1101|
|`usm_civilwar.6.d`|212|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1102|
|`usm_civilwar.6.f`|213|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1103|
|`usm_civilwar.6.1`|214|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1118|
|`usm_civilwar.7.t`|216|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1141|
|`usm_civilwar.7.d`|217|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1142|
|`usm_civilwar.7.f`|218|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1143|
|`usm_civilwar.7.1`|219|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1176|
|`usm_civilwar.8.t`|221|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1258|
|`usm_civilwar.8.d`|222|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1259|
|`usm_civilwar.8.f`|223|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1260|
|`usm_civilwar.8.1`|224|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1274|
|`usm_loss_the_civil_war_tt`|226|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.9.t`|227|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1297|
|`usm_civilwar.9.d`|228|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1298|
|`usm_civilwar.9.f`|229|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1299|
|`usm_civilwar.9.1`|230|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1320|
|`usm_civilwar.10.f`|234|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.11.t`|239|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1446|
|`usm_civilwar.11.d`|240|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1447|
|`usm_civilwar.11.f`|241|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1448|
|`usm_civilwar.11.1`|242|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1473|
|`usm_civilwar.11.2`|243|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1508|
|`usm_civilwar.12.f`|247|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1576|
|`usm_civilwar.12.1`|248|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1597|
|`usm_civilwar.13.f`|252|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1623|
|`usm_civilwar.13.1`|253|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1644|
|`usm_civilwar.14.t`|255|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1664|
|`usm_civilwar.14.d`|256|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1665|
|`usm_civilwar.14.f`|257|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1666|
|`usm_civilwar.14.1`|258|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1699|
|`usm_civilwar.15.t`|260|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1761|
|`usm_civilwar.15.d`|261|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1762|
|`usm_civilwar.15.f`|262|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1763|
|`usm_civilwar.15.1`|263|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1778|
|`usm_civilwar.16.t`|265|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1826|
|`usm_civilwar.16.d`|266|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1827|
|`usm_civilwar.16.f`|267|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1828|
|`usm_civilwar.16.1`|268|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1843|
|`usm_civilwar.16.2`|269|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1862|
|`usm_civilwar.17.t`|271|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1916|
|`usm_civilwar.17.d`|272|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1917|
|`usm_civilwar.17.f`|273|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:1918|
|`usm_civilwar.17.1`|274|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2184|
|`usm_civilwar.18.t`|276|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2250|
|`usm_civilwar.18.d`|277|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2251|
|`usm_civilwar.18.f`|278|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2252|
|`usm_civilwar.18.1`|279|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2267|
|`usm_civilwar.19.t`|281|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2296|
|`usm_civilwar.19.d`|282|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2297|
|`usm_civilwar.19.f`|283|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2298|
|`usm_civilwar.19.1`|284|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2313|
|`usm_civilwar.20.t`|286|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2326|
|`usm_civilwar.20.d`|287|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2327|
|`usm_civilwar.20.1`|288|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2359|
|`usm_civilwar.20.2`|289|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2390|
|`usm_civilwar.21.t`|291|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2424|
|`usm_civilwar.21.d`|292|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2425|
|`usm_civilwar.21.f`|293|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2426|
|`usm_civilwar.21.1`|294|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2441|
|`usm_civilwar.22.t`|296|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2461|
|`usm_civilwar.22.d`|297|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2462|
|`usm_civilwar.22.f`|298|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2463|
|`usm_civilwar.22.1`|299|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2481|
|`usm_civilwar.23.f`|303|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.24.t`|308|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2561|
|`usm_civilwar.24.d`|309|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2562|
|`usm_civilwar.24.f`|310|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2563|
|`usm_civilwar.24.1`|311|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2578|
|`usm_civilwar.25.t`|313|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2593|
|`usm_civilwar.25.d`|314|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2594|
|`usm_civilwar.25.f`|315|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2595|
|`usm_civilwar.25.1`|316|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2623|
|`usm_civilwar.26.t`|318|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2641|
|`usm_civilwar.26.d`|319|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2652|
|`usm_civilwar.26.f`|320|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2657|
|`usm_civilwar.26.1`|321|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/usm_civilwar_events.txt:2672|
|`ce_caved_to_OPEN_pressure_opposition`|323|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:448；events/flavorJAP_ce.txt:73|
|`ce_caved_to_OPEN_pressure_government`|324|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:453；events/flavorJAP_ce.txt:84|
|`ce_land_owner_change_sides`|325|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:459；events/flavorJAP_ce.txt:230|
|`ce_royal_ig_changed_back`|326|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:471；events/flavorJAP_ce.txt:491|
|`ce_royal_ig_pressed_by_monarch`|327|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:466；events/flavorJAP_ce.txt:407|
|`USM_benifit_of_an_emperor`|329|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/static_modifiers/ce_event_modifiers.txt:152；events/usm_civilwar_events.txt:2686|
|`flavorJAP_ce.1.t`|331|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:18|
|`flavorJAP_ce.1.d`|332|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:20|
|`flavorJAP_ce.1.f`|333|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:23|
|`flavorJAP_ce.1.1`|334|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:57|
|`flavorJAP_ce.2.t`|336|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:103|
|`flavorJAP_ce.2.d`|337|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:105|
|`flavorJAP_ce.2.f`|338|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:108|
|`flavorJAP_ce.2.1`|339|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:184|
|`flavorJAP_ce.2.2`|340|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:242|
|`flavorJAP_ce.3.t`|342|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:315|
|`flavorJAP_ce.3.d`|343|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:317|
|`flavorJAP_ce.3.f`|344|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:320|
|`flavorJAP_ce.3.1`|345|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:396|
|`flavorJAP_ce.3.2`|346|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：events/flavorJAP_ce.txt:420|
|`ce_usm_conflict_looming_tt`|348|保留作者原文|成熟作者基线逐字一致；本轮无制度冲突改动。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:282|
### localization/simp_chinese/replace/nesnd_japan_l_simp_chinese.yml

共7键；主MOD SHA256 `9a2d353cb69b0dac9f26142d570aae330f81abc2cc2e6498bb1cc55e5f89b7e9`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_wu_eastern_question`|8|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_japan.txt:1|
|`nesnd_wu_eastern_question_reason`|9|日本交接|三日本政权叙述不一致，已通知主代理。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_wu_eastern_question_status`|10|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_japan.txt:18|
|`nesnd_wu_eastern_question_status_offer`|11|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_japan.txt:17|
|`nesnd_wu_eastern_question_status_war`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_japan.txt:16|
|`nesnd_wu_eastern_question_goal`|13|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_wu_eastern_question_progress`|47|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
### localization/simp_chinese/replace/zz_nesnd_crisis_l_simp_chinese.yml

共97键；主MOD SHA256 `fb93963c5893bf59898a74d16c217312f13a93d28e1a13e27891599260b2af1f`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`flavorUSM.4.t`|102|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/flavorUSM_ce.txt:485|
|`flavorUSM.4.d`|103|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/flavorUSM_ce.txt:486|
|`flavorUSM.4.f`|151|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/flavorUSM_ce.txt:710|
|`flavorUSM.4.1`|101|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/flavorUSM_ce.txt:704|
|`flavorUSM.6.t`|104|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/flavorUSM_ce.txt:809|
|`flavorUSM.6.d`|105|重写|现行flavorUSM.6是死亡后续，旧AI文字误写仅离开首辅。明确死亡但不强写遇刺，兼容自然死亡。 来源：events/flavorUSM_ce.txt:813|
|`ce_usm_conflicts_within_reason`|100|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`ce_usm_cw_japanese_interest_reason`|134|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.1.d`|106|重写|避免尚未正式执行accession就称已有天子诏；国际国家与国内省分开。 来源：events/usm_civilwar_events.txt:7|
|`usm_civilwar.1.1`|107|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/usm_civilwar_events.txt:35；events/usm_civilwar_events.txt:152|
|`usm_civilwar.1.2`|108|重写|仅中国branch适用，海外或日本须保留本国；建议正文中泛称本国，选项改本国见report。 来源：events/usm_civilwar_events.txt:270|
|`usm_civilwar.1.3`|109|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:304|
|`usm_civilwar.2.t`|115|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:358|
|`usm_civilwar.2.d`|116|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/usm_civilwar_events.txt:359|
|`usm_civilwar.2.1`|110|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:379|
|`usm_civilwar.2.2`|111|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:392|
|`usm_civilwar.2.3`|112|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:483|
|`usm_civilwar.2.4`|113|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:515|
|`usm_civilwar.2.5`|114|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:524|
|`usm_civilwar.3.t`|118|重写|统一本轮设定与名称，保持原有数值和功能。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.3.d`|119|重写|准确无共同反吴联盟不等于全体同意整合。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.3.1`|117|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`usm_civilwar.10.t`|123|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1340|
|`usm_civilwar.10.d`|124|重写|此处真正军事联盟保留联盟；不给各地议局赋予中央国会职权。 来源：events/usm_civilwar_events.txt:1341|
|`usm_civilwar.10.1`|120|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1358|
|`usm_civilwar.10.2`|121|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1388|
|`usm_civilwar.10.3`|122|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1415|
|`usm_civilwar.12.t`|125|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1574|
|`usm_civilwar.12.d`|126|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1575|
|`usm_civilwar.13.t`|127|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:1621|
|`usm_civilwar.13.d`|128|重写|去册籍道具；留实际country引用。 来源：events/usm_civilwar_events.txt:1622|
|`usm_civilwar.23.t`|132|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:2515|
|`usm_civilwar.23.d`|133|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:2516|
|`usm_civilwar.23.1`|129|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:2535|
|`usm_civilwar.23.2`|130|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:2542|
|`usm_civilwar.23.3`|131|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/usm_civilwar_events.txt:2549|
|`nesnd_hna_academy`|43|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:36；common/scripted_effects/nesnd_supply_effects.txt:15|
|`nesnd_hna_supply`|44|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:43；common/scripted_effects/nesnd_supply_effects.txt:21|
|`nesnd_hna_veterans`|45|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:50；common/scripted_effects/nesnd_supply_effects.txt:27|
|`nesnd_hna_prepared`|46|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_effects/nesnd_supply_effects.txt:9；common/scripted_effects/nesnd_supply_effects.txt:11|
|`nesnd_federal_compact`|47|重写|此修正是明廷内部权力约束，不是国际宗盟。 来源：common/scripted_effects/nesnd_ming_court.txt:221；common/scripted_effects/nesnd_south_peace.txt:418|
|`nesnd_court_protection`|48|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_effects/nesnd_chen_security.txt:8；common/scripted_effects/nesnd_chen_security.txt:8|
|`nesnd_wu_administration`|49|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:13；events/nesnd_crisis_events.txt:207|
|`nesnd_wu_clemency`|50|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:14；events/nesnd_crisis_events.txt:138|
|`nesnd_wu_repression`|51|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:15；events/nesnd_crisis_events.txt:212|
|`nesnd_foreign_commitment`|52|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:16；events/nesnd_crisis_events.txt:168|
|`nesnd_foreign_supplies`|53|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:17；events/nesnd_crisis_events.txt:168|
|`nesnd_refugee_reception`|54|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:18|
|`nesnd_maritime_security`|55|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:19|
|`nesnd_japan_reorganization`|56|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/static_modifiers/nesnd_crisis_modifiers.txt:20；events/nesnd_crisis_events.txt:234|
|`nesnd_huguang_preparations`|57|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/journal_entries/nesnd_regional_preparations.txt:2|
|`nesnd_huguang_preparations_reason`|58|重写|保留作者对西府政治根基和郑氏排挤的叙述；学政不作学籍/教育机关；朱斑博统一为朱班博。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_hna_academy_button`|59|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:32；common/scripted_buttons/nesnd_crisis_buttons.txt:32|
|`nesnd_hna_academy_button_desc`|60|重写|按最新用户设定重写政治教育因果；不把书院降格为粮饷培训；考试只叙述制度，不冒称按钮有考试机制。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:32|
|`nesnd_hna_supply_button`|61|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:39；common/scripted_buttons/nesnd_crisis_buttons.txt:39|
|`nesnd_hna_supply_button_desc`|62|重写|保留作者政治口吻与真实省际协定；此处约不是宪法，不能机械改为礼法。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:39|
|`nesnd_hna_veterans_button`|63|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:46；common/scripted_buttons/nesnd_crisis_buttons.txt:46|
|`nesnd_hna_veterans_button_desc`|64|重写|保留作者退伍组织与社会改革主题；删除冗余断句。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:46|
|`nesnd_federal_compact_button`|65|重写|作者旧按钮名保留为兼容键；真实按钮引用south_offer。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:53|
|`nesnd_federal_compact_button_desc`|66|重写|采用作者拥明主张；内阁六部、一院制礼议院；把即时效果写为遣使争取支持。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.10.a`|69|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：events/nesnd_crisis_events.txt:134|
|`nesnd_crisis.10.t`|70|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：events/nesnd_crisis_events.txt:128|
|`nesnd_crisis.10.d`|71|重写|作者稿精修；绝对多数/永久消灭所有地方权力无机制依据，改为支持新法和权力边界。【闲置/兼容字段，未接入现行界面】 来源：events/nesnd_crisis_events.txt:128|
|`nesnd_crisis.11.a`|72|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.11.b`|73|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.11.t`|74|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.11.d`|75|重写|保留作者刑部/大理寺/锦衣卫办案争议，修复碎句；当前不可见。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.20.a`|76|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:159|
|`nesnd_crisis.20.b`|77|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:164|
|`nesnd_crisis.20.c`|78|重写|襄樊是据点/大营，不造“襄樊诸府”。 来源：events/nesnd_crisis_events.txt:170|
|`nesnd_crisis.20.t`|79|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_crisis_events.txt:153|
|`nesnd_crisis.20.d`|80|重写|保留北朝敌视吴的阵营语气；原稿无条件说土改继续，事件实际可在土改后触发，改条件性。 来源：events/nesnd_crisis_events.txt:153|
|`nesnd_crisis.21.a`|81|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.21.b`|82|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.21.c`|83|重写|统一本轮设定与名称，保持原有数值和功能。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.21.t`|84|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.21.d`|85|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.40.a`|86|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:203|
|`nesnd_crisis.40.b`|87|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:208|
|`nesnd_crisis.40.t`|88|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:197|
|`nesnd_crisis.40.d`|89|重写|作者English稿“伪南府”与吴胜利事件本方叙述相冲突，明确删伪；非擅改敌方立场。 来源：events/nesnd_crisis_events.txt:197|
|`nesnd_crisis.41.a`|90|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:230|
|`nesnd_crisis.41.b`|91|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:235|
|`nesnd_crisis.41.t`|92|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:224|
|`nesnd_crisis.41.d`|93|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:224|
|`nesnd_early_accession`|98|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:205；common/scripted_buttons/nesnd_crisis_buttons.txt:68|
|`nesnd_early_accession_desc`|99|重写|旧文“一并列入版籍”承诺不存在即时吞并；实际只是易代事件与表态链。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:70|
|`nesnd_huguang_preparations_status`|143|重写|更新组织名称；保留旧机制说明作为闲置键。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_south_status_qin`|144|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:224|
|`nesnd_south_pressure_bar`|147|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:206；common/scripted_effects/nesnd_presentation_effects.txt:45|
|`nesnd_south_compact_bar`|149|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:207；common/scripted_effects/nesnd_presentation_effects.txt:49|
|`nesnd_crisis.11.f`|152|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.10.f`|157|重写|本轮拟写引文，不冒称已存在作者史料。【闲置/兼容字段，未接入现行界面】 来源：events/nesnd_crisis_events.txt:145|
|`nesnd_crisis.20.f`|158|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:182|
|`nesnd_crisis.21.f`|159|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_crisis.40.f`|160|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:219|
|`nesnd_crisis.41.f`|161|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：events/nesnd_crisis_events.txt:246|
### localization/simp_chinese/replace/zz_nesnd_crisis_rules_l_simp_chinese.yml

共9键；主MOD SHA256 `373699009053b67b48075ebf74faf2952fc1e5286c92020c9c9c7e7c43f84f05`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_hna_academy_button_requirements`|7|重写|旧提示误称军校；按现有按钮flag修正。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:33|
|`nesnd_hna_academy_button_outcome_tt`|8|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:35|
|`nesnd_hna_supply_button_requirements`|9|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:40|
|`nesnd_hna_supply_button_outcome_tt`|10|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:42|
|`nesnd_hna_veterans_button_requirements`|11|重写|旧提示误称整编老营。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:47|
|`nesnd_hna_veterans_button_outcome_tt`|12|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:49|
|`nesnd_federal_compact_button_requirements`|13|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_protect_chen_button_outcome_tt`|16|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。【闲置/兼容字段，未接入现行界面】 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_early_accession_requirements`|17|重写|修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:76|
### localization/simp_chinese/replace/zzzz_nesnd_usm_local_authority_l_simp_chinese.yml

共1键；主MOD SHA256 `a833dd9a10c6b710ab596646812d4d31cfa297acdf811ba019dd04327538d1f7`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_usm_old_guard_local`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/static_modifiers/nesnd_usm_local_authority.txt:3；events/flavorUSM_ce.txt:387|
### localization/simp_chinese/replace/zzzzz_nesnd_south_journal_ui_l_simp_chinese.yml

共10键；主MOD SHA256 `140db9380e3e0e3bc2994039e518cfef67e70382bc3abdcf2f49c32ea63ac48a`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_south_status_succession`|13|重写|状态只描述现状；日期门槛已由规则提示承担，不预告所有案件必然结束。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:226|
|`nesnd_south_rules`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_south_pressure_bar_desc`|8|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_crisis_bars.txt:31|
|`nesnd_south_compact_bar_desc`|9|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_progress_bars/nesnd_crisis_bars.txt:32|
|`nesnd_south_unsettled_tt`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:41|
|`nesnd_south_qin_departed_tt`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:47|
|`nesnd_south_conflicts_failure_tt`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:69|
|`nesnd_south_settled_tt`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:166|
|`nesnd_south_wu_established_tt`|6|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:170|
|`nesnd_south_monarchy_ended_tt`|7|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:174|
### localization/simp_chinese/replace/zzzzzz_nesnd_chen_security_l_simp_chinese.yml

共35键；主MOD SHA256 `89becbf5f2e583bfab49ce3c46b5793aae9b57e9709c8252136006d8ca7e3d95`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_protect_chen_button`|2|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:204；common/scripted_buttons/nesnd_crisis_buttons.txt:61|
|`nesnd_protect_chen_button_desc`|3|重写|把用户保护改革领袖的动机接到真正后覆盖警卫按钮；保留真实有期限/风险，不恢复旧永久保护。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:61|
|`nesnd_protect_chen_button_requirements`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:63|
|`nesnd_chen_inner_guard`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_chen_security.txt:9；common/scripted_effects/nesnd_chen_security.txt:9|
|`nesnd_chen_residence_guard`|6|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_chen_security.txt:10；common/scripted_effects/nesnd_chen_security.txt:10|
|`nesnd_chen_intelligence`|7|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_chen_security.txt:11；common/scripted_effects/nesnd_chen_security.txt:11|
|`nesnd_chen.1.t`|8|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:4|
|`nesnd_chen.1.d`|9|重写|采用作者攻击改革领袖背景；删账册隐喻；保留具体代价与术语。 来源：events/nesnd_chen_security.txt:9|
|`nesnd_chen.1.active`|10|重写|英文旧句仍把已修中文变回名册日查；同步明确内阁护卫和经费主体。 来源：events/nesnd_chen_security.txt:8|
|`nesnd_chen.1.f`|11|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:11|
|`nesnd_chen.1.a`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:14|
|`nesnd_chen.1.b`|13|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:15|
|`nesnd_chen.1.c`|14|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:16|
|`nesnd_chen.1.e`|15|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:17|
|`nesnd_chen.1.z`|16|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:18|
|`nesnd_chen.guard_tt`|17|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:14|
|`nesnd_chen.residence_tt`|18|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:15|
|`nesnd_chen.intel_tt`|19|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:16|
|`nesnd_chen.3.t`|20|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:98|
|`nesnd_chen.3.d`|21|重写|南朝省制；不把各省称府。其余人物叙事保留。 来源：events/nesnd_chen_security.txt:98|
|`nesnd_chen.3.f`|22|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:98|
|`nesnd_chen.3.a`|23|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:100|
|`nesnd_chen.wounded_tt`|24|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:100|
|`nesnd_chen.4.t`|25|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:104|
|`nesnd_chen.4.d`|26|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:104|
|`nesnd_chen.4.f`|27|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:104|
|`nesnd_chen.4.a`|28|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:106|
|`nesnd_chen.escape_tt`|29|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:106|
|`nesnd_chen.3.residence`|30|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:98|
|`nesnd_chen.4.residence`|31|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:104|
|`nesnd_chen.death_residence_desc`|32|重写|南朝省制；不把各省称府。其余人物叙事保留。 来源：events/flavorUSM_ce.txt:723|
|`nesnd_chen.1.residence`|33|重写|英文旧句仍把已修中文变回名册日查；同步明确内阁护卫和经费主体。 来源：events/nesnd_chen_security.txt:7|
|`nesnd_chen.1.intel`|34|重写|英文旧句仍把已修中文变回名册日查；同步明确内阁护卫和经费主体。 来源：events/nesnd_chen_security.txt:6|
|`nesnd_chen.finance_rules`|35|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_chen.withdraw_tt`|36|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_chen_security.txt:17|
### localization/simp_chinese/replace/zzzzzz_nesnd_succession_board_l_simp_chinese.yml

共27键；主MOD SHA256 `c2cd174ba0dd71bab627bcaba1df5e1eecbada1935792d1d96ba3b986c37a06c`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_federal_compact_button_outcome_tt`|33|闲置旧机制|旧+20/−8/18月循环无当前caller；现行遣使6月/36月承诺，不得把旧数值当上线效果。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`je_group_nesnd_succession`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:3；common/journal_entry_groups/nesnd_succession.txt:1|
|`nesnd_south_succession_board`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:1；common/scripted_buttons/nesnd_succession_board.txt:5|
|`nesnd_south_succession_board_status`|5|重写|统一本轮设定与名称，保持原有数值和功能。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_board_table_heading`|6|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：gui/journal_entry_widgets/nesnd_succession_board.gui:8|
|`nesnd_board_supply_known`|8|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:13；common/customizable_localization/nesnd_succession_board.txt:13|
|`nesnd_board_supply_unknown`|9|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:14|
|`nesnd_board_stance_unstated`|10|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:9|
|`nesnd_board_stance_ming`|11|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:5|
|`nesnd_board_stance_wu`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:6|
|`nesnd_board_stance_neutral`|13|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:7|
|`nesnd_board_stance_autonomy`|14|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:8|
|`nesnd_board_stance_available_tt`|15|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_succession_board.txt:16；common/scripted_buttons/nesnd_succession_board.txt:71|
|`nesnd_board_choose_ming`|17|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:28；common/scripted_buttons/nesnd_succession_board.txt:1|
|`nesnd_board_choose_ming_desc`|18|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_succession_board.txt:3|
|`nesnd_board_choose_wu`|19|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:29；common/scripted_buttons/nesnd_succession_board.txt:56|
|`nesnd_board_choose_wu_desc`|20|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_succession_board.txt:58|
|`nesnd_board_choose_neutral`|21|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:30；common/scripted_buttons/nesnd_succession_board.txt:111|
|`nesnd_board_choose_neutral_desc`|22|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_succession_board.txt:113|
|`nesnd_board_choose_autonomy`|23|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:31；common/scripted_buttons/nesnd_succession_board.txt:172|
|`nesnd_board_choose_autonomy_desc`|24|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_succession_board.txt:174|
|`nesnd_board_pressure_bar_name`|30|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:23|
|`nesnd_board_pressure_bar_desc`|32|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:24|
|`nesnd_board_not_ming_tt`|35|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_succession_board.txt:20|
|`nesnd_board_not_wu_tt`|36|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_succession_board.txt:75|
|`nesnd_board_not_neutral_tt`|37|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_succession_board.txt:136|
|`nesnd_board_not_autonomy_tt`|38|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_succession_board.txt:197|
### localization/simp_chinese/replace/zzzzzzz_nesnd_ming_court_l_simp_chinese.yml

共32键；主MOD SHA256 `70c014fef2f53014654c1d62245e3aeff9d10c8b9acc43f54d03c46b519c6949`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_south_succession_board_reason`|22|重写|去同一张案/账册隐喻；区分西府与南府；保留作者论争社会范围。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_ming_host_huguang`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:19；common/scripted_buttons/nesnd_ming_court.txt:1|
|`nesnd_ming_host_huguang_desc`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_ming_court.txt:2|
|`nesnd_ming_host_sichuan`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:20；common/scripted_buttons/nesnd_ming_court.txt:8|
|`nesnd_ming_host_sichuan_desc`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_ming_court.txt:9|
|`nesnd_ming_host_effect_tt`|6|重写|删除“目标失效/另一核心”内部术语。 来源：common/scripted_buttons/nesnd_ming_court.txt:6；common/scripted_buttons/nesnd_ming_court.txt:13|
|`nesnd_ming_renew_convocation`|7|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:22；common/scripted_buttons/nesnd_ming_court.txt:15|
|`nesnd_ming_renew_convocation_desc`|8|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_ming_court.txt:16|
|`nesnd_ming_court.3.t`|9|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:6|
|`nesnd_ming_court.3.d`|10|重写|删除印信厅堂清册堆砌，写行在的政治与财政代价。 来源：events/nesnd_ming_court.txt:6|
|`nesnd_ming_court.3.a`|11|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:9|
|`nesnd_ming_court.9.t`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:12|
|`nesnd_ming_court.9.d`|13|重写|具体接驾失败原因，不用文书道具代替政治冲突。 来源：events/nesnd_ming_court.txt:12|
|`nesnd_ming_court.9.a`|14|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:16|
|`nesnd_ming_court.9.b`|15|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:19|
|`nesnd_ming_court.10.t`|16|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_ming_court.txt:29|
|`nesnd_ming_court.10.d`|17|重写|这是实际未形成反吴联盟，不是所有人已经签约。 来源：events/nesnd_ming_court.txt:29|
|`nesnd_ming_court.10.a`|18|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_ming_court.txt:31|
|`nesnd_ming_court_country`|19|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/dynamic_country_names/zz_nesnd_ming_court.txt:31；common/dynamic_country_names/zz_nesnd_ming_court.txt:84|
|`nesnd_ming_interregnum_country`|20|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/dynamic_country_names/zz_nesnd_ming_court.txt:37；common/dynamic_country_names/zz_nesnd_ming_court.txt:90|
|`nesnd_ming_court_adj`|21|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/dynamic_country_names/zz_nesnd_ming_court.txt:31；common/dynamic_country_names/zz_nesnd_ming_court.txt:37|
|`nesnd_ming_court_transfer_effect_tt`|23|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:9|
|`nesnd_ming_court.12.t`|24|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:38|
|`nesnd_ming_court.12.d`|25|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_ming_court.txt:38|
|`nesnd_ming_court.12.a`|26|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:41|
|`nesnd_ming_court.12.b`|27|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_ming_court.txt:45|
|`nesnd_ming_seek_refuge`|28|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:21；common/scripted_buttons/nesnd_ming_court.txt:22|
|`nesnd_ming_seek_refuge_desc`|29|重写|删除查询“核对条件”和状态维持实现说明。 来源：common/scripted_buttons/nesnd_ming_court.txt:23|
|`nesnd_ming_after_truce`|30|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_ming_after_truce.txt:1|
|`nesnd_ming_after_truce_reason`|31|重写|统一本轮设定与名称，保持原有数值和功能。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_ming_after_truce_status`|32|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_ming_refuge_available_tt`|33|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_ming_court.txt:26|
### localization/simp_chinese/replace/zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml

共52键；主MOD SHA256 `356917203ecd3d0011176a7dfd723854046420fbf7079c4dfa468e4f1703a2a7`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_south_compact_detail_tt`|52|重写|指标统计支持不是宪法本身，不称国制为盟约；与中央交战才失效，保留数值。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_board_country_metrics`|53|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：gui/journal_entry_widgets/nesnd_succession_board.gui:36|
|`nesnd_board_stance_effect_tt`|17|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_succession_board.txt:34；common/scripted_buttons/nesnd_succession_board.txt:89|
|`nesnd_board_ming_bar_name`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:2|
|`nesnd_board_wu_bar_name`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:9|
|`nesnd_board_ming_bar_desc`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:3|
|`nesnd_board_wu_bar_desc`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:10|
|`nesnd_board_compact_bar_name`|6|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:16|
|`nesnd_board_compact_bar_desc`|7|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_progress_bars/nesnd_succession_board.txt:17|
|`nesnd_south_offer_accord`|9|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_succession_board.txt:26；common/scripted_buttons/nesnd_crisis_buttons.txt:54|
|`nesnd_south_offer_accord_desc`|10|重写|中性回退，只说明当前按钮发送提案；不宣称点击就通过宪法。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:54；common/scripted_buttons/nesnd_south_accords.txt:3|
|`nesnd_south_offer_available_tt`|11|重写|in_default不是违约；保留实际门槛。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:56；common/scripted_buttons/nesnd_south_accords.txt:9|
|`nesnd_south_accord_offer_tt`|12|重写|保留发送行为和实际成本，区分国家礼法与各方同意。 来源：common/scripted_buttons/nesnd_crisis_buttons.txt:58；common/scripted_buttons/nesnd_south_accords.txt:17|
|`nesnd_south_accord_accept_tt`|13|重写|旧文“对吴交战”漏掉明廷；保留36/6/15及真实割地风险。 来源：events/nesnd_south_accords.txt:95；events/nesnd_south_accords.txt:154|
|`nesnd_south_leave_accord`|14|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_succession_board.txt:27；common/scripted_buttons/nesnd_south_accords.txt:23|
|`nesnd_south_leave_accord_desc`|15|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_south_accords.txt:25|
|`nesnd_south_accord_leave_tt`|16|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_south_accords.txt:39|
|`nesnd_south_retry_confrontation`|18|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_succession_board.txt:25；common/scripted_buttons/nesnd_south_accords.txt:51|
|`nesnd_south_retry_confrontation_desc`|19|重写|各府改为地方，不误称布政司为独立府。 来源：common/scripted_buttons/nesnd_south_accords.txt:52|
|`nesnd_south_accords.1.t`|20|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:7|
|`nesnd_south_accords.1.ming`|21|重写|用宪法说明中央内部制度；明确不自动吞并、不直接改变各成员法律；真实外交条约保留。 来源：events/nesnd_south_accords.txt:14|
|`nesnd_south_accords.1.integration`|22|重写|删除簿册移交流水账；说明真实主权代价；只写接受条款，尚未即时转移领土。 来源：events/nesnd_south_accords.txt:20|
|`nesnd_south_accords.1.japan`|23|重写|实际日本割地条件是外交条款，仍保留；不把未来吴政权叫现成新朝。 来源：events/nesnd_south_accords.txt:26|
|`nesnd_south_accords.1.overseas`|24|重写|保留国际承认/宗属/条约，不以礼法替换外交安排。 来源：events/nesnd_south_accords.txt:28|
|`nesnd_south_accords.1.a`|25|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:38|
|`nesnd_south_accords.1.b`|26|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:99|
|`nesnd_south_accords.1.c`|27|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:158|
|`nesnd_south_accords.1.d`|28|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:209|
|`nesnd_south_accords.20.t`|29|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:225|
|`nesnd_south_accords.20.d`|30|重写|接收作者event10历史论说，放到真实明和平确认事件；改绝对多数、彻底结束割据/万世难改等超出机制断言。 来源：events/nesnd_south_accords.txt:226|
|`nesnd_south_accords.20.a`|31|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:235|
|`nesnd_south_accords.21.t`|32|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:266|
|`nesnd_south_accords.21.d`|33|重写|吴二元君主制；精确只断言中国范围整合同意+日本条件，不能称所有海外同意。 来源：events/nesnd_south_accords.txt:267|
|`nesnd_south_accords.21.a`|34|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:276|
|`nesnd_south_accords.reconsider`|35|重写|删除“重新计算履约期”开发腔；必须另保留重置12月的操作后果。 来源：events/nesnd_south_accords.txt:247；events/nesnd_south_accords.txt:288|
|`nesnd_south_ming_peace_result_tt`|36|重写|删除“真实”实现口吻，明确仍是游戏成员政府不变。 来源：events/nesnd_south_accords.txt:243|
|`nesnd_south_wu_peace_result_tt`|37|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_south_accords.txt:284|
|`nesnd_south_accords.22.t`|38|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:307|
|`nesnd_south_accords.22.d`|39|重写|真实颁诏者动态标题姓名；一院制、不写中央宗盟。保留作者宏观政治过程。 来源：events/nesnd_south_accords.txt:308|
|`nesnd_south_accords.23.t`|40|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:322|
|`nesnd_south_accords.23.d`|41|重写|实际新吴君主的标题/姓名；不把所有海外吞并；二元君主立宪政治结果。 来源：events/nesnd_south_accords.txt:323|
|`nesnd_south_accords.done`|42|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_south_accords.txt:313；events/nesnd_south_accords.txt:328|
|`nesnd_south_negotiation_cost`|43|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_effects/nesnd_south_accords.txt:12；common/static_modifiers/nesnd_south_accords.txt:1|
|`nesnd_south_accord_respected`|44|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_effects/nesnd_south_peace.txt:181；common/static_modifiers/nesnd_south_accords.txt:2|
|`nesnd_south_prepared_member`|45|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_south_peace.txt:190；common/static_modifiers/nesnd_south_accords.txt:3|
|`nesnd_south_prepared_mobilization`|46|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_south_peace.txt:151；common/static_modifiers/nesnd_south_accords.txt:4|
|`nesnd_south_hasty_mobilization`|47|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_south_peace.txt:160；common/static_modifiers/nesnd_south_accords.txt:5|
|`nesnd_south_peace_administration`|48|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_effects/nesnd_south_peace.txt:422；common/scripted_effects/nesnd_south_peace.txt:473|
|`nesnd_south_new_province`|49|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_effects/nesnd_south_peace.txt:245；common/scripted_effects/nesnd_south_peace.txt:315|
|`nesnd_south_ready_unknown`|50|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_south_politics.txt:4|
|`nesnd_south_ready_known`|51|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_south_politics.txt:3|
|`nesnd_south_failed_alignment`|54|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_effects/nesnd_south_peace.txt:206；common/static_modifiers/nesnd_south_accords.txt:9|
### localization/simp_chinese/replace/zzzzzzzzz_nesnd_south_feedback_l_simp_chinese.yml

共5键；主MOD SHA256 `8488f82c6e2b5a2c7dc8fe697ab77de329eaad46de20b6596c0bf915db2d6ae3`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_chen_case_concluded_tt`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/ce_usm_the_last_days_of_ming.txt:51；common/scripted_buttons/nesnd_crisis_buttons.txt:86|
|`nesnd_supply_status_jobs_hna`|3|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_supply_journals.txt:72；common/journal_entries/nesnd_supply_journals.txt:221|
|`nesnd_supply_status_jobs_sih`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:81；common/journal_entries/nesnd_supply_journals.txt:230|
|`nesnd_supply_status_jobs_gng`|5|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:90；common/journal_entries/nesnd_supply_journals.txt:239|
|`nesnd_supply_status_jobs_hus`|6|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_supply_journals.txt:99；common/journal_entries/nesnd_supply_journals.txt:248|
### localization/simp_chinese/replace/zzzzzzzzz_nesnd_south_peace_gates_l_simp_chinese.yml

共4键；主MOD SHA256 `8ea075c977277b9d1ca8e2029582354fc7a979ed47f2d15986851a8032c54536`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_south_politics_summary`|5|重写|覆盖最终peace_gates层中旧英文大段说明；CN/EN同结构同数值；不能用国际盟约称中央国制。 来源：common/journal_entries/nesnd_succession_board.txt:41；gui/journal_entry_widgets/nesnd_south_politics.gui:2|
|`nesnd_south_peace_stability_tt`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_triggers/nesnd_south_politics.txt:347；common/scripted_triggers/nesnd_south_politics.txt:389|
|`nesnd_south_ming_supply_tt`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_triggers/nesnd_court_followup.txt:21；common/scripted_triggers/nesnd_south_politics.txt:351|
|`nesnd_south_peace_b1_note`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
### localization/simp_chinese/replace/zzzzzzzzzz_nesnd_court_followup_l_simp_chinese.yml

共28键；主MOD SHA256 `f0a65e0ab6aff4c89bbaee56f78263ed8c7ffa29624d2c955d0d0baea4f843fc`。

|键|行|判定|依据／机制来源|
|---|---:|---|---|
|`nesnd_south_pressure_detail_tt`|27|重写|同一修正改名，保留机制数字和本有英文。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`character_role_nesnd_ming_refuge`|2|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/character_roles/nesnd_ming_refuge.txt:1；common/on_actions/nesnd_court_followup.txt:18|
|`character_role_nesnd_ming_refuge_desc`|3|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_board_external_observer`|4|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/customizable_localization/nesnd_succession_board.txt:2|
|`nesnd_south_reconciliation`|5|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_south_reconciliation.txt:1；common/scripted_effects/nesnd_south_reconciliation.txt:14|
|`nesnd_south_reconciliation_reason`|6|重写|去遍海帝国网络与账册化；不把中央施政写成诸府联盟的会办。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_south_reconciliation_status`|7|重写|履行的是礼法改制安排，海外条约另外处理。 来源：自动字段／本地化引用；无直接脚本文字命中|
|`nesnd_south_reconciliation_start`|8|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_succession_board.txt:23；common/scripted_buttons/nesnd_court_followup.txt:1|
|`nesnd_south_reconciliation_start_desc`|9|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_court_followup.txt:2|
|`nesnd_south_reconciliation_stop`|10|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_south_reconciliation.txt:12；common/scripted_buttons/nesnd_court_followup.txt:8|
|`nesnd_south_reconciliation_stop_desc`|11|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_court_followup.txt:9|
|`nesnd_south_reconciliation_requirements`|12|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/scripted_buttons/nesnd_court_followup.txt:4|
|`nesnd_south_reconciliation_effect_tt`|13|重写|保留实际月度财政代价、真实门槛/退出；删原定、月度核验等实现词。 来源：common/scripted_buttons/nesnd_court_followup.txt:6|
|`nesnd_south_reconciliation_cost`|14|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/journal_entries/nesnd_south_reconciliation.txt:11；common/static_modifiers/nesnd_court_followup.txt:1|
|`nesnd_ming_royal_allowance`|15|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/on_actions/nesnd_court_followup.txt:26；common/on_actions/nesnd_court_followup.txt:28|
|`nesnd_ming_receive_court_tt`|16|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/usm_civilwar_events.txt:425|
|`nesnd_court_followup.15.t`|17|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_court_followup.txt:3|
|`nesnd_court_followup.15.d`|18|重写|不再用册籍/家谱/开支堆砌；不承诺恢复帝位。 来源：events/nesnd_court_followup.txt:3|
|`nesnd_court_followup.15.a`|19|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_court_followup.txt:6|
|`nesnd_court_followup.19.t`|20|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_court_followup.txt:13|
|`nesnd_court_followup.19.d`|21|重写|僵局结算不是新宪法/盟约通过；保留实际主权状态。 来源：events/nesnd_court_followup.txt:13|
|`nesnd_court_followup.19.a`|22|重写|统一本轮设定与名称，保持原有数值和功能。 来源：events/nesnd_court_followup.txt:16|
|`nesnd_court_followup.19.b`|23|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_court_followup.txt:22|
|`nesnd_south_inconclusive_order`|24|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/journal_entries/nesnd_succession_board.txt:24；common/scripted_buttons/nesnd_court_followup.txt:13|
|`nesnd_south_inconclusive_order_desc`|25|重写|统一本轮设定与名称，保持原有数值和功能。 来源：common/scripted_buttons/nesnd_court_followup.txt:14|
|`nesnd_south_inconclusive_result_tt`|26|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：events/nesnd_court_followup.txt:19|
|`character_role_nesnd_ming_patron`|28|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：common/character_roles/nesnd_ming_refuge.txt:7；common/scripted_effects/nesnd_ming_royal_refuge.txt:334|
|`character_role_nesnd_ming_patron_desc`|29|通过|名称、短状态、数值/动态读数或已核人物叙述与本轮设定相容。 来源：自动字段／本地化引用；无直接脚本文字命中|

新增键：`nesnd_federal_compact_button_alt_desc`、`nesnd_south_reconsider_tt`；两语言均已在提案JSON中。

判定计数：{"重写": 298, "通过": 132, "保留作者原文": 251, "日本交接": 1, "闲置旧机制": 1}。
