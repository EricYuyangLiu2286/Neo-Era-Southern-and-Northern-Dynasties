# 日本、西秦—波斯与周边文本逐项审校

状态：EDITORIAL_PROPOSALS / ENGINE_NOT_RUN。只写WORK报告；未改MOD、E、C、技能或游戏。
共776个键记录，266项双语修改/新增分支建议。统计与每文件SHA见japan-qin-summary.json和japan-qin-reviewed-files.json。

## 来源与本轮编辑决定

作者样本来自指定pre-update基准，直接回读并重新核SHA；当前原版为1.13.11/build24799966，catalog状态CURRENT。完整20条来源见japan-qin-sources.json。此前缓存的law_autocracy行号落在空行，已按实际键重新定位；未拿缓存摘要当原文。

|类别|作者/原版样本|本轮应用|
|---|---|---|
|改革结果|flavorCNE.3.d将法律、劳动迁移与政治利益连成因果|日本军政结局写现有兵制/工场支持；不统一添无来源反对者和道德总结。|
|承担者|flavorCNE.4.d具体区分旧社会、新贵、乡绅与社会中层|西秦安国胜利按实际effect写军队、小市民、知识分子、实业家，不把小市民改成勋贵地主。|
|历史与行动者|flavorUSM.4.d的过去征战及现时军政关系|陈秦皇帝历史不删除；共和后常驻日志改过去时，奖掖对象保留皇族势力。|
|政治选项|ce_french_support_dynasty_button_desc明确行动立场|外交成功答复陈述已得到的自治/独立/许可/资金，不只写依商定办法办理。|
|英文JE|native je_meiji_restoration_reason；je_sick_man_bureaucracy_reason|用明确行为者和英语因果句重写；不逐个复制中文逗号，已发生/计划/条件分开。|
|英文军政|native je_french_foreign_legion_reason|吕宋直接解释谁提供舰船、谁承担军费、何时同意；不反复铺陈册簿印信。|
|UI数值|原作者ce_french_empire_oreleans_progress_bar_desc|金额、库存/每周流量、binding period与自动终止分别保留。所有引号/动态scope保留。|

## 适用包与交接约束

- C_only：尚未部署的日本开发候选。包括JIM摄政、七地区统一结局；E/main仍九地区条件，严禁仅改文案偷换目标。
- E_and_C：既有秦/波斯/吕宋/丹那沙林/地图等文本。
- requires_branch：只有根任务补齐实际desc分支/回复类型scope后方能生效；新增localization键本身不会改变显示。
- `.4.d_unavailable` 供波斯援助路线无法成立QE1朝贡关系时使用；默认`.4.d`只用于当下仍真实subject_of QE1。
- 日本foreign.2六段分支需在clear_request之前保存request_kind；kind6吞并不发送该答复，不新加死对象引用。
- 外国交涉external、供应supply、混合crisis和HNA由USM审校者负责；CNE_attrative_general_as_leader和混合文件中的supply_status_bankruptcy标DELEGATED。

## 逐项对照

下列原稿是本次读到的有效键值。被日本开发覆盖的旧值仍保存在inventory的occurrences.original_value中，不能把旧层存在等同于生效。所有编辑改稿均为本轮提案，不冒称作者原作。

### `nesnd_japan.1.d`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：南京的使节带来了一份新的封国方案。天皇将亲政京都与大阪，德川以江户为府，丰臣退守关西，九州和四国则交由吴朝直接管理。两百年来丰臣依靠唐土军力取得的霸业，如今被写进了另一位天下人的分封册。家臣们已将各处兵粮与守备送到[ROOT.GetCountry.GetRuler.GetFullName]案前，等候大坂的命令。

**原AI英文**：Envoys from Nanjing propose direct imperial rule in Kyoto and Osaka, a Tokugawa government in Edo, a reduced Toyotomi domain, and Wu administration of Kyushu and Shikoku. Retainers have placed the garrison and supply returns before [ROOT.GetCountry.GetRuler.GetFullName]. The decision now rests with Osaka.

**本轮中文**：南京使节带来了新的分封方案：京都与大阪奉天皇名位，由摄政主持政务；德川以江户为府，丰臣退守关西，九州和四国则归吴朝直辖。丰臣借唐土之力建立的霸业，如今面临唐土朝廷提出的分割。家臣已呈上各地兵力与军粮，等候[ROOT.GetCountry.GetRuler.GetFullName]决定如何答复。

**本轮英文**：Envoys from Nanjing have brought new terms. Kyoto and Osaka would recognize the Emperor, with a regent conducting the government; the Tokugawa would rule from Edo, the Toyotomi would retain a reduced western domain, and Wu would administer Kyushu and Shikoku directly. The mainland court whose armies helped establish Toyotomi power now proposes to divide it. Retainers have reported the strength and supplies of the garrisons to [ROOT.GetCountry.GetRuler.GetFullName], who must decide how to answer.

**原因**：天皇亲政与林摄政冲突；删去分封册的道具式收束，保留谈判局势与现有ruler引用。

**来源**：Author latest JIM/Lin correction; C/events/nesnd_japan_events.txt:2; C/common/scripted_effects/nesnd_jp_imperial_court.txt

**实际机制**：Partition proposal, not completed partition. Existing ROOT ruler token retained.

### `nesnd_japan.3.d`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：新的封国诏令已经发往日本各地。丰臣以中国地区和关西余部存其家业，德川接掌江户及北方诸侯，天皇在京都亲理政务，大阪商人与公卿有了共同的朝廷。九州、四国归吴朝直接管理。各府随领土接收百姓、田地与产业，旧日统一的征税和军需体系也由此分开。

**原AI英文**：The Toyotomi retain western domains, the Tokugawa govern Edo and the north, and the Emperor rules Kyoto and Osaka. Wu administers Kyushu and Shikoku directly. Each authority receives the people, land and industries of its territory; taxation and military supply must now follow the new jurisdictions.

**本轮中文**：日本的分封已经施行。丰臣保有关西余部与中国地区，德川接掌江户及北方领地；京都与大阪奉天皇名位，由摄政主持和国政务。九州、四国归吴朝直辖。各政权接管辖地的税赋与军队，原由丰臣统一调度的兵力和财源从此分属数家。

**本轮英文**：The settlement in Japan is in force. The Toyotomi retain Chugoku and the remainder of Kansai; the Tokugawa take Edo and the northern domains. Kyoto and Osaka recognize the Emperor, with a regent conducting Wa’s government. Wu administers Kyushu and Shikoku directly. The new governments take charge of local revenues and armies, dividing the resources once commanded by the Toyotomi.

**原因**：天皇亲理政务与已确认摄政制度冲突；各府为日本军政政权用语合法，无需全局改省。

**来源**：Author latest JIM/Lin correction; C/events/nesnd_japan_events.txt:80

**实际机制**：Only valid with new C partition/regency behavior.

### `nesnd_japan.5.d`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：本州、九州与四国的政令终于归于一府。[ROOT.GetCountry.GetName]取得了自行处理内外事务的地位，各地官员开始合并税册、衔接道路，编整曾分属不同诸侯的军队。城下町的货物越过旧日关卡，商人与农民也将逐渐面对同一套赋役和法令。

**原AI英文**：Honshu, Kyushu and Shikoku now answer to one independent government. [ROOT.GetCountry.GetName] begins consolidating taxation, roads and military administration across the former domains.

**本轮中文**：本州各地终于归于同一个独立政府。[ROOT.GetCountry.GetName]开始接管旧诸侯的赋税与军队，使彼此分立的领地遵行共同的法令。城下町的商人也在等待关卡和赋役的重新议定，准备把生意做到旧日领界之外。

**本轮英文**：Honshu now answers to one independent government. [ROOT.GetCountry.GetName] is bringing the revenues and armies of the former domains under common authority. Merchants in the castle towns await a settlement of tolls and taxes as they prepare to trade beyond the old domain boundaries.

**原因**：新C日志只需本州七地区；旧事件断言九州四国已统一。E仍九地区要求，禁止把该改稿提前套入E。

**来源**：C/common/journal_entries/nesnd_japan.txt:64; C/common/scripted_triggers/nesnd_japan.txt:87; C/common/scripted_triggers/nesnd_jp_development.txt:12; C/events/nesnd_japan_events.txt:98

**实际机制**：Seven Honshu regions + independence; no Kyushu/Shikoku ownership guarantee.

### `nesnd_japan_war_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：日本若为吴朝属国，将脱离吴朝并进入真实外交博弈。吴朝主张重组日本，日本获得羞辱吴朝的战争目标。#v 只有重组目标被执行才划分领土。#!

**原AI英文**：A Japanese subject will become independent and enter a real diplomatic play. Wu demands partition; Japan receives a humiliation war goal. #v Territory changes only if the partition goal is enforced.#!

**本轮中文**：日本若为吴朝属国，将脱离吴朝并进入[concept_diplomatic_play]。吴朝主张重组日本，日本则要求羞辱吴朝。#v 重组日本的战争目标获执行后，才会划分领土。#!

**本轮英文**：If Japan is a Wu subject, it will become independent as the [concept_diplomatic_play] begins. Wu demands the reorganization of Japan; Japan demands Wu’s humiliation. #v The territorial settlement takes effect only if Wu’s war goal is enforced.#!

**原因**：真实/real是开发验证口吻；保留独立、双方战目标及领土执行条件。

**来源**：M/common/scripted_effects/nesnd_japan.txt; M/common/war_goal_types/nesnd_japan.txt

**实际机制**：No change to truce, relationship or war goal.

### `nesnd_wu_eastern_question_reason`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：丰臣氏借明吴之力平定战国，又与郑氏共争朝鲜。两家的旧盟维持了海东秩序，也使九州的吴人驻军与日本诸侯结下了绵延数代的利害。如今南朝大局已定，朝廷开始议论东征：将西军旧部调往海东，以天皇和德川分掌日本，收九州、四国为直辖。远洋诸藩的军饷、商路和驻军同样等着南京作出安排。

**原AI英文**：The Toyotomi unified Japan with Ming and Wu assistance and fought beside the Zheng in Korea. The court now considers dividing authority between the Toyotomi, Tokugawa and Emperor, with Kyushu and Shikoku under direct Wu administration. The expedition would also remove old western officers from the mainland. Overseas garrisons and commerce still compete for the same ships and revenue.

**本轮中文**：丰臣氏借明吴之力平定战国，又与郑氏共争朝鲜。两家的旧盟维持了海东秩序，也使九州驻军与日本诸侯结下了绵延数代的利害。如今南朝大局已定，朝廷开始议论东征：将西军旧部调往海东，在丰臣之外扶植天皇与德川的政权，使三家各领其土，九州、四国则归吴朝直辖。远洋驻军与海上商路，也将随这次分封重新安排。

**本轮英文**：The Toyotomi unified Japan with Ming and Wu assistance and fought beside the Zheng in Korea. Their old alliance bound the garrisons in Kyushu to the interests of Japan’s lords. With affairs in the south settled, the court is considering an expedition: send former western officers overseas and establish imperial and Tokugawa governments alongside the Toyotomi, while placing Kyushu and Shikoku under direct Wu administration. The settlement would also reshape overseas garrisons and maritime trade.

**原因**：原中文只提天皇/德川分掌，遗漏仍保留的丰臣政权；三方分封符合E/C共同效果，不宣布天皇亲政或提前写入C摄政。

**来源**：M/common/scripted_effects/nesnd_japan.txt; C/common/scripted_effects/nesnd_japan.txt

**实际机制**：Three Japanese governments plus direct Wu holdings; regency identity not asserted in this shared JE.

### `nesnd_japan.2.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：日本使者请求收回分封诸藩的方案，仍由丰臣主持海东政务。南京已经掌握九州驻军、舰队和诸藩商路，东征可以调走本土旧军，扶植更依赖朝廷的日本诸侯。军费、舰船与海外防务也将随远征重新分配。这份安排现已送至[ROOT.GetCountry.GetRuler.GetFullName]面前。

**原AI英文**：Japan asks to retain a unified government. Wu controls garrisons, fleets and trading connections, and an expedition could install dependent lords while employing old mainland officers overseas. Its costs will compete with other imperial commitments. The proposal is before [ROOT.GetCountry.GetRuler.GetFullName].

**本轮中文**：日本使者请求撤回分封方案，仍由丰臣统一主持海东政务。南京朝廷准备以东征扶植新的日本政权，把丰臣掌握的兵力与财源分到数家。军费、舰船与海外防务也须随之重新安排。如何答复这项请求，已交由[ROOT.GetCountry.GetRuler.GetFullName]裁定。

**本轮英文**：Japan asks the court to withdraw the partition proposal and retain a unified Toyotomi government. The proposed expedition would establish new Japanese governments and divide the forces and revenues now commanded by the Toyotomi. It would also require new arrangements for military spending, shipping and overseas defence. The decision rests with [ROOT.GetCountry.GetRuler.GetFullName].

**原因**：原文无条件声称南京控制九州驻军，但分封允许保留外国领土且不保证吴当前控制九州；以真实提议替代无守卫持地断言。

**来源**：M/events/nesnd_japan_events.txt:32; M/common/scripted_triggers/nesnd_japan.txt

**实际机制**：Fallback negotiation event; existing ROOT ruler token retained. No new direct possession asserted.

### `nesnd_jp_food_supply_reason`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：田间的收成、渔人的船和往来的粮商，维持着城里的生活。粮价一涨，官署里的争论很快便会传到街市。政府须让运粮的人愿意进城，也让城里的人买得起饭。

**原AI英文**：Harvests, fishing boats and grain merchants sustain life in the towns. A rise in food prices can carry a dispute from government offices into the streets. Food must reach the markets at prices townspeople can afford.

**本轮中文**：田间的收成、渔人的船和往来的粮商，维持着城里的生活。粮价一涨，街市上的怨声便传到官署。政府须让运粮的人愿意进城，也让城里的人买得起饭。

**本轮英文**：Harvests, fishing boats and grain merchants sustain life in the towns. When food prices rise, complaints from the markets soon reach the authorities. The government must keep food coming into the towns at prices their people can afford.

**原因**：原句把粮价危机写成官署争论传到街市，因果和行动主体含混。

**来源**：C/common/scripted_triggers/nesnd_jp_industry.txt:57; author flavorCNE.3.d

**实际机制**：Food supply allows farming OR affordable grain; no invented self-sufficiency requirement.

### `nesnd_jp_food_processing_reason`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：罐藏技术让粮食与鱼获能够保存得更久，也把收购、加工和远途运输变成了同一门生意。商人可以等待更好的价钱，工场里的雇工则希望生产不再随着收获季节一同停下。

**原AI英文**：Canning allows food and fish to be stored longer, bringing purchasing, processing and long-distance transport into a single trade. Merchants can wait for better prices, while workers hope the factories will offer employment beyond the harvest season.

**本轮中文**：城镇需要能够储存和远运的食品，粮商与渔商也在寻找收获季节以外的买主。罐藏技术让他们有机会把收购、加工和运输连成一门生意；办起食品工场，还能让雇工不必随收获季节结束而失去工作。

**本轮英文**：The towns need food that can be stored and carried over long distances. Grain and fish merchants want customers beyond the harvest season. Canning offers a way to combine purchasing, processing and transport in one business, while food factories could provide work after the harvest is over.

**原因**：常驻待完成日志尚未保证已研发罐藏；由已实现事实改为待建产业及技术用途。

**来源**：C/common/scripted_triggers/nesnd_jp_industry.txt:71

**实际机制**：Technology canneries and active cannery PM are completion requirements, not entry requirements.

### `nesnd_jp_development.2.d_military`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：主张集权的军官终于让自己的办法成为国策。征募、训练和军需被纳入更严密的组织，地方官员也须执行中央的命令。\n\n他们把这一结果视为国家重新强盛的开端。军费的负担和军官的权力，却会长久留在民间的议论之中。

**原AI英文**：Officers who argued for central authority have secured the policy they wanted. Recruitment, training and military supply are more closely organized, with local officials expected to carry out the government’s orders.\n\nIts advocates see the beginning of renewed national strength. The cost of the army, and the power of its officers, will remain matters of public dispute.

**本轮中文**：主张集权的军官终于让自己的办法成为国策。征募、训练和军需被纳入统一调度，地方官员也须执行中央的命令。兵工厂与工具厂为扩充后的军队提供装备，军府由此取得了在各地贯彻政令的力量。

**本轮英文**：The officers have secured the centralized government they sought. Recruitment, training and supplies come under common direction, and local officials must carry out the government’s orders. Arsenals and tool workshops equip the expanded army, giving the military administration the means to enforce its policy in the provinces.

**原因**：原段最后泛论军费/军官权力将长久争议，凭空补反对者与代价收束；完成条件足以陈述实际军政结果。

**来源**：C/common/scripted_triggers/nesnd_jp_politics.txt:26; author flavorCNE.3.d

**实际机制**：Appointed bureaucracy; autocracy/oligarchy; army/building thresholds. Does not invent elections or force different governance law.

### `nesnd_jp_foreign.2.d`

判定：返工 → 编辑提案通过；适用 `C_only`。未接入游戏。

**原AI中文**：使者带回了[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复。对方已经接受我们的提议，双方将依照商定的安排处理此事。

**原AI英文**：Our envoy has returned with the reply from [SCOPE.sCountry('jp_partner').GetNameNoFormatting]. They have accepted our proposal, and the agreed arrangements will govern the matter.

**本轮中文**：使者带回了[SCOPE.sCountry('jp_partner').GetNameNoFormatting]的答复。对方已经接受我们的提议，双方将依照商定的安排处理此事。

**本轮英文**：Our envoy has returned from [SCOPE.sCountry('jp_partner').GetNameNoFormatting] with an agreement. Their government has accepted the proposal.

**原因**：原英文the agreed arrangements will govern the matter是空泛抽象收尾；保留无kind时的中性回退。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Fallback only. Kind-specific variants need saved reply kind before request cleanup.

### `nesnd_jp_foreign.2.d1`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：宗主已同意放宽对本国的约束，原有的宗属关系升为更自主的等级。双方议定休兵五年，政府可以据此着手处理此前受制的事务。

**本轮英文**：Our overlord has agreed to loosen its control, granting us a more autonomous status. The two governments have established a five-year truce.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 1. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_jp_foreign.2.d2`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：[SCOPE.sCountry('jp_partner').GetNameNoFormatting]已经承认本国独立。宗属关系就此解除，双方议定休兵五年；今后的内外事务，将由本国政府自行决定。

**本轮英文**：[SCOPE.sCountry('jp_partner').GetNameNoFormatting] has recognized our independence. The subject relationship is dissolved, and a five-year truce now stands between us. Our government will conduct its own domestic and foreign affairs.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 2. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_jp_foreign.2.d3`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：宗主同意本国推行新政。政府可以开始筹划任官、军政与议政制度的改革，原有的宗属关系仍然保留。

**本轮英文**：Our overlord has given its assent to domestic reform. The government may pursue changes to public appointments, military administration and representation while the subject relationship remains in force.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 3. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_jp_foreign.2.d4`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：[SCOPE.sCountry('jp_partner').GetNameNoFormatting]同意拨给建设资金。工场扩建与工匠训练有了新的助力；政府须善用这笔资助，三年内不能再获同类拨款。

**本轮英文**：[SCOPE.sCountry('jp_partner').GetNameNoFormatting] has provided development funds. The grant will support construction and the training of skilled workers. Further funding of this kind will be unavailable for three years.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 4. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_jp_foreign.2.d5`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：对方接受了朝鲜和解方案。本国对釜山与两湖的宣称已经撤回，两地尚在本国掌握中的领土也已依约移交朝鲜。海峡两岸的关系将依新的边界继续经营。

**本轮英文**：The Korean settlement has been accepted. Our claims to Busan and Yangho have been withdrawn, and any territory we still held there has passed to Korea. Future relations across the strait will proceed within these borders.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 5. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_jp_foreign.2.d7`

判定：返工 → 编辑提案通过；适用 `C_only_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：宗主允许本国与其他日本属国商议合邦。使者可以带着这份许可前去交涉，受邀国家仍须自行同意归并。

**本轮英文**：Our overlord has authorized negotiations for union with the other Japanese subjects. Our envoys may now approach them, though each invited government must still consent to the union.

**原因**：按已发生的结算陈述实际结果，代替所有成功外交共用空泛答复。

**来源**：C/events/nesnd_jp_foreign.txt:29; C/common/scripted_effects/nesnd_jp_foreign.txt:56

**实际机制**：Kind 7. Save kind as event scope value BEFORE nesnd_jp_clear_request; no reply for kind6 annex.

### `nesnd_qe1_ruler_delta`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：秦王的倾向

**原AI英文**：The Sovereign's Preference

**本轮中文**：君主的倾向

**本轮英文**：The Sovereign's Preference

**原因**：秦王是固定王号，与本系统陈秦皇帝和可变国体不一致；本项仅君主路线贡献非零。

**来源**：M/common/scripted_effects/nesnd_qe1_agendas.txt:20

**实际机制**：nesnd_qe1_assign_ruler clears the two preference variables outside monarchy; neutral label avoids false rank.

### `nesnd_qe1.1.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷终于决定把恢复生产与改造旧法置于军府的要求之前。新任官员将凭借工场、学校和商人的支持施展其主张；军士与武勋门阀则退到了朝议的后列。

**原AI英文**：The court has placed economic recovery and legal reform ahead of the army's demands. New officials will draw their support from workshops, schools and merchants. Soldiers and the military nobility must now yield their former prominence in the imperial councils.

**本轮中文**：安国派的主张成为朝廷施政的方向。支持改制的士人与工商业者声望日隆，军府及其市民拥护者则失去了原有的政治优势。恢复生产与改造旧法，将成为新政府争取人心的凭借。

**本轮英文**：The reformers have set the government’s course. Scholars and industrialists who supported reform have gained political influence, while the army and its supporters among the urban middle classes have lost ground. The new government looks to economic recovery and legal reform to win public support.

**原因**：原文“军士与武勋门阀”把实际受损小市民误写成勋贵地主；按armed_forces+petty_bourgeoisie降低、intelligentsia+industrialists增加修正行动者。

**来源**：M/common/static_modifiers/nesnd_qe1_agendas.txt:3; M/common/scripted_effects/nesnd_qe1_agendas.txt:75

**实际机制**：Only IG strength/attraction modifiers and SoL-loyalty observation, no forced office/law change.

### `nesnd_qe1_economy_push_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：削减军府的特权与乡村的旧规，把朝廷的力量投入安国之策。

**原AI英文**：Curb military privilege and the old rural restrictions, and commit the court to economic reform.

**本轮中文**：朝廷力推安国之策，要求军府与乡民团体让步，使恢复生产与改造旧法的主张占据朝议。

**本轮英文**：Press the reform agenda at court, demanding concessions from the military and rural associations so that economic recovery and legal reform take priority.

**原因**：原文削减乡村旧规没交代实际承担者；效果降低军队、乡村民众赞同而非地主，且并不直接删除军队/更改法律。

**来源**：M/common/scripted_buttons/nesnd_qe1_agendas.txt:5; M/common/static_modifiers/nesnd_qe1_agendas.txt:2

**实际机制**：Balance -25; armed forces and rural folk approval -2 for six months. Existing policy/button name retained.

### `nesnd_qe1.2.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：统治派取得了朝廷的信任。军令与征收将更紧密地连在一起，新的官员也更多出自营伍。伊犁的朝议暂时归于一致，代价则由被排除在权力之外的人承担。

**原AI英文**：The military faction has won the confidence of the court. Military command and tax collection will be more closely joined, and more appointments will go to men of the army. Ili has reached an agreement, for now; those excluded from power will bear its cost.

**本轮中文**：统治派取得了朝廷的支持，军府将掌握更多征募、军需与任官事务。此前要求恢复生产、改造旧法的官员未能主导新政府，伊犁已把扩充军队列为国策。

**本轮英文**：The military faction has won the government’s support and will take a greater part in recruitment, supply and appointments. Officials who argued for economic recovery and legal reform have failed to set its course. Ili has made expansion of the army a priority.

**原因**：删除“代价由被排除者承担”的无对象总结；将抽象代价改成议程争夺的实际结果。

**来源**：M/common/scripted_effects/nesnd_qe1_agendas.txt:75; M/common/static_modifiers/nesnd_qe1_agendas.txt

**实际机制**：Military winner flag + ten-year modifier; no claim that laws/appointments are forcibly replaced.

### `nesnd_qe1.3.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝议延续了十年，田地、军饷与官职的争论仍没有结果。地方听过太多振兴帝国的许诺，越来越少的人相信下一道诏令能改变自己的处境。

**原AI英文**：For ten years the court has argued over land, military pay and appointments without reaching a settlement. The provinces have heard promise after promise of imperial renewal. Fewer now believe that another decree will improve their lot.

**本轮中文**：朝议延续了十年，田地、军饷与官职的争论仍没有结果。地方听过太多振兴帝国的许诺，越来越少的人相信下一道法令能改变自己的处境。

**本轮英文**：For ten years the court has argued over land, military pay and appointments without reaching a settlement. The provinces have heard promise after promise of imperial renewal. Fewer now believe that another decree will improve their lot.

**原因**：朝议终局不限定君主制，用法令代替仅君主可发的诏令；保留十年真实计时。

**来源**：M/common/scripted_effects/nesnd_qe1_agendas.txt:94; M/common/scripted_triggers/nesnd_qe1_campaign.txt:2

**实际机制**：Ten-year unresolved agenda; does not require monarch to remain in office.

### `nesnd_qe1_court_journal_reason`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：皇帝凭借旧日征服的威望任命官员，地方士人依靠学堂、商号和官署主持日常政务，军队则掌握了帝国赖以扩张的武力。三者的合作使朝廷得以运转，他们也都希望把其他两方变成自己的助力。

**原AI英文**：The Emperor appoints officials by the authority of past conquests. Provincial scholars conduct the business of government through schools, trading houses and public offices. The army commands the force on which the Empire's expansion depends. All three sustain the court, and each hopes to bend the others to its purposes.

**本轮中文**：皇族以旧日征服的威望维系奉宸官僚，地方士人依靠学堂、商号和官署经营政务，军队则掌握帝国赖以扩张的武力。三方都要借助另外两方治理各地，也都在争取任官、征税和调兵的决定权。

**本轮英文**：The imperial house draws on the prestige of past conquests and the loyalty of officials who owe it their position. Provincial literati work through schools, trading houses and public offices; the army commands the force on which imperial expansion depends. Each faction needs the others to govern, yet each seeks authority over appointments, revenue and military command.

**原因**：三权日志在总统共和+比例代表制下仍有效，原文现在时“皇帝任命”不一定成立；保留皇族政治力量但不虚构在位皇帝。

**来源**：M/common/scripted_triggers/nesnd_qe1_campaign.txt:20; M/common/scripted_buttons/nesnd_qe1_court.txt:6

**实际机制**：Court eligibility excludes universal suffrage/council republic, not presidential republic.

### `nesnd_qe1_unity_journal_reason`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：商路、村社与军屯把许多不同来历的人联结在陈秦皇帝的治下。西域汉羌既是帝国扩张的产物，也为这个国家提供了兵员与税源。人们在繁荣中接受共同的身份，也会在征役与贫困中重新寻找旧日的族名、信仰和乡里。

**原AI英文**：Trade routes, village communities and military colonies bind peoples of many origins to the Chen emperors of Qin. The Western Regions Han-Qiang emerged from imperial expansion and now provide much of the Empire's manpower and revenue. Prosperity encourages a common identity. Conscription and hardship can lead people back to older loyalties of kinship, faith and homeland.

**本轮中文**：商路、村社与军屯曾将许多不同来历的人联结在陈秦皇帝的治下。西域汉羌既是帝国扩张的产物，也为这个国家提供了兵员与税源。人们在繁荣中接受共同的身份，也会在征役与贫困中重新寻找旧日的族名、信仰和乡里。

**本轮英文**：Trade routes, village communities and military colonies brought peoples of many origins under the Chen emperors of Qin. The Western Regions Han-Qiang emerged from that expansion and now provide much of the country’s manpower and revenue. Prosperity encourages a common identity. Conscription and hardship can lead people back to older loyalties of kinship, faith and homeland.

**原因**：常驻团结日志在共和后仍存在；陈秦皇帝统治作为历史保留，不写成无条件现在时。

**来源**：M/common/scripted_triggers/nesnd_qe1_campaign.txt:21

**实际机制**：Historical identity remains relevant under every current Qin government.

### `nesnd_qe1_patron_crown_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：让依靠皇室任命的军士与官员掌握更多职位。

**原AI英文**：Grant more offices to soldiers and administrators whose position depends on imperial appointment.

**本轮中文**：让拥护皇室的军士与官员掌握更多职位。

**本轮英文**：Give more offices to soldiers and administrators loyal to the imperial house.

**原因**：共和分支仍可奖掖皇族势力，不能以现有皇室任命为职位前提。

**来源**：M/common/scripted_buttons/nesnd_qe1_court.txt:1

**实际机制**：Patronage modifier; does not require an actual reigning emperor.

### `nesnd_qe1_coup_literati_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：废除皇位，由民选总统与实行比例代表的议会主持国政。

**原AI英文**：Abolish the throne and establish an elected president and a parliament chosen by proportional representation.

**本轮中文**：改立总统共和，由民选总统与实行比例代表的议会主持国政。

**本轮英文**：Establish a presidential republic with an elected president and a parliament chosen by proportional representation.

**原因**：可从法团国家等非君主国体执行，原文无条件“废除皇位”不适用所有入口。

**来源**：M/common/scripted_buttons/nesnd_qe1_court.txt:6

**实际机制**：Activates presidential republic and custom voting law; no assumption of existing throne.

### `nesnd_qe1_coup_crown_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：保留皇位，把官署交给受过专业训练的技术官僚，以此重建君主的统治。

**原AI英文**：Preserve the throne and entrust the administration to trained technocrats, restoring the monarch's control of government.

**本轮中文**：以君主制与技术官僚重组政府，使皇室重新掌握国家的统治。

**本轮英文**：Reorganize the government as a monarchy administered by trained technocrats, restoring the imperial house to power.

**原因**：按钮可从共和国恢复君主，原文“保留皇位”并非所有分支成立。

**来源**：M/common/scripted_buttons/nesnd_qe1_court.txt:7

**实际机制**：Activates law_monarchy + law_technocracy; not gated to an existing monarchy.

### `law_nesnd_qe1_proportional_representation_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：拥有财产与读写能力的选民选出代表，各政治团体依其支持组成议会与政府。

**原AI英文**：Literate voters with sufficient property elect representatives. Political groups take their seats in parliament and form governments according to their share of support.

**本轮中文**：财产达到门槛的选民取得投票资格，识字程度也影响其选票的政治分量。各政治团体依支持力量组成议会与政府。

**本轮英文**：Property determines eligibility to vote, while literacy increases a voter’s political influence. Political groups form parliament and government according to their support.

**原因**：原文将识字写成独立资格门槛；实际law是wealth threshold10 + voting_power_from_literacy50，文意需区分资格与票权。

**来源**：M/common/laws/nesnd_qe1_laws.txt:10

**实际机制**：Retains custom proportional-representation name; does not claim actual district seat-allocation simulation.

### `nesnd_per_claim_levant_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。

**原AI英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**本轮中文**：向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。

**本轮英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**原因**：地区不能接受照会，外交行动者是有关国家；英文现稿已正确。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:44

**实际机制**：A selected unclaimed foreign-owned state; adds claim only without obstruction.

### `nesnd_per_claim_egypt_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。

**原AI英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**本轮中文**：向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。

**本轮英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**原因**：地区不能接受照会，外交行动者是有关国家；英文现稿已正确。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:44

**实际机制**：A selected unclaimed foreign-owned state; adds claim only without obstruction.

### `nesnd_per_claim_arabia_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。

**原AI英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**本轮中文**：向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。

**本轮英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**原因**：地区不能接受照会，外交行动者是有关国家；英文现稿已正确。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:44

**实际机制**：A selected unclaimed foreign-owned state; adds claim only without obstruction.

### `nesnd_per_claim_central_asia_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。

**原AI英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**本轮中文**：向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。

**本轮英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**原因**：地区不能接受照会，外交行动者是有关国家；英文现稿已正确。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:44

**实际机制**：A selected unclaimed foreign-owned state; adds claim only without obstruction.

### `nesnd_per_claim_india_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：朝廷将向尚未承认我方权利的地区发出照会；相关强国可能出面阻挠。

**原AI英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**本轮中文**：向有关国家递交领土照会，申明我方对当地的主张。与该地区有利害关系的强国可能出面阻挠。

**本轮英文**：Present our territorial claims by diplomatic note. Powers with interests in the region may oppose them.

**原因**：地区不能接受照会，外交行动者是有关国家；英文现稿已正确。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:44

**实际机制**：A selected unclaimed foreign-owned state; adds claim only without obstruction.

### `nesnd_per_claim_india_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：申明印度河流域旧权

**原AI英文**：Assert Our Claims in the Indus Valley

**本轮中文**：申明印度西北诸地的权利

**本轮英文**：Assert Claims in Northwestern India

**原因**：原名“印度河流域”不能涵盖Delhi/Agra/Rajputana/Gujarat；去掉未给出处的“旧权”历史断言。

**来源**：M/common/scripted_triggers/nesnd_per_campaign.txt:34

**实际机制**：Targets Sindh, Punjab, Hill Punjab, Delhi, Agra, Rajputana, Gujarat.

### `nesnd_per.4.d`

判定：返工 → 编辑提案通过；适用 `E_and_C_requires_branch`。未接入游戏。

**原AI中文**：朝廷已经完成面向西方的部署。伊犁能否继续提供援助，仍取决于两国眼下的处境；波斯的军府与商人则已开始议论新的道路和土地。

**原AI英文**：Preparations for expansion to the west are complete. Further aid from Ili will depend on the circumstances of both states. Persian commanders and merchants are already discussing new routes and new lands.

**本轮中文**：本朝与伊犁已经确定朝贡往来，朝廷也将扩张的方向转向西方。军府准备新的远征，商人则打算沿着军队前进的道路寻找市场。

**本轮英文**：Our tributary relationship with Ili is settled, and the government has chosen expansion to the west. Commanders are preparing new campaigns, while merchants seek markets along the routes the army will take.

**原因**：按实际当前仍为QE1属国的成功分支确认朝贡关系，删去关于下一轮援助的空泛预告。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:24; root planned guarded event branch 2026-11-02

**实际机制**：Use only when QE1 exists/alive and PER is currently subject_of QE1; root will branch on actual relationship, not stale route flag.

### `nesnd_per.4.d_unavailable`

判定：返工 → 编辑提案通过；适用 `E_and_C_requires_branch`。未接入游戏。

**原AI中文**：（新增分支）

**原AI英文**：（新增分支）

**本轮中文**：朝廷已经决定向西扩张，原定与伊犁建立的朝贡安排却未能成立。军府与商人仍可经营西方，所需兵力与财源须从眼下能够取得的支持中筹措。

**本轮英文**：The government has chosen expansion to the west, but the proposed tributary arrangement with Ili has not taken effect. Commanders and merchants can still pursue a western policy, drawing on the troops, revenues and support presently available.

**原因**：缺失QE1或受第三国宗主等分支不能虚构签成朝贡或已获援助。

**来源**：M/common/scripted_effects/nesnd_per_campaign.txt:24; root planned guarded event branch 2026-11-02

**实际机制**：Fallback when actual PER->QE1 subject relationship is absent. Future progress/completion unchanged.

### `nesnd_per_future_status_aid`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：使者正在往来，朝廷准备借秦国的力量经营西方。

**原AI英文**：Envoys are seeking Qin support for expansion in the west.

**本轮中文**：朝廷已选定求援伊犁、向西经营的方针。

**本轮英文**：The government has chosen to seek support from Ili for expansion to the west.

**原因**：状态只检查route_aid，不保证援助方仍存在或使者正在往来；陈述已选方针而非当前实存援助。

**来源**：M/common/journal_entries/nesnd_per_campaign.txt:21; M/common/scripted_triggers/nesnd_per_campaign.txt:5

**实际机制**：Route choice persists if aid becomes unavailable; progress intentionally continues.

### `modifier_state_nesnd_qe1_conversion_cohort_standard_of_living_add_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：对西域汉羌人口的影响。

**原AI英文**：The effect on the Standard of Living of Western Regions Han-Qiang Pops.

**本轮中文**：对西域汉羌人口生活水平的影响。

**本轮英文**：The effect on the Standard of Living of Western Regions Han-Qiang Pops.

**原因**：现有中文三项均泛写“人口的影响”，补齐实际量。

**来源**：M/common/modifier_type_definitions/nesnd_qe1_cohort.txt

**实际机制**：Labels only; English already identifies the correct quantity.

### `modifier_country_nesnd_qe1_conversion_cohort_cultural_acceptance_add_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：对西域汉羌人口的影响。

**原AI英文**：The effect on the Cultural Acceptance of Western Regions Han-Qiang Pops.

**本轮中文**：对西域汉羌人口文化接纳的影响。

**本轮英文**：The effect on the Cultural Acceptance of Western Regions Han-Qiang Pops.

**原因**：现有中文三项均泛写“人口的影响”，补齐实际量。

**来源**：M/common/modifier_type_definitions/nesnd_qe1_cohort.txt

**实际机制**：Labels only; English already identifies the correct quantity.

### `modifier_country_fervor_target_nesnd_qe1_conversion_cohort_add_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：对西域汉羌人口的影响。

**原AI英文**：The effect on the Cultural Fervor of Western Regions Han-Qiang Pops.

**本轮中文**：对西域汉羌人口文化热情的影响。

**本轮英文**：The effect on the Cultural Fervor of Western Regions Han-Qiang Pops.

**原因**：现有中文三项均泛写“人口的影响”，补齐实际量。

**来源**：M/common/modifier_type_definitions/nesnd_qe1_cohort.txt

**实际机制**：Labels only; English already identifies the correct quantity.

### `nesnd_phi_service_recovery`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋驻屯经费

**原AI英文**：吕宋驻屯经费

**本轮中文**：吕宋驻屯经费

**本轮英文**：Funding the Luzon Garrison

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_service_recovery_reason`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：楚军南渡之后，吕宋的营垒里又添了许多湖广乡音。随林则徐出海的将士在此领饷、操练，把故乡的消息夹在家书里传回军中。宣慰司的船队往来海上，税粮与军饷也一道经过马尼拉的库房。\n\n驻屯军的开销逐年列在吕宋账下，朝廷征调的海船仍须备齐官兵。宣慰司将营册与税册并排呈送，要求重新议定驻屯、海防和岁贡。

**原AI英文**：楚军南渡之后，吕宋的营垒里又添了许多湖广乡音。随林则徐出海的将士在此领饷、操练，把故乡的消息夹在家书里传回军中。宣慰司的船队往来海上，税粮与军饷也一道经过马尼拉的库房。\n\n驻屯军的开销逐年列在吕宋账下，朝廷征调的海船仍须备齐官兵。宣慰司将营册与税册并排呈送，要求重新议定驻屯、海防和岁贡。

**本轮中文**：楚军南渡之后，吕宋的营垒里又添了许多湖广乡音。随林则徐出海的将士在此领饷、操练，把故乡的消息夹在家书里传回军中。群岛要供养这些驻军，也须为朝廷的远洋征调备齐舰船与水手。\n\n宣慰司请求重新商议驻屯军费、海防和岁贡。当地收入须同时维持军队与百姓的生计，中央承担多少，吕宋留下多少，将决定这支海外军队能够长久驻守的根基。

**本轮英文**：The soldiers who sailed south with Lin Zexu brought the voices of Huguang to Luzon’s garrisons. Their pay, provisions and training now depend on the islands, while the administration must also keep ships ready for imperial service.\n\nThe cost of these obligations has become a question for both governments. Luzon seeks a new settlement of garrison expenses, naval service and tribute, so that its revenues can support the troops as well as the people who sustain them.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_external`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：现有宗属、共同市场或双方和平条件已改变。原协议停止续付；按本国现有收入、军事义务与外交安排重订经费。

**原AI英文**：现有宗属、共同市场或双方和平条件已改变。原协议停止续付；按本国现有收入、军事义务与外交安排重订经费。

**本轮中文**：宗属、共同市场或两国间的和平已经改变，原定补贴停止续付。今后的军费须依当前收入与军事义务重新商定。

**本轮英文**：The subject relationship, shared market or peace between the two countries has changed. Payments under the agreement will cease. A new settlement must reflect our present income and obligations.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_stalled`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：付款方当前未能履行钱款条约。检查条约冻结与其[concept_default]情况；账面约定金额不计作已收到的收入。

**原AI英文**：付款方当前未能履行钱款条约。检查条约冻结与其[concept_default]情况；账面约定金额不计作已收到的收入。

**本轮中文**：议定的拨款尚未到账。付款国可能陷入[concept_default]，条约也可能暂停履行；驻屯经费暂须依靠已经收到的收入。

**本轮英文**：The paying country is unable to meet its obligations. The treaty may be suspended or the country in [concept_default]. Promised payments count as income only when received.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_pending`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：议案正在两国间审议，120天内须由双方确认。尚未拨款或移交舰船，吕宋继续按现有财政运作。

**原AI英文**：议案正在两国间审议，120天内须由双方确认。尚未拨款或移交舰船，吕宋继续按现有财政运作。

**本轮中文**：两国须在120天内确认议案。签署之前，钱款与舰船仍由原有政府掌管。

**本轮英文**：Both governments must approve the proposal within 120 days. Until then, no money or ships change hands.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_active`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：协定正在履行。按每月实际收支、驻军、舰员与居民生计检验恢复；本次钱款协定在签订12个月后结束。

**原AI英文**：协定正在履行。按每月实际收支、驻军、舰员与居民生计检验恢复；本次钱款协定在签订12个月后结束。

**本轮中文**：协定正在履行，钱款将在签订12个月后终止。驻军、舰员与居民的生计仍须由现有收入维持。

**本轮英文**：The agreement is in force. The subsidy ends 12 months after signature; garrison strength, naval staffing and local livelihoods must remain sustainable.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_review`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：钱款协定已经结束。以现有收入和义务维持三个月；需要续议时，重新取得两国同意。

**原AI英文**：钱款协定已经结束。以现有收入和义务维持三个月；需要续议时，重新取得两国同意。

**本轮中文**：补贴已经结束。军费、驻军与民生须再维持三个月；若需续款，仍须取得两国同意。

**本轮英文**：The subsidy has ended. Sustain the required finances, forces and livelihoods for three months. Renewed payments require the consent of both governments.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_status_proposal`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：可请求中央承担驻屯军费，或议定舰队分任。先检查宗属与条约资格，再提出正式议案。

**原AI英文**：可请求中央承担驻屯军费，或议定舰队分任。先检查宗属与条约资格，再提出正式议案。

**本轮中文**：可请求中央分担驻屯军费，或商议分任舰队与地方海防。

**本轮英文**：Request central funding for the garrison, or negotiate a division of naval responsibilities.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_service_bar`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：军民经费

**原AI英文**：军民经费

**本轮中文**：军民经费

**本轮英文**：Garrison Finances and Livelihoods

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_service_bar_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 4#!

**原AI英文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 4#!

**本轮中文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 4#!

**本轮英文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 4#!

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_service_bar_detail`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：当前非建设周结余：#v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\n舰队实际满员需求：#v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\n无业劳动力：#v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\n\n四项各计一格：非建设收支非负、未[concept_default]或[concept_bankruptcy]且现行拨款确在履行；常备军至少#v 35营#!；驻屯协定至少#v 40舰#!、海防分任至少#v 20舰#!各有#v 75%#!船员，海军维护履行至少#v 80%#!；无业不超过#v 12%#!且欠食不超过#v 15%#!。每月更新。

**原AI英文**：当前非建设周结余：#v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\n舰队实际满员需求：#v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\n无业劳动力：#v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\n\n四项各计一格：非建设收支非负、未[concept_default]或[concept_bankruptcy]且现行拨款确在履行；常备军至少#v 35营#!；驻屯协定至少#v 40舰#!、海防分任至少#v 20舰#!各有#v 75%#!船员，海军维护履行至少#v 80%#!；无业不超过#v 12%#!且欠食不超过#v 15%#!。每月更新。

**本轮中文**：非建设周结余：#v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\n舰队满员所需水手：#v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\n无业劳动力：#v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\n\n四项各计一格：非建设收支非负，未陷入[concept_default]或[concept_bankruptcy]，且议定的补贴正在支付；常备军至少#v 35营#!；驻屯协定至少#v 40舰#!、海防分任至少#v 20舰#!各有#v 75%#!水手，海军维护履行至少#v 80%#!；无业至多#v 12%#!，欠食至多#v 15%#!。每月更新。

**本轮英文**：Weekly balance excluding construction: #v £[Country.MakeScope.Var('nesnd_phi_budget').GetValue|0]#!\nCrew required for a fully staffed fleet: #v [Country.MakeScope.Var('nesnd_phi_needed_crew').GetValue|0]#!\nUnemployed workforce: #v [Country.MakeScope.Var('nesnd_phi_unemployment').GetValue|%1]#!\nWorkforce below the starvation threshold: #v [Country.MakeScope.Var('nesnd_phi_starving').GetValue|%1]#!\n\nEach requirement fills one segment: a nonnegative balance excluding construction, no [concept_default] or [concept_bankruptcy], and any agreed subsidy actually being paid; at least #v 35 battalions#! in the standing army; at least #v 40 ships#! under the garrison agreement or #v 20 ships#! under the naval division, with #v 75%#! of crews and at least #v 80%#! naval maintenance fulfillment; unemployment at most #v 12%#! and no more than #v 15%#! of the workforce below the starvation threshold. Updated monthly.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_continuity_bar`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：经费巩固

**原AI英文**：经费巩固

**本轮中文**：经费巩固

**本轮英文**：Financial Stability

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_continuity_bar_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 3个月#!

**原AI英文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 3个月#!

**本轮中文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 3个月#!

**本轮英文**：#v [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|0] / 3 months#!

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_continuity_bar_detail`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：和平期间四项军民经费条件持续达标，每月增加#p 1#!，中断后归零。钱款终止时重新计算；终止后三个月达标才完成日志。完成不额外增加建筑、军队或财政收入。

**原AI英文**：和平期间四项军民经费条件持续达标，每月增加#p 1#!，中断后归零。钱款终止时重新计算；终止后三个月达标才完成日志。完成不额外增加建筑、军队或财政收入。

**本轮中文**：和平期间，四项军民经费条件持续达标，每月增加#p 1#!；中断后归零。钱款终止时重新计算，终止后三个月达标才完成日志。

**本轮英文**：Gain #p 1#! each month at peace with all four requirements met. A failure resets the count. The count also resets when the subsidy ends; three successful months after that are required to complete the Journal Entry.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_a_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：议定驻屯军费

**原AI英文**：议定驻屯军费

**本轮中文**：议定驻屯军费

**本轮英文**：Negotiate Garrison Funding

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_a_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：凭已签署且与吕宋、中央当前立场一致的拥明或拥吴盟书，请中央承担海外驻屯。中央须再次同意支出，吕宋最后确认。\n\n$nesnd_phi_route_1_terms_tt$

**原AI英文**：凭已签署且与吕宋、中央当前立场一致的拥明或拥吴盟书，请中央承担海外驻屯。中央须再次同意支出，吕宋最后确认。\n\n$nesnd_phi_route_1_terms_tt$

**本轮中文**：依据双方已经确认且仍然一致的拥明或拥吴承诺，请中央分担海外驻屯军费。中央同意支出后，再由吕宋最后确认。\n\n$nesnd_phi_route_1_terms_tt$

**本轮英文**：Use the confirmed commitment to Ming or Wu, which must match both governments’ present allegiances, to seek central funding for the overseas garrison. The central government must approve the expense before Luzon gives final consent.\n\n$nesnd_phi_route_1_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_b_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：议定海防分任

**原AI英文**：议定海防分任

**本轮中文**：议定海防分任

**本轮英文**：Divide Naval Responsibilities

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_b_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：提出分任远洋舰队与地方海防，保留吕宋西府驻屯大营。此议案不改变政治立场。\n\n$nesnd_phi_route_2_terms_tt$

**原AI英文**：提出分任远洋舰队与地方海防，保留吕宋西府驻屯大营。此议案不改变政治立场。\n\n$nesnd_phi_route_2_terms_tt$

**本轮中文**：议定远洋舰队与群岛海防的分工，保留西府驻屯大营。此次交涉不改变两国的政治立场。\n\n$nesnd_phi_route_2_terms_tt$

**本轮英文**：Propose a division between the ocean-going fleet and the defence of the islands, retaining the Western Administration’s garrison in Luzon. The agreement does not change either government’s political allegiance.\n\n$nesnd_phi_route_2_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_cancel_request_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：撤回议案

**原AI英文**：撤回议案

**本轮中文**：撤回议案

**本轮英文**：Withdraw the Proposal

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_cancel_request_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：结束尚未履行的议案，30天后可重提。已签署的其他外交安排不受影响。

**原AI英文**：结束尚未履行的议案，30天后可重提。已签署的其他外交安排不受影响。

**本轮中文**：撤回尚未签成的议案，30天后可重提。已有外交协定仍然有效。

**本轮英文**：Withdraw the unsigned proposal. Another may be submitted after 30 days. Existing diplomatic agreements remain in force.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_withdraw_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：提前终止钱款协定

**原AI英文**：提前终止钱款协定

**本轮中文**：提前终止钱款协定

**本轮英文**：End the Subsidy Early

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_withdraw_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：由吕宋撤回本日志签订的钱款条约，依原生条约计算约束期内违约的恶名和关系损失。减贡、免役与其他条约照常依原生外交规则存续。移交过的舰船仍归中央。

**原AI英文**：由吕宋撤回本日志签订的钱款条约，依原生条约计算约束期内违约的恶名和关系损失。减贡、免役与其他条约照常依原生外交规则存续。移交过的舰船仍归中央。

**本轮中文**：由吕宋提前退出议定的补贴条约。约束期内退出将招致条约规定的恶名与关系损失；减贡、免役及其他条约仍依各自条款履行，已经移交的舰船仍归中央。

**本轮英文**：Withdraw from the subsidy treaty negotiated here. Leaving during its binding period incurs the treaty’s Infamy and relations penalties. Tribute reductions, exemption from military service and other treaties retain their own terms. Ships already transferred remain with the central government.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_route_1_terms_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：中央每周向吕宋转付#v £8,000#!，期限#v 12个月#!；原生减贡协议降低#v 10个百分点#!的收入转移比例。保留舰队与驻军。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，且原生钱款条约与减贡合法可签。钱款到期主动撤回，减贡按原生外交规则继续。

**原AI英文**：中央每周向吕宋转付#v £8,000#!，期限#v 12个月#!；原生减贡协议降低#v 10个百分点#!的收入转移比例。保留舰队与驻军。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，且原生钱款条约与减贡合法可签。钱款到期主动撤回，减贡按原生外交规则继续。

**本轮中文**：中央每周向吕宋支付#v £8,000#!，持续#v 12个月#!；另以减贡协定将收入转移比例降低#v 10个百分点#!。吕宋保留舰队与驻军。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，并具备签署两项协定的资格。补贴条约于一年后撤回，减贡协定仍依自身条款履行。

**本轮英文**：The central government pays Luzon #v £8,000#! a week for #v 12 months#!. A separate treaty reduces the share of income paid in tribute by #v 10 percentage points#!. Luzon retains its fleet and garrison. The central government needs at least #v £10,000#! in weekly surplus excluding construction, #v £100,000#! in reserves, and eligibility for both treaties. The subsidy treaty is withdrawn at the end of the year; the tribute reduction retains its own terms.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_route_2_terms_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：首次签订时将吕宋实际拥有且未参战的#v 20艘战列舰#!移交中央，保留#v 20艘护卫舰#!与驻屯军。中央每周转付#v £3,000#!，期限#v 12个月#!，并签原生减贡与免役协议。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签钱款不重复转舰；钱款到期终止，减贡、免役按原生外交规则继续。

**原AI英文**：首次签订时将吕宋实际拥有且未参战的#v 20艘战列舰#!移交中央，保留#v 20艘护卫舰#!与驻屯军。中央每周转付#v £3,000#!，期限#v 12个月#!，并签原生减贡与免役协议。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签钱款不重复转舰；钱款到期终止，减贡、免役按原生外交规则继续。

**本轮中文**：首次签订时，吕宋向中央移交所持且未参战的#v 20艘战列舰#!，保留#v 20艘护卫舰#!与驻屯军。中央每周支付#v £3,000#!，持续#v 12个月#!，并另行签署减贡与免役协定。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不再交舰；一年后补贴结束，减贡与免役仍依各自条款履行。

**本轮英文**：On the first agreement, Luzon transfers #v 20 ships of the line#! that it owns and that are not engaged in war. It retains #v 20 frigates#! and the garrison. The central government pays #v £3,000#! weekly for #v 12 months#!, and concludes separate treaties for reduced tribute and exemption from military service. It needs at least #v £5,000#! in weekly surplus excluding construction and #v £60,000#! in reserves. Renewals do not transfer more ships. The subsidy ends after a year; the other agreements retain their own terms.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_usm_accept_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将核准的条款交回吕宋作最后确认。确认前再次核对条约、财政、宗属和舰队条件；此刻不支付补贴、不转移舰船。

**原AI英文**：将核准的条款交回吕宋作最后确认。确认前再次核对条约、财政、宗属和舰队条件；此刻不支付补贴、不转移舰船。

**本轮中文**：把核准的条款交回吕宋，待其最后确认。届时两国的签约资格、财力、宗属与舰队仍须符合议案条件，之后才支付补贴、交接舰船。

**本轮英文**：Return the approved terms to Luzon for final consent. Treaty eligibility, finances, the subject relationship and the fleet must still meet the requirements. No subsidy is paid and no ships are transferred yet.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_reject_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：退回议案，90天后可再提。

**原AI英文**：退回议案，90天后可再提。

**本轮中文**：退回议案，90天后可再提。

**本轮英文**：Return the proposal. Another may be submitted after 90 days.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_defer_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：本次不签约，30天后可再议。

**原AI英文**：本次不签约，30天后可再议。

**本轮中文**：本次不签约，30天后可再议。

**本轮英文**：Do not sign this agreement. Negotiations may resume after 30 days.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.reject`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：此项开支暂不核拨。

**原AI英文**：此项开支暂不核拨。

**本轮中文**：此项开支暂不核拨。

**本轮英文**：We cannot authorize this expense.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.defer`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：退回重议。

**原AI英文**：退回重议。

**本轮中文**：退回重议。

**本轮英文**：Return it for further negotiation.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.cancel`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：暂缓签署。

**原AI英文**：暂缓签署。

**本轮中文**：暂缓签署。

**本轮英文**：Withhold our signature.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.1.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋军饷

**原AI英文**：吕宋军饷

**本轮中文**：吕宋军饷

**本轮英文**：Paying the Luzon Garrison

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.1.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋送来的奏牍附着两本册子，一本记税粮，一本记军饷。宣慰司在末页列明驻屯大营与海船各项开销，请朝廷按年拨款，并减去一部分岁贡。\n\n“将士远戍海疆，营中一日不可缺饷。请先定经制，再议久远。”\n\n库曹依此开列每周#v £8,000#!的军费，支给一年，另议减贡。

**原AI英文**：吕宋送来的奏牍附着两本册子，一本记税粮，一本记军饷。宣慰司在末页列明驻屯大营与海船各项开销，请朝廷按年拨款，并减去一部分岁贡。\n\n“将士远戍海疆，营中一日不可缺饷。请先定经制，再议久远。”\n\n库曹依此开列每周#v £8,000#!的军费，支给一年，另议减贡。

**本轮中文**：吕宋请求中央分担驻屯军与远洋舰队的开销。宣慰司认为，这些兵船听候朝廷征调，其军饷和日常供给也不宜长久只靠群岛的收入维持。\n\n议案请中央每周拨给#v £8,000#!，支给一年，并另行减贡。是否承接这笔开支，须由中央议定。

**本轮英文**：Luzon asks the central government to share the cost of the troops and ships maintained on the islands. Its administration argues that overseas service cannot depend indefinitely on local revenue alone.\n\nThe proposal provides #v £8,000#! a week for one year, alongside a reduction in tribute. It now falls to the central government to decide whether to undertake these obligations.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.1.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：准此军费，交吕宋核议。

**原AI英文**：准此军费，交吕宋核议。

**本轮中文**：准此军费，交吕宋核议。

**本轮英文**：Approve the funding and seek Luzon’s consent.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.2.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：海船归属

**原AI英文**：海船归属

**本轮中文**：海船归属

**本轮英文**：A Division of the Fleet

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.2.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋的海防册另附了一份交舰清单：二十艘战列舰可由中央接管，护卫舰留守群岛，驻屯大营照旧编练。朝廷受领舰船之后，远洋征调与军费也须另立章程。\n\n议案请免吕宋从征，减其岁贡，以每周#v £3,000#!支给一年的整顿费用。中央海军将为受领的战列舰安排驻地、船员与日常供给。

**原AI英文**：吕宋的海防册另附了一份交舰清单：二十艘战列舰可由中央接管，护卫舰留守群岛，驻屯大营照旧编练。朝廷受领舰船之后，远洋征调与军费也须另立章程。\n\n议案请免吕宋从征，减其岁贡，以每周#v £3,000#!支给一年的整顿费用。中央海军将为受领的战列舰安排驻地、船员与日常供给。

**本轮中文**：吕宋提议将二十艘战列舰交由中央海军，护卫舰留下守备群岛，驻屯大营仍归宣慰司。中央接管这些海船，也须承担它们的驻地、船员与日常供给。\n\n为此，吕宋请求免除从征义务，减轻岁贡，并由中央每周支付#v £3,000#!，支给一年，以备海防整顿。

**本轮英文**：Luzon proposes to transfer twenty ships of the line to the central navy. The frigates would remain to defend the islands, as would the garrison. Taking over the ships would also make the central government responsible for their crews, bases and supplies.\n\nIn return, Luzon seeks exemption from military service, reduced tribute and #v £3,000#! a week for one year to support the reorganization.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.2.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：按此分任海防。

**原AI英文**：按此分任海防。

**本轮中文**：按此分任海防。

**本轮英文**：Agree to this division of responsibilities.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.3.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：核拨文书

**原AI英文**：核拨文书

**本轮中文**：核拨文书

**本轮英文**：The Funding Offer

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.3.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：核拨军费的文书到了马尼拉。军需官按月重排支用，缺额的水手、营中口粮和船厂费用逐项登记。\n\n印信尚待钤下。此后一年，中央须按周付给吕宋#v £8,000#!，减贡另依新议；驻屯大营与舰队继续由宣慰司维持。

**原AI英文**：核拨军费的文书到了马尼拉。军需官按月重排支用，缺额的水手、营中口粮和船厂费用逐项登记。\n\n印信尚待钤下。此后一年，中央须按周付给吕宋#v £8,000#!，减贡另依新议；驻屯大营与舰队继续由宣慰司维持。

**本轮中文**：中央已经核准吕宋的请求，愿意每周拨给#v £8,000#!，支给一年，减贡则另依新议。驻屯大营与舰队仍由吕宋维持。\n\n宣慰司还须最后确认，钱款才能开始支付。

**本轮英文**：The central government has approved Luzon’s request. It offers #v £8,000#! a week for one year, with reduced tribute under a separate agreement. The fleet and garrison would remain Luzon’s responsibility.\n\nThe administration in Manila must now give its consent before the payments can begin.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.3.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：钤印，依约支用。

**原AI英文**：钤印，依约支用。

**本轮中文**：钤印，依约支用。

**本轮英文**：Sign the agreement.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.4.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：交舰议定

**原AI英文**：交舰议定

**本轮中文**：交舰议定

**本轮英文**：The Naval Agreement

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.4.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：中央的批复抵达之后，海军衙门将战列舰的名册、船籍与修理记录一并备齐。留守群岛的护卫舰仍归吕宋调遣，西府驻屯大营的营册也留在宣慰司。\n\n此次签押将确定舰队分任、减贡和免役。整顿款按周支付#v £3,000#!，支给一年；已经办过交舰的续议沿用旧册。

**原AI英文**：中央的批复抵达之后，海军衙门将战列舰的名册、船籍与修理记录一并备齐。留守群岛的护卫舰仍归吕宋调遣，西府驻屯大营的营册也留在宣慰司。\n\n此次签押将确定舰队分任、减贡和免役。整顿款按周支付#v £3,000#!，支给一年；已经办过交舰的续议沿用旧册。

**本轮中文**：中央已经同意分任海防。护卫舰将守备群岛，西府驻屯大营仍留吕宋。\n\n宣慰司此次签署，将确认交舰、减贡与免役的安排，以及每周#v £3,000#!、支给一年的补贴。续签时沿用已经交舰的结果，不再另交舰船。

**本轮英文**：The central government has accepted the proposed division of naval duties. The frigates will defend the islands, and the Western Administration’s garrison will remain in Luzon.\n\nLuzon’s signature will confirm the ship transfer, reduced tribute and exemption from service, together with #v £3,000#! in weekly payments for one year. A renewal will retain the previous transfer without requiring further ships.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.4.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：签押，照册办理。

**原AI英文**：签押，照册办理。

**本轮中文**：签押，照册办理。

**本轮英文**：Sign and carry out the transfer.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.5.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支用新章

**原AI英文**：支用新章

**本轮中文**：支用新章

**本轮英文**：A Settlement of Expenses

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.5.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：两地官署各存了一份签押文书。库曹将新议的拨款列入常支，宣慰司也把营饷、船员与税粮重新分册。\n\n下一次呈报，须连同实际收支与各营缺额一并送来。

**原AI英文**：两地官署各存了一份签押文书。库曹将新议的拨款列入常支，宣慰司也把营饷、船员与税粮重新分册。\n\n下一次呈报，须连同实际收支与各营缺额一并送来。

**本轮中文**：两国已经签署协定。中央须按约支付钱款，吕宋则须统筹驻军、舰队与地方民生的开支。\n\n这一年的援助能否让群岛在款项结束后维持自己的军政，还要看现有收入能够承担多少义务。

**本轮英文**：Both governments have signed. The central treasury must now make the agreed payments, while Luzon’s administration must use its revenues to support the garrison, the fleet and the islands’ civilian needs.\n\nThe coming year will show whether these obligations can be maintained after the temporary subsidy ends.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.5.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：按月查核。

**原AI英文**：按月查核。

**本轮中文**：按月查核。

**本轮英文**：Put the agreement into effect.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.6.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：一年军费

**原AI英文**：一年军费

**本轮中文**：一年军费

**本轮英文**：A Year of Funding

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.6.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：一年的军费支用期已满，钱款条约依议终止。吕宋官署把本年账册送交中央，请核阅驻军与舰队的现况。\n\n新一年的经费须另行商定。既有宗属与军事义务依现行约定办理。

**原AI英文**：一年的军费支用期已满，钱款条约依议终止。吕宋官署把本年账册送交中央，请核阅驻军与舰队的现况。\n\n新一年的经费须另行商定。既有宗属与军事义务依现行约定办理。

**本轮中文**：一年的拨款已经付完，补贴条约依约终止。吕宋须以现有收入维持所留军队，或再向中央商议援助。其他军事与外交义务，仍按当前宗属关系及各项条约办理。

**本轮英文**：The year of payments is over, and the subsidy treaty has ended as agreed. Luzon must now support its remaining forces from current revenues or negotiate fresh assistance. Its other obligations remain governed by the existing subject relationship and treaties.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.6.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：重核来岁经费。

**原AI英文**：重核来岁经费。

**本轮中文**：重核来岁经费。

**本轮英文**：Settle the coming year’s expenses.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.7.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：军费中止

**原AI英文**：军费中止

**本轮中文**：军费中止

**本轮英文**：Funding Interrupted

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.7.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：钱款条约已不能按原议继续。宣慰司将未结账目另列一册，通知营伍与海军官署重新编排支出。\n\n下一份经费方案，将依现有宗属、市场与军事义务商议。

**原AI英文**：钱款条约已不能按原议继续。宣慰司将未结账目另列一册，通知营伍与海军官署重新编排支出。\n\n下一份经费方案，将依现有宗属、市场与军事义务商议。

**本轮中文**：中央已不能按原议继续拨款。吕宋的军需与海军官员须重新安排开支，下一份军费协定也须依当前宗属、市场与军事义务商定。

**本轮英文**：The subsidy can no longer continue on the agreed terms. Luzon’s military and naval authorities must revise their spending. Any new agreement will have to reflect the present subject relationship, market arrangements and military obligations.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.7.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：查明账目，另议支用。

**原AI英文**：查明账目，另议支用。

**本轮中文**：查明账目，另议支用。

**本轮英文**：Reconsider the budget.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.8.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：营饷有经

**原AI英文**：营饷有经

**本轮中文**：营饷有经

**本轮英文**：The Garrison Sustained

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.8.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：钱款支用期结束之后，吕宋接连三个月的账目已经报齐。军营照常发饷，海船补入了水手，宣慰司也终于可以按实际收入编定下一季开支。\n\n核销过的营册已经封存，库曹另留副本。往后的军费审议，便从这些有据可查的账目开始。

**原AI英文**：钱款支用期结束之后，吕宋接连三个月的账目已经报齐。军营照常发饷，海船补入了水手，宣慰司也终于可以按实际收入编定下一季开支。\n\n核销过的营册已经封存，库曹另留副本。往后的军费审议，便从这些有据可查的账目开始。

**本轮中文**：钱款支用期结束后，吕宋已连续三个月维持军民经费。驻屯大营仍能受领军需，海船已有足够水手，地方居民的生计也达到了此前议定的条件。宣慰司可以依实际收入安排下一季开支。

**本轮英文**：For three months after the subsidy ended, Luzon has maintained its finances, forces and civilian livelihoods. The garrison remains supplied and the fleet has the crews it needs. The administration can plan its next season of spending from revenues it actually receives.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.8.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：照章续办。

**原AI英文**：照章续办。

**本轮中文**：照章续办。

**本轮英文**：Maintain this settlement.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.10.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：另订的条款

**原AI英文**：另订的条款

**本轮中文**：另订的条款

**本轮英文**：Revised Terms

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.10.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：两国已通过外交程序改订了原条约，所列条款与旧军费协定不同。宣慰司将新约另行存档，往后依新约办理。\n\n新约的付款期限与其余条款，应在外交界面重新查核。

**原AI英文**：两国已通过外交程序改订了原条约，所列条款与旧军费协定不同。宣慰司将新约另行存档，往后依新约办理。\n\n新约的付款期限与其余条款，应在外交界面重新查核。

**本轮中文**：两国已经通过外交交涉改订条约，其条款与此前军费协定不同。吕宋今后依新约办理，付款期限与其余义务可在外交界面查看。

**本轮英文**：The two governments have amended the treaty through diplomatic negotiations. Its terms now differ from the earlier military funding agreement. Luzon’s administration will follow the revised treaty; its payment schedule and other obligations can be reviewed in the diplomacy panel.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.10.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：依新约办理。

**原AI英文**：依新约办理。

**本轮中文**：依新约办理。

**本轮英文**：Observe the revised agreement.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_cash_a_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：驻屯岁费（定额）

**原AI英文**：驻屯岁费（定额）

**本轮中文**：驻屯岁费（定额）

**本轮英文**：Negotiate a Fixed Garrison Subsidy

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_cash_a_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：按驻屯大营与远洋舰队的支出，议定中央每周承担的岁费。须先有双方立场一致的正式拥明或拥吴盟书。\n\n$nesnd_phi_cash_1_terms_tt$

**原AI英文**：按驻屯大营与远洋舰队的支出，议定中央每周承担的岁费。须先有双方立场一致的正式拥明或拥吴盟书。\n\n$nesnd_phi_cash_1_terms_tt$

**本轮中文**：依据双方已经确认且仍然一致的拥明或拥吴承诺，商议中央每周分担的驻屯与远洋海防经费。\n\n$nesnd_phi_cash_1_terms_tt$

**本轮英文**：Agree on a weekly contribution from the central government towards the garrison and ocean-going fleet. A confirmed commitment to Ming or Wu must match both governments’ present allegiances.\n\n$nesnd_phi_cash_1_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_cash_b_button`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：海防分任（定额）

**原AI英文**：海防分任（定额）

**本轮中文**：海防分任（定额）

**本轮英文**：Divide Naval Duties with Fixed Funding

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_request_cash_b_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：由中央接管战列舰，吕宋留护卫舰守备群岛；驻屯大营照旧编练，分任之后另订定额经费。此协议不改变拥明、拥吴、中立或自主立场。\n\n$nesnd_phi_cash_2_terms_tt$

**原AI英文**：由中央接管战列舰，吕宋留护卫舰守备群岛；驻屯大营照旧编练，分任之后另订定额经费。此协议不改变拥明、拥吴、中立或自主立场。\n\n$nesnd_phi_cash_2_terms_tt$

**本轮中文**：中央接管战列舰，吕宋留护卫舰守备群岛，驻屯大营照旧编练，再议定分任后的军费。协议不改变拥明、拥吴、中立或自主立场。\n\n$nesnd_phi_cash_2_terms_tt$

**本轮英文**：Transfer the ships of the line to the central government, retaining frigates to defend the islands and the existing garrison. Negotiate fixed funding for the new arrangement. This agreement does not change allegiance to Ming or Wu, neutrality or independence.\n\n$nesnd_phi_cash_2_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_cash_1_terms_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：中央每周向吕宋支付#v £8,700#!，持续#v 12个月#!。保留驻屯军与舰队，属国贡赋按现有宗属关系另计；本协定不降低贡率或附加独立倾向效果。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，且原生钱款条约可签。两国先后确认后才开始付款；期满终止本笔钱款。

**原AI英文**：中央每周向吕宋支付#v £8,700#!，持续#v 12个月#!。保留驻屯军与舰队，属国贡赋按现有宗属关系另计；本协定不降低贡率或附加独立倾向效果。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，且原生钱款条约可签。两国先后确认后才开始付款；期满终止本笔钱款。

**本轮中文**：中央每周向吕宋支付#v £8,700#!，持续#v 12个月#!。吕宋保留驻屯军与舰队，贡赋仍依现有宗属关系支付；此约不改贡率与独立倾向。中央须有至少#v £10,000#!非建设周结余、#v £100,000#!储备，并具备签约资格。两国确认后开始付款，一年后结束。

**本轮英文**：The central government pays Luzon #v £8,700#! weekly for #v 12 months#!. Luzon retains its garrison and fleet. Tribute continues under the existing subject relationship; this agreement neither reduces the tribute rate nor changes Liberty Desire. The central government needs at least #v £10,000#! in weekly surplus excluding construction, #v £100,000#! in reserves, and eligibility for the subsidy treaty. Payments begin only after both governments consent and end after the agreed year.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_cash_2_terms_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：首次签订时向中央移交实际#v 20艘战列舰#!，吕宋保留#v 20艘护卫舰#!和驻屯军；原生免役资格通过后免除军事服务。中央每周支付#v £3,700#!，持续#v 12个月#!。属国贡赋按现有关系另计，本协定不降低贡率；中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不重复交舰，期满只终止本笔钱款。

**原AI英文**：首次签订时向中央移交实际#v 20艘战列舰#!，吕宋保留#v 20艘护卫舰#!和驻屯军；原生免役资格通过后免除军事服务。中央每周支付#v £3,700#!，持续#v 12个月#!。属国贡赋按现有关系另计，本协定不降低贡率；中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不重复交舰，期满只终止本笔钱款。

**本轮中文**：首次签订时向中央移交#v 20艘战列舰#!，吕宋保留#v 20艘护卫舰#!与驻屯军；符合资格后免除军事服务。中央每周支付#v £3,700#!，持续#v 12个月#!。贡赋仍按原有比例支付。中央须有至少#v £5,000#!非建设周结余、#v £60,000#!储备。续签不再交舰；一年后仅结束这项补贴。

**本轮英文**：The first agreement transfers #v 20 ships of the line#! to the central government. Luzon retains #v 20 frigates#! and the garrison, and gains exemption from military service if eligible. The central government pays #v £3,700#! weekly for #v 12 months#!. Tribute continues at the existing rate. The central government needs at least #v £5,000#! in weekly surplus excluding construction and #v £60,000#! in reserves. Renewals do not transfer additional ships; the end of the year terminates only this subsidy.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.11.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：驻屯岁费

**原AI英文**：驻屯岁费

**本轮中文**：驻屯岁费

**本轮英文**：A Garrison Subsidy

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.11.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋呈来驻屯大营与海船的支用册，请朝廷按年核拨岁费。宣慰司仍按旧章解送贡款，营饷与远洋海防另列一项，由中央库曹承支。\n\n此次议案开列每周#v £8,700#!，支给一年。朝廷与吕宋各存一册，以备逐月核销。

**原AI英文**：吕宋呈来驻屯大营与海船的支用册，请朝廷按年核拨岁费。宣慰司仍按旧章解送贡款，营饷与远洋海防另列一项，由中央库曹承支。\n\n此次议案开列每周#v £8,700#!，支给一年。朝廷与吕宋各存一册，以备逐月核销。

**本轮中文**：吕宋请求中央分担每年的驻屯与海防开销。岁贡仍依现有章程解送，中央另从国库承担一部分军费。\n\n此次议案请每周支付#v £8,700#!，支给一年。

**本轮英文**：Luzon requests an annual contribution towards the troops and ships it maintains for imperial service. Tribute would continue under the existing arrangement, while the central treasury would take on a separate share of the military expense.\n\nThe proposed payment is #v £8,700#! a week for one year.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.11.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：核准岁费，交吕宋签议。

**原AI英文**：核准岁费，交吕宋签议。

**本轮中文**：核准岁费，交吕宋签议。

**本轮英文**：Approve the subsidy and seek Luzon’s consent.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.12.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：岁费签押

**原AI英文**：岁费签押

**本轮中文**：岁费签押

**本轮英文**：Consent to the Subsidy

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.12.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：中央核拨岁费的文书送到了马尼拉。军需官把新款列在贡粮之外，重新登记各营的口粮、船员与修理开销。\n\n这一年，库曹每周支付#v £8,700#!。贡款仍循现有宗属章程解送，舰队与驻屯大营由宣慰司继续维持。

**原AI英文**：中央核拨岁费的文书送到了马尼拉。军需官把新款列在贡粮之外，重新登记各营的口粮、船员与修理开销。\n\n这一年，库曹每周支付#v £8,700#!。贡款仍循现有宗属章程解送，舰队与驻屯大营由宣慰司继续维持。

**本轮中文**：中央已经核准每周#v £8,700#!、支给一年的补贴。吕宋仍按现有宗属章程解贡，舰队与驻屯大营继续由宣慰司维持。\n\n还须吕宋最后同意，拨款才能开始。

**本轮英文**：The central government has approved #v £8,700#! in weekly payments for one year. Luzon would continue paying tribute under its present obligations and remain responsible for the fleet and garrison.\n\nThe administration in Manila must give final consent to begin the payments.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.12.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：签押，分册支用。

**原AI英文**：签押，分册支用。

**本轮中文**：签押，分册支用。

**本轮英文**：Sign the agreement.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.13.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：分任海防岁费

**原AI英文**：分任海防岁费

**本轮中文**：分任海防岁费

**本轮英文**：Funding the Naval Division

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.13.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：吕宋请将二十艘战列舰及其船籍交由中央，留下护卫舰守备群岛。驻屯大营仍留宣慰司，远洋从征的义务另按免役之议办理。\n\n贡款照章解送；整顿岁费则由中央每周支付#v £3,700#!，限一年。受领战列舰的驻地、船员和日常供给，由中央海军筹办。

**原AI英文**：吕宋请将二十艘战列舰及其船籍交由中央，留下护卫舰守备群岛。驻屯大营仍留宣慰司，远洋从征的义务另按免役之议办理。\n\n贡款照章解送；整顿岁费则由中央每周支付#v £3,700#!，限一年。受领战列舰的驻地、船员和日常供给，由中央海军筹办。

**本轮中文**：吕宋请求中央海军接管二十艘战列舰，由中央安排驻地、船员与供给；护卫舰与驻屯大营仍留群岛。\n\n贡款照旧解送。吕宋另请每周#v £3,700#!、支给一年的补贴，并按议定条件免除从征义务。

**本轮英文**：Luzon asks the central navy to take over twenty ships of the line, retaining the frigates and garrison for local defence. The central government would provide their new bases, crews and supplies.\n\nTribute would continue on the existing terms. Luzon seeks #v £3,700#! a week for one year and exemption from further military service under the agreed arrangements.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.13.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：按册分任，核拨岁费。

**原AI英文**：按册分任，核拨岁费。

**本轮中文**：按册分任，核拨岁费。

**本轮英文**：Approve the division and its funding.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.14.t`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：交舰与岁费

**原AI英文**：交舰与岁费

**本轮中文**：交舰与岁费

**本轮英文**：Ships and Funding

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.14.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：中央的批复和交舰清单一同摆在宣慰司案上。二十艘战列舰归中央接管，护卫舰与驻屯军留守；续签时沿用已经办结的船籍清单。\n\n整顿岁费每周#v £3,700#!，支给一年。贡赋依现有关系另计，免役依两国现行约定办理。

**原AI英文**：中央的批复和交舰清单一同摆在宣慰司案上。二十艘战列舰归中央接管，护卫舰与驻屯军留守；续签时沿用已经办结的船籍清单。\n\n整顿岁费每周#v £3,700#!，支给一年。贡赋依现有关系另计，免役依两国现行约定办理。

**本轮中文**：中央已经接受分任海防的提议。二十艘战列舰将由中央接管，护卫舰与驻屯军留守群岛；续签时仍承认此前的交舰结果。\n\n补贴每周#v £3,700#!，支给一年。贡赋与免役另依各自条款办理。吕宋尚须最后确认这份协定。

**本轮英文**：The central government has accepted the naval division. Twenty ships of the line would pass to its navy, while the frigates and garrison remain in Luzon. Renewals retain the transfer already made.\n\nThe agreement provides #v £3,700#! a week for one year. Tribute and exemption from military service follow their separate terms. Luzon must now give final consent.

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_finance.14.a`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：签押，照册交接。

**原AI英文**：签押，照册交接。

**本轮中文**：签押，照册交接。

**本轮英文**：Sign and complete the handover.

**原因**：英文槽为中文回退；保留既有金额、期限、主体、条约与舰船边界，以自然英文表达。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_propose_native_a_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_route_1_terms_tt$

**原AI英文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_route_1_terms_tt$

**本轮中文**：将议案送交中央审议，获准后由吕宋最后确认。拟议条款：\n\n$nesnd_phi_route_1_terms_tt$

**本轮英文**：Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\n\n$nesnd_phi_route_1_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_propose_native_b_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_route_2_terms_tt$

**原AI英文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_route_2_terms_tt$

**本轮中文**：将议案送交中央审议，获准后由吕宋最后确认。拟议条款：\n\n$nesnd_phi_route_2_terms_tt$

**本轮英文**：Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\n\n$nesnd_phi_route_2_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_propose_cash_a_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_cash_1_terms_tt$

**原AI英文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_cash_1_terms_tt$

**本轮中文**：将议案送交中央审议，获准后由吕宋最后确认。拟议条款：\n\n$nesnd_phi_cash_1_terms_tt$

**本轮英文**：Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\n\n$nesnd_phi_cash_1_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_phi_propose_cash_b_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_cash_2_terms_tt$

**原AI英文**：将议案送交中央审议，获准后由吕宋最后确认。拟定条款：\n\n$nesnd_phi_cash_2_terms_tt$

**本轮中文**：将议案送交中央审议，获准后由吕宋最后确认。拟议条款：\n\n$nesnd_phi_cash_2_terms_tt$

**本轮英文**：Submit the proposal to the central government. If approved, it returns to Luzon for final consent. Proposed terms:\n\n$nesnd_phi_cash_2_terms_tt$

**原因**：英文槽为中文回退，完整补译；把签署前同意、实际付款与期满后的维持区分，删去无选择价值的核册反复。

**来源**：M/localization/simp_chinese/nesnd_phi_finance_l_simp_chinese.yml; M/common/scripted_effects/nesnd_phi_finance.txt; M/events/nesnd_phi_finance.txt

**实际机制**：Existing four proposal routes and two-party consent retained. No new law, aid, ship or population effect; script outputs require source-level review, not engine certification.

### `nesnd_ten_status_sampling`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：正在采集前三个月的地方就业与生计数据。林场委办和正常立法可先行安排。

**原AI英文**：Collecting the first three monthly observations.

**本轮中文**：地方官正在汇报最初三个月的就业与生计。林场委办和法案审议可以先行。

**本轮英文**：Local officials are reporting on employment and livelihoods over the first three months. Logging commissions and legislation may proceed in the meantime.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_status_war`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：战争中暂停巩固。检查丹那沙林的港口、海运和实际市场接入。

**原AI英文**：Consolidation is interrupted by war. Review the port and market access.

**本轮中文**：战争已使生计巩固中断，港口、海运与市场往来有待恢复。

**本轮英文**：War has interrupted the recovery. Ports, shipping and access to markets must be restored.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_status_review`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：继续检验就业、收入与市场接入；完成还需一处非占地产业达到75%配员。

**原AI英文**：Continue monitoring; a non-arable industry must also reach 75% occupancy.

**本轮中文**：地方生计正在恢复，还须有一处不占耕地的产业达到75%配员。

**本轮英文**：Local livelihoods are recovering. At least one industry that does not use arable land must also reach 75% staffing.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_build_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将林场列入政府的正常建设计划，向木商和承包人开放雇工。保留染料园和稻田，先以一处林场检验当地的招工与销路。\n\n每次排入#v 1级#!，专项最多委办#v 2次#!，间隔#v 6个月#!。第二次需已有林场达到#v 75%#!配员且无原料短缺；木材市场价格须不低于基础价的#v 50%#!，国库至少#v £5,000#!，实际资源容量允许施工。工程照常消耗建设力和财政。新建后检查生产方式，工具或技工资质不足时可选原始林业。

**原AI英文**：Queue one level of government construction, at normal construction and treasury cost. At most two commissions, six months apart. Existing logging must reach 75% occupancy with no input shortage before expansion; market wood price must be at least 50% of base, reserves at least £5,000, and actual capacity available. Check production methods after creation; simple forestry avoids tool and machinist requirements.

**本轮中文**：委托商人经营林场，为当地增加不占耕地的雇工岗位。\n\n每次排入#v 1级#!政府建设，最多委办#v 2次#!，间隔#v 6个月#!。已有林场须达到#v 75%#!配员且无原料短缺；木价至少为基础价的#v 50%#!，国库至少#v £5,000#!，当地仍可建林场。工程照常消耗建设力和财政。工具或技工资质不足时，可选原始林业。

**本轮英文**：Commission a logging camp to provide paid work without taking arable land.\n\nEach commission queues #v 1 level#! of government construction, up to #v 2 commissions#! at least #v 6 months#! apart. Any existing logging camp must be #v 75%#! staffed without input shortages. Wood must sell for at least #v 50%#! of its base price, the treasury must hold #v £5,000#!, and local capacity must permit construction. Normal construction and treasury costs apply. Simple forestry can be used where tools or trained machinists are scarce.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_tenant_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：以固定租佃关系取代农奴的人身依附，让农户在交租之后安排自己的生计。\n\n启动原生租佃法立法：法律须可制定，有在阁利益集团或支持率至少#v 10%#!的政治运动支持；预计通过机会至少#v 15%#!、合法性至少#v 25#!，且没有其他法案、战争或革命。法案照常经历辩论、挫折与反对。

**原AI英文**：Begin normal Tenant Farmers enactment only if legally enactable, supported by a government interest group or a movement with 10% support, with at least 15% enactment chance and 25 legitimacy. No other enactment, war or revolution may be active.

**本轮中文**：以固定租佃关系取代农奴的人身依附，让农户在交租之后安排自己的生计。\n\n开始审议租佃法案：法律须可制定，并有执政利益集团或支持率至少#v 10%#!的政治运动支持；预计通过机会至少#v 15%#!，合法性至少#v 25#!，且没有其他在议法案、战争或革命。

**本轮英文**：Replace serfs’ personal dependence with tenancy, allowing farmers to plan their livelihoods after paying rent.\n\nBegin enacting Tenant Farmers. The law must be enactable and supported by an interest group in government or a political movement with at least #v 10%#! support. Enactment chance must be at least #v 15%#! and legitimacy at least #v 25#!, with no other law being enacted, war or revolution.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_abolish_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：终止以债务拘束人身的制度，把劳动契约与债契分开。\n\n取消农奴制后，地方无业劳动力至多#v 15%#!且已采样三个月，方可由此提出废奴法案。其余支持、通过机会及合法性门槛与租佃法案相同。实际解放发生在原生立法通过时。

**原AI英文**：After serfdom ends and local unemployment is at most 15%, begin normal slavery abolition with the same support and legitimacy requirements. At least three monthly samples are required. Enactment must actually pass.

**本轮中文**：废除奴隶制度，使劳动者不再作为他人的财产。\n\n取消农奴制后，地方无业劳动力至多#v 15%#!，且已有三个月的地方汇报，方可由此提出废奴法案。支持、通过机会及合法性门槛与租佃法案相同。法律通过后实行解放。

**本轮英文**：Abolish slavery so that workers can no longer be held as another person’s property.\n\nOnce serfdom has ended, local unemployment must be at most #v 15%#! and three months of local reports must be available. The support, enactment-chance and legitimacy requirements are the same as for Tenant Farmers. Emancipation takes effect when the law passes.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_dismiss_button_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：将地方经营交回现有官署与商行，停止专项统计和教习安排。一年后可以重新开办。

**原AI英文**：Return responsibility to existing local authorities. The programme can reopen after one year.

**本轮中文**：将地方经营交回现有官署与商行，停办专项教习。一年后可以重新开办。

**本轮英文**：Return the programme’s duties to the existing administration and merchants, ending its special instruction. The programme can reopen after one year.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_continue_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：继续专项，保留已有投资、法律和统计。不会增加土地、建筑或免费补贴。

**原AI英文**：Continue reviewing existing investments, laws and local livelihoods. No free land, buildings or subsidy is added.

**本轮中文**：续办丹那沙林专项，保留已有的工程、法案与拨款安排。

**本轮英文**：Continue the Tenasserim programme with its existing construction, legislation and funding arrangements.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_reopen_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：重新检验丹那沙林的就业与农户生计。保留以前的委办记录，从零重新计算连续巩固月份。

**原AI英文**：Resume observation and restart the consolidation streak. Prior commission records remain.

**本轮中文**：重新着手改善丹那沙林的就业与农户生计。以前的委办次数保留，生计巩固重新累计。

**本轮英文**：Resume efforts to improve employment and rural livelihoods in Tenasserim. Previous commissions still count towards the limit, and the period of recovery begins again.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_tenasserim.1.d`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：丹那沙林的地方官把村社账目送到了联省首府。许多农户一年到头守着稻田，收成出手之后，还要逐项偿还田租、种粮和债息。园主的货船照常离港，招工告示也已经贴出，村民手里的余钱仍买不起一家人所需的食粮。\n\n专项的账目需要重新审议：已有产业怎样雇人，旧契约怎样征收，官署又能从中拨出多少款项，都须一项项作出安排。

**原AI英文**：Village accounts have reached the provincial capital. Families work their rice fields throughout the year, then settle rent, seed advances and interest. Ships still carry plantation exports away while many households lack the money for food. Officials must review recruitment, tenancy and the funds available to sustain the programme.

**本轮中文**：丹那沙林的经营遇到了困难。为林场与工场招工，需要有人肯付工钱；让村民留住收成，则须处理租佃与债务。官署提供的教习也需要持续的经费。\n\n政府必须决定，是继续投入资源改善这些条件，还是把地方经营交回现有官署与商行。

**本轮英文**：The Tenasserim programme has run into difficulty. Logging camps and workshops need employers able to pay wages; villagers need tenancy and credit arrangements that leave them a livelihood. The practical instruction provided by the authorities also requires sustained funding.\n\nThe government must decide whether to keep committing resources or return these responsibilities to the existing administration and merchants.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `nesnd_ten_dismiss_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：移除本日志与专项教习效果；一年后可从决议重新开办。已排入的正常建设、正在审议的法律及已支付的补偿继续有效；委办额度和已得奖励不会重置。

**原AI英文**：Remove this journal and its instructional grant. Normal construction, enactment and paid compensation continue. Reopening after one year does not reset commissions or rewards.

**本轮中文**：停办专项并撤回学工教习，一年后可重新开办。已排入的建设、正在审议的法律及已付补偿继续有效；此前的委办次数与奖励仍然保留。

**本轮英文**：End the programme and withdraw its practical instruction. It may reopen after one year. Queued construction, ongoing legislation and compensation already paid remain in effect; previous commissions and rewards still count.

**原因**：去除采样/核验/免费效果反证等实现视角，保留具体行动、真实门槛与程序状态。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt; M/common/scripted_buttons/nesnd_tenasserim.txt; M/events/nesnd_tenasserim.txt

**实际机制**：No effect/threshold changes. Abolition refers to Slavery Banned, not a distinct debt-contract law.

### `STATE_SHAANBEI`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陕北

**原AI英文**：陕北

**本轮中文**：陕北

**本轮英文**：Shanbei

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:2

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_HANZHONG`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：汉中

**原AI英文**：汉中

**本轮中文**：汉中

**本轮英文**：Hanzhong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:3

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_CHUANNAN`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：川南

**原AI英文**：川南

**本轮中文**：川南

**本轮英文**：Southern Sichuan

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:4

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：关中农区

**原AI英文**：关中农区

**本轮中文**：关中农区

**本轮英文**：Guanzhong Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:5

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：秦岭林区

**原AI英文**：秦岭林区

**本轮中文**：秦岭林区

**本轮英文**：Qinling Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:6

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SICHUAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：川西矿区

**原AI英文**：川西矿区

**本轮中文**：川西矿区

**本轮英文**：Western Sichuan Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:7

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SICHUAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：岷江林区

**原AI英文**：岷江林区

**本轮中文**：岷江林区

**本轮英文**：Min River Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:8

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SHAANBEI_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：延安

**原AI英文**：延安

**本轮中文**：延安

**本轮英文**：Yan'an

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:9

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SHAANBEI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陕北煤田

**原AI英文**：陕北煤田

**本轮中文**：陕北煤田

**本轮英文**：Shanbei Coalfields

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:10

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SHAANBEI_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陕北农区

**原AI英文**：陕北农区

**本轮中文**：陕北农区

**本轮英文**：Shanbei Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:11

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SHAANBEI_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陕北林区

**原AI英文**：陕北林区

**本轮中文**：陕北林区

**本轮英文**：Shanbei Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:12

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HANZHONG_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：汉中

**原AI英文**：汉中

**本轮中文**：汉中

**本轮英文**：Hanzhong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:13

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HANZHONG_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：巴山矿区

**原AI英文**：巴山矿区

**本轮中文**：巴山矿区

**本轮英文**：Bashan Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:14

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HANZHONG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：汉水农区

**原AI英文**：汉水农区

**本轮中文**：汉水农区

**本轮英文**：Han River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:15

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HANZHONG_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：汉中林区

**原AI英文**：汉中林区

**本轮中文**：汉中林区

**本轮英文**：Hanzhong Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:16

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHUANNAN_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：泸州

**原AI英文**：泸州

**本轮中文**：泸州

**本轮英文**：Luzhou

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:17

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHUANNAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：西昌

**原AI英文**：西昌

**本轮中文**：西昌

**本轮英文**：Xichang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:18

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHUANNAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：川南农区

**原AI英文**：川南农区

**本轮中文**：川南农区

**本轮英文**：Southern Sichuan Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:19

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHUANNAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：川南林区

**原AI英文**：川南林区

**本轮中文**：川南林区

**本轮英文**：Southern Sichuan Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:20

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_xian`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陈秦水利・关中

**原AI英文**：陈秦水利・关中

**本轮中文**：陈秦水利・关中

**本轮英文**：Chen-Qin Irrigation: Guanzhong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:21

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_xian_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：沿用陈秦以来的水利设施与陆运驿路。

**原AI英文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮中文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮英文**：Irrigation works and overland post roads inherited from Chen-Qin support the region.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:22

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_shaanbei`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陈秦水利・陕北

**原AI英文**：陈秦水利・陕北

**本轮中文**：陈秦水利・陕北

**本轮英文**：Chen-Qin Irrigation: Shanbei

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:23

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_shaanbei_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：沿用陈秦以来的水利设施与陆运驿路。

**原AI英文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮中文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮英文**：Irrigation works and overland post roads inherited from Chen-Qin support the region.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:24

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_hanzhong`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陈秦水利・汉中

**原AI英文**：陈秦水利・汉中

**本轮中文**：陈秦水利・汉中

**本轮英文**：Chen-Qin Irrigation: Hanzhong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:25

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_hanzhong_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：沿用陈秦以来的水利设施与陆运驿路。

**原AI英文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮中文**：沿用陈秦以来的水利设施与陆运驿路。

**本轮英文**：Irrigation works and overland post roads inherited from Chen-Qin support the region.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:26

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_river_state_sichuan`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：长江水运・蜀国

**原AI英文**：长江水运・蜀国

**本轮中文**：长江水运・蜀国

**本轮英文**：Yangtze Navigation: Shu

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:27

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_river_state_sichuan_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：本地港埠经支流与长江干流连接。

**原AI英文**：本地港埠经支流与长江干流连接。

**本轮中文**：本地港埠经支流与长江干流连接。

**本轮英文**：Local river ports connect to the Yangtze through its tributaries.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:28

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_river_state_chuannan`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：长江水运・川南

**原AI英文**：长江水运・川南

**本轮中文**：长江水运・川南

**本轮英文**：Yangtze Navigation: Southern Sichuan

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:29

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_river_state_chuannan_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：本地港埠经支流与长江干流连接。

**原AI英文**：本地港埠经支流与长江干流连接。

**本轮中文**：本地港埠经支流与长江干流连接。

**本轮英文**：Local river ports connect to the Yangtze through its tributaries.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_geography_l_simp_chinese.yml:30

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_JINBEI_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：大同

**原AI英文**：大同

**本轮中文**：大同

**本轮英文**：Datong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:2

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_JINBEI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：雁北煤田

**原AI英文**：雁北煤田

**本轮中文**：雁北煤田

**本轮英文**：Yanbei Coalfields

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:3

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_JINBEI_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桑干农区

**原AI英文**：桑干农区

**本轮中文**：桑干农区

**本轮英文**：Sanggan Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:4

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_JINBEI_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：恒山林区

**原AI英文**：恒山林区

**本轮中文**：恒山林区

**本轮英文**：Hengshan Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:5

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SHANXI_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：太行山

**原AI英文**：太行山

**本轮中文**：太行山

**本轮英文**：Taihang Mountains

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:6

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_shanxi`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：太原水运

**原AI英文**：太原水运

**本轮中文**：太原水运

**本轮英文**：Taiyuan River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:7

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_shanxi_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:8

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_jinbei`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：晋北水运

**原AI英文**：晋北水运

**本轮中文**：晋北水运

**本轮英文**：Northern Shanxi River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:9

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_jinbei_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:10

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHENGDE_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：承德

**原AI英文**：承德

**本轮中文**：承德

**本轮英文**：Chengde

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:11

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHENGDE_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：热河矿区

**原AI英文**：热河矿区

**本轮中文**：热河矿区

**本轮英文**：Rehe Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:12

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHENGDE_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：滦河农区

**原AI英文**：滦河农区

**本轮中文**：滦河农区

**本轮英文**：Luan River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:13

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHENGDE_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：燕山林区

**原AI英文**：燕山林区

**本轮中文**：燕山林区

**本轮英文**：Yanshan Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:14

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SONGJIANG_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：宁古塔

**原AI英文**：宁古塔

**本轮中文**：宁古塔

**本轮英文**：Ningguta

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:15

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SONGJIANG_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：牡丹江矿区

**原AI英文**：牡丹江矿区

**本轮中文**：牡丹江矿区

**本轮英文**：Mudan River Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:16

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SONGJIANG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：三江农区

**原AI英文**：三江农区

**本轮中文**：三江农区

**本轮英文**：Sanjiang Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:17

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_SONGJIANG_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：完达山林区

**原AI英文**：完达山林区

**本轮中文**：完达山林区

**本轮英文**：Wanda Mountains Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:18

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ZITONG_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：绵阳

**原AI英文**：绵阳

**本轮中文**：绵阳

**本轮英文**：Mianyang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:19

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ZITONG_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：广元

**原AI英文**：广元

**本轮中文**：广元

**本轮英文**：Guangyuan

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:20

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ZITONG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：嘉陵农区

**原AI英文**：嘉陵农区

**本轮中文**：嘉陵农区

**本轮英文**：Jialing Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:21

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ZITONG_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：剑门林区

**原AI英文**：剑门林区

**本轮中文**：剑门林区

**本轮英文**：Jianmen Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:22

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHONGQING_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：川东矿区

**原AI英文**：川东矿区

**本轮中文**：川东矿区

**本轮英文**：Eastern Sichuan Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:23

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_CHONGQING_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：华蓥山

**原AI英文**：华蓥山

**本轮中文**：华蓥山

**本轮英文**：Huaying Mountains

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:24

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_chongqing`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：重庆水运

**原AI英文**：重庆水运

**本轮中文**：重庆水运

**本轮英文**：Chongqing River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:25

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_chongqing_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:26

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_zitong`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：梓潼水运

**原AI英文**：梓潼水运

**本轮中文**：梓潼水运

**本轮英文**：Zitong River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:27

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_zitong_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:28

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIANGYANG_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：襄阳

**原AI英文**：襄阳

**本轮中文**：襄阳

**本轮英文**：Xiangyang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:29

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIANGYANG_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：襄北矿区

**原AI英文**：襄北矿区

**本轮中文**：襄北矿区

**本轮英文**：Northern Xiangyang Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:30

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIANGYANG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：南襄农区

**原AI英文**：南襄农区

**本轮中文**：南襄农区

**本轮英文**：Nanxiang Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:31

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_XIANGYANG_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：荆山林区

**原AI英文**：荆山林区

**本轮中文**：荆山林区

**本轮英文**：Jingshan Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:32

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_WESTERN_HUBEI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：荆西矿区

**原AI英文**：荆西矿区

**本轮中文**：荆西矿区

**本轮英文**：Western Jingzhou Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:33

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_western_hubei`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：荆州水运

**原AI英文**：荆州水运

**本轮中文**：荆州水运

**本轮英文**：Jingzhou River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:34

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_western_hubei_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:35

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_xiangyang`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：襄阳水运

**原AI英文**：襄阳水运

**本轮中文**：襄阳水运

**本轮英文**：Xiangyang River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:36

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_xiangyang_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:37

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GANZHOU_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣州

**原AI英文**：赣州

**本轮中文**：赣州

**本轮英文**：Ganzhou

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:38

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GANZHOU_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣南矿区

**原AI英文**：赣南矿区

**本轮中文**：赣南矿区

**本轮英文**：Southern Jiangxi Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:39

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GANZHOU_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣江农区

**原AI英文**：赣江农区

**本轮中文**：赣江农区

**本轮英文**：Gan River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:40

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GANZHOU_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：南岭林区

**原AI英文**：南岭林区

**本轮中文**：南岭林区

**本轮英文**：Nanling Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:41

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_JIANGXI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣北矿区

**原AI英文**：赣北矿区

**本轮中文**：赣北矿区

**本轮英文**：Northern Jiangxi Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:42

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_jiangxi`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：南昌水运

**原AI英文**：南昌水运

**本轮中文**：南昌水运

**本轮英文**：Nanchang River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:43

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_jiangxi_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:44

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_ganzhou`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣南水运

**原AI英文**：赣南水运

**本轮中文**：赣南水运

**本轮英文**：Southern Jiangxi River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:45

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_ganzhou_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:46

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUILIN_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桂林

**原AI英文**：桂林

**本轮中文**：桂林

**本轮英文**：Guilin

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:47

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUILIN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桂北矿区

**原AI英文**：桂北矿区

**本轮中文**：桂北矿区

**本轮英文**：Northern Guangxi Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:48

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUILIN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：柳江农区

**原AI英文**：柳江农区

**本轮中文**：柳江农区

**本轮英文**：Liu River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:49

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUILIN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：越城岭林区

**原AI英文**：越城岭林区

**本轮中文**：越城岭林区

**本轮英文**：Yuecheng Mountains Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:50

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUANGXI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桂南矿区

**原AI英文**：桂南矿区

**本轮中文**：桂南矿区

**本轮英文**：Southern Guangxi Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:51

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUANGXI_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：郁江农区

**原AI英文**：郁江农区

**本轮中文**：郁江农区

**本轮英文**：Yu River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:52

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_guangxi`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：南宁水运

**原AI英文**：南宁水运

**本轮中文**：南宁水运

**本轮英文**：Nanning River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:53

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_guangxi_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:54

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_guilin`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桂北水运

**原AI英文**：桂北水运

**本轮中文**：桂北水运

**本轮英文**：Northern Guangxi River Transport

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:55

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_water_state_guilin_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：支流、渡口与沿河驿道构成当地的运输网络。

**原AI英文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮中文**：支流、渡口与沿河驿道构成当地的运输网络。

**本轮英文**：Tributaries, ferries and riverside post roads form the local transport network.

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_national_map_l_simp_chinese.yml:56

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTHERN_FUJIAN_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：闽江府

**原AI英文**：闽江府

**本轮中文**：闽江府

**本轮英文**：Minjiang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:2

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTHERN_FUJIAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：三明

**原AI英文**：三明

**本轮中文**：三明

**本轮英文**：Sanming

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:3

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTHERN_FUJIAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：南平

**原AI英文**：南平

**本轮中文**：南平

**本轮英文**：Nanping

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:4

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTHERN_FUJIAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：闽北林区

**原AI英文**：闽北林区

**本轮中文**：闽北林区

**本轮英文**：Northern Fujian Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:5

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTHERN_FUJIAN_port`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：闽江港

**原AI英文**：闽江港

**本轮中文**：闽江港

**本轮英文**：Minjiang Harbor

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:6

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_FUJIAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：晋江农区

**原AI英文**：晋江农区

**本轮中文**：晋江农区

**本轮英文**：Jin River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:7

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_FUJIAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：闽西矿务

**原AI英文**：闽西矿务

**本轮中文**：闽西矿务

**本轮英文**：Western Fujian Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:8

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_refine_water_state_dzungaria`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：分区供水工程

**原AI英文**：分区供水工程

**本轮中文**：水利工程

**本轮英文**：Irrigation Works

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_dzungaria_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**原AI英文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**本轮中文**：既有水利设施支持农田灌溉，当地道路与水道也因此便于维持。

**本轮英文**：Established waterworks support irrigation and the upkeep of local transport routes.

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_ili`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：分区供水工程

**原AI英文**：分区供水工程

**本轮中文**：水利工程

**本轮英文**：Irrigation Works

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_ili_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**原AI英文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**本轮中文**：既有水利设施支持农田灌溉，当地道路与水道也因此便于维持。

**本轮英文**：Established waterworks support irrigation and the upkeep of local transport routes.

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `HUB_NAME_STATE_ILI_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：伊犁

**原AI英文**：伊犁

**本轮中文**：伊犁

**本轮英文**：Ili

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:13

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ILI_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：伊犁屯田

**原AI英文**：伊犁屯田

**本轮中文**：伊犁屯田

**本轮英文**：Ili Military Farms

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:14

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ILI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：伊犁山矿

**原AI英文**：伊犁山矿

**本轮中文**：伊犁山矿

**本轮英文**：Ili Mountain Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:15

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_ILI_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：胡杨地

**原AI英文**：胡杨地

**本轮中文**：胡杨地

**本轮英文**：Poplar Groves

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:16

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_WESTERN_TIANSHAN_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：乌恰

**原AI英文**：乌恰

**本轮中文**：乌恰

**本轮英文**：Wuqia

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:17

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_WESTERN_TIANSHAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：西天山绿洲

**原AI英文**：西天山绿洲

**本轮中文**：西天山绿洲

**本轮英文**：Western Tianshan Oases

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:18

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_WESTERN_TIANSHAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：阿克苏

**原AI英文**：阿克苏

**本轮中文**：阿克苏

**本轮英文**：Aksu

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:19

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_WESTERN_TIANSHAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：西天山河林

**原AI英文**：西天山河林

**本轮中文**：西天山河林

**本轮英文**：Western Tianshan River Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:20

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_TIANSHAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：盆地北缘矿务

**原AI英文**：盆地北缘矿务

**本轮中文**：盆地北缘矿务

**本轮英文**：Northern Basin Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:21

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_TIANSHAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：盆地北缘河林

**原AI英文**：盆地北缘河林

**本轮中文**：盆地北缘河林

**本轮英文**：Northern Basin River Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:22

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_refine_water_state_gansu`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：分区供水工程

**原AI英文**：分区供水工程

**本轮中文**：水利工程

**本轮英文**：Irrigation Works

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_gansu_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**原AI英文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**本轮中文**：既有水利设施支持农田灌溉，当地道路与水道也因此便于维持。

**本轮英文**：Established waterworks support irrigation and the upkeep of local transport routes.

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_hexi`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：分区供水工程

**原AI英文**：分区供水工程

**本轮中文**：水利工程

**本轮英文**：Irrigation Works

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `nesnd_refine_water_state_hexi_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**原AI英文**：原供水工程的固定运输容量按实际分区分摊；灌溉增益沿用既有设计。

**本轮中文**：既有水利设施支持农田灌溉，当地道路与水道也因此便于维持。

**本轮英文**：Established waterworks support irrigation and the upkeep of local transport routes.

**原因**：删除分区分摊、沿用设计等地图编辑说明，描述实际农业及基础设施作用。

**来源**：M/common/state_traits/nesnd_refinement_water.txt:1,9,17,25

**实际机制**：Four traits retain +5% agriculture throughput, 12/18 flat infrastructure and +15% infrastructure. No territorial or engineering claim added.

### `HUB_NAME_STATE_HEXI_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：敦煌

**原AI英文**：敦煌

**本轮中文**：敦煌

**本轮英文**：Dunhuang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:27

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HEXI_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：河西屯田

**原AI英文**：河西屯田

**本轮中文**：河西屯田

**本轮英文**：Hexi Military Farms

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:28

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HEXI_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：河西矿务

**原AI英文**：河西矿务

**本轮中文**：河西矿务

**本轮英文**：Hexi Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:29

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_HEXI_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：祁连林区

**原AI英文**：祁连林区

**本轮中文**：祁连林区

**本轮英文**：Qilian Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:30

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GANSU_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：陇中矿务

**原AI英文**：陇中矿务

**本轮中文**：陇中矿务

**本轮英文**：Central Gansu Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:31

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GAOLIANG_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：高凉城

**原AI英文**：高凉城

**本轮中文**：高凉城

**本轮英文**：Gaoliang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:32

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GAOLIANG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：茂名

**原AI英文**：茂名

**本轮中文**：茂名

**本轮英文**：Maoming

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:33

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GAOLIANG_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：高凉矿务

**原AI英文**：高凉矿务

**本轮中文**：高凉矿务

**本轮英文**：Gaoliang Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:34

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GAOLIANG_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：高凉山林

**原AI英文**：高凉山林

**本轮中文**：高凉山林

**本轮英文**：Gaoliang Forests

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:35

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GAOLIANG_port`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：高凉港

**原AI英文**：高凉港

**本轮中文**：高凉港

**本轮英文**：Gaoliang Harbor

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:36

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_GUANGDONG_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：珠江农区

**原AI英文**：珠江农区

**本轮中文**：珠江农区

**本轮英文**：Pearl River Farmland

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:37

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTH_DAYUAN_city`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：北原府

**原AI英文**：北原府

**本轮中文**：北原府

**本轮英文**：Beiyuan

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:38

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTH_DAYUAN_farm`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：北原屯田

**原AI英文**：北原屯田

**本轮中文**：北原屯田

**本轮英文**：Beiyuan Military Farms

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:39

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTH_DAYUAN_mine`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：北原山矿

**原AI英文**：北原山矿

**本轮中文**：北原山矿

**本轮英文**：Beiyuan Mountain Mines

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:40

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTH_DAYUAN_wood`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：黄山

**原AI英文**：黄山

**本轮中文**：黄山

**本轮英文**：Huangshan

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:41

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `HUB_NAME_STATE_NORTH_DAYUAN_port`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：北原港

**原AI英文**：北原港

**本轮中文**：北原港

**本轮英文**：Beiyuan Harbor

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\replace\zz_nesnd_map_refinement_l_simp_chinese.yml:42

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_JINBEI`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：晋北

**原AI英文**：晋北

**本轮中文**：晋北

**本轮英文**：Northern Shanxi

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:2

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_CHENGDE`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：热河

**原AI英文**：热河

**本轮中文**：热河

**本轮英文**：Rehe

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:3

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_SONGJIANG`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：松江

**原AI英文**：松江

**本轮中文**：松江

**本轮英文**：Songjiang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:4

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_ZITONG`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：梓潼

**原AI英文**：梓潼

**本轮中文**：梓潼

**本轮英文**：Zitong

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:5

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_XIANGYANG`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：襄阳

**原AI英文**：襄阳

**本轮中文**：襄阳

**本轮英文**：Xiangyang

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:6

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_GANZHOU`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：赣南

**原AI英文**：赣南

**本轮中文**：赣南

**本轮英文**：Southern Jiangxi

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:7

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `STATE_GUILIN`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：桂北

**原AI英文**：桂北

**本轮中文**：桂北

**本轮英文**：Northern Guangxi

**原因**：英文槽为中文回退；按既有中文地名/功能转写，不另造地名或改变归属。

**来源**：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties\localization\simp_chinese\nesnd_editor_l_simp_chinese.yml:8

**实际机制**：Map/hub/state-trait label only; fictional working names retained as names, not upgraded to author canon.

### `nesnd_jingyin_departure_title`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：淮王登极

**原AI英文**：淮王登极

**本轮中文**：淮王登极

**本轮英文**：The Prince of Huai Takes the Throne

**原因**：英文槽中文回退；原有头衔不改。

**来源**：M/localization/simp_chinese/nesnd_character_notifications_l_simp_chinese.yml:2

**实际机制**：Notification of existing relocation; not new succession.

### `nesnd_jingyin_departure_desc`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：登极的诏书传到了[ROOT.GetCountry.GetName]。#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!已受群臣拥戴，前往[SCOPE.sCountry('new_jingyin_owner').GetCapital.GetName]主持朝政。随行官属整点印信、车马，旧邸诸事留待本国料理。

**原AI英文**：登极的诏书传到了[ROOT.GetCountry.GetName]。#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!已受群臣拥戴，前往[SCOPE.sCountry('new_jingyin_owner').GetCapital.GetName]主持朝政。随行官属整点印信、车马，旧邸诸事留待本国料理。

**本轮中文**：登极的消息传到了[ROOT.GetCountry.GetName]。#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!已受群臣拥戴，前往[SCOPE.sCountry('new_jingyin_owner').GetCapital.GetName]主持朝政。旧邸的官员须留下料理交接，随行臣属则将辅佐新朝的政务。

**本轮英文**：News of the accession has reached [ROOT.GetCountry.GetName]. #bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#! has received the ministers’ support and left for [SCOPE.sCountry('new_jingyin_owner').GetCapital.GetName] to take charge of government. Officials at the former residence must complete the handover, while those accompanying the new ruler will serve at the new court.

**原因**：避免无明确颁诏主体的登极诏书，去除印信车马道具堆叠；保留现有人物/新拥有国scope。

**来源**：M/events/usm_civilwar_events.txt:2635; M/common/scripted_triggers/nesnd_character_notification_triggers.txt:4; M/common/scripted_effects/nesnd_character_notification_effects.txt:20

**实际机制**：Existing saved country/character scopes guarded by notification trigger, ownership and alive checks. Generic fallback permits any valid new capital; GNG->Nanjing uses the separate original-author branch.

### `nesnd_jingyin_departure_tt`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!现为[SCOPE.sCountry('new_jingyin_owner').GetName]的统治者。[ROOT.GetCountry.GetName]获得#v 10年#!的#bold $USM_benifit_of_an_emperor$#!。

**原AI英文**：#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!现为[SCOPE.sCountry('new_jingyin_owner').GetName]的统治者。[ROOT.GetCountry.GetName]获得#v 10年#!的#bold $USM_benifit_of_an_emperor$#!。

**本轮中文**：#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#!现为[SCOPE.sCountry('new_jingyin_owner').GetName]的统治者。[ROOT.GetCountry.GetName]获得#v 10年#!的#bold $USM_benifit_of_an_emperor$#!。

**本轮英文**：#bold [SCOPE.sCharacter('nesnd_jingyin_claimant').GetFullName]#! now rules [SCOPE.sCountry('new_jingyin_owner').GetName]. [ROOT.GetCountry.GetName] gains #bold $USM_benifit_of_an_emperor$#! for #v 10 years#!.

**原因**：英文槽中文回退；保留原动态引用、既有修正名和十年时长。

**来源**：M/localization/simp_chinese/nesnd_character_notifications_l_simp_chinese.yml:4

**实际机制**：Only reports existing benefit; no monarch scope invented.

### `nesnd_ten_continuity_bar_detail`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：采样至少三个月后，四项地方条件达标，且林场、渔场、铁矿、工具厂、纺织厂或食品厂中至少一处配员达到#v 75%#!并无原料短缺，每月增加#p 1#!。条件中断时连续月份归零。完成后当地获得#v 24个月#!的#p +10%#!资质获取。\n\n全国制度改革仍由$je_reform_indies$推进。

**原AI英文**：After three samples, meet all four conditions and keep a logging camp, fishery, iron mine, tooling workshop, textile mill or food industry at 75% occupancy without an input shortage for six consecutive months. Interruption resets the streak. Completion grants local qualifications +10% for 24 months. National reform continues separately.

**本轮中文**：最初三个月的地方汇报送齐后，四项生计条件达标，且林场、渔场、铁矿、工具厂、纺织厂或食品厂中至少一处配员达到#v 75%#!并无原料短缺，每月增加#p 1#!。条件中断时连续月份归零。完成后当地获得#v 24个月#!的#p +10%#!资质获取。\n\n全国制度改革仍由$je_reform_indies$推进。

**本轮英文**：After the first three months of local reports, gain #p 1#! per month with all four livelihood requirements met and at least one logging camp, fishery, iron mine, tooling workshop, textile mill or food industry #v 75%#! staffed without input shortages. A failure resets the consecutive-month count. Completion grants #p +10%#! qualifications gain locally for #v 24 months#!.\n\nNational institutional reform proceeds through $je_reform_indies$.

**原因**：将samples改成地方汇报并保留被旧英译漏掉的国家改革日志引用；数字和效果不变。

**来源**：M/common/scripted_triggers/nesnd_tenasserim.txt:10; M/common/scripted_effects/nesnd_tenasserim.txt

**实际机制**：Three observation months then six healthy months; local modifier only.

### `nesnd_ten_conditions_bar_detail`

判定：返工 → 编辑提案通过；适用 `E_and_C`。未接入游戏。

**原AI中文**：无业劳动力：#v [Country.MakeScope.Var('nesnd_ten_unemployment').GetValue|%1]#!\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_ten_starving').GetValue|%1]#!\n其中在岗且欠食：#v [Country.MakeScope.Var('nesnd_ten_working_hungry').GetValue|%1]#!\n劳动力家庭[concept_sol]：#v [Country.MakeScope.Var('nesnd_ten_sol').GetValue|1]#!\n[concept_market_access]：#v [Country.MakeScope.Var('nesnd_ten_access').GetValue|%1]#!\n\n四项条件：无业至多#v 12%#!；欠食至多#v 25%#!且生活水平至少#v 6.5#!；接入至少#v 85%#!；和平且未受[concept_bankruptcy]惩罚。份额按丹那沙林本国州的劳动力计算，自给农属于有业人口，每月更新。

**原AI英文**：Unemployed workforce: #v [Country.MakeScope.Var('nesnd_ten_unemployment').GetValue|%1]#!\nHungry workforce: #v [Country.MakeScope.Var('nesnd_ten_starving').GetValue|%1]#!\nEmployed and hungry: #v [Country.MakeScope.Var('nesnd_ten_working_hungry').GetValue|%1]#!\nWorkforce-weighted living standards: #v [Country.MakeScope.Var('nesnd_ten_sol').GetValue|1]#!\nMarket access: #v [Country.MakeScope.Var('nesnd_ten_access').GetValue|%1]#!\n\nTargets: unemployment <=12%; hunger <=25% and living standards >=6.5; access >=85%; peace and no active [concept_bankruptcy] penalty. Workforce shares are refreshed monthly. Subsistence farmers are employed.

**本轮中文**：无业劳动力：#v [Country.MakeScope.Var('nesnd_ten_unemployment').GetValue|%1]#!\n欠食劳动力：#v [Country.MakeScope.Var('nesnd_ten_starving').GetValue|%1]#!\n其中在岗且欠食：#v [Country.MakeScope.Var('nesnd_ten_working_hungry').GetValue|%1]#!\n劳动力家庭[concept_sol]：#v [Country.MakeScope.Var('nesnd_ten_sol').GetValue|1]#!\n[concept_market_access]：#v [Country.MakeScope.Var('nesnd_ten_access').GetValue|%1]#!\n\n四项条件：无业至多#v 12%#!；欠食至多#v 25%#!且生活水平至少#v 6.5#!；接入至少#v 85%#!；和平且未受[concept_bankruptcy]惩罚。份额按丹那沙林本国州的劳动力计算，自给农属于有业人口，每月更新。

**本轮英文**：Unemployed workforce: #v [Country.MakeScope.Var('nesnd_ten_unemployment').GetValue|%1]#!\nWorkforce below the starvation threshold: #v [Country.MakeScope.Var('nesnd_ten_starving').GetValue|%1]#!\nEmployed and below the starvation threshold: #v [Country.MakeScope.Var('nesnd_ten_working_hungry').GetValue|%1]#!\nWorkforce household [concept_sol]: #v [Country.MakeScope.Var('nesnd_ten_sol').GetValue|1]#!\n[concept_market_access]: #v [Country.MakeScope.Var('nesnd_ten_access').GetValue|%1]#!\n\nRequirements: unemployment at most #v 12%#!; at most #v 25%#! below the starvation threshold and living standards of at least #v 6.5#!; market access of at least #v 85%#!; peace and no active [concept_bankruptcy] penalty. Shares are calculated from the workforce in our part of Tenasserim and updated monthly. Subsistence farmers count as employed.

**原因**：现有英译遗漏本国丹那沙林分母，且用代码式<=；补齐地域与scope边界，保留真正生效的bankruptcy override。

**来源**：M/localization/english/replace/zzzzzz_nesnd_concept_clarity_l_english.yml:3; M/common/script_values/nesnd_tenasserim.txt

**实际机制**：Only DEI-owned Tenasserim state workforce, not national or whole foreign-held region.

## 边界

审阅是逐条编辑判断。正则仅用于键清单、引用保留、SHA与未译回退检查，未据关键词自动判定作者风格。没有运行引擎，没有保证所有分支无BUG，也没有验证实际窗口排版。新人物对话未添加；秦军府、日本幕府/军府和合法国际盟约不因词形被机械替换。