# 「西岸的砝码」共同殖民误完成与十州目标

Record: implementation
Category: bug
Status: ready-for-human
Execution: completed
Assignee: Codex
Validation: STATIC_PASS，待作者新开局复测
Deployment: 480a9e72ce21d40e091e59e9679d4c6b

## 现象与期望

玩家反馈提出边境宣称时，共同持有的州区会立即结束日志。用户选择 B，要求十个宣称州全部经领土要求取得才完成。自动宣称、自动东进分别开关。内战及战后向实际持州的 USA、CSA、FSA 索地。

## 原因

宣称记录的是 state_region，原完成条件只要求东洲有该州区任一 state。东洲已有部分立即匹配。原失败和失效条件还会在美国日志结束或不再接壤时结束本条目。

## 修改

登记十个州区及其对方省份，原生归还州、征服州的 on_enforced 记录取得事实。当前持有且战争已经结束才计数。两个独立自动化开关默认关闭，月度执行与手动共享条件。内战及战后保留日志，战后 +2 宣称是本次采用的数值。

11 个运行文件、检查和所有边界详见[交付说明](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-17-west-coast-claims/delivery.md>)。

## 检查与复测

九份脚本解析、中英键与动态函数、写作扫描、17 个脚本正反例通过。Toolkit 的 CK3 单数 on_action 目录诊断为误报。全局 71 处其他 any 比较风险仅记录。
未启动游戏。以新开局验收。重点检查共同分州合并后的 target_state、原生交地回调顺序、战中兑现至和平结算。快造分州的控制台步骤在交付说明中。

## Result

用户批准恢复部署后运行 deploy.bat force，1492 文件 SHA-256 一致，随后 check 三处版本一致。先前中断产物 1481 文件匹配源目录，8 个差异均匹配改前备份。旧日志未查到本条目报错，其余键缺失等见交付说明。


## 2026-11-17 文案复核
四轮审读全部55对文本，修改36对。修正套式、臆造态度、条件反义、和平结束情形、国名及术语动态引用和英文对应。最终套式、函数引用及Toolkit检查通过。已随部署752609ec65fbedbd0145378c185c459c写入MOD文件夹，两份文案SHA-256与源目录一致。[审读记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-17-west-coast-writing/review.md>)。本轮文案可读档查看，机制仍待新开局实机验收。