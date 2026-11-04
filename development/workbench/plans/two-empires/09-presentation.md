# 09 文本、图标、动态信息与UI

状态：风格指南与原始对照已存在；新系统尚未改写全部文本。机制和状态先确定，展示同步完成。

剧情事实来自ppet和人物资料；游戏文风来自 `WORK/backups/pre-update-20261030T233944Z/mod/localization/*/replace` 的同类条目。分别比较JE标题/reason/status、event title/desc/flavor、option、button、bar、modifier、tooltip；不能拿简化设定文案推导小说句法，也不能把所有类别写成同一文学长段。

每组文本先写“作者原文—候选—具体差距—修订依据”。保留长短句和专名、行动细节、历史因果；减少没有新信息的转折，不强造双方辩论。标题凝练、正文讲具体发生、功能说明平述条件和后果。词频/字数统计只用来发现异常，不把作者风格变成固定句长配方。

关系图中display边必须接实际机制：JE icon与reason/status/按钮/条；事件portrait/illustration与角色scope、文字；modifier图标与真实效果；动态值读权威变量。`[ROOT.GetCountry.GetName]`等只在支持scope使用；concept链接从当前localization/game_concepts查，颜色#v/#p/#n/#bold闭合。不能用有色假数字代替变量，也不能靠tooltip承诺脚本没做的供应/保护。

本地化通常改MOD `localization/simp_chinese/replace`与english同键，BOM和头保留。原生GUI只读参考 `GAME/gui/journal_entry.gui`、`journal.gui`、`eventwindow.gui`；只有真实布局缺口才修改自有GUI。图标先选当前有效资源；原创媒体确有需要才生成，EACR仅外部依赖引用，绝不搬运模型/纹理。

验证：真实JE按初始/进行/障碍/成功失败状态截图检查；动态数值改变后同步、按钮不可用原因、段落溢出、portrait存亡fallback、全部语言键。文本变化通常不需要重跑全年经济；若动态scope或tooltip背后改执行条件，则回归对应机制。下一步先完成04/05状态与效果合同，再按同类逐条改写，保留对照记录。
