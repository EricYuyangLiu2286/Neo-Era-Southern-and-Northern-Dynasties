# 62 成都焚掠加载画面

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: ENGINE_PASS（作者测试完毕，2026-11-10）
Evidence: [第四版纹理回读](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-chengdu-loadingscreen/revision-4/verification.json>)

## 现象与期望
按所附成都画稿、军服与成都城图修正透视、动作、衣饰和城池，并导出 4K 加载画面。

## 原因
原稿村前人物、马车和远处炮兵阵地各自使用了不同的尺度参照。

## 改了什么
新增 `gfx/loadingscreens/nesnd_chengdu_after_the_breach.dds`。以村门校准搬运者和押解人员，以田路行人校准炮组，保留山顶六人、临河厂房和城墙缺口。工作台保留实际 1672 × 941 的修订源图及 Lanczos 重采样的 3840 × 2160 母版。DDS 使用 DXT3，已逐层验证 12 级 mipmap 及全部压缩块的完全不透明 alpha。

第二版依军服素材重绘山顶六人，校正进城桥、门洞与主街的透视，将临河厂区改作川西瓦顶木构长坊；以门槛上的站立成人校准村屋，补回炮床及城墙外的两层驻军与营房，恢复城墙破口。重绘使用的[完整提示词](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-chengdu-loadingscreen/revision-2/redraw-prompt.txt>)和修订源图一同归档。已替换主 MOD 同名 DDS。

第三版统一两名副将的深靛服色、短翅官帽、武职方补与佩刀，参谋采用灰青素服和文书匣。左侧田间小营与门楼炮损按底稿比例合回。源图与本次来图逐像素比对，局部编辑区以外差异为零。第三版已替换游戏 DDS。

## 怎么复测
第四版按作者提供的勇字盔照片修改最左持枪卫兵；在副将身后及河弯桥左后方补画两层成队步兵和营帐，并加入营道车辙、受损田地。已替换游戏 DDS，回读各级 alpha 均为完全不透明。

启用 MOD 后重启，在随机加载画面中观察。可使用现有存档。

## 遗留问题
实机加载和屏幕裁切待作者复测。炮轮与人高的精确比例在远景中仅能估读。
