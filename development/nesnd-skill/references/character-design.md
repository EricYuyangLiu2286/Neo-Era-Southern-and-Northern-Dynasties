# 人物设计

设计或修改一个具体人物的出场、任职、玩家选择、保护和退场时读。只换名字、衣着或画像时按原有本地化／人物像流程处理。

[1.15.1 案例清单、案例卡和逐行人物树](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/2026-11-14-character-design/README.md>)。先选与设计最接近的一张卡，用树核对实际承担玩法的对象。

## 先选身份，再决定存什么

问一个能改变设计的问题：如果明天换了执政者、将军或公司经理，下一阶段应当跟着谁？要跟本人，创建或查到人物后保存对象；要跟职位，在结算当日重读 ruler、leader 或 executive；要跟国家制度，把进度和倒计时留在国家或日志上。人物上的布尔标记适合“这是曾经担任某职的人”，不能代替对人物对象的引用。流亡池中的活人、退役、死亡、被吞并后对象失效各有不同后果。

下列为分文件嵌入的 Jomini 片段。大写字是需替换的数据库键或本地化键；`person_demo.1` 等换成本项目未用的事件 ID。事件放在声明 `namespace = person_demo` 的事件文件里。模板的固有人名、文化、出生日期、IG 和特质选自该人物设定。各节给出差异部分；需要跨弹窗持有本人的类型共用下面这个最小骨架。

### 共用的创建、引用和退场

```pdx
# common/character_templates/ — PERSON 是模板 key
PERSON = {
    first_name = FIRST
    last_name = LAST
    historical = yes
    culture = cu:CULTURE
    birth_date = 1820.1.1
    interest_group = IG
    role = character_role_politician
}

# 国家效果。放在已满足日期和制度条件的唯一入口。
if = {
    limit = { NOT = { is_template_used = PERSON } }
    create_character = { template = PERSON save_scope_as = appointee }
    set_variable = { name = demo_appointee value = scope:appointee }
    add_journal_entry = { type = je_demo_person }
}

# common/journal_entries/ — 条件和效果在国家作用域
je_demo_person = {
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"
    group = je_group_historical_content
    outcome = {
        header = je_standard_completion_header
        effect_header = je_standard_on_completion_header
        conclusion_desc = je_standard_completion_conclusion_desc
        color = "gold_positive"
        trigger = {
            has_variable = demo_task_done
            var:demo_appointee ?= { is_character_alive = yes owner ?= root }
        }
        effect = {
            var:demo_appointee = { save_scope_as = speaker }
            trigger_event = { id = person_demo.1 }
            remove_variable = demo_appointee
            remove_variable = demo_task_done
        }
    }
    outcome = {
        flags = { hidden invalid_outcome }
        conclusion_desc = je_standard_failure_conclusion_desc
        trigger = {
            NOT = { var:demo_appointee ?= { is_character_alive = yes owner ?= root } }
        }
        effect = {
            remove_variable = demo_appointee
            remove_variable = demo_task_done
        }
    }
}

# events/ — 仅保护需要在窗口中等玩家作答的本人
person_demo.1 = {
    type = country_event
    title = person_demo.1.t
    desc = person_demo.1.d
    duration = 3
    immediate = {
        scope:speaker ?= {
            set_temporary_event_immortality = { DURATION = 3 }
        }
    }
    cancellation_trigger = {
        NOT = { scope:speaker ?= { is_character_alive = yes owner ?= root } }
    }
    option = {
        name = person_demo.1.a
        scope:speaker ?= { add_trait = TRAIT }
    }
    after = {
        revoke_temporary_event_immortality = { CHARACTER = scope:speaker }
    }
}
```

在结算前由本类的按钮、事件或原生制度写 `demo_task_done`。跨国或允许流亡的剧情应把 owner 检查换成自己的承接条件。只需一个事件时直接使用局部 scope，不建日志和国家变量。若有取消路径，不把长期资源的唯一清理寄托在窗口 after；可在日志结案时先把人物转存事件 scope，再释放国家引用。涉及同一人的多个保护来源时，只撤本剧情取得的保护。

正文用 `[SCOPE.sCharacter('speaker').GetFullName]`，职位用 `GetPrimaryRoleTitle`，日志持久引用可用 `[ROOT.Var('demo_appointee').GetCharacter.GetFullName]`。无人时用有效性条件切换到机构或地点文案。短期保护 helper 的 DURATION 是后备月度计数；窗口的 `duration` 和正常 after 撤保护另算。原版依据：`00_victoria_ep2_scripted_effects.txt:3063`、`00_code_on_actions.txt:697`。

## 一、王朝继承和外交关系

**用于** 继位会改变另一国家的条约、王朝或继承资格。维多利亚是共主邦联分裂的入口，明治另显示有名天皇与实际统治者可以并存。

```text
开局创建前君与继承人 → 双方国家日志 → 前君离位
    → 新君作用域 → 修改双方条约 → 次国确认
    → 邦联已解除／继承人缺失 → 失效
```

```pdx
# 放在 history/characters 的 c:COUNTRY 块；模板分别给 ruler/heir
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

## 二、思想家、运动与法律

**用于** 玩家能决定政治人物留国、流亡、出任领袖或继续一项事业。孙中山可一场结清，马克思的出版则需跨年保存作者，列宁可让 IG 接过议程。

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

**用于** 总统、现任 IG 领袖或谈判代表随政治制度选出，政局要记录“那时是谁”。林肯式遇刺保存内战获胜时的元首；郭庆达的保护保存开局总统，二者对换届的处理相反。

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

## 四、能移动的军官或特派员

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

**用于** 产业比任职者寿命长。原版周学熙以开平矿务经理的任用规则入场，银行案例则允许随机姓名与多任经理。选公司及其经理两个对象。

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

## 六、由日志任用的专家或改革者

**用于** 成果取决于实际人选的专业特质、所属机构和在岗时间。居里的学术职位可以换人；若是本人承接的委任，任期中断可直接关闭该项目。

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

## 反面例子

| 不要这样写 | 应该这样写 | 原因 |
|---|---|---|
| 沈季川旧链先报姓名、再尝试生成人，90 天后作一次表态 | 人物不可替代时先确认其在场，再给任用或拒绝后果；废奴后的识字直接由受影响地方承接 | 弹窗和创建分别检查会出现无人发言、文本却点名；全国 IG 好感无法说明识字怎样改变当地 |
| 洪秀全旧旅途仅检查死亡旗标，每周按州强制转籍 | 校验同一对象、职务、所在国与州；自己发起吞并时先处理当地任职者；死亡和失联汇入同一退出 | 旧档记录退休及对象清理，未触发故事死亡；脚本能选中本人只是风险证据，不能据此认定某事件杀了他 |
| 为郭庆达保住职位，换届后硬改回总统或只设终身不死 | 三次选举内保住参选机会，政治力量给实际 IG，选举自行定胜者；落选、政体变化或期满时清保护 | 玩家能通过原生制度改变结果。清理须引用离任者，否则容易把保护留给旧人或误伤新任 |

## 检查清单

- 哪个玩家行动或制度变化需要此人？姓名换掉后哪项选择、代价或收益会改变？若只有一句引语，只做本地化。
- 明确创建入口、日期／DLC／法律、角色、IG 和模板是否已用；开局、事件、引擎任用及替补路径是否可能重复造人？
- 写出“谁保存、谁读取、何时删除”。区分国家／全局槽、事件 scope、身份旗标。列出候选的排序、备选和无人时的分支。
- 逐阶段写清 JE、脉冲、事件、按钮或 on_action 的实际调用；分别验证条件、随机权重、提示和真实效果。
- 保护防的是哪类退出？谁获得保护、谁解除？流亡、退职、失势、国家消失、换任、普通死亡时分别继续、替补还是结案？
- 本地化读的是同一角色、实际职务及状态吗？无人版能否显示机构或地点？静态引语不要求人物 scope。
- 以 `character:模板键` 跑 near 和 person；反查模板键、实际变量和关键效果行，核对每条分支的接收人、原文出处和结束后的残留。
