Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Antigravity（2026-11-27，奥斯曼 B9 worktree）
Blocked by: none
Validation: STATIC_PASS
Evidence: 调研 `_agy_checks/调研.md`；推演 `_agy_checks/推演.md`；模拟 `_agy_checks/meso_sim.py` 与 `_agy_checks/meso_sim_result.txt`；交付说明 `_agy_checks/交付说明.md`；检查 `_agy_checks/summary.txt`、`_agy_checks/tree_diff.md` 与 `_agy_checks/grep6.txt`

# 129 奥斯曼 B9：两河（`nesnd_ottoman_meso`）

## 1. 现象与期望

开局巴格达（`STATE_BAGHDAD`）、摩苏尔（`STATE_MOSUL`）、巴士拉（`STATE_BASRA`）三区均在波斯将军府（`c:PER`，西秦朝贡国）手里，奥斯曼的成功线与失败线均有意收复两河，此前仅有「重整东方秩序」里的宣称按钮与战后「兵锋所向」事件，缺乏独立的对外日志、动态对手选法以及波斯一侧对两河失地的反攻应对。

本批（B9）按 F2「北方战争通用化」的范式，新增对外日志 `nesnd_ottoman_meso`（「两河」）：对手不写死国名，按三区州归属与最上层宗主动态选出并记入 `global_var:nesnd_meso_foe`（`c:PER` / `c:IRN` 仅作 R11 a 类 +10 历史加权）；两线共用入口（事件 `.5`/`.6` 与月度补加），设 3 枚按钮、3 则事件（`.23`–`.25`）、7 项按 R10/R12/R13 排序的结局（非隐藏结局不写 `event_outcome_desc`）；同步排除两河对手成为北方战争求援候选，并在 PER「重启远西战争」日志补上巴格达、摩苏尔、巴士拉三枚边界宣称按钮（R4）。中英新本地化键按规定全以 `TODO_CLAUDE` 占位，由主会话填写玩家文字。

## 2. 改了什么

- **新建两河日志、触发器、脚本值、效果、按钮、修正与自定义本地化**：
  - `common/scripted_triggers/nesnd_ottoman_meso.txt`：新建目标区判断、持地判断（`any_subject_or_below`）、候选与有效性、入口补加、东南快照失守、交战/博弈、局面已变、宣称与直接持有国等触发器。
  - `common/script_values/nesnd_ottoman_meso.txt`：新建对手计分（每州 +20、`c:PER`/`c:IRN` +10）与直接持州计数脚本值。
  - `common/scripted_effects/nesnd_ottoman_meso.txt`：新建选对手、东南快照、统一入口 `nesnd_ottoman_meso_start`、R13 失去自主月数维护、失地加宣称、划界放弃三区宣称、结局统一清理效果。
  - `common/journal_entries/nesnd_ottoman_meso.txt`：新建「两河」日志（无 `possible`/`is_shown_when_inactive`，240 个月自定义期限 `nesnd_ottoman_meso_deadline` 不截断交战，7 结局依次为东南失守、失去自主、收复两河、划界、局面已变、搁置、隐藏失效，三档 `status_desc`）。
  - `common/scripted_buttons/nesnd_ottoman_meso.txt`：新建「联络两河部族」（36 个月冷却，三区外手州加 `small_radicals`，与对手关系 −15，发 `.23`）、「定下东征方略」（限一次，需宣称，三区设 `conquer` 秘密目标，60 个月军需/征召修正）、「提议划界」（60 个月冷却，向对手发 `.24`）三枚按钮。
  - `common/static_modifiers/nesnd_ottoman_meso.txt`：新建 6 项静态修正（4 项结局永久修正、东征准备修正、两河增兵修正）。
  - `common/customizable_localization/nesnd_ottoman_meso.txt`：新建 `nesnd_ottoman_meso_foe_name`，从 `global_var:nesnd_meso_foe` 动态取对手名并带兜底键。
- **既有文件衔接**：
  - `common/on_actions/nesnd_ottoman_recovery.txt`：`on_monthly_pulse_country` 新增 `nesnd_ottoman_meso_fallback` 及上方注释，负责旧存档补加与 24 个月重开冷却到期后重开重选对手。
  - `events/nesnd_ottoman_recovery.txt`：事件 `.5` 与 `.6` 各选项补加调用 `nesnd_ottoman_meso_start`；文末新增 `.23`（两河告急，12 个月收件冷却，独立国隐藏求助宗主选项）、`.24`（提议划界，接受时奥斯曼放弃三区宣称、关系 +30、60 个月双向停战）、`.25`（奥斯曼收到划界回复）。
  - `common/scripted_triggers/nesnd_north.txt`：`nesnd_north_helper_candidate` 新增一行 `NOT = { global_var:nesnd_meso_foe ?= this }`。
  - `common/journal_entries/nesnd_per_campaign.txt`：`nesnd_per_west_journal` 挂入巴格达、摩苏尔、巴士拉三枚宣称按钮（不改结局条件）。
  - `common/scripted_buttons/nesnd_per_border_claims.txt`：文末照阿达纳按钮写法新增 `nesnd_per_claim_baghdad_button`、`nesnd_per_claim_mosul_button`、`nesnd_per_claim_basra_button`。
- **本地化占位**：
  - `localization/simp_chinese/replace/nesnd_ottoman_l_simp_chinese.yml`、`localization/english/replace/nesnd_ottoman_l_english.yml`：同步新增 64 对中英键（值均为 `TODO_CLAUDE`）。
  - `localization/simp_chinese/replace/nesnd_persia_l_simp_chinese.yml`、`localization/english/replace/nesnd_persia_l_english.yml`：同步新增 6 对中英键（3 个按钮名 + 3 个 `_effect_tt`，值均为 `TODO_CLAUDE`）。

## 3. 怎么复测

1. 坦志麦特成功（`.5`）与失败（`.6`）各测一局：核对选项执行后立即开出「两河」日志，开局 PER 仍为西秦朝贡国时对手为西秦（60 分），PER 独立后重开对手切换为波斯（70 分）。对已过 `.5`/`.6` 的旧存档推进一个月，核对 `nesnd_ottoman_meso_fallback` 正常补开。
2. 逐项验证 7 项结局与 R10 判序：同时失迪亚巴克尔并收复巴格达时先走东南失守；成为附属或失首都连续 12 个月走失去自主并设 24 个月重开冷却；三区全归奥斯曼及附属走收复两河并给重整东方秩序热情 +20；对手独立/被吞并/结盟时非交战状态走局面已变并 24 个月后重开；240 个月届满时若正与对手交战不截断，战后再结算搁置。
3. 测三枚按钮与事件 `.23`–`.25`：联络部族后三区非奥斯曼州加激进派、主要持有国收到 `.23`（独立国仅见 a/c，附属国见 a/b/c 且 b 给宗主加关系与 `protect`）；有宣称后点东征方略得 60 个月修正与 `conquer` 秘密目标；点提议划界对手收 `.24`，接受后放弃三区宣称、关系 +30、建 60 个月双向停战、奥斯曼收 `.25` 并次月走划界结局。
4. 测北方战争求援候选排除当前 `nesnd_meso_foe`；测 PER 在助秦西向路线下失巴格达/摩苏尔/巴士拉后，`nesnd_per_west_journal` 出现对应宣称按钮。

## 4. 遗留问题

- 本批所有新增本地化键均以 `TODO_CLAUDE` 占位，待主会话按 `_agy_checks/交付说明.md` 屏幕位置表填入中英正式文案（含 `nesnd_ottoman_meso_foe_name_active` 的 `[GetGlobalVariable('nesnd_meso_foe').GetCountry.GetName]`）。
- 结局变量 `nesnd_ottoman_meso_outcome`（`flag:lost` / `flag:dependent` / `flag:won` / `flag:demarcated` / `flag:changed` / `flag:shelved`）目前只写不读，留待后续批次读取。
- 与沙阿结盟分西秦（B13）、唐衣哈里发（B11）、埃及与黎凡特（B10）按任务规定不在本批范围。
