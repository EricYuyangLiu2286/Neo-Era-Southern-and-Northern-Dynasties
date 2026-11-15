Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-14）
Blocked by: none
Validation: STATIC_PASS
Evidence: 日志副本 `nesnd-workbench/reports/2026-11-14-keju-law-variant/logs/`（部署 `0fc4bf0b`）

# 105 联合州事权目标：`has_law_or_variant` 报错

## 1. 现象与期望

作者截图：error.log 22:10 刷屏 `has_law_or_variant trigger [ Given law is a variant, we expect the parent ]`，位置 `common/script_values/nesnd_civic_routes.txt:93`（存档副本中共 490 条）。

## 2. 原因

`nesnd_usm_mandate_settled_value` 用 `has_law_or_variant = law_type:law_nesnd_keju_voting`。科举投票是 `law_wealth_voting` 的变体，这个触发器只接受母法。原版检查某个变体时用 `has_law`（如 `has_law = law_type:law_crownland_diets`）。2026-11-14 90e4f6d 加入。

## 3. 改了什么

- `common/script_values/nesnd_civic_routes.txt:93`：改为 `has_law = law_type:law_nesnd_keju_voting`。与说明文字「科举投票使制度目标向朝廷移动5点」一致。源目录中没有其他把变体法传给 `has_law_or_variant` 的写法。

## 4. 怎么复测

读档即可。联合州事权日志打开后，error.log 不再出现该报错。实行科举投票时，「撤回支持后的制度目标」比原先多 5。

## 5. 遗留问题

无。
