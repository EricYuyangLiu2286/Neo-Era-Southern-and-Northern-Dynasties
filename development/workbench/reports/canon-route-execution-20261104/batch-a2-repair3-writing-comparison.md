# A2 repair3 玩家文本逐键对读

执行者 `/root/sol_b2_implementation/a2_repair3_confirmed_batch`，委派声明 `gpt-6.1-sol / medium`。只完成编辑自审，不运行行为测试、Tiger、MCP或游戏。

本轮适用 nesnd-player-writing。作者样本读取独立备份 `WORK/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_french_empire_journals_l_simp_chinese.yml` L41（共和运动的政治因果）、L43（“共和呼声”）、L54–55（“游行示威”及直接说明行动目的）。原始文件 SHA256 为 `352501e3baa2a92b9c04d96a464eea466bd411b4d4820916ae9b0c587063c844`，沿用既有写作报告的来源记录。本轮回读实际样本，不用当前代理文字充当作者文风。

本轮局部规则：名称沿用已确定专名；说明句直接写行动者、目标及结果，不把条件守卫或修复历史放入玩家文字。`NKH` 沿用既有“大平原汗国”，不是新定名。战争事实取当前 `common/diplomatic_plays/nesnd_american_restoration.txt`、`nesnd_native_khanate.txt` 与 `common/war_goal_types/nesnd_native_americas.txt`：复统双方互相吞并；干涉方吞并汗国，汗国反向羞辱对手。说明诉求不保证所有战争必然以诉求执行结束。

|键|作者/既有契约对照|新增中文|新增英文|逐项结论|
|---|---|---|---|---|
|NKH|作者样本L43以具体政治对象命名；当前汗国事件与日志已经使用大平原汗国|大平原汗国|Great Plains Khanate|通过。沿用专名，无机制或版本说明。|
|NKH_ADJ|同上；用于国家形容词|大平原汗国|Great Plains|通过。中英文按各自词法使用同一地理政治对象。|
|dp_nesnd_native_restoration_desc|L55直接写行动与目的；当前双方专用目标均执行吞并|复统王朝与共和国争夺国家的统治权，胜者将吞并败者。|The restored dynasty and the republic contest rule over the country. The victor will annex the defeated state.|通过。统治权是冲突对象，吞并对应目标；未增加人口、奖励或自动胜利承诺。英文独立句承接结果。|
|dp_nesnd_native_restoration_tooltip|同一事实不重复撰写第二份；本项目既有日本战争tooltip使用标题加desc|#header $dp_nesnd_native_restoration$#!\n$dp_nesnd_native_restoration_desc$|#header $dp_nesnd_native_restoration$#!\n$dp_nesnd_native_restoration_desc$|通过。引用已存在标题及本轮实际说明键，无动态scope。|
|dp_nesnd_khanate_suppression_desc|L55行动与目的；当前专用目标为干涉方吞并/汗国羞辱|干涉者要求吞并大平原汗国，汗国则要求羞辱干涉者。|The intervening power demands annexation of the Great Plains Khanate; the khanate demands the humiliation of its opponent.|通过。两方主语清楚，逐一对应不同诉求；没有将停战或未开战称为胜利。|
|dp_nesnd_khanate_suppression_tooltip|同上，本项目现有标题/desc引用形状|#header $dp_nesnd_khanate_suppression$#!\n$dp_nesnd_khanate_suppression_desc$|#header $dp_nesnd_khanate_suppression$#!\n$dp_nesnd_khanate_suppression_desc$|通过。引用有效标题及说明；不另写重复正文。|

本轮六键均通过编辑自审；保留原先134对的全部正文。没有需要推广至永久技能的新规则。游戏显示、有效加载与完整隐式键覆盖交独立测试，不以本表代替。
