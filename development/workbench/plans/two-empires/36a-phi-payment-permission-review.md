# 36a — 吕宋减贡资格 NO：源码分解与下一次冷启诊断

2026-10-31，当前1.13.11/build24799966。**更新：run202721 May12实际诊断已证subject_and_bloc_actions=NO；没有把NO改成YES，也没有移除DLC门槛。** 已交付只读诊断B，并获根授权把独立定额经费实施为A2条件候选，不改冻结、原版或A1父版。

## 已观察到的事实

run192545的Jan1在PHI与USM真实event root分别检查，`payments_possible`为NO；relation/exemption/ships为YES。原生pacts唯一USM→PHI的宗属关系是62/`dominion`，没有既有raise/decrease冲突。旧Feb5原生账本有PHI周贡1,642.80，不能据“确在交钱”就推出新外交动作有资格创建。

根代理May12实际进入USM→外交→吕宋→宗主国行动，只见7项：免除军事服务、给予自有市场、授予地区、降低自治权、支持政权、取得地区、强制军事通行；不存在增加/减少贡赋、知识分享、传教和任命总督。这组缺项与同一feature门槛吻合，因此下一次直接读feature是优先检查，不继续无证猜测ROOT问题。此次仅查看，未点击执行外交动作。

`disabledDLC=[]`、游戏目录包含某DLC文件和ep2海军功能可用，均不足以证明`has_dlc_feature = subject_and_bloc_actions`为YES。这一项必须从当前宿主的真实trigger读回。官方[Sphere of Influence发布说明](https://www.paradoxinteractive.com/media/press-releases/paradox-interactive/first-victoria-3-expansion-pack-released-today)和[产品页](https://www.paradoxinteractive.com/games/victoria-3/add-ons/victoria-3-sphere-of-influence)均将调整属国付款列为该扩展内容；它们说明功能归属，不能证明本机许可证状态。

## 当前源码与函数，分别核对

|层|本机文件/函数|真正要求与边界|
|---|---|---|
|原宗属|MOD `common/diplomatic_actions/ce_21_subject_dominion.txt`，对照GAME `21_subject_dominion.txt`|base income_transfer=.25；second_country_gets=no；based_on_second=yes；first=USM、second=PHI。相关定义与当前原版一致，不能先把MOD贡赋设置认定错误。|
|selectable|GAME `33_subjects_decrease_payments.txt:7–9`|宿主`has_dlc_feature=subject_and_bloc_actions`。不能删这条使按钮可用。|
|potential|同文件:12–27|当前actor持有与target相连且income_transfer>0的pact；target不为protectorate/personal_union；不在对方外交博弈敌方。|
|possible|同文件:30–35|双方没有raise_payments。|
|维持条件|同文件:52–82，`diplomatic_action.md`|双方和平、仍有正贡赋pact。README明确这些条件同时参与propose/potential/possible，而不仅创建后检查。README中的旧subject_relation接口不能代替当前实际subject_type实现。|
|engine资格|triggers.log:8924 `can_create_diplomatic_pact`|country scope的原生整体资格；不能拿自己重写的部分条件替代。`can_send_diplomatic_action`另作交叉证据，不据返回差异虚构不存在的send effect。|
|贡率getter|triggers.log:11096 `income_transfer`|比较pact的**base fraction**，例如>.05，不是当周£收入缓存。过一周复测有价值，但不能把NO直接解释为首日尚未缴税。|
|other-country作用域|event_targets.log:254 `diplomatic_pact_other_country`|输入pact、需要country参数。当前原版用`"diplomatic_pact_other_country(root)"`。需要对比真正USM event root、PHI event root和显式`c:USM`参数，以免把外层event root当action initiator。|
|减贡效果|33文件pact|额外−.10同基数转移，原.25加上−.10→.15；它是第二个原生pact。forced_duration12是最低约束期，不是到期自动消失。|

## 已提交的只读诊断B

路径 `WORK/runtime/phi-permission-diagnostic-20261031-b`；完整保留names代理A的13项检查，另新增19项上下文/原始条件检查。可复制其中`events/*.txt`进入**下一次新冻结QA overlay**，不热改当前192545。

```text
event nesnd_phi_permission_context.2
event nesnd_phi_permission_context.3
```

.2让实际USM成为新事件root，.3让PHI成为root；都先运行A的资格探针，再运行B。Jan1和至少过一周后各测一次，并记录完整 `NESND_PHI_PERMISSIONS`/`NESND_PHI_CONTEXT` 日志。只含debug_log、country scope、trigger_event和只读triggers，没有钱款、船权、变量、pact等写入effect。

新增项目：实际DLC feature、PHI实际subject_type、基础pact端点、other_country显式actor与root分别判断、base fraction为0/负数的反证、原生potential/possible逐项复现、can_create与can_send、是否已有decrease、creation_unbound硬锁、双方default、ep2 feature。仅预检3,700/8,700的cash treaty能力，**不创建这些条约，也不表示已经采纳金额**。

由于诊断overlay本身不含metadata/USM国家定义，直接拿它当完整MOD跑Tiger会失败。已另建静态组合 `WORK/projects/phi-permission-static-20261031-b`（父A1只读复制+诊断两文件），Tiger对这两个诊断文件0报告，原A1与诊断B源哈希保持。记录：`evidence/phi-permission-static-stage.json`、`phi-permission-diagnostic-b-tiger.json`、`phi-permission-diagnostic-b-new-reports.json`。这些不等于引擎已执行。

## 结果如何决定下一修改

1. **DLC NO，其余原始条件YES：** 缺少该feature是已证阻挡，保留原生减贡不可用的事实；可选择下述本MOD自己的真实经费合同。不复制一个去掉DLC条件的decrease_payments。
2. **DLC YES，base-pact/other-country检查异常：** 先查pact端点、实际base fraction与event-root传递。若显式actor通过而外层root不通过，可把正式发起和最终确认的付款操作移到真正USM事件root，再使用同一个原生can_create重新确认。不能以静态“应该有权限”强行创建。
3. **DLC YES，raw全部YES，原生can_create仍NO：** 记录未暴露的engine约束，结合can_send结果及原生外交界面禁用提示继续定位。当前没有已证安全的发送effect可以替代，因此不能把它当“可忽略的trigger bug”。
4. **money_transfer也NO：** 分离来源/目标的central_banking、default、原生数量上限和条约资格。不能临时用单向add_treasury伪装钱款，也不能悄悄给PHI科研解锁。
5. **原生减贡YES：** 才允许本项目原A/B流程继续；之后仍必须验证真实pact出现、PHI缴款/USM收入下降、钱款实际双方记账、合同ID与20艘真实交割。

## 若确实缺少feature：独立经费合同（A2条件实现，尚未实机）

本MOD可以让两个政府谈判实际的驻屯和海防支出，不要求先取得“减贡”外交动作。建议提供新的、明确命名的**定额协定**：A维持驻屯与舰队，B分任20艘战列舰、保留地方驻军/护卫舰；原本25%宗属缴款继续存在。付款方按原生money_transfer从自己预算支付，双方再次同意后建立独立条约，仍有12个月期限、序号和精确ID清理。B免役也必须另过其原生资格；若无权限，不能把免役效果写进已签条款。

3,700/8,700已获根授权作为A2的明确候选报价：比原3k/8k加700，比旧Feb5估算减贡657.12略高42.88。**不是精确“退还10%贡赋”公式，也未平衡完整船员和35楚军。** 它与原生减贡并不等价：原生减贡随受款国税基变化且可在一年后继续存在；定额经费固定、期满停止，本协定不改变原25%贡赋率。

如果采用，应在新候选基于A1（保留unbound三guard）实现独立relief mode：只有在真实feature缺失且未有原生减贡时显示现金路线；有feature而资格异常时继续提示具体阻挡，避免用备用分支掩盖未知bug。报价、帮助手册、USM核准、PHI确认和最终条约金额必须一致；现有写死的8k/3k及“减贡”文本不能沿用。创建后的UI只显示“中央经费××/周、原贡赋照旧”，不显示减贡成功、不加对应liberty desire效果。

任何现金方案仍须先过同步hook门禁：`creation_unbound`一旦出现即锁死续申并拒绝交付，不能把创建成功却无ID归属的钱款称安全回滚。若异步hook问题存在，应先解决条约身份捕获；不能扩大功能后再掩盖失踪合同。

## A2交付记录

候选`exports/phi-imperial-service-20261031-a2`，精确父`phi-imperial-service-20261031-a1`。只有9个财政模块/本地化/metadata文件改变；未改变任何军事、人口、地图、建筑或既有外交动作定义。备份`backups/candidate-phi-cash-a2-final-20261031T201042Z`，完整父子SHA和diff在`evidence/phi-conditional-cash-a2.json`/`.diff`。

四报价管线已静态逐项核对：native A8000/B3000、cash A8700/B3700，request保存quote→pending再次资格→USM核准→PHI确认→commit原生钱款→capture匹配quote→原始binding与单条款ID→付款方quote/binding镜像→12个月/提前撤回/关系变化清理。身份判断始终与本合同保存的精确金额比较，不是“只要四个金额之一就接管”。A1 unbound三guard及不自动清除的硬锁保留。

现金按钮只在真实feature NO且没有现存减贡pact时显示；有feature而其他资格失败不会偷走现金旁路。保留的原生按钮适用于feature YES或已有合法减贡pact的旧存档。现金完成不创建decrease_payments，不获得它的独立倾向效果；B真正签订原生免役时，其本来就附带的效果按原生规则存在，没有额外添加liberty modifier。A现金仍要求两国与真实政治盟书同阵营，B保持中立/自主可选。

另补**提案序号**，与合同到期序号分开：每次四类正式请求保存独立serial；8个请求/确认事件和所有接受、拒绝、搁置、撤回效果都绑定对应serial与现金/原生模式。旧弹窗仍可关闭，但不能批准或拒绝后一次新报价。手工force event缺少该提案上下文不算production路径测试；下一轮应点日志按钮或调用完整request helper，不能直接跳最终确认。

Tiger本模块仍只有A1已有`total_crew_needed`旧词库报告，没有新增报告；当前引擎docs已支持此getter；旧 G0 实际原生变量 `nesnd_phi_needed_crew=26000` 另已证实月度测量执行并序列化。它是需求量，不能当作实际在舰水手数量；新钱款与舰船交割仍待。`check_phi_cash_a2.py`核四金额闭环、提案保护、精确身份、付款镜像与退出保持；这些检查没有认证原生付款或舰船交割。

冷启顺序：加载诊断B→执行`.2/.3`核feature和钱款预检→经真实现金B按钮申请→USM核准→PHI确认→同tick检查typed treaty/active_cash/quote3700/20舰且无unbound→走一周检查USM扣款、PHI收款、原贡赋仍在→再测拒绝/搁置/旧弹窗/到期/读档与完整军事规模。任何unbound或错舰数应停止，不连点申请。

## 旧 G0 兼容与本轮实际加载边界

`evidence/phi-proposal-legacy-guard-201812.json` 核定旧 May12 G0：已有 `nesnd_phi_initialized`，尚无 `nesnd_phi_proposal_serial`、pending 或 unbound。四个正式申请 effect 均先 `if missing → set 0`，再 `add 1 → save_scope_value_as`，所以兼容保护位于请求入口，不依赖 initialize 再跑。旧版已排队但没有 proposal serial 的确认事件不得冒充新版提案；应等待旧请求过期/撤回，使用新版完整申请流程。静态源序证明尚不是旧档实际签约证明。

run201812 仅完成冷加载；启动后才复制存档，菜单未发现它们。运行工具已调整为启动前放入测试存档，实际加载实验改为 run202721，仍沿用同一 A2 effects SHA `be0c35c33651aceda1e89e6ca402a6748fb3d3b81c02e605d608ac419fd16e88`。截至只读核查 20:27:51 的冷日志，没有真实诊断 payload；orphan 提示不能算执行了 `.2/.3`。后来实际诊断与签约应使用各自时间戳、真实当前存档来源，不把拷贝目录名当执行来源。

复用 `tools/audit_politics_phi_native.py`；新增小补充器 `tools/audit_phi_contract_native.py` 调用其 `audit()`，只补财政原数组、原生 pact、水手来源州、活舰筛选与来源 SHA 复核。预试报告 `WORK/evidence/phi-native-wrapper-pretest-201812-jan1-old-g0.md` 明确两个旧档跨自然时间、不是本轮合同实验。实际验收需同 tick 签约前后档查同 ID 20 舰归属与 typed treaty、之后稳定周档查两边款项、12 月到期/提前退出/原生改约各自独立覆盖；预算数组差额不自动证明合同的因果金额。
## 20:48 实机诊断已返回

当前结论和操作边界见 [May12权限审计](evidence/phi-permission-202721-May12-assessment.md)。USM/PHI两种真实root均缺subject_and_bloc_actions，原始宗属/.25贡率/possible通过，原生减贡创建与发送均NO。USM root现金3700/8700条约预检YES；PHI后段日志尚未flush，不能补写。ep2_content也是NO，但原生ship_transfer条约门槛不等于通用剧情set_ship_owner_multiple必然受限；根已明确暂不增加推定的B门禁、不删用户授权功能，保留独立实测API边界。A2/冻结不动，没有A3候选。

Gbuy的两国拥吴/真实盟书/国库与固定收支满足现金A前提，可以使用该旧局正式申请，不需重新构造Jan1；实际资格仍由按钮当时复查。两次事件转递均无days=1，不能保证单人切国前AI不做决定。下一门槛是实际typed条约绑定、双边支付与准确记载的人类/AI确认路径，见审计的逐步清单。