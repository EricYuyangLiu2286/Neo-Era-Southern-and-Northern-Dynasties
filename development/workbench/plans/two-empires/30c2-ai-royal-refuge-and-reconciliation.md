# C2 王室去向与高压无战的收尾

父版B1。独立候选，禁止修改B/B1或当前冻结run。状态：已冻结独立候选C2，23文件差异，备份candidate-court-reconciliation-c2-20261031T200537Z；尚未实机。

## 王室与控制权分离

现C1的`nesnd_ming_commit_player_transfer`把人物迁移绑在原USM玩家的is_player和拥明意图内，AI USM没有同样的避难过程。C2保留玩家分支，新增不切国的人物避难：真实DP成立后，合法活王室可去实际拥明且已独立、有自控首都的HNA/SIH。接收方在既有“拥明”选项中奉君或监国；选择共和保留人物为可见宗室，不凭空杀掉或复活。

有接收国也不意味着它必须被夺取玩家控制；只有原玩家分支调用play_as。无合法接收地则明确留京，以新scripted other-role保持可见身份并支付宗室安置成本，角色仍会自然死亡。使用`add/remove_character_role`、`set_is_noble`及原版日本天皇other-role实例。旧朱氏heir须从吴国解除heir角色，迁往行在后再实际set_heir；原版00_victoria_ep2_scripted_effects:13/59有remove_character_role=heir实例。

王室对象来源仍为B已验证的作者模板或合法继承标记。缓存指向死者/外邦在位君主时不强取；不生成新的朱氏模板。地方旧统治者保留对象与原职责。行在真实奉朱氏君主时，复用本MOD皇帝政体称号条件，防止因HNA/SIH静态country tier而仍显示藩王；不修改国家实力等级或地图。

## 履约安定：持续成本，不按续签刷条

高压无战的USM在没有真实DP/对南方战争、无settled时，可以开启“履约安定”。基础使用B1各路线全部严条件，唯独暂不要求pressure<60；仍需真实有效盟书、主权/割地同意、财政/供应/军务等。

任务期间政府工资+5%、权威−50。开始后实际支付至少一个月，之后每次月检仅降低压力3点；按钮本身不降压，续签也不降压。每周/每月重新检查，不符合即停止任务；重新开始须重新付满一月。降至40完成，为后续B1的真实一年和平观察留出缓冲。无自动设winner/settled/吞并。

高压未开战状态两年仍无解，可明确接受现有秩序作为不圆满结局：只关闭本轮危机，不改国界/宗属/政府、不发和平胜利奖励；真实财政/贸易条约继续按自己的期限运行。此选项与有成本履约提供退出路径，不能把无反对者直接算吴朝完全胜利。

## 外部观察者界面

立场四选的visible和possible限USM或真实political_member。CNE/HUS/FRA等保留全球视图，显示“外部参与者”，使用既有外援日志行动，不参与帝国内部派系选择。旧外部stance变量不删其他系统数据，只不再解释为内部派别。

## 文件闭包和实测

新增royal refuge/reconciliation triggers/effects/events/role/modifiers/localization；窄改hidden转移入口、既有反吴路线选项、吴登基后的旧heir处理、global按钮显示、实际月度压力读数与政府称号条件。B1政治权重、计票、所有状态/海港/人口历史、服装素材不改。

场景：AI USM+AI HNA/SIH；AI USM+人类HNA；人类Wu+AI拥明方；人类Ming原C1；父活/父死子活/皆死/无host/重复事件；旧heir不留在Wu succession，宗室存读档后仍可见。高压100且无战原生断点→无有效约不能降压→真实接受+付费一月→月度−3→破约停止→40结束→B1一年观察；24月接受现状不吞并/发奖。外部CNE与HUS只能观察，真实帝国成员仍能四选。不能用静态验证代替以上。


## 复核与交付

names_and_testing独立审查发现并修正：24月时钟在每周/月检查context失效时重置；已迁走角色不先排过时留居通知；general refuge完成清旧player_intent/waiting，避免改吴后再改明走空位重迁；地方旧统治者用真实对象的“行在保护人”角色继续显示。helper保存显式host，避免root仍USM而owner检查错位。

结构验证通过，父B1/主MOD/其他候选未改。Tiger新增两条other角色枚举诊断均有当前原版日本天皇type=other的源码依据；真实角色可见/退休/继承与读档仍未认证。具体原生检查清单：evidence/court-reconciliation-c2-engine-checklist.md。静态报告、manifest、diff：evidence/court-reconciliation-c2-static.json/.diff。
