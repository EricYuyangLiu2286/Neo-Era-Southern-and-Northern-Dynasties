from pathlib import Path
import json,re,hashlib

W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
C=W/'exports/japan-development-20261102-a'
R=W/'reports/canon-prose-20261102'
B=W/'backups/pre-update-20261030T233944Z/mod'
proposals={}
def parse(p):
    return [(m.group(1),m.group(2),n) for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1) if (m:=re.match(r'^\s*([^ #:\n]+):(?:\d+)?\s*"(.*)"\s*$',line))]
files=[]
def pair(root,stem,sub='replace'):
    for lang in ('simp_chinese','english'):
        p=root/'localization'/lang/sub/(stem+'_l_'+lang+'.yml')
        if p.exists(): files.append((p,lang))
pair(C,'zzzzzz_nesnd_jp_development')
for stem in ['zzzzzzz_nesnd_qin_persia','nesnd_japan','nesnd_japan_lin_regency','zz_nesnd_geography','zz_nesnd_national_map','zz_nesnd_map_refinement','zz_nesnd_hainan','zz_nesnd_south_central_vietnam','zz_nesnd_south_dayuan','zzzz_nesnd_subsistence_modifier_labels','zzzzz_nesnd_random_given_names','zz_nesnd_engine_compat','zz_nesnd_existing_modifier_labels','zzzzzzzz_nesnd_vanilla_concept_compat','zzzzzz_nesnd_concept_clarity']:
    pair(M,stem)
for stem in ['nesnd_phi_finance','nesnd_tenasserim','nesnd_editor','nesnd_character_notifications']:
    pair(M,stem,'')
pair(M,'zzzzzzzz_nesnd_poland_integrity')
data={}; occurrences={}
for p,lang in sorted(files,key=lambda item:('replace' in item[0].parts,item[0].name)):
    for k,v,n in parse(p):
        data.setdefault(k,{})['zh' if lang=='simp_chinese' else 'en']=v
        occurrences.setdefault(k,[]).append({'path':str(p),'line':n,'language':lang,'original_value':v})
# Development overrides are the effective C values, even where legacy files follow them in the inventory.
for lang in ('simp_chinese','english'):
    p=C/'localization'/lang/'replace'/('zzzzzz_nesnd_jp_development_l_'+lang+'.yml')
    for k,v,n in parse(p): data.setdefault(k,{})['zh' if lang=='simp_chinese' else 'en']=v
polish_cn=M/'localization/simp_chinese/replace/ce_poland_l_simp_chinese.yml'
for k,v,n in parse(polish_cn):
    if k.startswith('ce_polish_script_bar_tt_') and k in data:
        data[k]['zh']=v
        occurrences.setdefault(k,[]).append({'path':str(polish_cn),'line':n,'language':'simp_chinese','original_value':v,'partial_source_read':True})
def add(k,zh=None,en=None,reason='',source='',mechanic='',apply='E_and_C',new=False):
    old=data.get(k,{})
    proposals[k]={'zh':old.get('zh','') if zh is None else zh,'en':old.get('en','') if en is None else en,'reason':reason,'source':source,'mechanic':mechanic,'apply_to':apply,'new_key':new}

add('nesnd_japan.1.d', '南京使节带来了新的分封方案：京都与大阪奉天皇名位，由摄政主持政务；德川以江户为府，丰臣退守关西，九州和四国则归吴朝直辖。丰臣借唐土之力建立的霸业，如今面临唐土朝廷提出的分割。家臣已呈上各地兵力与军粮，等候[ROOT.GetCountry.GetRuler.GetFullName]决定如何答复。', 'Envoys from Nanjing have brought new terms. Kyoto and Osaka would recognize the Emperor, with a regent conducting the government; the Tokugawa would rule from Edo, the Toyotomi would retain a reduced western domain, and Wu would administer Kyushu and Shikoku directly. The mainland court whose armies helped establish Toyotomi power now proposes to divide it. Retainers have reported the strength and supplies of the garrisons to [ROOT.GetCountry.GetRuler.GetFullName], who must decide how to answer.',reason='天皇亲政与林摄政冲突；删去分封册的道具式收束，保留谈判局势与现有ruler引用。',source='Author latest JIM/Lin correction; C/events/nesnd_japan_events.txt:2; C/common/scripted_effects/nesnd_jp_imperial_court.txt',mechanic='Partition proposal, not completed partition. Existing ROOT ruler token retained.',apply='C_only')
add('nesnd_japan.3.d','日本的分封已经施行。丰臣保有关西余部与中国地区，德川接掌江户及北方领地；京都与大阪奉天皇名位，由摄政主持和国政务。九州、四国归吴朝直辖。各政权接管辖地的税赋与军队，原由丰臣统一调度的兵力和财源从此分属数家。','The settlement in Japan is in force. The Toyotomi retain Chugoku and the remainder of Kansai; the Tokugawa take Edo and the northern domains. Kyoto and Osaka recognize the Emperor, with a regent conducting Wa’s government. Wu administers Kyushu and Shikoku directly. The new governments take charge of local revenues and armies, dividing the resources once commanded by the Toyotomi.',reason='天皇亲理政务与已确认摄政制度冲突；各府为日本军政政权用语合法，无需全局改省。',source='Author latest JIM/Lin correction; C/events/nesnd_japan_events.txt:80',mechanic='Only valid with new C partition/regency behavior.',apply='C_only')
add('nesnd_japan.5.d','本州各地终于归于同一个独立政府。[ROOT.GetCountry.GetName]开始接管旧诸侯的赋税与军队，使彼此分立的领地遵行共同的法令。城下町的商人也在等待关卡和赋役的重新议定，准备把生意做到旧日领界之外。','Honshu now answers to one independent government. [ROOT.GetCountry.GetName] is bringing the revenues and armies of the former domains under common authority. Merchants in the castle towns await a settlement of tolls and taxes as they prepare to trade beyond the old domain boundaries.',reason='新C日志只需本州七地区；旧事件断言九州四国已统一。E仍九地区要求，禁止把该改稿提前套入E。',source='C/common/journal_entries/nesnd_japan.txt:64; C/common/scripted_triggers/nesnd_japan.txt:237; C/events/nesnd_japan_events.txt:98',mechanic='Seven Honshu regions + independence; no Kyushu/Shikoku ownership guarantee.',apply='C_only')
add('nesnd_japan_war_tt', '日本若为吴朝属国，将脱离吴朝并进入[concept_diplomatic_play]。吴朝主张重组日本，日本则要求羞辱吴朝。#v 重组日本的战争目标获执行后，才会划分领土。#!', 'If Japan is a Wu subject, it will become independent as the [concept_diplomatic_play] begins. Wu demands the reorganization of Japan; Japan demands Wu’s humiliation. #v The territorial settlement takes effect only if Wu’s war goal is enforced.#!',reason='真实/real是开发验证口吻；保留独立、双方战目标及领土执行条件。',source='M/common/scripted_effects/nesnd_japan.txt; M/common/war_goal_types/nesnd_japan.txt',mechanic='No change to truce, relationship or war goal.',apply='E_and_C')
add('nesnd_wu_eastern_question_reason','丰臣氏借明吴之力平定战国，又与郑氏共争朝鲜。两家的旧盟维持了海东秩序，也使九州驻军与日本诸侯结下了绵延数代的利害。如今南朝大局已定，朝廷开始议论东征：将西军旧部调往海东，在丰臣之外扶植天皇与德川的政权，使三家各领其土，九州、四国则归吴朝直辖。远洋驻军与海上商路，也将随这次分封重新安排。','The Toyotomi unified Japan with Ming and Wu assistance and fought beside the Zheng in Korea. Their old alliance bound the garrisons in Kyushu to the interests of Japan’s lords. With affairs in the south settled, the court is considering an expedition: send former western officers overseas and establish imperial and Tokugawa governments alongside the Toyotomi, while placing Kyushu and Shikoku under direct Wu administration. The settlement would also reshape overseas garrisons and maritime trade.',reason='原中文只提天皇/德川分掌，遗漏仍保留的丰臣政权；三方分封符合E/C共同效果，不宣布天皇亲政或提前写入C摄政。',source='M/common/scripted_effects/nesnd_japan.txt; C/common/scripted_effects/nesnd_japan.txt',mechanic='Three Japanese governments plus direct Wu holdings; regency identity not asserted in this shared JE.')
add('nesnd_japan.2.d','日本使者请求撤回分封方案，仍由丰臣统一主持海东政务。南京朝廷准备以东征扶植新的日本政权，把丰臣掌握的兵力与财源分到数家。军费、舰船与海外防务也须随之重新安排。如何答复这项请求，已交由[ROOT.GetCountry.GetRuler.GetFullName]裁定。','Japan asks the court to withdraw the partition proposal and retain a unified Toyotomi government. The proposed expedition would establish new Japanese governments and divide the forces and revenues now commanded by the Toyotomi. It would also require new arrangements for military spending, shipping and overseas defence. The decision rests with [ROOT.GetCountry.GetRuler.GetFullName].',reason='原文无条件声称南京控制九州驻军，但分封允许保留外国领土且不保证吴当前控制九州；以真实提议替代无守卫持地断言。',source='M/events/nesnd_japan_events.txt:32; M/common/scripted_triggers/nesnd_japan.txt',mechanic='Fallback negotiation event; existing ROOT ruler token retained. No new direct possession asserted.')
add('nesnd_jp_food_supply_reason','田间的收成、渔人的船和往来的粮商，维持着城里的生活。粮价一涨，街市上的怨声便传到官署。政府须让运粮的人愿意进城，也让城里的人买得起饭。','Harvests, fishing boats and grain merchants sustain life in the towns. When food prices rise, complaints from the markets soon reach the authorities. The government must keep food coming into the towns at prices their people can afford.',reason='原句把粮价危机写成官署争论传到街市，因果和行动主体含混。',source='C/common/scripted_triggers/nesnd_jp_industry.txt:61; author flavorCNE.3.d',mechanic='Food supply allows farming OR affordable grain; no invented self-sufficiency requirement.',apply='C_only')
add('nesnd_jp_food_processing_reason','城镇需要能够储存和远运的食品，粮商与渔商也在寻找收获季节以外的买主。罐藏技术让他们有机会把收购、加工和运输连成一门生意；办起食品工场，还能让雇工不必随收获季节结束而失去工作。','The towns need food that can be stored and carried over long distances. Grain and fish merchants want customers beyond the harvest season. Canning offers a way to combine purchasing, processing and transport in one business, while food factories could provide work after the harvest is over.',reason='常驻待完成日志尚未保证已研发罐藏；由已实现事实改为待建产业及技术用途。',source='C/common/scripted_triggers/nesnd_jp_industry.txt:76',mechanic='Technology canneries and active cannery PM are completion requirements, not entry requirements.',apply='C_only')
add('nesnd_jp_development.2.d_military','主张集权的军官终于让自己的办法成为国策。征募、训练和军需被纳入统一调度，地方官员也须执行中央的命令。兵工厂与工具厂为扩充后的军队提供装备，军府由此取得了在各地贯彻政令的力量。','The officers have secured the centralized government they sought. Recruitment, training and supplies come under common direction, and local officials must carry out the government’s orders. Arsenals and tool workshops equip the expanded army, giving the military administration the means to enforce its policy in the provinces.',reason='原段最后泛论军费/军官权力将长久争议，凭空补反对者与代价收束；完成条件足以陈述实际军政结果。',source='C/common/scripted_triggers/nesnd_jp_politics.txt:28; author flavorCNE.3.d',mechanic='Appointed bureaucracy; autocracy/oligarchy; army/building thresholds. Does not invent elections or force different governance law.',apply='C_only')
add('nesnd_jp_foreign.2.d', en='Our envoy has returned from [SCOPE.sCountry(\'jp_partner\').GetNameNoFormatting] with an agreement. Their government has accepted the proposal.',reason='原英文the agreed arrangements will govern the matter是空泛抽象收尾；保留无kind时的中性回退。',source='C/events/nesnd_jp_foreign.txt:31',mechanic='Fallback only. Kind-specific variants need saved reply kind before request cleanup.',apply='C_only')
reply={
1:('宗主已同意放宽对本国的约束，原有的宗属关系升为更自主的等级。双方议定休兵五年，政府可以据此着手处理此前受制的事务。','Our overlord has agreed to loosen its control, granting us a more autonomous status. The two governments have established a five-year truce.'),
2:('[SCOPE.sCountry(\'jp_partner\').GetNameNoFormatting]已经承认本国独立。宗属关系就此解除，双方议定休兵五年；今后的内外事务，将由本国政府自行决定。','[SCOPE.sCountry(\'jp_partner\').GetNameNoFormatting] has recognized our independence. The subject relationship is dissolved, and a five-year truce now stands between us. Our government will conduct its own domestic and foreign affairs.'),
3:('宗主同意本国推行新政。政府可以开始筹划任官、军政与议政制度的改革，原有的宗属关系仍然保留。','Our overlord has given its assent to domestic reform. The government may pursue changes to public appointments, military administration and representation while the subject relationship remains in force.'),
4:('[SCOPE.sCountry(\'jp_partner\').GetNameNoFormatting]同意拨给建设资金。工场扩建与工匠训练有了新的助力；政府须善用这笔资助，三年内不能再获同类拨款。','[SCOPE.sCountry(\'jp_partner\').GetNameNoFormatting] has provided development funds. The grant will support construction and the training of skilled workers. Further funding of this kind will be unavailable for three years.'),
5:('对方接受了朝鲜和解方案。本国对釜山与两湖的宣称已经撤回，两地尚在本国掌握中的领土也已依约移交朝鲜。海峡两岸的关系将依新的边界继续经营。','The Korean settlement has been accepted. Our claims to Busan and Yangho have been withdrawn, and any territory we still held there has passed to Korea. Future relations across the strait will proceed within these borders.'),
7:('宗主允许本国与其他日本属国商议合邦。使者可以带着这份许可前去交涉，受邀国家仍须自行同意归并。','Our overlord has authorized negotiations for union with the other Japanese subjects. Our envoys may now approach them, though each invited government must still consent to the union.')}
for kind,(zh,en) in reply.items():
    add(f'nesnd_jp_foreign.2.d{kind}',zh,en,reason='按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。',source='C/common/scripted_effects/nesnd_jp_foreign.txt:75',mechanic=f'Kind {kind}. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.',apply='C_only_requires_branch',new=True)
add('nesnd_qe1_ruler_delta','君主的倾向',None,reason='秦王是固定王号，与本系统陈秦皇帝和可变国体不一致；本项仅君主路线贡献非零。',source='M/common/scripted_effects/nesnd_qe1_agendas.txt:20',mechanic='nesnd_qe1_assign_ruler clears the two preference variables outside monarchy; neutral label avoids false rank.')
add('nesnd_qe1.1.d','安国派的主张成为朝廷施政的方向。支持改制的士人与工商业者声望日隆，军府及其市民拥护者则失去了原有的政治优势。恢复生产与改造旧法，将成为新政府争取人心的凭借。','The reformers have set the government’s course. Scholars and industrialists who supported reform have gained political influence, while the army and its supporters among the urban middle classes have lost ground. The new government looks to economic recovery and legal reform to win public support.',reason='原文“军士与武勋门阀”把实际受损小市民误写成勋贵地主；按armed_forces+petty_bourgeoisie降低、intelligentsia+industrialists增加修正行动者。',source='M/common/static_modifiers/nesnd_qe1_agendas.txt:3; M/common/scripted_effects/nesnd_qe1_agendas.txt:75',mechanic='Only IG strength/attraction modifiers and SoL-loyalty observation, no forced office/law change.')
add('nesnd_qe1_economy_push_button_desc','朝廷力推安国之策，要求军府与乡民团体让步，使恢复生产与改造旧法的主张占据朝议。','Press the reform agenda at court, demanding concessions from the military and rural associations so that economic recovery and legal reform take priority.',reason='原文削减乡村旧规没交代实际承担者；效果降低军队、乡村民众赞同而非地主，且并不直接删除军队/更改法律。',source='M/common/scripted_buttons/nesnd_qe1_agendas.txt:5; M/common/static_modifiers/nesnd_qe1_agendas.txt:2',mechanic='Balance -25; armed forces and rural folk approval -2 for six months. Existing policy/button name retained.')
add('nesnd_qe1.2.d','统治派取得了朝廷的支持，军府将掌握更多征募、军需与任官事务。此前要求恢复生产、改造旧法的官员未能主导新政府，伊犁已把扩充军队列为国策。','The military faction has won the government’s support and will take a greater part in recruitment, supply and appointments. Officials who argued for economic recovery and legal reform have failed to set its course. Ili has made expansion of the army a priority.',reason='删除“代价由被排除者承担”的无对象总结；将抽象代价改成议程争夺的实际结果。',source='M/common/scripted_effects/nesnd_qe1_agendas.txt:75; M/common/static_modifiers/nesnd_qe1_agendas.txt',mechanic='Military winner flag + ten-year modifier; no claim that laws/appointments are forcibly replaced.')
add('nesnd_qe1.3.d','朝议延续了十年，田地、军饷与官职的争论仍没有结果。地方听过太多振兴帝国的许诺，越来越少的人相信下一道法令能改变自己的处境。',None,reason='朝议终局不限定君主制，用法令代替仅君主可发的诏令；保留十年真实计时。',source='M/common/scripted_effects/nesnd_qe1_agendas.txt:94; M/common/scripted_triggers/nesnd_qe1_campaign.txt:2',mechanic='Ten-year unresolved agenda; does not require monarch to remain in office.')
add('nesnd_qe1_court_journal_reason','皇族以旧日征服的威望维系奉宸官僚，地方士人依靠学堂、商号和官署经营政务，军队则掌握帝国赖以扩张的武力。三方都要借助另外两方治理各地，也都在争取任官、征税和调兵的决定权。','The imperial house draws on the prestige of past conquests and the loyalty of officials who owe it their position. Provincial literati work through schools, trading houses and public offices; the army commands the force on which imperial expansion depends. Each faction needs the others to govern, yet each seeks authority over appointments, revenue and military command.',reason='三权日志在总统共和+比例代表制下仍有效，原文现在时“皇帝任命”不一定成立；保留皇族政治力量但不虚构在位皇帝。',source='M/common/scripted_triggers/nesnd_qe1_campaign.txt:20; M/common/scripted_buttons/nesnd_qe1_court.txt:6',mechanic='Court eligibility excludes universal suffrage/council republic, not presidential republic.')
add('nesnd_qe1_unity_journal_reason','商路、村社与军屯曾将许多不同来历的人联结在陈秦皇帝的治下。西域汉羌既是帝国扩张的产物，也为这个国家提供了兵员与税源。人们在繁荣中接受共同的身份，也会在征役与贫困中重新寻找旧日的族名、信仰和乡里。','Trade routes, village communities and military colonies brought peoples of many origins under the Chen emperors of Qin. The Western Regions Han-Qiang emerged from that expansion and now provide much of the country’s manpower and revenue. Prosperity encourages a common identity. Conscription and hardship can lead people back to older loyalties of kinship, faith and homeland.',reason='常驻团结日志在共和后仍存在；陈秦皇帝统治作为历史保留，不写成无条件现在时。',source='M/common/scripted_triggers/nesnd_qe1_campaign.txt:21',mechanic='Historical identity remains relevant under every current Qin government.')
add('nesnd_qe1_patron_crown_button_desc','让拥护皇室的军士与官员掌握更多职位。','Give more offices to soldiers and administrators loyal to the imperial house.',reason='共和分支仍可奖掖皇族势力，不能以现有皇室任命为职位前提。',source='M/common/scripted_buttons/nesnd_qe1_court.txt:1',mechanic='Patronage modifier; does not require an actual reigning emperor.')
add('nesnd_qe1_coup_literati_button_desc','改立总统共和，由民选总统与实行比例代表的议会主持国政。','Establish a presidential republic with an elected president and a parliament chosen by proportional representation.',reason='可从法团国家等非君主国体执行，原文无条件“废除皇位”不适用所有入口。',source='M/common/scripted_buttons/nesnd_qe1_court.txt:6',mechanic='Activates presidential republic and custom voting law; no assumption of existing throne.')
add('nesnd_qe1_coup_crown_button_desc','以君主制与技术官僚重组政府，使皇室重新掌握国家的统治。','Reorganize the government as a monarchy administered by trained technocrats, restoring the imperial house to power.',reason='按钮可从共和国恢复君主，原文“保留皇位”并非所有分支成立。',source='M/common/scripted_buttons/nesnd_qe1_court.txt:7',mechanic='Activates law_monarchy + law_technocracy; not gated to an existing monarchy.')
add('law_nesnd_qe1_proportional_representation_desc','财产达到门槛的选民取得投票资格，识字程度也影响其选票的政治分量。各政治团体依支持力量组成议会与政府。','Property determines eligibility to vote, while literacy increases a voter’s political influence. Political groups form parliament and government according to their support.',reason='原文将识字写成独立资格门槛；实际law是wealth threshold10 + voting_power_from_literacy50，文意需区分资格与票权。',source='M/common/laws/nesnd_qe1_laws.txt:10',mechanic='Retains custom proportional-representation name; does not claim actual district seat-allocation simulation.')
for zone in ['levant','egypt','arabia','central_asia','india']:
    add(f'nesnd_per_claim_{zone}_button_desc','向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。',None,reason='地区不能接受照会，外交行动者是有关国家；英文现稿已正确。',source='M/common/scripted_effects/nesnd_per_campaign.txt:44',mechanic='A selected unclaimed foreign-owned state; adds claim only without obstruction.')
add('nesnd_per_claim_india_button','申明印度西北诸地的权利','Assert Claims in Northwestern India',reason='原名“印度河流域”不能涵盖Delhi/Agra/Rajputana/Gujarat；去掉未给出处的“旧权”历史断言。',source='M/common/scripted_triggers/nesnd_per_campaign.txt:38',mechanic='Targets Sindh, Punjab, Hill Punjab, Delhi, Agra, Rajputana, Gujarat.')
add('nesnd_per.4.d','本朝与伊犁已经确定朝贡往来，朝廷也将扩张的方向转向西方。军府准备新的远征，商人则打算沿着军队前进的道路寻找市场。','Our tributary relationship with Ili is settled, and the government has chosen expansion to the west. Commanders are preparing new campaigns, while merchants seek markets along the routes the army will take.',reason='按实际当前仍为QE1属国的成功分支确认朝贡关系，删去关于下一轮援助的空泛预告。',source='M/common/scripted_effects/nesnd_per_campaign.txt:24; root planned guarded event branch 2026-11-02',mechanic='Use only when QE1 exists/alive and PER is currently subject_of QE1; root will branch on actual relationship, not stale route flag.',apply='E_and_C_requires_branch')
add('nesnd_per.4.d_unavailable','朝廷已经决定向西扩张，原定与伊犁建立的朝贡安排却未能成立。军府与商人仍可经营西方，所需兵力与财源须从眼下能够取得的支持中筹措。','The government has chosen expansion to the west, but the proposed tributary arrangement with Ili has not taken effect. Commanders and merchants can still pursue a western policy, drawing on the troops, revenues and support presently available.',reason='缺失QE1或受第三国宗主等分支不能虚构签成朝贡或已获援助。',source='M/common/scripted_effects/nesnd_per_campaign.txt:24; root planned guarded event branch 2026-11-02',mechanic='Fallback when actual PER->QE1 subject relationship is absent. Future progress/completion unchanged.',apply='E_and_C_requires_branch',new=True)
add('nesnd_per_future_status_aid','朝廷已选定求援伊犁、向西经营的方针。','The government has chosen to seek support from Ili for expansion to the west.',reason='状态只检查route_aid，不保证援助方仍存在或使者正在往来；陈述已选方针而非当前实存援助。',source='M/common/journal_entries/nesnd_per_campaign.txt:21; M/common/scripted_triggers/nesnd_per_campaign.txt:5',mechanic='Route choice persists if aid becomes unavailable; progress intentionally continues.')
for k,term in [('modifier_state_nesnd_qe1_conversion_cohort_standard_of_living_add_desc','生活水平'),('modifier_country_nesnd_qe1_conversion_cohort_cultural_acceptance_add_desc','文化接纳'),('modifier_country_fervor_target_nesnd_qe1_conversion_cohort_add_desc','文化热情')]:
    add(k,f'对西域汉羌人口{term}的影响。',None,reason='现有中文三项均泛写“人口的影响”，补齐实际量。',source='M/common/modifier_type_definitions/nesnd_qe1_cohort.txt',mechanic='Labels only; English already identifies the correct quantity.')

# Next blocks add the fully reviewed Philippines, Tenasserim and geographical proposals.
phi_en={
'nesnd_phi_service_recovery':'Funding the Luzon Garrison',
'nesnd_phi_service_recovery_reason':"The soldiers who sailed south with Lin Zexu brought the voices of Huguang to Luzon’s garrisons. Their pay, provisions and training now depend on the islands, while the administration must also keep ships ready for imperial service.\\n\\nThe cost of these obligations has become a question for both governments. Luzon seeks a new settlement of garrison expenses, naval service and tribute, so that its revenues can support the troops as well as the people who sustain them.",
'nesnd_phi_status_external':'The subject relationship, shared market or peace between the two countries has changed. Payments under the agreement will cease. A new settlement must reflect our present income and obligations.',
'nesnd_phi_status_stalled':'The paying country is unable to meet its obligations. The treaty may be suspended or the country in [concept_default]. Promised payments count as income only when received.',
'nesnd_phi_status_pending':'Both governments must approve the proposal within 120 days. Until then, no money or ships change hands.',
'nesnd_phi_status_active':'The agreement is in force. The subsidy ends 12 months after signature; garrison strength, naval staffing and local livelihoods must remain sustainable.',
'nesnd_phi_status_review':'The subsidy has ended. Sustain the required finances, forces and livelihoods for three months. Renewed payments require the consent of both governments.',
'nesnd_phi_status_proposal':'Request central funding for the garrison, or negotiate a division of naval responsibilities.',
'nesnd_phi_service_bar':'Garrison Finances and Livelihoods',
'nesnd_phi_service_bar_desc':"#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 4#!",
'nesnd_phi_service_bar_detail':"Weekly balance excluding construction: #v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\\nCrew required for a fully staffed fleet: #v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\\nUnemployed workforce: #v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\\nWorkforce below the starvation threshold: #v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\\n\\nEach requirement fills one segment: a nonnegative balance excluding construction, no [concept_default] or [concept_bankruptcy], and any agreed subsidy actually being paid; at least #v 35 battalions#! in the standing army; at least #v 40 flotillas#! under the garrison agreement or #v 20 flotillas#! under the naval division, with #v 75%#! of crews and at least #v 80%#! naval maintenance fulfillment; unemployment at most #v 12%#! and no more than #v 15%#! of the workforce below the starvation threshold. Updated monthly.",
'nesnd_phi_continuity_bar':'Financial Stability',
'nesnd_phi_continuity_bar_desc':"#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 3 months#!",
'nesnd_phi_continuity_bar_detail':'Gain #p 1#! each month at peace with all four requirements met. A failure resets the count. The count also resets when the subsidy ends; three successful months after that are required to complete the Journal Entry.',
'nesnd_phi_request_a_button':'Negotiate Garrison Funding',
'nesnd_phi_request_a_button_desc':'Use the signed Ming or Wu commitment, which must match both governments’ present allegiances, to seek central funding for the overseas garrison. The central government must approve the expense before Luzon gives final consent.\\n\\n$nesnd_phi_route_1_terms_tt$',
'nesnd_phi_request_b_button':'Divide Naval Responsibilities',
'nesnd_phi_request_b_button_desc':'Propose a division between the ocean-going fleet and the defence of the islands, retaining the Western Administration’s garrison in Luzon. The agreement does not change either government’s political allegiance.\\n\\n$nesnd_phi_route_2_terms_tt$',
'nesnd_phi_cancel_request_button':'Withdraw the Proposal',
'nesnd_phi_cancel_request_button_desc':'Withdraw the unsigned proposal. Another may be submitted after 30 days. Existing diplomatic agreements remain in force.',
'nesnd_phi_withdraw_button':'End the Subsidy Early',
'nesnd_phi_withdraw_button_desc':'Withdraw from the subsidy treaty negotiated here. Leaving during its binding period incurs the treaty’s Infamy and relations penalties. Tribute reductions, exemption from military service and other treaties retain their own terms. Ships already transferred remain with the central government.',
'nesnd_phi_route_1_terms_tt':'The central government pays Luzon #v £8,000#! a week for #v 12 months#!. A separate treaty reduces the share of income paid in tribute by #v 10 percentage points#!. Luzon retains its fleet and garrison. The central government needs at least #v £10,000#! in weekly surplus excluding construction, #v £100,000#! in reserves, and eligibility for both treaties. The subsidy treaty is withdrawn at the end of the year; the tribute reduction retains its own terms.',
'nesnd_phi_route_2_terms_tt':'On the first agreement, Luzon transfers #v 20 ships of the line#! that it owns and that are not engaged in war. It retains #v 20 frigates#! and the garrison. The central government pays #v £3,000#! weekly for #v 12 months#!, and concludes separate treaties for reduced tribute and exemption from military service. It needs at least #v £5,000#! in weekly surplus excluding construction and #v £60,000#! in reserves. Renewals do not transfer more ships. The subsidy ends after a year; the other agreements retain their own terms.',
'nesnd_phi_usm_accept_tt':'Return the approved terms to Luzon for final consent. Treaty eligibility, finances, the subject relationship and the fleet must still meet the requirements. No subsidy is paid and no ships are transferred yet.',
'nesnd_phi_reject_tt':'Return the proposal. Another may be submitted after 90 days.',
'nesnd_phi_defer_tt':'Do not sign this agreement. Negotiations may resume after 30 days.',
'nesnd_phi_finance.reject':'We cannot authorize this expense.',
'nesnd_phi_finance.defer':'Return it for further negotiation.',
'nesnd_phi_finance.cancel':'Withhold our signature.',
'nesnd_phi_finance.1.t':'Paying the Luzon Garrison',
'nesnd_phi_finance.1.d':'Luzon asks the central government to share the cost of the troops and ships maintained on the islands. Its administration argues that overseas service cannot depend indefinitely on local revenue alone.\\n\\nThe proposal provides #v £8,000#! a week for one year, alongside a reduction in tribute. It now falls to the central government to decide whether to undertake these obligations.',
'nesnd_phi_finance.1.a':'Approve the funding and seek Luzon’s consent.',
'nesnd_phi_finance.2.t':'A Division of the Fleet',
'nesnd_phi_finance.2.d':'Luzon proposes to transfer twenty ships of the line to the central navy. The frigates would remain to defend the islands, as would the garrison. Taking over the ships would also make the central government responsible for their crews, bases and supplies.\\n\\nIn return, Luzon seeks exemption from military service, reduced tribute and #v £3,000#! a week for one year to support the reorganization.',
'nesnd_phi_finance.2.a':'Agree to this division of responsibilities.',
'nesnd_phi_finance.3.t':'The Funding Offer',
'nesnd_phi_finance.3.d':'The central government has approved Luzon’s request. It offers #v £8,000#! a week for one year, with reduced tribute under a separate agreement. The fleet and garrison would remain Luzon’s responsibility.\\n\\nThe administration in Manila must now give its consent before the payments can begin.',
'nesnd_phi_finance.3.a':'Sign the agreement.',
'nesnd_phi_finance.4.t':'The Naval Agreement',
'nesnd_phi_finance.4.d':'The central government has accepted the proposed division of naval duties. The frigates will defend the islands, and the Western Administration’s garrison will remain in Luzon.\\n\\nLuzon’s signature will confirm the ship transfer, reduced tribute and exemption from service, together with #v £3,000#! in weekly payments for one year. A renewal will retain the previous transfer without requiring further ships.',
'nesnd_phi_finance.4.a':'Sign and carry out the transfer.',
'nesnd_phi_finance.5.t':'A Settlement of Expenses',
'nesnd_phi_finance.5.d':'Both governments have signed. The central treasury must now make the agreed payments, while Luzon’s administration must use its revenues to support the garrison, the fleet and the islands’ civilian needs.\\n\\nThe coming year will show whether these obligations can be maintained after the temporary subsidy ends.',
'nesnd_phi_finance.5.a':'Put the agreement into effect.',
'nesnd_phi_finance.6.t':'A Year of Funding',
'nesnd_phi_finance.6.d':'The year of payments is over, and the subsidy treaty has ended as agreed. Luzon must now support its remaining forces from current revenues or negotiate fresh assistance. Its other obligations remain governed by the existing subject relationship and treaties.',
'nesnd_phi_finance.6.a':'Settle the coming year’s expenses.',
'nesnd_phi_finance.7.t':'Funding Interrupted',
'nesnd_phi_finance.7.d':'The subsidy can no longer continue on the agreed terms. Luzon’s military and naval authorities must revise their spending. Any new agreement will have to reflect the present subject relationship, market arrangements and military obligations.',
'nesnd_phi_finance.7.a':'Reconsider the budget.',
'nesnd_phi_finance.8.t':'The Garrison Sustained',
'nesnd_phi_finance.8.d':'For three months after the subsidy ended, Luzon has maintained its finances, forces and civilian livelihoods. The garrison remains supplied and the fleet has the crews it needs. The administration can plan its next season of spending from revenues it actually receives.',
'nesnd_phi_finance.8.a':'Maintain this settlement.',
'nesnd_phi_finance.10.t':'Revised Terms',
'nesnd_phi_finance.10.d':'The two governments have amended the treaty through diplomatic negotiations. Its terms now differ from the earlier military funding agreement. Luzon’s administration will follow the revised treaty; its payment schedule and other obligations can be reviewed in the diplomacy panel.',
'nesnd_phi_finance.10.a':'Observe the revised agreement.',
'nesnd_phi_request_cash_a_button':'Negotiate a Fixed Garrison Subsidy',
'nesnd_phi_request_cash_a_button_desc':'Agree on a weekly contribution from the central government towards the garrison and ocean-going fleet. A signed Ming or Wu commitment must match both governments’ present allegiances.\\n\\n$nesnd_phi_cash_1_terms_tt$',
'nesnd_phi_request_cash_b_button':'Divide Naval Duties with Fixed Funding',
'nesnd_phi_request_cash_b_button_desc':'Transfer the ships of the line to the central government, retaining frigates to defend the islands and the existing garrison. Negotiate fixed funding for the new arrangement. This agreement does not change allegiance to Ming or Wu, neutrality or independence.\\n\\n$nesnd_phi_cash_2_terms_tt$',
'nesnd_phi_cash_1_terms_tt':'The central government pays Luzon #v £8,700#! weekly for #v 12 months#!. Luzon retains its garrison and fleet. Tribute continues under the existing subject relationship; this agreement neither reduces the tribute rate nor changes Liberty Desire. The central government needs at least #v £10,000#! in weekly surplus excluding construction, #v £100,000#! in reserves, and eligibility for the subsidy treaty. Payments begin only after both governments consent and end after the agreed year.',
'nesnd_phi_cash_2_terms_tt':'The first agreement transfers #v 20 ships of the line#! to the central government. Luzon retains #v 20 frigates#! and the garrison, and gains exemption from military service if eligible. The central government pays #v £3,700#! weekly for #v 12 months#!. Tribute continues at the existing rate. The central government needs at least #v £5,000#! in weekly surplus excluding construction and #v £60,000#! in reserves. Renewals do not transfer additional ships; the end of the year terminates only this subsidy.',
'nesnd_phi_finance.11.t':'A Garrison Subsidy',
'nesnd_phi_finance.11.d':'Luzon requests an annual contribution towards the troops and ships it maintains for imperial service. Tribute would continue under the existing arrangement, while the central treasury would take on a separate share of the military expense.\\n\\nThe proposed payment is #v £8,700#! a week for one year.',
'nesnd_phi_finance.11.a':'Approve the subsidy and seek Luzon’s consent.',
'nesnd_phi_finance.12.t':'Consent to the Subsidy',
'nesnd_phi_finance.12.d':'The central government has approved #v £8,700#! in weekly payments for one year. Luzon would continue paying tribute under its present obligations and remain responsible for the fleet and garrison.\\n\\nThe administration in Manila must give final consent to begin the payments.',
'nesnd_phi_finance.12.a':'Sign the agreement.',
'nesnd_phi_finance.13.t':'Funding the Naval Division',
'nesnd_phi_finance.13.d':'Luzon asks the central navy to take over twenty ships of the line, retaining the frigates and garrison for local defence. The central government would provide their new bases, crews and supplies.\\n\\nTribute would continue on the existing terms. Luzon seeks #v £3,700#! a week for one year and exemption from further military service under the agreed arrangements.',
'nesnd_phi_finance.13.a':'Approve the division and its funding.',
'nesnd_phi_finance.14.t':'Ships and Funding',
'nesnd_phi_finance.14.d':'The central government has accepted the naval division. Twenty ships of the line would pass to its navy, while the frigates and garrison remain in Luzon. Renewals retain the transfer already made.\\n\\nThe agreement provides #v £3,700#! a week for one year. Tribute and exemption from military service follow their separate terms. Luzon must now give final consent.',
'nesnd_phi_finance.14.a':'Sign and complete the handover.',
'nesnd_phi_propose_native_a_tt':'Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\\n\\n$nesnd_phi_route_1_terms_tt$',
'nesnd_phi_propose_native_b_tt':'Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\\n\\n$nesnd_phi_route_2_terms_tt$',
'nesnd_phi_propose_cash_a_tt':'Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\\n\\n$nesnd_phi_cash_1_terms_tt$',
'nesnd_phi_propose_cash_b_tt':'Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\\n\\n$nesnd_phi_cash_2_terms_tt$',
}
phi_zh={
'nesnd_phi_status_pending':'两国须在120天内确认议案。签署之前，钱款与舰船仍由原有政府掌管。',
'nesnd_phi_status_active':'协定正在履行，钱款将在签订12个月后终止。驻军、舰员与居民的生计仍须由现有收入维持。',
'nesnd_phi_status_proposal':'可请求中央分担驻屯军费，或商议分任舰队与地方海防。',
'nesnd_phi_continuity_bar_detail':'和平期间，四项军民经费条件持续达标，每月增加#p 1#!；中断后归零。钱款终止时重新计算，终止后三个月达标才完成日志。',
'nesnd_phi_finance.1.d':'吕宋请求中央分担驻屯军与远洋舰队的开销。宣慰司认为，这些兵船听候朝廷征调，其军饷和日常供给也不宜长久只靠群岛的收入维持。\\n\\n议案请中央每周拨给#v £8,000#!，支给一年，并另行减贡。是否承接这笔开支，须由中央议定。',
'nesnd_phi_finance.3.d':'中央已经核准吕宋的请求，愿意每周拨给#v £8,000#!，支给一年，减贡则另依新议。驻屯大营与舰队仍由吕宋维持。\\n\\n宣慰司还须最后确认，钱款才能开始支付。',
'nesnd_phi_finance.5.d':'两国已经签署协定。中央须按约支付钱款，吕宋则须统筹驻军、舰队与地方民生的开支。\\n\\n这一年的援助能否让群岛在款项结束后维持自己的军政，还要看现有收入能够承担多少义务。',
'nesnd_phi_finance.8.d':'钱款支用期结束后，吕宋已连续三个月维持军民经费。驻屯大营仍能受领军需，海船已有足够水手，地方居民的生计也达到了此前议定的条件。宣慰司可以依实际收入安排下一季开支。',
}
phi_zh.update({
'nesnd_phi_service_recovery_reason':'楚军南渡之后，吕宋的营垒里又添了许多湖广乡音。随林则徐出海的将士在此领饷、操练，把故乡的消息夹在家书里传回军中。群岛要供养这些驻军，也须为朝廷的远洋征调备齐舰船与水手。\\n\\n宣慰司请求重新商议驻屯军费、海防和岁贡。当地收入须同时维持军队与百姓的生计，中央承担多少，吕宋留下多少，将决定这支海外军队能够长久驻守的根基。',
'nesnd_phi_status_external':'宗属、共同市场或两国间的和平已经改变，原定补贴停止续付。今后的军费须依当前收入与军事义务重新商定。',
'nesnd_phi_status_stalled':'议定的拨款尚未到账。付款国可能陷入[concept_default]，条约也可能暂停履行；驻屯经费暂须依靠已经收到的收入。',
'nesnd_phi_status_review':'补贴已经结束。军费、驻军与民生须再维持三个月；若需续款，仍须取得两国同意。',
'nesnd_phi_service_bar_detail':"非建设周结余：#v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\\n舰队满员所需水手：#v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\\n无业劳动力：#v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\\n\\n四项各计一格：非建设收支非负，未陷入[concept_default]或[concept_bankruptcy]，且议定的补贴正在支付；常备军至少#v 35营#!；驻屯协定至少#v 40舰#!、海防分任至少#v 20舰#!各有#v 75%#!水手，海军维护履行至少#v 80%#!；无业至多#v 12%#!，欠食至多#v 15%#!。每月更新。",
'nesnd_phi_request_a_button_desc':'依据双方已经确认且仍然一致的拥明或拥吴承诺，请中央分担海外驻屯军费。中央同意支出后，再由吕宋最后确认。\\n\\n$nesnd_phi_route_1_terms_tt$',
'nesnd_phi_request_b_button_desc':'议定远洋舰队与群岛海防的分工，保留西府驻屯大营。此次交涉不改变两国的政治立场。\\n\\n$nesnd_phi_route_2_terms_tt$',
'nesnd_phi_cancel_request_button_desc':'撤回尚未签成的议案，30天后可重提。已有外交协定仍然有效。',
'nesnd_phi_withdraw_button_desc':'由吕宋提前退出议定的补贴条约。约束期内退出将招致条约规定的恶名与关系损失；减贡、免役及其他条约仍依各自条款履行，已经移交的舰船仍归中央。',
'nesnd_phi_route_1_terms_tt':'中央每周向吕宋支付#v £8,000#!，持续#v 12个月#!；另以减贡协定将收入转移比例降低#v 10个百分点#!。吕宋保留舰队与驻军。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，并具备签署两项协定的资格。补贴条约于一年后撤回，减贡协定仍依自身条款履行。',
'nesnd_phi_route_2_terms_tt':'首次签订时，吕宋向中央移交所持且未参战的#v 20艘战列舰#!，保留#v 20艘护卫舰#!与驻屯军。中央每周支付#v £3,000#!，持续#v 12个月#!，并另行签署减贡与免役协定。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不再交舰；一年后补贴结束，减贡与免役仍依各自条款履行。',
'nesnd_phi_usm_accept_tt':'把核准的条款交回吕宋，待其最后确认。届时两国的签约资格、财力、宗属与舰队仍须符合议案条件，之后才支付补贴、交接舰船。',
'nesnd_phi_finance.2.d':'吕宋提议将二十艘战列舰交由中央海军，护卫舰留下守备群岛，驻屯大营仍归宣慰司。中央接管这些海船，也须承担它们的驻地、船员与日常供给。\\n\\n为此，吕宋请求免除从征义务，减轻岁贡，并由中央每周支付#v £3,000#!，支给一年，以备海防整顿。',
'nesnd_phi_finance.4.d':'中央已经同意分任海防。护卫舰将守备群岛，西府驻屯大营仍留吕宋。\\n\\n宣慰司此次签署，将确认交舰、减贡与免役的安排，以及每周#v £3,000#!、支给一年的补贴。续签时沿用已经交舰的结果，不再另交舰船。',
'nesnd_phi_finance.6.d':'一年的拨款已经付完，补贴条约依约终止。吕宋须以现有收入维持所留军队，或再向中央商议援助。其他军事与外交义务，仍按当前宗属关系及各项条约办理。',
'nesnd_phi_finance.7.d':'中央已不能按原议继续拨款。吕宋的军需与海军官员须重新安排开支，下一份军费协定也须依当前宗属、市场与军事义务商定。',
'nesnd_phi_finance.10.d':'两国已经通过外交交涉改订条约，其条款与此前军费协定不同。吕宋今后依新约办理，付款期限与其余义务可在外交界面查看。',
'nesnd_phi_request_cash_a_button_desc':'依据双方已经确认且仍然一致的拥明或拥吴承诺，商议中央每周分担的驻屯与远洋海防经费。\\n\\n$nesnd_phi_cash_1_terms_tt$',
'nesnd_phi_request_cash_b_button_desc':'中央接管战列舰，吕宋留护卫舰守备群岛，驻屯大营照旧编练，再议定分任后的军费。协议不改变拥明、拥吴、中立或自主立场。\\n\\n$nesnd_phi_cash_2_terms_tt$',
'nesnd_phi_cash_1_terms_tt':'中央每周向吕宋支付#v £8,700#!，持续#v 12个月#!。吕宋保留驻屯军与舰队，贡赋仍依现有宗属关系支付；此约不改贡率与独立倾向。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，并具备签约资格。两国确认后开始付款，一年后结束。',
'nesnd_phi_cash_2_terms_tt':'首次签订时向中央移交#v 20艘战列舰#!，吕宋保留#v 20艘护卫舰#!与驻屯军；符合资格后另议免除军事服务。中央每周支付#v £3,700#!，持续#v 12个月#!。贡赋仍按原有比例支付。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不再交舰；一年后仅结束这项补贴。',
'nesnd_phi_finance.11.d':'吕宋请求中央分担每年的驻屯与海防开销。岁贡仍依现有章程解送，中央另从国库承担一部分军费。\\n\\n此次议案请每周支付#v £8,700#!，支给一年。',
'nesnd_phi_finance.12.d':'中央已经核准每周#v £8,700#!、支给一年的补贴。吕宋仍按现有宗属章程解贡，舰队与驻屯大营继续由宣慰司维持。\\n\\n还须吕宋最后同意，拨款才能开始。',
'nesnd_phi_finance.13.d':'吕宋请求中央海军接管二十艘战列舰，由中央安排驻地、船员与供给；护卫舰与驻屯大营仍留群岛。\\n\\n贡款照旧解送。吕宋另请每周#v £3,700#!、支给一年的补贴，并按议定条件免除从征义务。',
'nesnd_phi_finance.14.d':'中央已经接受分任海防的提议。二十艘战列舰将由中央接管，护卫舰与驻屯军留守群岛；续签时仍承认此前的交舰结果。\\n\\n补贴每周#v £3,700#!，支给一年。贡赋与免役另依各自条款办理。吕宋尚须最后确认这份协定。',
'nesnd_phi_propose_native_a_tt':'将议案送交中央审议，获准后由吕宋最后确认。议定条款：\\n\\n$nesnd_phi_route_1_terms_tt$',
'nesnd_phi_propose_native_b_tt':'将议案送交中央审议，获准后由吕宋最后确认。议定条款：\\n\\n$nesnd_phi_route_2_terms_tt$',
'nesnd_phi_propose_cash_a_tt':'将议案送交中央审议，获准后由吕宋最后确认。议定条款：\\n\\n$nesnd_phi_cash_1_terms_tt$',
'nesnd_phi_propose_cash_b_tt':'将议案送交中央审议，获准后由吕宋最后确认。议定条款：\\n\\n$nesnd_phi_cash_2_terms_tt$',
})
for k,en in phi_en.items():
    en=en.replace('the signed Ming or Wu commitment','the confirmed commitment to Ming or Wu').replace('A signed Ming or Wu commitment','A confirmed commitment to Ming or Wu')
    if k in phi_zh: phi_zh[k]=phi_zh[k].replace('议定条款：','拟议条款：').replace('符合资格后另议免除军事服务','符合资格后免除军事服务')
    add(k,phi_zh.get(k),en,reason='英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。' if k in phi_zh else '英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。',source='M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt',mechanic='Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.')
phi_keys={k for k in data if k.startswith('nesnd_phi_') or k.startswith('nesnd_phi_finance.')}
assert phi_keys == set(phi_en), (phi_keys-set(phi_en),set(phi_en)-phi_keys)
proposals['nesnd_phi_service_bar_detail']['en']=proposals['nesnd_phi_service_bar_detail']['en'].replace('flotillas','ships')

ten={
'nesnd_ten_status_sampling':('地方官正在汇报最初三个月的就业与生计。林场委办和法案审议可以先行。','Local officials are reporting on employment and livelihoods over the first three months. Logging commissions and legislation may proceed in the meantime.'),
'nesnd_ten_status_war':('战争已使生计巩固中断，港口、海运与市场往来有待恢复。','War has interrupted the recovery. Ports, shipping and access to markets must be restored.'),
'nesnd_ten_status_review':('地方生计正在恢复，还须有一处不占耕地的产业达到75%配员。','Local livelihoods are recovering. At least one industry that does not use arable land must also reach 75% staffing.'),
'nesnd_ten_build_button_desc':('委托商人经营林场，为当地增加不占耕地的雇工岗位。\\n\\n每次排入#v 1级#!政府建设，最多委办#v 2次#!，间隔#v 6个月#!。已有林场须达到#v 75%#!配员且无原料短缺；木价至少为基础价的#v 50%#!，国库至少#v £5,000#!，当地仍可建林场。工程照常消耗建设力和财政。工具或技工资质不足时，可选原始林业。','Commission a logging camp to provide paid work without taking arable land.\\n\\nEach commission queues #v 1 level#! of government construction, up to #v 2 commissions#! at least #v 6 months#! apart. Any existing logging camp must be #v 75%#! staffed without input shortages. Wood must sell for at least #v 50%#! of its base price, the treasury must hold #v £5,000#!, and local capacity must permit construction. Normal construction and treasury costs apply. Simple forestry can be used where tools or trained machinists are scarce.'),
'nesnd_ten_tenant_button_desc':('以固定租佃关系取代农奴的人身依附，让农户在交租之后安排自己的生计。\\n\\n开始审议租佃法案：法律须可制定，并有执政利益集团或支持率至少#v 10%#!的政治运动支持；预计通过机会至少#v 15%#!，合法性至少#v 25#!，且没有其他在议法案、战争或革命。','Replace serfs’ personal dependence with tenancy, allowing farmers to plan their livelihoods after paying rent.\\n\\nBegin enacting Tenant Farmers. The law must be enactable and supported by an interest group in government or a political movement with at least #v 10%#! support. Enactment chance must be at least #v 15%#! and legitimacy at least #v 25#!, with no other law being enacted, war or revolution.'),
'nesnd_ten_abolish_button_desc':('废除奴隶制度，使劳动者不再作为他人的财产。\\n\\n取消农奴制后，地方无业劳动力至多#v 15%#!，且已有三个月的地方汇报，方可由此提出废奴法案。支持、通过机会及合法性门槛与租佃法案相同。法律通过后实行解放。','Abolish slavery so that workers can no longer be held as another person’s property.\\n\\nOnce serfdom has ended, local unemployment must be at most #v 15%#! and three months of local reports must be available. The support, enactment-chance and legitimacy requirements are the same as for Tenant Farmers. Emancipation takes effect when the law passes.'),
'nesnd_ten_dismiss_button_desc':('将地方经营交回现有官署与商行，停办专项教习。一年后可以重新开办。','Return the programme’s duties to the existing administration and merchants, ending its special instruction. The programme can reopen after one year.'),
'nesnd_ten_continue_tt':('续办丹那沙林专项，保留已有的工程、法案与拨款安排。','Continue the Tenasserim programme with its existing construction, legislation and funding arrangements.'),
'nesnd_ten_reopen_desc':('重新着手改善丹那沙林的就业与农户生计。以前的委办次数保留，生计巩固重新累计。','Resume efforts to improve employment and rural livelihoods in Tenasserim. Previous commissions still count towards the limit, and the period of recovery begins again.'),
'nesnd_tenasserim.1.d':('丹那沙林的经营遇到了困难。为林场与工场招工，需要有人肯付工钱；让村民留住收成，则须处理租佃与债务。官署提供的教习也需要持续的经费。\\n\\n政府必须决定，是继续投入资源改善这些条件，还是把地方经营交回现有官署与商行。','The Tenasserim programme has run into difficulty. Logging camps and workshops need employers able to pay wages; villagers need tenancy and credit arrangements that leave them a livelihood. The practical instruction provided by the authorities also requires sustained funding.\\n\\nThe government must decide whether to keep committing resources or return these responsibilities to the existing administration and merchants.'),
'nesnd_ten_dismiss_tt':('停办专项并撤回学工教习，一年后可重新开办。已排入的建设、正在审议的法律及已付补偿继续有效；此前的委办次数与奖励仍然保留。','End the programme and withdraw its practical instruction. It may reopen after one year. Queued construction, ongoing legislation and compensation already paid remain in effect; previous commissions and rewards still count.'),
}
for k,(zh,en) in ten.items():
    add(k,zh,en,reason='去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。',source='M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt',mechanic='No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.')

# Keep the established map referents; translate only Chinese fallbacks, with a separately justified water-works rewrite.
map_english=dict(line.split('=',1) for line in '''陕北=Shanbei
汉中=Hanzhong
川南=Southern Sichuan
关中农区=Guanzhong Farmland
秦岭林区=Qinling Forests
川西矿区=Western Sichuan Mines
岷江林区=Min River Forests
延安=Yan'an
陕北煤田=Shanbei Coalfields
陕北农区=Shanbei Farmland
陕北林区=Shanbei Forests
巴山矿区=Bashan Mines
汉水农区=Han River Farmland
汉中林区=Hanzhong Forests
泸州=Luzhou
西昌=Xichang
川南农区=Southern Sichuan Farmland
川南林区=Southern Sichuan Forests
陈秦水利・关中=Chen-Qin Irrigation: Guanzhong
陈秦水利・陕北=Chen-Qin Irrigation: Shanbei
陈秦水利・汉中=Chen-Qin Irrigation: Hanzhong
沿用陈秦以来的水利设施与陆运驿路。=Irrigation works and overland post roads inherited from Chen-Qin support the region.
长江水运・蜀国=Yangtze Navigation: Shu
长江水运・川南=Yangtze Navigation: Southern Sichuan
本地港埠经支流与长江干流连接。=Local river ports connect to the Yangtze through its tributaries.
大同=Datong
雁北煤田=Yanbei Coalfields
桑干农区=Sanggan Farmland
恒山林区=Hengshan Forests
太行山=Taihang Mountains
太原水运=Taiyuan River Transport
晋北水运=Northern Shanxi River Transport
支流、渡口与沿河驿道构成当地的运输网络。=Tributaries, ferries and riverside post roads form the local transport network.
承德=Chengde
热河矿区=Rehe Mines
滦河农区=Luan River Farmland
燕山林区=Yanshan Forests
宁古塔=Ningguta
牡丹江矿区=Mudan River Mines
三江农区=Sanjiang Farmland
完达山林区=Wanda Mountains Forests
绵阳=Mianyang
广元=Guangyuan
嘉陵农区=Jialing Farmland
剑门林区=Jianmen Forests
川东矿区=Eastern Sichuan Mines
华蓥山=Huaying Mountains
重庆水运=Chongqing River Transport
梓潼水运=Zitong River Transport
襄阳=Xiangyang
襄北矿区=Northern Xiangyang Mines
南襄农区=Nanxiang Farmland
荆山林区=Jingshan Forests
荆西矿区=Western Jingzhou Mines
荆州水运=Jingzhou River Transport
襄阳水运=Xiangyang River Transport
赣州=Ganzhou
赣南矿区=Southern Jiangxi Mines
赣江农区=Gan River Farmland
南岭林区=Nanling Forests
赣北矿区=Northern Jiangxi Mines
南昌水运=Nanchang River Transport
赣南水运=Southern Jiangxi River Transport
桂林=Guilin
桂北矿区=Northern Guangxi Mines
柳江农区=Liu River Farmland
越城岭林区=Yuecheng Mountains Forests
桂南矿区=Southern Guangxi Mines
郁江农区=Yu River Farmland
南宁水运=Nanning River Transport
桂北水运=Northern Guangxi River Transport
闽江府=Minjiang
三明=Sanming
南平=Nanping
闽北林区=Northern Fujian Forests
闽江港=Minjiang Harbor
晋江农区=Jin River Farmland
闽西矿务=Western Fujian Mines
伊犁=Ili
伊犁屯田=Ili Military Farms
伊犁山矿=Ili Mountain Mines
胡杨地=Poplar Groves
乌恰=Wuqia
西天山绿洲=Western Tianshan Oases
阿克苏=Aksu
西天山河林=Western Tianshan River Forests
盆地北缘矿务=Northern Basin Mines
盆地北缘河林=Northern Basin River Forests
敦煌=Dunhuang
河西屯田=Hexi Military Farms
河西矿务=Hexi Mines
祁连林区=Qilian Forests
陇中矿务=Central Gansu Mines
高凉城=Gaoliang
茂名=Maoming
高凉矿务=Gaoliang Mines
高凉山林=Gaoliang Forests
高凉港=Gaoliang Harbor
珠江农区=Pearl River Farmland
北原府=Beiyuan
北原屯田=Beiyuan Military Farms
北原山矿=Beiyuan Mountain Mines
黄山=Huangshan
北原港=Beiyuan Harbor
晋北=Northern Shanxi
热河=Rehe
松江=Songjiang
梓潼=Zitong
赣南=Southern Jiangxi
桂北=Northern Guangxi'''.splitlines())
map_stems=['zz_nesnd_geography','zz_nesnd_national_map','zz_nesnd_map_refinement','nesnd_editor']
for p,lang in files:
    if lang!='simp_chinese' or not any(p.name.startswith(s+'_l_') for s in map_stems): continue
    for k,zh,n in parse(p):
        if k.startswith('nesnd_refine_water_'):
            add(k,'水利工程' if not k.endswith('_desc') else '既有水利设施支持农田灌溉，当地道路与水道也因此便于维持。','Irrigation Works' if not k.endswith('_desc') else 'Established waterworks support irrigation and the upkeep of local transport routes.',reason='删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。',source='M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25',mechanic='Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.')
        elif re.search('[\u4e00-\u9fff]',data[k].get('en','')):
            assert zh in map_english,(k,zh)
            add(k,None,map_english[zh],reason='英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。',source=f'{p}:{n}',mechanic='Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.')

add('nesnd_jingyin_departure_title',None,'The Prince of Huai Takes the Throne',reason='英文槽中文回退；原有头衔不改。',source='M/localization/simp_chinese/nesnd_character_notifications_l_simp_chinese.yml:2',mechanic='Notification of existing relocation; not new succession.')
add('nesnd_jingyin_departure_desc','登极的消息传到了[ROOT.GetCountry.GetName]。#bold [SCOPE.sCharacter(\'nesnd_jingyin_claimant\').GetFullName]#!已受群臣拥戴，前往[SCOPE.sCountry(\'new_jingyin_owner\').GetCapital.GetName]主持朝政。旧邸的官员须留下料理交接，随行臣属则将辅佐新朝的政务。',"News of the accession has reached [ROOT.GetCountry.GetName]. #bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#! has received the ministers’ support and left for [SCOPE.sCountry('new_jingyin_owner').GetCapital.GetName] to take charge of government. Officials at the former residence must complete the handover, while those accompanying the new ruler will serve at the new court.",reason='避免无明确颁诏主体的登极诏书，去除印信车马道具堆叠；保留现有人物/新拥有国scope。',source='M/events/nesnd_character_notifications.txt; M/localization/simp_chinese/nesnd_character_notifications_l_simp_chinese.yml:3',mechanic='Existing scopes retained verbatim; final root must verify event source filename/caller before application.')
add('nesnd_jingyin_departure_tt',None,"#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#! now rules [SCOPE.sCountry('new_jingyin_owner').GetName]. [ROOT.GetCountry.GetName] gains #bold $USM_benifit_of_an_emperor$#! for #v 10 years#!.",reason='英文槽中文回退；保留原动态引用、既有修正名和十年时长。',source='M/localization/simp_chinese/nesnd_character_notifications_l_simp_chinese.yml:4',mechanic='Only reports existing benefit; no monarch scope invented.')
proposals['nesnd_jingyin_departure_desc']['source']='M/events/usm_civilwar_events.txt:2635; M/common/scripted_triggers/nesnd_character_notification_triggers.txt:4; M/common/scripted_effects/nesnd_character_notification_effects.txt:20'
proposals['nesnd_jingyin_departure_desc']['mechanic']='Existing saved country/character scopes guarded by notification trigger, ownership and alive checks. Generic fallback permits any valid new capital; GNG->Nanjing uses the separate original-author branch.'
# Correct inspected line anchors; preserve old file rows through the separate inventory.
proposals['nesnd_japan.5.d']['source']='C/common/journal_entries/nesnd_japan.txt:64; C/common/scripted_triggers/nesnd_japan.txt:87; C/common/scripted_triggers/nesnd_jp_development.txt:12; C/events/nesnd_japan_events.txt:98'
proposals['nesnd_jp_food_supply_reason']['source']='C/common/scripted_triggers/nesnd_jp_industry.txt:57; author flavorCNE.3.d'
proposals['nesnd_jp_food_processing_reason']['source']='C/common/scripted_triggers/nesnd_jp_industry.txt:71'
proposals['nesnd_jp_development.2.d_military']['source']='C/common/scripted_triggers/nesnd_jp_politics.txt:26; author flavorCNE.3.d'
proposals['nesnd_per_claim_india_button']['source']='M/common/scripted_triggers/nesnd_per_campaign.txt:34'
for k in proposals:
    if k.startswith('nesnd_jp_foreign.2'):
        proposals[k]['source']='C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56'
add('nesnd_ten_continuity_bar_detail','最初三个月的地方汇报送齐后，四项生计条件达标，且林场、渔场、铁矿、工具厂、纺织厂或食品厂中至少一处配员达到#v 75%#!并无原料短缺，每月增加#p 1#!。条件中断时连续月份归零。完成后当地获得#v 24个月#!的#p +10%#!资质获取。\\n\\n全国制度改革仍由$je_reform_indies$推进。','After the first three months of local reports, gain #p 1#! per month with all four livelihood requirements met and at least one logging camp, fishery, iron mine, tooling workshop, textile mill or food industry #v 75%#! staffed without input shortages. A failure resets the consecutive-month count. Completion grants #p +10%#! qualifications gain locally for #v 24 months#!.\\n\\nNational institutional reform proceeds through $je_reform_indies$.',reason='将samples改成地方汇报并保留被旧英译漏掉的国家改革日志引用；数字和效果不变。',source='M/common/scripted_triggers/nesnd_tenasserim.txt:10; M/common/scripted_effects/nesnd_tenasserim.txt',mechanic='Three observation months then six healthy months; local modifier only.')
add('nesnd_ten_conditions_bar_detail',None,"Unemployed workforce: #v [Country.MakeScope.Var('nesnd_ten_unemployment').GetValue|%1]#!\\nWorkforce below the starvation threshold: #v [Country.MakeScope.Var('nesnd_ten_starving').GetValue|%1]#!\\nEmployed and below the starvation threshold: #v [Country.MakeScope.Var('nesnd_ten_working_hungry').GetValue|%1]#!\\nWorkforce household [concept_sol]: #v [Country.MakeScope.Var('nesnd_ten_sol').GetValue|1]#!\\n[concept_market_access]: #v [Country.MakeScope.Var('nesnd_ten_access').GetValue|%1]#!\\n\\nRequirements: unemployment at most #v 12%#!; at most #v 25%#! below the starvation threshold and living standards of at least #v 6.5#!; market access of at least #v 85%#!; peace and no active [concept_bankruptcy] penalty. Shares are calculated from the workforce in our part of Tenasserim and updated monthly. Subsistence farmers count as employed.",reason='现有英译遗漏本国丹那沙林分母，且用代码式<=；补齐地域与scope边界，保留真正生效的bankruptcy override。',source='M/localization/english/replace/zzzzzz_nesnd_concept_clarity_l_english.yml:3; M/common/script_values/nesnd_tenasserim.txt',mechanic='Only DEI-owned Tenasserim state workforce, not national or whole foreign-held region.')

def filehash(p): return hashlib.sha256(p.read_bytes()).hexdigest()
source_records=[]
old_sources=json.loads((W/'reports/integrity-recheck-20261102/english/editorial-sources.json').read_text(encoding='utf-8'))
for x in old_sources:
    p=Path(x['file']); found=[(k,t,n) for k,t,n in parse(p) if k==x['key']]
    if not found: continue
    k,t,n=found[-1]
    source_records.append({'kind':x['kind'],'path':str(p),'key':k,'line':n,'sha256':filehash(p),'cached_sha_match':filehash(p)==x['sha256'],'text':t,'baseline_role':'Original author baseline / current native source, not current AI prose'})

delegated={'CNE_attrative_general_as_leader','nesnd_supply_status_bankruptcy'}
inventory=[]
for k,v in data.items():
    if k in delegated: decision='DELEGATED'; reason='CNE/USM reviewer owns this mixed-file key.'
    elif k in proposals: decision='REVISE'; reason=proposals[k]['reason']
    elif re.search('[\u4e00-\u9fff]',v.get('en','')): decision='REVISE_UNTRANSLATED'; reason='English still contains Chinese; requires completion.'
    elif not v.get('en') and v.get('zh'): decision='CHECK_MISSING_EN'; reason='No English counterpart in reviewed file set; check effective original/override.'
    else:
        decision='KEEP'; reason='Read in full; wording, actor and supplied canon are compatible with the observed script role. Labels/names retained; no new mechanism asserted.'
    if k.startswith('nesnd_jp_') or k in ['gov_nesnd_japan_lin_regency','gov_nesnd_japan_lin_regency_desc','RULER_TITLE_NESND_JAPAN_REGENT'] or k.startswith('nesnd_japan_reunification_'):
        applicability='C effective value shown; legacy E differs where occurrence is overridden by development file.'
    else: applicability='M source, proposals for E/C unless separately restricted.'
    inventory.append({'key':k,'decision':decision,'reason':reason,'zh':v.get('zh'),'en':v.get('en'),'occurrences':occurrences[k],'applicability':applicability,'proposed':proposals.get(k)})
for k,x in proposals.items():
    if x['new_key']: inventory.append({'key':k,'decision':'NEW_BRANCH_PROPOSAL','reason':x['reason'],'proposed':x})

R.mkdir(parents=True,exist_ok=True)
(R/'japan-qin-proposals.json').write_text(json.dumps(proposals,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'japan-qin-inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'japan-qin-sources.json').write_text(json.dumps(source_records,ensure_ascii=False,indent=2),encoding='utf-8')
snapshot=[{'path':str(p),'language':lang,'sha256':filehash(p),'key_count':len(parse(p))} for p,lang in files]
(R/'japan-qin-reviewed-files.json').write_text(json.dumps(snapshot,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
counts=Counter(x['decision'] for x in inventory)
summary={'inventory_keys':len(inventory),'proposals':len(proposals),'decisions':dict(counts),'files':len(files),'game':'1.13.11 / build 24799966 / catalog CURRENT / changed_count0','status':'EDITORIAL_PROPOSALS; ENGINE_NOT_RUN','read_only_game_files':True}
(R/'japan-qin-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False))
print('Incomplete:',[(x['key'],x['decision']) for x in inventory if x['decision'] in ('REVISE_UNTRANSLATED','CHECK_MISSING_EN')])

qa=[]
for k,x in proposals.items():
    zht=re.findall(r'\[[^\]]+\]|\$[^$\n]+\$|@[A-Za-z_]+!',x['zh'])
    ent=re.findall(r'\[[^\]]+\]|\$[^$\n]+\$|@[A-Za-z_]+!',x['en'])
    if sorted(zht)!=sorted(ent): qa.append({'key':k,'zh_tokens':zht,'en_tokens':ent})
(R/'japan-qin-token-review.json').write_text(json.dumps({'bilingual_dynamic_token_mismatches':qa,'untranslated_owned_keys':[],'note':'Token parity is a reference-preservation check, not a language-quality or engine test.'},ensure_ascii=False,indent=2),encoding='utf-8')
print('Dynamic token mismatches:',len(qa))
comparison=['# 日本、西秦—波斯与周边文本逐项审校','',
    '状态：EDITORIAL_PROPOSALS / ENGINE_NOT_RUN。只写WORK报告；未改MOD、E、C、技能或游戏。',
    f'共{len(inventory)}个键记录，{len(proposals)}项双语修改/新增分支建议。统计与每文件SHA见japan-qin-summary.json和japan-qin-reviewed-files.json。',
    '', '## 来源与本轮编辑决定','',
    '作者样本来自指定pre-update基准，直接回读并重新核SHA；当前原版为1.13.11/build24799966，catalog状态CURRENT。完整20条来源见japan-qin-sources.json。此前缓存的law_autocracy行号落在空行，已按实际键重新定位；未拿缓存摘要当原文。',
    '', '|类别|作者/原版样本|本轮应用|', '|---|---|---|',
    '|改革结果|flavorCNE.3.d将法律、劳动迁移与政治利益连成因果|日本军政结局写现有兵制/工场支持；不统一添无来源反对者和道德总结。|',
    '|承担者|flavorCNE.4.d具体区分旧社会、新贵、乡绅与社会中层|西秦安国胜利按实际effect写军队、小市民、知识分子、实业家，不把小市民改成勋贵地主。|',
    '|历史与行动者|flavorUSM.4.d的过去征战及现时军政关系|陈秦皇帝历史不删除；共和后常驻日志改过去时，奖掖对象保留皇族势力。|',
    '|政治选项|ce_french_support_dynasty_button_desc明确行动立场|外交成功答复陈述已得到的自治/独立/许可/资金，不只写依商定办法办理。|',
    '|英文JE|native je_meiji_restoration_reason；je_sick_man_bureaucracy_reason|用明确行为者和英语因果句重写；不逐个复制中文逗号，已发生/计划/条件分开。|',
    '|英文军政|native je_french_foreign_legion_reason|吕宋直接解释谁提供舰船、谁承担军费、何时同意；不反复铺陈册簿印信。|',
    '|UI数值|原作者ce_french_empire_oreleans_progress_bar_desc|金额、库存/每周流量、binding period与自动终止分别保留。所有引号/动态scope保留。|',
    '', '## 适用包与交接约束','',
    '- C_only：尚未部署的日本开发候选。包括JIM摄政、七地区统一结局；E/main仍九地区条件，严禁仅改文案偷换目标。',
    '- E_and_C：既有秦/波斯/吕宋/丹那沙林/地图等文本。',
    '- requires_branch：只有根任务补齐实际desc分支/回复类型scope后方能生效；新增localization键本身不会改变显示。',
    '- `.4.d_unavailable` 供波斯援助路线无法成立QE1朝贡关系时使用；默认`.4.d`只用于当下仍真实subject_of QE1。',
    '- 日本foreign.2六段分支需在clear_request之前保存request_kind；kind6吞并不发送该答复，不新加死对象引用。',
    '- 外国交涉external、供应supply、混合crisis和HNA由USM审校者负责；CNE_attrative_general_as_leader和混合文件中的supply_status_bankruptcy标DELEGATED。',
    '', '## 逐项对照','',
    '下列原稿是本次读到的有效键值。被日本开发覆盖的旧值仍保存在inventory的occurrences.original_value中，不能把旧层存在等同于生效。所有编辑改稿均为本轮提案，不冒称作者原作。','']
for k,x in proposals.items():
    original=data.get(k,{})
    comparison += [f'### `{k}`','',f"判定：返工 → 编辑提案通过；适用 `{x['apply_to']}`。未接入游戏。",'',
        '**原AI中文**：'+original.get('zh','（新增分支）'),'', '**原AI英文**：'+original.get('en','（新增分支）'),'',
        '**本轮中文**：'+x['zh'],'','**本轮英文**：'+x['en'],'',
        '**原因**：'+x['reason'],'','**来源**：'+x['source'],'','**实际机制**：'+x['mechanic'],'']
comparison += ['## 边界','',
    '审阅是逐条编辑判断。正则仅用于键清单、引用保留、SHA与未译回退检查，未据关键词自动判定作者风格。没有运行引擎，没有保证所有分支无BUG，也没有验证实际窗口排版。新人物对话未添加；秦军府、日本幕府/军府和合法国际盟约不因词形被机械替换。']
(R/'writing-comparison-japan-qin.md').write_text('\n'.join(comparison),encoding='utf-8')
findings=[
 {'id':'JP01','severity':'P1','kind':'canon_and_branch','keys':['nesnd_japan.1.d','nesnd_japan.3.d'],'observed':'Effective legacy text promises direct imperial rule, while C implements Emperor nominally retained and regent conducting government.','source':str(C/'events/nesnd_japan_events.txt')+':6,84','disposition':'C-only proposals; do not silently certify E old behavior as repaired.'},
 {'id':'JP02','severity':'P1','kind':'effect_mismatch','keys':['nesnd_japan.5.d'],'observed':'C completion requires independence and seven Honshu regions, but result says Honshu, Kyushu and Shikoku are united. E still has the old nine-region requirement.','source':str(C/'common/journal_entries/nesnd_japan.txt')+':64; '+str(C/'common/scripted_triggers/nesnd_japan.txt')+':87','disposition':'C-only result rewrite. E nine-island prose retained until corresponding code changes.'},
 {'id':'JP03','severity':'P2','kind':'premature_fact','keys':['nesnd_jp_food_processing_reason'],'observed':'Canneries technology and operating cannery PM are completion conditions, but the active JE can appear before them.','source':str(C/'common/scripted_triggers/nesnd_jp_industry.txt')+':70-76','disposition':'Describe canning as prospective industry, not guaranteed present operation.'},
 {'id':'JP04','severity':'P2','kind':'outcome_visibility','keys':['nesnd_jp_foreign.2.d'],'observed':'Kinds1/2/3/4/5/7 all show generic agreement; request kind is erased after trigger_event. Kind6 annex intentionally skips reply.','source':str(C/'common/scripted_effects/nesnd_jp_foreign.txt')+':56-108; '+str(C/'events/nesnd_jp_foreign.txt')+':29','disposition':'Save kind scope before cleanup; six proposed descs. No new union success popup referring to dead partner.'},
 {'id':'QE01','severity':'P2','kind':'government_lifecycle','keys':['nesnd_qe1_court_journal_reason','nesnd_qe1_unity_journal_reason','nesnd_qe1_coup_crown_button_desc','nesnd_qe1_coup_literati_button_desc'],'observed':'Court remains eligible under presidential republic/custom proportional voting; imperial ruler narration and preserve throne/abolish throne are not universal entry facts.','source':str(M/'common/scripted_triggers/nesnd_qe1_campaign.txt')+':20-21; '+str(M/'common/scripted_buttons/nesnd_qe1_court.txt')+':6-7','disposition':'Keep imperial-house faction/history; use government-neutral action and historical tense where needed.'},
 {'id':'QE02','severity':'P2','kind':'mechanic_description','keys':['law_nesnd_qe1_proportional_representation_desc'],'observed':'Description treats literacy as eligibility requirement; custom law sets wealth threshold10 and literacy voting weight50.','source':str(M/'common/laws/nesnd_qe1_laws.txt')+':11','disposition':'Separate property franchise from literacy vote weight; do not claim literal district seat allocation.'},
 {'id':'QE03','severity':'P2','kind':'wrong_affected_actor','keys':['nesnd_qe1.1.d','nesnd_qe1_economy_push_button_desc'],'observed':'Economic winner affects Armed Forces and Petite Bourgeoisie, not Landowners; economy push penalizes Armed Forces and Rural Folk.','source':str(M/'common/static_modifiers/nesnd_qe1_agendas.txt')+':2-8; '+str(M/'common/scripted_buttons/nesnd_qe1_agendas.txt')+':5','disposition':'Name the actual affected constituencies; preserve existing mechanical labels.'},
 {'id':'PER01','severity':'P1','kind':'missing_actor_guard','keys':['nesnd_per.1.d','nesnd_per.2.d','nesnd_per.3.d'],'observed':'Original nesnd_per_aid_live checks route/future only; missing, hostile or invalid-overlord Qin can still appear as sending aid.','source':str(M/'common/scripted_triggers/nesnd_per_campaign.txt')+':5; '+str(M/'events/nesnd_per_campaign.txt')+':2-18','disposition':'Root explicitly plans exists/alive QE1, no has_war_with QE1, if subject direct QE1; event cancellation when aid_live false. Existing received six-month help persists. Not verified here after root mutation.'},
 {'id':'PER02','severity':'P2','kind':'result_branch','keys':['nesnd_per.4.d','nesnd_per.4.d_unavailable'],'observed':'Aid-route completion may fail to create/retain Qin tributary relationship, but outcome text was generic and did not distinguish this.','source':str(M/'common/scripted_effects/nesnd_per_campaign.txt')+':22-40','disposition':'Root to branch on actual current subject_of QE1. Progress must still complete if Qin disappears; no deadlock added.'},
 {'id':'PER03','severity':'P2','kind':'geography_and_actor','keys':['nesnd_per_claim_india_button','nesnd_per_claim_levant_button_desc','nesnd_per_claim_egypt_button_desc','nesnd_per_claim_arabia_button_desc','nesnd_per_claim_central_asia_button_desc','nesnd_per_claim_india_button_desc'],'observed':'India targets include Delhi/Agra outside Indus basin; diplomatic notes are addressed to states, not geographical regions.','source':str(M/'common/scripted_triggers/nesnd_per_campaign.txt')+':34; '+str(M/'common/scripted_effects/nesnd_per_campaign.txt')+':42','disposition':'Wider northwestern India label; name governments as recipients, without inventing historical title.'},
 {'id':'TEN01','severity':'P2','kind':'incorrect_generalization','keys':['nesnd_ten_abolish_button_desc','nesnd_ten_build_button_desc'],'observed':'Abolition activates Slavery Banned, not merely debt-contract separation. Existing logging staffing requirement applies whenever a logging camp exists, including first commission.','source':str(M/'common/scripted_buttons/nesnd_tenasserim.txt')+':25-29; '+str(M/'common/scripted_triggers/nesnd_tenasserim.txt')+':78-92','disposition':'Describe slavery generally; require any existing logging camp staffed before expansion. No code changes.'},
 {'id':'MAP01','severity':'P2','kind':'developer_text','keys':[k for k in proposals if k.startswith('nesnd_refine_water_')],'observed':'Four waterworks descriptions explain post-split allocation and retained design; English repeats Chinese.','source':str(M/'localization/simp_chinese/replace/zz_nesnd_map_refinement_l_simp_chinese.yml')+':9-25; '+str(M/'common/state_traits/nesnd_refinement_water.txt'), 'disposition':'Describe irrigation/infrastructure benefits; preserve actual numbers and state locations.'},
 {'id':'LANG01','severity':'P2','kind':'untranslated','keys':list(phi_en),'observed':'All79 English Philippines values are Chinese fallback. Map/state labels also contain fallback, not intentional English proper-name practice.','source':str(M/'localization/english/nesnd_phi_finance_l_english.yml'), 'disposition':'All79 proposals completed, preserving 8000/3000 and8700/3700 routes,12months,20ships, bilateral consent and political-allegiance independence of B.'},
]
(R/'japan-qin-findings.json').write_text(json.dumps(findings,ensure_ascii=False,indent=2),encoding='utf-8')
overview=['# 日本、西秦—波斯与周边审校：发现与边界','',f'审阅{len(inventory)}个唯一键（含7个新增分支），提出{len(proposals)}项建议。逐项对照见writing-comparison-japan-qin.md；机器可读建议、原值、来源、SHA分别见同目录japan-qin-*.json。','',
 '本报告只读实际游戏源码和作者资料。报告产物不改变E/C/主MOD；源码版本1.13.11/build24799966。无游戏运行，无“零BUG”认证。','',
 '|编号|问题|处理|','|---|---|---|']
for x in findings: overview.append('|'+x['id']+'|'+x['observed']+'|'+x['disposition']+'|')
overview += ['', '未判为缺陷的例子：秦身份衰退确实把所选本国州约半数西域汉羌同步改为目标文化与宗教（identity effect第35–40行）；原句半数分母正确，予以保留。日本国际盟约、军府、幕府和各府指当地政权时合法；没有机械改成礼法或各省。日本政治分支的代议/军府/君主条件已分别核读；当前正文不再无条件硬写丰臣家/先前战胜。', '', '所有KEEP为本轮来源与文意判断，不能保证任意未来存档、游戏更新或未读外围脚本的行为。根任务应用requires_branch后仍须核对新的有效覆盖键、延迟scope和本次源码指纹。']
(R/'japan-qin-findings.md').write_text('\n'.join(overview),encoding='utf-8')
