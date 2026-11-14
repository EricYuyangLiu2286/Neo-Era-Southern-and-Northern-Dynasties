# 02 宫廷与共和日志美术

- Record: implementation
- Category: enhancement
- Status: ready-for-agent
- Execution: completed
- Assignee: Codex
- Blocked by: none
- Validation: STATIC_PASS
- Evidence: [已安装 DDS 核验](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-court-power-art-east-west-rev2/installed-validation.json>)、[本版全套预览](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-court-power-art-east-west-rev2/preview.jpg>)

## 现象与期望

作者要求按[画稿](../art-prompt.md)逐张绘制 2 张面板、16 张行动卡与 4 枚透明图标，交付 PNG 与游戏所用 DDS。

## 原因

两个日志当前使用原版占位图。宫廷素材须兼用于东亚、奥地利、奥斯曼及波斯等国。

## 改了什么

18 张面板与行动卡放入 `gfx/interface/illustrations/journal/nesnd_power/`，4 枚图标放入 `gfx/interface/icons/nesnd_power/`。原画和最终尺寸的 PNG 分别保存在工作台证据目录的 `source/` 和 `png/`。

## 怎么复测

已逐文件读回 DDS、核对尺寸与数据长度。插图为 DXT5、11 级 mipmap，图标为单层 B8G8R8A8，与 PNG 解码后的 RGBA 像素完全一致。已检查横幅裁切与费用图标的 24 像素缩略图。

## 遗留问题

游戏内叠加人物像和按钮文字的效果待作者实测。

## 接入（Claude，2026-11-11）

- `common/scripted_buttons/nesnd_power.txt`：16 个按钮的 `icon` 改为各自的行动卡底图。宫廷 8 个按钮加 `tags = { nesnd_palace }`。
- `gui/journal_entry_widgets/nesnd_power.gui`：两个人物面板分别用宫廷、共和面板底图。卡片费用图标按 `ScriptedButton.HasTag('nesnd_palace')` 在宫廷、共和两枚之间切换。
- 两个日志的 `icon` 改为新日志图标（经 WORK `journal_template.txt` 生成）。
- 检查：22 个引用全部指向存在的文件，没有未引用的素材。解析与语言服务器检查通过。游戏内显示待作者复测。

## 按作者参考重绘

参照六张图的空间和席位关系，将宫廷改为宽殿、矮台、两侧列班，将共和议场改为高侧窗、直排长席和主席长桌。22 张 DDS 已同名覆盖，已按三个脚本的引用逐一读回；22 份文件的哈希均已改变。18 张插图共 198 层 mipmap 均已解码，4 枚单层图标与对应 RGBA PNG 逐像素相同。旧版 DDS 保存在同级工作台目录 `2026-11-11-court-power-art/dds/`。

## 左东右西定稿

作者确认每幅图在中线交接风格，两侧共用一个空间、一件道具或一个动作。全套 22 张同名替换，已从脚本的安装路径复核尺寸、编码、文件长度与全部纹理层，费用图标另按 24×24 检视。上一版 22 张 DDS 的哈希均与工作台 `2026-11-11-court-power-art-neutral/dds/` 存档一致。

## 发式、地区服饰与原定画风修订

作者指出「动员」中出现清式辫发。重绘集会人群，检查原画和横幅里可见的后颈与衣背；中国人物按全发束髻、方巾或软帽处理。左侧按场合采用中国、日本、南亚、波斯的衣物和器具，右侧增加中东欧、多瑙流域与巴尔干的席位、官署与市民衣着。全套重读原画稿，按暖赭、深青、低对比侧光与中景人物处理。22 张 DDS 已同名替换，安装检查与 24 像素图标检查通过，待实机查看。

## 三张行动卡复核

「整饬宫廷」跨墙巨闩为废稿，已从主 MOD 的 DDS 确认实际显示门缝上的短搭扣。「安抚」重画成三人劝坐与交谈，「推法」重画为一名坐在桌前的书记员执笔按卷。这两张已同名替换，三张均在安装路径读回并解码 11 层 BC3。[实际纹理预览](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-court-power-art-east-west-rev2-two-cards/installed-preview.jpg>)、[逐张核验](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-court-power-art-east-west-rev2-two-cards/validation.json>)。
