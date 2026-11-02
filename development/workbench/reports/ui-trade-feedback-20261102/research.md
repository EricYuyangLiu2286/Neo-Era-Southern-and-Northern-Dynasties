# UI 与通商反馈源码研究

日期：2026-11-02。范围：只读检查主 MOD 与当前 GAME；未开游戏，未改 MOD，未改技能。此报告记录父代理开始修改前读取到的代码；主 MOD 若随后由父代理修订，下面行号属于该次观察。结论是 SOURCE_VERIFIED / ENGINE_NOT_RUN，不认证截图所用运行候选。

## 来源与版本

- MOD = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties`。
- GAME = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`。
- DOCS = `D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031`。
- 本轮 `python C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts/catalog.py status` 返回 `version=1.13.11, build=24799966, status=CURRENT, changed_count=0`。已读 NESND 技能、工程适配、当前执行图和 research 技能。依据工程适配，成果放 WORK，不放 MOD。
- 后文 `MOD/...:行号`、`GAME/...:行号`、`DOCS/...:行号` 都以上述绝对根目录展开。没有采用百科或其他游戏 API。

## 1. CNE 全国建筑等级：已有原生国家接口

**推荐将七个门槛直接写成 `country_has_building_type_levels` 国家 trigger。** 不再让自定义求和的两个循环进入门槛展示。原生接口计算全国某类型建筑等级之和，并非要求每一州都达到门槛。

```text
country_has_building_type_levels = {
    target = bt:building_iron_mine
    value >= 25
}
```

完整来源链：

| 层 | 一手来源 | 已证事实 |
| --- | --- | --- |
| 引擎 API | DOCS/triggers.log:9384–9391 | `country_has_building_type_levels` 描述为某国某建筑类型等级总和，supported scope 为 country，参数为 target/value。相比之下 14421–14428 的 `state_has_building_type_levels` 才是州级。 |
| 当前原版完成条件 | GAME/common/journal_entries/00_negotiation_quests_je.txt:414–423 | 原版谈判建筑任务直接调用国家 trigger，target 来自所许诺建筑类型，value 与目标比较。 |
| 当前原版数值读法 | GAME/common/script_values/negotiation_values.txt:629–631 | 活跃实现 `add = "owner.country_has_building_type_levels(scope:ig_for_calc.var:promised_building_type)"`，IG owner 提供国家 scope。 |
| 数值调用者 | GAME/common/journal_entries/00_negotiation_quests_je.txt:383–401 | 起始及每月 current_building_amount 调用上述脚本值，证明它用作数值而非仅布尔 trigger。 |
| 原生 UI 文本 | GAME/localization/simp_chinese/triggers_l_simp_chinese.yml:1628–1633；英文同文件:2046–2051 | 生成“某国的某建筑等级至少 N”一行。可以保留原生门槛提示，不需列出所有州。 |
| 当前 MOD 调用者 | MOD/common/scripted_triggers/nesnd_cne_programs.txt:33–39 | 七个自定义合计脚本值只用于这七项国家城市化门槛。 |
| 当前 MOD 求和 | MOD/common/script_values/nesnd_cne_programs.txt:11–17 | `every_scope_state` 内套 `every_scope_building`，筛类型累加 level。没有限定本土22州；替换也应保留全国语义。 |

对应门槛为铁矿25、煤矿40、炼钢厂10、工具厂30、发动机厂6、伐木场60、造船厂12。建筑类型定义：GAME/common/buildings/03_mines.txt:1、38；01_industry.txt:100、251、286、318；09_misc_resource.txt:1。

如其他 UI 确实需要数值，可以用 `value = "country_has_building_type_levels(bt:building_iron_mine)"`；活跃原版证明的是带动态建筑类型参数形式。GAME/common/script_values/je_values.txt:74 的固定 `bt:` 例子仅为注释，不应把它单独当成运行实证。最稳妥、最接近当前原版的改法仍是直接使用上面的 country trigger，并删除失去调用的七个循环求和值。

适用差异：原版任务位于国家 JE，目标变量存在于 IG；本项目目标是七个固定建筑类型，直接传 `bt:`。没有改州归属、行业目标或计算范围。源码证据足以支持接口选择；实际 tooltip 排版和引擎执行未在本轮运行验证。

## 2. USM 两个“遣使议约”来自两个 JE 挂载

它们不是两个独立外交制度，也不是两个不同国家有意共用按钮；是旧危机 JE 和共享局势 JE 同时挂了两个调用相同 effect 的按钮。

| JE 挂载 | 按钮定义 | 可见 / AI | 行为 |
| --- | --- | --- | --- |
| MOD/common/journal_entries/ce_usm_the_last_days_of_ming.txt:1、203，`ce_usm_conflicts_within` | MOD/common/scripted_buttons/nesnd_crisis_buttons.txt:50–56，`nesnd_federal_compact_button` | always=yes；AI=0 | 与下行同一 `nesnd_south_can_offer_accord` 和 `nesnd_south_offer_chosen_accord` |
| MOD/common/journal_entries/nesnd_succession_board.txt:1、26，`nesnd_south_succession_board` | MOD/common/scripted_buttons/nesnd_south_accords.txt:1–22，`nesnd_south_offer_accord` | 只对 USM 可见；AI=20 | effect 在 hidden_effect 内调用同一邀请效果 |

两者 name/desc 都取 `nesnd_south_offer_accord` / `_desc`，对应 MOD/localization/simp_chinese/replace/zzzzzzzz_nesnd_south_politics_l_simp_chinese.yml:9–12 的“遣使议约”。所以玩家确实会看到两个同名入口。

**最小收口：只删旧 JE 第203行的 `scripted_button = nesnd_federal_compact_button` 挂载，保留共享局势 JE 的入口。** 不必删除 effect、trigger 或调整已定外交数值。孤立的旧按钮定义可另作无行为清理，但不是去重所必需。

保留链条与边界：

- 邀请资格：MOD/common/scripted_triggers/nesnd_south_politics.txt:190–210，USM、和平、未违约、未结算/开战、无6月冷却、拥明或拥吴、有可接收成员。
- 邀请行为：MOD/common/scripted_effects/nesnd_south_accords.txt:8–18，存 sender，6月冷却与议约成本；遍历可接收国家，4月 pending，3日后 `nesnd_south_accords.1`。这条链与删旧挂载无关。
- 月度 AI 仍在 MOD/common/on_actions/nesnd_south_politics.txt:1–14、138–143 直接调用相同 effect。保留共享按钮的 AI=20 不会引入新的行动类型，二者仍被同一冷却守卫。
- 成员仍保留共享 JE 的 `nesnd_south_leave_accord` 与站队按钮（nesnd_succession_board.txt:27–31）；接收资格在 triggers/nesnd_south_politics.txt:162–188，回复有效性在212起。不可为隐藏重复入口而隐藏整个共享 JE。
- 接受盟约仍在 scripted_effects/nesnd_south_accords.txt:20–67：成员获得36月盟约、6月立场冷却、按路线设置整合/日本让步标识、直接关系+15。该+15属于南朝盟约关系，不能混成“商人先行”的影响力。

## 3. “商人先行”：当前源码没有接受后影响力 +15

**已证：接受事件直接关系 +10；派使者消耗的是六个月的外交影响力容量 -15；完成整项商路任务才一次获得容量 +25、持续24个月。** 不能将三者合并描述为“商人先行给关系10、影响力15”。本代理未收到原始截图文件，也未核运行候选，截图若明确是 +15，则与当前主 MOD 源码存在待解释差异。

### HUS → CNE 的精确调用链

1. HUS 专用 JE `nesnd_supply_hus_preparations`，MOD/common/journal_entries/nesnd_supply_journals.txt:158、174–179，挂载 `nesnd_supply_invite_cne`。
2. 按钮定义 MOD/common/scripted_buttons/nesnd_supply_buttons.txt:329–406：只对 HUS 可见；CNE 存活、和平、可用 `influence >= 15`（351）、没有 pending/partner/cooldown。AI权重1（372–374）。
3. 点击后 HUS 设置30日 pending（381–385）、6月冷却（386–389）、6月 `nesnd_supply_envoys`（390–393），保存 requester；7日后在 CNE 触发 `nesnd_supply.1`（394–401）。
4. 该修正仅有 `country_influence_add = -15`，MOD/common/static_modifiers/nesnd_supply_modifiers.txt:1。中文名“驻外通商使团”，localization/simp_chinese/nesnd_supply_l_simp_chinese.yml:29。负15是派使发起者的容量扣减，不是收信者的奖励，更不是一次消耗库存15。
5. 事件 MOD/events/nesnd_supply_events.txt:2–108，标题定位在6及中文本地化:34；requester/pending/主权有效性守卫来自 scripted_triggers/nesnd_supply_triggers.txt:95–153。
6. 接受 .1.a 存 receiver，然后在 requester（HUS）scope 设置 partner=CNE、清 pending、自筹标记、刷新双方 sponsor（events:55–79），**80–83 为 `change_relations = { country = root value = 10 }`**。此事件接受分支没有 add_modifier，没有 influence/leverage effect。它也不直接建立市场合并、实际贸易路线或条约。
7. 拒绝 .1.b 仅清与该请求匹配的 pending/pending_sponsor（events:92–107）。它不撤回6月派使费用。
8. 后续互惠条约是独立按钮 `nesnd_supply_trade`（buttons:501–570），30日 pending、6月冷却、7日延迟；事件 `.2` 建立两个方向的 `trade_privilege` 条款、约束2年（events:110–248）。这与 `.1` 初步联系分开。
9. 商路各项条件连稳12周后完成（buttons:597–636；triggers:83–94；scripted_effects/nesnd_supply_effects.txt 的 `nesnd_supply_week`），HUS JE on_complete 触发 `.3`（journals:277–285）。`.3` 的 `NOT nesnd_supply_rewarded` 一次性守卫设 rewarded，并加 `nesnd_supply_verified months=24`（events:249–261）。定义为 `country_influence_add=25`（static_modifiers:2）。

重复性：初步联系没有永久“已获+10”标记。玩家可用结束联系按钮（buttons:495–500）清partner，6月邀请冷却过后再次邀约，因此关系+10可以反复获得。当前代码支持重复联系；不可把关系奖励当全局一次性。完成奖励受 `nesnd_supply_rewarded` 守卫，且 done 阻止常规重复进入 JE。自筹/结束/清理均不会提前 remove_modifier `nesnd_supply_envoys`；现有中文也明确费用支付至期满（localization:28）。

### 单位与配置上限

| 量 | 当前配置 / 单位 | 一手证据 |
| --- | --- | --- |
| 双边 relations | -100 到 +100；总跨度200不是正上限200。分档阈值 -80/-50/-20/20/50/80。 | GAME/common/defines/00_defines.txt:979–987；GAME/localization/english/concepts_l_english.yml:1137直接显示该defines范围 |
| `change_relations` | 直接改变关系值，本事件输入10。 | DOCS/effects.log:661–667；原版同形 events/alaska_events.txt:98–101直接+10；英文effects_l_english.yml:80–85及中文:68–73显示“关系提高VALUE” |
| relations progress | 普通积累达到100提高1，-100降低1；与直接改变关系的 effect 分开。 | GAME/common/defines/00_defines.txt:988–989；DOCS/effects.log:51–57；英文effects_l_english.yml:33明确progress |
| 外交影响力 influence | 连续产生/占用的 capacity，不储存成点数；可用余额和消耗量分别有trigger。未找到原版或本MOD“1000硬上限”配置。 | GAME/localization/english/concepts_l_english.yml:604、614；DOCS/triggers.log:11110–11120；GAME/common/modifier_type_definitions/00_modifier_types.txt:165–187 |
| 原始 leverage | `MAX_LEVERAGE=1000`，注释为本国与各集团瓜分的raw leverage；这不是influence容量上限。每周趋向目标的factor0.02、至少1。 | GAME/common/defines/00_defines.txt:1374–1379 |

中文 `ADD_CHANGE_RELATIONS_PROGRESS`（GAME/localization/simp_chinese/effects_l_simp_chinese.yml:30）简写为“关系将会改变VALUE”，易与直接关系混淆；英文明确说 progress。这一翻译本身不能证明内部effect输入缩放。不过本事件确定使用直接 `change_relations`，因此无需依靠progress换算判定其+10。任何“add_change_relations_progress一次effect是否内部另有缩放”的争议，本轮没有实机测量，不从周期定义过度推断。

### 原生规模基线与 MOD 覆盖

- GAME/common/static_modifiers/00_code_static_modifiers.txt:7–18，base_values 的影响力容量为100。
- GAME/common/country_ranks/00_country_ranks.txt:42/80/111/138/172/207/239：列强1000、主要750、次要600、弱小500；未认可主要/地区/弱小为750/600/500。加base后的初步基线为1100/850/700/600，之后仍有修正和开支。这已足以反证“影响力最大1000”。不要把某时刻 HUS/CNE 的可用余额等同该静态基线。
- GAME/common/static_modifiers/00_code_static_modifiers.txt:700–704 原版 rivalry 容量额外200，另受 defines:971–977 的重合利益与游说团因素缩放。
- 原版改善关系 pact 基础开支150，3 progress/日，到关系50为止（GAME/common/diplomatic_actions/00_relations_actions.txt:23–32）；目标等级等会影响实际开支，country_ranks.txt:9–10、23–24、61–62等。这里只用150作未修正量级比较。
- 原版贸易特权基础开支50、0.5 relations progress/日、改善到20；由target承担，source获得 treaty leverage generation +300（GAME/common/treaty_articles/25_trade_privilege.txt:1–30）。这是独立条款机制；+300生成修正并不等于立刻拿到300/1000份额。双向条款各自按规则承担对应成本。
- 全MOD `common/defines` 只有 ce_graphics.txt 的NFrontend镜头设置；没有 NDiplomacy/relations/leverage 数值覆盖。MOD没有country_ranks覆盖，也没有base_values覆盖。本轮搜索 `country_influence` 的自定义写入只有供给-15/+25、波兰相关修正（static_modifiers/ce_poland_modifiers.txt:56/61/85/95/115）与日本锁国-50%（laws/ce_trade_policy.txt:25–34）。这些不是全局上限。

### 规模建议（未实施）

1. **关系+10可保留。** 它是直接关系值，等于中立0到亲善20所需的一半；作为量级参照，原版基础改善关系3 progress/日约333日积累才有10关系。不要改成progress+10，否则语义截然不同，也不要以“关系上限200”为由翻倍。它还可每6月结束后重邀，增幅过大会变成很快刷满关系的入口。
2. **先确认截图+15的对象，再改数值。** 当前真正15是发起者的-15/6月成本，约静态600–1100容量的1.4%–2.5%，约原版改善关系基础150的十分之一。该轻成本更像使团联络手续费；初步联系本身的主要功能是满足商路外交条件及解锁正式条约。
3. **若目标是让“完成商路”的奖励更有存在感，优先调整一次性+25/24月奖励。** 当前仅约基线2.3%–4.2%；建议候选为+75/24月（约6.8%–12.5%，相当于1.5份未修正贸易条款开支），需要更强奖励才取+100（9.1%–16.7%）。这应作为明确设计决策，不把+75/+100伪装成修复了“+15”。保留一次性守卫、两年持续时间及现有邀请成本，可降低通过重复接洽刷容量的动机。
4. 当前 `.1` 只给发起者记录伙伴。若用户期待 CNE 作为收信者获得独立贸易收益，属于新的行为设计，应先决定收益对象、双向/单向、持续时间和重复保护，再写入。不能仅改本地化使之声称不存在的收益。

## 本轮可直接供实现引用的结论

- CNE全国等级有原生country trigger，现有七项门槛可用它直接替代循环脚本值。
- USM重复入口可只删旧危机JE挂载；保留共享局势面板、AI月度邀请、盟友回复/站队/退出链。
- 商人先行接受确定直接关系+10。当前主MOD不存在接受奖励影响力+15；真正的15是HUS派使的6月容量负修正，完成奖励另为+25/24月。
- 关系范围-100..100；1000属于raw leverage；影响力容量至少有基础100+等级1000等来源，非1000硬帽。
- 没有启动游戏，因此截图候选一致性、原生提示最终排版、实际存档数值与运行时修正均未认证。

## 补充：按最新要求优先原生逐项勾选

父代理转达最新明确要求：尽量少用 custom_tooltip，采用原生 trigger 的逐项 checkbox；只将内部生命周期守卫隐藏，玩家实际资格逐项公开。以下是一手实例，不需要用自定义一句话遮住整个条件树。

### 同按钮语境的全国固定类型实例（强于此前动态参数实例）

GAME/common/scripted_buttons/07_japan_buttons.txt:1–33，`button_je_tenpo_combat_rice_hoarding`：

```text
possible = {
    OR = {
        AND = {
            country_has_building_type_levels = {
                target = bt:building_rice_farm
                value >= 40
            }
            NOT = {
                any_scope_state = {
                    state_region = { is_homeland = cu:japanese }
                    has_famine = yes
                }
            }
        }
        market_capital.market = {
            mg:grain = { market_goods_pricier < 0.1 }
        }
    }
}
```

这里 `target = bt:...` 是活跃原版 scripted_button possible，直接支持七项国家建筑门槛，毋须援引 je_values 中已注释的函数形式。

### 隐藏内部守卫，公开玩家条件

GAME/common/scripted_buttons/00_balkan_wars_buttons.txt:143–169，停止研究按钮，possible 中先给可见 `has_modifier`，再以 `hidden_trigger` 隐藏成员/退出/JE存在等内部条件：

```text
possible = {
    has_modifier = balkan_wars_military_tech_boost_mod
    hidden_trigger = {
        has_variable = balkan_league_acceptor
        NOT = { has_variable = resign_button_pressed }
        has_journal_entry = je_the_balkan_league
    }
    # 原版最后还以custom_tooltip解释冷却；本项目可按最新要求避免宽泛包装。
}
```

DOCS/triggers.log:11002–11005 明言 enclosed triggers 不显示在 tooltip。另一原版按钮 GAME/common/scripted_buttons/05_hungary_buttons.txt:14–49 把额外 AI 条件放在 OR 的 hidden_trigger 分支，支持将自动控制所需的额外条件从玩家可见门槛中分离。

适用边界：内部“JE仍活跃、未重复启动、引用存在”等可以隐藏，但 effect 仍须再次守卫；真实资格如建筑、法律、资源不可仅在 hidden_trigger 里留下一个不解释的禁用按钮。移除玩家的政力/破产/动荡65启动限制属于父代理依据用户授权作出的行为变化，本研究只给原生展示与 AI 分支的来源，不把它说成纯UI修复。

### 城市分布与全国工业等级应分两层

建议原生条件形状：

```text
any_scope_state = {
    count >= 5
    state_has_building_type_levels = {
        target = bt:building_urban_center
        value >= 5
    }
}
country_has_building_type_levels = { target = bt:building_iron_mine value >= 25 }
country_has_building_type_levels = { target = bt:building_coal_mine value >= 40 }
country_has_building_type_levels = { target = bt:building_steel_mill value >= 10 }
country_has_building_type_levels = { target = bt:building_tooling_workshop value >= 30 }
country_has_building_type_levels = { target = bt:building_motor_industry value >= 6 }
country_has_building_type_levels = { target = bt:building_logging_camp value >= 60 }
country_has_building_type_levels = { target = bt:building_shipyard value >= 12 }
```

- 全国至少5个州各有5级城市中心，保留当前分布要求；七项工业门槛为全国合计。
- 原版 `any_scope_state count>=2` 见 GAME/common/journal_entries/02_coffee_and_milk.txt:16–27；该例紧接着另做全国建筑组等级门槛，正好体现分布与合计分开。
- 州数量内部带 `state_has_building_type_levels` 的原版实例见 GAME/common/journal_entries/07_korea_colonization.txt:120–135（count>=3；铁路value>=10作为其中一项）；引擎州接口见 DOCS/triggers.log:14421–14428。

## 补充：派使100、完成100、直接关系25候选的回路检查

父代理提出的新候选值为派使容量-100/6月、完成容量+100/24月、直接关系+25。该候选取代前文“优先保留关系10”的研究建议时，应记录为明确数值设计变化，而不是引擎单位修复。

- **数值单位成立**：关系25是直接 `change_relations` 点数；不会被progress100:1换成0.25。原版关系上限100，三次+25为75，四次为100。
- **需要联动六处门槛**：`nesnd_supply_buttons.txt:25/107/189/271/351/431` 的 `influence>=15` 要随费用改为100；static_modifiers:1改-100；邀请说明的15要同步。仅改修正而保留15门槛会允许可用容量不足100者点击。
- **费用无即时退款路径**：六个按钮共用 `nesnd_supply_cooldown`，冷却与费用修正都6个月。拒绝、请求超时、self、end_contact、JE cleanup都没有remove_modifier envoys；`scripted_effects/nesnd_supply_effects.txt:32–39、181–193`清变量也不清费用。旧中文说明已明确“支付至期满”。因此不能通过结束联系/自筹/暂缓马上拿回占用再免费点击。
- **正常界面不能重叠连点**：共用6月冷却+pending/partner守卫；结束联系可清partner但不清冷却。费用按时结束；持续拒绝后重试仍每6月一笔。直接强制调用effect没有possible重检不是正常UI重复路径，本研究不以控制台强调用推定玩家漏洞。
- **关系仍可反复刷**：没有每伙伴首联奖励标记。结束联系后每6月重新邀请，同一伙伴4次直接+25可从0到100，约首邀后18个月再加响应延迟。收费100/6月会让该循环有实际机会成本，但若目标是不允许重复关系奖励，需另设关系奖励守卫；它不是现有代码已保障的事项。
- **完成奖励仍一次**：`.3`只在 `NOT nesnd_supply_rewarded` 时奖励，24月到期不会删除rewarded，正常JE也受done阻止。因此+100不会形成每次重新开JE叠加奖励的常规入口。
- **容量生成与消耗的区别**：现有 `country_influence_add=-100` 是生成侧的负加值。GAME/localization/english/modifiers_l_english.yml:296–301 分别描述 `country_influence_add`、`country_influence_cost_add`（flat cost to usage）、`country_influence_mult`。存在生成百分比修正时，不应承诺UI可用余额恰少100。若需严格“额外占用100”，cost_add语义更直接，但GAME活跃脚本仅发现其modifier_type定义，未发现实际使用实例；本批保持现有modifier种类较符合不夹带未验证语义变化的原则。
- 对600–1100的初步容量基线，100约9.1%–16.7%，比旧15明显；但实际HUS/CNE余额还受power bloc500开支、等级、宿敌、法律和其他行动影响，不能用这一区间代替实机余额。完成+100为持续收益，不是一次入账100的库存。
