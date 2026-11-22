Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Claude（2026-11-22）
Blocked by: none
Validation: STATIC_PASS
Evidence: 备份 `nesnd-workbench/backups/pre-change-hus-west-province-vars-20261122T201131Z/`；Tiger 差量 `nesnd-workbench/reports/2026-11-22-hus-west-province-vars/tiger/`（新增 0）

# 100 东洲「西进」：地块上读写变量报错

## 1. 现象

error.log（部署 8ac873a）每次月脉冲报三条，都从日志 `nesnd_hus_west_lever` 的 on_monthly_pulse（journal_entries 第 301 行）进来：

- `set_variable effect [ This scope doesn't support variables. Scope: 地块 … ]`，scripted_effects/nesnd_acw_slavery_question.txt:94
- `remove_variable effect [ This scope does not have variables ]`，同文件 :103、:104

## 2. 原因

西进把宣称地区里美方的地块记进州地区名单 `nesnd_hus_west_land`（这一步不报错，遍历名单能走到地块），随后在地块身上读写 `nesnd_hus_west_giver`、`_recent_giver`、`_awarded`、`_pending_play`。地块作用域不能存变量，写入全部失败，读取永远为空，所以 `nesnd_hus_west_region_won` 从来不成立，「已判给」这项玩法没有生效过。

## 3. 改了什么

- `common/scripted_effects/nesnd_acw_slavery_question.txt`
  - `nesnd_hus_west_observe_owner`（地块作用域，PREV 为所在州地区；两个调用处都从州地区遍历名单）：持有国是美方（USA/CSA/FSA）且地块不在它的 `nesnd_hus_west_held_land` 里时，从其他美方国家的名单移出，加进它的名单。转到非美方手里时留在最后一个美方持有国的名单里。持有国不是东洲时，从州地区的 `nesnd_hus_west_awarded_land` 移出。
  - `nesnd_hus_west_territorial_award`：「原持有国是 X」改判为「在 X 的名单里」；判给的地块进州地区的 `nesnd_hus_west_awarded_land`，博弈进 `nesnd_hus_west_award_plays`，都先查重。
  - `nesnd_hus_west_make_claim`：登记地块后对该地区跑一遍 observe，美方持有国的名单当场记下。
  - `nesnd_hus_west_cleanup`：清空每个州地区的三个名单和每个国家的 `nesnd_hus_west_held_land`。
- `common/scripted_triggers/nesnd_acw_slavery_question.txt`：`nesnd_hus_west_region_won` 改读 `nesnd_hus_west_awarded_land`，博弈一项改为「`nesnd_hus_west_award_plays` 里没有仍是战争、又没有 `nesnd_hus_west_peace_signed` 的博弈」。
- 所有 `is_target_in_variable_list` 前都先查 `has_variable_list`：名单不存在时求长度会报错（engine-facts「名单长度」），成员判断是否也报未查到，按同样做法守住。
- 日志文件与 on_action 文件未改（调用写法不变）。

## 4. 与原写法的差别

原来地块交出后把原持有国留 1 天（`recent_giver`），之后清掉。现在留在最后一个美方持有国的名单里，直到地块再被别的美方国家持有或日志结束。差别只在一种情形：地块早先已归东洲，后来同一地区再由战争目标判给东洲、被判方正是它最后的美方持有国，现在这块地也算判给，原来超过 1 天就不算。判给时仍要求地块的持有国是被判方或东洲。

## 5. 全 MOD 同类排查

扫了 `every/random/any/ordered_*province*` 块内与 `p:x…` 块内的变量读写、名单里的地块、保存的地块作用域。只有本处。`scripted_effects/nesnd_europe_america.txt:135` 把地块放进 c:USA 的名单，是对的写法，未改。大陆会议副本未改。

## 6. 旧档

地块变量从来没写进去过，不需要迁移。已登记的 `nesnd_hus_west_land` 照用；没有原持有国记录的地块，下一次月脉冲观察到持有国是美方国家时补上。

## 7. 检查

script_xcheck：本组文件 10 条，都是改前已有（三条 progress_condition 误报、七条原版或旧变量），新增 0。static_lints：locsv/tipctx/deadhook/replace 0。tiger_delta：新增 0。

## 8. 待实机

1. 月脉冲和换主时不再报上面三条。
2. 东洲宣称地区、战争目标判给、和约签订后地区内地块全归东洲，`nesnd_hus_west_region_won` 成立（成功计数加一）。
