# 波兰线重做 · 第一批（修旧链）

2026-11-17。设计与作者决定见工作台 `reports/2026-11-17-poland-redesign/`：`content-tree-v2.md`（内容树与作者两轮回复）、`extensions-congress.md`（第二、三批的煽动、内战、大流亡、大陆会议）、`report.md`（旧链为什么不帮扩张、为什么无声消失）。

## 作者要求（本批相关）

- 方向三，三批递进；本批对应方向一：在旧系统上修，不新增日志。
- 1860 年结束（原生倒计时，到期弹事件）。
- 胜利条件由代理按地图定：首都在华沙（大波兰），完整拥有大波兰、马佐维亚、小波兰、西加利西亚、波森五州（1809 年华沙公国，波兰人过半的全部州）。
- 复国改回 POL，默认 +10 恶名；可以称王（成功事件给“迎回王冠”）。
- 瓜分结局偏向奥地利保护。英、瑞、西保留立场与日志。
- 10 个东部宣称按钮不退役。地图模式代替更多日志。合并 1.15.1 “派遣鼓动者”。

## 改了什么

| 文件 | 改动 |
|---|---|
| `common/journal_entries/ce_europe_poland_issude.txt` | 根日志：去掉 1850 年条件，`timeout = 8766`（到 1860-01-01）走新事件 16；新增两条进度条「和议的稳固」「法国的意志」；状态行按阶段（共识 / 动摇 / 决断）；地图模式（复国五州蓝／橙、其余可声索州浅红、KRA 有宣称的州斜纹、悬停说明主人与立场）；结局改为复国 / 瓜分（新，可见）/ 超时 / 失效，结局写全局结果变量 `nesnd_poland_result`。四个国家日志：去掉 `year >= 1850`，按结果变量各有可见结局（复国、瓜分、和议延续）；备战、阻击的分级修正改加在国家上（原来加在日志上、却从国家移除）；支持国日志挂上通牒按钮；加马佐维亚按钮 |
| `common/scripted_progress_bars/ce_poland_progress_bars.txt` | 新条两条；备战条去掉 GDP 排名与影响力四项（按大国标准，KRA 八个月只到 3），改为「与法国同在权力集团 +2」「陆军含征召兵 ≥20 营 +1」「法国意志 <30 −2」 |
| `common/scripted_buttons/ce_poland_scripted_buttons.txt` | 宣称、通牒按钮按模板重生成：去掉“宣称满 3 次才给 AI 权重”的死锁，按三档给权重（复国五州 / 其余波兰家园 / 旧联邦东部），第三档 +5 恶名；宣称按钮只在可宣称时显示，通牒按钮只对已宣称未持有的州显示；新增马佐维亚两个按钮；迁都按钮加 AI 权重（只在已持有五州时迁），迁后隐藏；「煽动支持者叛乱」的 `any_country` 条件包进具名提示（防刷屏） |
| `common/scripted_triggers|effects|script_values/nesnd_poland_repairs.txt` | 复国条件、五州与外围州判定、瓜分判定、结果变量；月度写入（担保数、法国意志、阶段）；结果与清理效果；法国意志读作者原作法兰西帝国链的稳定条（链结束后 70，波拿巴倒台后 20） |
| `events/ce_poland_events.txt` | 1：支持国可“抗议但维持支持”；2：让步的 AI 权重随法国意志与阶段变化；10：复国者 +10 恶名，三选一（迎回王冠 / 请法国承认新王冠 / 保持共和）；11：KRA 可请求奥地利保护（新事件 17）；13：去掉 “This is a bug” 兜底；16（新）：1860 年和议延续；97：“支持”不再删 KRA 宣称、不再立 200 年停战 |
| `events/poland_events.txt`、`common/scripted_buttons/00_christ_of_europe_buttons.txt` | 恢复 1.15.1 的 `poland_events.1/.2`（派遣鼓动者），修原版缺陷：按钮要求至少有一个目标国，`.1` 第一个选项补存在检查，事件内用完的选取标记当场清除，`.2` 只在目标国仍有波兰家园州时触发 |
| `common/on_actions/ce_code_on_actions.txt` | 不再在 KRA 消失时由月度回调先设结束变量（那样根日志会跳过可见的瓜分结局） |
| `common/journal_entry_groups/CE_journal_entries.txt` | 两个日志组改用原版闲置的 `je_group_illu_poland.dds` |
| 本地化 `ce_poland_l_*.yml`、`nesnd_button_tooltips_l_*.yml` | 新增 51 对中英键；通牒提示改为“吞并克拉科夫”（支持国也能发通牒）。作者原文未改 |

## 检查

STATIC_PASS（未启动游戏），已部署 `7fc648f6`。证据在工作台 `reports/2026-11-17-poland-redesign/batch1/`。

- `verify.py`：11 个文件可解析、BOM 与 CRLF 齐全；被引用的本地化键中英成对；事件、脚本触发器与效果均有定义。唯一残留 `ce_polish_claim_state_count_inverse` 是旧月度事件写的全局变量名，不是本地化键。
- `cliche_check.py`：新键中英各 51 条，命中 0。
- `loc_link_check.py`：全 MOD 0 条。
- `static_lints.py`：本链 `anyeq` 一条已修（另一条在注释掉的代码里）；`locsv`、`tipctx`、`deadhook` 0。
- `script_xcheck.py`：仅已知误报（`ai_chance` 的 `base/trigger/factor`）与原版代码。
- Toolkit 语言服务器：对照组（多一个右括号）未被检出，语言服务器未工作，本次结果无效。
- vic3-tiger 1.19.0 前后对比（`batch1/tiger2/`）：改动文件新增 5 条，都是 tiger 不认识的字段 `map_color`、`map_color_second`、`map_tooltip`、`illustration`。原版 1.15.1 的 12 个日志用前三个字段（人民之春、俄化、沙皇权威等），34 个日志组文件用 `illustration`，属 tiger 规则落后。第一轮报的 `$BAR$` 参数写在引号形式里，已按原版 `je_tsarpoints_add_partial` 改为 `scripted_bar_progress = { name = $BAR$ … }`，第二轮不再出现。

## 未经实机验证

- 地图模式的打开方式（按钮由引擎给）、配色与悬停。
- `timeout` 从 1836-01-01 计 8766 天是否正好在 1860 年初结束。
- `change_tag` 后国家变量是否保留（王冠三选项依赖 `nesnd_poland_restorer`）。
- 奥地利 `create_diplomatic_pact = { type = protectorate }` 对仍在法国集团中的 KRA 是否成立。
- 法国意志读取 `je:je_ce_unstable_imperium` 的进度条档位。
- AI 是否真的宣称、发通牒；“和议的稳固”的走势（目标约 1845±3 年进入动摇）。按技能要求，下一步按已部署的脚本写逐月模拟定数值。
- 旧存档：未做迁移。

## 遗留

- 第二批：红与白、煽动、内战选项、大流亡日志、ce_ 版欧洲宪兵（设计见 `content-tree-v2.md` §10、`extensions-congress.md`）。
- 第三批：窗口与大陆会议。
- 已存在 POL 时的“合并”路线留到第二批（随分离内战一起做），本批仍沿用旧的隐藏失效。
