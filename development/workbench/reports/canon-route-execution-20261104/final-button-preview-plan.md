# 最小按钮数值反馈计划

状态：**PLAN_READY；未编辑 MODscript/本地化，未运行行为、Tiger、MCP 或游戏测试。**

配置沿 root 明确委派：gpt-6.1-sol / medium。只读当前候选 `WORK/exports/canon-route-execution-20261104-a`。本机 1.13.11 / build 24799966，catalog CURRENT、changed_count=0。C2 repair3 既有通过结论不变；这是 root 最终阅读发现的新增显示缺口，不追认成旧测试失败。架构与最终范围由 root 裁定，当前阶段只提交可执行窄计划。

## 原版完整链与接口结论

以下 G= `D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`；每个实际文件 SHA 和引用原文收在 `final-button-preview-source-chain.json`。

1. `G/common/journal_entries/00_poland.txt:13` 实际挂载 `christ_of_nations_button` → `common/scripted_buttons/00_christ_of_europe_buttons.txt:17–33` 的 effect 同时调用事件、文字提示、`show_as_tooltip { add_modifier }` → `common/static_modifiers/content_3_modifiers.txt:507–510` 定义实际 `country_expenses_add=500`。因此按钮可用原生修正预览显示具体开支；不需要自造 GUI API。
2. `G/common/scripted_buttons/04_indian_famines_buttons.txt:18–69`：国家费用以 `multiplier=money_amount_multiplier_medium`、`months=12` 显示；逐州真实收益在 hidden_effect；外层简短 custom_tooltip 加 show_as_tooltip 中的 state/add_modifier 单独展示实际地方修正。数据库 `common/static_modifiers/00_ip2_02_modifiers.txt:39–69` 定义费用基数1及两个地方效果。这直接适用于 C2 国家报价与确定目标州显示；C2 已经存在点击前目标，不能照抄原版随机选州。
3. `G/common/journal_entries/00_land_reclamation.txt:25–35`：JE 完成预览用 show_as_tooltip/add_modifier，真正奖励由别处事件完成。`common/static_modifiers/content_1_modifiers.txt:1105` 为对应修正定义。说明该包装不限按钮、可与隐藏真实执行分离。
4. `G/common/scripted_buttons/00_cuba_scripted_buttons.txt:175–198`：show_as_tooltip 内可使用 if、现存国家 scope 和动态 multiplier 展示条件结果。只能读取已存在对象，不能在预览里先写 saved scope 再读。
5. 本机引擎导出 `WORK/references/engine-docs-1.13.11-20261031/effects.log:37209–37212` 明示 enclosed effects 仅显示 tooltip、不实际执行；`:312–315` 的 add_modifier 支持 country/state/IG 等作用域；`:1124–1128` 确认 custom_tooltip 可单 key 或带 text/subject。实际 root 国家 ScriptValue 本地化形状见 `G/localization/english/ip3_serbia_l_english.yml:300,303`：`[ROOT.GetCountry.MakeScope.ScriptValue('...')|D]`。不能拿 GetPlayer 替代事件当事国。

没有证据宣称同名修正已存在时原生 UI 必定仍列出数值，也没有打开游戏验证渲染。因此计划不依赖该推测：费用给始终可见的当前/锁定报价文字；地方与政治修正在同名已存在时加精确简短文字退路。原生预览为主，退路只在原生可能去重的既存修正分支出现。此为计划依据，不是 ENGINE_PASS。

## C2 必修显示闭包（无玩法改动）

当前 `common/scripted_buttons/nesnd_civic_routes.txt:1–117` 的27项目按钮只有 target custom_description 和10项经营条件 TT；真实 `_start` 全在 hidden_effect。`common/scripted_effects/nesnd_civic_routes.txt` 启动函数实际给费用12月、地方24月、政治12月；`common/static_modifiers/nesnd_civic_routes.txt` 中逐选项值包含建设+5%、教育+5百分点、交通+10%、牧道交通+5%/建设−2.5%、税容+10%，以及具体两 IG +2/−2。27条 option→category_quote→点击前 option_target→三个真实 modifier 的逐项对应已附源链 JSON，编辑不得凭文案主题猜 modifier（例如油业监督实际是教育协助）。

最小修改文件：

- `common/scripted_buttons/nesnd_civic_routes.txt`：仅27项目 effect 的显示部分；hidden_effect 中实际 `_start` 调用及顺序逐字保留。
- `common/script_values/nesnd_civic_routes.txt`：新增10个 category display_quote；双边预算另加 compact display_quote。真实 weekly_quote、真正 set_variable/支付函数均不变。
- `localization/{simp_chinese,english}/replace/nesnd_civic_routes_l_*.yml`：27 desc 仅删除重复财政/期限结尾，保留 final_standards 新具体正文。增最少的报价/必要退路 TT；不动人物文件与人物文案。四份当前 civic locale SHA 已记录，人物两份必须原 SHA 保留。
- C2 双边预算补 `events/nesnd_civic_routes.txt` 两个接受选项显示层，见下。

每个 display_quote 定义为 `value=nesnd_c2_weekly_quote`，只在 `if { limit { has_variable=<category>_quote } value=var:<category>_quote }` 的实际 body 读取旧报价。缺变量返回当前 `gdp*.0001` round/clamp25..2500；存在则返回已冻结值。只读、无 setter、不用同层短路。报价文字在原国家 root 取该 wrapper，明确“每周金额，起办时锁定，支付12个月”；若已锁定则措辞“本期已锁定每周金额，原支付期12个月”，不能让玩家以为变GDP会重新计费或点击会重启计时。

每个项目按钮在当前 target 已存在的实际 if body 内，再进入该 option_target 的 owner=root/原 candidate 安全分支；保留现有目标名 custom_description，同时加入：

```text
show_as_tooltip = {
  add_modifier = { name = <category>_expense months = 12 multiplier = <category>_display_quote }
  var:<option>_target ?= {
    add_modifier = { name = <option>_local months = 24 }
  }
  add_modifier = { name = <option>_politics months = 12 }
}
```

上例是计划形状：外层确有目标存在 body，owner/candidate 检查也须实际嵌套，不能依赖同层 AND/OR 或 visible 的求值短路。不能使用仅 `_start` 写出的 category_target、provider、choice、baseline。显示主体保持国家，进入目标州后再显示州修正，不能把国家费用/政治修正误放州作用域。缺目标/失去owner/不合候选时不显示该州收益，也不写任何状态。报价只依赖已定义数值 wrapper，不依赖 start 写变量。

对于 state 已有 local、国家已有 politics 的相应分支，用短 custom_tooltip 写出该选项真实数值与原期限（本期地方24月、政治12月；不是剩余期限、不是再次发放）。包含负面效果和准确 IG，不泛称“协助”。报价始终可见，避免已有 expense 使原生同名预览去重后金额消失。文字不应承诺重复领取；必要时明确“当前已生效，不能重复开办”。可用27个精确 option TT 复用到既存修正 fallback，不能用一个笼统共同句替代差别。

C2双边预算：`.10.a` 和 `.11.a` 实际接受会分别在 sender 与 receiver 记录当时各自报价并各付12月（effect:891–910）。现有事件正文仅泛称拨款。外层只读 preview 在真实 saved sender/partner/serial 存在分支和既有 accept/confirm eligibility 分支后，分别以两国 scope 展示 `nesnd_c2_compact_expense` multiplier 各国 compact display_quote、months12；附一句“双方各按自己起办时报价付款”。不得在请求发出时宣称已经扣费，不得在替代建议/拒绝选项显示接受后的费用为已发生。

## 188文件有界筛查

范围严格来自 `R/final-review-contract.json` 的188个 changes 路径，读取当前候选相同路径；不是全 MOD 文案重审。文件内共有215 buttons、159 options，228个含 hidden_effect。保序源码读取筛出58个含可追踪实际修正/关系等关键效果的候选；其余大部分为同构外交请求、72个宣称按钮、重选州内务、既有原生兼容逻辑。这个清单是静态阅读辅助，不是行为测试，递归 helper 上限6只作为候选生成；结论按下述原文链人工核定。原始 source/line/反馈文本在 `final-button-preview-bounded-inventory.json`，不得将228个 hidden 一概报错。

### 可纳入同一次仅显示修复的确认缺口

| 项 | 确认缺失 | 最小显示修复 |
|---|---|---|
| C2 27项目 +2接受选项 | 上述费用/地方/政治及双边费用 | 按上述闭包处理 |
| B2 `nesnd_small_specialise_button` | 已准确说12月、权威−25和市场取消条件；“资格增长提高”缺真实+10%（static_modifiers/nesnd_small_states.txt:6） | 只加原生 specialised_market 12月预览，保留现有精确 TT；不能说整项无反馈 |
| B2 `nesnd_small_own_market_button` | 本国已是真实市场主人时 helper 会立即尝试 start_public，而按钮只说“可承担公共投入”，未预览这条条件分支的12月实际费用/公共服务 | 仅在与 start_public 同一完整资格的只读分支下展示两个现有修正、正确当前报价；其他市场分支不显示实际扣费。不得承诺一律启动 |
| B2 `.10.organise/.10.suppress` | 已明确12月、权威−25/−50和激进派1%/2%，不可与 C2 泛话混同；运动支持幅度实际±15%未写，organise适格支持人物人气实际+10也只说“声望帮助” | 只补现有两个TT这两个明确数值；人物额外帮助必须保留“存在适格实际人物时”、12月，不新建人物、不改scope |
| A2 `nesnd_native_recognize` 的实际自行复统分支 | 现有TT准确说明恢复/申请两种政治动作，但自行复统隐藏120月 prestige+30、ruralfolk认可+3、建设+10% | 仅真实即时复统分支预览 restored_rule 120月；已有TWT的申请分支只显示申请，不预告立即奖励 |
| A2 `nesnd_native_suppress` | TT已有迁徙40%和失败留地，未说明本国原住民实际激进派+15%（effects:71）及真实接纳国60月迁徙吸引+25%（effects:24） | 只把现有TT补准这两项条件结果；接纳国依当次实际选择、不能拿不存在或预览未选中的 saved refuge 去读 |
| C1共享外交 `.1.a` kind2/3/5 | TT仅“按来函承诺”，事件正文只写协议/信用期限；实际kind3给sender72月 influence+100/prestige+25，kind2首次给60月建设+15%/制造吞吐+10%/技术传播+10%，kind5首次给60月建设+10%/技术传播+10%，且首次成功关系+25 | 外层合法saved对象+kind+首次receipt分支显示正确sender修正/期限；显示为“达成实际协议后”的条件后果，不把申请/许可说成已经有产业。不得改C1 helper，不能重新发奖；请求按钮可复用“对方接受且实际协议生效才获…”的准确TT |

以上额外项是具体源码反馈缺口，建议 root 批准到哪些文件后再编辑；它们不是原已通过外部矩阵的追溯失败。特别是 C1 必须只加显示分支，保持其原有后验成功/一次性receipt逻辑；若 root 仅批准 C2，本表其余留作记录，不抢写。

### 已足够或不归该类（保持）

- B1 material/political：原生费用/assistance预览 + 月度+0.50及0.1%激进派 TT、12月不可撤销；Ottoman军改按实际三个结果预览；72宣称按钮 TT 已明示耗25热情并原生展示实际州宣称。无需重写。
- B2 public：原生 weekly_quote 12月费用+public_services；五个改革承诺 TT 已明确实际法组、24月、IG+2；自治/独立/市场/防约请求明确双边同意与后验，不能为隐藏请求nonce加数值说明。
- A2 negotiate：已有原生地方议会36月 authority−100/ruralfolk+2，加准确压力−15说明；不得重复添泛话。合并申请不等于立即复统，军队/迁徙内务不能伪作当前按钮保证收益。
- C1 Egypt六投资按钮已有原生投资与各国具体产业修正预览、每月独立性−1 TT；AUS两按钮、USA边界均已有原生修正/关系或宣称数值，不能因 hidden helper 判漏。
- C2 retarget内部变量、拒绝/替代建议清理、人物receipt/永久dead控制、学术往返nonce不是新的财政/修正收益；不展示内务。学术接受段是已定人物资格，现有叙事记录即可，不新增承诺。
- 原生意大利兼容事件吞并前清除旧国意大利激进派是原生防链式吞并内务；不在此次窄显示修复中发明新的玩家奖励承诺。

## 批准后编辑/冻结/独立验证顺序

1. root裁定 C2必修及额外表的纳入项。编辑前保存当前已完成 final_standards 文案 SHA；只准删27desc重复尾巴/添加必需精确效果行，人物两本地化字节保留。
2. 仅显示脚本和只读值/必要双语，真实 `_start`、支付、modifier数据库、角色、生命周期、经营阈值、原三月逐厂、receipt、外交后验全部原 AST/数值保留。不得借显示工作修玩法。
3. 集中编辑后新时间戳独立freeze、显示diff与payload不变对照；停止READY_FOR_TEST，由独立测试者测试。
4. 未来独立测试应覆盖27选项目标缺失/有效/失地、已启动报价与GDP变化、报价缺失、三个既存修正、费用12月/地方24月/IG12月与真实DB逐项相符、无start预写变量的skip-write preview；双边两选项分别两国报价与saved对象失效。纳入表外项另按其真实分支验证，不能只看YML存在。不开游戏的报告只能STATIC/SOURCE，不宣称实际悬浮UI已验。

当前输出仅计划、源链与有界清单；没有新增行为测试或覆盖原冻结。
