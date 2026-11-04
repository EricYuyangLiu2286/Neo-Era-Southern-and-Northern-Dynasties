# 最终实现与原生链条

GAME为D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game，1.13.11/build24799966；原始研究31份指纹见seven-countries-source-manifest.json。以下补充最终实现区别，指纹见implementation-source-hashes.json。

|机制|当前来源|最终使用/差异|
|---|---|---|
|国家建设JE→country_event→两项奖励|common/journal_entries/00_art_jes.txt:1—48；events/tech_events/society_tech_events.txt:192起；common/static_modifiers/02_event_modifiers.txt:1746起|原生any_scope_building+level+occupancy，7国分别读取自己的地区/建筑。原版艺术主题不搬入；改成各国架空建设议题。|
|原生累计进度|common/scripted_progress_bars/scripted_progress_bars.md:1—34；00_victoria_progress_bars.txt:149—160；本MOD ce_french_empire.txt:31—37|进度唯一存于JE本身，monthly_progress在owner国家读取当前条件；12个合格月可不连续，战争暂停。没有变量镜像、周期helper和手动同步，避免双重增长。完成在JE scope读取scripted_bar_progress。|
|时间及失效|journal_entries.md:335起、00_art_jes.txt:47的3650日实例；05_austria_journal_entries.txt既有结束逻辑|采用5475日（15×365游戏日）上限，失败/timeout发一次无奖励通知，身份失效封口。失败州数有本地化，不复发用户的num_states缺文字问题。|
|国家修正|society_tech_events.txt:471、548的国家选项add_modifier（realist_art/new_academia），对应02_event_modifiers.txt:1746—1752；引擎effects.log add_modifier；modifiers.log:439、1695、1871、3013、3105、3113、3193、3201、3209|最终采用国家范围限时奖励，让当前所有国控制其应用，避免生成已失去地区的持久scope。资源键包括州/建筑修正可由国家向下传播。相对研究初稿州局部5%，定稿为行业15%、建设10%、教育机会5百分点等5年；两项只选一项。|
|模板参数|GAME/common/scripted_effects/00_scripted_effects.txt:1161—1199及项目已有参数化效果|EVENT/MODIFIER/IDENTITY是脚本参数，不是持久scope。外部AST先展开参数再执行，Tiger解析全部调用，MCP核真实节点。没有把动态字符串当对象引用。|
|PRU来源保留|common/on_actions/00_code_on_actions.txt:1—14的无root开局；本MOD nesnd_india_core.txt:1—4的country周期例|开局安全c:PRU写标记，旧PRU存档周脉冲补标；PRU变NGF/GER同国延续。已经形成且没有原籍标记的GER旧档不猜其是否普鲁士发起。|
|AUS/TUR/USA后置|05_austria_journal_entries.txt:18、29、72；sick_man.2/.3的sick_man_complete；原生je_acw_war|AUS使用曾存在的hungarian_acceptance_var/established标记加旧JE不活跃；TUR必须有结算标记，不能只查没有日志；USA废奴且原生内战JE不活跃，和平废奴也适用。|
|物资与工人|building定义、生产方法、原生occupancy、state_regions资源上限|不发军需库存。PEU利马/伊卡/阿雷基帕有实际铁矿上限；铁路目标为卡哈马卡/阿雷基帕。普鲁士真实ID是LOWER_SILESIA/UPPER_SILESIA，未使用猜测的SILESIA/CUSCO。|
|事件图片|GAME/gfx/event_pictures/*.bk2|逐个验证unspecific_trains、art_gallery、middleeast_engineer_blueprint、southamerica_election/factory_opening、unspecific_factory_closed，不复制工坊素材。|

人物/运动设计参考RAHF的实际思想传播、运动、人物复用链，详见small-state-survival-plan原始来源R01—R06。它是未来方案的机制启发；本轮7国独立短链没有复制RAHF剧情或覆盖其文件。

## 测试观察

当前error.log最后修改00:03，早于b374be5。保存为error-before.log，只作为已知失败输入；不能当本轮运行报告。前轮97项回归对当前候选重跑通过。

新AST测试初版67通过1失败：完成后重复JE的on_invalid删除待领票据。已改为同一身份保留票据、真实身份变化才取消。修复后的同用例通过；加上周期、迟答和预览等共71项。测试工具的漏传prev参数另修工具，不归类游戏BUG。

原生累计bar、自动事件选项、同日JE回调、实际就业/AI建设速度仍需游戏验证。新增数据/静态和模型证据不证明引擎无BUG。
