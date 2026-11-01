# 地图候选：引用语义只读复核

对象：`WORK/research/20261101/map-refinement/inventory.json`、`reference-closure.json`，以及 `WORK/exports/map-refinement-20261101-a` 的当前有效文件。共同父版为 sequence A。此复核未修改地图候选、工具、GAME 或 Workshop；不含游戏内验证。它是重点语义复核，未把 368 个文本命中都当成已逐个验收。

## 已核对的主要语义

- `events/flavorUSM_ce.txt` 的广东四处引用（159、171、345、357 行）分别成对位于 `any_scope_state` 和 `random_scope_state` 的南方不满来源候选州集合；OR 纳入高凉保留原地理覆盖。没有城市专属行为，不应只保广州。
- `events/flavorCNE_ce.txt:1107/1149` 是牧沐子东渡事件的存在门槛和目的国选择，检查某国有一个 state 的 region 是 CALIFORNIA。没有“首都等于该地”的代码条件。当前设计保留大梁/新郑都港核心仍在旧 CALIFORNIA，把这个目的地域保持单一是可以解释的设计；不要把报告写成程序实际检查首都，也不应因新北大原人口而随机换目的国。
- `common/company_types/ce_companies_china.txt` 的福海、满洲合作社等已改引用主要是 attainable/possible/AI 建设经营范围；OR 增加新州适合该用途。总部 preferred_headquarters 的唯一地点未被误扩。
- GAME 的诺顿事件、岩仓使团、横贯铁路最终落点属于具体城市/核心地区场景，旧核心仍保留时可不扩为随机新州；其中铁路 JE 的领土门槛与事件落点需要分别解释。

## 已反馈地图代理的问题

### 1. 军阀初始地盘不能以“单城市 seed”概括

GAME `events/warlord_china_events.txt:163–186` 和 `:232–254` 通过 `create_country` 把 CHI 的整个 TIANSHAN/GUANGDONG state 移给 XIN/YUE，随后每个选项的 `while`/`every_country` 让现存军阀随机吸收邻接 CHI 州。它没有指定将拆出的 KASHGAR/GAOLIANG 交还对应军阀。

原广州地区被切成两州后，YUE 保证取得旧广东残部；高凉也可能邻接 GNG（广西）而被后续循环分给 GNG。仅保留原 seed 和 unchanged generic expansion 因此不能证明原始起家地盘等价。建议仍只创建一次国家，然后将 CHI 所有的对应子州转入同一新 TAG；第三国所有的 state 必须保留。如果 CHI 仅持子州、不持原核心，还需显式记录是设计上不创建该军阀，还是使用单次备选 seed；不要重复 `create_country` 同一 TAG。

这是当前源码导致的范围变化判断，不是本次已观察到该晚期引擎路线。

### 2. achievement 人口阈值不是城市引用

`common/achievements/base_achievements.txt:105` 的 `go_west_young_man` 要求 USA 在 CALIFORNIA 有 state、该 state 不分治、人口至少 250000。`reference-closure.json` 将它与城市目的地混标，缺乏依据。这是完整地区和人口阈值的混合条件；拆后只验旧残部会改变地域与人口计算，给每个子州分别要求 250000 又会提高原门槛。应明确采用原地理总范围/总人口方案，或保留为未迁移的继承例外，不能仅靠文件白名单把 unresolved 变零。

### 3. 写后 SHA 不等于变更前 SHA

`WORK/tools/close_map_refinement_20261101.py` 的 `transform()` 在 `dest.write_text(...)` 之后读 `sha256(f.read_bytes())` 保存为 source_sha。当 f 本来位于候选目录时，f 与 dest 相同，记录的是写后文件指纹。应在写入前捕获源字节哈希，或者将现字段改名并另录真正的 source-before。父候选 manifest 仍可提供对照，但当前字段不能据名字当成前像证据。

## 范围与证据边界

地图代理已收到上述逐点反馈。此文件记录审查时的发现，不会随候选后续修订自动变成“已修复”。若实现收口，应以修改后的具体文件 SHA、对应差异和重新审查结果补充记录。静态引用闭包不替代新局、道路/海港、舰队和存读档验收。

## 修订后的复核

地图代理随后用 `fix_refinement_semantic_review.py` 修正上述三项；本审查者以只读工具 `review_map_refinement_semantics_20261101.py` 重核，结果为 **STATIC_TARGETED_REVIEW_PASS**。XIN/YUE 的创建后子州转移带 CHI 所有权守卫，子州独占情形使用紧邻 `else_if` 单次备选 seed；逆转这些新增后完整军阀事件文件的有序 AST 等于 GAME。成就改为三片完整拥有且人口仅合计一次；其 country→every_scope_state→add 数值形状、limit 过滤与 numeric state_population 分别有当前 GAME 的 `building_values.txt:19`、`event_values.txt:207`、`occupation_values.txt:43` 作为来源。重命名的 exact_parent_source_sha256 字段逐项匹配实际父版/GAME。

精确文件指纹和断言见 `map-refinement-20261101-independent-reference-review-fixes.json`。这关闭本文件提出的三项局部问题，不提升为地图整包或引擎验收通过。

最终命名修订将子州 `STATE_KASHGAR` 改为 `STATE_WESTERN_TIANSHAN`（西天山，ID3174不变）。已对新名称重新执行同一只读核验，仍通过；旧复核JSON保留，新结果及当前文件SHA见 `map-refinement-20261101-independent-reference-review-final.json`。
