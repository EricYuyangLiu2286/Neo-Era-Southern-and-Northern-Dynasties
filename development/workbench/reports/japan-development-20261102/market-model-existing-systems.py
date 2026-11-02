from pathlib import Path
import json,re,hashlib
M=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/mod/Neo-Era Southern and Northern Dynasties')
W=M.parent.parent/'nesnd-workbench'
C=W/'exports/japan-development-20261102-a'
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
R=Path(__file__).parent
DOC=W/'references/engine-docs-1.13.11-20261031'
families=('nesnd_supply','nesnd_external','nesnd_phi_finance','nesnd_tenasserim')
files=sorted(p.relative_to(M).as_posix() for base in ('common','events','localization') for p in (M/base).rglob('*') if p.is_file() and any(f in p.name for f in families))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ln(root,f,needle):return next(i for i,s in enumerate((root/f).read_text(encoding='utf-8-sig').splitlines(),1) if needle in s)
def link(root,f,line=None):return f'[{f}{":"+str(line) if line else ""}](<{(root/f).as_posix()}{":"+str(line) if line else ""}>)'
rx=re.compile(r'^\s*([^\s:#]+):\s*(?:\d+\s*)?"(.*)"\s*$')
loc={}
for lang in ('simp_chinese','english'):
    loc[lang]={}
    for p in sorted((M/'localization'/lang).rglob('*.yml'),key=lambda p:('replace' in p.parts,p.name,str(p))):
        for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
            match=rx.match(line)
            if match:loc[lang][match[1]]={'text':match[2],'file':p.relative_to(M).as_posix(),'line':n}
old='''nesnd_supply_diplomacy_ready = {
    OR = { has_variable = nesnd_supply_self_reliance nesnd_supply_partner_valid = yes }
}'''
new='''nesnd_supply_diplomacy_ready = {
    OR = {
        capital.market = { participants >= 2 }
        has_variable = nesnd_supply_self_reliance
        nesnd_supply_partner_valid = yes
    }
}'''
old_clear='''nesnd_supply_clear_partner = {
    remove_variable = nesnd_supply_partner
    remove_variable = nesnd_supply_partner_sponsor
    remove_variable = nesnd_supply_pending
    remove_variable = nesnd_supply_pending_sponsor
    remove_variable = nesnd_supply_trade_pending
    set_variable = { name = nesnd_supply_weeks value = 0 }
}'''
new_clear=old_clear.replace('    set_variable = { name = nesnd_supply_weeks value = 0 }\n','')
changes=[
{'file':'common/scripted_triggers/nesnd_supply_triggers.txt','find':old,'replace':new,'count':1,'reason':'Read actual current capital market participants. A shared market already provides the commercial framework; do not require a fictitious procurement handshake. Preserve independent-market diplomatic policy choices.'},
{'file':'common/scripted_effects/nesnd_supply_effects.txt','find':old_clear,'replace':new_clear,'count':1,'reason':'Ending an optional diplomatic contact does not interrupt existing common-market buy/sell orders. Actual market changes and genuinely failed live requirements retain their existing weekly reset.'}
]
P={}
def add(k,z,e,why):
    P[k]={'zh':z,'en':e,'reason':why,'mechanic':'Display only; code changes above are a prerequisite for descriptions of automatic shared-market qualification. No goods stock, prepayment, purchase order or production effect is introduced.','current_zh':loc['simp_chinese'][k],'current_en':loc['english'][k]}
add('nesnd_supply_status_diplomacy','商贸联络的安排尚未议定。可以派使接洽，也可以交由商人自行往来。\n$nesnd_supply_rules_link$'.replace('\n','\\n'),'Commercial contacts remain undecided. Send envoys to discuss them, or leave merchants to maintain their own dealings.\\n$nesnd_supply_rules_link$','Shared-market members now bypass this status automatically; independent-market political choice remains, without suggesting goods begin flowing only after acceptance.')
add('nesnd_supply_self','由商人自行往来','Leave Commerce to the Merchants','Actual effect only selects a policy flag and clears contacts. It does not improve production or jobs, so do not call it industrial reorganisation.')
add('nesnd_supply_self_desc','撤回专项使团与待答请求，由商人继续经营现有买卖。市场归属和已经签署的条约照旧。','Withdraw the special mission and pending requests, leaving merchants to continue their existing trade. Market membership and signed treaties remain unchanged.','Describe the actual clear_partner/self flag; no production, procurement, stock or access effect exists.')
add('nesnd_supply_invite_desc','派使与对方商议商业往来，争取更好的两国关系。现有市场中的买卖照常进行。','Send envoys to discuss commercial relations and improve diplomatic ties. Existing market exchange continues.','The first accepted contact changes relations by +25. It neither creates goods nor establishes a market connection.')
add('nesnd_supply_invitation_tt','商使将在#v 7日#!后抵达。使团任期#v 6个月#!，期间[concept_influence]#n −100#!。','The envoys arrive in #v 7 days#!. The mission lasts #v 6 months#! and applies #n −100#! [concept_influence] during that time.','State existing diplomatic influence cost; no fictitious purchase fee or commodity payment.')
add('nesnd_supply_accept_tt','建立商业联络；首次接受时，两国关系#p +25#!。','Establish commercial contacts. The first acceptance improves relations by #p 25#!.','Exact event1 first_contact_rewarded effect; do not claim guaranteed supply.')
add('nesnd_supply_end_contact_desc','召回专项使团，结束此次商业联络。现有市场中的买卖与已签条约继续有效。','Recall the mission and end these commercial contacts. Existing market exchange and signed treaties continue.','Contact is diplomatic, not a pipe that switches ordinary common-market production on or off.')
add('nesnd_supply_end_contact_tt','结束此次联络。若商贸安排因此中断，连续稳定周数重新累计；已经签署的正式条约仍依约履行。','End these contacts. If this leaves commercial arrangements unresolved, consecutive stable weeks restart; signed treaties remain in force.','No unconditional zero when shared-market arrangements remain valid; independent-market selection still follows live qualification.')
add('nesnd_supply_finish_desc','货源、工场、民生与商贸安排连续安定#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。','After supplies, employment, livelihoods and commercial arrangements remain stable for #v 12 weeks#!, first completion grants #p +100#! [concept_influence] for #v 2 years#!.','The reward is influence capacity, not extra goods or income; preserve exact +100/24-month modifier.')
add('nesnd_supply_finish_shared_desc','继续在现有共同市场中经营。各项条件连续维持#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。','Continue trading in the existing common market. Maintain all conditions for #v 12 weeks#! to gain #p +100#! [concept_influence] for #v 2 years#! on first completion.','The button only records completion. It does not create or preserve a new market treaty.')
add('nesnd_supply_finish_autonomous_desc','在本国掌管的市场中继续经营。各项条件连续维持#v 12周#!后，首次获得持续#v 2年#!的[concept_influence]#p +100#!。','Continue trading in the market our country already controls. Maintain all conditions for #v 12 weeks#! to gain #p +100#! [concept_influence] for #v 2 years#! on first completion.','Requires market.owner=root before click; no market secession happens here. Avoid saying the button takes control of the market.')
z=loc['simp_chinese']['nesnd_supply_rules']['text']
e=loc['english']['nesnd_supply_rules']['text']
z=z.replace('确定联络伙伴或依靠本国商帮，四项条件连续维持#v 12周#!。','处于共同市场时，商贸安排自动满足；本国单独掌管市场时，可确定联络伙伴或由商人自行往来。四项条件连续维持#v 12周#!。')
e=e.replace('Choose a commercial partner or rely on domestic merchants, and maintain all four conditions for #v 12 weeks#!.','A shared market automatically fulfils the commercial-arrangements requirement. A country alone in its market may choose a contact or leave dealings to its merchants. Maintain all four conditions for #v 12 weeks#!.')
add('nesnd_supply_rules',z,e,'Explain the actual market read and retained independent-market policy choice. Prices, local shortages and domestic specialisations remain unchanged; no autarky requirement is added.')
manifest=[]
for f in files:
    manifest.append({'file':f,'main_sha256':sha(M/f),'candidate_sha256':sha(C/f) if (C/f).exists() else None,'same':(C/f).exists() and (M/f).read_bytes()==(C/f).read_bytes()})
for c in changes:
    c['match_counts']={name:(root/c['file']).read_text(encoding='utf-8-sig').count(c['find']) for name,root in [('main',M),('candidate',C)]}
checks={'no_code_or_main_edits':True,'engine_run':False,'scopes_equal':all(sorted(re.findall(r'\[[^]]+\]',p['zh']))==sorted(re.findall(r'\[[^]]+\]',p['en'])) for p in P.values()),'exact_matches':all(v==c['count'] for c in changes for v in c['match_counts'].values()),'scope_files':len(files),'different_files':[x['file'] for x in manifest if not x['same']]}
payload={'status':'READ_ONLY_AUDIT_AND_REPAIR_PROPOSAL_NO_ENGINE_RUN','code_changes':changes,'localization':P,'checks':checks,'preserve':['PHI money_transfer, tribute changes, military exemptions, set_ship_owner_multiple and clear_ownership_transfer_fleet','Tenasserim start_building_construction, qualifications, enacted laws and cash compensation','Existing real external goods_transfer and money_transfer treaties; same-market production needs no new agreement','Supply current prices, country-local shortages, country-specific staffed buildings, unemployment, famine, grain conditions, durations and existing one-time reward flags'],'excluded_false_positive':{'good_vs_goods':'Do not normalise: current engine triggers.log:8930 documents good for can_create_treaty; effects.log:1030 documents goods for create_treaty. Native article required_inputs alone does not prove trigger input spelling is wrong.'},'manifest':manifest}
(R/'market-model-existing-systems-proposals.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
report='''# 现有南朝经济系统：共同市场模型审查

范围为当前主MOD（本轮文案提交38cf3ea后的加载目录）与日本候选 `japan-development-20261102-a` 的 Supply、External、PHI、Tenasserim四组脚本和双语本地化。只读审查，只输出报告与修正提案；未改游戏源码、主MOD、候选或技能，也未打开游戏。`catalog.py status`确认本机1.13.11／Steam build24799966、CURRENT、0变更。

## 结论

确认两处同根机制问题，均在现有Supply系统：

1. 共同市场已经发挥作用时，仍以“自行采购”或“收到商使答复”的旗标决定能否累计供需稳定期。市场价格、当地短缺和就业全都达标也会被第四格挡住。
2. 取消或失去外交联络直接清零稳定周数，即使国家仍处同一共同市场、实际商品供应和就业没有变化。

提案只改两个旧函数，并修正12个说明键。直接读取当前首都市场的参与国数量，至少两个成员时自动满足“商贸安排”；原有独立市场外交选择保留。取消联络不再直接归零；真实市场发生变化、战争、破产或任一实际门槛失效时，原有周度检查仍会归零。不会给共享市场成员自动补货、降军需成本或指定出口对象。

未发现需要删去的PHI“库存系统”：补贴是财政流量，贡赋是财政关系，交舰是既有舰船资产的所有权改变。Tenasserim的林场为正常政府建设，完工、招聘与生产进入真实市场。External的军械援助采用真实跨市场 goods_transfer 条约，而不是虚构政府仓库；这些机制全部保留。

## 原始来源与当前版本核对

官方DD37说明，共同市场成员的生产与消费共同形成买卖订单，基础设施和海上连接影响市场接入。它只用于解释共享供需，旧版贸易操作界面不作为1.13.11接口。[官方DD37](https://www.paradoxinteractive.com/games/victoria-3/news/dev-diary-37-market-expansion)

2025年3月27日DD143介绍1.9贸易重做：人口和建筑仍在国家市场买卖，世界市场提供自主跨市场贸易，贸易中心按盈利调整贸易量；国家间定向协议仍另有机制。当前源码进一步确认了这些类别。[官方DD143](https://steamcommunity.com/games/529340/announcements/detail/524212840420081890)

'''
native=[('localization/english/concepts_l_english.yml',1652,'concept_market：同一市场州之间交易；市场接入决定连接程度。'),('localization/english/concepts_l_english.yml',1658,'concept_market_access：影响州产出和消费形成的订单及地方价。'),('localization/english/concepts_l_english.yml',2365,'concept_sell_orders与2371 buy_orders：按市场内各州生产/消费形成。'),('localization/english/concepts_l_english.yml',170,'concept_trade：自主世界市场贸易与国家定向条约并存。'),('localization/english/concepts_l_english.yml',178,'trade_privilege给另一市场参与国贸易优势，并不分配一个库存。'),('localization/english/concepts_l_english.yml',1178,'foreign investment：产权收益和当地劳动力/税收/市场分开，货物仍属当地市场。'),('common/journal_entries/00_player_objectives_economic_dominance.txt',121,'当前country JE实例：market={owner=ROOT participants>=8}。由此验证participants为实际市场成员读数。'),('common/journal_entries/04_india_non_cooperation.txt',56,'当前JE直接比较 root.market 与 top_overlord.market，之后读取市场卖单；不是宗属旗标替代市场。'),('common/journal_entries/00_trade_route_event_missions.txt',50,'原版以首都商品补贴政策及capital.market粮价检查经济结果，不建立库存。'),('common/history/treaties/00_historical_treaties.txt',233,'法国援埃及：create_treaty→goods_transfer small_arms quantity10，证明跨市场定向援助确有同类。'),('common/treaty_articles/13_goods_transfer.txt',1,'required inputs、市场可达、非关税同盟从属成员、运输/出口上限与冻结条件。'),('common/treaty_articles/25_trade_privilege.txt',1,'两市场所有者的贸易优势条款，内有junior限制和履行条件。'),('common/treaty_articles/05_transfer_money.txt',1,'quantity为财政转移，付款国default导致冻结；没有商品库存输入。'),('events/agitators_events/land_ownership_law_events.txt',1576,'原版state scope start_building_construction调用，正常排队建设。'),('common/buildings/09_misc_resource.txt',1,'logging camp→required_construction、PM groups、图标/资源。'),('common/production_method_groups/09_misc_resource.txt',1,'林场基础PM组→simple_forestry/saw_mills。'),('common/production_methods/09_misc_resource.txt',1,'林场PM workforce_scaled wood30；saw_mills投入tools5、产出wood60，实际雇员决定生产，而非点按钮发木材。')]
for f,n,ex in native:report+=f'- {link(G,f,n)}：{ex} SHA256 `{sha(G/f)}`。\n'
report+=f'\n引擎文档：{link(DOC,"effects.log",37128)}的set_ship_owner_multiple说明真实舰船批量转移，并须clear_ownership_transfer_fleet；{link(DOC,"triggers.log",8930)}与{link(DOC,"effects.log",1030)}分别记录条约检查与创建格式。\n'
report+='''
## 逐系统结果

### Supply：需要修正

`nesnd_supply_inputs_ready`从当前 `capital.market`读取paper/tools/small_arms价格，并按root国家检查本地短缺。`jobs_ready`分别要求湖广大学与军营、四川工具厂及铁矿/林场、广西纸厂及林场、东洲港口与官署。这些是产业与行政专业能力门槛，**没有要求每国自建所有投入品**，应保留。`livelihood_ready`看就业、饥荒及共同市场粮价，也接受共同市场供应。

错误集中在商贸旗标门槛与联络清理。真实调用链如下：

'''
supply_refs=[('common/journal_entries/nesnd_supply_journals.txt','scripted_button = nesnd_supply_invite_hna'),('common/scripted_triggers/nesnd_supply_triggers.txt','nesnd_supply_diplomacy_ready ='),('common/scripted_triggers/nesnd_supply_triggers.txt','nesnd_supply_all_ready ='),('common/scripted_effects/nesnd_supply_effects.txt','nesnd_supply_clear_partner ='),('common/scripted_effects/nesnd_supply_effects.txt','nesnd_supply_refresh ='),('common/scripted_effects/nesnd_supply_effects.txt','capital.market = var:nesnd_supply_market'),('common/scripted_buttons/nesnd_supply_buttons.txt','nesnd_supply_self ='),('events/nesnd_supply_events.txt','nesnd_supply.1 ='),('events/nesnd_supply_events.txt','nesnd_supply.3 ='),('common/static_modifiers/nesnd_supply_modifiers.txt','nesnd_supply_verified =')]
for f,n in supply_refs:report+=f'- {link(M,f,ln(M,f,n))}。\n'
report+='''
`self`实际只清除partner/pending、设置self_reliance并刷新；没有建厂、改PM、改就业、增产或转移货物。因而不能将其改名“整顿本国生产”来掩盖没有生产效果。提案将其准确表述为交由商人继续往来。商使首次接受的实际政治收益是关系+25，六个月−100影响力；完成奖励是24个月+100影响力，不是商品或收入收益。已经存在的外交联系与双向trade_privilege可作为可选外交行动留下，不把它们当作共同市场供需的前提。

### External：机制保留；排除一项初步误报

钱款条约为每周500；军械条约是quantity10的small_arms goods_transfer。创建之前重复检查can_create_treaty以及供应者市场价格/本地短缺，原生条约定义另负责市场可达、成员身份、运输与进出口上限。它不设置“军械库存”、预付款库存或自定义交货量，也没有用buff冒充商品。待答请求失效时清理的是外交提议，不删除产业；已签条约由原生机制继续履行。

审查中初看见can_create_treaty写 `good`、create_treaty写 `goods`，曾向主代理提示可疑。继续读取当前引擎完整文档后立即撤回：triggers.log明确使用单数good，effects.log明确使用复数goods。**不得对这六处检查盲改为goods**。当前本体历史条约只有create侧的goods实例，不能据此反推can_create侧语法。无本轮引擎运行，不给这项接口另立成功或失败结论。

'''
for f,n in [('common/journal_entries/nesnd_external_journal.txt','nesnd_external_policy ='),('common/scripted_triggers/nesnd_external_triggers.txt','nesnd_external_can_offer_arms ='),('events/nesnd_external_events.txt','nesnd_external.3 ='),('events/nesnd_external_events.txt','nesnd_external.6 ='),('common/scripted_effects/nesnd_external_effects.txt','nesnd_external_cleanup =')]:report+=f'- {link(M,f,ln(M,f,n))}。\n'
report+='''
### PHI：不删财政和舰船机制

PHI的relation_valid明确要求当前 `market = c:USM.market`、直属宗属及和平；这是军费协定适用关系，不是市场供需开关。四种补贴数额8000/3000/8700/3700经真实money_transfer支付，减贡和免役经独立外交协定处理。首次B路线将现有20艘战列舰转归USM，`b_transferred`防止续签重复交舰。`needed_crew`是舰员需求，绝非商品库存。

市场或宗属改变时，PHI军费协议停止或重新评估可以保留：它反映补贴的政治条款，不代表两市场之间商品从此完全断绝。当前文案写重新商议军费，与效果相符。既有舰船不回收、不重新创建、不删除；没有理由因本轮经济模型纠正重做已验证海军。

'''
for f,n in [('common/scripted_triggers/nesnd_phi_finance.txt','nesnd_phi_relation_valid ='),('common/scripted_effects/nesnd_phi_finance.txt','nesnd_phi_commit ='),('common/scripted_effects/nesnd_phi_finance.txt','nesnd_phi_finish_creation ='),('common/scripted_effects/nesnd_phi_finance.txt','set_ship_owner_multiple = c:USM'),('common/scripted_effects/nesnd_phi_finance.txt','nesnd_phi_clear_active =')]:report+=f'- {link(M,f,ln(M,f,n))}。\n'
report+='''
### Tenasserim：正常地方发展，保留

林场按钮按本国实际state排入一级政府建设，仍需建设力、财政、完工和招聘。`nesnd_ten_orders`仅累计该按钮委办过几次，最多2次；不是“商品订单库存”。林场PM产出进入该州实际市场，若DEI仍在USM共同市场，就自然参与USM共享卖单，不需要再发一份运木材给吴国的合同。

完成检查使用就业、家庭饥饿/生活水平、人口加权市场接入，以及至少一处适当非农建筑75%配员/无投入短缺。教习增加资质获取，补偿扣财政并给地主好感，法律按钮走真实enactment。停止专项只清理专项教习和连续月数；已排建设、既有产业、当前法案和已付补偿保留。没有本轮市场模型问题。

“南洋海船将染料运往江南”是作者世界中的地理与经济叙事，没有承诺某次按钮把一批存货交给USM，不应机械删除。产业专业化与不同地方市场价格仍然可以产生实际地理贸易关系。

'''
for f,n in [('common/journal_entries/nesnd_tenasserim.txt','nesnd_tenasserim_recovery ='),('common/scripted_effects/nesnd_tenasserim.txt','nesnd_ten_build ='),('common/scripted_triggers/nesnd_tenasserim.txt','nesnd_ten_can_build ='),('common/script_values/nesnd_tenasserim.txt','nesnd_ten_access_sum ='),('common/scripted_effects/nesnd_tenasserim.txt','nesnd_ten_cleanup =')]:report+=f'- {link(M,f,ln(M,f,n))}。\n'
report+='''
## 修复闭包与极值场景

|场景|修复后预期|保留的限制|
|---|---|---|
|HNA/SIH/GNG与USM同一实际市场|第四格自动满足；可凭真实货源、专业建筑与民生累计12周|仍会因价格、当地短缺、招工、失业、粮价、战争/破产不合格而停|
|仍是USM附属但获独立市场|不按宗属假定共享；依当前参与国数与原有独立市场选择判断|消费可来自本市场及自主世界市场贸易，不要求全套自给工厂|
|HUS仍在北朝共同市场|直接读取其实际市场，完全不硬编码USM|HUS本有港口/官署、硬木条件保留|
|取消商使，市场和经济条件没变|不直接归零；共同市场第四格仍成立|尚未付款的商业请求可清理，真实已签条约不受影响|
|退出共同市场，首都市场确实改变|原有market比较将连续周数重算；旧联络按现有政治关系校验|已建建筑、在建工程、人口、PM、舰船不删除|
|独立市场失去唯一已选伙伴且未选自行往来|现有all_ready不满足，依原规则重算|这是保留的外交安排选择，不写成物资库存归零|
|JE已完成后市场改变|不重新激活已经完成的JE，不撤销产业|本有一次奖励与期限保持；没有新的快照/采购系统|
|外援签署前加入别人市场|保留真实can_create_treaty再次校验|不绕过原生同盟从属成员和市场可达条件|

## 文案对读

前一轮已读取并保存的成熟作者样本为备份ce_usm_events的flavorUSM.4.d（海贸、兵财与政治地位的因果）、ce_usm_conflicts_within_reason（读书议政的社会过程）。本轮只调整操作事实和必要条件，不再次重写这些叙事。下面逐项列出旧句、提案与原因；仅编辑提案通过，尚未接入游戏。

|键|当前中文|提案中文|原因|
|---|---|---|---|
'''
for k,p in P.items():report+=f'|`{k}`|{p["current_zh"]["text"].replace("|","／")}|{p["zh"].replace("|","／")}|{p["reason"]}|\n'
report+='\n## 精确代码修改\n\n'
for c in changes:report+=f'文件 `{c["file"]}`，M/C匹配数量 `{c["match_counts"]}`。以以下块替换当前同名块：\n\n```text\n{c["replace"]}\n```\n\n'
report+='该两处与双语文案详见同目录JSON。未对External、PHI、Tenasserim提出删除或机制改写。\n\n## M/C逐文件指纹\n\n|文件|一致|主MOD SHA256|\n|---|---|---|\n'
for x in manifest:report+=f'|`{x["file"]}`|{x["same"]}|`{x["main_sha256"]}`|\n'
report+='\n检查结果：`'+json.dumps(checks,ensure_ascii=False)+'`。精确文本匹配和双语引用对等是外部检查，不是游戏内验收。\n'
(R/'market-model-existing-systems.md').write_text(report,encoding='utf-8')
print(json.dumps({'report_chars':len(report),'proposal_keys':len(P),'checks':checks},ensure_ascii=False))
