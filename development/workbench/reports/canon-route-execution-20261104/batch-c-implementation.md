# C批实现交接

状态：**READY_FOR_TEST**。2026-11-04。全部C1–C6编辑已结束；从本交接起停止修改这些文件，等待root安排冻结后的测试。

- 候选：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\canon-route-execution-20261104-a`。
- 固定父：`b94582ecec7b0b6dd5620a184658190157fc1729`；主MOD未部署，Git未提交/推送。
- 本批独立文件冻结：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-edit-freeze-20261104T124748Z\mod`，仅C批拥有的31份文件，没有复制正在被A/B编辑的文件。
- 精确SHA与新增/修改清单：`batch-c-owned-sha.json`；开始编辑的原指纹为`batch-c-pre-edit.json`。
- 本机源码版本：1.13.11 / Steam build24799966；源链与指纹在`batch-c-native-sources.json`。
- 本阶段没有运行行为、AST回归、Tiger、MCP或游戏测试。编辑完成不等于STATIC_PASS，更不等于ENGINE_PASS。

## 实际落库内容

|任务|实际实现|关键闭包|
|---|---|---|
|C1共用请求|kind1联盟、kind11德邦防御协约、kind2欧洲投资、kind4意大利防御；kind3/5接口保留；次日事件、1月事件窗、45日请求锁、6月发函冷却|双方存在与存活、政体快照、当前资格/关系、serial/kind/partner匹配；真正条约/信用后置条件成立才成功；首次关系奖防重复；拒绝/过期不清新nonce；有向article先查source/target存在|
|C2埃及|六个1825投资＋保证协定，1845仅撤已登记对象；主JE保留六投资国＋none＋独立性条；子JE改大学2/工具3/主业5且各就业75%的真实能力目标|主动none不重抽；失去赞助对象才替换；唯一月度扣分；三十年钟不重置；0有活赞助走保护安排，无赞助invalid一次；2日保护关系稳定观察后确认，无法成立保持pending及通知；成功奖120月一次|
|C2保护国|先按原生31号外交行动的方向尝试标准protectorate；必要时用EGY专用rank/type宽容的保护国type/action|隐藏外交入口，不修改任何标准subject类型；不解除赞助者既有宗属、不允许EGY属国反向循环；赞助can_have_subjects等阻碍保留pending；玩家名称仍为保护国|
|C3普鲁士|PRU及有连续origin的NGF/GER；独立德邦的联盟/防御协约＋军队75/军工5；3个distinct伙伴；莱茵后继|实际伙伴不能已与FRA联盟；多边同盟科技仍由原生can_create检查；协约失去暂停共同参谋利益；十年到期事件确定停止，初奖不重领；阿尔萨斯仍由FRA持有才赋一次宣称；真实GER形成或法莱茵支配退出结算|
|C4奥地利|常驻意大利外交、防御条约、领土/统一DP选择、目标方干预、有限代价的不干预选择|用is_war/escalation及21–80原生阶段；明示侧/敌/战略区与原生side规则、停战/盟约/既承诺限制；加入实际敌友双方后才记承诺；绑定DP直到终局；匹配wargoal证据、目标保全/失守/白和分开；结束后留1日grace并次两日核验|
|C5美国|真实欧洲投资权及军力/军工/铁路/就业准备；保存一个实际接壤HUS州；单州宣称、正式return_state要求|不破停战、不一次拿全北美claim、不在开战时领奖；开战前保存原HUS份额的province列表；native DP回调绑定；真实匹配wargoal与全部原省份归USA才给首次五年军事成果；白和/失败保留claim并冷却；ACW暂停进攻，原住民HUS身份不继续套原冲突|
|C6退役与文本|8个旧regional事件惰性取消壳、领奖helper无可执行奖励、遗留pending清理；旧veiled_protectorate唯一事件定点停用；独立中英replace|原已获修正不撤销；保留旧effect参数接口；204个成对新文本，固定名称用原生国家键；动态对象按分支/事件取消条件保护|

## 明确的数值与计时

- EGY独立性0–100；存活赞助−1/月；额外外资压力`−2 × max(0, foreign_share−0.25)`，foreign_share为实际所有外国GDP所有权ratio总和。此为批准的平衡选值，不是原生经济公式。主JE的bar明细与国家结算使用同源数值。
- EGY能力奖60月：教育机会+2百分点、制造吞吐+5%。完全不要求外资持股，也不恢复独立性、免费造厂或改变人口。
- EGY三十年成功奖120月、无赞助0点合法性处罚60月。1845历史条约到期独立于JE是否还活动。
- 德邦合作窗口120月，持续满足3伙伴＋军力时按月维持，十年事件结束；莱茵结果奖60月一次。
- AUS干预军费/防御修正最长24月，结果结算时清临时承诺；胜利影响36月、失败24月；决定后24月冷却。白和无胜利奖。
- USA单州claim花6月影响力−50并对HUS关系−10；6月claim冷却。争端结束24月冷却；首次确实取得原要求全部province时军事奖60月，不因以后再次获地刷新。

## 保留给后续批次的真实接口

1. **kind3**：意大利发送国资格使用后续`nesnd_italy_country`，FRA接收；结果仅限时政治信用变量/修正，没有伪造投资权、结盟、统一支持或吞并。后续意大利批次在C1冻结后补政治担保随法国改制等存续规则。
2. **kind5**：B2供应真实`nesnd_small_state_country`及后继资格；C1已提供有向投资约、nonce与回复保护，未定义always=yes/no占位。缺少后续国家定义应作为外部待接依赖报告，不能涂成全包引用通过。
3. kind6/7/8完全留给B2。本批只新增kind11防御协约，不触碰A法组和B团结度/既有印度文件。
4. `common/static_modifiers/nesnd_europe_america.txt`原意大利信用及小国资本键保留；后续接手同一文件前请明确所有权。

## 测试阶段需要重点解决

- 先从冻结SHA读取C批，不在测试中途编辑；发现具体问题后交回本代理修复，再冻结复验。
- 请求缺scope/缺变量、旧nonce迟答、新请求覆盖、政体改变、国家死亡/宗属变化、三类条约创建失败、失去最后一份投资权及仍有替代条约。
- EGY0与30年同日、亡国替换和主动none、六国全失效、正常SIH层级USM→SIH→EGY；标准创建后被引擎撤销的grace；专用type在实际引擎中能否稳定仍待真实证据；它不是标准type的别名。
- EGY两JE无重复按钮/独立性写入者；子JE0外资可达、阈值/75%就业、重复完成、主JE结束和奖励不重置。
- PRU→NGF→GER及旧任务33起源标记；distinct伙伴计数、FRA盟友排除、多边联盟技术门槛；十年延迟事件与月界顺序。
- AUS原生参战资格与force-backers effect的实际引擎限制未声称全部等价；保存DP同侧确认、开放期边界、未参战/加入失败、旧DP消失、失地/白和/成功。延迟结束grace避免同帧先于转地结算。
- USA province列表在owner-state合并/第三国夺地后仍只认原要求；发起失败、即时退让、国家死亡、ACW与NativeHUS身份；任何无关战争不得给本案奖励。原生create DP及on_wargoal/on_war_end回调顺序仍要在来源/静态与引擎边界之间区分。
- 新UI字段/双语键/BOM/引用覆盖、有效后层文本、角色名/州scope、所有原生及自定义提示。`batch-c-writing-comparison.md`是人工编辑对读，不替代这一检查。

## 文本及证据

作者原始样本来自pre-update-20261030T233944Z独立备份。对读文件列来源SHA、S1–S4原文、真实返工及每个最终键的编辑结论；完整中英候选在batch-c-writing-entries.json。明确返工包括HUS共和国主体、埃及三十年与1825日期、未完成能力目标不能在父JE成功稿中宣称已成长、英文HUS tag改原生名称。没有改永久技能：本批未取得新引擎证据，既有规则已经覆盖这些编辑教训。

此交接仅交付候选实现与冻结文件。后续测试和两轴复审由root组织；主MOD/Git合入仍未发生。
