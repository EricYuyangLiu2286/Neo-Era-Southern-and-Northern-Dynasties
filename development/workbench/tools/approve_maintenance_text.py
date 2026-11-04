"""Root editorial decisions after reading the submitted bilingual drafts."""
from pathlib import Path
import json
R=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/branch-naming-cleanup-20261104')
draft=json.loads((R/'proposed-loc-edits.json').read_text(encoding='utf-8-sig'))
conditions=json.loads((R/'proposed-condition-text.json').read_text(encoding='utf-8-sig'))
rewrites={}
def pair(key,zh,en):
    rewrites[('simp_chinese',key)]=zh
    rewrites[('english',key)]=en
pair('nesnd_prussian_rhine_reason',
'共同防卫把德意志诸邦的军队与普鲁士联系起来。柏林的参谋开始协调各邦的军备，法国和莱茵邦联也必须正视这股力量。共同承担的军费与防务，正使普鲁士在德意志获得更大的发言权。',
"Common defence has brought the armies of the German states into cooperation with Prussia. Staff officers in Berlin are coordinating their preparations, confronting France and the Confederation of the Rhine with a stronger force. Shared military commitments are giving Prussia a greater voice in German affairs.")
pair('nesnd_usa_continental_reason',
'联邦的扩张者自称白人美洲的保护者，要求夺取东洲的西部领地。边疆移民觊觎当地土地，工商集团则希望借欧洲资本兴建铁路与兵工厂。支持扩张的议员正争取拨款，准备以军备迫使东洲让步。',
"Federal expansionists call themselves the protectors of white America and demand the western territories of $HUS$. Settlers seek land, while business interests look to European capital to finance railways and armaments. Their allies in Congress are seeking the funds to force concessions from $HUS$.")
pair('nesnd_ottoman_recovery_reason',
'近西战争暴露了旧军制的弱点。如今西秦退出中原，伊斯坦布尔的军官主张趁势向东方扩张，夺回奥斯曼在伊斯兰世界的威望。\n\n坦志麦特留下的成果与阻力都将影响这支军队。政府既要筹措军费，也要在新的领土要求和军队整顿之间分配力量。',
"The Near Western War exposed the weaknesses of the old army. With Western Qin driven out of central China, officers in Istanbul urge an advance eastward to restore Ottoman standing in the Islamic world.\\n\\nThe achievements and failures of the Tanzimat will shape this army. The government must raise the money and decide how much strength to devote to territorial demands and how much to military reform.")
# Store Clausewitz localization newlines as literal backslash-n, not YAML line breaks.
rewrites[('simp_chinese','nesnd_ottoman_recovery_reason')]=rewrites[('simp_chinese','nesnd_ottoman_recovery_reason')].replace('\n','\\n')
pair('nesnd_ottoman_reform_army_desc','仿效秦国的编制、训练与补给办法，整顿陆军。',"Reorganize the army along Qin lines, adopting its methods of training and supply.")
pair('nesnd_khanate_emergence_reason',
'美国内战使大平原的统治陷入动摇。东洲的新登记法又激起原住民的不满，各共同体的首领开始联络旧日起义的支持者，准备在草原建立自己的汗国。',
"The American Civil War has shaken authority on the Great Plains. Dongzhou's new registration law has stirred Indigenous resentment, and community leaders are rallying supporters of the earlier uprising to establish a khanate of their own.")
pair('nesnd_hus_registration.1.d',
"[SCOPE.sCountry('nesnd_a2_khanate').GetName]已经建立。来自东洲与美国的原住民正在迁入新国，各共同体将拥立的新汗视作保卫土地的领袖。华盛顿与东洲政府都拒绝承认这次割地，草原上的战争迫在眉睫。",
"[SCOPE.sCountry('nesnd_a2_khanate').GetName] has been established. Indigenous communities from Dongzhou and the United States are settling there, looking to their new khan to defend their lands. Washington and the government of Dongzhou reject the loss of this territory. War on the Plains is imminent.")
pair('nesnd_khanate_survival_reason',
'美国与东洲都要求收回汗国的领土。新汗必须率领各共同体抵御两国进攻，守住迁民赖以安身的草原。',
"Both the United States and Dongzhou demand the khanate's territory. The new khan must lead its communities against both powers and defend the lands on which their people have settled.")
pair('nesnd_khanate_legacy_status','汗国已经建立。','The khanate has been established.')
pair('nesnd_native_khanate.3.d',
'从北方的草原到南方的群山，美洲已归于同一个政府。旧东洲政权不复存在，新的[ROOT.GetCountry.GetName]继承了它的国号，废除等级制度，以共和国的名义统治这片大陆。',
"From the northern plains to the southern mountains, the Americas now answer to one government. The old state of Dongzhou is gone. The new [ROOT.GetCountry.GetName] has taken its name, abolished its social hierarchy and proclaimed republican government across the continent.")
pair('nesnd_small_order_button_desc','巩固本国的法律、公共服务与防务。','Consolidate our laws, public services and defence.')
pair('nesnd_small_states.10.organise_tt',
'相关运动的支持权重#p +15%#!，权威#n −25#!，持续#v 12个月#!；受影响人群的#v 1%#!转为激进派。运动中若有本国支持者，其人气#p +10#!，持续#v 12个月#!。',
'The relevant movement gains #p +15%#! support weight and Authority falls by #n 25#! for #v 12 months#!. #v 1%#! of the affected population becomes Radical. A local character supporting the movement, if available, gains #p +10#! Popularity for #v 12 months#!.')
pair('nesnd_small_states.10.suppress_tt',
'相关运动的支持权重#n −15%#!，权威#n −50#!，持续#v 12个月#!；受影响人群的#v 2%#!转为激进派。',
'The relevant movement loses #n 15%#! support weight and Authority falls by #n 50#! for #v 12 months#!. #v 2%#! of the affected population becomes Radical.')
for row in draft:
    k=(row['lang'],row['key'])
    if k in rewrites:continue
    text=row['new']
    if row['key'].startswith('nesnd_small_states.10.promise_'):
        if row['lang']=='simp_chinese':
            text=text.replace('兑现或失约后有一次有限的人群反应。','按期立法可争取效忠；到期仍未兑现且诉求未解，会增加激进派。')
        else:
            text=text.replace('fulfilment or failure produces a limited, one-time response.','fulfilling the promise gains Loyalists; an unfulfilled demand at the deadline gains Radicals.')
        rewrites[k]=text
    if row['key'] in ('nesnd_native_restoration_war_reason','nesnd_american_restoration.1.d'):
        rewrites[k]=text.replace('共和国','中央政府').replace('the republic','the central government')
approved=[]
for row in draft:
    k=(row['lang'],row['key']);row=dict(row)
    if k in rewrites:
        row['astra_draft']=row['new'];row['new']=rewrites[k];row['root_verdict']='REWRITTEN_AND_REREAD'
        row['root_reason']='Remove implementation commentary, redundant conclusions, inaccurate regime assumptions or imprecise rule language.'
    else:row['root_verdict']='ACCEPTED_AFTER_ROOT_READING'
    row['status']='ROOT_EDITORIAL_APPROVED_PENDING_SOURCE_VALIDATION'
    approved.append(row)
existing={(x['lang'],x['key']) for x in approved}
for (lang,key),value in rewrites.items():
    if (lang,key) not in existing:
        # Root's new HUS event edit is explicitly tracked, rather than silently added to the draft.
        approved.append({'lang':lang,'key':key,'new':value,'root_verdict':'ROOT_REWRITE','status':'ROOT_EDITORIAL_APPROVED_PENDING_SOURCE_VALIDATION'})
for row in conditions:
    row['root_verdict']='ACCEPTED_AFTER_PREDICATE_AND_TEXT_READING'
    row['status']='ROOT_EDITORIAL_APPROVED_PENDING_SOURCE_VALIDATION'
    approved.append(row)
for row in approved:
    assert '\n' not in row['new'], row['key']
(R/'root-approved-localization.json').write_text(json.dumps(approved,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'root-editorial-review.md').write_text('''# 主代理逐条编辑复核

已阅读246条Astra中英候选与64条条件提示；没有直接采信代理的PASS或统计。重写普鲁士末尾无信息转折、美国重复经济常识及HUS固定共和国称谓、奥斯曼近西战争背景/军制按钮、汗国建国/生存/终局的开发式数字叙述，以及小国“原生/有限反应/实际支持者”等词。条件提示逐项对照29天、6/12月、5年、40/60份额及兵营基准+25；不在缺值分支读取goal变量。

有意保留必要条件与实际效果，不以“简短”删掉费用/期限/互斥/失败。地方福利不是定额采购；正文不替按钮重复数据库说明。最终值与返工轨迹见root-approved-localization.json；依然必须通过唯一key、源谓词、动态数据上下文和实机检查。

重复key的root取值：GNG为Huai；地权改革进度+1/+2按实际数值；日本重统一按当前本州七地区、林摄政保留天皇名位；南朝bar按当前支持/新政分数而非国家计数；HUS建国采用A2真实创建链后文；文化动荡按unity分组。停用的CNE旧腐化JE保留作者原始叙事，不保留“已并入另一个日志”的开发备注。秦bar保留已修的蓝/金两端说明，而非Luna建议回退；这由root核实际double_sided_gold后裁定。英文文件中的旧中文覆盖去除，保留对应英文有效文案。
''',encoding='utf-8')
print({'approved_entries':len(approved),'root_rewritten':sum(x['root_verdict'].startswith('REWRITTEN') or x['root_verdict']=='ROOT_REWRITE' for x in approved)})
