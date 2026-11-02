# Lin／JIM候选定向复核

2026-11-02；对象：WORK/exports/japan-development-20261102-a；主MOD未改。本轮只读复核，未开游戏。当前GAME 1.13.11/build24799966，catalog CURRENT。候选受查文件指纹：`lin-implementation-source-sha.json`；原生链及37源指纹见`lin-native-chain.md`、`lin-native-source-sha.json`。以下行号相对于此次读取的候选；G=当前GAME。

## 必须修正

### P1：摄政结束后没有恢复已保存的帝室继承人

定位：`common/scripted_effects/nesnd_jp_imperial_court.txt:59–68`。

`capture_court`第8–10行会保存原来的Yamato heir；建立摄政时第57行把国家heir换成当前天皇。这是有原版依据的表示。但Lin死亡/退出、天皇重新成为ruler后，非Lin分支只更新emperor变量，完全不把保存的 `nesnd_jp_imperial_heir` 还原为国家heir。该对象只会在“Lin仍为ruler且天皇无效”的分支被消费（31–35行）。因此先有天皇A＋合法heir B→Lin摄政→Lin先死→A复位时，B仍活着却失去继承席位，随后继承可能由引擎另生人物接管。

原版JAP月度历史heir入口在G/common/on_actions/00_code_on_actions.txt:1069–1076，仅`c:JAP`；不会替JIM补回B。修正：在已确认当前ruler就是该帝室接任者、仍君主制的还政分支，验证原B alive、owner为该JIM、house_yamato、非流亡、不是当前ruler后，country-scope `set_heir = var:nesnd_jp_imperial_heir`，成功后清已移交记录；不覆盖共和/政变产生的新合法继承安排。需测试Lin先死、天皇先死、B已死/转国三种次序。

### P1：旧迁移可以推翻JAP后来建立的共和政体

定位：`common/scripted_effects/nesnd_jp_imperial_court.txt:74–88、92–110`。

初始捕获只看JAP当前ruler是Lin及旧`nesnd_japan_lin_regency_appointed`。执行只查JIM君主制，**未查JAP目前的法律/政权**；随后无条件寻找丰臣并`set_character_as_ruler`。旧appointed标记按现有清理规则永久保留，所以“旧JAP摄政完成→JAP改为共和/军事政体、Lin仍任现统治者→载入候选”的存档仍会被当成旧误任命，丰臣强行替换总统/独裁者并把Lin送走。

这违背修订3与L24的当前法律优先、合法政治交接不重播原则。修正：先区分仍属原君主摄政的旧状态与已改变制度的历史记录；后一种只清本模块失效office/迁移请求，保留当前ruler和owner，不作恢复君主操作。对仍可迁移的JAP增加本国实际君主制和原政治身份验证，再确认合法接任。

### P1：USM灭亡后，旧JAP林摄政迁移没有执行者

定位：`common/on_actions/nesnd_japan_lin_regency.txt:3–10`；`common/scripted_effects/nesnd_jp_imperial_court.txt:73–74`。

迁移入口和效果都只接受USM country scope；JIM月度仅refresh court，startup bootstrap也不迁移。旧档若USM已经灭亡，JAP和JIM仍在、Lin仍按旧版本任JAP ruler，永远无人迁移；旧对象/请求还全部存在于死宗主。新的JIM文化和日志会启动，但人物身份仍错位。

修正：由仍存活的准确JAP/JIM或唯一全局案件承接迁移；将精确actor/recipient/阶段保存于存活持有者，USM存在时才更新其旧赞助记录。不能用新USM复国或c:TAG重新枚举代替原案件身份。按照共同生命周期第10/12条覆盖“原赞助者死、被继承、改号”的旧档，不要求重建USM。

### P1：原历史heir生成器仍能复制／重生具名继承人

定位：`common/scripted_effects/ce_japan_gov_effects.txt:359–598`，最小实例 `512–521`。

本批只给`country_generate_japanese_shogun`加了managed守卫（第2行），`japan_generate_scripted_heirs`仍按缺少国家spawn旗标直接create。候选history/characters/JAP - Japan.txt:6–8在开局创建Shimei，但不写`heir_shimei_spawned`；zz_ce_JAP.txt:21–40模板也不写它。若Shimei死亡或已合法离开、Hideharu仍在（包括旧迁移恢复原丰臣ruler），原月度`can_generate_scripted_heirs`只排除“现在存在历史heir”，不会核曾死亡人物；512–521就再次create同一具名Shimei。其他Yamato/Tokugawa/Toyotomi分支同形，部分直接事件调用也不经过native月度资格门。

这是此前遗留行为，但仍在本轮要求的迁移/人物不复活闭包内。修正不能简单禁用全部heir生成，否则会切断原世系：为已存在的历史人物登记spawn/曾生成事实；查本国已有同实例并复用，查第三国/已故实例不抢回不重生；只有从未生成且符合出生和现朝廷资格时create，并立即持久登记。`events/flavorJAP_ce.txt:166–179`与1846同类fallback也要纳入同一实例登记规则，不能让事件绕过修好的generator。

## 已核对通过的边界与名称

- 本机没有 `country_generate_scripted_japanese_heir` 这个symbol；真实函数是 `japan_generate_scripted_heirs`。`country_generate_japanese_emperor`在原版的有效直接调用点是`country_restore_japanese_emperor`后备分支，候选已有的REPLACE在nesnd_jp_country下阻断这条强制换天皇路径。
- `character_appoint_new_shogun_when_no_heir`的REPLACE阻断了日本三国的德川强制改姓路径；character→owner scope形状正确。
- `nesnd_jp_court_ruler_changed` / `...character_died`从character root先进入owner，再给JIM排次日country事件；与原版scope文档一致。没有发现把character root直接作为country操作的新增错误。
- 旧迁移在USM月度中先于maintain/try_appoint执行，pending存在时跳过旧清理；JAP旧office最后只清country变量，未调用会删Lin新commission的旧clear_recipient。这两项正确。
- 旧迁移已先把JAP合法候选设ruler，确认Lin不再ruler/heir才transfer。actor只有JAP/JIM owner可续接；不接收第三国owner。复跑不会把已经完成的JAP接任再执行一遍。
- 新JIM双主流在definition、on_created及bootstrap均落实；不是改Lin个人文化。已用原生天皇role与country `set_heir`，没有引入永生摄政effect。
- JAP专用 `on_new_ruler_japan_effect`、帝室death chain未被错误调用到JIM；本次未见其他可直接把JIM皇帝或Lin转到JAP的新增调用。

以上是源码定向复核，不是引擎通过。修正后需要按用户新授权统一静态与文案复核，再由主代理执行定向游戏验证；本子任务不启动游戏。
