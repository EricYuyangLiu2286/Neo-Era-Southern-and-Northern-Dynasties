# 人物设计：君主与宫廷

> 何时读：设计继位、宠臣、觊觎者、复国或起义建国中的具体人物。先读 [character-design.md](character-design.md) 的共用骨架。不必读：总统、IG 领袖、将军、经理、专家等职位人物（见 [character-office.md](character-office.md)）。

## 一、王朝继承和外交关系

**用于** 继位会改变另一国家的条约、王朝或继承资格。维多利亚是共主邦联分裂的入口，明治另显示有名天皇与实际统治者可以并存。

```text
开局创建前君与继承人 → 双方国家日志 → 前君离位
    → 新君作用域 → 修改双方条约 → 次国确认
    → 邦联已解除／继承人缺失 → 失效
```

```pdx
# 放在 common/history/characters 的 c:COUNTRY 块；ruler/heir 可写在模板里，也可在此写 heir = yes
create_character = { template = OLD_RULER }
create_character = { template = HEIR heir = yes }

# JE 成功 outcome，确需该人继位时精确检查
trigger = { ruler ?= { has_template = HEIR } }
effect = { trigger_event = { id = person_demo.2 } }

# person_demo.2 的 immediate、option、after
immediate = {
    ruler = {
        save_scope_as = successor
        set_temporary_event_immortality = { DURATION = 3 }
    }
}
option = {
    name = person_demo.2.a
    c:PARTNER ?= { remove_diplomatic_pact = { country = root type = personal_union } }
}
after = { revoke_temporary_event_immortality = { CHARACTER = scope:successor } }
```

在 JE 的 hidden invalid_outcome 中检查次国消失、条约已解除，或继承人已死且设计不接受替代者。若按职位承接，直接取新 ruler，并让本地化跟着他。把君主更换和常设制度分开，后继者可以继续国家改革。

## 七、君主身边的宠臣或近臣

**用于** 此人的权力来自某位君主的宠信，不是常设官职；换君、改政体或撤换都让他失势。原版有专门的宠臣角色 `character_role_favorite`（显赫度、忠诚各 +25），只在专制、寡头、地主投票或技术官僚法下、且不是共主邦联附庸的国家可设（`can_have_favorites`）。玩家用人物互动任免：任命冷却 180 天，立场相左的在朝集团反弹；撤换要求任满 12 个月。新君即位或法律改到不能设宠臣时，on_action 自动解职所有宠臣。见 `common/character_roles/00_auto_assigned_roles.txt:307`、`common/scripted_triggers/00_scripted_triggers.txt:16`、`common/character_interactions/02_favorite_interactions.txt:1`、:279、`common/on_actions/00_code_on_actions.txt:1584`、:3183。

```text
政体允许 → 事件引荐或玩家任命 → 在朝集团反弹
    → 宠臣事件、议程日志 → 撤换／新君即位／政体改变 → 解职
```

```pdx
# 引荐事件（国家作用域），仿原版 rasputin.1。PERSON 是宠臣模板
trigger = { can_have_favorites = yes NOT = { is_template_used = PERSON } }
immediate = {
    create_character = { template = PERSON save_scope_as = favourite }
    scope:favourite = { set_temporary_event_immortality = { DURATION = 3 } }
    set_variable = { name = favorite_event_active_var months = 3 } # 原版锁：事件期间不能任免宠臣
}
option = {
    name = person_demo.7.a
    every_scope_character = {
        limit = { has_role = character_role_favorite }
        revoke_favorite_effect = yes
    }
    scope:favourite = { add_character_role = favorite }
}
option = {
    name = person_demo.7.b
    default_option = yes
    scope:favourite = { add_modifier = { name = modifier_favorite_rebuffed days = normal_modifier_time } }
}
after = {
    remove_variable = favorite_event_active_var
    revoke_temporary_event_immortality = { CHARACTER = scope:favourite }
}

# 宠臣议程日志的 immediate：记下开场时的宠臣
random_scope_character = {
    limit = { has_role = character_role_favorite }
    save_scope_as = favourite
}
scope:journal_entry = { set_variable = { name = demo_favourite value = scope:favourite } }

# 该日志的 hidden invalid_outcome：此人死去或不再是宠臣即结束
trigger = {
    NOT = { scope:journal_entry.var:demo_favourite ?= { is_character_alive = yes has_role = character_role_favorite } }
}
```

不另查“君主是否换人”：新君即位时引擎已解除所有宠臣，上面的宠臣检查会随之成立。宠臣事件开场设 `favorite_event_active_var`、结束时移除，避免玩家在弹窗未答时换掉宠臣；每位宠臣每类事件只发一次，用人物身上的标记记录。政体不能设宠臣时，不要拿政治家角色冒充，改按第三类写成制度席位。原版依据：`events/russia_events/ip5_rasputin_events.txt:33`、:58、:81、:117、:125；`events/russia_events/ip5_favorites_events.txt:62`、:177；`common/journal_entries/08_tsarpoints.txt:3197`；`common/scripted_effects/05_tsarpoints_scripted_effects.txt:1199`。

## 八、流亡觊觎者、复国与起义建国

**用于** 复辟、复国或起义建国时由一个具名人物登位。原版法国三派觊觎者由国家日志积累复辟进度，政变事件里召回本人立为君主、流放旧君，再开“巩固王朝”日志；太平天国在起义建国时为新国家立洪秀全为天王。见 `common/journal_entries/01_french_monarchism.txt:1`、`events/french_pretenders.txt:4`、`events/heavenly_kingdom_events.txt:300`。

```text
国家日志积累复辟／起义进度 → 换君或建国事件
    → 召回本人（流亡池、虚空、他国）或按模板新建 → 立为君主、流放旧君
    → 巩固日志按王朝标记判断 → 王朝被推翻或君主制废除 → 失败
```

```pdx
# 模板写明王朝，巩固时按王朝而不是按个人判断
CLAIMANT = {
    # 名字、文化、生日、IG 等按共用模板填写
    on_created = { set_variable = { name = dynasty_var value = flag:house_DEMO } }
}

# 复辟事件 immediate（国家作用域）
ruler = {
    save_scope_as = old_ruler
    set_temporary_event_immortality = { DURATION = 3 }
}
country_summon_character_effect = {           # 原版效果：已有本人就召回，没有才新建
    TEMPLATE = CLAIMANT
    ON_CREATED_EFFECT = summon_generic_make_ruler_effect
}
scope:old_ruler ?= { exile_character_with_martyrdom = yes }
# option 中加巩固日志；after 撤 old_ruler 的保护
option = { name = person_demo.8.a add_journal_entry = { type = je_demo_restoration } }
after = { revoke_temporary_event_immortality = { CHARACTER = scope:old_ruler } }

# je_demo_restoration 的失败条件
trigger = {
    OR = {
        NOT = { country_has_monarchy_law = yes }
        NOT = { ruler ?= { var:dynasty_var ?= flag:house_DEMO } }
    }
}
```

`country_summon_character_effect` 处理本人的各种处境：在虚空中先放出，在流亡池就转籍并延长任期，在别国任职就转籍登位；如果他正是另一个君主国的现任君主，原版不转籍，而是让两国结成共主邦联（威望高者为宗主）。设计东燕复国这类内容时先决定这一情形能否接受。见 `common/scripted_effects/00_victoria_ip4_scripted_effects.txt:2014`、:2119、:2130、:2166、:2210。巩固日志按 `dynasty_var` 判断，同一王朝内换人不算失败。见 `01_french_monarchism.txt:268`、:299、:418。

**同一人从煽动者变成新国家君主。** 原版太平天国在起义时处死作为煽动者的洪秀全，再按同一模板为新国家另建一个天王，人物前一阶段的修正、变量和人气都不带过去；若他此前被流放并为别国所用，新国家改用无名替身。见 `events/heavenly_kingdom_events.txt:325`、:333、:519；`common/scripted_effects/00_victoria_scripted_effects.txt:151`、:162、:182。要保留同一人时，建国后在原引用上转籍并立君：

```pdx
c:NEWTAG ?= { save_scope_as = new_state }
global_var:demo_leader ?= {
    transfer_character = scope:new_state
    set_character_as_ruler = yes
}
```
