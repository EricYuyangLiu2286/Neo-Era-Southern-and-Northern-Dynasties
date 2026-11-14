# 08 勘金条件与《八州约书》后续文案

Record: implementation  
Category: bug  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS，待作者实测  
Evidence: [检查与文件清单](../../../../../nesnd-workbench/reports/denglai-route/yan-prose-and-survey/verification.json) · [改前备份](../../../../../nesnd-workbench/backups/pre-change-denglai-yan-author-prose-20261111T014117Z/manifest.json)

## 1. 现象与期望

作者截图显示勘金地点一项为红，冷却、次数、破产检查均通过。按钮应从登莱领有的三个候选州中选择仍有砂金且余量最多的一处。作者另已改写「复燕之路」至「海参崴」标题，后续文字与英文应接得上《八州约书》。

## 2. 原因与接口

旧按钮把地名与一个未显示的差值检查叠在同一项条件里。差值以地图初始储量减两类建筑容量估算，悬停无法显示哪个州尚有砂金。原版橡胶事件在州区域使用 remaining_undepleted，在具体所属州执行 force_resource_discovery。本机没有本次截图的存档，无法还原三州当时的余量。

## 3. 改了什么

- 勘金按钮、条件和数值文件改在 common/scripted_buttons、common/scripted_triggers、common/script_values 下的 nesnd_sha_far_north.txt。资格与排序都读金矿场的原生剩余资源，选定州后才执行勘探、扣款和记次。中英文远北本地化拆开显示领土与储量两项条件，地名引用州键。
- 中英文复燕本地化承接作者改稿，重写「海参崴」以后的胜败、筹备事件与引语，并译出作者改写的前史、盖州誓词和李合德原话。叙事保留东北六州与登莱合称八州的地理口径，玩法提示列明参与起事或供船商寻人的州；地点、割地与数值沿用定稿。events/nesnd_sha_restore_yan.txt 给即位与清丈事件传入对方国家供显示国名。
- 比较备份、pdx.py、双语键与动态引用、audit.py、内容树 index 与 near 均已检查。Tiger 1.13 将排序参数当作建筑组，本机 1.15 的资源触发器和原版事件使用建筑键。排序与实际发现仍待实机。

## 4. 怎么复测

重新加载 MOD 后，选登莱通商路线。查看勘金悬停的两个地点条件。在开局储量尚存的局面，应能派队并见到「金沙」。查看目标州、支出和次数，次日再看按钮的 24 个月冷却。若三州仍属登莱、余矿却为红，只需截余矿面板和游戏日期即可区分当前资源状态。

## 5. 遗留问题

未启动游戏。待看实机剩余砂金、优先级、发现量及动态国名。第三批之后的内容尚待作者实测。
