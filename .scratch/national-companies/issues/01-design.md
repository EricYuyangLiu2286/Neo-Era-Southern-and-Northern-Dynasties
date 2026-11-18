Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Blocked by: none
Validation: STATIC_PASS
Evidence: [设计表](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-18-national-companies/design-table.md>)、[画图提示词](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-18-national-companies/codex-icon-prompt.md>)

# 01 MOD 自建国家的本国公司

## 1. 现象与期望

“MOD 自建的国家几乎没有自己的公司。……按各国开局位置和风格补齐”。按地区和条件开放，解锁方式多样，数值对标原版。作者确认设计后，三轮改名，名字按作者 2026-11-18 定稿；一部分公司生成经理。

## 2. 原因

此前只有作者三家（`common/company_types/ce_companies_china.txt`）与代理稿北海公司、登莱远洋公司。

## 3. 改了什么（源目录，全部新增）

- `common/company_types/nesnd_national_companies.txt`：19 家公司。
- `common/script_values/nesnd_national_companies.txt`：五个先到先得用的地区建筑合计。
- `common/scripted_triggers/nesnd_national_companies.txt`：远南澳新诸州。
- `common/prestige_goods/nesnd_national_prestige_goods.txt`：鲸油、羊绒披肩、库姆比呢、远南细羊毛（贴图暂用原版）。
- `common/character_templates/nesnd_national_company_executives.txt`：7 名经理。
- `events/nesnd_national_companies.txt`：4 个特许事件；`common/on_actions/nesnd_national_companies.txt`：年度脉冲；`common/static_modifiers/nesnd_national_companies.txt`：开办经费。
- `common/journal_entries/nesnd_national_companies.txt`：「横贯大陆的干线」。
- 中英本地化 `nesnd_national_companies_l_*.yml`。

部署 `a6699181`。

## 4. 怎么复测

见交付说明与设计表。新开局或读档均可（公司、事件、日志都按条件即时判断）。

## 5. 遗留问题

- 北海公司、登莱远洋公司只限登莱成立，与本批规则不一致。未改。
- 技能 `lookup/canon/worldbook.json` 中文为乱码。未改。
- 远北“宗主国兜底”：宗主国在该地区无州时能否成立公司，未实机验证。
- 北朝西北工业总行无经理，待作者指定。
