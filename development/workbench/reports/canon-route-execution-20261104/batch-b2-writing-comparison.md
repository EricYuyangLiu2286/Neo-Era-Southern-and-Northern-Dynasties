# B2 作者原文与候选逐项对读

2026-11-04。**编辑对读通过，脚本与引擎验收待独立测试。** 本代理显式委派配置gpt-6.1-sol / medium。本表只判断措辞、叙事主体与已写脚本的对应，不证明作者身份或游戏行为。来源SHA与实际行号见同目录 `batch-b2-sources.json`；本轮生效文件与SHA见 `batch-b2-freeze.json`。

## 可追溯作者样本

基准为独立备份 `WORK/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace`，未把当前代理写过的replace当作者训练样本。

|编号|原作者原文与出处|本轮可观察语体|
|---|---|---|
|S1|ce_cne_events_l_simp_chinese.yml，ce_cne_land_reform_reason，第15行：“用赎买或强制剥夺的手段，将超额聚敛的土地从其旧时代的所有者手中剥夺，平均到部分农民手中。”|土地、生产、利益持有者与权力的实际动作构成因果；不是办证流程。|
|S2|ce_country_flavor_text_l_simp_chinese.yml，MUG_FLAVOR_TEXT，第30行：“或许他们应该进一步倚重法国的帮助，以对抗日益膨胀的东方天朝，抑或完全相反，乃至自力更生。”|外援、自主和实际利益允许多条政治道路，叙事不替玩家宣布未来已经发生。|
|S3|ce_french_empire_journals_l_simp_chinese.yml，ce_french_support_dynasty_button_desc，第237行：“波拿巴的道路是[ROOT.GetCountry.GetAdjective]民族团结和繁荣的唯一办法。”；同文件ce_french_against_dynasty_button_desc，第240行以共和派的政治判断发言。|行动与判断有主体。按钮可直接表态，但不将作者既有立场随意套给不相关国家。|
|S4|同文件，ce_french_empire_oreleans_progress_bar_name，第248行：“政变准备”；第249行用原生JournalEntry.GetCurrentBarValue显示实际数值。|短名称、原生读数与正文分工；数值字段不承担开发说明。|
|S5|ce_00_countries_l_simp_chinese.yml中的LAN/DEI/YN1既有名称；本轮按钮最终复用$TAG$。|专名沿既有覆盖层，不重译兰芳、南洋联省与远南。|

## 已返工的具体问题

|原候选|问题|最终修改与脚本依据|
|---|---|---|
|“南朝与其他外国持有的股份仍依实际所有权存在”/“过去的外国股份也没有被一纸许诺抹去”|开局存在的股份不保证完成阶段时还存在；后一表述带开发辩解口吻。|远南完成事件改写两地区生产、港口和公共收入；脚本根本不转移资产，叙事不再臆断当前股权。|
|“不必把夺取阿拉干作为生活的出路”/“不必把征服外国港口当作唯一的出路”|把开发约束写成玩家正文，重复解释不存在的强制任务。|缅甸事件写上下游农户/商人收入、行政教育和对外关系；原有政治路线不被预告。|
|中文正文中的“Pegu”、按钮手写国家译名|与既有译名覆盖脱节。|正文复用$STATE_PEGU$/$STATE_MANDALAY$；防御按钮复用$TAG$。|
|“全国失业率”作为J指标的可能概括|J的分子是满足失业率门槛的州内全体人口，分母为直接州人口。|本轮所有状态与标签明确“失业率不高于10%的州内人口占比”；T也按州内人口覆盖叙述。|
|同类专业化的宽泛一句话|可能误导为稻1+茶1就满足地区2级。|提示写“每区一种至少2级、同类而两地type不同”；源码按每type分别聚合。|
|正文预告独立或外国已经建厂|不符合高自主分支、投资许可与实际经营的区别。|政府提出请求，实际执行与结果另核；资本文案引用已审C1许可原文，经营阶段看真实就业/利润。|

## 全部186对有效新增文本

每行“原文”使用上表可追溯样本编号。候选为冻结文件内最终中英文；“通过”是编辑判断。中文长句未逐逗号机械翻译英文，条约/法组/期限与脚本同名对象对应。

|键|作者样本|最终中文候选|最终英文候选|对读决定|
|---|---|---|---|---|
| `nesnd_small_livelihood_journal` | S1/S3/S4 | 邦国的生计 | The Livelihood of the Country | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_livelihood_journal_reason` | S1/S2 | 本国的农户、工匠和商人各有生计，也承受着地租、税负和市场变动。政府若要争得更多自主，就须先使地方生产有销路，公共事务有人承担。外国投资能够带来新的机会，实际厂房与雇工却仍要在本地经营；宗主和市场主人的承诺，也须成为真正生效的安排。 | Farmers, artisans and merchants earn their living under rents, taxes and changing markets. Greater autonomy requires working local industries and public services. Foreign investment may open opportunities, but workshops and employment must take root here, and diplomatic promises must become effective arrangements. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_subject_status` | S4 | [JournalEntry.GetCountry.TryGetOverlordTooltipEntry]<br>失业率不高于10%的州内人口占比：[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_job_coverage')\|%1]。市场接入达80%的州内人口占比：[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_transport')\|%1]。 | [JournalEntry.GetCountry.TryGetOverlordTooltipEntry]<br>Population living in states with unemployment at or below 10%: [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_job_coverage')\|%1]. Population in states with at least 80% market access: [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_transport')\|%1]. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_independent_status` | S4 | 本国已独立。失业率不高于10%的州内人口占比：[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_job_coverage')\|%1]。市场接入达80%的州内人口占比：[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_transport')\|%1]。 | The country is independent. Population living in states with unemployment at or below 10%: [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_job_coverage')\|%1]. Population in states with at least 80% market access: [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_transport')\|%1]. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_targets_lost` | S1/S3/S4 | 原定地区已失去足够的人口或实际支点，地区建设暂停。可待条件恢复，也可重订当前国土上的两区目标。 | The selected regions no longer retain sufficient population or their actual centres. Regional work is paused. Restore the conditions or select two regions within the present territory. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_economy_journal` | S1/S3/S4 | 活下去 | Making a Living | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_economy_journal_reason` | S1/S2 | 农户与雇工能否维持生活，取决于生产、就业和货物运输。现有产业也可成为发展的根基。 | Existing industries can sustain the country if they provide work, earn a profit and reach their markets. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_economy_months_tt` | S3/S4 | 已累计12个达标月 | Accumulate 12 qualifying months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_governance_journal` | S1/S3/S4 | 地方的根基 | Local Foundations | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_governance_journal_reason` | S1/S2 | 税收、教育和公共事务需要长期有人承担。首都的一所学校不能代替地方的经营，政治上的许诺也不能代替实际服务。 | Tax collection, education and public affairs require people and resources. Political promises must be supported by functioning services. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_governance_months_tt` | S3/S4 | 已累计12个达标月 | Accumulate 12 qualifying months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_regional_economy_journal` | S1/S3/S4 | 地区生产与市场 | Regional Production and Markets | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_regional_economy_journal_reason` | S1/S2 | 人口中心与其他地区需要各有能维持的产业，并通过交通参与同一个市场。农牧、种植、矿业、渔林和加工可以形成不同的分工；不必在每个地区重造一套产业。 | Population centres and outlying regions need viable industries linked by transport. Agriculture, plantations, mining, timber, fishing and manufacturing can support different specialities. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_regional_economy_months_tt` | S3/S4 | 已累计12个达标月 | Accumulate 12 qualifying months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_regional_governance_journal` | S1/S3/S4 | 地区治理 | Governing the Regions | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_regional_governance_journal_reason` | S1/S2 | 地方的收入不能只供养首都。两个地区都须有人办理公共事务，学校和大学才能使越来越多的居民承担新的职业。 | Public revenue must support more than the capital. Both regions need functioning administration, while schools and universities prepare residents for new occupations. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_regional_governance_months_tt` | S3/S4 | 已累计12个达标月 | Accumulate 12 qualifying months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_order_journal` | S1/S3/S4 | 自主后的秩序 | An Order We Can Sustain | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_order_journal_reason` | S1/S2 | 独立或高度自主能扩大政府的选择，也把市场、法律与防御的责任留给本国。既有法律与外交安排可以沿用，前提是它们仍在实际发挥作用。 | Independence or high autonomy broadens the government's choices and responsibilities for markets, law and defence. Existing laws and agreements may serve, provided they remain effective. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_order_months_tt` | S3/S4 | 已累计24个达标月 | Accumulate 24 qualifying months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_working_status` | S4 | 本月条件满足，经营观察可以继续。 | Conditions are met this month; observation can continue. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_paused_status` | S4 | 本月尚未满足全部条件，已积累的有效月份保留。 | Some conditions are unmet this month. Previously earned qualifying months are retained. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_dispute_journal` | S1/S3/S4 | 国内争议 | A Domestic Dispute | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_dispute_journal_reason` | S1/S2 | 生活的困顿与法律上的束缚，使地方运动得到支持。政府可以容许组织、承诺改法，或动用警察压制；每一种做法都会触及具体人群的利益。 | Hardship and restrictive laws have given a local movement support. The government may permit organisation, promise legal reform or use the police to suppress it. Each choice affects particular interests. | 通过：以生产、公共事务或利益冲突说明国家面对的问题，未列开发步骤。 |
| `nesnd_small_dispute_status` | S4 | 地方运动正在争取支持。改革承诺只有实际改法才能兑现。 | The movement is seeking support. A promise of reform is fulfilled only by an actual change in law. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_observation_months` | S4 | 达标月数 | Qualifying Months | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_bar_desc` | S3/S4 | [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0]个月 | [JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)\|0] months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_qualified_month` | S4 | 当前建设条件满足 | Construction and operating conditions met | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_public` | S1/S3/S4 | 培养地方人才 | Train Local People | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_public_desc` | S3/S4 | 行政与产业都缺少能够承担新职责的人。政府可用一年的公共投入帮助地方培养人才。 | Administration and industry need people able to take on new duties. A year of public spending can help build those skills. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_public_tt` | S3/S4 | 按开始时的报价承担12个月每周开支；资格与税收能力暂时提高。此项投入不能中途撤销或重复开办。 | Pay the weekly quote fixed when the programme begins for 12 months. Qualifications and tax capacity receive temporary help. The programme cannot be cancelled early or duplicated. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_specialise_button` | S1/S3/S4 | 依托现有市场 | Specialise within the Present Market | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_specialise_button_desc` | S3/S4 | 商人和行会希望借现有市场扩大销路，政府将给地方经营更多余地。 | Merchants and guilds seek wider outlets within the present market, with greater room to manage local business. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_specialise_button_tt` | S3/S4 | 12个月内资格增长提高，权威减少25。市场主人改变或取得自有市场后，这项安排结束。 | For 12 months, qualifications improve and authority falls by 25. The arrangement ends if the market owner changes or the country controls its own market. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_own_market_button` | S1/S3/S4 | 筹办自有市场 | Prepare a Market of Our Own | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_own_market_button_desc` | S3/S4 | 本国可以争取市场自主，但许可本身不能代替原料、运输和销路。 | Market autonomy requires more than permission: producers still need inputs, transport and customers. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_own_market_button_tt` | S3/S4 | 选择12个月的自有市场筹备方向，不立即改变市场归属。实际自有市场后，可承担公共投入；达标产业须没有投入品短缺。 | Choose a 12-month policy without immediately changing market ownership. Public investment becomes available after actual market autonomy; qualifying industries must have no input shortages. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_retarget_button` | S1/S3/S4 | 重订地区目标 | Select New Regional Centres | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_retarget_button_desc` | S3/S4 | 失去旧地区后，政府仍可在现有国土上组织生产和公共事务。重订也意味着重新检验这项安排。 | The government may reorganise production and services within its present territory, but the new arrangement must prove itself. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_retarget_button_tt` | S3/S4 | 按当前人口最大州与其余直接州重订两区及支点，当前地区观察月数归零。24个月内不能再重订；既有奖励不重复发放。 | Select the largest state and remaining directly owned states as two regions. Current regional observation resets. Another revision is unavailable for 24 months; past rewards are not repeated. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_restore_geography_button` | S1/S3/S4 | 重建本土地理联系 | Restore the Homeland Connection | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_restore_geography_button_desc` | S3/S4 | 收复的地区可以重新纳入本土经营，但旧日成果不能代替今日的交通和公共服务。 | Recovered regions may rejoin the homeland programme, once current transport and services can support them. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_restore_geography_button_tt` | S3/S4 | 只有原定本土地理组重新满足人口与支点条件时，才重订目标并重新观察；同样受24个月间隔限制。 | Only valid original homeland groups and centres can be restored. Regional observation restarts, with the same 24-month interval. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_order_button` | S1/S3/S4 | 经营自主后的秩序 | Build a Sustainable Political Order | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_order_button_desc` | S3/S4 | 政府将以实际法律、市场关系和防御安排维持地方的建设成果。区域国家也可以选择保留高度自主的宗属关系。 | The government will sustain its achievements through actual laws, market ties and defence. Regional countries may choose to retain a highly autonomous subject relationship. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_order_button_tt` | S3/S4 | 选择与当前主权事实相符的目标，在120个月内累计24个达标月。主权分支变化后须重新观察；共同奖励一生只发一次。 | Choose the objective matching current sovereignty and accumulate 24 qualifying months within 120 months. A change of sovereignty branch restarts observation; the shared reward is granted once. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_autonomy` | S1/S3/S4 | 要求扩大自治 | Request Greater Autonomy | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_request_autonomy_desc` | S3/S4 | 地方政府希望以已有的经营能力争取更多自行处理事务的权利。 | The local government seeks more authority on the strength of its practical achievements. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_autonomy_tt` | S3/S4 | 向实际直接宗主提出请求。批准后执行原生自治提升，核对实际结果，并按原生安排减少自由渴望、订立停战。 | Ask the actual direct overlord. Approval applies the native autonomy increase, verifies the outcome, reduces liberty desire and establishes a truce. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_independence` | S1/S3/S4 | 商谈和平独立 | Negotiate Peaceful Independence | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_request_independence_desc` | S3/S4 | 本国希望由自己承担内外事务，也必须使宗主相信放手已有现实依据。 | The country seeks responsibility for its own affairs and must give the overlord practical grounds to agree. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_independence_tt` | S3/S4 | 向实际直接宗主请求和平独立。只有实际独立才算成功；拒绝后仍可依原生外交规则争取自主。 | Ask the actual direct overlord for peaceful independence. Success requires actual independence; native diplomatic options remain available after refusal. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_market` | S1/S3/S4 | 请求自有市场 | Request Market Autonomy | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_request_market_desc` | S3/S4 | 市场自主将把更多供需与运输责任交给本国，政府须争取当前市场主人的同意。 | Controlling the market brings responsibility for supply and transport and requires the present market owner's agreement. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_market_tt` | S3/S4 | 向实际市场主人请求原生自有市场 pact。核对真实市场归属；pact已生效但市场尚未重算时，最多等候30日。 | Request the native market-autonomy pact from the actual market owner. Verify real ownership; if the pact exists but the market has not recalculated, allow at most 30 days. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_fra` | S3/S5 | 与$FRA$商谈防御协定 | Discuss Defence with $FRA$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_fra_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_fra_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_gbr` | S3/S5 | 与$GBR$商谈防御协定 | Discuss Defence with $GBR$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_gbr_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_gbr_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_usm` | S3/S5 | 与$USM$商谈防御协定 | Discuss Defence with $USM$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_usm_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_usm_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_mug` | S3/S5 | 与$MUG$商谈防御协定 | Discuss Defence with $MUG$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_mug_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_mug_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_phi` | S3/S5 | 与$PHI$商谈防御协定 | Discuss Defence with $PHI$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_phi_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_phi_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_dei` | S3/S5 | 与$DEI$商谈防御协定 | Discuss Defence with $DEI$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_dei_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_dei_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_yn1` | S3/S5 | 与$YN1$商谈防御协定 | Discuss Defence with $YN1$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_yn1_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_yn1_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_bur` | S3/S5 | 与$BUR$商谈防御协定 | Discuss Defence with $BUR$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_bur_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_bur_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_sia` | S3/S5 | 与$SIA$商谈防御协定 | Discuss Defence with $SIA$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_sia_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_sia_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_dai` | S3/S5 | 与$DAI$商谈防御协定 | Discuss Defence with $DAI$ | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_dai_desc` | S3/S4 | 共同防御取决于双方实际独立与生效条约。 | Mutual defence requires two independent countries and an effective treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_dai_tt` | S3/S4 | 向对方提出五年防御条约请求；批准且条款实际生效后才算达成。 | Propose a five-year defensive treaty. It counts only after approval and actual entry into force. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_neighbour` | S3/S5 | 与邻邦商谈防御 | Seek a Neighbour's Protection | 通过：行动名称复用既有国家译名；实际独立及生效条款另由条件核对。 |
| `nesnd_small_defence_neighbour_desc` | S3/S4 | 先选关系最好的合格邻邦，再决定是否正式提出防御条约。 | Review the eligible neighbour with the best relations before making a formal proposal. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_defence_neighbour_tt` | S3/S4 | 显示合格邻邦的名称供确认。关系相同时优先选择GDP较高者。 | Review the selected neighbour before sending. Equal relations favour the country with higher GDP. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_request_defence_tt` | S3/S4 | 正式提出五年防御条约请求。 | Send the proposal for a five-year defensive treaty. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_states.continue` | S1/S3/S4 | 事情还要继续。 | The work continues. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.2.t` | S1/S2 | 生计渐有根基 | A Firmer Livelihood | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.2.d` | S1/S2 | 农户与雇工已经在本国的生产中得到较为稳定的出路。政府可以从这样的经营中征收收入、培养人才，地方的发展也因此有了继续下去的条件。 | Production has provided a steadier livelihood for farmers and workers. These activities support revenue and skills, giving local development firmer foundations. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.3.t` | S1/S2 | 地方事务有人承担 | People to Govern | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.3.d` | S1/S2 | 行政与教育已能承担更多地方事务。新的职业和知识逐渐进入社会，政府也有了扩大自主的现实基础。如何使用这些能力，仍取决于它对国内利益和对外关系的选择。 | Administration and education can now shoulder more local responsibilities. New occupations and knowledge give the government a practical basis for greater autonomy; how it uses them remains a political choice. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.4.t` | S1/S2 | 市场关系改变 | A Change in Market Relations | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.4.d` | S1/S2 | 原市场主人已不再主持本国的市场，商人与行会据此获得的临时经营安排随之结束。现有产业仍在本地，今后的供需和运输须按新的市场关系调整。 | The former owner no longer directs the country's market. The temporary arrangement with merchants and guilds has ended. Existing industries remain, while supply and transport must adapt to the new market relationship. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.5.t` | S1/S2 | 秩序仍待建立 | An Unfinished Order | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.5.d` | S1/S2 | 多年过去，法律、市场和防御还未能共同支撑原定安排。政府可以在条件改善后重新经营这项事业，已有的产业、学校与法律并不因这一挫折消失。 | Years have passed without laws, markets and defence jointly sustaining the intended arrangement. The government may try again when conditions improve. Existing industries, schools and laws remain. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.6.t` | S1/S2 | 能够维持的秩序 | An Order We Can Sustain | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.6.d` | S1/S2 | 本国以实际法律、生产和对外安排维持了地方秩序。这些关系仍可能受到战争、市场变动与国内政治的冲击；眼前的成果使政府有了应对它们的能力。 | Actual laws, production and external arrangements have sustained local order. War, changing markets and domestic politics may still test these relationships; the country now has stronger means to respond. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.11.t` | S1/S2 | 改革承诺兑现 | A Promise Fulfilled | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.11.d` | S1/S2 | 政府承诺的法律改革已经实施。获益的人群有理由相信自己的要求能够得到回应，原有利益的持有者则要面对新的分配。地方争议由此进入了另一个阶段。 | The promised reform has become law. Its beneficiaries have reason to believe that their demands can be answered, while established interests face a new distribution of benefits. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.12.t` | S1/S2 | 落空的承诺 | A Broken Promise | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.12.d` | S1/S2 | 许诺的期限已经过去，原有法律仍约束着提出要求的人群。政府未能以实际改革回答他们，失望正在加深地方的不满。 | The promised term has passed, and the old law still binds those who sought change. The government's failure to act has deepened local resentment. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.10.t` | S1/S2 | 地方组织的要求 | Demands from Local Organisations | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.10.land` | S1/S2 | 地租与债役压着地方农户和雇工，主张土地改革的人正在组织他们。人们要求改变土地与劳动的支配关系，政府则必须决定如何回应已有运动。 | Rents and debt bondage weigh on local farmers and labourers. Land reformers are organising them to change who controls land and work. The government must decide how to respond to this existing movement. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.10.labor` | S1/S2 | 雇工的生活困顿使劳动运动得到支持。工资、工时和工作中的保障成为争议的中心，政府对组织与立法的态度，将影响劳资双方的力量。 | Hardship among labourers has strengthened the labour movement. Wages, hours and protection at work have become matters of dispute. The government's approach to organisation and law will affect the balance between workers and employers. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.10.representation` | S1/S2 | 现有的自由派或激进派运动正在争取地方支持。种姓和政治权利的限制使一些居民难以参与公共事务，运动要求改变现状，政府也将面对权力重新分配的压力。 | An existing liberal or radical movement is seeking local support. Caste or political restrictions prevent residents from participating in public affairs. Demands for change place the distribution of power under pressure. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.10.organise` | S1/S3/S4 | 允许地方组织。 | Permit local organisation. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.10.organise_tt` | S3/S4 | 12个月内提高相关原生运动的支持权重，权威减少25；相关人群一次增加1%激进派。有适格的实际支持人物时，给予其12个月声望帮助。 | For 12 months, increase the relevant native movement's support weight and reduce authority by 25. Move 1% of the affected pops towards radicalism once. An eligible living supporter, if present, receives temporary popularity. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_states.10.promise_land` | S1/S3 | 承诺改变土地制度。 | Promise land reform. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_land_tt` | S1/S3 | 在24个月内以原生立法改变土地制度，实际实行自耕农、土地商品化或集体农业。期间相关利益集团认可提高2；兑现或失约后有一次有限的人群反应。 | Within 24 months, change land tenure through native law enactment to peasant proprietorship, commercialised agriculture or collectivised agriculture. The relevant interest group receives +2 approval in the meantime; fulfilment or failure produces a limited, one-time response. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_debt` | S1/S3 | 承诺结束债役。 | Promise to end debt bondage. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_debt_tt` | S1/S3 | 在24个月内以原生立法改变奴隶制，实际实行禁止奴隶制。期间相关利益集团认可提高2；兑现或失约后有一次有限的人群反应。 | Within 24 months, change slavery through native law enactment to slavery banned. The relevant interest group receives +2 approval in the meantime; fulfilment or failure produces a limited, one-time response. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_labor` | S1/S3 | 承诺确立劳动保障。 | Promise protection at work. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_labor_tt` | S1/S3 | 在24个月内以原生立法改变劳动权利，实际实行监管机构或工人保护。期间相关利益集团认可提高2；兑现或失约后有一次有限的人群反应。 | Within 24 months, change labour rights through native law enactment to regulatory bodies or worker protections. The relevant interest group receives +2 approval in the meantime; fulfilment or failure produces a limited, one-time response. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_caste` | S1/S3 | 承诺解除种姓限制。 | Promise to remove caste restrictions. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_caste_tt` | S1/S3 | 在24个月内以原生立法改变种姓制度，实际实行不执行印度种姓或平权措施。期间相关利益集团认可提高2；兑现或失约后有一次有限的人群反应。 | Within 24 months, change caste through native law enactment to caste not enforced or affirmative action. The relevant interest group receives +2 approval in the meantime; fulfilment or failure produces a limited, one-time response. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_representation` | S1/S3 | 承诺扩大政治代表。 | Promise wider representation. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.promise_representation_tt` | S1/S3 | 在24个月内以原生立法改变权力分配，实际实行财产选举、资格选举或普选。期间相关利益集团认可提高2；兑现或失约后有一次有限的人群反应。 | Within 24 months, change the distribution of power through native law enactment to wealth voting, census suffrage or universal suffrage. The relevant interest group receives +2 approval in the meantime; fulfilment or failure produces a limited, one-time response. | 通过：承诺明确法组及原生立法结果，未把承诺写成即刻改法。 |
| `nesnd_small_states.10.suppress` | S1/S3/S4 | 动用警察压制组织。 | Use the police to suppress organisation. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.10.suppress_tt` | S3/S4 | 12个月内降低相关原生运动的支持权重，权威减少50；相关人群一次增加2%激进派。 | For 12 months, reduce the relevant native movement's support weight and reduce authority by 50. Move 2% of the affected pops towards radicalism once. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_states.20.t` | S1/S2 | 地方政府的提议 | A Proposal from the Local Government | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.20.autonomy` | S1/S3/S4 | [SCOPE.sCountry('canon_sender').GetName]希望以地方经营和治理的成果争取更大的自治。接受提议将实际提升其原生自主等级，并按现有宗属规则调整关系。 | [SCOPE.sCountry('canon_sender').GetName] seeks greater autonomy on the strength of its local economy and government. Acceptance will apply the native autonomy increase and adjust relations under the existing subject rules. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.20.independence` | S1/S3/S4 | [SCOPE.sCountry('canon_sender').GetName]请求以和平方式结束直接宗属关系，由自己承担内外事务。放弃宗主权将改变双方的权利与义务，也可使一场冲突止于谈判。 | [SCOPE.sCountry('canon_sender').GetName] asks to end direct subjection peacefully and assume responsibility for its own affairs. Relinquishing overlordship will change both countries' rights and obligations and may settle the dispute through negotiation. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.20.market` | S1/S3/S4 | [SCOPE.sCountry('canon_sender').GetName]请求自行主持市场。政府将通过原生市场安排授予这一权利；当地生产能否得到原料和销路，仍取决于之后的经营。 | [SCOPE.sCountry('canon_sender').GetName] asks to control its own market. Approval grants that right through the native market arrangement. Local industries will still need to obtain inputs and find customers. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.20.defence` | S1/S3/S4 | [SCOPE.sCountry('canon_sender').GetName]提出缔结防御条约。双方将承担实际条款规定的义务，既有生产与外交联系也可能因此受到战争的考验。 | [SCOPE.sCountry('canon_sender').GetName] proposes a defensive treaty. Both countries will assume the obligations of its effective terms, and war may put their economic and diplomatic ties to the test. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_accept_tt` | S3/S4 | 执行提议对应的自治、独立、市场或防御安排，并核对实际结果。 | Apply the proposed autonomy, independence, market or defence arrangement and verify its actual result. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_refuse_tt` | S3/S4 | 拒绝本次提议。自治请求被拒时，按原生规则产生相关外交催化剂。 | Refuse this proposal. Refusing an autonomy request produces the native diplomatic catalysts. | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_states.21.t` | S1/S2 | 邻邦的选择 | Choosing a Neighbour | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.21.d` | S1/S2 | [SCOPE.sCountry('small_receiver').GetName]是当前关系最好的合格邻邦。政府可以正式提出防御协定，也可以暂缓此事。 | [SCOPE.sCountry('small_receiver').GetName] is the eligible neighbour with the best current relations. The government may send a formal defensive proposal or leave the matter for now. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.21.a` | S1/S3/S4 | 向他们正式提出协定。 | Send the formal proposal. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_states.21.b` | S1/S3/S4 | 暂缓此事。 | Leave it for now. | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_livelihood` | S1/S3/S4 | 稳定的地方生计 | Steadier Local Livelihoods | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_learning` | S1/S3/S4 | 地方学识的传播 | Local Exchange of Knowledge | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_order` | S1/S3/S4 | 地方秩序的根基 | Foundations of Local Order | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_public_investment` | S1/S3/S4 | 地方公共投入 | Local Public Spending | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_public_services` | S1/S3/S4 | 培养地方人才 | Training Local People | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_specialised_market` | S1/S3/S4 | 现有市场专业化 | Specialisation in the Present Market | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_own_market` | S1/S3/S4 | 自有市场筹备 | Preparing Market Autonomy | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_local_spokesperson` | S1/S3/S4 | 地方运动的代言者 | A Local Movement's Spokesperson | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_reform_approval` | S1/S3/S4 | 改革承诺 | A Promise of Reform | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_organise_land` | S1/S3/S4 | 土地改革组织 | Land Reform Organisation | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_organise_labor` | S1/S3/S4 | 劳动组织 | Labour Organisation | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_organise_representation` | S1/S3/S4 | 争取公民权利 | Organising for Civic Rights | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_suppress_land` | S1/S3/S4 | 压制土地改革组织 | Suppressing Land Reform Organisations | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_suppress_labor` | S1/S3/S4 | 压制劳动组织 | Suppressing Labour Organisations | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_suppress_representation` | S1/S3/S4 | 压制公民权利运动 | Suppressing Civic Rights Organisations | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_regional_status` | S4 | 地区支点：[JournalEntry.GetCountry.MakeScope.Var('nesnd_small_anchor_one').GetState.GetName]、[JournalEntry.GetCountry.MakeScope.Var('nesnd_small_anchor_two').GetState.GetName]。<br>市场：[JournalEntry.GetCountry.GetMarket.GetName]。<br>[JournalEntry.GetCountry.TryGetOverlordTooltipEntry]<br>两地区达到80%市场接入的州内人口占比分别为[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_group_one_transport')\|%1]、[JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_group_two_transport')\|%1]。 | Regional centres: [JournalEntry.GetCountry.MakeScope.Var('nesnd_small_anchor_one').GetState.GetName] and [JournalEntry.GetCountry.MakeScope.Var('nesnd_small_anchor_two').GetState.GetName].<br>Market: [JournalEntry.GetCountry.GetMarket.GetName].<br>[JournalEntry.GetCountry.TryGetOverlordTooltipEntry]<br>Population in states with at least 80% market access: [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_group_one_transport')\|%1] and [JournalEntry.GetCountry.MakeScope.ScriptValue('nesnd_small_group_two_transport')\|%1] in the two regions. | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_no_regional_crisis_tt` | S3/S4 | 本国实际持有的地区没有尚在进行的印度地方案件 | No active Indian regional case affects a directly owned state | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_regional_targets_tt` | S3/S4 | 两个登记地区各有至少10万人及分母人口的5%，实际支点仍属本国且各达分母人口的5% | Both selected regions retain at least 100,000 people and 5% of the relevant population; their directly owned centres each retain 5% | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_governance_completed_tt` | S3/S4 | 已完成当前规模所需的地方治理建设 | The local government programme required by the country's current structure is complete | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_specialisation_tt` | S3/S4 | 两个地区各有一种至少2级的合格专业生产，分属同一产业类别，且两地所用建筑类型不同 | Each region has a qualifying production type of at least two levels, within the same industrial class but using different building types | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_population` | S4 | 直接持有州人口 | Population in directly owned states | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_populated_states` | S4 | 直接持有的有人州数 | Directly owned populated states | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_scale` | S1/S3/S4 | 人口规模所需的基础等级 | Base levels required by population | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_admin_target` | S1/S3/S4 | 所需行政等级 | Required administration levels | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_army_target` | S1/S3/S4 | 自卫所需陆军规模 | Army size required for self-defence | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_job_coverage` | S4 | 失业率不高于10%的州内人口占比 | Population in states with unemployment at or below 10% | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_transport` | S4 | 市场接入达80%的州内人口占比 | Population in states with at least 80% market access | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_production` | S4 | 有就业、盈利且未补贴的生产等级 | Employed, profitable and unsubsidised production levels | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_clean_production` | S4 | 没有投入品短缺的合格生产等级 | Qualifying production levels without input shortages | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_administration` | S1/S3/S4 | 本国行政建筑等级 | Domestic administration levels | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_barracks` | S1/S3/S4 | 本国军营等级 | Domestic barracks levels | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_industry_classes` | S1/S3/S4 | 至少有2级合格生产的产业类别数 | Industrial classes with at least two qualifying levels | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_region_one_production` | S4 | 第一地区合格生产等级 | Qualifying production levels in the first region | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_region_two_production` | S4 | 第二地区合格生产等级 | Qualifying production levels in the second region | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_group_one_transport` | S4 | 第一地区市场接入达80%的州内人口占比 | First-region population in states with at least 80% market access | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_group_two_transport` | S4 | 第二地区市场接入达80%的州内人口占比 | Second-region population in states with at least 80% market access | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_weekly_quote` | S1/S3/S4 | 每周公共投入报价 | Weekly public-spending quote | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_army_ratio` | S1/S3/S4 | 相对实际宗主的陆军规模 | Army size relative to the actual overlord | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_gdp_ratio` | S1/S3/S4 | 相对实际宗主的GDP | GDP relative to the actual overlord | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_pressure_coverage` | S4 | 生活困顿或动乱州内人口占比 | Population in states experiencing hardship or turmoil | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_generic_anchor_min` | S1/S3/S4 | 按当前全国人口所需的支点人口 | Centre population required by the current national population | 通过：短名称/选项承担明确行动或状态，不附重复结论、不虚构效果。 |
| `nesnd_small_native_one_pop` | S4 | 第一本土地理组人口 | First homeland group's population | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_native_two_pop` | S4 | 第二本土地理组人口 | Second homeland group's population | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_native_one_share` | S4 | 第一本土地理组人口占比 | First homeland group's population share | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_native_two_share` | S4 | 第二本土地理组人口占比 | Second homeland group's population share | 通过：短标签或受守卫的实际读数；人口覆盖、就业/利润与主权事实分别表述。 |
| `nesnd_small_states.2.far_south` | S1/S2 | 澳洲的加工与人口中心已经同新西兰的地方生产保持了有效联系。港口能够雇用工人，货物也能进入市场。远南可以从这些已有的产业继续成长，政府也将从中获得维持地方事务的收入。 | Australia's population and processing centres now maintain effective links with local production in New Zealand. Working ports carry goods to market. These industries support the Far South's growth and provide revenue for local services. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.2.burma` | S1/S2 | $STATE_MANDALAY$所在的上游与$STATE_PEGU$下游已有能够经营的生产，并通过现有交通参与市场。农户与商人的收入改善了地方生计，也使政府有余力考虑上下游的行政与教育。 | Production in the upper country around $STATE_MANDALAY$ and the lower country at $STATE_PEGU$ now reaches the market through existing transport. Better earnings for farmers and merchants support livelihoods and give the government more room to provide administration and education. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.2.siam` | S1/S2 | 曼谷之外的生产已经同人口与财政中心保持了联系。现有军队仍要从全国收入中获得供养，地方经营的成果也将检验政府如何分配行政与教育的资源。 | Production outside Bangkok is now linked to the population and fiscal centre. The existing army still draws on national revenue, while local development raises the question of how administration and education should be distributed. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.6.far_south` | S1/S2 | 澳洲与新西兰的生产、海运和公共事务已能共同支撑远南的发展。政府在现行主权关系下维持着本国法律与实际地区伙伴，两个地区也都有了继续经营和培养人才的条件。 | Production, shipping and public services in Australia and New Zealand can now sustain the Far South together. Under its present sovereignty arrangement, the government maintains its laws and actual regional partners, while both regions can continue developing industries and skills. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.6.burma` | S1/S2 | 上游与$STATE_PEGU$下游的经营和公共事务已经得到维持，本国也有了实际法律、市场与地区伙伴作为依靠。缅甸的政府可以据此处理对外关系，继续安排生产与公共收入的用途。 | Production and services in the upper country and $STATE_PEGU$ have been sustained, supported by actual laws, markets and regional partners. Burma's government can conduct its external affairs on this basis and continue deciding how production and public revenue should serve the country. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_states.6.siam` | S1/S2 | 曼谷与地方的生产、公共事务和防御已经能够共同维持。军队的供养仍是一项真实负担，政府可以在现行主权关系和地区合作中继续调整军政与民生的分配。 | Production, public services and defence in Bangkok and the regions can now be sustained together. Army upkeep remains a real cost, and the government can continue balancing military and civilian needs through its present sovereignty arrangement and regional relationships. | 通过：以实际行动者、利益与已发生条件叙述；不造人物或保证未来产出。 |
| `nesnd_small_order_available_tt` | S3/S4 | 当前没有正在观察的自主秩序目标，也不在重开间隔内 | No political-order observation is active or awaiting its retry interval | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |
| `nesnd_small_retarget_ready_tt` | S3/S4 | 最近24个月内没有重订地区目标 | Regional targets have not been revised within the last 24 months | 通过：承担必要行动/条件/期限说明；数值对应冻结脚本，不泄漏内部期次字段。 |

## 本轮引用而未改写的有效文本

C1 repair4双语文件 `zzzzzzzzzzzz_nesnd_batch_c_l_*.yml` 保持原SHA与覆盖顺序。逐项对读以下实际引用：`nesnd_canon_no_pending_reply`、`nesnd_canon_diplomatic_cooldown`、`nesnd_canon_request_5_desc`、`nesnd_canon_small_fra/gbr/usm/mug/hus`、`nesnd_small_state_capital`、`nesnd_canon_diplomacy.1.d/a/b/investment`、`.2.t/d/a`、`.3.t/d/a`。判定通过：等待/冷却指向真实共用事务；投资明确“协定给予投资的权利，企业是否动工仍取决于实际经营”；成功通知只在B2真实后验成功时触发，拒绝/取消/创建失败用未成协议文本；无C1法国政治信用或德意志同盟正文被借作B2自治正文。

旧印度request4/7的名称、desc与通用请求提示仍由旧有效覆盖层显示，原metadata未改。真实土邦使用B2实际批准效果，非B2帝国仍走旧协议；因此未把两者写成不同虚构党派路线。原生law/building/IG/type名称直接复用当前GAME/既有MOD词条，不重译。

## 结论与边界

本轮新文本186对均给出编辑结论；上列发现已返工。BOM/header、键集合、覆盖完整性、动态引用及实际UI仍交独立测试，不能拿本表替代。技能无新永久规则；旧样本和失败稿保留于本报告及实现过程记录，未改作者原文文件。
