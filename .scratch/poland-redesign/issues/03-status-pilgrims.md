# 收复状态行与「波兰朝圣者」

作者复测部署 8b4680c2。工作台 reports/2026-11-17-poland-redesign/status-fix/logs 中，同次运行四份 error 日志共保留普通状态行 2951 条 Data error。普通、白党守约两个状态的宣称经费均从国家变量读取。两种语言共四处由 JournalEntry.GetCountry 改为 ROOT.GetCountry。依据见技能 lookup/journal-ui.md §3 与原版经济复兴国家日志的状态行。进度条自身的 GetCurrentBarValue 使用其原有上下文。

全局日志中英标题改为「波兰朝圣者」／The Polish Pilgrims，取意于1832–1833年的巴黎流亡刊物 Pielgrzym Polski 及密茨凯维奇的波兰朝圣意象。[法国国家图书馆书目](https://catalogue.bnf.fr/ark:/12148/cb328397493)；[华沙大学馆藏](https://crispa.uw.edu.pl/object/files/15612/display/Default)。

本次运行差异仅四个本地化文件。STATIC_PASS：Toolkit 正负对照有效、5 文件零诊断，全包本地化链接零命中，bom/locsv/tipctx 均为零。部署 7c0328b3a86fffdcda69623538f60554，1524 个文件哈希一致。未启动游戏。重启读原档可检查两种状态的经费和新标题，正式验收以新局为准。

## 同次日志另记

流亡日志地图配色第80行解析器报告 else/else_if，nesnd_polish_diet.1–8 与 ce_poland_events.1 报无默认选项。加载器另将 ce_poland_events.10/.11/.12/.16 列为 orphaned，提示部分结果变量、调试字段与第三批否决标记读写不匹配。这些是加载器记录，尚未判定实际玩法影响。本次按范围保留。
