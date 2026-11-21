# 土邦的本地项目：自己出资、邻邦出资或外国出资

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none

依据工作台 `reports/2026-11-21-india-development/印度发展与帝国设计报告.md` 第六、七、九节和同目录 `第一批/落地核查.md`。这是设计报告的第一个闭环，验收样本是占西（JHN，法国朝贡国）、莫卧儿和法国。写法通用，没有写死标签。

## 玩家看到什么

土邦在「诸邦之间」点「筹办本地项目」，依次选：

1. 办什么：大学、工具工坊、铁路，或者先请别国工程人员来考察。
2. 办在哪里：有两个以上的州可建时才问，最多列三个，按人口排。
3. 由谁出资：我国出资，向最富的印度政府提出，或者向外国政府提出。属国的外国只有宗主，与「出使求援」的规则相同。

| 出资办法 | 结果 |
|---|---|
| 我国出资 | 一级建筑进入政府建造队列 |
| 别国出资办工具工坊或铁路 | 对方拨款 `nesnd_india_grant`，一级建筑立即落成，产权归对方政府，我国欠一份义务 |
| 别国出资办大学 | 对方拨款，不取得产权，工程进入我国建造队列，我国欠一份义务 |
| 考察与培训 | 我国付 £5,000，得 24 个月的修正 `nesnd_india_survey` |

答复的政府得到一条 30 日的日志「印度事务」（`nesnd_india_foreign_affairs`），上面是许可／不许可或同意／婉拒。30 日不答复算没有答复。AI 在日志的周脉冲上按概率答复。

## 宗主许可

- 傀儡国向别国提任何一种请求，都要宗主先许可。
- 朝贡国、自治领、保护国只有让别国政府取得产权（工具工坊、铁路）时要宗主许可。
- 出资的就是宗主时不问。
- 傀儡国不能作出资方。

宗主许可以后，请求才送到出资的政府。占西请莫卧儿出资办工具工坊：先问法国，再问莫卧儿。

## 约定记录

别国出资的约定记在州所在的地区上（`nesnd_india_deal_host`、`_funder`、`_permit`、`_quote`、`_kind`、`_term`），为期五年。期内该地不能再订出资约定。期满只清记录并通知，已取得的产权不变。州换了主人，旧记录不再算数。

## 文件

新文件：`common/script_values`、`scripted_triggers`、`scripted_effects`、`scripted_buttons` 下的 `nesnd_india_projects.txt`，`common/journal_entries/nesnd_india_foreign_affairs.txt`，`common/static_modifiers/nesnd_india_projects.txt`，`common/customizable_localization/nesnd_india_projects.txt`，`events/nesnd_india_project.txt`，中英 `nesnd_india_projects_l_*.yml`。

改动：`common/journal_entries/nesnd_india_core.txt`（「诸邦之间」挂两个按钮、三行状态、AI 每月 3% 起一个项目），`common/scripted_effects/nesnd_india_core.txt`（月度检查），`common/scripted_triggers/nesnd_india_diplomacy.txt`（等候答复的项目占用交涉名额）。

## 没有做

- 别国出资只能新建，不能给已有的工具工坊或铁路扩股。已有建筑由本国出资扩建，或走「出使求援」的工程师。
- 邻邦和外国各只列一个候选（最富且付得起的）。
- 小国系统的「邀请莫卧儿投资」按钮（要求对方独立）没有动。
- 贷款、担保、驻军、不丹和西秦、自治加入、帝国制度、海外都不在这一项里。

## 待实机

1. 答复方日志由效果加入后正常出现，30 日超时结局按期触发；同一国家答复完一件以后，第二件能再次加入同类日志。
2. 状态行里沿变量取国名、州名的长链（`…Var('nesnd_india_matter_from').GetCountry.MakeScope.Var(…)`）显示正常。
3. 事件 `.2`、`.3` 的选项读到上一步保存的作用域，国名和州名正确。
4. `create_building … add_ownership` 给铁路记外国政府产权（工具工坊已有存档证据，铁路没有）。
5. `start_building_construction` 之后建成一级，「工程落成」事件按月弹出。
6. AI 宗主和出资方在周脉冲上答复，`random` 读 `scope:` 数值的概率生效。
7. 五年期满后弹「约定期满」，地区上的记录清掉。
