Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/2026-11-14-invalid-concepts/`；工具 `nesnd-workbench/tools/fix_invalid_concepts.py`

# 96 地权革命悬停"民生与制度""本月民生统计"显示丢失

## 1. 现象与期望

作者原话：“民生与制度和民生统计键值双重丢失。检测，修复。”截图中地权革命日志另有一行 `states_greater_or_equal has no localization`。期望：两处悬停正常列出各项数值，条件列表不出现缺键文字。

## 2. 原因

- 两段悬停文字（`nesnd_land_rules`、`nesnd_cne_stability_detail_tt`，`nesnd_cne_land_reform_l_simp_chinese.yml`）都写了 `[concept_starving]`。1.15.1 里 `concept_starving` 只是本地化字符串，游戏概念是 `concept_starvation`，因此整段文字解析失败。
- 全 MOD 扫描共查出 8 个同类无效概念、91 处：starving、claims、interest_groups、loyalists、radicals、primary_culture、states、unemployment。原版没有对应的同名概念，只有本地化字符串。
- `num_states >= 4` 原版没有触发器本地化，直接显示 `states_greater_or_equal has no localization`。出处有三：`ce_cne_land_draft.txt:23`（完成条件）、`nesnd_cne_reform.txt:132`（复核按钮）、`nesnd_cne_programs.txt:2`。

## 3. 改了什么

- 中英 36 个本地化文件：`[concept_x]` 改为 `[Concept('<有效概念>','$concept_x$')]`。显示的词不变，链接改指有效概念。
- 上述三处脚本：改为 `custom_tooltip = { text = nesnd_cne_states_4_tt num_states >= 4 }`。
- `nesnd_cne_land_reform_l_*`：新增 `nesnd_cne_states_4_tt`，中文“拥有至少4个地区”，英文 "Owns at least 4 states."。

## 4. 怎么复测

以中华帝国读档或新开局，打开地权革命，悬停“本月民生统计”和完成条件里的“民生与制度条件”，应列出失业、饥饿、生活水平、市场接入等数值。条件列表应显示“拥有至少4个地区”。另抽查小国、波斯、西秦日志里的激进派、效忠派、利益集团链接是否正常。

## 5. 三角贸易按钮刷屏（同批处理）

- 现象：2026-11-13 00:44:55 控制台 `observe` 进入观察者模式，6 秒后 error.log 开始逐帧刷出北洋 6 个按钮 `visible` 的 `Scoped object of type 'country' is not valid (国家 （4294967295）)`，约 6,500 条。
- 原因：两个三角贸易日志由 `add_contextless_journal_entry` 挂出，按原版 `journal_entries.md`，这类日志的 root 是“正在查看的国家”。观察者没有国家，root 为空，按钮条件里的国家触发器全部报错。
- 改法：`common/scripted_buttons/nesnd_triangle_trade.txt` 12 个 `visible` 首行加 `exists = root`，与原版 `04_princely_states.txt:83` 用 `exists = ROOT` 判空同法。
- 未确认：报错行号指向 `visible = {` 本身。若引擎在进入块时就校验 root，这一守卫拦不住，需要观察者模式实测确认。

## 6. 检查

vic3-tiger 前后对比：改动文件新增报错 0，全 MOD 报告 3413 → 3321。Toolkit 语言服务器 6 个文件 0 诊断。static_lints：BOM、color 无问题。报告在 `nesnd-workbench/reports/2026-11-14-invalid-concepts/`。
