# 西秦朝议：原生周变化与来源研究

**推荐：保留现有每周权力重算与绝对同步，只给三个bar添加 `weekly_progress`，显示“当前各项条件应得的折算份额 − 已结算份额”。** 原生每周净变化由此真实可算，份额总和仍为100。为满足具体来源要求，采用下方分项版；两行净变化版只是更小的备选，不足以单独解释法律、利益集团和军队规模。无需monthly_progress或yearly_progress，也不要将原始权重点写成百分数。

本研究仅写报告与算术样例；未改主MOD/候选，未启动游戏。游戏1.13.11/build24799966，catalog CURRENT。代码为可审查提案，尚未经引擎执行。

## 源码链条与同步

- [原版周期顺序](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/scripted_progress_bars.md:20>)明确规定bar周期更新先于JE同周期pulse。[两种西班牙](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_ip4_victoria_progress_bars.txt:65>)已有带变量守卫的“目标−当前”原生进度；[对应JE回调](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/journal_entries/06_the_two_spains.txt:69>)在月脉冲记录进度。该原版例子会缓慢追赶目标，本提案系数为1，符合现有西秦每周直接重估而非逐渐累积的行为。
- [原生owner作用域](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_progress_bars/00_ip4_victoria_progress_bars.txt:9>)在weekly_progress内用owner进入国家；提案沿用，纯值与triggers均在该国家域求值。[GUI悬停](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/gui/journal_entry.gui:260>)调用GetPeriodicProgressBreakdown，因此应添加具名add/subtract来源，而非只扩大bar desc。
- [现有西秦JE](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/journal_entries/nesnd_qe1_court.txt:23>)每周调用compute_court；[compute完整链](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/scripted_effects/nesnd_qe1_court.txt:1>)先按现有扶持计算份额，逐个删除首轮份额<40的扶持，再重算一次并绝对set_bar_progress。无其他月/年流量。
- [原始权重](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_qe1_court.txt:1>)每方15基础，原始权重相加后归一化；[扶持修正](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/static_modifiers/nesnd_qe1_court.txt:1>)只改变IG人口吸引力，不直接加减当前IG clout。因此同一结算内模拟扶持变量撤除即可预测本次归一化。[文化项](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties/common/script_values/nesnd_qe1_identity.txt:7>)统计占人口至少1%的文化，每种文化在行政不足时给士人原始权重2、封顶20。

## 必须模拟现有撤销，不能直接用原始份额

令首轮原始权重为r、首轮份额为100r/Σr。保留扶持的条件必须是“该扶持变量存在且首轮份额≥40”，不得读取上周存储份额。对每个势力，把已有敌对扶持的−10先还原，再仅在仍有敌对扶持被保留时扣10，得到最终原始权重，再归一化。OR关系必须保留：两份异常旧扶持也只扣一次10。现有每方基础至少15、其他项非负，故原始min5下还原10是精确的，不存在低于0被裁掉后无法逆推的合法状态。

例：无扶持基数25/75/75，皇权扶持开启时首轮25/65/65，对应16.129/41.935/41.935。皇权低于40，现代码撤掉其扶持，最终回到14.286/42.857/42.857。只展示首轮份额会给出错误预报。

## 只读计算定义

分别追加到script_values与scripted_triggers；原有raw、calculate_power_values、prune_patronage与compute_court保持原样。没有新持久变量，也不要求旧档迁移。分项版不需要最后三个preview_share定义，可省掉。

```paradox
# Proposed country-scope script values. Read-only; no saved variables.
nesnd_qe1_preview_first_total = { value = nesnd_qe1_crown_raw add = nesnd_qe1_literati_raw add = nesnd_qe1_army_raw }
nesnd_qe1_preview_first_crown = { value = nesnd_qe1_crown_raw divide = nesnd_qe1_preview_first_total multiply = 100 }
nesnd_qe1_preview_first_literati = { value = nesnd_qe1_literati_raw divide = nesnd_qe1_preview_first_total multiply = 100 }
nesnd_qe1_preview_first_army = { value = nesnd_qe1_army_raw divide = nesnd_qe1_preview_first_total multiply = 100 }
nesnd_qe1_preview_raw_crown = {
    value = nesnd_qe1_crown_raw
    if = { limit = { OR = { has_variable = nesnd_qe1_patron_literati has_variable = nesnd_qe1_patron_army } } add = 10 }
    if = { limit = { OR = { nesnd_qe1_preview_keep_literati = yes nesnd_qe1_preview_keep_army = yes } } subtract = 10 }
    min = 5
}
nesnd_qe1_preview_raw_literati = {
    value = nesnd_qe1_literati_raw
    if = { limit = { OR = { has_variable = nesnd_qe1_patron_crown has_variable = nesnd_qe1_patron_army } } add = 10 }
    if = { limit = { OR = { nesnd_qe1_preview_keep_crown = yes nesnd_qe1_preview_keep_army = yes } } subtract = 10 }
    min = 5
}
nesnd_qe1_preview_raw_army = {
    value = nesnd_qe1_army_raw
    if = { limit = { OR = { has_variable = nesnd_qe1_patron_crown has_variable = nesnd_qe1_patron_literati } } add = 10 }
    if = { limit = { OR = { nesnd_qe1_preview_keep_crown = yes nesnd_qe1_preview_keep_literati = yes } } subtract = 10 }
    min = 5
}
nesnd_qe1_preview_final_total = { value = nesnd_qe1_preview_raw_crown add = nesnd_qe1_preview_raw_literati add = nesnd_qe1_preview_raw_army }
nesnd_qe1_preview_share_crown = { value = nesnd_qe1_preview_raw_crown divide = nesnd_qe1_preview_final_total multiply = 100 }
nesnd_qe1_preview_share_literati = { value = nesnd_qe1_preview_raw_literati divide = nesnd_qe1_preview_final_total multiply = 100 }
nesnd_qe1_preview_share_army = { value = nesnd_qe1_preview_raw_army divide = nesnd_qe1_preview_final_total multiply = 100 }
```

```paradox
# Retention uses the FIRST calculation, exactly as existing prune_patronage does.
nesnd_qe1_preview_keep_crown = { has_variable = nesnd_qe1_patron_crown nesnd_qe1_preview_first_crown >= 40 }
nesnd_qe1_preview_keep_literati = { has_variable = nesnd_qe1_patron_literati nesnd_qe1_preview_first_literati >= 40 }
nesnd_qe1_preview_keep_army = { has_variable = nesnd_qe1_patron_army nesnd_qe1_preview_first_army >= 40 }
```

## 推荐的分项原生明细

每行数值已经除以同一个最终总权重并乘100，是当前条件贡献的份额点；最后一项扣除当前份额，合计才是本周净变化。源项不应叫“每周获得+25皇权”：25只是归一化前权重。这种显示会在局势稳定时得到0净变化，但仍能展开看到法律和社会条件的贡献。

以下三个块分别放入对应bar，保留其name/desc/min/max/start/style。原bar数量和现有JE脉冲不变。

```paradox
# Insert only this weekly_progress into nesnd_qe1_crown_bar.
weekly_progress = {
    owner = {
        if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_crown }
            add = { desc = nesnd_qe1_share_base value = { value = 15 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_crown_laws value = { value = 0 if = { limit = { has_law_or_variant = law_type:law_monarchy } add = 25 } if = { limit = { has_law_or_variant = law_type:law_autocracy } add = 25 } if = { limit = { has_law_or_variant = law_type:law_technocracy } add = 15 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_appointments value = { value = 0 if = { limit = { has_law_or_variant = law_type:law_appointed_bureaucrats } add = 10 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_governance value = { value = 0 if = { limit = { bureaucracy >= 0 government_legitimacy >= 75 } add = 20 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            if = { limit = { OR = { nesnd_qe1_preview_keep_literati = yes nesnd_qe1_preview_keep_army = yes } }
                subtract = { desc = nesnd_qe1_share_patronage value = 10 divide = nesnd_qe1_preview_final_total multiply = 100 }
            }
            subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_crown }
        }
    }
}

# Insert only this weekly_progress into nesnd_qe1_literati_bar.
weekly_progress = {
    owner = {
        if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_literati }
            add = { desc = nesnd_qe1_share_base value = { value = 15 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_civil_clout value = { value = ig:ig_intelligentsia.ig_clout add = ig:ig_industrialists.ig_clout multiply = 100 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_representative_laws value = { value = 0 if = { limit = { has_law_or_variant = law_type:law_elected_bureaucrats } add = 20 } if = { limit = { has_law_or_variant = law_type:law_census_voting } add = 20 } if = { limit = { has_law_or_variant = law_type:law_wealth_voting } add = 15 } if = { limit = { has_law_or_variant = law_type:law_presidential_republic } add = 20 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_schools value = { value = 0 if = { limit = { institution_investment_level = { institution = institution_schools value >= 3 } } add = 20 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_admin_gap value = { value = 0 if = { limit = { bureaucracy < 0 } add = { value = nesnd_qe1_significant_cultures multiply = 2 max = 20 } } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            if = { limit = { OR = { nesnd_qe1_preview_keep_crown = yes nesnd_qe1_preview_keep_army = yes } }
                subtract = { desc = nesnd_qe1_share_patronage value = 10 divide = nesnd_qe1_preview_final_total multiply = 100 }
            }
            subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_literati }
        }
    }
}

# Insert only this weekly_progress into nesnd_qe1_army_bar.
weekly_progress = {
    owner = {
        if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_army }
            add = { desc = nesnd_qe1_share_base value = { value = 15 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_army_size value = { value = army_size divide = 4 max = 60 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_military_clout value = { value = ig:ig_armed_forces.ig_clout multiply = 60 } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_military_laws value = { value = 0 if = { limit = { has_law_or_variant = law_type:law_professional_army } add = 10 } if = { limit = { has_law_or_variant = law_type:law_militarized_police } add = 15 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_victory value = { value = 0 if = { limit = { has_variable = nesnd_qe1_military_winner } add = 15 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            add = { desc = nesnd_qe1_share_war value = { value = 0 if = { limit = { is_at_war = yes } add = 10 } } divide = nesnd_qe1_preview_final_total multiply = 100 }
            if = { limit = { OR = { nesnd_qe1_preview_keep_crown = yes nesnd_qe1_preview_keep_literati = yes } }
                subtract = { desc = nesnd_qe1_share_patronage value = 10 divide = nesnd_qe1_preview_final_total multiply = 100 }
            }
            subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_army }
        }
    }
}

```

### 极小备选：只显示净变动的两项

若时间只容许极小修复，可先接此版；仍应补下一节来源，才能充分回应用户要求。此版与上方分项版二选一，不能叠加。

```paradox
# nesnd_qe1_crown_bar
weekly_progress = { owner = {
    if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_crown }
        add = { desc = nesnd_qe1_share_target value = nesnd_qe1_preview_share_crown }
        subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_crown }
    }
} }
# nesnd_qe1_literati_bar
weekly_progress = { owner = {
    if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_literati }
        add = { desc = nesnd_qe1_share_target value = nesnd_qe1_preview_share_literati }
        subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_literati }
    }
} }
# nesnd_qe1_army_bar
weekly_progress = { owner = {
    if = { limit = { nesnd_qe1_court_live = yes has_variable = nesnd_qe1_power_army }
        add = { desc = nesnd_qe1_share_target value = nesnd_qe1_preview_share_army }
        subtract = { desc = nesnd_qe1_share_previous value = var:nesnd_qe1_power_army }
    }
} }
```

## 来源标签提案

| Key | 中文 | English |
|---|---|---|
| `nesnd_qe1_share_previous` | 扣除当前份额 | Current share to deduct |
| `nesnd_qe1_share_patronage` | 扶持其他势力 | Patronage of rival factions |
| `nesnd_qe1_share_target` | 按当前局势折算的份额 | Share warranted by current conditions |
| `nesnd_qe1_share_base` | 固有势力 | Established influence |
| `nesnd_qe1_share_crown_laws` | 君主与中央政体 | The crown and central government |
| `nesnd_qe1_share_appointments` | 任命官僚 | Appointed bureaucrats |
| `nesnd_qe1_share_governance` | 行政充足与政府威望 | Adequate administration and legitimacy |
| `nesnd_qe1_share_civil_clout` | 知识分子与实业家的政治力量 | Intelligentsia and industrialist clout |
| `nesnd_qe1_share_representative_laws` | 选举与共和制度 | Elective and republican institutions |
| `nesnd_qe1_share_schools` | 广设学校 | Extensive schooling |
| `nesnd_qe1_share_admin_gap` | 行政不足下的地方势力 | Provincial influence under administrative shortages |
| `nesnd_qe1_share_army_size` | 军队规模 | Size of the army |
| `nesnd_qe1_share_military_clout` | 军队集团的政治力量 | Armed forces clout |
| `nesnd_qe1_share_military_laws` | 职业军队与军事化警察 | Professional army and militarized police |
| `nesnd_qe1_share_victory` | 军方胜局 | Military ascendancy |
| `nesnd_qe1_share_war` | 战时地位 | Wartime standing |

原文对读：原始备份ce_french_empire_journals_l_simp_chinese.yml:19–26用“GDP排名符合预期”“合作vs对抗的利益集团”“社会福利机构总等级”等实际政治/经济来源作为标签，45行“大革命的遗产”为基础来源。此处沿用具名来源格式，省去开发说明；来源词按实际效果，不把军队集团力量与军队规模混写。提案标签编辑通过，未接入游戏。原始备份SHA256：352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844。

## 安全边界和检查

- 只有已存在nesnd_qe1_power_*时计算周期变化；旧档缺值时本轮原生增量为0，既有JE回调照常初始化并同步。纯preview不读未初始化的country变量。
- 保留绝对set_bar_progress；不要从已经增长的bar读回再加delta，也不要让新明细写回country份额。这样原生条临时更新后，现有回调仍得出原样的最终结果。
- 按钮即时调用compute_court时同步country与bar，之后预览通常归零；这是局势已重新结算的正确结果。立法、军队/IG变化后预览才出现偏移。
- 不添加月/年线性外推。周变化是目标差，持续累计会人为漂移。
- 算术模型核80个（含39.9/40/40.1边界、无扶持/单扶持/旧档多扶持）组合，每个对4组旧份额核“旧+delta=最终目标”。结果见qe1-court-progress-arithmetic.json。该检查证明计算式一致，不证明引擎scope与UI实际渲染。
- 原有min5始终不额外截断合法基数；若未来新增负原始权重来源，必须重新审阅“还原10”公式。当前提案只针对本次读取源码。
- 新脚本文件采用项目既有UTF-8格式；新中英文localization键需BOM与有效覆盖核查。无须修改用户正编辑的日本中文文件。
