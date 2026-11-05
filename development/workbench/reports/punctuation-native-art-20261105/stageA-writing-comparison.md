# StageA 玩家文本对读与交付

实际配置 `gpt-6-astra / high`。先读全部文本契约、9个冻结脚本的实际差异及当前调用，再保存双语初稿，逐项审稿后写入。主MOD只改现有两语 `nesnd_native_americas_l_*.yml`；35个新增配对键、9个改写配对键，共88条。9个脚本文件在写作期间SHA完全未变。

## 作者与原版来源

本轮重新提取 `f18b6c4:localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml`，SHA256 `c736f53d59fbcb3213e45c1d18e5e6499121cf86fca9a79fa94bf471c33b1d4f`。实际样本及行号见 `stageA-author-samples.json`，不把新写原住民文本冒充作者原稿。

|实际样本|可观察特点|本轮采用与界限|
|---|---|---|
|`ce_usm_conflicts_within_reason`:118，政治争论在乡校、议会和文字传播之间展开|具体政治场所和不同群体承担因果|动员事件写村社联络、地方首领、人手与给养，不写内部计时器或已生成国家|
|`usm_civilwar.2.d`:179，旧王朝支持者、受损地主、革命派因现实政治压力结盟|不同诉求可以共同举兵，不能把所有参与者写成同一动机|原住民村社保土地与自治，王朝拥护者求复统。战争通知只在对应调用后出现|
|`usm_civilwar.3.d`:194，暂时和平不等于政治矛盾消失|阶段性结果与长远政治过程分开|镇压事件只写打击组织与不满增加，不写永久击败、流亡或人口迁徙|
|`ce_usm_civilwar_journal_fail.tt`:136，明写参与者条件和数值|必要条件采用直接事实句|50压力、12个月准备、75压力复起分别落在相应条件或状态，不混成“已开战”|

通知原生调用链：GAME `events/central_america_events.txt:25–33` 保存formation_country再向外交相关国家post_notification；GAME `localization/english/anniversary_formations_l_english.yml:100–102` 使用保存的country scope及name/desc/tooltip三个键。本批采用脚本实际保存的 `nesnd_restoration_notice_actor`，不采用接收国ROOT或可能已经灭亡的对手／州scope。新event14是country_event，其唯一动态引用 `ROOT.GetCountry.GetName`与该上下文对应。

## 初稿返工

`stageA-player-text-draft-v1.json`保留首稿。event14首稿说驻军已经在削弱复统派号召，会提前宣布玩家尚未选择的军事压制。修订后只陈述地方争夺趋向武装对抗，及地方议会／地权谈判可能影响举兵。没有替玩家做出选择，也没有将筹备期写成新国家已经出现。

当前已写文本在 `stageA-player-text-draft.json`，完整实际前后差异在 `stageA-player-text-actual.diff`。每个键的字段、脚本契约、初稿修订理由和最终文本在 `stageA-player-text-applied.json`。

## 逐类结论

- 镇压按钮说明：通过。只写暂时压制。效果提示仅显示压力−20和原住民人口5%激进化。12个月、军队认可+1、乡村民众认可−2由已有show_as_tooltip的真实修正展示，不重复抄入自定义提示。
- 谈判：通过。压力−15及取消正在进行的准备明确。36个月地方议会修正仍由原生预览承担，未写成永久消除复统问题。
- 三个准备状态与event14：通过。区分正在准备、准备期已满但压力不足、等待其他真实资格。没有读取timer.GetValue，没有宣称既定地区即使失地仍受原主控制。
- 九条通知：通过。建国通知只陈述实际分离建国。战争通知对应创建war=yes并找到目标与双方战争要求。失败发起／失去原对手／争端未决结束／实际吞并胜利分别表述，未合并成必然胜利。所有消息正文只引用通知actor。
- 旧档重开：通过。只写政治诉求再起，不写人口回迁、重新外逃或修复存档的过程。
- 旧事件1、3、6与战争状态：通过。战争事件1按新调用点写已开战。事件3删除迁徙／流亡叙述。事件6使用各终止原因均成立的未统一结果，不虚构同一原因。战争日志常驻状态只写两政权并立，不因waiting状态而冒称已经开战。
- 大平原提示：保持根代理已修订的原句，两语未被本批覆盖。MEX/Andean文本没有套用汗国名称。

## 读回与冻结

实际文件读回88条，88个语言／键组合在全MOD本地化中均唯一。两语UTF-8 BOM、原文中的所有非目标键不变，通知不含ROOT或JournalEntry引用。全量键／行号见 `stageA-writing-final-readback.json`。

独立修改前备份：`WORK/backups/pre-change-stageA-player-text-20261105T022134Z`。
文本子集冻结：`WORK/reports/punctuation-native-art-20261105/stageA-player-text-freeze/`。只有两份文本，不是完整可运行MOD。脚本冻结与文本冻结分别绑定来源，不把前一阶段纯标点的镇压文案继续当作有效说明。

写作和源码对读完成，根代理最终审稿与整体行为验证待进行。未运行游戏，不保证观察者必定看到弹窗，不给AI权重编造月度概率。
