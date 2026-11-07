# 64 《接旗》主菜单正式美术

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [安装文件解码记录](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-07-dongting-persia/verification.json>)

## 现象与期望
执行任务63复核后的构图清单，制作洞庭湖战场、独立人物肖像与「南 · 北」角标，替换宫殿占位视频。

## 依据
《朱班博传（上）》的保旗、接旗事件构成底板。封面为1836年开局人物，左起牧仲棠、陈东阳、李霄业、拿破仑三世。作者确认李霄业既是西秦波斯将军府留后，也是唐衣大食贵族承认的波斯沙阿。面貌及服饰细节属美术演绎。

## 改了什么
替换主菜单视频第三席，更新 PER_li_xiaoye 的一行注释。洞庭底板与角标哈希相同，实装视频为 3840 × 2160、15 fps、6.4 秒循环。工作台 reports/2026-11-07-dongting-persia/ 保存分层源稿、合成稿、解码预览、修订依据和上版备份。

## 怎么复测
重启并启用主 MOD，主菜单 Theme → 主菜单背景 → 南 · 北（NESND）。检查四张脸、双翅乌纱帽、接旗动作、湖烟循环和角标。切到俄国主题再切回，关闭选择器后重启确认记忆。无需读档。

## 遗留问题
同版游戏解码器已从安装路径读完96帧，抽查画面及循环接缝。按1920×1080布局折算的安全区已核对；真实 GUI、极宽屏与重启记忆待作者实测。
