from pathlib import Path
import json,re,hashlib
R=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/canon-prose-20261102')
rows=json.loads((R/'cne-inventory-data.json').read_text(encoding='utf-8'))
by={x['key']:x for x in rows}
P={}
def old(k,lang='simp_chinese'):
 return by[k][lang]['candidate']['text'] if k in by and by[k][lang]['candidate'] else ''
def put(k,zh,en,reason,source,mechanic):
 P[k]={'zh':old(k) if zh is None else zh,'en':en,'reason':reason,'source':source,'mechanic':mechanic}
def trans(k,en,source='current effective Chinese; original author text where identified',mechanic='Localization only; preserve Chinese and all gameplay effects.'):
 put(k,None,en,'English effective layer contains Chinese or omits material from the Chinese text.',source,mechanic)
CR='events/nesnd_crisis_events.txt:3-124; common/scripted_effects/nesnd_land_choices.txt:1-114; common/scripted_effects/nesnd_crisis_effects.txt:17-164; author-revision-original.txt'
CAN='Latest author canon: six ministries; Senate of veteran commanders and senior ministers monopolises legislative authority; advisory 咨议局; provincial 省督/总督.'
PR='common/journal_entries/nesnd_cne_programs.txt; common/scripted_buttons/nesnd_cne_programs.txt; common/scripted_effects/nesnd_cne_programs.txt; common/static_modifiers/nesnd_cne_programs.txt'
CF='common/scripted_effects/nesnd_cne_confidence.txt; common/scripted_triggers/nesnd_cne_confidence.txt; events/nesnd_cne_confidence.txt'
BASE='backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml (SHA256 3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a)'

put('nesnd_crisis.30.local',
"[SCOPE.sState('nesnd_land_petition_state').GetName]的清丈官带着新法下乡勘定后，当地几处军功庄园却仍在按旧例征租。已经缴清赎价的农户被他们的“老爷”告知，所耕之田属于军籍，不许抵触租税。一些替农民代写申诉的塾师也因包庇隐产而遭拘押。\\n\\n涉事各县呈来的契约与军营的册籍彼此抵牾。省督要求接手复核，清丈官则请朝廷派兵收缴隐匿的文书。迁延日久，原本期待分田的农民聚集到县城，等待这个许诺解放他们的新政府作出答复。",
"Land commissioners in [SCOPE.sState('nesnd_land_petition_state').GetName] have surveyed the countryside under the new law, yet several local military estates still collect rent under the old rules. Farmers who have paid the redemption price are told by their old masters that their fields remain military property and that the dues must be paid. Teachers who helped draft their petitions have been arrested for concealing property.\\n\\nThe deeds submitted by the affected counties contradict the garrison registers. The provincial governor seeks authority to review the cases, while the commissioners ask the court to send troops to recover the withheld records. As the dispute drags on, farmers gather in the county towns, awaiting an answer from the government that promised to free them.",
'Retain the author’s redemption/rent conflict and delayed petition. Name one selected locality, keep the crisis local, and identify the provincial governor without adding new Senate involvement.',CR+'; '+CAN,
'Disorder ≥55 triggers once. Requires the locality scope addition and first_valid exists-state description branch specified by root. No extra law, arrest effect, land transfer or national breakdown is added.')
put('nesnd_crisis.30.d',
 P['nesnd_crisis.30.local']['zh'].replace("[SCOPE.sState('nesnd_land_petition_state').GetName]的清丈官",'地方呈来一桩清丈争讼：清丈官'),
 P['nesnd_crisis.30.local']['en'].replace("Land commissioners in [SCOPE.sState('nesnd_land_petition_state').GetName] have surveyed",'A provincial land dispute has reached the court. Land commissioners have surveyed'),
 'Guarded fallback for an already queued event without the newly saved locality scope. The normal branch is nesnd_crisis.30.local.',CR+'; '+CAN,
 'No fabricated place name or undefined scope if an old queued event lacks nesnd_land_petition_state.')
put('nesnd_crisis.30.b','责成省督议处，酌从地方之请。','Have the governor reach a settlement on local terms.',
'The Advisory Council can present petitions, not take over executive authority. Distinguish the local compromise from the central appeals review in A.',CR+'; '+CAN,'Keep disorder -8 and 60-month compromise modifier, with reduced authority/tax collection.')
put('nesnd_crisis.30.c','令各营交册，抗命聚众者依法惩办。','Order the garrisons to surrender their records and punish those who defy the law.',
'The actual option is repression, with radicals and higher disorder; merely declaring that the law binds garrisons hides the choice.',CR,'Keep disorder +12, radicals +2%, repression flag; no troop command or purge added.')
for k,en in {
 'nesnd_crisis.30.t':'The Survey Dispute',
 'nesnd_crisis.30.a':'Review the deeds and suspend the disputed cases.',
 'nesnd_crisis.30.f':'“The garrison says the land belongs to the army. The county says it belongs to the state. We ask only this: what did our payment last year redeem?”',
}.items():trans(k,en,CR)

put('nesnd_crisis.33.d',
'山西的退伍军人、地方士人与失地农户，因清丈后的生计困顿和接连搜捕聚到了一处。共和派借乡校与旧日军中关系传递文书，要求各县推举代表，追究侵夺田产的军官。\\n\\n几处驻军大营拒绝交出涉案军官，省督派去查问的官员也被挡在营外。各县代表因而要求撤换清丈主官，重审田产并赔补受害农户。共和派已开始联络愿意倒戈的营伍，准备在请愿无门时举兵。刑部将案情呈至朝廷，请求裁定是撤官重审，还是以抗命聚众治罪。',
"Veterans, local scholars and dispossessed farmers in Shanxi have gathered over the hardship and arrests that followed the land surveys. Republican organisers use village schools and old military connections to circulate petitions, calling on each county to choose delegates and hold officers accountable for the seizure of farmland.\\n\\nSeveral garrisons refuse to surrender the accused officers and have turned away the governor's investigators. The county delegates demand the removal of the chief commissioner, a fresh review of titles and compensation for the injured farmers. Republican organisers are seeking allies among the troops and preparing to rise if their petitions fail. The Ministry of Justice has referred the case to the court: dismiss the officials and reopen the inquiry, or prosecute the assemblies for defying the law.",
'Preserve the author’s arrests, refusal to surrender officers, and compensation demand; join them to actual persistent hardship and make the imminent NSX secession intelligible without declaring it before choice.',CR+'; common/scripted_triggers/nesnd_cne_reform.txt:85-102; '+CAN,
'Shanxi/Jinbei noncapital state, ≥6 bad months, unemployment >10%, turmoil >25%, national disorder ≥65, ≥9 samples. A lowers progress/order and adds 36-month administrative expense; B may release NSX and create annexation play. Narrative dismissal/compensation remain policy flavour; no literal character dismissal or treasury compensation exists.')
for k,en in {
 'nesnd_crisis.33.t':'Old Banners in the Hills',
 'nesnd_crisis.33.a':'Dismiss the officials, provide compensation and reopen the case.',
 'nesnd_crisis.33.b':'Punish these unlawful assemblies!',
 'nesnd_crisis.33.f':'“When we marched, they said we were fighting for land to farm and a hearing for every grievance. Back in our own villages, we have to ask for it all again.”',
}.items():trans(k,en,CR)

put('nesnd_crisis.31.d',
'各地行营开始截留本应解往户部的税款。军官以供饷为名接管关卡、仓廪与地方官署，省督或被迫迁就驻军，或依靠自己的亲军与之争夺财源。清丈官只能在驻军准许的地方办案。欠饷的营伍纷纷向主将索要田产，原有的营兵集团由此取得了更广的地方权力。\\n\\n兵部奉[ROOT.GetCountry.GetRuler.GetFullNameWithTitle]之命发出的调防令接连退回。元老院中的勋旧要求承认各营与省督已经掌握的兵财之权，以换取各省继续奉朝廷正朔。咨议局送来的地方陈情也已无从逐案办理。朝廷若不能作出让步，失去约束的营兵便可能拥立自己的政府。',
"Field commands across the Empire are withholding taxes owed to the Ministry of Revenue. Officers seize customs posts, granaries and provincial offices in the name of paying their troops. Governors either yield to the garrisons or use their own loyal units to contest the revenue. Land commissioners can work only where the troops permit them, while unpaid soldiers demand estates from their commanders. The military blocs have acquired powers far beyond their former holdings.\\n\\nRedeployment orders issued by the Ministry of War in the name of [ROOT.GetCountry.GetRuler.GetFullNameWithTitle] are repeatedly returned. Senior members of the Senate demand recognition of the military and fiscal powers already seized by governors and commands in exchange for their continued allegiance. The court can no longer hear the provincial petitions forwarded by the Advisory Council. Without a settlement, commands beyond its control may establish governments of their own.",
'Keep author’s national military-fiscal breakdown, clarify governors’ relationship to armies, remove country-as-ordering-person and advisory council executive sovereignty.',CR+'; '+CAN+'; GAME localization/english/events_l_english.yml:858 (native GetFullNameWithTitle)',
'Only terminal extreme crisis invokes this. A ends reform plus 60-month secession-disorder; B releases eligible NSX/NHB/NSD, ends reform and adds radicals. Do not claim every province secedes.')
for k,en in {
 'nesnd_crisis.31.t':'Military Power Slips Away',
 'nesnd_crisis.31.a':'Settle provincial powers and preserve their allegiance.',
 'nesnd_crisis.31.b':'The armies now answer to their own masters.',
 'nesnd_crisis.31.f':'“This province pays the troops and this province feeds them. If the ministers cannot send our wages, they must let us raise the money ourselves.”',
}.items():trans(k,en,CR)

put('nesnd_crisis.32.t','安石旧祸','The Old Disaster of Anshi','Preserve the author’s changed historical title.',CR,'Title only.')
put('nesnd_crisis.32.d',
'各省请求停止地权改革的文书已经汇集到朝廷。元老院中的勋旧提出一份妥协草案，拟请[ROOT.GetCountry.GetRuler.GetFullNameWithTitle]颁诏收束这场运动。所谓“新契”确认的土地仍归军户，但须由军户承诺减轻佃租，并准许佃农离乡务工；尚未处置的庄田、军田与宗族产业，则交由省督督办，暂列为“国家公田”，由官府招佃。\\n\\n这份草案使力主改革的公卿难堪，也将使依靠旧有地权组织起来的地方势力重新参与征税与乡里治理。户部与兵部都希望借此平息各省争端，将有限的财赋与人力收回常政。若予批准，地权革命便将在这些妥协中结束；余下的理想，只能留待后人。',
"Memorials requesting an end to land reform have reached the court. The senior commanders and ministers of the Senate propose a compromise and ask [ROOT.GetCountry.GetRuler.GetFullNameWithTitle] to close the campaign by decree. Under their draft, land recognised by the new deeds would remain with military households, who must promise lower rents and allow tenants to leave for work. Unsettled estates, military land and lineage property would pass under the governors' supervision as state lands let to tenants.\\n\\nThe proposal humiliates the ministers who championed reform. It would also restore a place in taxation and village government to the local powers sustained by the old land system. The Ministries of Revenue and War hope to settle the provincial disputes and return scarce funds and officials to ordinary administration. Approval would bring the land revolution to an end on these terms, leaving its remaining ambitions to another generation.",
'Preserve author’s military-household ownership, reduced rent, freedom to migrate and state-land compromise as proposed policy. The event appears before the choice, and acceptance permanently ends this campaign.',CR+'; '+CAN,
'A sets nesnd_land_frozen and ce_CNE_land_reform_done, cleans programmes, applies 120-month compromise, fires flavorCNE.2. B simply continues. No enacted rent law, property ownership transfer or automatic population migration is implemented; these are proposed political terms, not claimed immediate mechanics.')
put('nesnd_crisis.32.a','准此颁诏，收束地权革命。','Issue the decree and bring the land revolution to a close.',
'The original “暂缓” promises a reversible pause; actual acceptance closes the whole reform permanently.',CR,'End campaign; no resume path.')
trans('nesnd_crisis.32.b','The reform must continue.',CR)
put('nesnd_crisis.32.f','“减其租，通其行，旧业仍存。如此，诸营或可罢争。”','“Lower the rents, let the tenants travel, and preserve the old holdings. Perhaps the garrisons will then end their resistance.”',
'The old flavour confirmed all deeds without the author’s military-household compromise; present it as the proponents’ words.',CR,'New anonymous in-world dialogue proposed in this editorial pass, not an attributed author quotation.')
put('nesnd_land_suspend','议止地权革命','Consider Ending the Land Revolution','Button opens an irrevocable ending proposal; a resumable pause belongs only to the three individual programmes.',CR,'Still opens crisis32; no immediate ending on button click.')
put('nesnd_land_suspend_desc','将各省停办改革之请交元老院议定，呈请颁诏收束清丈与改制。','Submit the provinces’ requests to end reform to the Senate and seek a decree closing the campaign.',
'Name the competent legislative body and preserve the fact that clicking opens a decision.',CR+'; '+CAN,'The confirmation event retains both acceptance and continuation.')
trans('nesnd_land_suspend_requirements','The land revolution is still underway.',CR)

put('nesnd_cne_feedback_end_reform','结束地权革命及其改革措施；此后不能恢复。','End the land revolution and its reform programmes. The campaign cannot be resumed.',
'Remove developer-language “buttons/monthly settlement”; state the material irreversible consequence.',CR,'Covers freeze options, not programme pause buttons.')
put('nesnd_cne_feedback_continue_reform','继续推行地权革命。','Continue the land revolution.','Remove redundant monthly accounting language.',CR,'No numerical effects.')

put('nesnd_crisis.20.t','伪朝禅代','The Pretender’s Accession','Preserve author’s imperial viewpoint and new title.','author-revision-original.txt; events/nesnd_crisis_events.txt:151-183','CNE foreign policy event, not neutral omniscient description.')
put('nesnd_crisis.20.d',
'倭吴叛明称制的消息传来，江北大臣纷纷弹冠相庆。更有人提起牧家天子当年御辇南下的盛举。毕竟伪吴郑狗与西府各省决裂互斗，无暇北顾，南征统一或可一举成功。\\n\\n有心人的策动下，边将请拨军饷，并派员联络湖广的“有识之士”。然而，我朝却不是什么太平兴国之世界。六部用于整军、赋税与民生的经费已有各自的去处；若地权革命尚未告成，南方战事更要同国内改制争夺钱粮与兵力。此时卷入南朝的混战，未来是福是祸仍未可知也。',
"News that the Japanese Wu have betrayed Ming and assumed the imperial title has brought jubilation among ministers north of the river. Some recall the Mu emperor's own southern expedition. The Zheng usurpers are fighting the western provinces and have little attention to spare for the north. A campaign for unification might now succeed at a single stroke.\\n\\nAt the urging of those eager for war, frontier commanders request military funds and send agents to contact sympathetic men in Huguang. Yet our own Empire enjoys no age of effortless peace. The Six Ministries already have claims upon the treasury for the army, taxation and public welfare. If the land revolution remains unfinished, a southern war will compete with reform for men and supplies. Whether intervention will bring fortune or calamity is still unknown.",
'Preserve the author’s partisan voice and intent. Remove unconditional claim that land reform is active: event20 can arrive after it ended. State the conditional opportunity cost in period terms.','author-revision-original.txt; events/nesnd_crisis_events.txt:157-175; '+CAN,
'A observation; B 36-month spending and HNA aid, +8 disorder only if active; C 60-month spending, +15 disorder only if active, joins available opposition play. No guaranteed declaration or military victory.')
put('nesnd_crisis.20.c','联络襄樊诸府，准备南下。','Contact the prefectures around Xiangyang and prepare to march south.','Preserve latest author edit.','author-revision-original.txt; events/nesnd_crisis_events.txt:170-175','Joins opposition play if available; preparation does not promise an unavoidable new war.')
for k,en in {
 'nesnd_crisis.20.a':'Put our own affairs in order first.',
 'nesnd_crisis.20.b':'Send military supplies to Huguang.',
 'nesnd_crisis.20.f':'“Men who crossed the river in the old campaign still serve in our ranks. If another southern expedition is proposed, I ask that we first reckon its provisions and pay.”',
}.items():trans(k,en,'author-revision-original.txt; events/nesnd_crisis_events.txt:151-183')

for k,zh,en in [('NSX','大晋共和邦','Great Jin Commonwealth'),('NHB','靖安军',"Jing’an Army"),('NSD','国人共和国',"Citizens’ Republic")]:
 put(k,zh,en,'Preserve author’s revised polity name and translate the English slot.','author-revision-original.txt','Country name only; tags and government mechanics unchanged.')
for k,en in {'NSX_ADJ':'Fenjin','NHB_ADJ':'Hebei','NSD_ADJ':'Shandong','nesnd_land_survey_cost':'Independent Land Survey Expenses','nesnd_land_appeals':'Land Appeals Commission','nesnd_army_audit':'Military Estate Audit','nesnd_land_compromise':'Suspended Land Clearance','nesnd_land_rapid':'Swift Recognition of Land Rights','nesnd_secession_disorder':'Military and Civil Reorganisation'}.items():trans(k,en,CR+'; common/static_modifiers/nesnd_crisis_modifiers.txt:1-6')

put('flavorCNE.6.d',
"[SCOPE.sState('cne_land_reform_mess_imprisonment_state').GetName]的清丈官员拘捕了一批代写田契诉状的乡民，将他们以串通隐产的罪名交由驻军看押。军官随即扩大搜捕，地方士绅、乡校教员与整理旧契的书吏都被带入营中。\\n\\n新法赋予官员清理田产的权力，也准许农户为自己的产业提出申诉。囚犯的家属带着田契到省城求告，省督将案情报请刑部查办。负责清丈的官员却以军民勾连、恐生变乱为由，请兵部保护承办军官。若只把涉事官吏调离，营中的追捕便可轻轻揭过；若要追究，清丈官也须为奉行新法时犯下的罪行负责。",
"Land commissioners in [SCOPE.sState('cne_land_reform_mess_imprisonment_state').GetName] have arrested villagers who drafted petitions over disputed titles and placed them in military custody for concealing property. Officers widened the arrests to local gentry, teachers and clerks who kept the old deeds.\\n\\nThe new law empowers officials to settle land ownership, but also permits farmers to defend their property. The prisoners' families have taken their deeds to the provincial capital, and the governor has referred the case to the Ministry of Justice. The commissioners warn of collusion and unrest and ask the Ministry of War to protect the officers involved. Transferring a few officials would allow the affair to pass quietly. A prosecution would make the reform's own agents answer for crimes committed in its name.",
'Give the new prose the actual choice between transfer/impunity and punishment, with governor and ministries instead of generic court referrals. Preserve the author’s options.', 'events/flavorCNE_ce.txt:349-441; '+BASE+':97-98; '+CAN,
'A gives military loyalists, intelligentsia/landowner radicals and +7 disorder; B -1 progress if possible and -4 disorder. No purge or literal character transfer effect.')
put('flavorCNE.7.d',
"[SCOPE.sState('cne_land_reform_industrialists_support_state').GetName]的厂主与商人联名呈请，愿意为土地改革垫付一笔款项。工坊正在扩建，商路上的货车日渐增多；他们希望新法能够准许农户自由迁居，将更多劳动力带入城镇。\\n\\n商人的代表还请求通过咨议局提出土地、道路与雇工契约方面的建议。省督愿意接纳这笔资助，户部官员则认为，这些人有财力，也熟悉实业，可以让他们更多参与政府事务。这批新兴的产业家，希望在帝国政府中取得与其财富相称的位置。",
"Manufacturers and merchants in [SCOPE.sState('cne_land_reform_industrialists_support_state').GetName] have jointly offered to finance land reform. Workshops are expanding and more carts travel the commercial roads. They want the new law to allow farming families to move freely and bring more workers into the towns.\\n\\nTheir representatives also seek to submit proposals on land, roads and employment contracts through the Consultative Council. The governor is willing to accept the funding. Officials in the Ministry of Revenue argue that these wealthy men understand industry and could take a greater part in government. The rising manufacturers hope to gain a position in imperial affairs commensurate with their wealth.",
'Do not imply purchase of a parliamentary seat; retain the author’s support-versus-political-influence choice and specify the advisory channel.', 'events/flavorCNE_ce.txt:443-532; '+BASE+':103-104; '+CAN,
'A state industrial modifier and industrialist loyalists; B national industrial influence modifier and +2 progress; both add disorder. No treasury gift or Senate appointment is explicitly scripted.')
put('flavorCNE.8.d',
"[SCOPE.sState('cne_land_reform_peasants_in_city_state').GetName]的街巷里住进了许多来自乡间的新客。农户卖去田产，带着家人寻找工钱；招工的牙行将他们送往厂房和工地，又从每一份工资中扣取引荐与食宿的费用。\\n\\n一批工人向官府告发牙行私扣契约、追索旧债。厂主担心查办牙行将妨碍招工，地方士绅也替这些与乡党往来密切的经纪说情。省督须决定，是责令官署查办这些束缚雇工的行会，还是将争端仍作普通民事案件处置。农民离开旧田庄以后能否自由谋生，正在这些新生的城镇中受到考验。",
"The streets of [SCOPE.sState('cne_land_reform_peasants_in_city_state').GetName] are filling with newcomers from the countryside. Farming families have sold their land and come in search of wages. Employment brokers send them to factories and building sites, deducting recruitment and lodging charges from their pay.\\n\\nWorkers have accused the brokers of withholding contracts and enforcing old debts. Manufacturers fear that an inquiry will disrupt recruitment, while local gentry defend brokers linked to their own associations. The governor must decide whether to prosecute the organisations that bind workers to them or leave the disputes to ordinary civil proceedings. In these growing towns, the promise that peasants could leave their old estates and freely earn a living faces its first practical tests.",
'Specify governor and connect protected brokers to the actual gang modifiers and industrialist/landowner costs. Avoid docks in randomly chosen inland states.', 'events/flavorCNE_ce.txt:534-638; '+BASE+':118-119; '+CAN,
'A gang crackdown, industrialist/landowner radicals, +2 progress/-4 disorder; B gang triumph,+3 progress/+7 disorder. Mature option wording retained.')

put('nesnd_cne_funding.1.d',
"[SCOPE.sState('nesnd_cne_funding_state').GetName]的省督呈报，许多离开田庄的乡民尚不熟悉工坊所需的手艺，在城镇中难以谋生。户部据此拟定拨款，供当地兴办实业学堂，并扶助工坊扩建。若能使乡民学会新业，地权改革所许诺的自由便有了生计上的依托。",
"The governor of [SCOPE.sState('nesnd_cne_funding_state').GetName] reports that many people leaving the estates lack the skills needed by workshops and struggle to find a living in town. The Ministry of Revenue proposes a grant for practical schools and workshop expansion. Learning a new trade would give these families the means to use the freedom promised by land reform.",
'Replace a land commissioner acting as a general economic ministry with provincial governor→Revenue Ministry funding; retain qualifications/construction causal link.', 'events/nesnd_cne_funding.txt:1-24; common/scripted_effects/nesnd_cne_reform.txt:40-49; common/static_modifiers/nesnd_cne_reform.txt:1-6; '+CAN,
'Chooses eligible reform state of highest unemployment; 12-month +10% construction, +15% qualifications, +2% education access after paid approval. Does not create an actual school/factory building.')
put('nesnd_cne_funding.2.d',
"[SCOPE.sState('nesnd_cne_funding_state').GetName]的省督请求增拨救济。失去收入的家庭已经开始减少口粮，城内的招工尚不足以安置他们。户部拟在原有救济上加发一年的补助，供这些家庭度过转业的难关，现已呈请批准。",
"The governor of [SCOPE.sState('nesnd_cne_funding_state').GetName] requests additional relief. Families without an income are cutting their meals, and the towns offer too few jobs to support them. The Ministry of Revenue proposes a year of additional payments through the existing relief institutions and has submitted the grant for approval.",
'Make the fiscal actors concrete and retain the one-year supplement rather than a new welfare institution.', 'events/nesnd_cne_funding.txt:25-48; common/scripted_effects/nesnd_cne_reform.txt:62-71; common/static_modifiers/nesnd_cne_reform.txt:7-10; '+CAN,
'12-month +0.10 state welfare payments; social security already required. No guaranteed end to starvation.')
put('nesnd_land_survey_desc','由户部拨助工坊与实业学堂，使离开田庄的乡民学会新业，参与产业的增长。','Provide Revenue Ministry funding for workshops and practical schools, helping people leaving the estates learn new trades and take part in industrial growth.',
'Actual cost comes from treasury, not an implemented stream of profits from land confiscation.', 'common/scripted_effects/nesnd_cne_reform.txt:40-49; '+CAN,'Funds existing state modifier via confirmation, not buildings or an earmarked sale-income account.')
put('nesnd_land_review_desc','由刑部会同户部复核地权争讼，责令省督查明地方官员执行新法的情形。已经取得田产的农户，应当能够依法保有他们的生计。','Have the Ministries of Justice and Revenue review land disputes and instruct provincial governors to investigate the conduct of reform officials. Farming families should be able to defend the property the new law has granted them.',
'Use competent ministries and provincial heads; retain the original promise of secure land rights.', 'common/scripted_effects/nesnd_cne_reform.txt:51-61; '+CAN,'Paid 12-month appeals modifier and -5 disorder; no automatic court institution/law enactment.')
put('nesnd_land_military_desc','由户部向已有救济机关增拨款项，接济离开田庄、尚未找到生业的农户，使失去收入的人仍能维持日用。','Have the Ministry of Revenue supplement existing relief funds for farming families who have left the estates and have yet to find a livelihood.',
'Concrete fiscal actor, existing institutions and affected population.', 'common/scripted_effects/nesnd_cne_reform.txt:62-71; '+CAN,'Relief through approval event only.')

put('nesnd_cne_camps_journal_reason',
'自1444年以来，北明秦藩的军屯逐渐发展为遍及北方的营产制度。军队凭借地产取得粮饷，朝廷借助军队推动征税、扩张与征服，军国与农业的利益由此紧密相连。如今要让田产与矿业转入民用经营，便必须触动军中的旧利。\\n\\n户部要求各省将营产纳入通常的赋税与经营，兵部则须应付将领对军饷和旧功的索求。省督负责推行新法，手中却未必有足以压服驻军的力量；元老院里的开国勋旧，也不会轻易答应剥去自己的产业。各省可以分别办理，遇到难以收束的争端时再予暂缓。军队失去的地产，终须由新的财政与生产来弥补。',
"Since 1444, the Qin military colonies of Northern Ming have developed into an estate system across the north. Land supplied the army's food and pay, while the army sustained taxation and conquest. Military and agricultural interests grew together. Bringing these lands and mines into civilian use now threatens entrenched military privileges.\\n\\nThe Ministry of Revenue wants the estates brought under ordinary taxation and management. The Ministry of War must answer officers who invoke unpaid wages and past service. Governors charged with enforcing the law may lack the force to compel their garrisons, while the founding commanders in the Senate are reluctant to surrender their own property. The provinces can proceed separately and suspend reform where disputes become unmanageable. New revenue and production must eventually replace the army's landed income.",
'Clarify the ministry/governor/garrison/Senate conflict requested by the author and retain historical origin and individual province pacing.',PR+'; '+CAN,
'22 separate state programmes; each adds civil production/tax/construction modifiers and cumulative military approval/officer loyalty opposition. No central parliament or universal compliant governors.')
put('nesnd_cne_urban_journal_reason',
'乡民离开田庄之后，必须在工坊、矿山与城市中找到新的位置。帝国需要从煤铁到钢铁、工具与机器的连续生产，也需要让劳动者能够承受疾病、失业与衰老。六部所议的实业、学政与救济，到了地方都须由省督筹措、施行。城市扩张所带来的新职业和新学问，也将动摇旧日乡校与士人的权威。',
"People leaving the estates need work in workshops, mines and towns. Coal and iron must sustain the production of steel, tools and engines, while relief helps workers endure illness, unemployment and old age. The industrial, educational and welfare measures discussed by the Six Ministries depend on governors to organise and carry them out. The occupations and learning that grow with the cities will also weaken the authority of the old rural schools and scholars.",
'Retain industrial/livelihood theme; concretise execution without inventing a ministry name or parliamentary sovereignty.',PR+'; '+CAN,'Activation requires existing industry/welfare; programme itself modifies politics, law success, minimum wages and monthly reform progress. It does not construct buildings.')

for x in rows:
 k=x['key']
 if re.match(r'nesnd_cne_camp_.+_start_button_desc$',k):
  state=re.search(r'\$STATE_[A-Z_]+\$',old(k))[0]
  put(k,None,f'Bring military land and mining revenues in {state} under civilian management and taxation.',
      'Retain suitable Chinese action; English omitted its civil administration purpose.',PR,'Same per-state start effect; no prose variations invented for identical mechanics.')
 elif re.match(r'nesnd_cne_camp_.+_stop_button_desc$',k):
  state=re.search(r'\$STATE_[A-Z_]+\$',old(k))[0]
  put(k,f'暂缓{state}的营产整顿，令地方官员停止清理，容各营暂依旧例经营。',f'Suspend estate reform in {state}, recall the officials conducting the clearance and allow the garrisons to continue under the old arrangements.',
      '“撤回收益与相应军队反对” describes removing modifiers, not an action within the world. The common tooltip already displays the mechanical removals.',PR,'Removes that state’s programme flag, benefits and matching military/officer penalties; restart remains possible.')

put('nesnd_cne_land_start_tt',None,
'Monthly reform progress #p +0.25#!. Landowners approval #n −2#!, Rural Folk approval #n −1#!; Landowners attraction #n −15%#! and Industrialists attraction #p +15%#!. Enactment success #p +5 percentage points#! and minimum wage #p +5%#!. Costs #n 10#! public confidence per year.',
'Remove English-only defensive “without approval gain”; retain exact actual effects.',PR,'No numerical change.')
put('nesnd_cne_confidence_journal_reason',
'大革命的烽火已经远去，却还照着这一代人的前路。县署中的吏员、营垒里的中下军官与士兵，以及渴望摆脱旧日束缚的农民，仍把地权革命视为当年誓言的延续。\\n\\n牧仲棠称帝以后，六部掌理政务，元老院中的开国将领与勋旧大臣独掌立法之权。咨议局收集陈情、提出建议，能否施行仍须由掌权者裁定。南方与西北的流亡共和党人将牧仲棠斥作叛国者；在许多支持改革的人心中，牧皇及其同道仍代表着开蒙运动与进步的希望。帝国的政令得以推行，也有赖于这些官员、士兵和农民尚未冷却的热情。一次次清丈、迁业与整营，都在要求他们继续忍耐。',
"The fires of the Great Revolution have faded, but its promises still guide clerks, junior officers, soldiers and peasants seeking release from old obligations. They see the land revolution as the continuation of an unfinished cause.\\n\\nAfter Mu Zhongtang became emperor, the Six Ministries administered the state, while founding commanders and senior ministers in the Senate monopolised legislative power. The Advisory Council gathers petitions and makes proposals whose fate rests with those who govern. Republican exiles in the south and northwest call Mu a traitor. Many supporters of reform still regard him and his companions as champions of enlightenment and progress. Imperial policy depends on the surviving enthusiasm of these officials, soldiers and farmers. Each new survey, change of occupation and reorganisation of the estates asks them to endure more.",
'Ground the new confidence JE in the author’s concrete constitutional canon; remove repetitive abstract contrast while preserving divided revolutionary loyalties.',CF+'; '+CAN,
'Confidence represents public/political endurance, not a legislature variable. No vote or constitutional mechanic is added.')
put('nesnd_cne_confidence.5.war','内战已经爆发，地方官署与营伍各奉其主。清丈与迁业的命令被军令取代，朝廷再也无法依照原定的章程推行地权革命。','Civil war has broken out. Provincial administrations and armies now answer to rival governments. Military orders have displaced the work of land reform, and the court can no longer carry out the campaign.',
'Trigger covers both native revolution and secession war; do not label every secession a revolutionary war.',CF+'; common/scripted_triggers/nesnd_cne_confidence.txt:1-13','No branch or effect changes.')
put('nesnd_cne_confidence.5.a','停止改制，收束诸项新政。','End the reform and close its programmes.',
'A reform failure may occur after monarchy was abolished, so “收回诏令” is not universal to all branches.',CF,'Single acknowledgement option; cleanup has already happened.')
put('nesnd_cne_confidence_aftermath',None,'The upheaval of the war has yet to subside.',
'Current English announces rebel defeat; status checks only rose=true and not currently fighting and may appear while war creation is pending. Match the noncommittal Chinese.',CF+'; common/journal_entries/nesnd_cne_confidence.txt:12-18','No state transition inferred.')
put('nesnd_cne_confidence.3.d','帝国旧政府已经倒下。共和军接收了其州郡与官署，以大汉共和邦之名建立新政府。对于湖南、湖北与四川尚未归本国或其附属统辖的地区，新政府重申了大革命以来统一国家的主张。',
'The imperial government has fallen. The republicans have taken over its provinces and offices and established the Han Commonwealth. The new government reasserts the revolutionary claim to national unity in those parts of Hunan, Hubei and Sichuan still outside its own rule or that of its subjects.',
'Do not introduce an unestablished republican assembly; align claim description with actual subject exclusions.', 'common/scripted_effects/nesnd_cne_republic.txt:110-175','Claims only for still foreign-controlled state regions; no automatic southern invasion or annexation.')

put('nesnd_reform_status_warmup','各省正在向户部呈报民生情形，初次汇总需三个月。\\n$nesnd_land_rules_link$','The provinces are reporting on living conditions to the Ministry of Revenue. The first survey takes three months.\\n$nesnd_land_rules_link$',
'Remove data-collection/settlement implementation voice while retain player-relevant initial wait.', 'common/scripted_effects/nesnd_crisis_effects.txt:17-28; '+CAN,'Monthly effects start after samples >3, not falsely at first month.')
put('nesnd_reform_status_law','#bold 产权改革尚待立法#!：须确立自耕农、商业化农业或集体化农业制度。\\n$nesnd_land_rules_link$','#bold Land legislation pending.#! Establish peasant proprietorship, commercialised agriculture or collectivised agriculture.\\n$nesnd_land_rules_link$',
'Remove “开始结算制度落实的成果”; keep actual law gate.', 'common/scripted_triggers/nesnd_cne_reform.txt:16-22; common/journal_entries/ce_cne_land_draft.txt','No law enacted by text.')

trans('ce_cne_land_reform','Land Rights Revolution',BASE+':13')
put('ce_cne_land_reform_reason',None,
'This movement began with the Western Qin Great Revolution of 1810. People of the age understood it as a modern economic transformation arising among the agrarian states of the East, where powerful lineages had long dominated rural life. Through purchase or compulsory confiscation, land accumulated beyond all measure by its old owners was redistributed among a portion of the peasantry. The aim was to break the lineages’ hold over the rural population. The ruling group of the Empire of China suspended the movement during its rise to power. Around Mu Zhongtang’s southern campaign of 1820, however, he and his confidants revived it to restore the economy, free productive activity and mobilise peasants and soldiers.',
'Keep the mature Chinese original byte-for-byte; replace Chinese fallback in the effective English layer with a faithful translation, without the older English’s invented extra theory.',BASE+':15','Historical JE reason; no condition or effect altered.')
put('flavorCNE.3.d',None,
'Our revised laws on land, employment and family relations have reached every corner of the Empire and established a new economic order. We have freed people from the bonds of kinship that held them for thousands of years. The fields have returned to their proper place as a natural resource.\\n\\nAs the old lineages and their land can no longer bind the peasantry, young faces, dusty yet full of life, stream from the countryside into the cities. They dream of a new life built through human intelligence and science. The remnants of hereditary power disguise themselves as local associations and try to regain control over them. Police batons and the magistrate’s gavel will break their ambitions.\\n\\nOnce more we have brought the founding emperor Mu Zhongtang’s ideals into reality. We have shown that this Empire was built for the interests of the Huaxia nation. It will protect even the weakest person’s freedom to choose a future. Those now seeking happiness in the cities are bringing new prosperity to the Empire.',
'Restore full English in the winning layer without rewriting the mature author Chinese or reducing land/labour emancipation to paperwork.',BASE+':69','Success event; preserve established author rhetoric and political viewpoint.')
trans('flavorCNE.3.f','From each according to ability, by free will. The state voices the people’s aspirations; together they build the Empire. \\n—Cha Wanfang, Memorial on the People’s Grant of the Imperial Mandate',BASE+':70')

# Keep complete parallel inventory, including inactive legacy keys. Decisions below
# are semantic review decisions, not a claim that regex reachability proves runtime.
inactive={
 'ce_cne_land_draft_failing','ce_cne_land_draft_failing_reason','ce_cne_land_draft_failing_goal','cne_landreform_failure_tracker_100',
 'nesnd_land_survey_requirements','nesnd_land_military_requirements','nesnd_land_review_requirements','nesnd_land_status_petition',
 'nesnd_cne_land_status','nesnd_cne_urban_status','nesnd_cne_start_requirements','nesnd_cne_land_requirements','nesnd_cne_urban_requirements','nesnd_cne_funding_requirements',
 'nesnd_reform_completion_tt','nesnd_reform_failure_tt',
}
for k in by:
 if k.startswith(('ce_cne_reform_limited_market_access','ce_cne_war_with_western_qin','ce_cne_war_with_usm','ce_cne_technology_advantage','ce_cne_reform_legal_system')):inactive.add(k)

for k in list(P):
 if k.startswith('nesnd_crisis.20.'):
  del P[k]
for p in P.values():
 p['en']=p['en'].replace('Advisory Council','Consultative Council')
 p['reason']=p['reason'].replace('Advisory Council','Consultative Council')
(R/'cne-proposals.json').write_text(json.dumps(P,ensure_ascii=False,indent=2),encoding='utf-8')
inventory=[]
for r in rows:
 k=r['key'];p=P.get(k)
 for lang in ['simp_chinese','english']:
  d=r[lang]['candidate']
  if not d:continue
  proposed=p['zh' if lang=='simp_chinese' else 'en'] if p else d['text']
  change=proposed!=d['text']
  if k.startswith('nesnd_crisis.20.'):why='交由 /root/usm_prose_research 审查与提案，已发送触发和效果核对；避免两个代理覆盖同一作者改稿。'
  elif p:why=p['reason']
  elif k in inactive:why='保留／未使用：当前调用已改为原生条件、其他状态或 disabled legacy JE；不把遗留文案列作已显示的新行为。'
  elif r[lang]['origin']=='baseline_unchanged':why='保留：与作者最初基准逐字相同；无本轮设定或效果冲突需要改动。'
  elif k.startswith('nesnd_cne_camp_'):why='保留：22州逐一核对相应启动/暂停 effect；名称、地区和修正对象一致。'
  elif k.startswith('nesnd_cne_feedback_'):why='保留：数值提示与对应 choice/effect 的增减及边界一致。'
  elif any(w in k for w in ['_tt','_condition','_requirements','_delta_','_conf_','_bar','_status','_running','_gone','_failure']):why='保留：显示条件、数值、统计或效果名称与现行脚本相符。'
  else:why='保留：已逐项核对叙事主语、制度、两种语言及触发/效果；无需为统一句式改写。'
  inventory.append({'key':k,'language':lang,'file':d['file'],'line':d['line'],'origin':r[lang]['origin'],'decision':'revise' if change else 'keep','reason':why,'before':d['text'],'after':proposed,'effective_layers':r[lang]['layers']})
for k,p in P.items():
 if k not in by:
  for lang,field in [('simp_chinese','zh'),('english','en')]:
   inventory.append({'key':k,'language':lang,'file':'NEW guarded branch','line':0,'origin':'new_guarded_localization_branch','decision':'revise','reason':p['reason'],'before':'','after':p[field],'effective_layers':[]})
(R/'cne-inventory-review.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
md=['# CNE 中英文逐项对读','', '这是只读编辑提案；未接入游戏、未开游戏。基准、现行文本、最终覆盖层及逐条结论见同目录 JSON。', '',f'共 {len(rows)} 个键 / {len(inventory)} 条语言记录；{len(P)} 个键有建议，{sum(x["decision"]=="revise" for x in inventory)} 条语言记录返工。','', '## 各文件完整清单','']
files=sorted({x['file'] for x in inventory})
for f in files:
 items=[x for x in inventory if x['file']==f]
 md += ['### '+f,'','|键|行|结论|依据|','|---|---:|---|---|']
 for x in items:md.append('|'+x['key']+'|'+str(x['line'])+'|'+x['decision']+'|'+x['reason'].replace('|','\\|')+'|')
 md.append('')
md += ['## 逐条返工对照','']
for k,p in P.items():
 md += ['### '+k,'','- 来源：'+p['source'],'- 效果：'+p['mechanic'],'- 原因：'+p['reason'],'','**原中文**',old(k),'','**建议中文**',p['zh'],'','**原英文**',old(k,'english'),'','**建议英文**',p['en'],'']
(R/'cne-writing-comparison.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'proposal_keys':len(P),'inventory_keys':len(rows),'language_rows':len(inventory),'revised_language_rows':sum(x['decision']=='revise' for x in inventory)},ensure_ascii=False))
