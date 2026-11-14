# 90 科举投票制

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: completed
Assignee: Codex
Blocked by: none
Validation: STATIC_PASS
Evidence: [静态核对与候选 SHA](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-keju-voting/static-checks.json>) · [Tiger 与改前完整备份对比](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-keju-voting/final/tiger-delta.json>) · [单条覆盖对照](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-keju-voting/step3>)

## 现象与期望

按[定稿第 3–7 节](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-keju-voting/科举投票制设计方案.md>)实施财产投票的儒家文化圈变体，由作者新开局复测。

## 原因

科举借用财产投票的立场。颁布条件、指定法类型、修正案适用清单和女性选举权解锁须逐处补入科举。生效时保存科举法律对象，供继承的修正案挂载。

## 改了什么

- 科举投票制使用专属考卷、毛笔与印记图标。DDS 格式与原版投票法一致，302×302，含透明通道和 9 级纹理。
- 新法采用全部 16 项修正。财产投票按文化与实业家强弱切换显隐，两法都在实行期间保持可见。
- 儒家、士大夫家长制及儒林两派按定稿取立场。四国替换开局投票法，添加三个国家的指定修正案与赞助者。
- 权力分配与煽动者事件、流散分配率、小国法治、日本废幕及岩仓使节团已接入。五条单项覆盖登记在技能及仓库副本。
- 科举已加入 1.15.1 的民族之春变量清理。核对生效回调及文件字节差异，清理条件只增加一行。
- 中英各 11 键，定稿说明逐条对照，中文全角分号为零。全部路径及方案第 6 节逐行结论见[改动文件与兼容核对](<D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/reports/2026-11-11-keju-voting/改动文件与兼容核对.md>)。

## 怎么复测

1. 查看四国权力分配。大明联邦挂文人赞助的“扩大通过率”，远南无指定修正案，登莱挂知识分子赞助的“自由选举传统”，东洲另有士大夫赞助的“礼部的最高决定权”。
2. 东洲新开局的地主应持“缙绅主义者”，面板应无“士绅主义者”。已删除 HUS 国家历史手加的士绅主义者，原版非君主制全局历史授予缙绅主义者，其对科举为中立。远南和湖南的地主则保留“士绅主义者”，在原版统一授予后移除“缙绅主义者”。士绅主义者应强烈赞成君主制，赞成总统共和制、社会君主制、法团国家。儒林两派仍应强烈赞成科举、赞成资格选举。登记全局历史的实际顺序，可对照大明联邦的儒林立宪派与登莱的儒林共和派。
3. 在实业家未举足轻重的日本查看科举，再到非儒家文化圈国家对照。实业家成为举足轻重时应显示财产投票，现行科举仍可见。改回其他法律后再观察显隐。
4. 从投票力明细核官僚 −15，从政治运动明细核法律的激进度 −0.05。查看东洲、登莱的原版修正案是否附着科举，再换投票法检验继承。

## 遗留问题

- 游戏未启动。官僚负票力、运动激进度、修正案单条覆盖、全局历史执行顺序、实业家变化后的显隐五项待实机确认。
- Tiger 新增错误 0。原版“自由选举传统”改由单条覆盖加载后报告 7 条警告，原版正文的隔离对照可完整复现。
- 原版立宪派与 MOD 立宪派的专属法律组差异、开局后新共和国，以及保留的父法显示和事件均见文件清单末段。
