# 02 · 删除区域发展空壳（七国）

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Claude
Blocked by: none
Validation: STATIC_PASS

## 现象与期望

作者：“已停用的空壳日志删除。不要留冗余文件。”随后：“一并删除”（其余六国同类空壳）。

## 原因

2026-11-04 的七国区域发展（普鲁士、奥地利、奥斯曼、埃及、墨西哥、美国、秘鲁）停用后，日志改成 possible = no 的空壳，效果改成 `always = no`，入口、完成条件、进度条、奖励修正和本地化都已无人调用。普鲁士身份读的 `nesnd_rg_prussian_origin` 与共同防卫的 `nesnd_prussian_coalition_origin` 重复；外交框架读的 `nesnd_rg_pending` 已无写入者。

## 改了什么

- 整份删除：`common/journal_entries/nesnd_regional_development.txt`、`…_overrides.txt`，`common/on_actions/`、`scripted_effects/`、`scripted_progress_bars/`、`scripted_triggers/`、`static_modifiers/` 下的 `nesnd_regional_development.txt`，两语 `nesnd_regional_development_l_*.yml`。
- `common/journal_entries/nesnd_egypt_independence.txt` 末尾：原样接收仍在生效的 `REPLACE:je_veiled_protectorate`（关闭原版埃及“帷幕保护国”），行为不变。
- `common/scripted_triggers/nesnd_europe_america.txt:3`：普鲁士身份只认 `nesnd_prussian_coalition_origin`。
- `common/on_actions/nesnd_canon_diplomacy.txt:3`、`common/scripted_effects/nesnd_canon_diplomacy.txt:79`：去掉 `nesnd_rg_pending` 的残留读取。

## 怎么复测

新开局：普鲁士日志面板只有“德意志的共同防卫”；控制台 `change_tag NGF` 后它仍在。埃及开局不应出现“帷幕保护国”。error.log 不应出现 `nesnd_rg_` 相关报错。

备份：WORK `backups/pre-change-germany-rg-pru-stub-20261112T224530Z`、`backups/pre-change-germany-rg-all-stubs-20261112T224821Z`。三份改动文件解析通过；audit 与迁移后基线一致（2/132/4，均为旧问题）；v3tree 未解析引用 16→11。

## 遗留问题

无。
