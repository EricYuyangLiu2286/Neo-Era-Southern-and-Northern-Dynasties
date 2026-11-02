from pathlib import Path
import runpy,json,re
R=Path(__file__).parent
ns=runpy.run_path(str(R/'usm-proposals.py'))
I,P,add,short=ns['I'],ns['P'],ns['add'],ns['short']
def en(k,e,z=None,reason='修复英文槽中的中文回退；按当前中文有效文本译出，不沿用过时英文说明。',mechanic='现有调用、条件和效果不变。'):
    add(k,z if z is not None else I[k]['zh']['text'],e,reason,mechanic)

# External affairs: these are real treaties and foreign alignments, never a domestic Constitution.
ext={
'choose_wu':'Contact the Wu Government','choose_sih':'Contact Sichuan','choose_hus':'Send Republican Envoys to Dongzhou','choose_fra':'Write to France',
'hus_title':'A Letter from Across the Sea','fra_title':'Between Two Seas','qe1_title':'The Mountains of Bashu','sha_title':'Dispatches in the Snow','bur_title':'The River Mouth and the Court','mug_title':'The Southern Coast','gbr_title':'After the Blockade','rus_title':'Dispatches from the East',
'follow':'Prepare our response and make further enquiries.','decline':'Attend to our own affairs first.',
'choose_opposition':'Contact the Anti-Wu Leader','offer_money':'Provide Military Funds','offer_arms':'Negotiate Arms Deliveries',
'status_choose':'Select a partner, then consider the available terms.',
'status_selected':"Partner: #bold [ROOT.Var('nesnd_external_target').GetCountry.GetName]#!. The proposed funds and arms are shown in the relevant offers.",
'status_pending':'Our envoy awaits a reply. An unsigned request may still be withdrawn.',
'status_committed':'The treaty has been signed. Its fulfilment, suspension and withdrawal terms are available in the treaty interface.',
'money_title':'An Offer of Funds','arms_title':'An Offer of Arms','accept':'Approve the treaty.','refuse':'Decline the offer.',
'request_money':'Request Financial Assistance','request_arms':'Request Arms','request_money_title':'A Request for Assistance','request_arms_title':'An Arms Request from Abroad',
'accept_request':'Approve the assistance and sign.','refuse_request':'Our resources are needed elsewhere.',
'reconsider':'Choose Another Partner','mysore':'Raise the Mysore Question','cancel_request':'Withdraw the Request','dismiss':'Set the Matter Aside','resume':'Reopen Southern Diplomacy',
'end_title':'Our Envoys Return','end_option':'Close the mission and fulfil our agreements.'}
for k,e in ext.items():en('nesnd_external_'+k,e)
en('nesnd_external_hus_desc','News of the Southern succession has reached Dongzhou. The Zheng maritime empire that we fought for independence is again divided over who should rule it. Its opponents may seek support from our republic, while merchants watch for changes to the ports and routes on which they depend.\\n\\nWe can pursue those openings, but assistance abroad will draw on our own treasury and industry. The government must decide which relationships serve the republic and which commitments it can sustain.',
'南朝易代的消息传到了东洲。曾与我们争夺独立的郑氏海上帝国，如今又因谁应当主持天下而分裂。反对郑氏的势力可能向共和国寻求援助，商人则在关注港口与航路的去向。\\n\\n我们可以借此扩大对外交往，援助别国却须动用自己的国库与工厂。政府应当判断哪些关系有利于共和国，又能承担多少承诺。',reason='去国库/工厂各交账目的机械隐喻；具体独立战争记忆与现实财力约束。')
en('nesnd_external_fra_desc','Southern envoys seek recognition and the continuation of old agreements, while India remains divided by disputes over the southern coast. French merchants, creditors and officers have interests in both regions. The government must decide whom to support and how far its money and arms should follow its diplomacy.',
'南朝使者请求承认易代并延续旧约，印度方面则仍有南部海岸与殖民地的争执。法国商人、债权人与军官在两地都有利益。政府须决定与谁往来，又愿意为外交主张付出多少资金与军械。',reason='FRA可改共和政体，删固定“皇帝裁定”；事件无当前君主守卫，不添加不安全ruler引用。')
en('nesnd_external_qe1_desc','Caravans from Sichuan have brought news of the Southern dispute. Since the defeat at Dunhuang, Western Qin has had to consider its military strength and finances carefully. Renewed war in the east would make the roads through Bashu more important to trade and security alike. We should decide whether to cultivate Sichuan, support the anti-Wu coalition, or keep our resources at home.',
'四川商队带来了南朝的消息。敦煌败绩以后，西秦更须慎用兵力与财赋。东方若再起兵戈，往来巴蜀的道路将同时牵动商贸与边防。我们应当决定，是联络川中、支持反吴联盟，还是先将财力用于本国。',reason='西秦外交当前可选SIH/反吴，写具体对象与代价；不捏造新国书动作。')
en('nesnd_external_sha_desc','News of the Southern succession has reached the northern republic. Exiles recognise familiar names among those now disputing power, and some are already seeking contacts in Dongzhou. A friendly republic might supply funds or arms, but our government must decide what help it needs and what relationship it can sustain.',
'南朝争位的消息传到了北地共和国。流亡者从往事中认出参与争斗的名字，也有人开始联络东洲的同道。共和国或可从这些关系中求得资金与军械，但政府须先决定自己需要什么援助，又愿意维持怎样的往来。',reason='SHA当前请求HUS援助，不写无功能的运粮过冬与议事厅对举。')
en('nesnd_external_bur_desc','The Southern succession may alter the court’s dealings with a powerful neighbour. Trade along the rivers and the obligations inherited from existing treaties remain immediate concerns. Before committing money or arms to either side, we must consider our own status and which government can best protect our interests.',
'南朝易代将改变王庭与这个强邻的往来。沿江贸易与既有条约所定的义务都不能置之不理。在向任何一方许诺资金或军械以前，朝廷须先考虑本国的地位，以及谁能维护我们的利益。',reason='国家不是亲自颁诏者，改为明确外部局势。')
en('nesnd_external_mug_desc','The Southern succession offers another opening to raise our claims on the Indian coast. Ming possessions in Mysore and the arrangements of coastal traders remain sources of contention. Our ministers may seek French assistance in money or arms; if Southern rule still holds land in Mysore, we can also press our territorial claim.',
'南朝易代使印度海岸的旧争端再受关注。明人在迈索尔的属地与沿海通商安排，长期牵动帝国的利益。朝臣可以向法国请求资金或军械；若南朝仍占据迈索尔土地，我们也可借此重新提出领土主张。',reason='事件无保证USM此刻仍有Mysore，使用条件句；法国援助不是无条件军事干预。')
en('nesnd_external_gbr_desc','The old alliance between France and Ming placed heavy pressure on British trade routes. A disputed succession in the Southern realm may create openings for commerce and diplomacy. Merchants seek access to its ports, while the government weighs the expense of supporting a foreign partner.',
'法兰西与明人的旧同盟曾使英国航路备受挤压。如今南朝争位，商人希望借局势变化进入新的港口，政府也可重新选择交往的对象。若要用资金与军械争取影响，我们仍须衡量这项支出对本国的用处。',reason='删除商报账目装饰，以旧同盟→新贸易机会→援助代价为因果。')
en('nesnd_external_rus_desc','Russia’s long eastern frontier gives the Southern dispute consequences far beyond its place of origin. A reliable trading partner or a government willing to accept our support might strengthen our position. We may wait for the outcome, or commit funds and arms while the rivals still need foreign friends.',
'漫长的东方疆界使南朝之争也牵动俄国的利益。一个可靠的贸易伙伴，或愿意接受援助的政府，都可能改善我们在东方的处境。朝廷可以等待胜负分明，也可以趁各方仍在寻求外援时，以资金和军械争取交往。',reason='删除笼统账册堆案和无对象总结，说明可做的外交行动。')
en('nesnd_external_policy','Diplomacy in the Southern Crisis','南朝变局与外交',reason='日志标题不再以账册代替外交内容。')
en('nesnd_external_policy_reason','The Southern succession has placed old treaties, trade routes and overseas dependencies in question. Our government must choose which relationships to cultivate and whether to offer assistance or seek it from abroad. Existing agreements continue to bind their parties while new proposals are negotiated.',
'南朝易代牵动旧约、商路与海外属邦的去向。政府须决定同谁往来，是否提供援助，又是否需要向外国求助。各项新提议尚待商定，既有条约则仍约束着签署它们的国家。',reason='去一场政变分前程的无内容概括；保留真实外交条约。')
en('nesnd_external_choose_desc','Choose a diplomatic partner. Existing treaties remain in force. Only one aid agreement can be concluded through this crisis.',
'选择接洽国。既有条约仍然有效；本次南朝危机中只能议定一份援助。',reason='删除“本项目”开发口吻，保留一次援助限制。')
en('nesnd_external_choose_opposition_desc','An anti-Wu coalition leader must exist. Our country must be independent and at peace with that government. Funds or arms require a separate proposal.',
'反吴联盟须已有领袖；本国须独立，且未与其交战。选定接洽对象后，再另议资金或军械。',reason='删“实际/真实”实现词。')
en('nesnd_external_offer_money_desc','Offer a transfer of @money!#v 500#! per week, binding for #v 1 year#!. This requires #v 26,000#! in reserves, fixed net income of at least #v 5,000#!, total net income of at least #v 1,000#! and eligibility to sign the treaty. The other government may refuse. The transfer continues after the binding period until withdrawn or renegotiated.',
'提出每周@money!#v 500#!的资金援助，约束期#v 1年#!。须有#v 26,000#!储备、固定净收入至少#v 5,000#!、总净收入至少#v 1,000#!，并满足条约签署条件。对方可以拒绝；约束期满后，仍须撤回或重谈才能停止转移。',reason='明确约束期不自动终止，删原生内部词；数字按现有trigger。')
en('nesnd_external_offer_arms_desc','Offer a transfer of #v 10#! small arms, binding for #v 1 year#!. Our supply, prices, export allowance and transport must permit it. The other government may refuse; shortages or transport difficulties can suspend deliveries.',
'提出#v 10#!小武器的商品援助，约束期#v 1年#!。本国的供应、价格、出口额度与运输须满足条件。对方可以拒绝；供给或运输不足时，输送可能中止。',reason='保留商品单位与约束期，玩家不读原生一词。')
en('nesnd_external_request_tt','Our envoy will present the request in #v 7 days#!. No funds or goods are transferred before acceptance.')
en('nesnd_external_money_desc',"The envoy from [SCOPE.sCountry('nesnd_external_requester').GetName] offers @money!#v 500#! each week under a treaty binding for #v 1 year#!. Acceptance would establish the transfer between our treasuries.")
en('nesnd_external_arms_desc',"[SCOPE.sCountry('nesnd_external_requester').GetName] offers a transfer of #v 10#! small arms under a treaty binding for #v 1 year#!. Its envoy has presented the terms for our government to accept or refuse.")
en('nesnd_external_commitment_tt','The treaty takes effect immediately. Its #bold binding period is not an expiry date#!. Early withdrawal carries the treaty’s penalties; normal withdrawal, suspension and costs can be reviewed in the treaty interface.',
'条约立即生效。#bold 约束期不是自动到期日#!；提前退出须承担违约后果。正常撤回、供给中止及费用可在条约界面查看。',reason='保留重要期限界限，删除原生实现词。')
en('nesnd_external_request_money_desc','Ask the selected partner for @money!#v 500#! each week under a treaty binding for #v 1 year#!. The partner must be able and willing to pay.',
'向选定伙伴请求每周@money!#v 500#!的资金援助，约束期#v 1年#!。须由对方承担支出，并自愿接受。',reason='删“不反向”防御式重复，付款方向已明确。')
en('nesnd_external_request_arms_desc','Request a transfer of #v 10#! small arms from the selected partner, binding for #v 1 year#!. Market access, transport and treaty eligibility must permit it. The partner may refuse.',
'向选定伙伴请求#v 10#!小武器的商品援助，约束期#v 1年#!。双方须满足市场、运输与条约签署条件；对方可以拒绝。')
en('nesnd_external_request_money_event_desc',"The envoy from [SCOPE.sCountry('nesnd_external_requester').GetName] requests financial assistance of @money!#v 500#! each week under a treaty binding for #v 1 year#!.")
en('nesnd_external_request_arms_event_desc',"[SCOPE.sCountry('nesnd_external_requester').GetName] requests a transfer of #v 10#! small arms under a treaty binding for #v 1 year#!. Its envoy awaits our decision on the proposed deliveries.")
en('nesnd_external_accept_request','Approve the assistance and sign.','同意援助，交付签署。',reason='此选项供金钱与军械共用，“拨款照准”只合钱支线。')
en('nesnd_external_reconsider_desc','Choose another partner before an aid agreement is signed.',
'在援助尚未签成时，另选接洽对象。',reason='按钮可用条件已禁止committed；删清除选择的技术口吻和重复领取。')
en('nesnd_external_mysore_desc','Assert a claim on Mysore while the Southern government still holds land there. Relations with it fall by #v 10#!. This establishes a claim without transferring territory or starting a war.',
'在南朝仍占据迈索尔土地时提出领土主张。与南朝关系降低#v 10#!；获得宣称，但不立即转移土地或发动战争。',reason='按钮验证USM持地，不验证已经吴朝；改南朝。')
en('nesnd_external_mysore_tt','The Mysore claim enters our diplomatic agenda. Subject status and the right to wage war remain governed by existing relationships and treaties.')
en('nesnd_external_cancel_request_desc','Withdraw the unsigned request. Existing treaties remain in force.')
en('nesnd_external_dismiss_desc','Close the diplomatic mission and withdraw pending requests. Treaties already in force must be handled separately through diplomacy.',
'结束此次外交议程并撤回待答请求。已经生效的条约仍须在外交界面分别处理。',reason='删本项目。')
en('nesnd_external_resume_desc','Resume negotiations while the Southern crisis remains unresolved. An aid agreement already concluded cannot be repeated through this mission.',
'南朝危机尚未结束，可以恢复接洽；此次议程已经签成的援助不能重复议定。')
en('nesnd_external_end_desc','The Southern succession has reached a settlement. Our envoys have completed their mission, but treaties already signed remain in force. The government must continue meeting those obligations and attend to the relationships that survive the crisis.',
'南朝争位已有定局，使臣也已完成此行的使命。已经签成的条约仍然有效，政府须继续承担相应义务，经营这场变局留下的关系。',reason='删除文书借据清单排比，不把外交承诺变成宪法。')

# Supply file: translate every stale Chinese English slot from the present Chinese version.
sup={
'invite_desc':'Send envoys to discuss merchant contacts and procurement arrangements, and hear the other government’s terms.',
'self':'Rely on Domestic Merchants','self_desc':'Ask our merchants to arrange procurement and recall the envoys already sent.',
'end_contact':'End Commercial Contacts','end_contact_desc':'Recall our envoys and seek trade routes that can be sustained.',
'end_contact_tt':'End these contacts and reset consecutive weeks of stability. Formal treaties already signed remain in force.',
'trade':'Negotiate Reciprocal Trade','trade_desc':'Give the two countries’ merchants reciprocal trading advantages through a treaty.',
'trade_request_tt':'In #v 7 days#!, propose a reciprocal trade treaty binding for #v 2 years#!. The other government may accept or refuse.',
'finish':'Trade Routes Stabilise','finish_desc':'After supply, employment, livelihoods and commercial arrangements remain stable for #v 12 weeks#!, gain trade benefits for #v 2 years#! on the first completion.',
'dismiss':'Defer Commercial Arrangements','dismiss_desc':'Recall the mission and return to commercial arrangements later. Existing mission expenses remain due until their term ends.',
'envoys':'Commercial Mission Abroad','verified':'Trade Routes Reopened','treaty':'Reciprocal Trade Agreement',
'resume':'Renew Commercial Contacts','resume_desc':'Reconnect with merchants, secure supplies and employment, and restore dealings with other states.',
'.1.t':'Merchants Lead the Way',
'.1.d':"Envoys from [SCOPE.sCountry('nesnd_supply_requester').GetName] have brought a request from their merchants. They hope to maintain procurement contacts between the two countries and exchange information about supplies of paper, timber and manufactured goods, preserving trading opportunities as the political situation changes.\\n\\nThese contacts would broaden our commercial relations, but need officials to receive the mission and merchants to sustain the exchanges. [ROOT.GetCountry.GetName] may appoint representatives to hear the proposed arrangements.",
'.1.a':'Invite them to discuss it.','.1.b':'Our domestic affairs must come first.',
'.2.t':'A Reciprocal Trade Agreement',
'.2.d':"[SCOPE.sCountry('nesnd_supply_requester').GetName] proposes a formal treaty granting reciprocal trade advantages. Merchants hope to expand their markets, while those buying supplies seek more stable commercial relations. Once signed, both countries will be obliged to fulfil its terms.",
'.2.a':'Approve the treaty.','.2.b':'The terms need further discussion.',
'.3.t':'Trade and Livelihoods',
'.3.d':"For the past season, workshops and garrisons in [ROOT.GetCountry.GetName] have been able to buy what they need, while schools, offices and factories have filled their posts. Merchants have renewed their trading contacts, and people across the states have supported themselves through production and exchange.\\n\\nThe Southern political dispute continues. The cargo ships leaving our ports give us the means to keep trading through it.",
'.3.a':'Keep trade flowing.',
'invite_hna':'Send Envoys to Huguang','invite_sih':'Send Envoys to Sichuan','invite_gng':'Send Envoys to Guangxi','invite_yn1':'Send Envoys to Yuannan','invite_cne':'Send Envoys to the Chinese Empire','invite_fra':'Send Envoys to France',
'hus_preparations':'The Republic’s Trade Routes','finish_shared':'Continue in the Common Market','finish_shared_desc':'Continue trading in the common market and retain existing agreements. Supply and livelihoods must remain stable for #v 12 weeks#!; first completion grants trade benefits for #v 2 years#!.',
'finish_autonomous':'Manage Our Own Trade','finish_autonomous_desc':'Control our own market and commercial arrangements. Maintain all conditions for #v 12 weeks#!; first completion grants trade benefits for #v 2 years#!.'}
for k,e in sup.items():en('nesnd_supply'+k if k.startswith('.') else 'nesnd_supply_'+k,e)

# Remaining crisis fallback entries, including inherited author history: preserve established Chinese, supply genuine English.
hist={
'flavorUSM.4.t':'The Ming–Wu Succession: Zheng Zhao’s Audience',
'flavorUSM.4.d':'In the spring of 1678, Zheng Zhao—later Emperor Wuzong of Wu, then Duke of Wu, Ming’s Nanjing Protector and Minister of Rites—announced that he would visit the emperor after a succession of victories at home and overseas. The ruler of Yan at Tianjin, victorious in the Great Constitutional War thirty years earlier, still stood at the height of his power. Yet Zheng’s determination overcame his ministers’ warnings and his enemies’ threats. He set out in June.\\n\\nNothing comparable to this procession had been seen in the nearly three centuries of Northern Ming’s military governors and princely states. Pressure from Yan, Qin and Qi limited Zheng to five thousand guards and a handful of officials, but the entourage included the finest of Wu’s forces: marines from the Southern Seas, Japanese swordsmen, early Jurchen grenadiers, and even exiled nobles of the Far Eastern Yin seeking imperial redress and military aid. They carried treasures gathered during a century of Wu expansion across the world, while nearly ten thousand labourers hauled tribute rice from Annam and Cambodia. Beyond the procession lay a Central Plain kept close to famine by local fighting and the exactions of military governors and transport officials.\\n\\nAfter returning, Zheng Zhao adopted the title of Supreme Lord. Wu and its colonies entered a period of rapid growth as refugees arrived from both north and south. Zheng and his successors pressed their centralising reforms and the commercialisation of land ever harder, securing the foundations of our authority over the Southern realm and its many states. Wu’s advance has continued to this day...',
'flavorUSM.4.f':'I had heard that the Zhu Son of Heaven held Heaven’s mandate, a divine dragon descended among men. The founding emperor rose from beggary, destroyed foreign rule and restored the Chinese heartland. His achievements would outlast the inscriptions of history. Though virtue might decline, the mandate seemed unchanged. Yet today I have seen him: the Zhu boy is mortal too.\\n—Zheng Zhao',
'flavorUSM.4.1':'Yao and Shun yielded the throne; Tang and Wu won it by revolution. Heaven’s favour rests with virtue among the people and service to humanity, not one family or an unbridgeable division between ruler and ruled.',
'flavorUSM.6.t':'After the Chief Minister’s Death',
'ce_usm_conflicts_within_reason':'Ming’s Zhu dynasty, or Wu’s Zheng house? For those able to take part in Southern Chinese politics, the question demands an answer at every moment. From village lecture halls on Sichuan’s frontier to the chamber of the Ministry of Rites in Nanjing, arguments, memorials, essays and reports call out to the public. There are more questions than answers, more quarrels than considered debate.',
'ce_usm_cw_japanese_interest_reason':'The Zheng foothold in Kyushu forms part of Wu’s maritime power and has long affected the interests of Japan’s great houses. With civil war threatening the Southern realm, rival envoys cross the sea seeking ships and supplies. The government has an opportunity to recover the Wu-held lands of Kyushu and reshape relations across the strait.',
'usm_civilwar.1.3':'Petition for accession and recognise Wu.',
'usm_civilwar.2.t':'The Second Jingnan War','usm_civilwar.2.1':'Raise funds and troops to uphold the new dynasty.','usm_civilwar.2.2':'Uphold Ming and unite against Wu.','usm_civilwar.2.3':'Unite against Wu, then establish government by the people.','usm_civilwar.2.4':'Honour our commitments in the mainland struggle.','usm_civilwar.2.5':'Watch the fighting and honour our commitments.',
'usm_civilwar.3.1':'Begin governing the new dynasty.',
'usm_civilwar.10.t':'Authority After Victory','usm_civilwar.10.1':'Restore the Zhu house to government.','usm_civilwar.10.2':'Retain Ming’s name under our government.','usm_civilwar.10.3':'Let the people govern without another emperor.',
'usm_civilwar.12.t':"[SCOPE.sCountry('usm_mister_rebel').GetNameNoFormatting] Insists on Independence",
'usm_civilwar.12.d':"Representatives of [SCOPE.sCountry('usm_mister_rebel').GetName] have declared their intention to conduct military, fiscal and diplomatic affairs in their own government’s name. They fought beside the coalition, but now intend to retain their own rule.",
'usm_civilwar.13.t':"[SCOPE.sCountry('usm_mister_rebel').GetNameNoFormatting] Swears Allegiance",
'usm_civilwar.23.t':'An Agreement Across the Strait',
'usm_civilwar.23.d':'The Southern civil war has brought Kyushu back to the centre of Japanese politics. Zheng ports, trade routes and garrisons on the island support Wu’s maritime power and affect the interests of Japanese lords and merchants.\\n\\nBoth Wu and its opponents seek Japanese intervention, offering to return the Zheng-held parts of Kyushu after victory. The side we support will determine our allies across the sea and the government from which we must claim our reward.',
'usm_civilwar.23.1':'Support Wu in exchange for its Kyushu holdings after the war.','usm_civilwar.23.2':'Join Wu’s opponents and seek Kyushu through victory.','usm_civilwar.23.3':'Remain neutral and make no military commitment.',
'nesnd_crisis.20.a':'Put our own country in order first.','nesnd_crisis.20.b':'Provide supplies to Huguang.',
'nesnd_crisis.21.a':'Protect commerce and maintain relations.','nesnd_crisis.21.b':'Receive those fleeing the South.','nesnd_crisis.21.t':'Visitors from the South',
'nesnd_crisis.21.d':'Zheng fleets, trading houses and dependencies have carried news of the Southern war abroad. Merchants fear the seizure of their cargoes, while envoys from the rival sides seek recognition, military supplies and loans.\\n\\n[ROOT.GetCountry.GetName] has interests of its own in these exchanges. Keeping trade open requires dealings with those who control the ports and sea routes. Receiving exiles or supplying the anti-Wu forces would draw us more deeply into the Southern political struggle.',
'nesnd_crisis.40.a':'Judge cases individually and retain local talent.','nesnd_crisis.40.b':'Purge the old parties and rebuild military rule.','nesnd_crisis.40.t':'Foundations of the New Dynasty',
'nesnd_crisis.41.a':'Reorganise government and the armed forces.','nesnd_crisis.41.b':'Reward the armies according to custom.','nesnd_crisis.41.t':'Back Across the Strait',
'nesnd_crisis.41.d':'The troops are returning from abroad. Local lords demand the rewards promised when they joined the campaign, merchants want shipping restored, and the government must arrange its garrisons and revenues.\\n\\nThe mainland war has given [ROOT.GetCountry.GetName] an opportunity to reorganise. More consistent taxation and official training would strengthen central administration; honouring military claims first would secure the commanders and lords on whom the expedition relied.',
'nesnd_early_accession':'Press for Early Accession','nesnd_south_pressure_bar':'Succession Pressure',
'nesnd_crisis.11.f':'“Hold the prisoners separately and secure all correspondence. Tomorrow, the cabinet will return to the case.”',
'nesnd_crisis.20.f':'“Some men who crossed the river in the former campaign remain in service. If Your Majesty considers another march south, let us first assess the grain and pay.”',
'nesnd_crisis.21.f':'“The cargo is loaded. We await only your answer: will the old trading papers still be honoured?”',
'nesnd_crisis.40.f':'“The provinces need work and commerce restored, so that soldiers and civilians can support themselves.”',
'nesnd_crisis.41.f':'“Every house still holds its promises from the expedition. Now that we have returned, we must settle them together.”',
'nesnd_hna_academy_button_outcome_tt':'Huguang preparations #p +30#!.',
'nesnd_hna_supply_button_requirements':'Military supplies have not yet been reorganised, and the country is not recovering from bankruptcy.',
'nesnd_hna_supply_button_outcome_tt':'Huguang preparations #p +30#!.',
'nesnd_hna_veterans_button_outcome_tt':'Huguang preparations #p +30#!.',
'nesnd_federal_compact_button_requirements':'The Ming–Wu dispute is active, [concept_bureaucracy] is not negative, [concept_legitimacy] is at least #v 50#!, and #v 18 months#! have passed since the last agreement.',
'nesnd_protect_chen_button_outcome_tt':'An assassination attempt against Chen Dongyang will include a possible rescue by his guards.',
'nesnd_early_accession_requirements':'Succession pressure is at least #v 70#!, Wu has not replaced Ming, and the Southern constitutional dispute remains unresolved.'}
for k,e in hist.items():en(k,e)
P['flavorUSM.6.t']['zh']='首辅身后'
P['flavorUSM.6.d']['mechanic']='VERIFIED: events/flavorUSM_ce.txt:806-844 requires no living Chen and calls nesnd_chen_after_death; date<=1862, earlier/later1870descbranch makes d1 unreachable throughnormaltrigger.'
P['flavorUSM.6.d']['reason']='现行flavorUSM.6是死亡后续，旧AI文字误写仅离开首辅。明确死亡但不强写遇刺，兼容自然死亡。'
P['usm_civilwar.23.d']['zh']=I['usm_civilwar.23.d']['zh']['text'].replace('反吴诸府','反吴诸省')
P['usm_civilwar.23.2']['zh']='联合反吴各省，以战果争取九州。'
P['nesnd_crisis.41.d']['zh']='参战军队陆续归国。地方领主要求兑现出兵时的许诺，港口商人催促恢复航运，中央也须重新安排驻军与征收。\\n\\n大陆战争使[ROOT.GetCountry.GetName]有了整理军政的机会。统一地方征收、训练官员，可以扩大中央的施政能力；先行酬赏军功，则能稳住此次出征所倚重的将领与领主。'
P['nesnd_crisis.20.c']['zh']='联络襄樊大营，准备南下。'
P['nesnd_crisis.20.c']['en']='Contact the Xiangfan garrison and prepare to march south.'

en('nesnd_supply_rules',
"#bold Supplies#!\\nPaper, tools and small arms must have no local shortages and cost no more than #v 50%#! above base price; Dongzhou also requires hardwood.\\n\\n#bold Buildings and workers#!\\nEach required building type must have at least one building staffed to #v 75%#! without input shortages. Huguang requires a university and barracks; Sichuan a tooling workshop and either an iron mine or logging camp; Guangxi a paper mill and logging camp; Dongzhou a port and government administration. If recruitment is difficult, check [concept_pop_qualifications], [concept_building_wage] and input supplies.\\n\\n#bold Livelihoods#!\\nUnemployed workers may be at most #v 12%#! of the national workforce. States with at least #v 50,000#! workers have a limit of #v 20%#!. Subsistence workers count as employed. There must be no famine or local grain shortage, and grain must cost no more than #v 25%#! above base price.\\nUnemployed workforce: #v [Country.MakeScope.Var('nesnd_supply_unemployed').GetValue|0] / [Country.MakeScope.Var('nesnd_supply_workforce').GetValue|0]#! (#v [Country.MakeScope.Var('nesnd_supply_unemployment').GetValue|%1]#!). States above the local unemployment limit: #v [Country.MakeScope.Var('nesnd_supply_critical_states').GetValue|0]#!.\\n\\n#bold Stable commerce#!\\nChoose a commercial partner or rely on domestic merchants, and maintain all four conditions for #v 12 weeks#!. War, bankruptcy, a change of market or failure of any condition restarts the consecutive count.",reason='现有EN遗漏纸张/工具/小武器50%及各国建筑类型，且保留Latestrefresh更新口吻；按当前CN完整译出。',mechanic='common/scripted_triggers/nesnd_supply_triggers.txt; native market/jobs/unemployment/grain/contact requirements; no gameplay changes.')
for k in ('nesnd_chen.1.active','nesnd_chen.1.residence','nesnd_chen.1.intel'):
    en(k,I[k]['en']['text'].replace('The guard detail is in place and its register is checked daily.','The cabinet has assigned dedicated guards to Chen Dongyang’s residence and journeys, with their wages paid weekly.'),reason='英文旧句仍把已修中文变回名册日查；同步明确内阁护卫和经费主体。')
en('nesnd_south_reconciliation_status',I['nesnd_south_reconciliation_status']['en']['text'].replace('Months of accord implementation:','Months implementing the settlement:').replace('The commission ends','Implementation ends'),reason='履行的是礼法改制安排，海外条约另外处理。')
P['nesnd_south_accords.22.d']['zh']=P['nesnd_south_accords.22.d']['zh'].replace('南明的儒家立宪联邦','南明儒家特色的立宪民主联邦')
P['nesnd_south_accords.22.d']['en']=P['nesnd_south_accords.22.d']['en'].replace('Southern Ming’s Confucian constitutional federation','Southern Ming’s Confucian form of constitutional democracy and federation')
P['nesnd_crisis.10.t']['en']='The Memorial on Constitutional Administration in the Provinces and Garrisons Is Adopted'
for k,p in P.items():
    if k.startswith(('nesnd_hna_','nesnd_huguang_')):
        p['mechanic']='DORMANT: old Huguang JE is retired (possible=no,shown=no,invalid=yes); three buttons have no active caller. '+p['mechanic']
    if k.startswith(('nesnd_crisis.10.','nesnd_crisis.11.','nesnd_crisis.21.')):
        p['mechanic']='LEGACY DISPLAY ONLY: event10 has no current caller; event11 is hidden security maintenance; event21 is hidden forwarding to nesnd_external. '+p['mechanic']
    if k in ('nesnd_federal_compact_button_requirements','nesnd_protect_chen_button_outcome_tt'):
        p['mechanic']='DORMANT legacy tooltip, no current caller. Preserved for old references, not an accurate description of the replacement live button.'

# Remaining late overrides with constitutional or province vocabulary.
en('nesnd_south_compact_detail_tt',
'#bold Support for the settlement#!\\nMainland, overseas and Japanese governments account for #v 50%, 30% and 20%#! respectively. Commitments last #v 36 months#! and cease to count after a change of alignment or overlord, war against the centre, or withdrawal.\\n\\n#bold A peaceful constitutional settlement#!\\nThe chosen side needs political support of #v 85#! and a lead of #v 20#!, sustained for #v 12 months#!. Ming needs #v 75%#! commitment support and at least two mainland core governments. Wu needs #v 80%#!, consent from every government due for integration and the Japanese territorial parties, and a sufficiently prepared fleet. A completed settlement ends the dispute.',
'#bold 改制承诺#!\\n大陆、海外与日本诸邦的承诺分别占#v 50%、30%、20%#!。承诺有效#v 36个月#!；改换立场、与中央交战、改投宗主或撤回支持后，相应承诺失效。\\n\\n#bold 和平议定国制#!\\n所选一方的政治支持须达到#v 85#!，领先另一方#v 20#!，并连续维持#v 12个月#!。明廷须获#v 75%#!支持及至少两个大陆核心政府同意；吴方须获#v 80%#!支持、拟改省诸国与日本割地各方同意，并备有合格舰队。新制议定后，朝争结束。',reason='指标统计支持不是宪法本身，不称国制为盟约；与中央交战才失效，保留数值。')
en('nesnd_south_politics_summary',
"#bold The Ming Court and Hangzhou#!\\nFinances and administration #v [GetGlobalVariable('nesnd_south_finance').GetValue|1]/20#!　Cooperation in government #v [GetGlobalVariable('nesnd_south_domestic').GetValue|1]/20#!\\nZhu succession #v 20#!　Wu military strength #v [GetGlobalVariable('nesnd_south_military').GetValue|1]/20#!\\n#bold Commitments#!　Ming #v [GetGlobalVariable('nesnd_south_ming_accord').GetValue|1]%#!　Wu #v [GetGlobalVariable('nesnd_south_wu_accord').GetValue|1]%#!\\nContinuous fulfilment #v [GetGlobalVariable('nesnd_south_peace_months').GetValue|0]/12#! months.\\n\\n$nesnd_south_compact_detail_tt$",
I['nesnd_south_politics_summary']['zh']['text'].replace('南京与杭州','明廷与南府').replace('诸府盟书','各方改制承诺').replace('盟约连续履行','连续履行'),reason='覆盖最终peace_gates层中旧英文大段说明；CN/EN同结构同数值；不能用国际盟约称中央国制。')
en('nesnd_south_reconciliation_effect_tt',
'Maintain additional [concept_budget_government_wages] of #n +5%#! and use #n 50#! [concept_authority]. After #v 1 month#!, each month in which the chosen side’s political, financial and commitment conditions hold reduces succession pressure by #p 3#!. Sending proposals or renewing commitments does not itself reduce pressure. Implementation stops if conditions cease to hold, and ends once pressure reaches #v 40#!. A formal peaceful settlement still requires #v 12 months#! of continuous fulfilment.',
'持续承担[concept_budget_government_wages]开支#n +5%#!和[concept_authority]#n −50#!。满#v 1个月#!后，所选路线的支持承诺、政治及财政条件每维持一个月，易代压力#p −3#!。遣使或续订承诺本身不降低压力。条件不再满足时停止履行，压力降至#v 40#!后结束；正式和平结局仍须连续维持#v 12个月#!。',reason='保留实际月度财政代价、真实门槛/退出；删原定、月度核验等实现词。')
for k in ('nesnd_chen.3.d','nesnd_chen.death_residence_desc'):
    z=I[k]['zh']['text'].replace('各府送往内阁的文书','各省送往内阁的文书').replace('各府派驻南京的官员','各省派驻南京的官员')
    e=I[k]['en']['text'].replace('prefectures','provinces').replace('regional courts','provincial governments')
    en(k,e,z,reason='南朝省制；不把各省称府。其余人物叙事保留。')
z=I['nesnd_south_pressure_detail_tt']['zh']['text'].replace('邦国契约修正','礼法定制修正')
e=I['nesnd_south_pressure_detail_tt']['en']['text'].replace('federal compact','constitutional settlement').replace('Federal Compact','Constitutional Settlement')
en('nesnd_south_pressure_detail_tt',e,z,reason='同一修正改名，保留机制数字和本有英文。')

# Standardise this round's English institution names without touching other historical names.
for k,p in P.items():
    p['en']=p['en'].replace('Liyi Assembly','Assembly of Rites').replace('provincial representatives','provincial delegates').replace('Provincial representatives','Provincial delegates')
    if k in I:
        p['current_zh']=I[k]['zh']['text'];p['current_en']=I[k].get('en',{}).get('text') if I[k].get('en') else None
        src='; current '+I[k]['zh']['file']+':'+str(I[k]['zh']['line'])
        if src not in p['source']:p['source']+=src
    p['status']='EDITORIAL_PROPOSAL_NO_ENGINE_RUN'
(R/'usm-proposals.json').write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf-8')
remaining=[k for k,v in I.items() if k not in P and v.get('en') and re.search('[\u4e00-\u9fff]',v['en']['text'])]
print('FINAL proposals',len(P),'remaining Chinese in English',remaining)
