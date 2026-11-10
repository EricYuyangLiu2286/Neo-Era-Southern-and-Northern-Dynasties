# 66 《接旗》作为主菜单默认背景

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [注册与选取分支的场外检查](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-main-menu-default/verification.json>)

## 现象与期望

启用 MOD 后第一次进主菜单就能看见《接旗》，并可在主菜单背景列表首项找到南北朝。手选其他背景后应能记住。

## 原因

1.15.0 的 `gui/theme_selector_window.gui:1187` 使用 `ThemeCategory.GetThemes`。前端按注册表填充该分类；没有有效选择时取首个可用背景。已有有效选择时读已存的键。
原版 `common/themes/00_themes.txt:13` 的 `main_menu_image_base` 属于 `default` 批量主题组。前端播放这种无 DLC 要求的背景时，再从可用 DLC 里选视频，因此旧设置可以写着「默认」而画面是俄国。1.15.0 本机文件静态定位：分类列表 RVA 0x2134950，默认初始化 0x23ebfc0，已选项读取 0x23ec6a0，菜单视频分派 0x230c300。

## 改了什么

- `common/themes/00_00_nesnd_main_menu.txt` 提前注册独立选项，沿用任务64的键。
- `common/themes/nesnd_main_menu.txt` 将已保存的原版默认入口接到《接旗》；把原版完整的自动选片规则保留在「原版自动（随 DLC）」及原版批量默认预设里。
- 中英各更新一份主菜单本地化，并在两个语言的 `replace/` 下各加一份默认入口标签。六个非默认原版背景及其 DLC 条件与原版相同。

## 怎么复测

只启用主 MOD 后进入主菜单，打开 Theme → 主菜单背景，检查首项与「默认（南 · 北）」。选后者，关闭选择器、重启，应显示《接旗》。手选俄国背景后再重启，应仍是俄国；「原版自动（随 DLC）」应按已启用的 DLC 选片。无需新开战役。

## 遗留问题

16 组场外用例通过，包括空设置、失效键、旧默认、原 NESND 选择、各原版背景及有无俄国 DLC 的自动选择。已核对视频与任务64哈希相同。本次未启动游戏，最终界面顺序与重启表现待作者复测。其他 MOD 同时覆盖默认背景时，结果取决于实际加载顺序。
