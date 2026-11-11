# 05 远北的阴谋、黄金与同盟及北海公司

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（1.15.0 / 26453692）  
Evidence: [文件与检查](<../../../../../nesnd-workbench/reports/denglai-route/batch2/verification.json>) · [75 个节点的 near 输出](<../../../../../nesnd-workbench/reports/denglai-route/batch2/near.json>) · [备份](<../../../../../nesnd-workbench/backups/pre-change-denglai-far-north-20261110T212851Z/manifest.json>)

## 1. 现象与期望

按已确认的 spec-v3 和 numbers-v1，开局选路后登莱先在远北积蓄力量，战争线等俄属辽东人实际分离，和平线经营黄金、移民和东洲关系。两条日志均限 4,380 天，届满可以推进。

## 2. 原因与接口

原版支持分离主义外交协定和文化分离进度均可供脚本调用。原生分离回调给出旧国及起事国，可区分真正的分离与第三国征服。投资条款按原版由登莱授予东洲在登莱投资的权利。集团仍由东洲主持。

## 3. 改了什么

- 新脚本同名 `nesnd_sha_far_north.txt`。`common/journal_entries` 管两条日志和结局，`events` 管十二个事件，均有中英文人物引语。`common/scripted_buttons` 管六项行动。
- `common/on_actions` 接原生分离、运动解散、战果和季度援助。复用条件、效果与数值分别在 `common/scripted_triggers`、`common/scripted_effects`、`common/script_values`。原有北朝、东洲变量仅读取。
- `common/scripted_progress_bars` 定义远北人心。`common/diplomatic_plays` 定义归并博弈，俄国排除在外，AI 另核双方军力。`common/diplomatic_actions` 定义入股、调停和共倡同盟。`common/static_modifiers` 定义资助开支、军械和经济、战争结果。
- `common/company_types` 定义北海公司。北方六州中任一州金矿或捕鲸站达到三级即可满足特色门槛，原生公司界面管理产业与垄断特许，煤矿为扩展产业。`localization/{simp_chinese,english}/replace/nesnd_sha_far_north_l_<语言>.yml` 各 159 个键。
- 共用界面的三处改动见[任务 04](04-snow-republic-prose.md)。已更新路线地图和 STATUS。未定期限取分离受挫后休整 12 个月、外交拒绝后冷却 24 个月。调停改善登莱与东洲、东洲与北朝两对关系各 15 点。
- 技能 pdx.py 解析 14 份新增或改动脚本。全量 audit.py 的 138 项旧提示逐项相同。重建内容树并运行 near。公司未被该工具收录，另核原生公司字段、图标与建筑定义。Tiger 的日志字段和 leave_power_bloc 版本差异已对照本机 1.15 文档。

## 4. 怎么复测

1. **整军。** 看「远北的阴谋」和远北人心。接济后查登莱每周开支、对俄协定、俄属伊尔库茨克与上叶尼塞斯克的非俄罗斯族人口。满三个月应再结算一次。分离进度达 50 可在雅库茨克整编 6 步 1 炮。起事期间暂不能归并。等真实分离结束，俄国失去伊尔库茨克、起事国独立持地后，查五年停战、归并目标与俄国能否加入。第三国普通征服不会解锁。
2. **通商。** 查「黄金与同盟」三项目标。勘金比较科雷马、雅库茨克、鄂霍次克的余量，在「金沙」试私采和国营。招徕后查原生迁徙的出发国、文化与目的州。向东洲送入股请求，分别核对拒绝冷却和获准后的投资方向。共同集团内可调停，东洲离开后可倡议新集团或加入它已领导的集团。
3. **公司与结局。** 例如把登莱库页的捕鲸站升到三级，原生公司条件满足后看北海公司及繁荣加成。两条路线分别试成功、超时；归并战败另有军队不满。结案后根日志应更新状态。「复燕」在第 3 批接入。

## 5. 遗留问题

未启动游戏。需实测无民族主义科技时协定能否建立并维持、分离条与胜败回调、俄国介入限制、金矿已发现容量读数、移民到岸、外交接受与换集团、公司特许界面及 AI。金额、节奏和接受分仍为源码估算。
