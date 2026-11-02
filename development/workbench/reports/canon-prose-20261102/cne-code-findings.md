# CNE 文案核对：来源、分支与实施边界

本报告为独立编辑研究。只写本报告目录，未改主 MOD、候选或技能，未启动游戏。`catalog.py status`：Victoria 3 **1.13.11 / build 24799966**，`CURRENT`，changed_count 0。结论为源码与编辑提案，不是引擎验收。

## 可直接用于合入的文件

- `cne-proposals.json`：105 个键，每键有 zh / en / reason / source / mechanic。包括新 `nesnd_crisis.30.local` 与缺 scope 时的 `.30.d` 后备文案。危机20已把源码发现交给 USM 代理，由其统一提供提案，避免覆盖作者改稿。
- `cne-inventory-data.json`：最初读取时的 462 个键及 main/candidate/baseline 两语言原文、行号、有效覆盖链。
- `cne-inventory-review.json`：原 924 条语言记录，加新 `.30.local` 两条，共 926 条；逐条 keep/revise。160 条语言记录建议改动；危机20清单注明由 USM 代理负责。
- `cne-writing-comparison.md`：每个有效来源文件的完整逐键清单，以及全部返工项的原文／候选／原因／效果对读。

原始统计：中文 119 键与最初基准完全相同、8 键在基准上修改、335 键后加；英文分别为 115 / 12 / 335。正常范围包括所有 CNE 专用文件的键，以及危机20、30—33、改革通用按钮、状态、修正与国名。原版通用本地化覆写及作者旧篇章在清单中保留，没有为了统一口吻重写。

## 作者样本与本轮局部规则

只读原稿：`WORK/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml`，SHA256 `3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`。

|样本|本轮观察|编辑运用|
|---|---|---|
|`ce_cne_land_reform_reason`，15行|由革命起源讲到土地转移、摆脱宗族，再解释牧仲棠重启运动的政治经济动机。|保留成熟中文原文。英文有效覆盖层中的中文回退改为忠实完整翻译；不增写旧英文原本夹带的军事贵族理论段落。|
|`flavorCNE.3.d`，69行|法律、劳动力自由、城市生活与帝国正当性形成完整因果；允许长段和明确的帝国政治立场。|保留中文逐字；补齐英文有效覆盖。官署材料只能服务利益冲突，不能取代这项主题。|
|`flavorCNE.4.d`，79行；`.4.1`，81行|叙述转移利益的受益者、受损者与强制手段；选项是统治者态度，不是后果摘要。|保留原文。危机30、33、31按军官、农户、省督、六部、元老院各自的利益说明冲突。|
|`flavorCNE.5.d`，87行|军人与家庭、士绅及旧土地利益之间存在具体联系。|省督有自己的军事实力和利益，既可能迁就驻军，也可能与驻军争夺财源；不写成各省一贯服从中央。|
|`.6.1/.6.2`，97—98行；`.7.1/.7.2`，103—104行；`.8.1/.8.2`，118—119行|作者已有两种不同政治处置，原正文空白。|保留选项，重写 AI 补入的正文以对应“调离/惩处”“地方资助/政治影响”“劳工保护/不干预”的实际分支。|

本轮规则来自上述原文及作者2026-11-02明确纠正：先辨明有权行动的人与机构；地方纠纷不提前描述全国瓦解；提案不写成既成政策；不把删除 modifier 直接写成“撤回反对”。重新回读规则后，逐条修订了上述 JSON，并复审两语言及 scope。

新增匿名对话只按本轮游戏风味提案处理；未把新句冒署为作者已有引文。成熟有出处的牧仲棠、查万方引文保持原中文。

## 当前原版完整链条

### 在 country_event 中选择并显示具体 state

- GAME `events/agitators_events/agitators_election_events.txt:2970`：`agitators_election_events.20` 是 country_event，placement 为保存州。
- 同文件 `3063—3094`：`ordered_scope_state`，明确 limit，`order_by = turmoil`，`position = 0`，`check_range_bounds = no`，保存 `hate_crime_state`。
- GAME `localization/english/agitators_4_l_english.yml:960`：正文使用 `[SCOPE.sState('hate_crime_state').GetName]`。
- 同事件 `3110`、`3128`、`3150`：保存的 state 用于具体选项效果；scope 是实际对象而非字符串造名。
- MOD `common/scripted_effects/nesnd_cne_reform.txt:40—49`、`62—71`：本项目现有工坊、救济拨款已经按 owned reform region 和 `nesnd_reform_state_unemployment_rate` 选择州，保存 `nesnd_cne_funding_state`。
- MOD `events/nesnd_cne_funding.txt:1—48` 与 `common/scripted_triggers/nesnd_cne_programs.txt:35—42`：country事件检查保存州存在且仍由 root 拥有，继续通过确认事件支出和添加州修正。
- MOD `common/static_modifiers/nesnd_cne_reform.txt:1—10`：实际为建造、资格、教育获取、福利付款修正；不是自动创建学校/工厂建筑。

适用差异：危机30只借用“选择州→保存scope→本地化显示”的结构，不借用仇恨犯罪效果、文化、DLC、随机政治事实或新媒体资源。国与州之间的 scope 保持现有 country_event 根。

### 当朝统治者姓名／称谓

- GAME `common/on_actions/00_code_on_actions.txt:6120` 调用 `ig_revolutions.8`。
- GAME `events/ig_revolutions.txt:789—826`：country_event，placement ROOT，事件正文及风味绑定相应键。
- GAME `localization/english/events_l_english.yml:858`：`[ROOT.GetCountry.GetRuler.GetFullNameWithTitle]` 已为原版正式实例。
- GAME `localization/english/events_l_english.yml:324`、`469`、`830` 另有 `GetRuler.GetPrimaryRoleTitle` 正式实例。
- GAME `gui/character_panel.gui:626` 亦显示 Character `GetFullNameWithTitleNoFormatting`，确认标题与姓名是角色呈现接口，不是用国名冒充行动者。
- 危机31、32在本项目均为 country_event（`events/nesnd_crisis_events.txt:66—123`）。建议正文中兵部奉现任统治者之命、元老院呈请现任统治者颁诏；历史回忆的牧仲棠照旧保留。

适用差异：不要把这一根链不加转换地搬进 state_event。此次 CNE 更新的 flavor6—8 及 funding1—2也均为 country_event，地点依已经保存的 state scope 读取，不由 state 根冒读国家。

## 唯一必需的新增脚本闭包：危机30地点

Root 已确认实施方案：危机30 immediate 从本国改革区域挑选失业率最高的州，保存 `nesnd_land_petition_state`；desc 的 first_valid 先检查该 state scope 存在，用新 `.30.local`，其余走不含动态地点的 `.30.d`。保留数值、选项、触发时间和全部结算。

建议形状，遵循现有 `nesnd_reform_invest`：

```text
desc = {
    first_valid = {
        triggered_desc = {
            trigger = { exists = scope:nesnd_land_petition_state }
            desc = nesnd_crisis.30.local
        }
        desc = nesnd_crisis.30.d
    }
}
immediate = {
    set_variable = nesnd_reform_petition_event_seen
    clear_saved_scope = nesnd_land_petition_state
    ordered_scope_state = {
        limit = { nesnd_reform_region = yes }
        order_by = nesnd_reform_state_unemployment_rate
        position = 0
        check_range_bounds = no
        save_scope_as = nesnd_land_petition_state
    }
}
```

`ordered_scope_state` 已由 country 的 owned-state 集合限定；若需要防止无候选时发出无意义事件，可在 trigger 加 `any_scope_state = { nesnd_reform_region = yes }`，但这是额外触发限制，root 选择保留后备描述即可避免引入数值/流程差异。不能只插入动态本地化而不保存 scope。旧排队事件没有新 scope 的情况下，不能硬填山西或任意州。

## 作者附件与当前效果逐项矛盾

|条目|现行代码与附件差异|本轮最小处理|
|---|---|---|
|危机30 `.d`|现行 event 没有州scope；月度只检查 disorder≥55，一次前期事件。作者要求局限于某些地方。|新增受保护地点分支。正文仅当地几处庄园和涉事各县，不写全国驻军抗命。|
|危机30 `.b`|`nesnd_land_choice_30_b` 降8失序，加60个月 compromise（征税/权威各-5%）；咨议局没有行政或司法接管权。|改为省督酌从地方之请达成妥协，咨议局只在正文陈情；与A的中央复核区别。|
|危机30 `.c`|实际 +12失序、+2% radicals、repressed标记；旧文仅要求军队依法交册，未交代压制。|保留交册，但明示抗命聚众者依法惩办。|
|危机33 `.d`|`zzzz_nesnd_cne_reform` 覆盖了作者改过的 `zz_nesnd_crisis`。实际地方条件为晋北/山西非首都、至少6个月困境、失业>10%、turmoil>25%，全国至少9次月度统计且失序≥65。|同时改有效覆盖。保留作者拘捕、军营拒交涉案者、撤官赔补争议；补上民生困顿与准备起兵，不能预先宣布已建共和国。|
|危机33 A/B|A只是进度-10、失序-15和36个月清丈支出（政府工资+10%、行政-5%）；B才尝试NSX分离，可能创建吞并play。|文案将A当政策妥协与重审，不声称脚本已转移钱款或删除角色；B为镇压决定与起兵危险。保留既有数值。|
|危机31|只有 extreme crisis 才进入：samples≥15、12坏月份、失序≥90、全国动乱>40%、合法性<25、战争/破产。|保留全国财政军事瓦解，并说明省督与驻军的兵财关系。兵部奉当朝统治者发调防令，国家不亲自颁命。|
|危机31 A/B|A结束改革并有60个月军政重组；B只能在仍满足极端危机时分离符合条件的NSX/NHB/NSD，再终止改革、+10% radicals。|不写所有省必然独立；“可能拥立自己的政府”保留条件性。|
|危机32|可由暂停按钮在改革活动时开启。附件把军户、减租、自由务工、国家公田写成已经施行；B其实允许继续改革。A调用 `nesnd_land_freeze` 永久设置done，清理子日志，10年 compromise，然后 `flavorCNE.2`。|保留作者军户与国家公田政治内容，改为元老院提出的妥协草案；选项与提示明示改革就此结束。没有增加租金法律、土地所有权或迁徙effect。|
|危机20|附件说国内改革仍在推进，但 trigger 只要CNE/USM存在和未看过事件；可能在改革已结束时出现。|已交 USM 代理：保留作者强烈北朝立场，改革争夺经费须为条件句。根代理明确“襄樊诸府”仍与最新省制纠正冲突，使用“联络襄樊大营，准备南下。”；不盲从附件旧制度词。|
|NSX/NHB/NSD|候选仍为汾晋共和邦/河北军政府/山东行营；作者附件为大晋共和邦/靖安军/国人共和国，主MOD英文文件还把新中文放在英文槽。|遵循附件的新专名，两语言均同步；tag和政体不变。|
|22州暂停按钮|中文“撤回当地收益与相应军队反对”是实现视角。|正文写停止地方清理、暂循旧例；共用效果提示仍精确说明修正移除。|
|confidence5.war|trigger覆盖革命和分离内战，正文只说革命内战。|改“内战”；不更改失败触发或分类顺序。|
|confidence aftermath|条件只有曾起义、不在交战；英文直接宣布叛军已败。|与中文一致：战事震荡未平，不预断结果。|
|confidence3|南方声索只针对仍在己方/属国外的地区；原文本新增“议会”未证实。|写新政府重申对应地区声索，不给新共和国杜撰议院架构。|

## 公开显示与遗留键

除已交 USM 代理统一处理的危机20外，当前活动调用所用的英文中文回退均已给出翻译建议。其余仍存在中文的六个英文键均无活动调用：`ce_cne_land_draft_failing`、其reason、`nesnd_land_survey_requirements`、`nesnd_land_review_requirements`、`nesnd_land_military_requirements`、`nesnd_land_status_petition`。旧腐化日志在 `ce_cne_land_draft.txt` 中 inactive/possible=no、invalid=yes；旧条件文本已被原生条件展示取代。这里保留记录，不因看见中文就批量改失效稿。

所有动态scope、`$STATE_*`、进度条引用均逐条保留；`.30.local` 是唯一新增动态state引用。现行 `GetFullNameWithTitle` 增加在两个 country_event 中，已有原版实例；尚未执行引擎显示检查。

除地点保存和desc保护分支外，编辑提案不要求修改任何数字、modifier、国家法令、领土、人物、起义、战争结算或时间。危机32“停办即终止”的问题通过诚实表达既有行为修正，不建立未经授权的新恢复功能。
