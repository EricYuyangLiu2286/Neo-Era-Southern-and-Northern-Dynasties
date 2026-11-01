# CNE 剩余终局的真实测试路线

目标版F；当前run162626冻结opiumA不能热改。QA仅活动源runtime/qa-overlay，下一轮冻结后生效，不进入发布MOD，不改GUI坐标。

## 来源与依赖

F/common/journal_entries/ce_cne_land_draft.txt 的 complete/fail/invalid → common/scripted_effects/nesnd_crisis_effects.txt 的 success/freeze/collapse/release → events/nesnd_crisis_events.txt .31/.33 → common/scripted_effects/nesnd_land_choices.txt 的真实optioneffects。全部门槛来自 common/scripted_triggers/nesnd_cne_reform.txt；真实测量由月度measure更新，不能把缓存值当修改真实人口/生活水平的接口。

QA仍用本机已有并已实际打开的 country_event、trigger_event popup=yes、if/else、debug_log固定字面串、var比较、set_variable。无新控制台命令，无ROOT动态字符串。进入国家后现有 `event nesnd_qa_routes.1` 必要时点击首都卷轴，再到CNE菜单。对战争/破产/就业的操作使用原生UI，不猜命令。

## 新子菜单设计

在既有CNE菜单仅加一个“终局门槛与真实事件”入口，不重复已有4–8、请愿、暂停与普通clock。新菜单：只读逐条guard检查；只有实际local_crisis且未读标记时可呼出.33；只有真实terminal_pending且未读时可呼出.31；健康且风险<30时可用“快速成功计时fixture”，仅completion98/good23/months47，不改健康、制度、人口、风险、samples。关闭菜单等待真实月度measure/tick，重新验证健康，不能立即调用success。

为了能分辨未达门槛和菜单坏掉，终局菜单始终保留只读检查，并以实际predicate打印YES/NO。未达条件的事件选项隐藏，不清终局旗；正路径必须重新载入实际基线。

## 最短分支矩阵

|分支|可复现操作|必须观察的实际结果|
|---|---|---|
|不健康不能靠计时成功|既有普通clock只改100/11/60 → 走过下月1日|实际measure仍不健康时good归0，成功旗无、JE继续；D已有此证据。|
|普通成功|真实调整土地制度、学校、财政与民生至下面全部门槛；原生保存；普通clock100/11/60 → 下月|good12、months61，真实JE完成触发flavorCNE.3，done/succeeded与清理存在；无rapid奖励。fixture只证明终局执行，不证明自然发展所需年数。|
|快速成功|同一真实健康基线且风险<30；新rapidclock98/23/47 → 下月|实际健康仍成立则completion100/good24/month48，成功并加nesnd_land_rapid120月；与普通成功分开重载。|
|本地危机让步|实际符合地方危机基线，保存；菜单.33选a|进度−10/风险−15（clamp）、国家调查成本36月；不创建NSX。|
|本地共和起义|同一真实地方危机基线重新载入；.33选b|按真实失业排序选山西或晋北非首都州创建NSX，人口/建筑/军队与所有权对照；共和国法；CNE claim、关系−75。双方无战争/承诺时才发吞并play，否则不凭空加第二战。|
|严重危机选择冻结|真实JE fail产生terminal_pending；原生保存；.31a|冻结/清理、60月secession disorder、单120月compromise，无虚构割据。|
|严重危机瓦解|同一真实基线重新载入；.31b|先重新measure，再重核extreme；合法NSX/NHB/NSD各自释放，至少保一州；已有TAG、非本国州、首都不能释放。若严重条件已消退，实际fallback冻结，不声称割据成功。|
|冻结后的寿命|真实.32a或.31a → JE关闭 → 过下一月1日 → 保存读回|done/frozen保留、month/sample不再增长；用manager dead_objects判JE死亡，不单读遗留active=yes；F新实例刷新后compromise仅1条。|

## 健康基线必须真实达成

reform_active、samples≥3、workforce>0；地权法律为自耕农/商业化/集体化之一；失业≤6%，或社会保障≥2且SoL≥12时失业≤12%；饥饿≤8%；无持续被忽略地区；加权SoL≥11、接入≥85%；学校≥2、识字≥48%；政力≥0、和平、未破产。完成还要求风险<50、completion100和good≥12。学校法律/机构、税率、建设、贸易等用真实游戏界面调整，运行至人口/市场状态实变，再保存。不能用set_variable把缓存涂绿。

## 地方/全国危机基线必须真实达成

地方：samples≥9、风险≥65、NSX不存在、CNE不止一州；山西/晋北当前属于CNE且非首都，实际失业>10%、动乱>25%、local_bad_months≥6。可在隔离QA存档通过原生关闭/缩减雇主、农业挤出与政策造成真实失业和动乱，必须逐州读就业/自给岗位及月度计数；仅缺货或招聘慢不算失业。若自给农业吸收劳动力，则该操作没有制造满足条件的危机，不能强行触发。

全国：samples≥15、风险≥90、bad_months≥12、实际全国动乱>40%、合法性<25，且实际参战或正式破产。通过原生政府更替/财政与战争操作达到；按钮直接加入declared_bankruptcy修正或改缓存不作为真实破产。长线测试仍需要运行足够月数。当前开局没有这些条件，只能做条件未达不出现的负例，不能把菜单可点当正例。

## QA保存与后果边界

源修改前完整备份；只保留菜单源码与本地化增量。每轮记录原生国家、日期、输入动作、日志增量、保存SHA。正负分支从各自原生基线读回；不删除done/frozen/succeeded来复活结束的改革。累积QA产生的修正/激进派不用于开局经济平衡；正常可达的modifier叠加仍按真实BUG修复。
