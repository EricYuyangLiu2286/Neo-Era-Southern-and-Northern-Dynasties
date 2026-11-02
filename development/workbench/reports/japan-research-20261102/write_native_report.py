from pathlib import Path
import json,collections,sys,hashlib,re
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/japan-research-20261102')
d=json.loads((W/'native-inventory.json').read_text(encoding='utf8'))
rows={}
for c in ['journal_entries','events','buttons','support_definitions','character_templates']:
 for r in d[c]:rows.setdefault(r['id'],r)
def cite(rel,line=1,label=None):return f'[{label or rel+":"+str(line)}](<{(G/rel).as_posix()}:{line}>)'
def ref(key):
 r=rows[key];return cite(r['path'],r['line'],key)
def compact(n):
 return re.sub(r'\s+',' ',pdx.emit(n)).strip()
def textblock(rel,key,field):
 t,r=pdx.read(G/rel);n=r.get(key);return n.get(field) if n else None
out=[]
def w(s=''):out.append(s)
w('# 原版日本研究：1.13.11 / Steam build 24799966')
w('')
w('研究日期：2026-11-02。范围：本机 GAME 原版脚本、历史初始化与资源数据库，只读；不启动游戏，不修改 GAME/MOD/技能。`catalog.py status` 返回 CURRENT、changed_count=0。本文件是原版研究，不是丰臣日本剧情方案，也不证明任一 MOD 分支已实现或实机可达。')
w('')
w('方法：使用 NESND `scripts/pdx.py` 保序 AST，保留重复的 create_pop、create_building、option、role、modifier 等。附属 `native-inventory.json` 保存原始条目、源路径/行号、直接引用边与 SHA-256；所有表格中的人口、等级、资源、PM 都是初始化输入，绝不是游戏运行后的 GDP、实际就业、产量、价格、军费或财政。')
w('')
w('## 1. 可用于设计的结论')
w('')
w('1. 原版已有三种维新终局：天皇胜利、公武合体幕府胜利、公议舆论下保留德川政治地位。`fail` 在这条 JE 里是另一阵营获胜，不能直接译成玩家失败。共和国等非君主化走 `invalid` 并写结束标记。'+ref('je_meiji_restoration'))
w('2. 原版幕府不是换个政体名称：law_bakufu 退出会调用 `country_restore_japanese_emperor`，处理皇帝、前将军、继承人、摄政；家族链硬绑 Tokugawa/Yamato。丰臣世界线不能只替换本地化后照搬。'+ref('law_bakufu')+'；'+ref('country_restore_japanese_emperor'))
w('3. 不含九州的日本存在独立制度适配点：原版锁国法只许九州贸易，且可见性要求拥有九州最大 state。它影响开国路线、港口/贸易中心与对华贸易入口，而不是简单损失一州人口。'+ref('law_sakoku'))
w('4. 分裂三政权需要检查国家变量与全局变量的区别。原版废大名使用 `japan_daimyo_abolished` 全局标记，武士终结使用 `fall_of_the_samurai_global_var`；三国共存时不能把一国的改制自然视为全日本共同完成。'+ref('country_clear_daimyo')+'；'+ref('meiji.3')+'；'+cite('common/interest_groups/00_armed_forces.txt',132))
w('5. 本轮找到的是日本维新、宗教、财阀、北海道、琉球、朝鲜链，以及通用自由主义/法西斯链；未找到一条命名为“大正民主”或“日本军国主义”的日本专属 JE 主线。军政人物与政治法律可以支撑新设计，但那属于之后的架空改编，不能声称原版已提供成套线路。日本原生 JE 全表见第2节。')
w('')
w('## 2. 剧情入口、推进、终局')
w('')
w('```mermaid\nflowchart TD\n  H[1836 国家历史 ep2_content] --> T[天保危机 12年]\n  H --> S[锁国]\n  S -->|退出锁国且不闭关| SO[开国奖励]\n  S -->|废君主或天皇已复位| SF[锁国巩固终局]\n  O[君主+幕府法+非孤立主义] --> R[维新争夺]\n  R -->|天皇掌权稳定6个月| E[meiji.1]\n  R -->|公武合体:婚姻+幕府更新| K[ep2_meiji.8 幕府胜利]\n  R -->|公议舆论:投票制+德川入阁+天皇| Q[ep2_meiji.9]\n  R -->|非君主制| I[invalid:标记争夺已结束]\n  E --> M[改革总JE 12年]\n  Q --> M\n  M --> A[军制改革]\n  M --> B[经济改革]\n  M -->|ep2| W[访西使团]\n  M -->|非ep2| D[外交改革]\n  A --> SM[武士安置或清退]\n  M -->|全部完成 或 到期已有进展| C[meiji.2 选军务/外交/生产奖励]\n  M -->|到期无一进展| F[meiji.14 改革失败]\n  E --> J[神佛分离决议再开宗教JE]\n  K --> BU[佛教振兴决议再开宗教JE]\n  Z[工业家/公司持有量达到阈值] --> ZA[财阀JE:巩固或约束]\n  HC[完全拥有并整合北海道+城市] --> HJ[北海道开发]\n  RP[开国+中日琉三国存在] --> RJ[琉球影响力竞争]\n  KC[直接拥有朝鲜五州+殖民机构] --> KJ[朝鲜殖民JE]\n```')
w('')
w('图中箭头是脚本因果/资格关系，不是承诺固定历史年份或必然发生。经济和军制子JE如果已满足条件，会直接记完成而跳过添加；使团由按钮和事件另行添加。真实添加位置：'+cite('events/meiji_restoration.txt',26)+'、'+cite('events/meiji_restoration.txt',133)+'、'+cite('events/japan_events/ep2_meiji_restoration.txt',938)+'。')
w('')
summary={
'je_tenpo_crisis':('国家历史在 ep2_content 下直接添加；首日 tenpo_events.1；本州5荒废+720日强度5暴雨','12年(4380日)内累计议程≥8→tenpo_events.3；逾期→.4；目标支持强硬/改革/混合奖励'),
'je_sakoku':('同一国家历史直接添加；按钮主动开国，年度事件含 ep2_sakoku.3','无锁国法且无闭关法→.4；废君主或天皇复位→.5；不是强制必须开国成功'),
'je_meiji_restoration':('闲置可见JAP、君主、幕府、未结束；possible要求君主+幕府且非孤立主义/变体','帝方：天皇特质+无内战进度+无幕府法+地主领袖非德川连续6月；幕方两路线另见下文；非君主invalid'),
'je_meiji_imperial_marriage':('公武合体按钮→ep2_meiji.3→婚姻JE；保存统治者、公主和条约scope','1825日内解除选中不利条约、闭关、非自由贸易、列岛无条约港→婚姻完成；失婚/逾期转公议舆论'),
'je_meiji_main':('meiji.1或ep2_meiji.9显式添加；没有开局possible自动铺开','12年；军制+经济+使团(ep2)/外交(无ep2)完成→meiji.2；到期有任一完成也给.2，否则.14'),
'je_meiji_economy':('改革事件先检测是否已达目标，未达才添加','不违约；超过70%的整合州同时有≥5级城市中心及铁路；完成+1并设flag'),
'je_meiji_army':('改革事件按军制条件添加；实际JE完成条件比事件跳过检查更细，应分别读','非农奴/农民征召变体，军队IG不在政府，拿破仑战争，军营不含无组织/武士训练；含非正规单位的陆军编队比例不能≥25%；完成meiji.3'),
'je_meiji_diplomacy':('仅无ep2改革支线','非传统主义、独立且recognized；完成+1并设flag'),
'je_iwakura_mission':('改革按钮→iwakura_mission.1选择团长→使团JE；法律和人物角色条件限制','返回且complete_iwakura_mission→.2；访问国/人物/学习量决定结果；不是固定历史团长'),
'je_shinbutsu_bunri':('ep2且维新结束+天皇复位；决议要求教团不强大、信仰自由','10个指定日本owner-state各神道≥60%→japan_religion.11；完全分离/国家无神论等失败'),
'je_elevate_buddhism':('ep2且维新结束但未天皇复位；教团不边缘、非完全分离/无神论；决议添加','原生目标完成且教团强大→japan_religion.12；教团边缘或世俗化失败'),
'je_taming_the_north':('ep2；JAP或特定EZO共和政体；有北海道；完全拥有+已整合+≥1城市','人口>50万、GDP>100万、农业潜力/耕地计数各≥3、建立殖民地标记→hokkaido_events.7；失去所有北海道→失败'),
'je_ryukyu_rivalry':('ep2国际情势；日本已非孤立/闭关，RYU/CHI存在；参与者及scope另行控制','得分≥40日本胜，≤-40中国胜；第三方宗主、中日附庸、任一关键国家消失等invalid'),
'je_colonize_korea':('ep2、JAP、非孤立；殖民机构≥1，非无殖民；完整直接拥有朝鲜5州','机构≥3、行政充足、公司/投资条件、所有朝鲜state整合、动乱<25%、日本文化≥5%→.2；失控/独立KOR等→.3；废殖民机构invalid'),
'je_zaibatsu':('ep2、JAP、非孤立/传统/行会；工业家非边缘，>2公司槽，≥2四大财阀，≥100持有等级且≥10%','巩固：已有财阀都繁荣、≥250级且≥25%；约束：合法性≥50、工业家离阁、选权或资本家政治力量条件、计划/合作制或份额<10%且无垄断；公司不足则invalid')}
w('| 原生JE | 入口/激活 | 完成、失败与退出 |\n|---|---|---|')
for key,(a,b) in summary.items():w(f'| {ref(key)} | {a} | {b} |')
w('')
w('维新“幕府胜利”另要求合法性≥75、无内战进度，维新运动若存在须支持<5%或激进度<50%。公武合体要求仍有幕府法、`japan_renewed_bakufu`、`japan_completed_imperial_marriage`；公议舆论要求德川地主领袖在政府、有选举权、大和家统治者。国家结束变量在complete/fail/invalid三路都写入，避免同一争夺重复出现。'+ref('je_meiji_restoration'))
w('')
w('天保议程不是单一GDP条：强硬四项为秘密警察、严格江户制度、小市民边缘、≥40水稻；改革四项为3个日本家园州≥3城市、宽松江户制度、小市民势力≥10%、非世袭官僚；共通四项为陆军投射>500、海军要塞≥10、家园无饥荒、达到事件设定GDP目标；总计≥8。强硬/宽松和小市民强弱互斥，不能把它当十二项全做。'+ref('tenpo_total_agenda_goals_completed'))
w('')
w('## 3. 从入口到底层的依赖闭包')
w('')
w('| 链条层 | 已核来源与作用 |\n|---|---|')
for a,b in [
('国家开局',cite('common/history/countries/jap - japan.txt',1)+' 启动科技、显式法律、警察机构1；ep2条件下添加天保/锁国；'+cite('common/history/characters/jap - japan.txt',1)+' 创建统治者、继承人、天皇与大名'),
('JE按钮',ref('je_meiji_restoration_proclaim_imperial_restoration')+'→ep2_meiji.5；'+ref('je_meiji_restoration_decide_shogunate_strategy')+'→.2或切换路线变量；'+ref('je_meiji_restoration_imperial_marriage')+'→.3'),
('7日延迟分支',ref('ep2_meiji.5')+'→.52(公武合体且合法性>50)或.51；'+ref('ep2_meiji.51')+'激活寡头法，按统治者/合法性再7日分.6或.7；'+ref('ep2_meiji.52')+'设置幕府更新标记'),
('法律与统治者',ref('law_bakufu')+'→'+ref('country_restore_japanese_emperor')+' / '+ref('country_generate_japanese_shogun')+'；退出幕府法不是仅换名称'),
('大名与GUI',ref('je_meiji_restoration_update_japanese_emperor')+'、'+ref('je_meiji_restoration_update_daimyos')+'更新角色列表；'+ref('country_calculate_and_cache_daimyo_loyalties_per_state')+'缓存州忠诚；'+cite('gui/journal_entry_widgets/ep2_japan_widgets.gui',1)+'呈现皇帝与大名列表'),
('内战开始',cite('common/on_actions/00_code_on_actions.txt',5502)+' country_has_pending_meiji_restoration→'+ref('meiji_civil_war_effects')+'按州归属转移大名、调整角色；其触发判断同时认active/inactive JE'),
('战争目标结算',cite('common/on_actions/00_code_on_actions.txt',6672)+'→'+ref('japan_reconcile_revolutionary_daimyos')+'→补缺大名和刷新列表'),
('继承与死亡',cite('common/on_actions/00_code_on_actions.txt',2817)+'、'+cite('common/on_actions/00_code_on_actions.txt',3083)+'→'+ref('character_japan_imperial_succession_chain_effect')+' / '+ref('character_japan_ruler_succession_chain_effect')+'；'+cite('common/on_actions/00_code_on_actions.txt',3112)+'→'+ref('on_new_ruler_japan_effect')),
('月/年脉冲',cite('common/on_actions/00_code_on_actions.txt',1561)+'、'+cite('common/on_actions/00_code_on_actions.txt',1836)+'接入日本王室；'+cite('common/on_actions/00_on_actions_yearly.txt',595)+'日本生活事件，:610地震；'+cite('common/on_actions/00_code_on_actions.txt',1581)+'日本IG改组事件'),
('制度层',ref('institution_police')+'每级动乱效果-10%；原版开局明确1级。'+ref('institution_colonial_affairs')+'与朝鲜殖民资格挂钩。'+ref('law_terakoya')+'直接教育可及性+25%、农民另+20%、科研-10%；它不在此块中显式设置学校机构等级'),
('宗教后置解锁',ref('shinbutsu_bunri_decision')+' / '+ref('elevate_buddhism_decision')+'→两宗教JE→japan_religion.11/.12；这是“主线已完+后续条件达成再生成JE”的完整原版实例'),
('公司与政治',ref('je_zaibatsu')+'→zaibatsu.1/.2→经济法修正案/IG/选举信心；'+cite('common/company_types/00_companies_japan.txt',1)+'公司数据库；选举信心月漂移由'+cite('common/on_actions/00_code_on_actions.txt',1535)+'统一处理')]:w('| '+a+' | '+b+' |')
w('')
w('以上已读到调用者、事件/按钮、脚本effect/trigger、法律/机构/角色数据库及JE界面引用。附属JSON保留完整重复节点和直接引用边；不声称对所有GUI动画/肖像贴图做视觉验收，也未解析引擎执行后的继承/内战结果。')
w('')
w('## 4. 中国、朝鲜、民主与军政的原版素材边界')
w('')
w('琉球的原版关系是日本的朝贡国，EZO是日本的vassal；不是日本完整直辖的两州。琉球竞争按钮分别使用宣示宗主权、当地港口投资≥2级、军事通行/造船投资与将军派驻、宗教尊崇等条件；中国也能操作，对手与琉球有延迟回应。可以借鉴“贸易/投资/军事顾问/宗教”四种外交资源，而不把它们改写成只有战争的单线。'+cite('common/history/diplomacy/00_subject_relationships.txt',644)+'；'+ref('je_ryukyu_rivalry_sway_merchants_button')+'；'+ref('je_ryukyu_rivalry_inspect_defenses_button')+'；'+ref('je_ryukyu_rivalry_honor_kikoeogimi_button'))
w('')
w('朝鲜有两套不同主线：其一是ep1东学运动，依韩国主文化、地理、技术、外国集团影响力与激进人口开启，派生请愿/起义，国际JE保存韩国君主、宗主和日本scope；政府胜利且日本参与、朝鲜仍为原宗主附属时，7日后日本获gg_korea.8交涉。其二是日本ep2在已经完整占有朝鲜五州后的殖民治理JE，要求殖民机构、投资、整合、低动乱与移民比重；它不是侵略朝鲜的开战按钮。'+ref('je_donghak_movement')+'；'+ref('je_gyojo_shinwon')+'；'+ref('je_korean_rebellion')+'；'+ref('je_colonize_korea'))
w('')
w('改革结算的军务奖励只在军制改革完成时可选，并添加朝鲜五州尚未持有部分的宣称；外交奖励需使团/外交改革，生产奖励需经济改革。它提供有条件的扩张倾向，未强迫对朝战争发生。'+ref('meiji.2'))
w('')
w('民主可用素材：原版兰学者在开放贸易和边境后改名知识分子、移除rangaku并获constitutionalism；财阀JE按有无选举权切换修正，约束财阀的民主选项给选举信心。通用`je_liberalism_1`先以democracy/international_trade技术显现，再要求政府中自由派/相应人物激活；完成需普选或财产普查选举、合法性≥50、和平且无叛乱IG，随后liberalism.1添加贸易/思想/移民支线。这是制度和政治力量共同驱动的入口模板。'+ref('japan_politics.1')+'；'+ref('je_zaibatsu')+'；'+ref('je_liberalism_1')+'；'+ref('liberalism.1'))
w('')
w('军政路线可用素材：山山县有authoritarian模板，陆军/军官政治力量受武士阶层法和幕府法影响，军制改革还可选择吸纳原武士或清退并制造军人激进派。通用法西斯JE需政治鼓动/大众宣传、社会主义威胁与≥10%激进人口，不能当作所有日本军事政府的同义词；其3年进度失败、胜利与后续警察/秘密警察/威权法巩固均有明确终局。'+ref('JAP_yamagata_aritomo')+'；'+ref('law_warrior_caste')+'；'+ref('meiji.3')+'；'+ref('je_fascism_1')+'；'+ref('je_fascism_2'))
w('')
w('## 5. 开局经济：实际历史输入')
w('')
w('原版国家定义是unrecognized、empire tier、日本主文化、江户身份体系，首都京都。国家历史显式加入15项法律：君主、幕府、信仰自由、农奴制、世袭官僚、臣民制、锁国、地方警察、土地税、出版审查、中等江户制度、闭关、寺子屋、武士阶层（共14项activate_law，见原文；不把未在本文件显式写出的默认法混入已核清单）。税级medium，警察机构1。'+ref('JAP')+'；'+cite('common/history/countries/jap - japan.txt',1))
w('')
w('科技基线函数本名虽然含tier_4，实际授予的是围地、工场、炼钢、竖井、蒸馏、勘探，及早期军事/官僚/民主/国际贸易等一组技术；日本另加学术、城市规划、中央集权、执法、殖民、养蚕。不能按函数名把它解读为“已研发第四时代所有科技”。'+ref('effect_starting_technology_tier_4_tech')+'；'+cite('common/history/countries/jap - japan.txt',3))
w('')
w('直接人口合计 **32,545,935**。以下资源数字为整个state_region数据库上限；北海道和琉球星号行只有部分province属于JAP，因此该行整州资源上限/耕地不能计作日本当下独占能力。九个完整州合计耕地805，煤66、铁100、铅200、硫121、林业106、渔业116。')
w('')
w('| 原版州 | JAP人口输入 | JAP/全州province数 | 全州耕地 | 煤/铁/铅/硫上限 | JAP历史建筑等级合计 | 来源 |\n|---|---:|---:|---:|---|---:|---|')
for st,e in d['economic_inputs'].items():
 p=sum(int(r['size']) for r in e['pops']);b=sum(r['ownership_levels'] for r in e.get('buildings',[]));caps={k:int(v) for q in e['resources']['capped'] for k,v in q.items()};own=e['state_history']['owners'];jp=sum(r['province_count'] for r in own if r['country']=='c:JAP');allp=sum(r['province_count'] for r in own);line=e['pops'][0]['line'];r=e['resources']
 w(f'| {st}'+('*' if len(own)>1 else '')+f' | {p:,} | {jp}/{allp} | {r["arable_land"]} | '+ '/'.join(str(caps.get('building_'+k+'_mine',0)) for k in ['coal','iron','lead','sulfur'])+f' | {b:g} | '+cite(e['pops'][0]['path'],line,'人口')+' / '+cite(r['path'],r['line'],'资源')+' / '+cite(e['state_history']['path'],e['state_history']['line'],'归属')+' |')
w('')
w('所有权来源计算方法：逐个create_building保留并累加add_ownership中的levels；不把每条记录当作1级。共141级，涵盖以下显式建筑；未计引擎根据人口/编队等建立的自给农场、城市中心、军营等自动内容。')
w('')
b=collections.Counter();groups=collections.defaultdict(list)
for st,e in d['economic_inputs'].items():
 for r in e.get('buildings',[]):b[r['building']]+=r['ownership_levels'];groups[r['building']].append((st,r))
w('| 建筑类型 | 历史等级 | 州分布 | 已激活PM（不同组合分别列） |\n|---|---:|---|---|')
for k,v in b.items():
 entries=groups[k];dis='；'.join(st.replace('STATE_','')+':'+str(int(r['ownership_levels'])) for st,r in entries);pms=sorted({', '.join(r['pms']) for _,r in entries});w('| '+cite(entries[0][1]['path'],entries[0][1]['line'],k)+f' | {v:g} | {dis} | '+ '<br>'.join(pms)+' |')
w('')
w('九州对完整原版JAP的边际输入：4,141,707人口、3/4港口、全部2级贸易中心、52/66个九个完整州煤矿上限；抽去九州后，直接人口剩28,404,228、历史建筑125级、港口1、贸易中心0，九个完整州组中的其余八州煤14。这个算术只表达原版输入差，不是NESND领土和人口的替代方案，亦不预测财政崩溃。')
w('')
w('初始显式工业很浅：没有历史创建煤矿、铁矿、钢厂、武器厂、军火厂、铁路、电厂；有1工具坊、4纺织、5食品、4玻璃、5纸、4家具、1造船。矿藏丰富不等于矿业已经就业或产出。上述“没有”限定本轮JAP历史create_building记录，不否定引擎的自动生成或后续建设。')
w('')
w('PM量纲例子：木架建造每满劳动力等级+2建造、耗25布75木；粗制工具每满劳动力等级耗30木产30工具；手缝衣耗40布产45衣；鲱鱼肥水稻耗10鱼产45粮（并受日本地理区域解锁）。它们是workforce_scaled系数，叠加PM、就业、吞吐、地方价格等才决定真实结果；不在此计算假GDP或假盈亏。'+ref('pm_wooden_buildings')+'；'+ref('pm_crude_tools')+'；'+ref('pm_handsewn_clothes')+'；'+ref('pm_herring_meal_farming_building_rice_farm'))
w('')
w('初始财富函数：基础11，上层+15、中层+7、劳工-2、农民-3；另调用奴隶重设。识字函数：基础0.35，官僚/学者/教士/工程师+0.5，上层+0.35，职员/店主+0.1，自给农业/牧业-0.1，未整合州再×0.5。原文件注释提及90%/75%/50%/30%，但实际代码分别为85%/70%/45%/25%基准，故报告以表达式为准；没有职业分配后的加权全国读数。'+ref('effect_starting_pop_wealth_medium')+'；'+ref('effect_starting_pop_literacy_middling'))
w('')
w('| 陆军编队 | 单位创建输入 | 计数 | 来源 |\n|---|---|---:|---|')
for r in d['formations']:w(f'| {r["name"]} | '+ '；'.join(u['state'].replace('s:STATE_','')+' '+u['count']+' 非正规步兵' for u in r['units'])+f' | {sum(int(u["count"]) for u in r["units"])} | '+cite(r['path'],r['line'])+' |')
w('')
w('共58非正规步兵，三个陆军均驻东北亚战略区；本JAP历史块未创建海军。这里不把58自动称为满编兵员、战斗力或可持续军费。军事PM默认分配需要引擎状态，历史编队块只证明单位类型与州输入。')
w('')
w('## 6. 人物：原版存在、生成条件与架空改编分开')
w('')
w('原版country_jap.txt共112个模板，包含两皇室备用随机模板；不等于1836已生成人数。历史人物块直接创建20人，另ep2条件加会泽正志斋1人。开局将军德川家齐、继承人家庆、天皇仁孝；7个IG首领、江川英龙/鸟居耀藏两将领及8个浮动大名。完整历史创建位置：'+cite('common/history/characters/jap - japan.txt',1)+'。')
w('')
w('下表列可供政治路线比较的模板。只说明原版游戏分配，不把该意识形态当作对真实历史人物的完整评判，更不据此宣布他们在丰臣世界线仍将出生、属于同一派别或按相同年份登场。表内“候选使用”是引擎模板池资格，非定时保证生成。')
w('')
selected=['JAP_ienari_tokugawa','JAP_ieyoshi_tokugawa','JAP_ninko_yamato','JAP_komei_yamato','JAP_meiji_yamato','JAP_taisho_yamato','JAP_showa_yamato','JAP_yoshinobu_tokugawa','JAP_yamagata_aritomo','JAP_ito_hirobumi','JAP_fukuzawa_yukichi','JAP_hara_takashi','JAP_saionji_kinmochi','JAP_katsura_taro','JAP_okuma_shigenobu','JAP_iwakura_tomomi','JAP_hamaguchi_osachi','JAP_yukio_ozaki','JAP_sakamoto_ryoma','JAP_nakae_chomin','JAP_kotoku_denjiro','JAP_sakai_toshihiko','JAP_kishida_toshiko','JAP_hiratsuka_raicho','JAP_yosano_akiko','JAP_suzuki_bunji','JAP_shibusawa_eiichi']
w('| 原版模板 | 出生日期输入 | IG/理念 | 候选使用或开局角色 |\n|---|---|---|---|')
for k in selected:
 r=rows[k];n=pdx.parse(r['source']).children[0];us=[]
 for child in n.children:
  if child.key and child.key.endswith('_usage'):
   us.append(child.key+': '+str(child.scalar('earliest_usage_date','?'))+'–'+str(child.scalar('latest_usage_date','?')))
 if not us:us=[('ruler' if n.scalar('ruler')=='yes' else 'heir' if n.scalar('heir')=='yes' else ','.join(x.value for x in n.all('role')) or '显式创建/继承链')]
 w(f'| {ref(k)} | {n.scalar("birth_date","—")} | {n.scalar("interest_group","—")} / {n.scalar("ideology","—")} | '+ '; '.join(us)+' |')
w('')
w('原版自然候选常见硬门槛是 `c:JAP ?= this` + `has_dlc_feature = ep2_content`，例如山县有朋1858–1922、原敬1882–1921、岸田俊子1882–1901（75概率）等。分裂后的非JAP tag不会自动共享这些候选；需要先决定人物存亡、家乡与教育网络，再在之后设计时处理，而非无条件复制112人。'+ref('JAP_yamagata_aritomo')+'；'+ref('JAP_hara_takashi')+'；'+ref('JAP_kishida_toshiko'))
w('')
w('## 7. 可借鉴的“后续按国情出现”模板')
w('')
w('| 形态 | 实际原版链 | 对后续设计的意义（推论） |\n|---|---|---|')
w('| 完成flag→决议资格→添加子JE | '+ref('je_meiji_restoration')+'→'+ref('shinbutsu_bunri_decision')+'→'+ref('je_shinbutsu_bunri')+' | 主线不必常驻；保留国家完成标记，后续法律/IG条件达到后再解锁。 |')
w('| 先检测是否已达目标 | '+cite('events/meiji_restoration.txt',133)+'→满足就设completed变量，否则添加经济JE | 路线不同的国家可以跳过已经完成的改革，避免强制重复任务。 |')
w('| 实际经济结构门槛 | '+ref('je_zaibatsu')+' | 公司数、持有份额、IG势力形成后才出现；统一与分裂国家不宜共用不经量纲调整的绝对100/250级阈值。 |')
w('| 主权/领土/城市组合门槛 | '+ref('je_taming_the_north')+' | 拥有部分州只显示前景，完全拥有、整合和城市化才进入开发。 |')
w('| 外部地区治理门槛 | '+ref('je_colonize_korea')+' | 区分征服前外交与征服后治理；部分占领、附属朝鲜和完全直辖需要不同资格。 |')
w('| 科技+执政力量门槛 | '+ref('je_liberalism_1')+' | 民主并非某年自动出现，而随技术与执政政治力量改变。 |')
w('')
w('这几种均有当前原版实例，但并不代表NESND应该复制原版数字、德川/天皇合法性前提或所有DLC限制。只读研究可确证脚本形状；接入架空三国后的scope、国家消失、领土失去、旧档继承与玩家AI行为仍需后续实现闭包和定向验收。')
w('')
w('## 8. 原版事件目录与直接调用索引')
w('')
w('日本专属的15个JE与124个事件均已保序采样；另收录通用政治与朝鲜参考，总计'+str(len(d['journal_entries']))+'个JE、'+str(len(d['events']))+'个事件、'+str(len(d['direct_reference_edges']))+'条直接引用边。以下按原文件列出日本事件ID；事件各自trigger/immediate/option/after完整内容与源行在JSON，不把事件池权重当作保证发生率。')
w('')
w('| 文件 | 事件（ID:起始行） |\n|---|---|')
evfiles=collections.defaultdict(list)
for r in d['events']:
 if '/japan_events/' in r['path'] or r['path']=='events/meiji_restoration.txt':evfiles[r['path']].append(r)
for rel,rs in evfiles.items():w('| '+cite(rel,1)+' | '+'；'.join(r['id']+':'+str(r['line']) for r in rs)+' |')
w('')
w('主链的逐条直接调用（展示JE/按钮/添加子JE与核心转场；全量见JSON）：')
w('')
w('| 调用者 | 边类型 | 目标 | 调用位置 |\n|---|---|---|')
core=set(summary)|{'ep2_meiji.5','ep2_meiji.51','ep2_meiji.52','ep2_meiji.6','ep2_meiji.7','ep2_meiji.8','ep2_meiji.9','meiji.1','meiji.2','meiji.3','meiji.14','shinbutsu_bunri_decision','elevate_buddhism_decision','je_iwakura_mission_button'}
for e in d['direct_reference_edges']:
 if e['caller'] in core and e['kind'] in ['event','add_je','button','progress_bar']:
  w('| `'+e['caller']+'` | '+e['kind']+' | `'+e['target']+'` | '+cite(e['path'],e['line'])+' |')
w('')
w('## 9. 来源指纹与边界')
w('')
w('GAME根目录：`'+G.as_posix()+'`。以下SHA-256来自本轮实际读取文件字节；不是下载文档摘要。原始目录只读。main报告与附属JSON写在WORK。本轮没有引擎运行、没有静态检查充当游戏验收、没有数值方案修改。未完整展开的范围：所有非日本全球制度的传递依赖、全部肖像资源渲染、UI实际点击、所有DLC组合实测、GDP/财政/市场与战争模拟。')
w('')
w('| 来源 | SHA-256 |\n|---|---|')
for s in d['sources']:
 rel=Path(s['path']).relative_to(G).as_posix();w('| '+cite(rel,1)+' | `'+s['sha256']+'` |')
report='\n'.join(out)+'\n'
# Counts are derived, correct wording before save.
report=report.replace('显式加入15项法律','显式加入14项法律')
(W/'native-japan.md').write_text(report,encoding='utf8')
print('report',len(report),'chars',len(out),'lines')
