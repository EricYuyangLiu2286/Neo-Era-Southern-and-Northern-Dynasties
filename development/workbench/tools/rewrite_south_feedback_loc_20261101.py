"""Author-style revisions; preserve localization API tokens, BOM and paired languages."""
from pathlib import Path
import json,re,hashlib
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');C=W/'exports/south-feedback-20261101-a';R=W/'reports/south-feedback-20261101'
zh={
'nesnd_south_succession_board_reason':'南朝的天下，究竟是朱氏皇帝的天下，还是郑氏开拓出来的天下？南京的诏书遍传诸邦，杭州的商船、税吏与兵舰也遍至诸邦。三百年来奉明正朔的名义与百余年来吴国经营海陆的功业，终于被摆到了同一张案上。\\n\\n襄樊大营奉朱氏正朔，四川士人仍在争论南府的新政；南洋总督与日本诸侯，则盘算着改朝换代将向他们索取多少钱粮、土地和兵员。各国的札子陆续送到南京与杭州。待到奉表称臣不再足以两全，今日的主张便要由各自的军队承担。',
'nesnd_south_succession_board_status':'各府正在遣使问讯、整饬营伍。南朝的争论已渐渐变成兵财的较量。',
'nesnd_board_table_heading':'诸国军政',
'nesnd_board_supply_known':'#v [Country.MakeScope.Var(\'nesnd_board_supply_score\').GetValue|0] / 4#!项',
'nesnd_board_supply_unknown':'商情未明',
'nesnd_board_stance_available_tt':'内战尚未爆发，本国不受固定立场约束，距上次改换立场已满#v 6个月#!。襄樊大营固定拥明；朝廷不能选择中立或自主。',
'nesnd_board_choose_ming_desc':'朱氏帝统历经诸侯分争，仍是南朝诸邦共同奉行的正朔。遣使南京，表明本国奉明的主张。',
'nesnd_board_choose_wu_desc':'郑氏经营海陆、掌握军财已久。遣使杭州，支持吴王以今日的功业改定天下的名位。',
'nesnd_board_choose_neutral_desc':'南京与杭州各有主张，本国的军队暂且留守境内，商旅仍照旧往来。',
'nesnd_board_choose_autonomy_desc':'朝廷将议改制，本国也当自掌财赋、官员与防务。以此向两方陈明条件。',
'nesnd_board_stance_effect_tt':'公开本国立场，#v 6个月#!内不再更改。撤回既有盟书时，尚未执行的并省或割地承诺一并作废，与中央关系#n −15#!。',
'nesnd_south_retry_confrontation_desc':'前次交涉未成，各府仍据地拥兵。再次召集使者，要求反对诸国作出答复。',
'nesnd_south_ready_unknown':'军政情形尚未报齐。',
'nesnd_board_compact_bar_desc':'诸府承诺：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1] / 100#!',
'nesnd_south_politics_summary':'#bold 南京与杭州#!\\n财政与行政 #v [GetGlobalVariable(\'nesnd_south_finance\').GetValue|1]/20#!　朝臣合作 #v [GetGlobalVariable(\'nesnd_south_domestic\').GetValue|1]/20#!\\n朱氏统绪 #v 20#!　吴方军力 #v [GetGlobalVariable(\'nesnd_south_military\').GetValue|1]/20#!\\n#bold 诸府盟书#!　奉明 #v [GetGlobalVariable(\'nesnd_south_ming_accord\').GetValue|1]%#!　拥吴 #v [GetGlobalVariable(\'nesnd_south_wu_accord\').GetValue|1]%#!\\n盟约连续履行 #v [GetGlobalVariable(\'nesnd_south_peace_months\').GetValue|0]/12#!个月。\\n\\n$nesnd_south_compact_detail_tt$',
'nesnd_south_compact_detail_tt':'#bold 诸府盟约#!\\n大陆、海外与日本诸邦的承诺分别占#v 50%、30%、20%#!。盟书有效#v 36个月#!；改换立场、交战、改投宗主或撤约后，相应承诺失效。\\n\\n#bold 以盟约定天下#!\\n所选一方的政治支持须达到#v 85#!，领先另一方#v 20#!，并连续履约#v 12个月#!。明廷须获#v 75%#!盟书及至少两个大陆核心邦国签署；吴方须获#v 80%#!盟书、拟并省诸国与日本割地各方同意，并备有合格舰队。已达成和解，朝争便告结束。',
'nesnd_south_qin_departed_tt':'郑钦已去世或离开本国，或朝争已延续至#v 1839年#!。',
'nesnd_chen_case_concluded_tt':'首辅案已经结案，或陈东阳已不在本国；遇刺死亡的后续事件须先完成。',
'nesnd_south_pressure_detail_tt':'#bold 易代压力#!：#v [Country.MakeScope.ScriptValue(\'nesnd_south_pressure_value\')|1] / 100#!\\n当前每月净变化：#v [Country.MakeScope.ScriptValue(\'nesnd_south_monthly_pressure_value\')|1]#!。通常每月#n ＋3#!，邦国契约修正生效时#n ＋2.5#!；有效和解进程另每月减少#p 3#!。\\n\\n#bold 首辅案#!\\n自#v 1837年7月#!起，压力超过#v 24#!时可能发生；至#v 1838年初#!，尚未结案且陈东阳仍在本国，就会进入刺杀与护卫分支。死亡使压力#n ＋25#!，受伤#n ＋10#!，脱险#n ＋3#!。\\n\\n案件结算后，压力达到#v 70#!可主动提前易代；达到#v 100#!且郑钦已离去，自动推进。至#v 1839年初#!仍未解决的朝争会达到#v 100#!，不再等待郑钦自然死亡，继而进入易代、诸国答复与内战交涉。已经达成的和平结局不受影响。',
'nesnd_south_status_qin':'吴王仍在约束近臣的易代之议，南京与杭州的争论却一日紧过一日。\\n#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_south_rules 朝争进展#!#!',
'nesnd_south_status_succession':'南府的易代之议已不能再拖。首辅案结算、压力达到#v 100#!后，诏书将送往各府，等待诸国答复。\\n#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_south_rules 朝争进展#!#!',
'nesnd_supply_preparations':'脆弱的贸易',
'nesnd_supply_preparations_reason':'吴人的海船把南洋的稻米、远方的木材和各国的货物运进南朝，内陆的工坊、营伍与学堂也早已依赖这些往来。旧日各府可以据地自守，今日停下一处港口、扣住一批货物，损失便会沿着商路传到许多人的家中。\\n\\n南京与杭州争论帝统的时候，商人同样在衡量自己的前程。[ROOT.GetCountry.GetName]的官署需要纸张，军队需要粮饷与军械，工坊中的人需要靠工钱生活。我们当与愿意往来的诸邦重续交游，也须让本国的生产支撑起这些生计。商路能否经受朝争，将决定我们届时有多少余力。',
'nesnd_supply_hus_preparations_reason':'共和国的沿海城镇因移民与商船而兴盛。反抗吴人的战争使东洲诸邦走到一起，北朝的盟约又为我们的货物打开了新的销路。港口中的装卸、工坊中的生产和各州的赋税，已经随着这些往来紧紧相连。\\n\\n如今南朝争位的消息越海而来。商人要打听货源，船主忧心航路，工人仍等着每周的工钱。无论继续经营共同市场，还是由共和国另定通商安排，我们都须先稳住自己的生产与生计。',
'nesnd_supply_status_war':'#n 战火已波及商路。#!军需征发与航运受阻，先前的安定未能延续。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_inputs':'#n 工坊与营伍所需的货物供给不济。#!纸张、工具与军械的价钱正在牵动各处开支。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs':'#n 工坊与官署尚缺人手。#!现有职位仍须招足工人，才能维持生产与日常事务。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_hna':'#n 营伍与学堂尚缺人手。#!襄樊的军营须补足兵额，大学也要延揽足够的教员与职员。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_sih':'#n 川中工场尚缺人手。#!工具厂及供应铁料或木材的产业，还不能维持应有的生产。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_gng':'#n 林场与纸厂尚缺人手。#!广西的木材与纸张要运往各处，先须让这些厂场正常开工。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_hus':'#n 港口与官署尚缺人手。#!共和国的船货需要装卸，各州的税赋与公事也不能无人办理。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_livelihood':'#n 各州的生计仍未安定。#!失业者难以谋生，粮价与饥馑也在拖累商贸往来。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_diplomacy':'各方商路尚待议定。可以遣使联络邻邦，也可以交由本国商帮筹措。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_stable':'#p 货源、工场与民生渐趋安定。#!若能维持一季，我们便有把握将这些往来长久经营下去。\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_bankruptcy':'#n 国库已经破产。#!官署须重整财政，商路的安定也要重新积累。\\n$nesnd_supply_rules_link$',
'nesnd_supply_readiness_bar':'通商根基',
'nesnd_supply_continuity_bar':'商路安定周数',
'nesnd_supply_self':'依靠本国商帮',
'nesnd_supply_self_desc':'请本国商人自行安排采购，召回此前遣出的使者。',
'nesnd_supply_end_contact_desc':'召回驻外使者，另寻能够长久往来的商路。',
'nesnd_supply_end_contact_tt':'结束此次联络，连续安定周数归零；已经签署的正式条约仍依约履行。',
'nesnd_supply_trade_desc':'把两国商人的往来写入盟约，互予贸易优惠。',
'nesnd_supply_trade_request_tt':'#v 7日#!后向对方提出互惠贸易条约，约束期#v 2年#!；对方可接受或拒绝。',
'nesnd_supply_accept_tt':'建立通商联络，双方关系#p ＋10#!。商人仍通过各自市场与航路买卖货物。',
'nesnd_supply_finish':'商路渐稳',
'nesnd_supply_finish_desc':'货源、工场、民生与通商安排连续安定#v 12周#!后，首次获得持续#v 2年#!的通商收益。',
'nesnd_supply_dismiss':'暂缓经营',
'nesnd_supply_dismiss_desc':'先收回使团，日后再议商路。既有派使开支仍须支付至期满。',
'nesnd_supply_verified':'商路渐通',
'nesnd_supply_resume':'重续商路',
'nesnd_supply_resume_desc':'重新联络商人，整顿货源与雇工，恢复与各邦的往来。',
'nesnd_supply_finish_shared_desc':'继续在共同市场中经营，保留既有盟约。货源与生计连续安定#v 12周#!，首次获得#v 2年#!通商收益。',
'nesnd_supply_finish_autonomous':'自掌商路',
'nesnd_supply_finish_autonomous_desc':'由本国掌管市场，安排对外通商。各项条件连续维持#v 12周#!，首次获得#v 2年#!通商收益。',
'nesnd_supply.3.d':'过去一季，[ROOT.GetCountry.GetName]的工坊与营伍有货可购，学堂、官署和厂场也逐渐补齐了人手。商人重新熟悉了往来的门路，各州的人们得以靠生产与买卖维持生活。\\n\\n海内外的朝争还在继续。那些装着货物驶离码头的船只，为我们留下了继续经营的本钱。',
'nesnd_supply_rules_link':'#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_supply_rules 货源与生计#!#!',
'nesnd_supply_rules':'#bold 货源#!\\n纸张、工具、小武器无本国短缺，价格涨幅不超过#v 50%#!；东洲另需硬木。\\n\\n#bold 工场与人手#!\\n所需建筑各有至少一座雇员达到#v 75%#!，且不缺生产投入。湖广为大学与军营；四川为工具厂，以及铁矿或伐木场；广西为纸厂与伐木场；东洲为港口与官署。招工困难时可查看[concept_pop_qualifications]、[concept_building_wage]与原料供应。\\n\\n#bold 生计#!\\n全国无业劳动力不超过#v 12%#!；劳动力至少#v 5万#!的州不超过#v 20%#!。自给农民属于有业人口。全国无饥荒，粮食无本国短缺且涨价不超过#v 25%#!。\\n现有无业劳动力：#v [Country.MakeScope.Var(\'nesnd_supply_unemployed\').GetValue|0] / [Country.MakeScope.Var(\'nesnd_supply_workforce\').GetValue|0]#!（#v [Country.MakeScope.Var(\'nesnd_supply_unemployment\').GetValue|%1]#!）；超过地方失业界线的州：#v [Country.MakeScope.Var(\'nesnd_supply_critical_states\').GetValue|0]#!。\\n\\n#bold 商路安定#!\\n确定联络伙伴或依靠本国商帮，四项条件连续维持#v 12周#!。战争、破产、市场改变或任一条件不满足，连续周数重新计算。',
}
en={
'nesnd_supply_preparations':'Fragile Trade',
'nesnd_south_succession_board_reason':'Does the southern realm belong to the Zhu emperors, or to the Zheng rulers whose fleets and armies have carried it across the seas? Edicts travel from Nanjing to the same countries reached by Hangzhou’s merchants, tax collectors and warships. Centuries of Ming legitimacy now stand against the achievements and resources of Wu.\\n\\nXiangfan remains loyal to the Ming. Sichuan debates the reforms of the Southern Court, while overseas governors and Japanese lords consider the money, land and troops a new dynasty might demand. Their answers will soon have to be sustained by their own forces.',
'nesnd_south_succession_board_status':'The provinces exchange envoys and prepare their forces. The dispute over the dynasty increasingly turns upon money and arms.',
'nesnd_board_table_heading':'The Southern Countries',
'nesnd_board_stance_available_tt':'The civil war has not begun and the six-month stance cooldown has ended. Xiangfan is committed to the Ming; the central court cannot choose neutrality or autonomy.',
'nesnd_south_qin_departed_tt':'Zheng Qin has died or left the country, or the crisis has reached #v 1839#!.',
'nesnd_chen_case_concluded_tt':'The attempt on Chen has been resolved, or he is no longer in this country; a pending death event must finish first.',
'nesnd_south_pressure_detail_tt':'#bold Succession pressure#!: #v [Country.MakeScope.ScriptValue(\'nesnd_south_pressure_value\')|1] / 100#!\\nCurrent monthly net change: #v [Country.MakeScope.ScriptValue(\'nesnd_south_monthly_pressure_value\')|1]#!. Base growth is #n +3#!, or #n +2.5#! under the Federal Compact modifier. Valid reconciliation separately subtracts #p 3#!.\\n\\nThe attempt on Chen can occur from #v July 1837#! above #v 24#! pressure, and is initiated by #v early 1838#! if still unresolved and Chen is present. Death adds #n 25#!, wounding #n 10#!, and escape #n 3#!.\\n\\nAfter the case, early accession is available at #v 70#! pressure. Automatic accession requires #v 100#! and Zheng Qin’s departure, or the #v early-1839#! crisis deadline. An unresolved crisis reaches #v 100#! at that deadline and proceeds to accession, provincial replies and confrontation. Completed peaceful settlements are preserved.',
'nesnd_south_status_qin':'The Prince of Wu still restrains his advisers, but the dispute between Nanjing and Hangzhou grows sharper.\\n#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_south_rules The succession dispute#!#!',
'nesnd_south_status_succession':'The dispute can no longer be deferred. Once Chen’s case is resolved and pressure reaches #v 100#!, the accession edict will be sent to the provinces.\\n#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_south_rules The succession dispute#!#!',
'nesnd_supply_preparations_reason':'Wu’s ships carry grain and raw materials between distant ports. The workshops, garrisons and schools of the southern countries have come to depend on that traffic. A closed harbour or a detained cargo can now take livelihoods away far beyond its own shores.\\n\\nWhile Nanjing and Hangzhou dispute the dynasty, merchants consider their own future. [ROOT.GetCountry.GetName] needs paper for its offices, supplies for its soldiers and employment for its people. We must renew our trading connections and sustain the production at home that gives us room to act.',
'nesnd_supply_hus_preparations_reason':'Immigrants and merchant ships built the republic’s coastal towns. War against Wu brought its states together; the northern alliance opened further markets. Work in the harbours, production in the mills and provincial revenue now depend upon these connections.\\n\\nNews of the southern dispute crosses the ocean. Whether we continue in the shared market or arrange our own trade, production and livelihoods at home must endure.',
'nesnd_supply_status_war':'#n War has reached the trading routes.#! Requisitions and disrupted shipping have broken the previous period of stability.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_inputs':'#n Workshops and garrisons lack reliable supplies.#! Paper, tools and arms are straining their budgets.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs':'#n Workshops and offices still lack workers.#! More posts must be filled to sustain their business.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_hna':'#n The garrisons and schools lack personnel.#! Xiangfan must fill its barracks and university posts.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_sih':'#n Sichuan’s workshops lack workers.#! The tooling industry and its iron or timber suppliers cannot yet maintain production.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_gng':'#n Logging camps and paper mills lack workers.#! Guangxi must put these establishments into regular operation.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_jobs_hus':'#n Ports and offices lack personnel.#! The republic needs both cargo handlers and staffed administrations.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_livelihood':'#n Livelihoods remain insecure.#! Unemployment, grain prices and famine threaten commercial life.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_diplomacy':'Trading arrangements remain undecided. Send envoys abroad or rely on merchants at home.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_stable':'#p Supplies, employment and livelihoods are becoming stable.#! Sustain them for a season to establish lasting trade.\\n$nesnd_supply_rules_link$',
'nesnd_supply_status_bankruptcy':'#n The treasury is bankrupt.#! Finances must recover before a new period of stability can be established.\\n$nesnd_supply_rules_link$',
'nesnd_supply_rules_link':'#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_supply_rules Supplies and livelihoods#!#!',
'nesnd_supply_readiness_bar':'Foundations of trade',
'nesnd_supply_continuity_bar':'Weeks of stable trade',
}
# Update existing authoritative and historical generated definitions consistently;
# missing keys get one explicit override in each language.
def update(lang,values):
 seen=set();changes=[]
 for p in sorted((C/'localization'/lang).rglob('*.yml')):
  s=p.read_text('utf-8-sig');original=s
  for key,value in values.items():
   pattern=r'(?m)^(\s*'+re.escape(key)+r':\d*\s+)"[^\n]*"\s*$'
   if re.search(pattern,s):
    assert '"' not in value,key
    s=re.sub(pattern,lambda m:m.group(1)+'"'+value+'"',s);seen.add(key)
  if s!=original:
   raw=p.read_bytes();p.write_bytes(b'\xef\xbb\xbf'+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'));changes.append(str(p.relative_to(C)))
 missing={k:v for k,v in values.items() if k not in seen}
 if missing:
  p=C/'localization'/lang/'replace'/('zzzzzzzzz_nesnd_south_feedback_l_'+lang+'.yml')
  p.write_text('l_'+lang+':\n'+''.join(' '+k+':0 "'+v+'"\n' for k,v in missing.items()),encoding='utf-8-sig');changes.append(str(p.relative_to(C)))
 return changes
changed=update('simp_chinese',zh)+update('english',en)
original=W/'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml'
lines=original.read_text('utf-8-sig').splitlines();samples=[x for x in lines if re.match(r'\s*(ce_usm_conflicts_within_reason|flavorUSM\.4\.d):',x)]
evidence={'author_source':str(original),'author_source_sha256':hashlib.sha256(original.read_bytes()).hexdigest(),'samples':samples,'before_candidate':'button-guards-20261101-a / current main 49fed23','revised':{k:zh[k] for k in ['nesnd_south_succession_board_reason','nesnd_south_succession_board_status','nesnd_supply_preparations_reason','nesnd_supply_status_jobs_hna']},'decision':'Keep historical political argument and concrete groups in prose; exact thresholds stay in tooltips. Country-specific staffing status replaces cross-country debugging instructions.','changed':changed}
(R/'prose-review.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'localization_files':len(changed),'chinese_keys':len(zh),'english_keys':len(en)},ensure_ascii=False))
