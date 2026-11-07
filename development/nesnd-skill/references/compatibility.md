# 东亚服装与 UI 兼容

## East Asian Clothes: Redux

用户于 2026-10-31 明确要求：同时启用本 MOD 与 EACR，只写引用/兼容脚本，禁止复制其模型、纹理、动画、附件等素材到本 MOD 或发布物。不存在“少量复制即可”的例外。工坊目录始终只读。此前素材审计见 `WORK/reports/eacr-resource-audit-20261031.json`：主 MOD 45 个媒体文件相对原备份无新增/更改，无 EACR 精确哈希匹配；这是本次修改溯源，不是对既有素材作全面版权鉴定。

当前版本 1.0.4 的源码依据：

- `common/scripted_triggers/EACR_scripted_triggers.txt` 的 `EACR_st_culture_is_chinese` 检查 `heritage_han` 或 `tradition_sinosphere`，排除韩国/越南/日本 heritage。文化名称与国家 tag 不足以判断。
- `EACR_st_pop_or_char_is_chinese` 从肖像 scope 的 `scope:pop` 或 `scope:character` 找 culture。`EACR_st_is_qing_china` 同时认 CHI 和 manchu 主文化；不能把 USM 当 CHI 来骗服装。
- `EACR_st_is_unwesternized` 综合原版西式衣服触发器、WCR兼容、特定国家/军队逻辑。`EACR_st_char_is_monarch/heir` 处理摄政，不能只检查 `is_ruler`。
- `00_EACR_mod_compat_trigger.txt` 是作者给第三方的接口说明，`zz_EACR_mod_compat_trigger.txt` 用 `REPLACE_OR_CREATE:` 提供激活状态和 court base 接口。第三方可定义默认 inactive trigger，然后由 EACR 替换；实际加载顺序仍需测试。
- `gfx/portraits/portrait_modifiers/EACR_clothes.txt`/headgear/hairstyles 决定使用哪个 gene 模板，`common/genes/EAC_genes_*.txt` → `gfx/portraits/accessories` → `gfx/models/portraits/attachments` 提供实际模型。

任务步骤：核查本 MOD 自定义文化的 heritage/traditions 与服装判定是否相容；核查自定义儒教是否需要最小触发器补丁；以同一人物在“仅主MOD”“EACR+主MOD”的两组新开局比对。现有 `common/decisions/ce_cloth_redux_decisions.txt` 全部为注释，不能当有效兼容实现。不得激活其中移除主文化的旧方法。

若需要补丁，在主 MOD 独立兼容文件里只替换必要的触发器并保留原逻辑，明确 EACR 是否必需及加载顺序；不编辑 Workshop 资源，不通过改 religion/primary culture 实现视觉需求。没有 EACR 时应正常退回原版服装，不留下未知 gene/template。

## UI

先读 GAME 对应页面，CMF 是共享集成模式参考，Expanded Building Grid 是 `states_panel_buildings.gui` 的实际改法。把需要改变的 widget、datacontext、位置、尺寸、tooltip、点击效果列清楚；同名 GUI 文件整替换容易遮蔽新版本字段。优先原版 JE widget anchor / scripted widget 或框架扩展点。

验证至少含简中/英文、不同 UI scale、窄窗口、满建筑列表、tooltip、按钮操作；没有实际安装依赖时不能宣称与其兼容。只参考其布局不应强加完整框架依赖。

### 日志人物像与悬停

原版 1.15.0 的 `gui/journal_entry_widgets/ep2_japan_widgets.gui` 给出了交互式人物像的完整上下文。大名列表用 `GetList('daimyos_list')` 作 `fixedgridbox` 的数据源（506、520–521 行），子控件在列表项内检查 `Scope.GetCharacter.IsValid`，并以 `[Scope.AccessCharacter]` 绑定头像（13–35 行）。从变量取人物时，沿数据源、列表项或父控件、头像、继承的 `FancyTooltip_Character` 查到实际使用人物的方法。人物列表只写入有效对象；列表为空时不会创建头像项。

`[GetGlobalVariable('…').AccessCharacter]` 会在 GUI 加载时被拒绝，原生日志报 `Invalid promote … requires non const promote`。直接换成 `GetCharacter` 可以读人物，悬停里的 `Character.GetMilitaryFormation.GetName` 仍可能因收到只读人物报 `wrong constness`。复制原版控件时一并核对上游如何提供可变人物。绑定已被拒绝时，子控件的 `Character.IsValid` 也会因缺失上下文而失败。

游戏外解析可以检查结构和方法名；可变性要核对当前版本的原版调用链和引擎日志。实机复测依次打开日志、悬停头像、点击进入人物面板，分别观察实例化、提示求值和交互。无符号的空地址异常只能给出异常类型与时刻，具体故障链要靠此前的绑定报错定位。
