# 项目状态

Updated: 2026-11-06

## 当前

- 最新交付：[任务47 · 中文代理文本去平衡腔](../../.scratch/debug-release/issues/47-chinese-prose-voice.md)。中文 33 个文件、439 键逐条重写；南朝内战事件恢复作者原句口气。只改中文，英文未动。
- 验证等级：STATIC_PASS（逐键比对动态代码、数字、颜色；UTF-8 BOM、语言头、键集合、无重复键）。未启动游戏，未实机验证。
- 分支：`claude/fervent-ramanujan-y1ajzz`，未合并 main，草稿 PR：EricYuyangLiu2286/Neo-Era-Southern-and-Northern-Dynasties#3。
- 主 MOD：本轮在云端完成，无法写入本机主 MOD。需在本机拉取该分支后同步。

## 待办

- 英文对应键按新中文改写（另开任务）。
- 34 个“作者改稿后又被代理改动”的键，本轮未动，待作者决定。清单见任务47。
- `nesnd_india_l_simp_chinese.yml`：本轮改了 12 键。本机主 MOD 若有未上传改稿，同步时须先比对，避免互相覆盖。
- 实机检查改写后的事件、日志和按钮显示（行宽、换行）。

## 历史

- 2026-11-06 任务46：四份英文同步与法国古吉拉特分舰队，STATIC_PASS。
- 更早记录见 [执行地图](../../.scratch/debug-release/map.md)。

## 更新规则

1. 每次交付后改写“当前”和“待办”，把上一轮“当前”压成一行移入“历史”，不删旧条目。
2. 只写结论和链接；过程、表格和证据放 `.scratch` 任务与 `development/evidence/`。
3. 写明验证等级（NOT_RUN／STATIC_PASS／ENGINE_PARTIAL／ENGINE_PASS），静态检查不得写成游戏内验证。
4. 写明分支、是否合并 main、是否已同步主 MOD。
