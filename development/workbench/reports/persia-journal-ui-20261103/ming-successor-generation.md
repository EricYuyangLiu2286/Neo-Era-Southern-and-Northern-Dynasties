# 明宗室检索、补生与行辈研究（2026-11-03）

状态：只读源码研究／可实施提案；未改主 MOD、候选、存档或游戏进程，未做引擎验收。当前本体为 1.13.11 / Steam build 24799966；本轮 catalog status = CURRENT，changed_count = 0。使用 NESND、NESND 玩家文本与 Matt research 工作流；本文件由背景研究代理产出。

## 结论与最新授权

最新作者要求取代先前“不再创建人物”的兜底：先尽力找回任何合格的现存明宗室，检索确实落空后可以创建一位新的宗室。新人物不是复活朱阔彬、朱作煜，也不能重用他们的历史模板来冒充后人。活着的外国君主及其指定继承人不被强行夺走。

作者本人的旧项目已有两支行辈和完整名字池，不能把所有朱氏混成宁王系：

| 场景 | 可证世系 | 本轮可用顺序 | 证据 |
| --- | --- | --- | --- |
| 召回原明天子、原明太子；两者及可用宗室均不在时补生 | 宁王／朱权系 | **阔 → 作 → 哲 → 向 → 亲 → 衷** | S01:494–515、656–715；S03:513–547；S04:3–4 |
| GNG 淮藩保留自己的朱氏；本宗无人可用时补生 | 淮王／朱棣（燕王）系 | **仲 → 简 → 靖 → 迪 → 先 → 猷** | S02:177–198、241–300；S03:746–778；S05；S06 slide 9 p6 |

S01 是作者旧文案，但发生系统性字符置换，例如“作”显示为“佛”。不能把整份文件当准确的现代中文。此次“作”的恢复有本 MOD 原始模板 `USM_zhu_zuoyu` 与 `Zuoyu: 作煜` 直接相互证明；哲、向、亲、衷在该文件的族谱、选项和名字池三处一致。**没有查到衷之后、猷之后的作者行辈；不循环回阔、不自行续诗。**

S06 原稿写明“淮王系（朱棣后人，北明淮国）和江西宁王系（朱权后人）宗室交叠为主”。这也是 GNG 不应召回外部宁系君主、也不应把本宗新人物改成“阔”字辈的依据。

最新存档证据 S07 中，3146 = Kuobing / Zhu / USM_zhu_kuobing，3147 = Zuoyu / Zhu / USM_zhu_zuoyu，均在 country 309（HNA）。3146 的角色为 magnate + Ming refuge，3147 为 Ming refuge；都没有死亡标记。它们是现存旧帝、旧太子的同一人物，不能因为没有 ruler/heir 角色而认作不存在。这个实际案例应走召回路径，不应创建兜底人物。

## 先查全链：原 MOD 与当前本体

原 MOD 法国：`common/journal_entries/ce_french_empire.txt:560` → `ce_set_orleanist_ruler`（S08:1020）→ 先找家族首领/历史人物 → `create_character` 通用家族人物（1140–1159），`on_created` 加家族变量并设为君主。`ce_find_bonaparte_in_exile_effect`（2437–2587）还依次查本国、全球非流亡、全球流亡。借鉴的是“优先现存人物，最后生成家族新人”的结构；不沿用它对外国人物直接流放等不适合本轮的动作。

原 MOD 日本：S09:1–81 依次查本国、全球、流亡池；S09:314–350 随机丰臣氏将军用 `last_name`、`female`、`culture`、`age`、`on_created`；S09:355–391 用 `heir_komei_spawned` 等变量防重复。**旧日本代码 74–77 在全球存在但不在流亡池时仍重新创建同模板，有复制人物风险，不照搬。**

当前本体日本：S10:1069–1076 的国家脉冲 → `can_generate_scripted_heirs`（S11:617–632，君主制且无历史继承人）→ S12 `japan_generate_scripted_heirs` → `JAP_komei_yamato`（S14）→ DNA（S15）及自动 ruler/heir roles（S16）。S12:79–90 另使用 `is_template_used` 防止历史模板重复生成，支持“使用过的历史模板不能拿来造后人”的处理。

当前本体法国：S13:1933–1946 `summon_napoleon_the_woat` 使用全球 `any_character/random_character`，调用未知状态人物转移；S13:2028–2056 `country_summon_heir_effect` 是“找现存人物，否则创建，再 set_heir”。S13:2059–2085 / 2105–2126 先 `free_character_from_void`，流亡者 `transfer_character` 后 `free_from_exile_effect`，再处理任职。**该原生 helper 后半段允许外国君主相关特殊关系，不整段调用；只重用已证实的虚空/流亡操作，并加本轮外国君主保护。**

引擎文档 S17/S18 明确：`any_character`、`every_character`、`random_character` 是全球人物列表，另有 exile_pool 和 void 列表。当前法国源码也依赖全球查询找到未知状态人物。仍建议在本轮生成前显式补查 exile/void 两列表，一方面满足“尽力寻找”，一方面避免把工具层对 global 的理解当作实际存档覆盖保证。

## 身份、资格与选择顺序

1. 每次入口先保存 `scope:nesnd_postwar_winner`，清掉本次临时 selected scopes。所有转移、归属比较使用该 saved country scope，不依赖多层 `root` 猜测。
2. 独立修复旧帝和旧太子的身份：分别检索原模板与 `this_is_zhukuobin_var` / `this_is_zhuzuoyu_var`。现有布尔 `nesnd_ming_original_identity_recorded` 不能阻止另一个人的身份恢复；单一布尔只说明至少记录过一个人。
3. 再检查各国保存的 claimant/heir/refuge 引用；引用存在后还必须检查存活和合法血统。引用只帮助找到既有人物，不能凭一个失效引用创造同名人物。
4. HNA/SIH 的优先级：原旧帝 → 原旧太子 → 具有明确 provenance 的同系宗室／合法后人 → 其他合格的已认证明宗室。每一档先本国，再全球可调动人物，再显式 exile、void 补查；每档只在尚未选出人时执行。**原旧帝、原旧太子的优先级是全球优先，不能让本地普通宗室截走在外国流亡的原君主。**
5. GNG：本国当前合法朱氏 ruler → 本国合法 heir → 本国其他已证淮/燕系宗室 → 因流亡、虚空、普通任职而离开的本宗现存人物。外国在位君主与外国 heir 不动；不调用宁系旧帝召回。确实没有合格本宗人物才在 GNG 生成人物。
6. “所有姓朱的人”不是合法候选。现有 `nesnd_ming_authorized_dynast` 的明确历史模板与 `nesnd_ming_dynastic_verified` 是合法性入口；新一代还要有 `nesnd_ming_ning_line` / `nesnd_ming_huai_line` 区分世系。不要靠文化、单姓、领土所在或出生地反推皇族。
7. 旧档中只有泛 `nesnd_ming_dynastic_verified` 而没有世系标记的人可以保持已认证宗室资格，但不强行猜测其行辈、更不改名。宁系可由原旧帝/旧太子模板准确恢复；淮系可由 GNG 两个历史模板准确恢复。已证的出生回调可以给后代复制父辈世系。

资格 trigger（character scope；调用前必须保存 winner）：

```text
nesnd_ming_recruitable_royal = {
    is_character_alive = yes
    nesnd_ming_authorized_dynast = yes
    trigger_if = {
        limit = { exists = owner }
        OR = {
            owner = scope:nesnd_postwar_winner
            NOR = {
                is_ruler_of_own_country = yes
                is_heir_of_own_country = yes
            }
        }
    }
}
```

生成前最后的“不存在可调动人” guard 应做三个集合的 NOR，选择和 guard 使用完全相同的合法性 trigger。这里的两个专门列表不是新的逻辑资格：

```text
NOR = {
    any_character = { nesnd_ming_recruitable_royal = yes }
    any_character_in_exile_pool = { nesnd_ming_recruitable_royal = yes }
    any_character_in_void = { nesnd_ming_recruitable_royal = yes }
}
```

GNG 在三个查询里额外要求 `nesnd_ming_huai_line` 或 `USM_zhu_zhongying / USM_zhu_jingyin`，不能用泛明宗室 guard 锁死本宗补生。存在但受保护的外国君主不构成可调动人，也不会被复制。

## 补生的字段、DNA与任职

`create_character` 是 country effect。S17:845–865 明列 `first_name/last_name`、culture、religion、female、noble、ruler/heir、age（整数或范围）、historical、template、on_created、save_scope_as。`set_first_name` 只接受一个 loc key；不能拼接字符串或把本地化显示名作为脚本身份。

下例是字段层面完整的宁系新宗室实例，21 岁取原 MOD 法国通用家族人的相同基线。人物年龄与性别是本轮玩法提案，不是作者已写出的具体人物生平。省略 DNA：原作者朱阔彬、朱作煜本来就没有固定 DNA；`ce_wuu` 定义 `ethnicities={1=asian}`、`graphics=east_asian`、`name_format=last_first`、宗教 kaimeng_confucianism（S19:1564–1570、1642–1645），会沿文化生成肖像。不要复制旧帝的固定外观来暗示复活。

```text
# Country scope; winner and the chosen generation/name slot already fixed.
create_character = {
    first_name = nesnd_ming_ning_zhekun
    last_name = Zhu
    female = no
    noble = yes
    historical = no
    age = 21
    culture = cu:ce_wuu
    interest_group = ig_landowners
    ideology = ideology_traditionalist
    on_created = {
        set_variable = nesnd_ming_dynastic_verified
        set_variable = nesnd_ming_generated_dynast
        set_variable = nesnd_ming_ning_line
        set_variable = { name = nesnd_ming_generation value = 2 }
        set_variable = nesnd_ming_name_ning_zhekun
        save_scope_as = nesnd_postwar_original_royal
        set_character_as_ruler = yes
    }
}
```

使用当前胜国已切换到君主制后的 country scope；GNG 替换为 `culture=cu:ce_xinan`、`nesnd_ming_huai_line`、`dizhao` 等本宗名称。先设置身份变量，再 `set_character_as_ruler`，完成后核验 `ruler ?= scope:nesnd_postwar_original_royal` 才提交 settlement。不附带创建一位无依据的假历史太子；已有合法本国太子优先保留，可调用原生 `set_heir` 指向已确认人物。

本体的固定 DNA 链是 `create_character template` → `common/character_templates/country_jap.txt dna=dna_emperor_komei` → `common/dna_data/00_emperor_komei.txt`。本轮无需新增该链。未找到当前 effect docs 中直接在 `create_character` 动态复制任意人的 DNA 的接口，不提出这种写法。角色 UI 由 S16 的 ruler/heir 自动角色与原生 icon/title 支持，不需自建新 ruler/heir role。

## 行辈与重入记账

建议宁系索引 0=阔、1=作、2=哲、3=向、4=亲、5=衷；淮系索引 0=仲、1=简、2=靖、3=迪、4=先、5=猷。两支用独立 global 高水位变量和独立姓名使用标记，不能共用一个全国代数。

旧档首次补生前：

- `nesnd_ming_ning_generation_highwater` 缺失时设 1（1836 已有作煜），`nesnd_ming_huai_generation_highwater` 缺失时设 2（1836 已有靖堙）。这两个是作者开局人名事实，不是按当前年份猜代数。之后扫描所有有明确世系与数值 `nesnd_ming_generation` 的活人，取更高值；每次读取数值前先有 `has_variable/has_global_variable` guard。
- 新补生取该系高水位 + 1，上限 5。所以旧帝、太子及所有合格宗室均不在的普通旧档宁系首位新人取哲；GNG 本宗都不在时取迪。不要每次从阔或仲重新开始，也不要每一次打开预览就推进索引。
- 高水位只在成功 `on_created` 且人物成为目标国 ruler 后提交。人物自身的世系、代数、generated 标记永久保留。检索可以重新找到刚创建但尚未完成结算的人，避免失败重试再创建。
- `nesnd_rebel_settlement_seen` / 全球结算锁仍为主幂等保护。新增 country `nesnd_ming_generation_in_progress` 可设 `days=1`：生成前设，成功清；仅失败路径保留一天退避。全局 `nesnd_ming_generation_cooldown` 也用 `days=1` 防同一 tick 的重复入口。S17 明确变量支持 days；**不能用 cooldown 代替实际人物检索，不能把“生成开始”永久当成成功。**
- 预览 trigger 和可选项不执行生成、不写高水位。最终 effect 重新检查国家存在、settlement 可提交、目标缺失、三个角色集合，防候选选择期间的状态变化。
- 衷／猷之后没有来源：到索引5后只能选该最后已证行辈中尚未使用的名字，作为**同辈旁支**，不能声称已推进一代。自然子代是否继续按行辈命名属于源码尚缺的末端规则，不编造新一代。若最终一辈名字池耗尽，允许新 generated 人物在无存活同名者时再用池内名字，拥有新 serial/出生时间/人物ID，绝不重用历史 template；这是同辈旁支命名复用，并非死者复活。该极端规则应在内部记录，不能将同名误当同一人。

本轮若要把生成家系延续到自然出生者，现有 `common/on_actions/nesnd_ming_dynasty.txt` 只给 USM/nesnd_ming_court 的后代写泛认证，HNA/SIH/GNG恢复后的后代可能漏记。当前 GAME `on_heir_born` 明确 ROOT=Character（S10:6751–6753），可在原生出生回调中，先确认 owner/ruler 存在且 ruler 有明确世系，再复制世系与 parent generation + 1；不要用固定国家名直接给任何新 heir 认证。不要改名已存活的历史人物；只处理本次新出生且未写行辈的随机 heir。索引5末端不自行推演后续诗。该钩子建议与本轮生成闭包一同修，不替换整个原生 `on_heir_born`。

## 名字池与中英文键

全部下列中文均来自作者旧项目名字池；仅将损坏的“佛”按原 MOD `作煜` 还原为“作”。英文是本轮拼音本地化。完整名由已有 `Zhu` 姓 + 新 `first_name` loc key 组成；不用重定义 `Kuobing`、`Zuoyu`、`Jingyin`、`Zhongying` 等旧键。下表每格列四个可立即采用的完整名字，足够本轮补生；S01/S02 的完整池可扩到每代10个，重复“哲坚”只保留一次。

| 世系/索引 | 中文 first_name 候选 | 英文 first_name | 新 key 前缀 | 原文 |
| --- | --- | --- | --- | --- |
| 宁0 阔 | 阔梁、阔槐、阔棠、阔槿 | Kuoliang, Kuohuai, Kuotang, Kuojin | nesnd_ming_ning_ | S01:657–665 |
| 宁1 作 | 作烨、作灿、作煦、作煐 | Zuoye, Zuocan, Zuoxu, Zuoying | nesnd_ming_ning_ | S01:666–673 |
| 宁2 哲 | 哲坤、哲塘、哲均、哲基 | Zhekun, Zhetang, Zhejun, Zheji | nesnd_ming_ning_ | S01:676–681 |
| 宁3 向 | 向钦、向铉、向铎、向铭 | Xiangqin, Xiangxuan, Xiangduo, Xiangming | nesnd_ming_ning_ | S01:686–690 |
| 宁4 亲 | 亲治、亲浩、亲清、亲澄 | Qinzhi, Qinhao, Qinqing, Qincheng | nesnd_ming_ning_ | S01:696–704 |
| 宁5 衷 | 衷梁、衷槐、衷棠、衷槿 | Zhongliang, Zhonghuai, Zhongtang, Zhongjin | nesnd_ming_ning_ | S01:707–715 |
| 淮2 靖 | 靖坤、靖塘、靖均、靖垣 | Jingkun, Jingtang, Jingjun, Jingyuan | nesnd_ming_huai_ | S02:261–265 |
| 淮3 迪 | 迪钊、迪锋、迪锐、迪钧 | Dizhao, Difeng, Dirui, Dijun | nesnd_ming_huai_ | S02:271–275 |
| 淮4 先 | 先流、先浩、先清、先澄 | Xianliu, Xianhao, Xianqing, Xiancheng | nesnd_ming_huai_ | S02:281–289 |
| 淮5 猷 | 猷梁、猷棱、猷松、猷桐 | Youliang, Youleng, Yousong, Youtong | nesnd_ming_huai_ | S02:293–299 |

例如 `nesnd_ming_ning_zhekun: "哲坤"` / `"Zhekun"`；`nesnd_ming_huai_dizhao: "迪钊"` / `"Dizhao"`。两种语言均 UTF-8 BOM，放独立 `replace` 文件。名字选取使用明确 `random_list` 分支／明确 loc key；不能把 `first_name` 写为需要运行时拼接的世代+后缀表达式。名字使用标记是脚本身份附加信息，不显示在人物姓名里。

文字审查：类别为人物姓名，不新增事件演说。作者原始对照是 S04 的“阔彬／作煜／仲桯／靖堙”与 S01/S02 的原作者族谱命名；候选沿用“姓朱＋行辈＋单字名”和对应木火土金水名字池。判断：来源与句式通过；“作”文字修复有第二原始来源支撑。中文新人物身份是玩法分支，不冒充作者小说中既有具体人物。

## 实施后外部检查与明确未验证点

必须覆盖以下静态场景：3146/3147仍活着但没有 ruler/heir role；旧帝死、旧太子活；现存人物在普通别国、exile、void；人物是外国 ruler/heir；旧档只有模板/旧变量没有新 flag；高水位变量缺失；同一结算重复调用；生成成功但后续步骤中断；GNG现任合法朱氏存在；GNG本宗继承人在国外执政；GNG无人且宁系旧帝仍活着。验证预期是同一现存ID优先，不改变受保护外国人物，不重用历史模板，新人物只出现一次且已成为胜国ruler。

本次仅源码可证，未用游戏运行证明任意一种边界。`any_character` 对所有死者保留记录的覆盖不作假设：是否已用历史模板用 `is_template_used`，存活资格用 `is_character_alive`。世系标记的继承、出生回调的次序、连续两次结算的实际重入，仍需真实存档证据或用户下一次运行日志；不得称 ENGINE_PASS。

## 原始来源、SHA-256与关键摘录

下列指纹由本轮直接从只读原件计算；PPT hash 与缓存 JSON 的 source hash 一致。后续来源变更时应重查该条，不把旧行号当当前源码。

### S01

文件：[CE_Greatming_missions_l_english.yml](<D:/Users/Eric Liu/Desktop/paratranz/decoded/CE_Greatming_missions_l_english.yml>)

SHA-256：`fec65a7bd4dccaf1b6113624b85cb08933f23bb4ee0f36c1e9dfaae819ce170c`


494–495：

```text
494:  CE_ming_missions_events.80.t:0 "宁王系族谱"
495:  CE_ming_missions_events.80.d:0 "磐奠觐宸拱，多谋统议中；怺添攮庶阔，佛哲向亲衷。"
```


510–515：

```text
510:  CE_ming_missions_events.80.15:0 "选择“阔”字辈"
511:  CE_ming_missions_events.80.16:0 "选择“佛”字辈"
512:  CE_ming_missions_events.80.17:0 "选择“哲”字辈"
513:  CE_ming_missions_events.80.18:0 "选择“向”字辈"
514:  CE_ming_missions_events.80.19:0 "选择“亲”字辈"
515:  CE_ming_missions_events.80.20:0 "选择“衷”字辈"
```


656–715：

```text
656:  CE_ming_missions_events.95.1:0 "就叫“阔檄”吧"
657:  CE_ming_missions_events.95.2:0 "就叫“阔梁”吧"
658:  CE_ming_missions_events.95.3:0 "就叫“阔槐”吧"
659:  CE_ming_missions_events.95.4:0 "就叫“阔棠”吧"
660:  CE_ming_missions_events.95.5:0 "就叫“阔极”吧"
661:  CE_ming_missions_events.95.6:0 "就叫“阔相”吧"
662:  CE_ming_missions_events.95.7:0 "就叫“阔柔”吧"
663:  CE_ming_missions_events.95.8:0 "就叫“阔柒”吧"
664:  CE_ming_missions_events.95.9:0 "就叫“阔枚”吧"
665:  CE_ming_missions_events.95.10:0 "就叫“阔槿”吧"
666:  CE_ming_missions_events.96.1:0 "就叫“佛烨”吧"
667:  CE_ming_missions_events.96.2:0 "就叫“佛烑”吧"
668:  CE_ming_missions_events.96.3:0 "就叫“佛炷”吧"
669:  CE_ming_missions_events.96.4:0 "就叫“佛灿”吧"
670:  CE_ming_missions_events.96.5:0 "就叫“佛燃”吧"
671:  CE_ming_missions_events.96.6:0 "就叫“佛炼”吧"
672:  CE_ming_missions_events.96.7:0 "就叫“佛煦”吧"
673:  CE_ming_missions_events.96.8:0 "就叫“佛煐”吧"
674:  CE_ming_missions_events.96.9:0 "就叫“佛燨”吧"
675:  CE_ming_missions_events.96.10:0 "就叫“佛灵”吧"
676:  CE_ming_missions_events.97.1:0 "就叫“哲坤”吧"
677:  CE_ming_missions_events.97.2:0 "就叫“哲塘”吧"
678:  CE_ming_missions_events.97.3:0 "就叫“哲坚”吧"
679:  CE_ming_missions_events.97.4:0 "就叫“哲均”吧"
680:  CE_ming_missions_events.97.5:0 "就叫“哲垢”吧"
681:  CE_ming_missions_events.97.6:0 "就叫“哲基”吧"
682:  CE_ming_missions_events.97.7:0 "就叫“哲坚”吧"
683:  CE_ming_missions_events.97.8:0 "就叫“哲圢”吧"
684:  CE_ming_missions_events.97.9:0 "就叫“哲垒”吧"
685:  CE_ming_missions_events.97.10:0 "就叫“哲墨”吧"
686:  CE_ming_missions_events.98.1:0 "就叫“向钦”吧"
687:  CE_ming_missions_events.98.2:0 "就叫“向锥”吧"
688:  CE_ming_missions_events.98.3:0 "就叫“向铉”吧"
689:  CE_ming_missions_events.98.4:0 "就叫“向铎”吧"
690:  CE_ming_missions_events.98.5:0 "就叫“向铭”吧"
691:  CE_ming_missions_events.98.6:0 "就叫“向钏”吧"
692:  CE_ming_missions_events.98.7:0 "就叫“向铃”吧"
693:  CE_ming_missions_events.98.8:0 "就叫“向钗”吧"
694:  CE_ming_missions_events.98.9:0 "就叫“向镮”吧"
695:  CE_ming_missions_events.98.10:0 "就叫“向锦”吧"
696:  CE_ming_missions_events.99.1:0 "就叫“亲治”吧"
697:  CE_ming_missions_events.99.2:0 "就叫“亲浩”吧"
698:  CE_ming_missions_events.99.3:0 "就叫“亲深”吧"
699:  CE_ming_missions_events.99.4:0 "就叫“亲清”吧"
700:  CE_ming_missions_events.99.5:0 "就叫“亲渉”吧"
701:  CE_ming_missions_events.99.6:0 "就叫“亲澜”吧"
702:  CE_ming_missions_events.99.7:0 "就叫“亲沫”吧"
703:  CE_ming_missions_events.99.8:0 "就叫“亲浅”吧"
704:  CE_ming_missions_events.99.9:0 "就叫“亲澄”吧"
705:  CE_ming_missions_events.99.10:0 "就叫“亲漓”吧"
706:  CE_ming_missions_events.100.1:0 "就叫“衷檄”吧"
707:  CE_ming_missions_events.100.2:0 "就叫“衷梁”吧"
708:  CE_ming_missions_events.100.3:0 "就叫“衷槐”吧"
709:  CE_ming_missions_events.100.4:0 "就叫“衷棠”吧"
710:  CE_ming_missions_events.100.5:0 "就叫“衷极”吧"
711:  CE_ming_missions_events.100.6:0 "就叫“衷相”吧"
712:  CE_ming_missions_events.100.7:0 "就叫“衷柔”吧"
713:  CE_ming_missions_events.100.8:0 "就叫“衷柒”吧"
714:  CE_ming_missions_events.100.9:0 "就叫“衷枚”吧"
715:  CE_ming_missions_events.100.10:0 "就叫“衷槿”吧"
```

### S02

文件：[CE_Greatming_missions_l_english.yml](<D:/Users/Eric Liu/Desktop/paratranz/paratranz/decoded/CE_Greatming_missions_l_english.yml>)

SHA-256：`efb1a42ab475db1b214e07df6858c88f724cca88b6e7e9c9e60c37275d759646`


177–198：

```text
177:  CE_ming_missions_events.36.1:0 "明朝燕王系"
178:  CE_ming_missions_events.37.t:0 "燕王系族谱"
179:  CE_ming_missions_events.37.d:0 "高瞻祁见佑，厚载翊常由；慈和怡伯仲，简靖迪先猷"
180:  CE_ming_missions_events.37.1:0 "选择“瞻”字辈"
181:  CE_ming_missions_events.37.2:0 "选择“祁”字辈"
182:  CE_ming_missions_events.37.3:0 "选择“见”字辈"
183:  CE_ming_missions_events.37.4:0 "选择“佑”字辈"
184:  CE_ming_missions_events.37.5:0 "选择“厚”字辈"
185:  CE_ming_missions_events.37.6:0 "选择“载”字辈"
186:  CE_ming_missions_events.37.7:0 "选择“翊”字辈"
187:  CE_ming_missions_events.37.8:0 "选择“常”字辈"
188:  CE_ming_missions_events.37.9:0 "选择“由”字辈"
189:  CE_ming_missions_events.37.10:0 "选择“慈”字辈"
190:  CE_ming_missions_events.37.11:0 "选择“和”字辈"
191:  CE_ming_missions_events.37.12:0 "选择“怡”字辈"
192:  CE_ming_missions_events.37.13:0 "选择“伯”字辈"
193:  CE_ming_missions_events.37.14:0 "选择“仲”字辈"
194:  CE_ming_missions_events.37.15:0 "选择“简”字辈"
195:  CE_ming_missions_events.37.16:0 "选择“靖”字辈"
196:  CE_ming_missions_events.37.17:0 "选择“迪”字辈"
197:  CE_ming_missions_events.37.18:0 "选择“先”字辈"
198:  CE_ming_missions_events.37.19:0 "选择“猷”字辈"
```


261–300：

```text
261:  CE_ming_missions_events.44.1:0 "就叫“靖坤”吧"
262:  CE_ming_missions_events.44.2:0 "就叫“靖塘”吧"
263:  CE_ming_missions_events.44.3:0 "就叫“靖坚”吧"
264:  CE_ming_missions_events.44.4:0 "就叫“靖均”吧"
265:  CE_ming_missions_events.44.5:0 "就叫“靖垣”吧"
266:  CE_ming_missions_events.44.6:0 "就叫“靖壑”吧"
267:  CE_ming_missions_events.44.7:0 "就叫“靖坛”吧"
268:  CE_ming_missions_events.44.8:0 "就叫“靖圣”吧"
269:  CE_ming_missions_events.44.9:0 "就叫“靖垒”吧"
270:  CE_ming_missions_events.44.10:0 "就叫“靖墨”吧"
271:  CE_ming_missions_events.45.1:0 "就叫“迪钊”吧"
272:  CE_ming_missions_events.45.2:0 "就叫“迪钒”吧"
273:  CE_ming_missions_events.45.3:0 "就叫“迪锋”吧"
274:  CE_ming_missions_events.45.4:0 "就叫“迪锐”吧"
275:  CE_ming_missions_events.45.5:0 "就叫“迪钧”吧"
276:  CE_ming_missions_events.45.6:0 "就叫“迪钟”吧"
277:  CE_ming_missions_events.45.7:0 "就叫“迪钰”吧"
278:  CE_ming_missions_events.45.8:0 "就叫“迪镜”吧"
279:  CE_ming_missions_events.45.9:0 "就叫“迪钗”吧"
280:  CE_ming_missions_events.45.10:0 "就叫“迪钏”吧"
281:  CE_ming_missions_events.46.1:0 "就叫“先流”吧"
282:  CE_ming_missions_events.46.2:0 "就叫“先浩”吧"
283:  CE_ming_missions_events.46.3:0 "就叫“先涿”吧"
284:  CE_ming_missions_events.46.4:0 "就叫“先清”吧"
285:  CE_ming_missions_events.46.5:0 "就叫“先渊”吧"
286:  CE_ming_missions_events.46.6:0 "就叫“先澜”吧"
287:  CE_ming_missions_events.46.7:0 "就叫“先沫”吧"
288:  CE_ming_missions_events.46.8:0 "就叫“先浅”吧"
289:  CE_ming_missions_events.46.9:0 "就叫“先澄”吧"
290:  CE_ming_missions_events.46.10:0 "就叫“先淼”吧"
291:  CE_ming_missions_events.47.1:0 "就叫“猷相”吧"
292:  CE_ming_missions_events.47.2:0 "就叫“猷栎”吧"
293:  CE_ming_missions_events.47.3:0 "就叫“猷梁”吧"
294:  CE_ming_missions_events.47.4:0 "就叫“猷棱”吧"
295:  CE_ming_missions_events.47.5:0 "就叫“猷松”吧"
296:  CE_ming_missions_events.47.6:0 "就叫“猷枭”吧"
297:  CE_ming_missions_events.47.7:0 "就叫“猷槐”吧"
298:  CE_ming_missions_events.47.8:0 "就叫“猷梵”吧"
299:  CE_ming_missions_events.47.9:0 "就叫“猷桐”吧"
300:  CE_ming_missions_events.47.10:0 "就叫“猷檬”吧"
```

### S03

文件：[historical_leaders_ce_asia.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/character_templates/historical_leaders_ce_asia.txt>)

SHA-256：`90dbd0ad6d7191c5639c86bb8688ad73fbdedb21ebcf0d89381ac07c168aff67`


513–547：

```text
513: USM_zhu_kuobing = {
514: 	# 朱阔椕
515: 	#role = politician # Remove this line
516: 	first_name = "Kuobing"
517: 	last_name = "Zhu"
518: 	ruler = yes
519: 	age = 36
520: 	culture = cu:ce_wuu
521: 	interest_group = ig_landowners
522: 	ideology = ideology_traditionalist
523: 	home_region = STATE_JIANGXI
524: 	traits = {
525: 		cautious
526: 	}
527: 	on_created = {
528: 		set_variable = this_is_zhukuobin_var
529: 	}
530: }
531: USM_zhu_zuoyu = {
532: 	# 朱作煜
533: 	#role = politician # Remove this line
534: 	first_name = "Zuoyu"
535: 	last_name = "Zhu"
536: 	heir = yes
537: 	age = 10
538: 	culture = cu:ce_wuu
539: 	interest_group = ig_petty_bourgeoisie
540: 	ideology = ideology_traditionalist
541: 	home_region = STATE_JIANGXI
542: 	traits = {
543: 		reserved
544: 	}
545: 	on_created = {
546: 		set_variable = this_is_zhuzuoyu_var
547: 	}
```


746–778：

```text
746: USM_zhu_jingyin = {
747: 	# 朱靖堙
748: 	#role = politician # Remove this line
749: 	first_name = "Jingyin"
750: 	last_name = "Zhu"
751: 	noble = yes
752: 	heir = yes
753: 	birth_date = 1818.2.20
754: 	home_region = STATE_GUANGXI
755: 	culture = cu:ce_xinan
756: 	interest_group = ig_petty_bourgeoisie
757: 	ideology = ideology_traditionalist
758: 	traits = {
759: 		direct
760: 	}
761: }
762: 
763: USM_zhu_zhongying = {
764: 	first_name = "Zhongying"
765: 	last_name = "Zhu"
766: 	noble = yes
767: 	ruler = yes
768: 	age = 68
769: 	culture = cu:ce_xinan
770: 	home_region = STATE_SICHUAN
771: 	interest_group = ig_landowners
772: 	ideology = ideology_traditionalist
773: 	traits = {
774: 		arrogant
775: 	}
776: 	on_created = {
777: 		set_variable = is_married
778: 	}
```

### S04

文件：[ce_names_l_simp_chinese.yml](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_names_l_simp_chinese.yml>)

SHA-256：`db6cc2bfa6cb5ae0eafab0cfb4c901798f68f30193bd2abe3be47e0818846784`


1–12：

```text
1: l_simp_chinese:
2:  Ming_Zhu: "朱"
3:  Kuobing: "阔彬"
4:  Zuoyu: "作煜"
5:  ce_Zuo: "左"
6:  Zongtang: "宗棠"
7:  Jiangchen: "绛臣"
8:  Zhongying: "仲桯"
9:  Yigong: "怡钒"
10:  Shenhui: "深橞"
11:  Jingyin: "靖堙"
12:  Mu: "牧"
```

### S05

文件：[GNG.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/history/characters/GNG.txt>)

SHA-256：`37ea6c96b197a042abd7cc3d2cd28ce05f0dbdd2414c982409e477037a7f13c1`


1–16：

```text
1: CHARACTERS = {
2: 	c:GNG ?= {
3: 		create_character = {
4: 			# 朱仲桯
5: 			#role = politician # Remove this line
6: 			template = USM_zhu_zhongying
7: 			ruler = yes
8: 		}
9: 		
10: 		create_character = {
11: 			template = USM_zhu_jingyin
12: 			heir = yes
13: 		}
14: 		
15: 		
16: 	}
```

### S06

文件：[北明ppet.pptx](<D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世/北明ppet.pptx>)

SHA-256：`b3306f4a610f9fedc594ef9f3268c4d10c80bb8cb0909e2fad95f89270f050ae`


原件直接核对：slide 9 p6

> 除了军事集权外，控制了宁王系宗室的吴国发明了“淮宁相禅”的制度。也就是淮王系（朱棣后人，北明淮国）和江西宁王系（朱权后人）宗室交叠为主。通过藩国的推举实现“兄”终“弟”及。由此吴国不仅拉拢了在北明时期有一定积蓄的淮王，也让淮国领袖不得不以储君身份长期在南京听政。而当淮王登基，成为金陵之主时，吴国对江南朝廷的控制又足相抗衡，不惧其势。反倒是淮王必须想办法将西南人才按插入金陵。与宁王系的官员斗争。

### S07

文件：[restoration-character-records.json](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/restoration-character-records.json>)

SHA-256：`4e02d2435bde9d2f4429ef4b5b1695b0b8cd9769aad1de819ee1905f10d82d3f`


记录 3146（完整记录在源 JSON；以下身份字段）：

```text
	first_name="Kuobing"
	last_name="Zhu"
	country=309
	character_roles={ character_role_magnate character_role_nesnd_ming_refuge }
	birth_date=1799.2.24
	last_health_value=1.3
	template=USM_zhu_kuobing
```


记录 3147（完整记录在源 JSON；以下身份字段）：

```text
	first_name="Zuoyu"
	last_name="Zhu"
	country=309
	character_roles={ character_role_nesnd_ming_refuge }
	birth_date=1825.5.23
	last_health_value=1.05
	template=USM_zhu_zuoyu
```

### S08

文件：[ce_french_empire_journal_effects.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/scripted_effects/ce_french_empire_journal_effects.txt>)

SHA-256：`b0f04eff52f308a5109f7df94f2280c97d6991c39721a33d8af20f0f91904c86`


1020–1029：

```text
1020: ce_set_orleanist_ruler = {
1021: 	if = {
1022: 		limit = {
1023: 			NOT = {
1024: 				any_scope_character = {
1025: 					has_variable = house_orleans_leader
1026: 				}
1027: 			}
1028: 		}
1029: 		ce_create_orleanist_ig_leader = yes
```


1140–1159：

```text
1140: 	else = {
1141: 		create_character = {
1142: 			last_name = d_Orleans
1143: 			female = no
1144: 			culture = primary_culture
1145: 			ig_leader = yes
1146: 			interest_group = ig:ig_petty_bourgeoisie
1147: 			ideology = ideology_orleanist
1148: 			age = 21
1149: 			on_created = {
1150: 				cleanup_ruler_character_roles = yes
1151: 				set_variable = {
1152: 					name = is_married
1153: 				}
1154: 				add_character_role = politician
1155: 				set_variable = house_orleans
1156: 				set_character_as_ruler = yes
1157: 				save_scope_as = FRA_ce_orl_leader_scope
1158: 			}
1159: 		}
```


2437–2464：

```text
2437: ce_find_bonaparte_in_exile_effect = {
2438: 	if = {
2439: 		limit = {
2440: 			any_scope_character = {
2441: 				has_template = fra_napoleon_iii_character_template
2442: 			}
2443: 		}
2444: 		random_scope_character = {
2445: 			limit = {
2446: 				has_template = fra_napoleon_iii_character_template
2447: 			}
2448: 			exile_character_with_martyrdom = yes
2449: 			save_scope_as = fra_old_ruler_scope
2450: 		}
2451: 	}
2452: 	else_if = {
2453: 		limit = {
2454: 			any_character = {
2455: 				has_template = fra_napoleon_iii_character_template
2456: 				is_in_exile_pool = no
2457: 			}
2458: 		}
2459: 		random_character = {
2460: 			limit = {
2461: 				has_template = fra_napoleon_iii_character_template
2462: 			}
2463: 			exile_character_with_martyrdom = yes
2464: 			save_scope_as = fra_old_ruler_scope
```


2620–2634：

```text
2620: 		else = {
2621: 			create_character = { # El Generico
2622: 				first_name = "NapoleO_n"
2623: 				last_name = "Bonaparte"
2624: 				culture = cu:french
2625: 				interest_group = ig_petty_bourgeoisie
2626: 				ruler = yes
2627: 				ideology = ideology_bonapartist
2628: 				on_created = {
2629: 
2630: 					cleanup_ruler_character_roles = yes
2631: 					set_variable = house_bonaparte
2632: 					set_variable = temp_bonaparte
2633: 					add_character_role = general
2634: 				}
```

### S09

文件：[ce_japan_gov_effects.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/scripted_effects/ce_japan_gov_effects.txt>)

SHA-256：`d9194199ca61ca81d2597e89297232e79763014036fba9a76dfda85ad769d4eb`


9–34：

```text
9: 			limit = {
10: 				NOT = { 
11: 					any_scope_character = {
12: 						has_template = JAP_toyotomi_hideharu
13: 					} 
14: 				}
15: 			}
16: 			if = {
17: 				limit = {
18: 					NOT = { any_character = { has_template = JAP_toyotomi_hideharu } }
19: 				}
20: 				create_character = {
21: 					template = JAP_toyotomi_hideharu
22: 				}
23: 			}
24: 			else_if = {
25: 				limit = {
26: 					any_character_in_exile_pool = {
27: 						has_template = JAP_toyotomi_hideharu
28: 					}
29: 				}
30: 				random_character_in_exile_pool =  {
31: 					limit = {
32: 						has_template = JAP_toyotomi_hideharu
33: 					}
34: 					transfer_character = root
```


74–78：

```text
74: 			else = {
75: 				create_character = {
76: 					template = JAP_toyotomi_hideharu
77: 				}
78: 			}
```


314–324：

```text
314: 		create_character = { # random toyotomi shogun
315: 			last_name = Toyotomi
316: 			female = no
317: 			culture = primary_culture
318: 			ig_leader = yes
319: 			interest_group = ig:ig_landowners
320: 			ideology = ideology_modernizer_leader
321: 			age = 39
322: 			on_created = {
323: 				cleanup_ruler_character_roles = yes
324: 				set_character_as_ruler = yes
```


362–376：

```text
362: 		if = {
363: 			limit = {
364: 				game_date >= 1831.7.22
365: 				NOT = { has_variable = heir_komei_spawned }
366: 				ruler ?= {
367: 					has_template = JAP_ninko_yamato
368: 				}
369: 			}
370: 			set_variable = heir_komei_spawned
371: 			create_character = {
372: 				template = JAP_komei_yamato
373: 				on_created = {
374: 					replace_character_roles = { add = { heir } remove_all = yes }
375: 				}
376: 			}
```

### S10

文件：[00_code_on_actions.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/on_actions/00_code_on_actions.txt>)

SHA-256：`ec3e3e97140777b10d4d99f41c528ec1dc6f1499429e3e2f566b3819a36e63bb`


1069–1076：

```text
1069: 		# Japan
1070: 		if = {
1071: 			limit = {
1072: 				c:JAP ?= this
1073: 				can_generate_scripted_heirs = yes
1074: 			}
1075: 			japan_generate_scripted_heirs = yes
1076: 		}
```


6751–6765：

```text
6751: # Root = Character
6752: on_heir_born = {
6753: 	effect = {
6754: 		if = {
6755: 			limit = {
6756: 				NOT = { # Iesada Tokugawa cannot produce heirs
6757: 					owner.ruler ?= {
6758: 						has_template = JAP_iesada_tokugawa
6759: 					}
6760: 				}
6761: 				owner ?= {
6762: 					has_gov_regency = no
6763: 				}
6764: 			}
6765: 			post_notification = heir_born_notification
```

### S11

文件：[00_ip4_victoria_scripted_triggers.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ip4_victoria_scripted_triggers.txt>)

SHA-256：`bb5c5ad92688562f46e3cdb5284aaf7097c922f7e373324b54aa0feb55621087`


617–632：

```text
617: can_generate_scripted_heirs = {
618:     has_law = law_type:law_monarchy
619:     NAND = { # Has a historical heir
620:         exists = heir
621:         heir = {
622:             is_historical = yes
623:         }
624:     }
625:     NAND = { # Austrian personal unions can cause some strange edge cases
626:         exists = overlord
627:         is_subject_type = subject_type_personal_union
628:         any_primary_culture = {
629:             is_primary_culture_of = overlord
630:         }
631:     }
632: }
```

### S12

文件：[00_victoria_heir_generation.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_heir_generation.txt>)

SHA-256：`c7d00a1b4d382f9a4ac9c6ea99d9699a5fad7e9c2c2e2e886ea2286dc46ded68`


8–22：

```text
8: 		if = {
9: 			limit = {
10: 				game_date >= 1831.7.22
11: 				NOT = { has_variable = heir_komei_spawned }
12: 				ruler ?= {
13: 					has_template = JAP_ninko_yamato
14: 				}
15: 			}
16: 			set_variable = heir_komei_spawned
17: 			create_character = {
18: 				template = JAP_komei_yamato
19: 				on_created = {
20: 					replace_character_roles = { add = { heir } remove_all = yes }
21: 				}
22: 			}
```


79–91：

```text
79: 		if = {
80: 			limit = {
81: 				NOT = { is_template_used = JAP_iesada_tokugawa }
82: 				ruler ?= {
83: 					has_template = JAP_ieyoshi_tokugawa
84: 				}
85: 			}
86: 			create_character = {
87: 				template = JAP_iesada_tokugawa
88: 				on_created = {
89: 					add_character_role = heir
90: 				}
91: 			}
```

### S13

文件：[00_victoria_ip4_scripted_effects.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_effects/00_victoria_ip4_scripted_effects.txt>)

SHA-256：`f1c4691e8734d0872283abd184b538d25f4474e68f7b0790c75cf252e03fcc8e`


1933–1946：

```text
1933: summon_napoleon_the_woat = { # Special case
1934: 	save_scope_as = summoning_country
1935: 	if = {
1936: 		limit = {
1937: 			any_character = {
1938: 				has_template = fra_napoleon_iii_character_template
1939: 			}
1940: 		}
1941: 		random_character =  {
1942: 			limit = {
1943: 				has_template = fra_napoleon_iii_character_template
1944: 			}
1945: 			save_scope_as = summoned_character_scope
1946: 			transfer_character_of_unknown_status_to_country_and_make_ruler_effects = yes
```


2028–2056：

```text
2028: country_summon_heir_effect = {
2029: 	save_scope_as = summoning_country
2030: 	if = {
2031: 		limit = {
2032: 			any_character = {
2033: 				has_template = $TEMPLATE$
2034: 			}
2035: 		}
2036: 		random_character =  {
2037: 			limit = {
2038: 				has_template = $TEMPLATE$
2039: 			}
2040: 			save_scope_as = new_heir_scope
2041: 			scope:summoning_country ?= {
2042: 				set_character_of_unknown_status_as_heir = yes
2043: 			}
2044: 		}
2045: 	}
2046: 	else = {
2047: 		hidden_effect = {
2048: 			create_character = {
2049: 				template = $TEMPLATE$
2050: 				save_scope_as = new_heir_scope
2051: 			}
2052: 			scope:summoning_country ?= {
2053: 				set_heir = scope:new_heir_scope
2054: 			}
2055: 		}
2056: 	}
```


2105–2126：

```text
2105: transfer_character_of_unknown_status_to_country_and_make_ruler_effects = { # Requires summoned_character_scope, occurs within this scope, scope:summoning_country is the summoning country
2106: 	if = {
2107: 		limit = {
2108: 			is_in_void = yes
2109: 		}
2110: 		hidden_effect = {
2111: 			free_character_from_void = yes
2112: 		}
2113: 	}
2114: 	if = {
2115: 		limit = {
2116: 			is_in_exile_pool = yes
2117: 		}
2118: 		transfer_character = scope:summoning_country
2119: 		set_variable = exile_to_ruler_var
2120: 		add_career_length = {
2121: 			months = 60
2122: 			random_range = { 1.0 1.5 } # 60-90 months
2123: 		}
2124: 		hidden_effect = {
2125: 			free_from_exile_effect = yes
2126: 		}
```

### S14

文件：[country_jap.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_templates/country_jap.txt>)

SHA-256：`a727ba61139ffd2ed58419cced1ab0c8d52147cafc6f1eb4f6347922c249c864`


28–40：

```text
28: JAP_ninko_yamato = {
29: 	# Emperor Ninko
30: 	first_name = "Ninko" # Ayahito
31: 	last_name = "Yamato"
32: 	historical = yes
33: 	culture = cu:japanese
34: 	noble = yes
35: 	birth_date = 1800.1.1
36: 	role = character_role_emperor_of_japan
37: 	dna = dna_ninko
38: 	religion = rel:shinto
39: 	interest_group = ig_devout # Mostly interested in court rituals and education
40: 	ideology = ideology_moderate
```


52–64：

```text
52: JAP_komei_yamato = {
53: 	first_name = "Osahito" # Later Komei
54: 	last_name = Yamato
55: 	historical = yes
56: 	culture = cu:japanese
57: 	noble = yes
58: 	birth_date = 1831.1.1
59: 	role = character_role_emperor_of_japan
60: 	dna = dna_emperor_komei
61: 	religion = rel:shinto
62: 	interest_group = ig_armed_forces
63: 	ideology = ideology_shojoi
64: 	home_region = STATE_KYOTO
```

### S15

文件：[00_emperor_komei.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/dna_data/00_emperor_komei.txt>)

SHA-256：`4c1bb058ed595df04e12b9888cfe5d67a38fc9bfe25b6a424fc5dd440683655a`


1–9：

```text
1: ##DNA STRING
2: 
3: #FOUU5TNMM0we8A33AD8AxwCQAJAAfwB/AAIAfwCuAK4AfwB/AH8AfwC7AH8AfwB/AH8AfwB/AH8AfwB/AH8AfwB/AH8ArACfAEEAQQBXAG4AVQBVAKUAhwCMAH8AYgDlAKAA5wAQAAAA/ABUAAAAAAB/AH8AfwB/AH8AfwCoAKgAfwB/AH8AfwB/AH8AaABoAH8AfwB/AH8AwQB/AIQAQgB/AH8ArQByAH8AfwB/AH8A4ADgAJAAfwB8AHwAlgDLAKMAgwB/AH8AOgB/AH8AfwCJAIkAfwB/AIMAgwB/AH8AfwB/AH8AfwB/AH8AfwB/AGkAaQDgAH8AmABrAH8AfwCIAIgAdgCXAHEAiQBoAGgAjQBFADQAlgB2AHYAJAAkAGwAbACeAIYAQwCOAIMAfwCbAOUAhwC9ADgAmQB7AGIARwBHAKcAJACRAJEAcgByAn8CfwB/AH8AfwB/AH8AfwAAAAABAAEAAgACAAB/AH8CAAIAAH8AfwIAAgAA/wT/AAAAAAAAAAAIxQLFBX8CfwutC2QA5gDmARABEAAAAAAAAAAAAAAAAAAAAAA=
4: 
5: dna_emperor_komei = {
6:      portrait_info = {
7:      genes={
8:           hair_color={ 20 229 20 229 }
9:           skin_color={ 51 76 51 76 }
```

### S16

文件：[00_auto_assigned_roles.txt](<D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/character_roles/00_auto_assigned_roles.txt>)

SHA-256：`7c53b49f0f79ac683811b3d5f5085197915f18de00864df8dc3873935ce49763`


1–35：

```text
1: # Roles that are automatically assigned from role archetypes
2: 
3: character_role_ruler = {
4: 	texture = "gfx/interface/icons/character_role_icons/ruler.dds"
5: 
6: 	type = ruler
7: 	priority = 100
8: 	
9: 	title_format = ruler
10: 	title_preposition = PREP_OF
11: 	
12: 	character_modifier = {
13: 		character_prominence_add = 100
14: 		character_loyalty_add = 25
15: 	}
16: 	
17: 	auto_assigned = yes
18: }
19: 
20: character_role_heir = {
21: 	texture = "gfx/interface/icons/character_role_icons/heir.dds"
22: 
23: 	type = heir
24: 	priority = 99
25: 	
26: 	title_format = heir
27: 	title_preposition = PREP_OF
28: 	
29: 	character_modifier = {
30: 		character_prominence_add = 50
31: 		character_loyalty_add = 25
32: 	}
33: 	
34: 	auto_assigned = yes
35: }
```

### S17

文件：[effects.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/effects.log>)

SHA-256：`24e7af8c1f338dea727e256c862a915f92260e22fa740a98a896738d3b4668e1`


845–865：

```text
845: ## create_character
846: Creates a character, any option can be omitted.  
847: create_character = {  
848: 	name = loc_key or alternatively first_name and last_name separately  
849: 	culture = culture_tag  
850: 	religion = religion scope (if omitted, it's defined by the character's culture religion)  
851: 	female = bool or character scope (gets the same value from the character)  
852: 	noble = bool or character scope (gets the same value from the character)  
853: 	ruler = bool  
854: 	heir = bool  
855: 	historical = bool  
856: 	age = integer, range, or character scope (gets the age from a character)  
857: 	ideology = ideology key or scope  
858: 	interest_group = interest group key or scope  
859: 	template = base template to generate the character from  
860: 	on_created = effect  
861: 	save_scope_as = scope name  
862: 	trait_generation = effect  
863: 	hq = HQ scope or strategic region scope  
864: }
865: **Supported Scopes**: country  
```


1264–1279：

```text
1264: ## every_character
1265: Iterate through all characters globally  
1266: every_character = { limit = { <triggers> } <effects> }
1267: **Supported Scopes**: none  
1268: **Supported Targets**: character  
1269: 
1270: ## every_character_in_exile_pool
1271: Iterate through characters in the exile pool  
1272: every_character_in_exile_pool = { limit = { <triggers> } <effects> }
1273: **Supported Scopes**: none  
1274: **Supported Targets**: character  
1275: 
1276: ## every_character_in_void
1277: Iterate through characters in the void  
1278: every_character_in_void = { limit = { <triggers> } <effects> }
1279: **Supported Scopes**: none  
```


36816–36819：

```text
36816: ## set_character_as_ruler
36817: Set scoped character as ruler in their country.  
36818: scope:larry = { set_character_as_ruler = yes }CAUTION: Do not use this effect with chartered companies, as the character's country will be affected
36819: **Supported Scopes**: character  
```


36886–36899：

```text
36886: ## set_first_name
36887: Changes the first name of a character to a loc key  
36888: set_first_name = loc_key
36889: **Supported Scopes**: character  
36890: 
36891: ## set_global_variable
36892: Sets a variable  
36893: set_variable = { name = X value = Y days = Z }  
36894: Where X is the name of the variable used to then access it  
36895: Where Y is any event target, bool, value, script value or flag (flag:W)  
36896: An optional days where Z is the number of days or script value  
36897: This variable will be accessible with <type_>var:X. With type being in a scope object or in a top scope  
36898: Can also be used as set_variable = X (equivalent to set_variable = { name = X value = yes })
36899: **Supported Scopes**: none  
```


36910–36914：

```text
36910: ## set_heir
36911: Sets the heir of the scoped country to the character scope specified  
36912: set_heir = scope_victoria
36913: **Supported Scopes**: country  
36914: **Supported Targets**: character  
```

### S18

文件：[triggers.log](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/references/engine-docs-1.13.11-20261031/triggers.log>)

SHA-256：`ad323401ead8b74c6bca34c147ce37fcea0f5dff98d4993f22d412d1aa31f94e`


100–115：

```text
100: ## any_character
101: Iterate through all characters globally  
102: any_character = { <count=num/all> / <percent=fixed_point> <triggers> }
103: **Supported Scopes**: none  
104: **Supported Targets**: character  
105: 
106: ## any_character_in_exile_pool
107: Iterate through characters in the exile pool  
108: any_character_in_exile_pool = { <count=num/all> / <percent=fixed_point> <triggers> }
109: **Supported Scopes**: none  
110: **Supported Targets**: character  
111: 
112: ## any_character_in_void
113: Iterate through characters in the void  
114: any_character_in_void = { <count=num/all> / <percent=fixed_point> <triggers> }
115: **Supported Scopes**: none  
```


12524–12527：

```text
12524: ## is_template_used
12525: Checks if character template has already been used  
12526: is_template_used = template_key
12527: **Supported Scopes**: none  
```

### S19

文件：[CE_cultures.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/cultures/CE_cultures.txt>)

SHA-256：`1227b26c826844abe9ada42ee57557070fe318cef6c805a9d0b8cb11dc1b3baa`


1564–1570：

```text
1564: ce_wuu={ # 江南
1565: 	color = rgb{ 201 50 50 }
1566: 	religion = kaimeng_confucianism
1567: 	heritage = heritage_han
1568: 	language = language_southern_mandarin
1569: 	traditions = { tradition_sinosphere }
1570: 	name_format = last_first
```


1642–1645：

```text
1642: 	ethnicities = {
1643: 		1 = asian
1644: 	}
1645: 	graphics = east_asian
```

### S20

文件：[latest_test_save.v3](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/persia-journal-ui-20261103/runtime-evidence/latest_test_save.v3>)

SHA-256：`6d1563547bf2ec4368625e23e3aed25b06352fe90d03aa6cd43ee27ef97711ee`


只读冻结实存档；本次没有重新解析或改写此文件。人物身份读取经现有提取件 S07，并与父任务的已完成存档取证结合使用。

### S21

文件：[ce_french_empire.txt](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/backups/pre-update-20261030T233944Z/mod/common/journal_entries/ce_french_empire.txt>)

SHA-256：`e8a32123bdcafd92ae366d3cb53bf03c2b9308ce95f8ed5aea8624382eb62ff6`


549–563：

```text
549: 							kill_character = yes
550: 						}
551: 						
552: 					}
553: 					if = {
554: 						limit = {
555: 							has_gov_regency = yes
556: 						}
557: 						remove_regency_modifier = yes
558: 					}
559: 				}
560: 				ce_set_orleanist_ruler = yes
561: 				scope:fra_old_ruler_scope = {
562: 					exile_character_with_martyrdom = yes
563: 				}
```


578–587：

```text
578: 						has_variable = house_orleans
579: 					}
580: 					set_ideology = ideology:ideology_orleanist
581: 					save_scope_as = french_monarch_scope
582: 				}
583: 				hidden_effect = {
584: 					ce_find_bonaparte_in_exile_effect = yes
585: 				}
586: 				
587: 			}
```
