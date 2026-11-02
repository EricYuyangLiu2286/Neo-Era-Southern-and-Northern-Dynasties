# 林摄政与日本人物链最终定向复核

2026-11-02；只读候选 `WORK/exports/japan-development-20261102-a`。已读 `character-fix-record.json`、当前帝室／迁移／继承／事件源码及最新 `nesnd-victoria3/references/north-south-institutions.md`。GAME 1.13.11/build24799966，catalog CURRENT。未编辑候选、未部署、未开游戏。此处“通过”为源码结论，不是引擎通过。

## 仍需修改的两项真实缺陷

### P1：平胜普通版与保守版仍会生成同一人物的第二实例

位置：`events/flavorJAP_ce.txt:471–495`；身份依据 `common/character_templates/zz_ce_JAP.txt:85–139`。

`JAP_toyotomi_heikatsu` 与 `JAP_toyotomi_heikatsu_alt` 同名Heikatsu、同生日1831.10.20、同姓氏/籍贯/集团，差异是政治意识形态；是同一人物的路线模板。新守卫只查 `_alt`，不把普通模板算作同一历史身份。因此普通平胜已存在、外流或已故时，保守选项仍可因没有alt模板而新create一位平胜。

源码可达例：秀和在1846年前死亡；秀明仍在位；1841以后历史heir生成器创建普通平胜。1846事件找不到活秀和，else_if可把普通平胜存为japanese_heir；选择保守分支时先创建alt并立为ruler，再于494–495行kill原japanese_heir，得到“杀原平胜、换一位同名同生日平胜”。这不是抽象风险，而是现有条件与effect的直接组合。

修正：两模板共用同一历史身份判断；已有本国活平胜时复用准确实例并改为保守意识形态，不再create。若任一身份已经在第三国/已故，不强抢、不通过另一个模板复活。保守分支清理原候选时排除“候选就是已选新统治者”，否则复用后会把新君主自己杀掉。原版名义模板可继续供未出生/从未创建时生成，不能作为复制人物的接口。

### P2：Tocho继承分支的前任条件写成Tocho自身，下一代永远不能生成

位置：`common/scripted_effects/ce_japan_gov_effects.txt:629–646`。

该分支要求日期>=1880.7.1、当前ruler为 `JAP_toyotomi_tocho`，随后尝试create或复用同一个Tocho模板。新`NOT any_character has_template`守卫必然失败，因为ruler本人已经是Tocho；本国复用还排除了ruler，故这个分支没有正常结果。真正前任Chokei在位时不符合该条件，Tocho也不会出现。

修正：前任模板应为 `JAP_toyotomi_chokei`，保留1880.7.1出生下界与同实例复用/禁重复守卫。模板依据：zz_ce_JAP.txt:141–178分别定义Chokei（1860.7.11）及Tocho（1880.7.1）。此错误是原代码遗留，但本轮no-clone处理后已明确成不可达的继承分支。

## 前四项问题的复核结果

|先前问题|当前结果|源码依据|
|---|---|---|
|Lin结束后原帝室heir未恢复|已修复：Yamato ruler分支验证保存对象alive、owner=JIM、非流亡、非ruler并set_heir，随后移除临时引用|imperial_court的非Lin分支（约69–76行）|
|旧JAP已共和仍强换君主|已修复：首次捕获与执行前都重新检查JAP country_has_monarchy_law；已有pending不符时终止|imperial_court的migration捕获/执行limit|
|USM灭亡后无迁移执行者|正常旧JAP实际Lin存档已修复：JAP月度在USM不存活时承办，effect允许同条件JAP为host|on_actions/nesnd_japan_lin_regency.txt:10；imperial_court入口|
|历史heir按缺flag重复create|同模板防护及本国实例复用已添加；普通/alt平胜跨模板身份仍未关闭，见P1|ce_japan_gov_effects.txt:359–650与flavorJAP_ce.2/.3|

## 其余已核边界

- Lin仍是同一`USM_lin_hanhan`现存actor：新任命只从USM非ruler/nonheir候选开始，持久pending捕获精确officer/country；迁移只续接该actor位于JAP/JIM的状态，拒绝死亡、流亡、第三国owner。
- 旧JAP先合法接任，确认Lin已非ruler/heir后才transfer；目标JIM当前为天皇或Lin时才继续。重复检查不会重复恢复已让出的JAP王位。
- 帝室捕获保留原天皇和原heir；Lin期间天皇先死亡会先用保存的合法本国帝室heir，非现存后备时使用新匿名家族人物，不复活具名模板。Lin结束后已补原heir恢复。
- 保存的原heir已死、已到第三国、已任ruler时不会set_heir；记录随后清除，避免月度反复覆盖。
- `set_character_as_ruler`仍在character scope；`set_heir`仍在country scope；death/new-ruler追加hook先进入owner，再延迟调用country事件。未发现这部分新增scope错误。
- 未来人物出生下界保留：Meiji1852.11.3、Taisho1879.8.31、Showa1901.4.29、Iemochi1846.7.16、Chokei1860.7.11、Tocho1880.7.1。Iesada与Shimei在1836已出生。Yoshinobu/Heikatsu采用既有较晚入场日期，未把未出生模板提前生成。Tocho仍需修正前任条件。
- `.2/.3`事件新增精确人物owner/alive/ruler条件、cancellation及effect重验；迟答不会直接对已转出的原君主/候选执行交接。
- 三个国家的原版天皇复位/强制德川改姓路径已有窄REPLACE；没有看到把JIM天皇更新错误写回c:JAP的新调用。
- 最新南北朝制度来源不改变本次日本角色接口结论；未将USM当前存在、吴朝旗标或南朝制度当成Lin个人/江南文化政策存续条件。

`any_character`的引擎文档是“all characters globally”。本次只认证存在的同模板对象会阻止新create；角色死亡后对象被引擎长期保存/清理的边界不靠源码推定为已测试。已存在的spawn记录继续保留，完整死亡与读档行为由主代理按用户授权统一验证。本报告没有把未观测的引擎内部清理行为列成确定缺陷。

## 补充：平胜两个模板的完整闭包和原生改意识形态依据

原生已证接口：G/events/agitators_events/revolution_events_02.txt:4246–4258 在 `random_scope_character` 内对现存继承人执行 `set_ideology = ideology:ideology_authoritarian`（4255行）；E/effects.log:36947–36951明定character scope、ideology target。复用平胜后可直接改意识形态，不需换模板或重生。

推荐共用character谓词（建议名称，不是现有接口）：

```text
nesnd_jp_is_heikatsu = {
    OR = {
        has_template = JAP_toyotomi_heikatsu
        has_template = JAP_toyotomi_heikatsu_alt
    }
}
```

同一集合贯穿以下位置：

1. `flavorJAP_ce.3.2` option trigger：本国有alive/non-exiled/non-ruler平胜（任一模板），或全球从未有任一模板；日期仍由1846事件约束。effect内独立重查，不能只依赖option trigger。
2. 本国人物选择的any/random limit使用相同union与资格；保存准确`jp_heikatsu_ruler`；`set_ideology = ideology:ideology_authoritarian`后对该实例set_character_as_ruler。create后也保存同一个scope。
3. create后备前的全球查询使用任一模板，不加alive限制：`NOT = { any_character = { nesnd_jp_is_heikatsu = yes } }`。不从第三国transfer回来。
4. 仅在选定actor确实alive、owner=JAP且为当前ruler后提交旧君主/敌对候选的死亡与政治后果；`scope:japanese_heir`与新actor相同时跳过kill。这同时避免迟答时新平胜已不合格、create分支跳过，却仍继续杀旧君主的问题。
5. `japan_generate_scripted_heirs`普通平胜分支（本次快照595–603行）也需用两模板union：global禁重复和本国已有实例复用一起修改。不能只修event，否则alt已在世/外流后，另一个缺spawn旗标的国家阶段仍可按normal模板再次生成。
6. 下一代Chokei的父代判定（612–613行）已经包括normal/alt，保持。无需把存活normal人物更改成alt模板，随后继承仍正确。
7. `country_generate_japanese_shogun`中243/258行仍有normal模板create，但整个函数已有 `NOT has_variable nesnd_jp_managed`入口。这些路径不是当前已托管日本的实际入口；若保留此函数作为旧档/未初始化后备，统一加上述身份复用/禁重复，而不能解除managed guard后直接调用旧body。

当前事件初始“另一个丰臣继承人”fallback（.3约378–390行）**只排除alt，未排除normal**；any_scope_character/random_scope_character为本国集合，未发现跨国scope错误。若保留normal作为合法临时候选，提交时同实例免杀是必需的；不要只把normal也排除来掩盖问题，因为那会在只剩平胜时取消本可成立的继承议程。其余两个兄弟/父子模板不应因为都姓丰臣就合并身份。

## 定向补丁复核：前述两项已修正

2026-11-02后续源码复核，取代上文“两项仍需修改”的当前状态；上文保留发现与原始证据。当前 `ce_japan_gov_effects.txt:634` 已为Chokei前任，1880.7.1下界保留。`nesnd_jp_is_heikatsu`将两模板合并为一身份；保守选项的可用、effect重查、本国选择及global存在检查均使用同一union。选定现存人物先`set_ideology`再set_ruler，确认其实际成为JAP ruler后才结算死亡，且跳过与新ruler相同的旧heir。普通历史heir生成器595–603行的global guard和本国复用也已用union。此定向补丁未发现残余源码缺陷。

### any_character是否包括死人：当前本机证据不能作保证

E/triggers.log:100–104的全部契约是：`Iterate through all characters globally`，Supported Scopes none、Targets character；未说“all living”或“including dead”，也没有保证死者会一直保留。检索GAME本地说明与已导出的script_docs未找到死者对象生命周期或全局枚举的进一步契约。因此不能把“肯定会枚举死者”或“肯定不枚举死者”写成已核事实；目前只能确定**尚在该全局枚举集合中的同模板对象会阻止create**。此处没有启动游戏或用二手资料推定引擎内部行为。

### 不依赖枚举生命周期的原生实现依据

- G/common/character_templates/country_pru.txt:32–45：Bismarck使用 `NOT has_global_variable = bismarck_variable` 控制历史生成，`on_created`设置该global。
- G/common/on_actions/00_code_on_actions.txt:2603–2604说明on_character_death的root=character；2710–2714按Espartero模板设置 `espartero_is_dead_var`。因此模板创建时持久登记与死亡回调补登记均有实际原版调用链。
- G/common/character_templates/historical_agitators.txt:108–110亦在模板on_created设置 `louise_michel_spawn`。

推荐为两个平胜模板共用一个“曾生成”global，未来各自on_created都写同一旗标；on_character_death识别任一alias并补同一旗标。旧档初始化从实际可枚举的alias、既有 `heir_heikatsu_spawned`及可证明的旧事件完成记录回填。保守选项/普通生成器的create分支同时要求global不存在且当前全局无alias；已有活本国实例的复用分支不受born global阻挡。记录永不因人物死亡、属国关系、国家灭亡或改号而清零。

只在出生日期以前加global会封死尚未出生人物，不能这样做；日期到达也不等于这个人物一定曾创建。旧档若人物已被完全移除且没有任何持久史证，on_death补丁不会追溯旧死亡，必须如实保留这一旧档证据边界，不能靠日历假造全部出生历史。对其他具名日本继承人的同类要求可使用相同原版登记模式，但应逐人物保留出生下界和已有spawn证据。

本轮未修改任何候选脚本。此补充认证定向补丁源码闭包；全局登记建议尚须以父任务实际补丁为准，不能将建议当作已实施。
