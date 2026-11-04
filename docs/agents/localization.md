# 本地化维护

每种语言内，一个key只保留一个定义。修改现有文案时直接编辑其所属文件；不得新建zz前缀、按轮次加覆盖层或复制同key。文件按内容命名，如`nesnd_egypt_l_english.yml`、`nesnd_qin_politics_l_simp_chinese.yml`。地图名放map目录；保留UTF-8 BOM、语言头、既有key及动态数据契约。

原版key可以在本MOD replace目录定义一次；这与本MOD内部反复覆盖不同。清理发现的同key不同文案须对照作者原稿、实际脚本及既有修复记录选定，不按文件名猜最终含义。历史源码在Git，不在游戏加载目录保留废稿。

国家日志的status_desc本地化以owning country为ROOT；不要从状态文本直接读取JournalEntry GUI上下文。进度条desc和真实GUI仍按各自原版实例使用JournalEntry/ScriptedProgressBar，不能全局替换。

条件优先用原生逐项显示；变量计时、独立性等不可原生表述的判断用单项短提示。纯初始化/防重复内部守卫hidden，真实冷却、互斥和失败期限必须说明。不要把整段条件塞进巨型custom_tooltip。

玩家文案至少GPT-6 Astra/Medium创作；主代理逐条对读并亲自返工，程序测试通过不能替代文字和剧情判断。详见两份NESND技能。改名同时核GAME+MOD有效定义，原版REPLACE需在目标定义之后；必要用目标领域的描述性文件名，不堆z。
