# Batch A2 实施交付

状态：**READY_FOR_TEST / 编辑冻结**。冻结时刻 UTC 2026-11-04T15:24:16.905511。本报告不是STATIC_PASS或ENGINE_PASS。

执行者 `/root/sol_a2_implementation`。实际分派配置 **gpt-6.1-sol / medium**；证据为root的NEW_TASK显式实施分派。没有把本代理当作Luna探索、Astra草案或独立Sol审查代理；复用交接所列既有源研究及root裁定。架构、计划结构、数值裁定和主MOD合入仍归root。

## 对象与所有权

- 唯一编辑候选：`WORK/exports/canon-route-execution-20261104-a`。
- 编辑前独立备份：`WORK/backups/batch-a2-pre-change-20261104`。
- 冻结的本批所有权副本：`WORK/backups/batch-a2-frozen-owned-20261104`。仅32个owned文件，不冒称整个并行候选C已冻结。
- 所有权SHA：`batch-a2-owned-files-sha256.json`。**32个owned文件，其中27个实际改变、5个保留不动**：原生月度progress bar、静态修正、NKH国家定义、已有Turtle Island JE守卫、Cherokee七事件stub。
- A1局部diff：`batch-a2-a1-localized.diff`。含HUS exodus函数body、HUS迁徙通知desc接线、NKH文件重写的完整可审查差异。
- 原版三个按钮窄diff：`batch-a2-turtle-island-native.diff`。原版body复制保留，只增加REPLACE及visible/possible/effect的NKH/native_successor守卫。AST等价证明留独立测试。
- 写作对读：`batch-a2-writing-comparison.md`，131键中英文逐条编辑判断及真实返工轨迹。

主MOD、GAME、创意工坊、作者材料均未写入。未重跑人口重配工具，未编辑任何history/pops、州归属或地图。工具与报告均在WORK，未把QA工具放进C。

## 原版完整链条与版本

入口运行NESND catalog status，结果 **CURRENT，1.13.11 / Steam build24799966，changed_count=0**。原有75项来源指纹在 `batch-a2-source-manifest.json`；本实施继续读取其原文件上下文，而非将旧草稿当API证明。

|闭包|实际只读来源|本批适用差异|
|---|---|---|
|JE→进度→建国→DP|GAME common/journal_entries/04_sepoy_mutiny.txt；common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt:461起；script_values.md:38–40、119起|保留原生bar月度更新为唯一月增写入者；政治谈判只通过add_progress一次扣15；实际create_country一次给完整1/2/4个state。|
|国家、文化与王朝|00_countries.txt:2786/3109；00_cultures.txt相关六文化；country_peu.txt:43；historical_leaders_americas.txt:20|NAH议会君主/TWT寡头宫廷；old_confucianism仅国教。NAH/TWT独立身份helper，不放宽A1 native helper。Juárez不凭空重生、Huachaca不被偷换。|
|战争目标与结算|war_goal_types.md:47起；00_annex_country.txt；08_humiliation.txt；29_restore_union.txt:152起；engine effects.log:909、536、36672|三专用goal，custom只on_enforced执行；复国败方仍活时先40%迁徙/流亡再annex；无泛occupation胜利；旧精确案件DP可移除旧annex/humiliation目标并补专用目标。|
|人口与人物|effects.log:9830/9844；red_scare_events.txt:1276；00_scripted_effects.txt:720；00_character_interactions.txt:997起|真实move_partial_pop/move_pop；HUS缺目的地即时终态。流亡最多三人、优先本案代表，实际invite_exile接纳门槛逐项保留；不满足者留流亡池。|
|军队与设施|effects.log:817、959、37330；00_land_combat_unit_types.txt:83；20_military.txt前置链；01_industry.txt:3/100/127/411/435；10_production.txt:30|只补现有正规营不足，分州兵营按全国容量目标补差；已有建筑级计入全国设施上限。最低军事链及manufacturies，不补整era2、金币或海军。|
|人物与生命周期|00_code_on_actions.txt:2566 on_character_creation、2604 on_character_death、6991 on_war_end；engine has_template/has_role/is_character_alive|四具名人物的seen/dead永久收据，全球/流亡/void查活体；不按月刷新人物。DP回调不是winner判断，周监视只读取实际终态。|
|汗号与旧入口|01_monarchies.txt:2350 gov_khanate；turtle_island_buttons.txt完整三按钮；00_turtle_island.txt；当前C的native_resettlement.txt|gov_khanate只增加本案NKH白名单，继承、摄政和臣属守卫及两个回调保留。Cherokee无证据无需扩大覆盖。|

新增接口补读记录：engine effects.log every_diplomatic_play:2995、every_scope_building:4671、every_scope_character:4677、create_character:845、remove_diplomatic_pact:36481、ordered_scope_state:16993、set_variable:37194、while:37383；triggers has_diplomatic_pact:10248、has_role:10746、has_template:10891、is_character_alive:11351、is_building_type:11327、play_participant_has_war_goal_of_type_against:13465；event_targets owner:451、level:270。set_variable内inline value有00_code_on_actions.txt:98原生实例；months期限有brazilian_slavery.txt:147等原生实例。

## 实现结果

1. 修订计划§8、§17及文案契约为用户原意：**每源pop一次70/30目的地概率**。双目的地使用random_list+move_pop；仅一目的地全送该处；均缺时人口留原地、清pending、写本epoch终态。A1 exodus只替换body调用外置A2 helper；外围A1 maintenance、12月时钟与.10回调未改。
2. 墨西哥与各秘鲁政府分别持有压力和政治行动。首次真实建国占用地区案件；旧resolved不等同实际胜利。大国两州、小安第斯一州、剩余人口和完整所有权限制落库。创建后首都取新国人口最大州；原国首都若被选则先迁到最大剩余人口州。
3. 镇压准备估计采用root后续裁定：大国min(当前全国人口50%,两座合格核心州最高人口合计)；小安第斯最高单个合格州。对应军力档×1.5，最低8。它是保守准备估计，实际建军仍按成功割地后的人口档。没有另造全pair预览枚举系统。
4. NAH与TWT有不同法律、主流文化、宫廷信仰与人物。和平承认和现有TWT的90日请求均在effect重验。请求持对象+递增epoch、期限、拒绝/逾期与12月冷却；旧窗口不能重复吞并。
5. 40%迁徙在实际受控败方或政治镇压国仍活时执行一次；每源pop随机HUS人口州。无HUS/人口州立即终结为无目的地；旧sent收据不重迁。原生流亡角色清理、HUS真实接纳资格与三人上限落库。
6. 复国custom war_goal执行是唯一吞并授权。双方互指、同epoch、同专用DP，并在enforced时核已保存DP对象；对手消失不授胜利。无目标执行的停战、建战失败、第三方中断分别终态。
7. NKH按原生邻接从USA人口州探索连通分量，最多15次种子尝试，选满4州才一次create_country。美国保留至少一座人口州。割地后才迁USA余下/HUS各50%，每源收据独立，每源pop一次目的州抽选。次日准备军政，四州原有人口不再迁第二遍。
8. NKH军队8/16/24/32/40档，复国2/4/8/12/16/24档，均只补不足。兵营容量与设施计入继承级数，军队落在各州；新队有同国将领。补standing_army→mandatory_service/gunsmithing/military_drill→artillery/line_infantry及manufacturies。
9. USA与原HUS两条独立真实直接战争，各自原对象、attempts、实际DP、dispatched与outcome；已在同pair普通战争则等待。最多12次月度尝试，失败不冒称胜利。只移除本pair盟约/防御约和停战。汗国仍活且两条均终态才结束生存日志。
10. 北美宣称和全美洲决议显式补格陵兰，并沿有效G+C geographic regions保留作者南北大原。原住民HUS要求旧HUS真亡、无现有战争、完整全美洲所有权；实际change_tag成功后执行24普通法和A1受限native文化helper，不重建人口/财富/军队。
11. 旧稿已迁人口、已准备军队及已创建收据不重发。旧NKH不足4州只标旧案不符，不自动割地或补军。NAH/TWT已有本案实体一次采用王朝身份，普通无本案标记国家不被接管。TIS三按钮旧窗口effect同样守卫。

## 冻结后必须由测试代理核查

**本代理未运行任何行为测试、AST测试、Tiger、MCP或游戏**。已执行的仅为源码阅读、apply_patch落库、独立备份、文本编辑对读和SHA/统一diff归档。下一步由root另派测试。

优先覆盖：全部ordered AST/宏展开/scope/value动态闭包；源SHA与32 owned freeze；A1 24文件保护与native helper原样；人口分母、1/2/4州选择、四州连通/split-state/移首都、继承建筑总上限、营数与实际formation；每源70/30抽签分支及两/一/零目的地；50%割地后分母；40% on_enforced先迁后吞并；邀请双窗口/拒绝/超时；角色死亡/已有模板/流亡pool；两独立DP与真实双方goal；Cherokee七stub与TIS三按钮非本案AST保留。

尤其不能仅凭静态检查宣称已证明的引擎语义：

- create_country当次total_population缓存是否已刷新（复国军政当次读取；NKH按次日读取）。
- 自定义on_enforced内move_partial_pop→角色流亡→annex的真实执行次序及死国scope有效性。
- 直接war=yes后定位真实DP、双方goal和formation的实际结果。
- 原生state邻接在split-state场景的具体粒度。
- 旧native DP已有战争目标的remove/add转换是否在战争中允许。当前迁移入口为周度监视，不能声称已证明“读档瞬间、周度回调之前直接接受旧和平窗口”受控；若真实验收要求该场景，需要有原生可证的load回调或其它明确入口，不能伪造on_game_loaded。
- 90日事件到期默认选项与pending期限的同日顺序；需区分真实点击拒绝和超时文案，不把源码guard当引擎证据。

以上均为待验证边界，不是已通过结果。冻结后本代理停止编辑，等待root的测试结果/修复分派。

