# C批玩家文本对读

2026-11-04；编辑阶段的人工文案判断，不是行为、Tiger、MCP或引擎测试。全部实际新键在两语言独立replace文件中；kind3/5保留接口文案，不据此宣称对应后续路线已完成。

## 可追溯作者样本

|来源|SHA256|本轮取用|
|---|---|---|
|D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml|`3432daa34986fbb931080f073251b7f6b9dbd4da29b2a94ae52dc8e8cf479f5a`|作者备份只读；同类字段样本，非当前AI文本|
|D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml|`352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844`|作者备份只读；同类字段样本，非当前AI文本|

- S1：ce_cne_events_l_simp_chinese.yml:15 / ce_cne_land_reform_reason：从真实历史矛盾进入政策过程；正文可以有完整论说，不压成核册式步骤。
- S2：同文件:69 / flavorCNE.3.d：点名利益承担者，把制度、劳动者和实际生产连接起来；不得声称脚本未实现的成果。
- S3：ce_french_empire_journals_l_simp_chinese.yml:237 / ce_french_support_dynasty_button_desc：“波拿巴的道路是……民族团结和繁荣的唯一办法。”按钮陈述政治立场，门槛/数值另由效果说明。
- S4：同文件:248 / ce_french_empire_oreleans_progress_bar_desc：只列当前读数及分母，来源明细归原生bar，不塞开发过程。

## 本轮编辑决定

|初稿问题|返工|结论|
|---|---|---|
|美国对HUS事件把行动者写成“朝廷与议会”|改为“东洲政府”，不凭空加入君主制或未核制度主体|通过|
|埃及三十年成功稿说“工场与学校的成长”已支撑独立，但父JE不要求子JE完成|改成今后的工场与学校可以继续巩固自主；既有三十年独立结果单独陈述|通过|
|埃及成功稿“30年前签下”可能与1825历史约混淆|改“维持自主的三十年”，父JE实际开启计时与1845条约到期分开|通过|
|无赞助终局容易暗示六个国家全部死亡|改“没有能够承担保护责任的投资伙伴”，覆盖主动none及已选对象消失|通过|
|英文正文直接写HUS开发tag|改原生$HUS$名称；固定作者“东洲”中文沿用|通过|
|普鲁士共同参谋利益缺少最大期限的说明|加入十年窗口、真实条件维持与暂停提示；脚本同时安排十年到期事件|通过|

投资权限与实际落厂分开；各国政治口号归行动者叙述，不作世界事实。无新引文冒署作者。六国产业名、收益/期限、三大学工场条件、联盟/防御区别和单州战争均按最终编写的代码含义陈述。中文保留连贯主语，英文按句意重写；拒绝/过期不解释程序字段。

## 全部有效文本逐项结论

|键 / 两语言行号|原文参照|候选对应行为与编辑判断|结论|
|---|---|---|---|
|`nesnd_egypt_independence` / 2|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_independence_reason` / 3|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt_with_investor_status` / 4|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_egypt_without_investor_status` / 5|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_egypt_investment_accounts` / 6|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investment_accounts_reason` / 7|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt_independence_bar` / 8|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_independence_bar_desc` / 9|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_egypt_sponsor_drain` / 10|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_foreign_drain` / 11|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_generation_passed` / 12|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_still_independent` / 13|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_dependence_reached` / 14|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_dependence_result` / 15|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_desc` / 16|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt_choose_cost` / 17|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt_investor_none` / 18|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_none_desc` / 19|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt_none_effect` / 20|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt_investor_fra` / 21|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_usm` / 22|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_sih` / 23|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_gbr` / 24|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_qe1` / 25|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investor_tur` / 26|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_investment` / 27|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_fra_industry` / 28|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_usm_industry` / 29|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_sih_industry` / 30|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_gbr_industry` / 31|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_qe1_industry` / 32|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_tur_industry` / 33|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_independent_generation` / 34|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_unsecured_independence` / 35|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_local_capability` / 36|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_1825_treaty` / 37|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`subject_type_nesnd_egypt_protectorate` / 38|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`subject_type_nesnd_egypt_protectorate_no_icon` / 39|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_protectorate` / 40|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt_protectorate_desc` / 41|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt_protectorate_pact_desc` / 42|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_egypt.1.t` / 43|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.1.d` / 44|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt.1.a` / 45|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.2.t` / 46|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.2.d` / 47|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt.2.a` / 48|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.3.t` / 49|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.3.d` / 50|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt.3.a` / 51|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.4.t` / 52|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.4.d` / 53|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt.4.a` / 54|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.5.t` / 55|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_egypt.5.d` / 56|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_egypt.5.a` / 57|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_no_pending_reply` / 58|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomatic_cooldown` / 59|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_no_french_alliance_tt` / 60|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_1_desc` / 61|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_11_desc` / 62|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_2_desc` / 63|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_3_desc` / 64|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_4_desc` / 65|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_5_desc` / 66|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_request_sent_tt` / 67|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_accept_request_tt` / 68|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_canon_diplomacy.1.t` / 69|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.1.d` / 70|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.1.alliance` / 71|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.1.defense` / 72|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.1.credit` / 73|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.1.investment` / 74|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.1.a` / 75|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.1.b` / 76|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.2.t` / 77|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.2.d` / 78|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.2.a` / 79|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.3.t` / 80|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_diplomacy.3.d` / 81|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_canon_diplomacy.3.a` / 82|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_prussian_coalition` / 83|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_prussian_coalition_reason` / 84|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_prussian_coalition_status` / 85|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_prussian_subordinate_status` / 86|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_prussian_rhine` / 87|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_prussian_rhine_reason` / 88|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_prussian_rhine_resolved_tt` / 89|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_prussian_rhine_cooperating` / 90|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_prussian_rhine_paused` / 91|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_prussian_joint_staff` / 92|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_prussian_rhine_settlement` / 93|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austrian_italy` / 94|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austrian_italy_reason` / 95|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_austrian_waiting_status` / 96|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_austrian_dispute_status` / 97|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_austrian_committed_status` / 98|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_austria_intervene` / 99|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austria_intervene_desc` / 100|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austria_intervene_tt` / 101|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austria_acknowledge` / 102|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austria_acknowledge_desc` / 103|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austria_acknowledge_tt` / 104|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austrian_cooldown_tt` / 105|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austrian_current_dispute_tt` / 106|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_austrian_italian_commitment` / 107|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austrian_concession` / 108|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austrian_italian_defeat` / 109|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_austrian_italian_influence` / 110|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_continental` / 111|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_continental_reason` / 112|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_usa_border_selected_status` / 113|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_usa_no_border_status` / 114|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_usa_civil_war_status` / 115|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_usa_war_status` / 116|S4|只呈现当前状态/读数；动态对象由对应first_valid条件保护，未叙述实现过程。|通过（编辑）|
|`nesnd_usa_european_treaty_tt` / 117|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_claim_cooldown_tt` / 118|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_border_cooldown_tt` / 119|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_civil_war_pause_tt` / 120|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_no_pending_war_tt` / 121|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_next_border` / 122|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_next_border_desc` / 123|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_next_border_tt` / 124|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_claim_border` / 125|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_claim_border_desc` / 126|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_claim_border_tt` / 127|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_press_west` / 128|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_press_west_desc` / 129|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_press_west_tt` / 130|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_usa_hus_confrontation` / 131|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_european_capital` / 132|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_continental_army` / 133|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_usa_frontier_claim` / 134|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_italy_french_credit` / 135|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_small_state_capital` / 136|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.1.t` / 137|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.1.d` / 138|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.1.a` / 139|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.2.t` / 140|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.2.d` / 141|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.2.a` / 142|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.3.t` / 143|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.3.d` / 144|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.3.a` / 145|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.4.t` / 146|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.4.d` / 147|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.4.a` / 148|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.5.t` / 149|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.5.d` / 150|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.5.a` / 151|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.6.t` / 152|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.6.d` / 153|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.6.a` / 154|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.7.t` / 155|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.7.d` / 156|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.7.a` / 157|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.8.t` / 158|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.8.d` / 159|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.8.a` / 160|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.10.t` / 161|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_europe_america.10.d` / 162|S1/S2|叙事主体、利害与实际结果分开；英文保留相同事实，未把权限/开战写成建设/获胜。|通过（编辑）|
|`nesnd_europe_america.10.a` / 163|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_pru_bav` / 164|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_bav` / 165|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_han` / 166|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_han` / 167|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_sax` / 168|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_sax` / 169|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_wur` / 170|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_wur` / 171|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_bad` / 172|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_bad` / 173|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_hes` / 174|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_hes` / 175|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_hek` / 176|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_hek` / 177|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_nas` / 178|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_nas` / 179|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_wld` / 180|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_wld` / 181|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_lip` / 182|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_lip` / 183|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_aus` / 184|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_pru_def_aus` / 185|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_usa_fra` / 186|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_usa_gbr` / 187|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_usa_pru` / 188|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_usa_ngf` / 189|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_usa_ger` / 190|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_italy_fra` / 191|S2/S3|名称/选项点明政治行动或结果；中英文对应，未加入额外承诺或制度。|通过（编辑）|
|`nesnd_canon_aus_pap` / 192|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_aus_sic` / 193|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_aus_sar` / 194|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_aus_tus` / 195|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_aus_par` / 196|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_aus_mod` / 197|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_small_fra` / 198|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_small_gbr` / 199|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_small_usm` / 200|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_small_mug` / 201|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_canon_small_hus` / 202|S3|固定国家名沿用原生本地化；同盟、防御、投资动作与kind一致，非同义加分按钮。|通过（编辑）|
|`nesnd_egypt_partner_exists_tt` / 203|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`subject_type_nesnd_egypt_protectorate_desc` / 204|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|
|`nesnd_prussian_staff_term_tt` / 205|S3/S4|行动理由与期限/真实效果各司其职；不复述开发状态，数值按所属脚本编写。|通过（编辑）|

候选全文另存batch-c-writing-entries.json，包含每键中英文本；本表按最终写入次序给两语言同一行号。此处未运行键覆盖、BOM解析、动态API或游戏布局测试，全部留在冻结后的测试关口。

## 修复2补充：原生保护国action键

原生action字段要求新增五个显示键。沿用“保护关系/解除保护关系”的玩家术语，不出现专用类型、脚本或兼容实现词。中英文均无缺对象动态引用。

|键|中文候选|英文候选|结论|
|---|---|---|---|
|`nesnd_egypt_protectorate_action_name`|保护关系|Protectorate|通过（编辑）|
|`nesnd_egypt_protectorate_action_propose_name`|建立保护关系|Establish a Protectorate|通过（编辑）|
|`nesnd_egypt_protectorate_action_break_name`|解除保护关系|End the Protectorate|通过（编辑）|
|`nesnd_egypt_protectorate_action_notification_break_name`|保护关系解除|Protectorate Ended|通过（编辑）|
|`nesnd_egypt_protectorate_action_notification_break_desc`|保护国协定已经终止，双方不再承担这项保护关系规定的义务。|The protectorate agreement has ended. Both countries are released from the obligations of that relationship.|通过（编辑）|

## 修复3：有期限的保护交涉

沿S1/S2说明王朝、投资伙伴及具体责任；沿S3/S4分开选择、期限与真实代价。正常6+none+bar保留，pending不能把改选写成恢复发展利益。活赞助无法履约与无伙伴分开；第三国附属只写既成政治事实，不虚构额外处罚。全部新稿是本轮剧情文本，不冒署原作者既有文章。

|键|决定|结论|
|---|---|---|
|`nesnd_egypt_choose_cost`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_none_effect`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.3.t`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.5.d`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.5.a`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_other_patron_tt`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_pending_select_tt`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_protection_negotiations`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_protection_negotiations_reason`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_pending_patron_status`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt_pending_no_patron_status`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.3.unworkable`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.6.t`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.6.d`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
|`nesnd_egypt.6.a`|90日期限只起一次；主语/实际权益/代价与对应分支一致，中英逐句对应|通过（编辑）|
