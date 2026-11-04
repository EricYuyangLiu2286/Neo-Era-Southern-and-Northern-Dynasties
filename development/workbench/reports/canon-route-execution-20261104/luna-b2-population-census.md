# B2人口源码普查（只读）

人口单位：直接 owner-state 中对应 `region_state:TAG` 的所有有效 `create_pop.size` 求和。使用 PDX 保序解析器，重复 `create_pop`、`region_state` 和 `create_state` 节点均逐项保留；注释文本不进入 AST。数值表示候选源码，不是引擎开局/存档实时人口。

候选：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\canon-route-execution-20261104-a`

## YN1

直接有人口州 8；总人口 4,408,410；最大州 QUEENSLAND 1,563,200 (35.46%)。
- Australia: 3,938,978 (89.35%)；组内最大州 QUEENSLAND 1,563,200 (39.69% of group) — QUEENSLAND 1,563,200 (35.46% of national P), NEW_SOUTH_WALES 1,173,120 (26.61% of national P), VICTORIA 555,794 (12.61% of national P), SOUTH_AUSTRALIA 379,800 (8.62% of national P), NORTHERN_TERRITORY 141,500 (3.21% of national P), WESTERN_AUSTRALIA 125,564 (2.85% of national P)
- New Zealand: 469,432 (10.65%)；组内最大州 NORTH_ISLAND 293,004 (62.42% of group) — NORTH_ISLAND 293,004 (6.65% of national P), SOUTH_ISLAND 176,428 (4.00% of national P)
- 所有直接人口州：QUEENSLAND 1,563,200 (35.46%), NEW_SOUTH_WALES 1,173,120 (26.61%), VICTORIA 555,794 (12.61%), SOUTH_AUSTRALIA 379,800 (8.62%), NORTH_ISLAND 293,004 (6.65%), SOUTH_ISLAND 176,428 (4.00%), NORTHERN_TERRITORY 141,500 (3.21%), WESTERN_AUSTRALIA 125,564 (2.85%)

## BUR

直接有人口州 4；总人口 3,599,494；最大州 PEGU 1,318,644 (36.63%)。
- Upper/interior: 2,280,850 (63.37%)；组内最大州 MANDALAY 1,047,934 (45.94% of group) — MANDALAY 1,047,934 (29.11% of national P), KACHIN 764,191 (21.23% of national P), SHAN_STATES 468,725 (13.02% of national P)
- Lower: 1,318,644 (36.63%)；组内最大州 PEGU 1,318,644 (100.00% of group) — PEGU 1,318,644 (36.63% of national P)
- 所有直接人口州：PEGU 1,318,644 (36.63%), MANDALAY 1,047,934 (29.11%), KACHIN 764,191 (21.23%), SHAN_STATES 468,725 (13.02%)

## SIA

直接有人口州 6；总人口 3,866,645；最大州 BANGKOK 1,618,404 (41.86%)。
- Central: 1,618,404 (41.86%)；组内最大州 BANGKOK 1,618,404 (100.00% of group) — BANGKOK 1,618,404 (41.86% of national P)
- Interior: 1,333,406 (34.48%)；组内最大州 NAKHON_RATCHASIMA 1,182,312 (88.67% of group) — NAKHON_RATCHASIMA 1,182,312 (30.58% of national P), LAOS 151,094 (3.91% of national P)
- Outer: 914,835 (23.66%)；组内最大州 TENASSERIM 348,700 (38.12% of group) — TENASSERIM 348,700 (9.02% of national P), CAMBODIA 301,335 (7.79% of national P), MALAYA 264,800 (6.85% of national P)
- 所有直接人口州：BANGKOK 1,618,404 (41.86%), NAKHON_RATCHASIMA 1,182,312 (30.58%), TENASSERIM 348,700 (9.02%), CAMBODIA 301,335 (7.79%), MALAYA 264,800 (6.85%), LAOS 151,094 (3.91%)

## 代表国家

|TAG|直接人口州数|总人口|最大州占比|最大两州合计占比|
|---|---:|---:|---:|---:|
|PHI|4|3,550,279|53.92%|92.90%|
|DEI|15|10,194,297|37.88%|58.50%|
|DAI|4|4,356,365|57.54%|95.46%|
|HYD|2|10,855,454|78.76%|100.00%|
|GWA|2|1,450,619|98.08%|100.00%|

代表国家逐州：
- PHI: LUZON 1,914,456 (53.92%), VISAYAS 1,383,743 (38.98%), MINDANAO 238,086 (6.71%), WEST_MICRONESIA 13,994 (0.39%)
- DEI: WEST_JAVA 3,861,212 (37.88%), CENTRAL_JAVA 2,102,816 (20.63%), EAST_JAVA 2,080,396 (20.41%), SUNDA_ISLANDS 705,184 (6.92%), TENASSERIM 358,600 (3.52%), MOLUCCAS 254,291 (2.49%), NORTH_SUMATRA 199,571 (1.96%), ARAKAN 188,316 (1.85%), SOUTH_SUMATRA 132,694 (1.30%), MALAYA 124,196 (1.22%), ACEH 55,875 (0.55%), WEST_BORNEO 54,660 (0.54%), CELEBES 49,863 (0.49%), EAST_BORNEO 20,700 (0.20%), PEGU 5,923 (0.06%)
- DAI: ANNAM 2,506,625 (57.54%), MEKONG 1,651,759 (37.92%), SOUTH_CENTRAL_VIETNAM 105,429 (2.42%), LAOS 92,552 (2.12%)
- HYD: HYDERABAD 8,549,837 (78.76%), CENTRAL_PROVINCES 2,305,617 (21.24%)
- GWA: MALWA 1,422,840 (98.08%), RAJPUTANA 27,779 (1.92%)

## 来源 SHA-256

|相对C路径|SHA-256|
|---|---|
|`common/history/states/00_states.txt`|`a07cb15be572ca63c8cd1cc3706d1c78ca55f7edbc955a031bff30c00b9e1caa`|
|`common/history/pops/10_india.txt`|`2d4674d742540bc1168daf3fe2397185a670dd7bae50e2dcf013605f6a3ad1d3`|
|`common/history/pops/11_east_asia.txt`|`85b9ef1a805b3b033fb31009b55d270c8d83736749c6255f8d1f4ab45711fd6b`|
|`common/history/pops/12_indonesia.txt`|`4edfc72f48cf30abe74518dd1af81bc0e4d1683518825f005fbafedde1323a29`|
|`common/history/pops/13_australasia.txt`|`8b12ed15ffdd378d7d0e337753453eadaa13a1d88f8f3aeeaf1aae9436309d5e`|

只统计 states 中明确由该国拥有、且 pops 有该 TAG 的州份额。共享州分开计本国份额。该源码普查不提供运行态的人口变动、宗主/市场状态或实辖 controller。

## 解析工具 SHA-256

|工具|SHA-256|
|---|---|
|`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\tools\canon_routes_context.py`|`51b165793ad262925ad1ed7fb5685ff718c058c8926d5320113ef595781e6e90`|
|`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\tools\qin_persia_context.py`|`d3ae8fa7a188213000c66e0ba1bb60de38ab608a755b6dd99a52beb4c36ac421`|
|`C:\Users\Eric Liu\.codex\skills\nesnd-victoria3\scripts\pdx.py`|`6807cc7df7e628b018556ddb58472d09dbb5a20219f777026df3fb011db4594e`|
