# 人物设计

> 何时读：设计或修改一个具体人物的出场、任职、玩家选择、保护和退场。先读本文件的共用骨架，再按下表读对应一类。不必读：只换名字、衣着或画像（按原有本地化／人物像流程处理）。

[1.15.1 案例清单、案例卡和逐行人物树](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/2026-11-14-character-design/README.md>)。先选与设计最接近的一张卡，用树核对实际承担玩法的对象。

## 先选身份，再决定存什么

问一个能改变设计的问题：如果明天换了执政者、将军或公司经理，下一阶段应当跟着谁？要跟本人，创建或查到人物后保存对象；要跟职位，在结算当日重读 ruler、leader 或 executive；要跟国家制度，把进度和倒计时留在国家或日志上。人物上的布尔标记适合“这是曾经担任某职的人”，不能代替对人物对象的引用。流亡池中的活人、退役、死亡、被吞并后对象失效各有不同后果。

下列及两个分类文件中的代码均为分文件嵌入的 Jomini 片段。大写字是需替换的数据库键或本地化键；`person_demo.1` 等换成本项目未用的事件 ID。事件放在声明 `namespace = person_demo` 的事件文件里。模板的固有人名、文化、出生日期、IG 和特质选自该人物设定。各节给出差异部分；需要跨弹窗持有本人的类型共用下面这个最小骨架。

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

正文用 `[SCOPE.sCharacter('speaker').GetFullName]`，职位用 `GetPrimaryRoleTitle`，日志持久引用可用 `[ROOT.Var('demo_appointee').GetCharacter.GetFullName]`。无人时用有效性条件切换到机构或地点文案。短期保护 helper 的 DURATION 是后备月度计数；窗口的 `duration` 和正常 after 撤保护另算。原版依据：`common/scripted_effects/00_victoria_ep2_scripted_effects.txt:3063`、`common/on_actions/00_code_on_actions.txt:697`。

## 八类用法去哪里查

| 类 | 用于 | 原版／NESND 案例 | 文件 |
|---|---|---|---|
| 一、王朝继承和外交关系 | 继位改变条约、王朝或继承资格 | 维多利亚、明治 | [character-court.md](character-court.md) |
| 二、思想家、运动与法律 | 留国、流亡、出任领袖、继续一项事业 | 马克思、孙中山、太平天国洪秀全（煽动者阶段） | [character-office.md](character-office.md) |
| 三、制度席位与可替代的执政者 | 总统、IG 领袖随制度选出，要记“那时是谁” | 林肯、郭庆达 | [character-office.md](character-office.md) |
| 四、跨国移动的人物 | 本人移交、拒绝、流亡会改变下一站 | 加里波第、洪秀全（NESND） | [character-office.md](character-office.md) |
| 五、公司经理与持续经营 | 产业比任职者寿命长 | 周学熙 | [character-office.md](character-office.md) |
| 六、由日志任用的人推动项目 | 成果取决于实际人选和在岗时间 | 沙皇宠臣议程 | [character-office.md](character-office.md) |
| 七、君主身边的宠臣或近臣 | 权力来自某位君主的宠信 | 拉斯普京与宠臣角色 | [character-court.md](character-court.md) |
| 八、流亡觊觎者、复国与起义建国 | 复辟、复国或建国时由此人登位 | 法国三派觊觎者、太平天国洪秀全 | [character-court.md](character-court.md) |

案例卡与人物树见上方研究目录；工坊 MOD 案例只在研究目录里作对照，不作为本技能的写法依据。

## 反面例子

| 不要这样写 | 应该这样写 | 原因 |
|---|---|---|
| 沈季川旧链先报姓名、再尝试生成人，90 天后作一次表态 | 人物不可替代时先确认其在场，再给任用或拒绝后果；废奴后的识字直接由受影响地方承接 | 弹窗和创建分别检查会出现无人发言、文本却点名；全国 IG 好感无法说明识字怎样改变当地 |
| 洪秀全旧旅途仅检查死亡旗标，每周按州强制转籍 | 校验同一对象、职务、所在国与州；自己发起吞并时先处理当地任职者；死亡和失联汇入同一退出 | 旧档记录退休及对象清理，未触发故事死亡；脚本能选中本人只是风险证据，不能据此认定某事件杀了他 |
| 把作者要的“保护郭庆达参加三次选举”写成换届后硬改回总统，或只给终身不死 | 三次选举内保住参选机会，政治力量给实际 IG，选举自行定胜者；落选、政体变化或期满时清保护 | 玩家能通过原生制度改变结果。清理须引用离任者，否则容易把保护留给旧人或误伤新任 |

## 检查清单

- 哪个玩家行动或制度变化需要此人？姓名换掉后哪项选择、代价或收益会改变？若只有一句引语，只做本地化。
- 明确创建入口、日期／DLC／法律、角色、IG 和模板是否已用；开局、事件、引擎任用及替补路径是否可能重复造人？
- 写出“谁保存、谁读取、何时删除”。区分国家／全局槽、事件 scope、身份旗标。列出候选的排序、备选和无人时的分支。
- 逐阶段写清 JE、脉冲、事件、按钮或 on_action 的实际调用；分别验证条件、随机权重、提示和真实效果。
- 保护防的是哪类退出？谁获得保护、谁解除？流亡、退职、失势、国家消失、换任、普通死亡时分别继续、替补还是结案？
- 本地化读的是同一角色、实际职务及状态吗？无人版能否显示机构或地点？静态引语不要求人物 scope。
- 以 `character:模板键` 跑 near 和 person（命令见 [tools.md](tools.md)）。人物存进变量列表、经列表撤保护这类路径在图上显示为列表节点，展开它再核；反查模板键、实际变量和关键效果行，核对每条分支的接收人、原文出处和结束后的残留。
