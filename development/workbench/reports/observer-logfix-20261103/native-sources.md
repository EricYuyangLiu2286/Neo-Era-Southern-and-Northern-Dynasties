# 实现前来源：1.13.11 / build24799966

GAME = `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`。本轮catalog status CURRENT、0 changed。源文件全部只读。

- `common/diplomatic_catalysts/01_event_catalysts.txt:24,30`：`"relations(scope:target_country)"` 的实际条件表达式。当前外交事件已在外层trigger_if确认sender存在；只修参数化表达式，维持比较发起国/接收国和AI加权。原来`relations:scope:`形式由实际引擎明确报Unknown trigger，不能只依赖通用parser成功。
- `events/agitators_events/luddite_law_events.txt:5,28`：先声明country_event，后定义cancellation_trigger，选项和取消条件负责法案结束后的事件寿命。项目四个援助事件把type放在取消字段之后，实际报invalid event type；移动声明顺序，不删条件。
- `events/africa_colonial_events_02.txt:341`调用`ideology_jingoist_leader`；`common/ideologies/01_character_ideologies.txt:2810–2813`定义character_ideology=yes。`00_ig_ideologies.txt:551`的ideology_jingoist属于IG。项目挑战者create_character只更正类别，不改变军队规模。
- `common/journal_entries/04_sepoy_mutiny.txt:4–8`：contextless分组搭配should_be_involved。项目`CE_04_sepoy_mutiny.txt`保留原链，最后加载的`zzzz_nesnd_india_native.txt`故意覆盖停用。错误来自最终覆盖缺参与条件；在最终定义加入always=no，不重新启用印度原生剧情。
- `WORK/references/engine-docs-1.13.11-20261031/triggers.log`的exists与trigger_if，以及项目已用`nesnd_ming_recruitable_royal`的owner存在分支：角色对象存在不等于owner存在。实际失败是`nesnd_ming_mark_retained_royals`经`nesnd_court_followup_monthly`读取已保存宗室；当前宗室可能迁移/流亡/死亡，不能用并列exists推定短路。候选把保存对象读取置于trigger_if内，再把owner比较置于独立exists owner分支，缺失返回false。角色生成、转移、姓名、阵营等实际effect逐项保留。

## 验证入口

- `GAME/gfx/map/spline_network/military_route_graphics/02_railroad_vehicles.txt:7,16`：日志六次报market无效；tag trigger决定是否显示火炮车厢（卖单阈值严格>5、>20），下面route_entities引用装甲火车资源并指定位置。新增同路径文本覆盖只保护两个market读取，缺market时两个tag均false；实体、位置、车长、计数及现有经济不变。没有搬运任何模型或纹理。

`test_observer_log_errors.py <root>`读取真实脚本AST与原生意识形态数据库。修改前六类检查失败，涵盖缺角色、无owner、字段顺序、关系语法、意识形态类别、全局JE参与；候选通过。字符链接fixture只验证已捕获的读取错误，不模拟游戏寿命、战争或引擎调度。
