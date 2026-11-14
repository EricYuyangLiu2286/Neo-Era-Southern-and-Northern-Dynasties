# 人物设计：职位与事业

> 何时读：设计煽动者、制度席位、跨国人物、公司经理或由日志任用的负责人。先读 [character-design.md](character-design.md) 的共用骨架。不必读：君主继位、宠臣、觊觎者与复国（见 [character-court.md](character-court.md)）。

## 二、思想家、运动与法律

**用于** 玩家能决定政治人物留国、流亡、出任领袖或继续一项事业。孙中山可一场结清，马克思的出版则需跨年保存作者。煽动者后来要当新国家的君主时，接第八节。

```text
日期＋制度＋席位 → 生成煽动者 → 留国／任领袖／流放
   → 后续日志或事件按本人／故国／集团接手 → 成果归运动
```

```pdx
# 国家事件 trigger；PERSON 模板设 is_agitator = yes
trigger = { empty_agitator_slots >= 1 NOT = { is_template_used = PERSON } }
immediate = {
    create_character = { template = PERSON save_scope_as = author }
    set_variable = { name = demo_author value = scope:author }
    scope:author = { set_temporary_event_immortality = { DURATION = 3 } }
}
option = {
    name = person_demo.3.a
    scope:author = { set_as_interest_group_leader = yes }
    add_journal_entry = { type = je_demo_publication }
}
option = {
    name = person_demo.3.b
    scope:author = { exile_character_with_martyrdom = yes }
    remove_variable = demo_author
}
after = { revoke_temporary_event_immortality = { CHARACTER = scope:author } }
# 出版 JE 的成功 effect：重新认作者，另为死后出版设计编辑/机构分支
if = {
    limit = { var:demo_author ?= { is_character_alive = yes } }
    var:demo_author = { add_trait = literary }
}
remove_variable = demo_author
```

给日志加研究、运动或法律的实际完成条件；若允许死后出版，保留作品进度并切换署名。若仅保留活作者的路线，沿共用失效结局收束。需要外国承接时由全局槽／故国重找本人，单国变量不会随转籍自动迁移。权重、年脉冲和固定延迟分别说明。

## 三、制度席位与可替代的执政者

**用于** 总统、现任 IG 领袖或谈判代表随政治制度选出，政局要记录“那时是谁”。林肯式遇刺只认内战获胜时被标记的那位元首，他不在位时事件不触发；郭庆达的保护保存开局总统，跨三次选举，换人即撤。

```text
开局创建或原生选举 → 制度节点读取 ruler → 保存本人／标记
    → 在任检查或选举回调 → 结算本人及原 IG → 清理离任者
```

```pdx
# 若需固定开局人，history 先 create_character = { template = PERSON }；
# 动态席位让原生选举产生。内战 JE 获胜时锁定当时的元首。
ruler = { save_scope_as = wartime_president }
set_variable = { name = demo_president value = scope:wartime_president }

# 政治事件 trigger 和 immediate，要求仍在位
trigger = { ruler ?= var:demo_president }
immediate = {
    ruler = {
        save_scope_as = incumbent
        set_temporary_event_immortality = { DURATION = 3 }
    }
}
option = { name = person_demo.4.a scope:incumbent = { add_modifier = { name = PERSONAL_REWARD } } }
after = {
    revoke_temporary_event_immortality = { CHARACTER = scope:incumbent }
    remove_variable = demo_president
}
```

给等待此事件的 JE 加上“新君已不是保存者”的失效清理；若本意是褒奖卸任者则直接读保存对象。竞选保护要设届数／日期、落选和政体废除出口，以离任者和原 IG 作清理对象。写真实死亡选项时先解除本事件的保护，并在触发阶段排除本来就不死的人。

## 四、跨国移动的人物

**用于** 接纳本人能改变军事力量或所在州，移交、拒绝、回国、流亡会改变下一站。加里波第把军力与国内政治代价一起带到东道国，洪秀全把州修正带到目的地。

```text
首站创建／流亡池认领 → 接受并授职 → 东道国日志与地方效果
    → 和平／驱逐／易主 → 撤原地效果 → 同一人转籍或结案
```

```pdx
# 首次接纳的国家事件 immediate，PERSON 是非将军模板
create_character = { template = PERSON save_scope_as = visitor }
set_global_variable = { name = demo_visitor value = scope:visitor }
scope:visitor = { set_temporary_event_immortality = { DURATION = 3 } }

# 接受选项
scope:visitor = { add_character_role = general }
add_journal_entry = { type = je_demo_mission }
# 拒绝选项，若设计允许回流则保留全局引用
scope:visitor = { exile_character = yes }
# 两选项共用 after
revoke_temporary_event_immortality = { CHARACTER = scope:visitor }

# 东道国 JE 完成后调用移交事件；receiver 是已选定的下一东道国
global_var:demo_visitor ?= {
    remove_character_role = general
    transfer_character = scope:receiver
}
```

上述创建只用于模板未用且无现存本人；后续接纳从原引用／流亡池取人。先撤原州或营房修正再移交。JE 的失效结局核角色仍任职、人在预期国家且不在流亡池；终局清全局引用。若任务允许流亡再回来，分开“本次东道国退出”和“全线终止”。别把临时不死当成防退休、防流放或防吞并。

## 五、公司经理与持续经营

**用于** 产业比任职者寿命长。原版周学熙以开平矿务经理的任用规则入场；经理可以换人，公司照常经营。公司和经理是两个对象，分开引用。

```text
成立实际公司 → executive_usage 匹配 → 原生任用
    → JE 调经营事件 → 公司取当任 executive → 退休／换任后重读
```

```pdx
# PERSON 模板内，名称与 IG 按共用模板填写
executive_usage = {
    country_trigger = { has_dlc_feature = mp1_content }
    company_trigger = { is_company_type = company_type:COMPANY }
    earliest_usage_date = 1880.1.1
    latest_usage_date = 1920.1.1
}
# 公司经营 JE 的成功 effect：trigger_event = { id = person_demo.5 }
# person_demo.5 的 immediate
ordered_company = {
    limit = { is_company_type = company_type:COMPANY }
    order_by = company_owned_levels
    position = 0
    save_scope_as = firm
    executive ?= {
        save_scope_as = manager
        set_temporary_event_immortality = { DURATION = 3 }
    }
}
# 任职者存在才开放人物选项；常规经营选项只读 firm
option = {
    name = person_demo.5.a
    trigger = { exists = scope:manager }
    scope:manager = { add_trait = TRAIT }
}
option = {
    name = person_demo.5.b
    default_option = yes
    add_treasury = 1000
}
after = { revoke_temporary_event_immortality = { CHARACTER = scope:manager } }
```

经理死亡时公司可继续经营，普通经营选项应照常开放；公司本身消失时再结算公司日志。永久性企业繁荣效果给公司，个人特质和任职期间效果给经理。显示名字时先确定有经理；没有就显示公司。原版经营事件取实际经理示例见 `events/japan_events/ep2_zaibatsu_events.txt:32`。

## 六、由日志任用的人推动项目

**用于** 成果取决于实际人选的集团、特质、所属机构和在岗时间。原版沙皇的宠臣议程在开场按宠臣所属集团定下工业目标，并把此人存进日志变量；宠臣死去或被撤即失败（`common/journal_entries/08_tsarpoints.txt:2678`、:2691、:2786）。若岗位允许换人，写明结算用新任还是原任。

```text
大学／机构符合资格 → 候选人 → 确认任命 → 项目日志按月读特质
   → 提前停止／失去负责人／达到目标 → 成果给机构，任职效果归还
```

```pdx
# 用共用创建入口保存 demo_appointee；任命后开 je_demo_person。
# JE 的 on_monthly_pulse：项目用国家进度，读的是实际受任者。
on_monthly_pulse = {
    effect = {
        if = {
            limit = { var:demo_appointee ?= { is_character_alive = yes owner ?= root } }
            change_variable = { name = demo_research add = 1 }
            if = {
                limit = { var:demo_appointee ?= { has_trait = meticulous } }
                change_variable = { name = demo_research add = 1 }
            }
            if = {
                limit = { var:demo_research >= 12 }
                set_variable = demo_task_done
            }
        }
    }
}
# 初始化 JE 时 set_variable = { name = demo_research value = 0 }。
# 成功调用 person_demo.1，清 demo_research；未完成且失去负责人
# 走共用 hidden invalid_outcome，也清 demo_research。
```

只给任职者窗口所需的短期保护；若必须忙碌到项目结束，先记录由谁加的标记，所有成功、失败、撤销分支调用相同解除逻辑。换人后允许继承进度时，明定结算用新任还是原任。把学校州或公司作为奖励对象可让角色死亡后留下制度结果。
