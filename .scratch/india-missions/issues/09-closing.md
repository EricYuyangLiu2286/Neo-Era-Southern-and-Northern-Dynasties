# 收尾：合并印度文件，全量代码与文本核验

Execution: completed  
Validation: STATIC_PASS  
Blocked by: none  
Evidence: 工作台 `reports/2026-11-21-india-development/收尾/交付记录.md`

印度线的最后一批，依据提示词 `prompts/07-收尾：合并与总核验.txt`。不加新功能，只合并、核验、改正。

## 合并

- 同一文件夹里的印度文件按组合成至多五个：core（原 core、reform）、matters（原 matters、foreign_affairs）、princes（原 diplomacy、projects、project、union、uprising、revolt）、empire（原 order、mughal）、foreign（原 frontier、overseas）。合并文件里每段以 `# ==== <标题> (formerly nesnd_india_<旧名>.txt) ====` 开头。事件三个文件，命名空间不变。本地化中英各五个，键序跟代码，两种语言顺序一致。
- 只有一个文件的文件夹不动：`customizable_localization/nesnd_india_projects.txt`，起义国的 coat_of_arms、country_definitions、diplomatic_plays、flag_definitions（`nesnd_india_uprising.txt`）。
- 同逻辑的定义合成带参数的：`nesnd_india_broke`、`nesnd_india_can_pay = { TEXT SUM }`、`nesnd_india_defence_possible = { FIRST SECOND YEARS }`、`nesnd_india_track_available/_visible`、`nesnd_india_sync_bar`、`nesnd_india_meter_tick`、`nesnd_india_matter_ai_asker_relations`、`nesnd_india_matter_refuse = { ROLE RESULT }`、`nesnd_mug_ask = { WHAT KIND AMOUNT }`、`nesnd_india_project_has_site`、`nesnd_india_project_offer_is`；南方起义六个地区的七组定义合成 `nesnd_india_case_*`（参数 R、STATE、TAG、HQ）。旧名到新名的全表在工作台 `收尾/键对照.tsv`。
- 变量没有改名。新加一个 `nesnd_india_project_build_clock`（本地项目第 4 阶段的三年期限）。旧存档里正在施工、没有这个变量的项目，第一次月度检查就会结束（新开局是验收基准，不写救档）。

## 核验与改正

- 代码：工作台 `收尾/代码核验.md`。待实机项改成「已按代码核验」，写在 03–08 各任务文件里。
- 改了的地方：本地项目施工期限；贸易特权加「两国都有自己的市场」的具名条件；自治领加宗主国类型与等级条件；中央与各邦撤约没生效时保留标记；违约担保文字改为有条件；两个回复事件和起义事件补 flavor 和效果提示；改选冷却提示不再读变量。
- 文字：三份审阅（工作台 `收尾/审阅/`）落到本地化，逐键记在 `收尾/文本改动.tsv`。禁用的说法在中文印度键里为 0；作者改过的 `nesnd_india_usm_reason`、`nesnd_india_diplomacy.1.d7` 中文未动，英文按中文对齐。
- 核对脚本：工作台 `收尾/verify_closing.py`（键对照、中英键序、引用的键都存在、没有无人引用的键、禁用词、变量清除），以及前七项的核对脚本（已改成读合并后的文件），全部通过。

## 没有做

- 开局给 MUG、BHU、NEP 自有市场（`grant_own_market`），让贸易特权开局就能签：交作者定。
- 日志「与法兰西的旧约」（`nesnd_mug_france`）名字写的是法兰西，脚本对任何非印度宗主国都成立：交作者定。
- 可选优化见 `代码核验.md` 第六节。

## 大陆会议副本要同步的文件

副本（工作台 `exports/continental-congress-session`）没有改。合入时要同步：删去旧的印度文件，换成合并后的文件。清单见交付记录第一节。
