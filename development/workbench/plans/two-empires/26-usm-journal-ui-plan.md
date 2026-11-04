# 26 — 吴明论战日志条件与进度说明

父版 `exports/map-reference-closure-20261031-a`。根代理在新run真实接受日志后看见裸 `has_template`、人物计数/泛化人物死亡标签和内部变量；首次契约悬停已稳定五分钟，不能把之前初始化错误继续列为未修。

## 范围与依赖图

`ce_usm_conflicts_within complete/fail/invalid` → 原条件仅包 `custom_tooltip` → 两语机制本地化；`nesnd_south_progress` → 只读月增 script value → bar读数上的country tooltip链接 → `Country.MakeScope.ScriptValue` 当前数值。现有JE脉冲/按钮负责全部变化；不添加第二份周期增量。作者reason/事件叙述、剧情顺序、人物、人口与地图均原样。

原生 `gui/journal_entry.gui:281/303` 悬停背景只读 GetPeriodicProgressBreakdown；没有monthly_progress定义的变量同步条只能输出标题。原生bar desc支持富文本（本体ep2_ryukyu_rivalry），因此把机制链接放在现有读数上；使用本机存在的 `JournalEntry.GetCountry` 与真实已验证的 Country.GetTooltipTag 上下文，不使用无ROOT嵌套tooltip。bar背景的自动周期分解不伪造；动态细则从读数链接进入。

## 真实规则与文案比较

|类别|原实现/现有显示|本次机制文案|
|---|---|---|
|完成生命条件|NOT any_scope_character USM_zheng_qin alive，界面出现任意角色/模板/泛名|“郑钦已去世或离开本国。”准确包括转属，不称必须死亡|
|完成结局条件|NOT global nesnd_south_settled|“南方政局尚未完成结算。”|
|失败|五个指定邦国全失去直接统属，或num_states<2；旧文案只写地区>=2|明列四川、湖南、菲律宾、南洋联省、远南与不足两州两条真实路径|
|失效|全局settled / tag_WUU_var / 非君主|分别说明危机已结算、吴朝已经建立、已废除君主制|
|进度说明|读数已有；bar悬停只有标题|当前压力、当前月增、通常+1/契约生效+0.4；契约每次+20/压力−8下限0，18月冷却，10年修正，100保明|

这些是条件/读数/按钮规则，不写角色对白或正反讨论。现有“郑钦已去世后”提示与实际判定不一致，一并改机制说明；作者 `_reason` 不动。

## 实施与验证

改前独立完整备份父版；派生独立 `usm-journal-ui-20261031-a`；只改JE包装、script value、两语新override与metadata。比较AST：移除本次新增tooltip wrapper后与父JE完全相同；其他所有游戏逻辑文件字节不变。新键两语齐全/BOM；规则数值直接核父按钮与月脉冲。Tiger比较新增问题，静态不能替代引擎。

根代理下次实际新局或同源存档：打开完成/失败/失效条件，核无裸模板/变量；悬停两条读数的机制链接并保持面板，记录error.log增量；订约前月增1，订约后月增0.4及契约+20/压力−8；过月核单次增加，另存读回。天然郑钦死亡/转属两个条件含义保留，本次不制造死亡或胜利夹具。
