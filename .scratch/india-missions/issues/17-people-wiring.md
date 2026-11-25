# 17 民情接线（批次 13）

Record: implementation  
Category: enhancement  
Status: ready-for-agent  
Execution: completed  
Assignee: agy  
Blocked by: none  
Validation: STATIC_PASS  
Evidence: [交付记录](../../../../nesnd-workbench/reports/2026-11-21-india-development/民情/交付记录.md) · [核对脚本](../../../../nesnd-workbench/reports/2026-11-21-india-development/民情/verify_people.py)

## 现象与期望

印度各日志此前多在国家层面的按钮与请求之间流转，未接到原版的人口状态（激进派、忠诚派、动荡、文化少数运动、文化热忱与海外文化社群）。按总纲第〇节 R1–R7 与 P1–P4、P5 后半，将饥荒援助、举事的烽火、谋求独立、属邦动向、缉查地方组织与印度国家获得认可全部接到原版人口输入上，并补齐两处小修。

## 改动

- 共用触发器（`common/scripted_triggers/nesnd_india_core.txt`）：新增 `nesnd_india_culture`（`has_discrimination_trait_group = heritage_group_south_asian`）与 `nesnd_india_cultural_minority_movement`（`movement_cultural_minority` 且文化为印度文化）。
- 饥荒回声与外迁（P1、P5 后半）：`nesnd_mug_famine_struck` 与 `nesnd_mug_famine_affected_state` 兼认原版 `has_famine = yes` 与事件标记州。饥荒援助（种类 9）同意时，在清除州标记前对求援国受灾各州的印度文化人口 `add_loyalists_in_state = 0.05`；被拒、超时未答复或排队 90 日作罢（结果 1、2、3、6）时，在 `nesnd_mug.24` 的 `immediate` 对受灾各州印度文化人口 `add_radicals_in_state = 0.10`，并在两个选项的提示里写明；受灾州 ≥ 3 且 10 年冷却未在期间时，取求援国人口最多的印度主体文化，向与其关系最高且在非印度州持有该文化社群（符合大规模迁徙目标条件）的外国州发起 `create_mass_migration`，并弹出通知事件 `nesnd_mug.25`（中英 flavor）。
- 起事读民情（P2）：`nesnd_india_case_launch_ready` 新增 `nesnd_india_case_popular_ready`，要求起事州动荡 ≥ 0.25 或州内印度文化在所属国存在活跃的文化少数运动；「举事的烽火」正文补写「起事要看当地民情」。批次 12 已在 `nesnd_india_case_failed` 实现起事失败州激进 +20%，不重复。
- 资助印度文化运动与宗主可见（P3）：`nesnd_india_indep_choose_movement` 另选宗主国内支持度最高的印度文化少数运动（`indep_choice_indian`）；`nesnd_india_indep.1` 新增该选项（无此类运动时灰显并写明原因）；`nesnd_india_indep_fund` 资助印度文化少数运动时沿用原扣款、修正与败露，另令该文化人口在宗主国各州 `add_radicals_in_state = 0.05`。「属邦动向」正文增一行，经脚本值 `nesnd_india_indep_indian_movements_count` 与 `nesnd_india_indep_indian_funded_count` 显示境内印度文化少数运动总数及受资助数。
- 热忱（P4）：「缉查地方组织」六枚镇压按钮每次缉查对其对应印度文化（`telegu`/`tamil`/`kannada`/`malayalam`/`gujarati`）施加 `add_fervor_target_modifier` −5、持续 1825 日（5 年）；新增月度与建国回调 `nesnd_india_recognition_check` → `nesnd_india_recognition_watch`，印度国家首次不再为 `unrecognized` 时，对本国人口最多的印度主体文化施加 `add_fervor_target_modifier` +5、持续 3650 日（10 年），以 `nesnd_india_recognition_fervor_done` 防重；「新秩序」已有热忱加成不动。
- 两件小事：`nesnd_india_core.6.d_subject`、`.6.d_seat` 中英分别将「朝廷 / court」改为「政府 / government」；`nesnd_india_indep_record_departure` 中 `nesnd_india_indep_second_departed` 补 `days = 3650`。

## 代码无法证实

数值均为默认值，实机测试后再调。交付记录「代码无法证实」一节列了 `has_cultural_community` 传动态作用域文化、单次触发器内 `save_temporary_scope_as` 与 `scope:x.owner` 链式跳转等原版未见完整同构调用的写法。
