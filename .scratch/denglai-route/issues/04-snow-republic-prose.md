# 04 雪国共和的处境与人物引语

Record: implementation  
Category: enhancement  
Status: ready-for-human  
Execution: completed  
Blocked by: none  
Validation: STATIC_PASS（1.15.0 / 26453692）  
Evidence: [本批文件指纹、文本与入口检查](<../../../../../nesnd-workbench/reports/denglai-route/batch2/verification.json>)

## 1. 现象与期望

作者截图已显示「雪国共和」及已选通商的状态。作者指出背景文字落在了旧账上，开局选择过于机械，事件缺少人物言语。截图验证了上批日志显示，三次选举保护仍待单独实测。

## 2. 原因

上一稿的日志由百年前的三角贸易跳到道德议论，未写出新来的流亡者如何度过眼下的冬天。首批九个事件各有正文，均缺少原作事件中的 flavor 字段。

## 3. 改了什么

- `localization/{simp_chinese,english}/replace/nesnd_sha_republic_l_<语言>.yml` 改写根日志和事件，加入九段人物引语。「雪中的抉择」用虚构议员梁秉舟父子对故乡的不同理解写还乡之念。1836 年距首批流亡者抵达约 123 年，两句涉及齐国旧事的中英文引语均已据此校正。两种选择都在提示中以红字标明雪国无力兼顾另一条路。
- `events/nesnd_sha_republic.txt` 逐事件绑定 `flavor = … .f`。两个开局选项分别开启对应的第二批日志。
- `common/journal_entries/nesnd_sha_republic.txt` 用准确的华夏组建文字显示成功、失败条件，北方阶段结束后显示南向寻港的状态。

## 4. 怎么复测

登莱新开局，读日志下半段和次日开场事件。若分别悬停两个选项，应读到整军或通商的计划，红字警示相同。再看年度事件的引语是否完整。英文局对应同一说话者和选择。

## 5. 遗留问题

新文字、着色和引语排版尚待游戏内查看。
