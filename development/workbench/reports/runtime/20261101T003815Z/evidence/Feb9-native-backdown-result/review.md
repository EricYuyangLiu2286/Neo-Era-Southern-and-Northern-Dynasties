# F2 原生日本退让：实际恢复结果与玩家/人物边界

操作由 ROOT 实际完成。Jan27 玩家控制 JAP，在真实DP选择 Back Down；立即出现“你已被吞并”Game Over。ROOT 随后**手动**选择继续作为观察者，世界继续运行。不得将后续恢复称为玩家无缝续玩。

Jan27前档：SHA `502efe594fec6887e948e9ade4b15c930fd0ae11687cb1a43cd0e9191d3ffff0`，实际日期 `1836.1.27.12`。Feb9结果档：SHA `5e9c64fc476b07b475d6fa7ab885e377552234f31bebd22bec58da6925580c41`，实际日期 `1836.2.9.6`。经过了自然时间，不能宣称同tick人口/全部人物集合守恒。

实际生产回调已触发：00:47:53 的 `on_wargoal_enforced` QA观测到 target对象仍存在；自然2日后Jan29观测到 JAP/JTK/JIM全部活、登记和pending/queued/blocked全清。当前日志仍有缓冲，Jan29完整END尚未落盘；`callback-observations.json`如实记录不完整周期，正常退出后应补全，不能拼造完整PASS。

Feb9原生档已证明：

- 新JIM `16777953`、JTK `16777954`、JAP `16777955`存在，原生保护国关系（实际action为`protectorate`）分别由pact282、281、283连接USM730。
- 全局 `nesnd_japan_partitioned` 与 `nesnd_japan_dossier_closed`为真；USM的登记、pending、queued、blocked变量消失。
- 原JAP96个province实际分配：德川53、遗留JAP31、皇室5、USM7。京都4+关西大阪1归皇室；关西其余5、中国8、釜山7、两湖11归遗留JAP；九州2、四国5归USM。原日本地区里的第三国province改变为0。
- Lin3153仍属USM。旧JAP人物多数仍属于**已dead的旧country17**，新三国分别生成fallback君主；同TAG不能解释为原人物已恢复到新国。

人物原生时序见 `original-character-timeline.json`：Jan27除3447已经retired外，旧君主3446、仁孝3448、德川3455/3457/3461、丰臣3460及储君6837有原角色且未retired；Feb1实际autosave中这些对象都retired留owner17，没有记录death_date或dead registry。Feb9状态相同，3447才被清出database。**这证明退休/旧owner变化，尚不证明引擎 `is_character_alive` 的结果或安全再转属能力。** 下一QA C已预备在吞并前保存typed对象并于真实回调后检查该谓词，未复活或转人。

player_manager在结果档仍保留country17旧对象；该字段不能独立证明正在控制国家，ROOT实际UI已经是观察者。

本报告认证范围为这次受控原生退让后的国家/领土/主从恢复。自然内战、战争胜利、自动玩家续玩、历史人物复用、失效重试、读档、舰队到达等仍各自待验。
