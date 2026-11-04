# 非中国国家玩家文案审读与候选计划

状态：**候选提案，尚未应用M；不是最终审稿通过，也不是引擎验收。** 实际模型 `gpt-6-astra / high`，来自父代理明确委派，满足用户“至少Astra medium”要求。主代理负责最终逐条审稿；不合格条目由主代理自己重写后复核。

## 范围与已产出

- 范围清单 `non_chinese_scope_inventory.json` 列出2618个中英条目，覆盖埃及、普鲁士、奥地利、美国、墨西哥/安第斯/汗国、奥斯曼、印度/土邦、意大利、日本及南洋共通文本。每条给出文件、行号、当前值与候选/保留待终审状态；没有把仅列入清单的全部条目冒称最终合格。
- 本轮候选为124键、246个语言条目，逐条 `key/lang/old/new/reason/source/checks` 见 `proposed-loc-edits.json`。以明确key清单和最终有效覆盖层为准。
- 本代理没有编辑M、候选MOD、玩法脚本、数字、存档或技能。待root指定新C后，按旧值与文件SHA校验再由主代理统一应用。

## 原始样本和本轮写法

作者样本取自不可变 `backups/pre-update-20261030T233944Z/mod`，与技能指定 `f18b6c4` 原始版本一致的来源入口；本轮实际读样本逐文件SHA与行号在 `non_chinese_source_samples.json`，没有拿现行AI稿充当作者风格。

- 法国 `je_ce_unstable_imperium_reason` 具体写拿破仑三世、工业支出与执政利益，说明作者允许长句与明确政治判断；候选不把正文压成中性规格表。
- 法国支持/反对王朝按钮各有政治立场；候选选项与按钮应讲所要采取的行动，不讲“原生接口”“核对结果”。
- `flavorCNE.3.d` 写劳动力离开宗族、进入城市的因果，`flavorCNE.4.d` 写阶层利益与执行阻力；不能只以“新秩序/真实成果”代替具体社会过程。
- 原版1.13.11 `content_1` 的德意志统一、奥斯曼教育与埃及保护国中英条目用于核异国称谓、行动和英语句法。原版埃及使用有scope的 `GetPrimaryRoleTitle`；本轮无需添加新函数，通用段落直接使用政府。

## 原稿—候选—裁定示例

| 键/类别 | 原稿问题 | 候选处理 | 状态 |
|---|---|---|---|
| `nesnd_egypt_investor_desc` / 按钮 | 夹入印度1825年权益与南朝附属资格的实现解释 | 整段删除，只写选择投资伙伴与建设教育合作 | 按用户要求；待root终审 |
| 埃及正文/事件 | 朝廷、王朝常驻用于不限定政体的EGY内容，且结尾反复议论自主 | 政府承担选择与后果；保留必要历史背景 | 候选 |
| `nesnd_prussian_rhine_reason` / JE | “真实协约”“纸上的宣称不会自行变边界”为代码辩解 | 直接写共同防卫、法莱压力、统一及阿尔萨斯外交战争 | 候选 |
| `nesnd_small_states.20.autonomy` / 事件 | “提升原生自主等级”破坏叙事视角 | 请求放宽宗主限制、提高自治权 | 候选 |
| 汗国状态/事件 | “两条干涉单独结算”“旧记录补发军队” | 描述哪个国家仍在干涉、建国领土不足或干涉结束 | 需root核触发分支 |
| 意大利shared tooltip | “原持续期/原支付期”是修复说明 | “总期限/拨款期共”，保留数值 | 需root确认显示时点 |
| `nesnd_jp_politics_reason` / 英译 | 现有英文漏掉中文作者段的吴主、朝鲜与票号 | 仅补英文，中文保持不动 | 需root核“东勘藩土”译法 |

## 分组应用清单

| 文件 | 条目数 |
|---|---:|
| `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_batch_c_l_simp_chinese.yml` | 27 |
| `localization/english/replace/zzzzzzzzzzzz_nesnd_batch_c_l_english.yml` | 26 |
| `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_simp_chinese.yml` | 8 |
| `localization/english/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_english.yml` | 8 |
| `localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_simp_chinese.yml` | 23 |
| `localization/english/replace/zzzzzzzzzzzz_nesnd_a2_native_americas_l_english.yml` | 23 |
| `localization/simp_chinese/replace/zzzzzzzzzzzzz_nesnd_small_states_l_simp_chinese.yml` | 21 |
| `localization/english/replace/zzzzzzzzzzzzz_nesnd_small_states_l_english.yml` | 21 |
| `localization/simp_chinese/replace/zzzzzzzzzzzzzz_nesnd_india_l_simp_chinese.yml` | 14 |
| `localization/english/replace/zzzzzzzzzzzzzz_nesnd_india_l_english.yml` | 14 |
| `localization/simp_chinese/replace/nesnd_civic_routes_l_simp_chinese.yml` | 27 |
| `localization/english/replace/nesnd_civic_routes_l_english.yml` | 27 |
| `localization/simp_chinese/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_simp_chinese.yml` | 3 |
| `localization/english/replace/zzzzzzzzzzzzzzzzzzz_nesnd_regional_l_english.yml` | 3 |
| `localization/english/replace/zzzzzz_nesnd_jp_development_l_english.yml` | 1 |

## 应用与检查方法

1. 根目录与当前用户作者改稿优先。候选key虽均未见于最初作者基准，仍不能据此推定后续每一处改稿都是AI；主代理用本轮交接及Git来源确认再应用。已知日本中文作者丰臣段不改。
2. 在新C中逐条核原值、文件SHA和最终有效覆盖键。命名规范化若已改变文件路径，应通过key和原值定位，不能依靠本报告中的长z文件名盲写；有重复定义时逐项核覆盖顺序。
3. JSON逐条保留旧/新文。中文和英文按同一个事实与行动重写，保持数字、概念、scope和token；不逐逗号硬译。原本已经是合格叙事的日本工业/朝鲜等段落不因“朝廷”等关键词机械替换。
4. 当前检查：所有候选动态token顺序一致；数值token仅埃及投资按钮中英1825移除，属于用户明确要求，1825背景仍保留在独立正文；没有未转义双引号。无其他数字增删。
5. 对脚本接口不做新增假设。埃及按钮possible已有签约方资格；该条件不靠正文重复保障。A2状态、独立干涉与印度来函按既有调用链核语义。最终审稿须注意“国家独立/政府存活/战争结束/赢得战争”不能相互替代。
6. shared tooltip显示总期限，不承诺每次查看重新开始期限。不得把叙事里的拨款、学校或军队写成额外实装奖励。
7. root先逐条判通过/返工；返工由root亲自重写再复核，不让机械替词检验替代编辑判断。全部通过才写C；随后做YAML BOM/header、重复键、两语言键集合、token与未改玩法字节核验。没有打开游戏，只能报告文本/源码检查结果。

## 每个候选键及本轮理由

以下每行对应JSON内旧文与候选中英全文；最终判定栏保持待root复核，不能把此列表当最终批准。

| 键 | 理由 |
|---|---|
| `nesnd_egypt_independence_reason` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt_investment_accounts` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt_investment_accounts_reason` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt_dependence_result` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt_investor_desc` | 按用户明确改稿整段删除印度1825投资权与南朝附属资格解释；按钮只说明选择投资伙伴的行动，资格由既有possible条件负责。 |
| `nesnd_egypt_unsecured_independence` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.1.d` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.2.d` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.3.d` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.3.a` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.4.t` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.4.d` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.4.a` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.3.unworkable` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_egypt.6.d` | 埃及文本去掉朝廷和无条件王朝称谓，使用政府；保留1825背景、三十年与独立/保护关系事实，删除反复抽象总结。 |
| `nesnd_prussian_coalition_reason` | 删去真实协约、纸上宣称等为实现正确性辩解的语言；保留联盟、军备、统一和阿尔萨斯争端。 |
| `nesnd_prussian_rhine_reason` | 删去真实协约、纸上宣称等为实现正确性辩解的语言；保留联盟、军备、统一和阿尔萨斯争端。 |
| `nesnd_prussian_subordinate_status` | 删去真实协约、纸上宣称等为实现正确性辩解的语言；保留联盟、军备、统一和阿尔萨斯争端。 |
| `nesnd_prussian_rhine_paused` | 删去真实协约、纸上宣称等为实现正确性辩解的语言；保留联盟、军备、统一和阿尔萨斯争端。 |
| `nesnd_austrian_italy_reason` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_austrian_committed_status` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_usa_continental_reason` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_usa_war_status` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_europe_america.1.d` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_europe_america.2.d` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_europe_america.4.d` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_europe_america.8.d` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_ottoman_unity_reason` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_unity_fractured` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_unity_calm` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_recovery_reason` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_recovery_success_status` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_recovery_failed_status` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_reform_army_desc` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_ottoman_claim_desc` | 以国家、政府、军官与地方利益说明行动；避免无条件套用朝廷或现任苏丹，不新增动态称号调用。 |
| `nesnd_native_suppress_tt` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_restoration_existing_court_status` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_native_restoration_war_reason` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_american_restoration.1.d` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_american_restoration.5.t` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_american_restoration.5.d` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_american_restoration.6.d` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_emergence_reason` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_survival_reason` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_usa_status` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_hus_status` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_survival_status` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_legacy_status` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_intervention_status` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_khanate_destroyed_tt` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_native_khanate.2.d` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_native_khanate.2.one` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_native_khanate.2.none` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_native_khanate.3.d` | 把单独结算、旧记录补发、实际执行等实现解释改成当前战争、领土与政治局面；保留迁徙/激进化数值、各国干涉独立结束的区别。 |
| `nesnd_small_livelihood_journal_reason` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_governance_journal_reason` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_regional_economy_journal_reason` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_order_journal_reason` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_order_button_desc` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.6.far_south` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.6.burma` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.6.siam` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.6.d` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.20.autonomy` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_states.20.market` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_accept_tt` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_small_refuse_tt` | 南洋与土邦使用政府、学校、税收和外交叙事；去除原生等级、核对结果等开发术语，保留自治/独立/市场/防御的不同承诺。 |
| `nesnd_india_reform` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_reform_status` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_dynasty_legitimacy` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_priority_desc` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_industry_reason` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_foreign_reason` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d1` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d2` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d3` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d4` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d5` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d6` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_india_diplomacy.1.d7` | 来函分别点明教育、工业、军训、自治、防御、合并或独立的请求与利害，删除逐项重复的责任解释；通用改革文本避免固定宫廷称谓。 |
| `nesnd_c2_italy_agenda_reason` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_civic_routes.11.d` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_civic_routes.13.d` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_c2_italy_direction_french_republic_desc` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_c2_italy_direction_autonomous_concord_desc` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_c2_italy_direction_southern_monarchy_desc` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_c2_italy_direction_plural_compact_desc` | 意大利合作围绕拨款、学校、军费和各邦同意说明；去掉实际执行/并非自动等开发辩解，不声称选方针自动改政体或吞并。 |
| `nesnd_rg_technical_schools` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_rg_provincial_schools` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_regional.5.d` | 删除实现说明、无效重复或空泛结尾；按实际国家与政体语境明确行动者，不改变玩法。 |
| `nesnd_italy_foundations_reason` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_italy_concord_reason` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_italy_common_budget_reason` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_construction_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_armed_forcesup_industrialistsdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_industrialistsup_landownersdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_education_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_petty_bourgeoisieup_industrialistsdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_administration_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_transport_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_rural_folkup_industrialistsdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_pasture_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_intelligentsiaup_landownersdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_trade_unionsup_landownersdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_c2_existing_politics_landownersup_industrialistsdown_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_c2_italy_common_budget_locked_quote_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_c2_italy_foundations_locked_quote_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_compact_receiver_quote_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_compact_sender_quote_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_compact_root_locked_quote_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `wg_nesnd_khanate_annex_desc` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `war_goal_wg_nesnd_khanate_annex_type_desc` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `war_goal_wg_nesnd_khanate_annex_desc` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `war_goal_wg_nesnd_khanate_annex_sway_desc` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.organise_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.promise_land_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.promise_debt_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.promise_labor_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.promise_caste_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.promise_representation_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_small_states.10.suppress_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_final_small_public_existing_tt` | 有限改写：原生→玩家行动，原持续期/原支付期→总期限/拨款期；数字和动态读数原样保留，不把总期限说成剩余期限。 |
| `nesnd_jp_politics_reason` | 中文现行丰臣段保留不动；英文补回吴主援助、朝鲜行动、明国朝廷与大阪票号，纠正现有中英漏译。 |

## 最后一次本代理返工

`nesnd_small_refuse_tt`初稿只写影响外交立场，信息过空。回读`common/scripted_effects/nesnd_small_diplomacy.txt:57–61`确认自治拒绝提高独立倾向并降低关系，已改成明确这两项后果。未新增或改变玩法数值。JSON是最终候选全文；TSV保留初稿轨迹，不用于应用。
