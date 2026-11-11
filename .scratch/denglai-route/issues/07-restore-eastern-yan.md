# 07 复燕与北朝镇压后的整编

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（Victoria 3 1.15.0 / 26453692）  
Evidence: [逐文件清单与静态报告](../../../../../nesnd-workbench/reports/denglai-route/batch3/verification.json) · [内容树 near](../../../../../nesnd-workbench/reports/denglai-route/batch3/near.json) · [旗面预览](../../../../../nesnd-workbench/reports/denglai-route/batch3/flag-preview.png) · [改动前备份](../../../../../nesnd-workbench/backups/pre-change-denglai-restore-yan-20261110T235247Z/manifest.json)

## 1. 现象与期望

第二批两条路线结案后均进入「复燕」。登莱要取得东北出海口，辽东的旧部要恢复徐氏朝廷与旧职，女真诸部关心的是谁有权划定田地、渔场与营地。依据[定稿](../spec-v3.md)和[数值表](../numbers-v1.md)。

## 2. 原因与接口

原版的州易手后可能合并或重建州对象。起事前在北朝名下记录四州中已整编的州区域。「吞并东燕」目标执行后，由北朝下一日的专用 on_action 查找各区域中北朝实际拥有的州并直接恢复整编。东燕存续时清理记录。

## 3. 改了什么

- 新增同名 `nesnd_sha_restore_yan.txt` 于 `common/` 的 country_definitions、character_templates、flag_definitions、coat_of_arms/coat_of_arms、journal_entries、scripted_progress_bars、scripted_buttons、scripted_triggers、scripted_effects、script_values、diplomatic_actions、diplomatic_plays、war_goal_types、on_actions、static_modifiers，以及 `events/`。新增燕字旗 DDS 和两个 replace 目录下的复燕本地化，各 112 键，8 个事件均有引语。
- 接入文件为 `common/journal_entries/nesnd_sha_far_north.txt`、`common/journal_entries/nesnd_sha_republic.txt`、`common/scripted_buttons/nesnd_sha_far_north.txt`。前两者接结案、旧存档入口及东北流民，后者复用原有船费。此前两批中英文原文与北朝现有内容文件均保持作者版本。
- 徐氏远支拟名徐景衡，起事时 38 岁，辽东文化，松江籍。国旗取蓝底白色燕字。未定量处取朝鲜流亡者一次加 10 点燕旗、起事时朝鲜对两国各加 15 点关系，年度权重 70/15/15，已记入数值表。
- pdx.py 解析 19 份脚本。audit.py 对比备份，138 项既有提示逐项相同，开局领土、人口和建筑相同。重建内容树并对 60 个节点跑 near，本链涉及的 17 个变量及列表均核到写入和读取。Tiger 1.13 对日志 outcome、activation_description、战争目标镜像和争夺条件的提示已对照原版 1.15 文件。

## 4. 怎么复测

1. 新开登莱，整军或通商的远北日志结案后检查「复燕」。资助会党并观察每月「燕旗」。朝鲜拒约后应冷却三年。进度满而北朝安定时继续等待，北朝实际交战、发生革命或地权革命失败后才出分地事件。在此存档便于复测两案。
2. 查东燕君主、国旗、松江首都和两种主流文化，再查双方主战目标、北朝六个月修正及东燕军队。整军甲、乙分别为 50、58 营，登莱参战并立即取得两州或黑龙江北加海参崴口岸。通商甲、乙分别为 56、64 营，登莱付军费且保持中立，东燕战后存续才交地并结盟。
3. 让北朝执行吞并，过一天查州。开局原状下，收回的松江、黑龙江应为已整编。外东北、黑龙江北维持原有未整编状态，已划归登莱的土地仍属登莱。可另在举旗前整编黑龙江北，走通商线让北朝吞并，核对这一州也恢复。
4. 另试十二年未起事，或在期限到来前举旗并拖过期限。前者结案、保留原都、开放招徕东北流民，后者等战果。成功后可另用「定都海参崴」决议。

## 5. 遗留问题

未启动游戏。需观察保护国参战、军队实际补员、乙案割港位置、战后结盟、吞并与整编回调的先后，以及 AI 实际胜率。原生大迁徙按出发国和文化执行，按钮按四州居民筛选人选，具体从哪个州离开由引擎决定。第 4 批留待实测后开始。
