# C1 repair4 implementation / READY_FOR_TEST

2026-11-04；实际显式配置 gpt-6.1-sol / medium。委派从只读审查转为GO授权实现，证据：/root对/root/sol_c1_review的followup NEW_TASK。候选 D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\exports\canon-route-execution-20261104-a；主MOD与GAME只读。

完整编辑已结束；冻结：D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\nesnd-workbench\backups\batch-c-owned-repair4-freeze-20261104T145402Z\mod。清单：batch-c-repair4-freeze.json；31份owned，12份与repair3实际不同。SHA生成/复制属于交付冻结；没有调用AST行为矩阵、Tiger、MCP或游戏。状态仅READY_FOR_TEST / ENGINE_NOT_RUN，不宣称STATIC_PASS。

实现：三层资格、独立即时结算、旧pending兼容迁移、终局final_patron、惰性旧事件、六按钮同级exists/独立条件、共享kind2/5独立投资国、现有月度请求资格清理、双政体快照、双语去掉等待期限。具体契约见batch-c-repair4-source-contract.md，逐项中英文旧稿/最终对读见batch-c-repair4-writing-comparison.md。

两项审查风险均已在源码落实：已成立保护国不走新建资格；先保留旧分支和投资对象再清legacy变量，且JE抢先invalid也走旧事实确认。finish后的通知依赖final_patron，不读取已删的当前investor。

旧证据及全owned修改前快照保存在batch-c-before-repair4；repair3验证目录未改。旧90日PASS只证明被否决设计，不复用为repair4通过。历史条约/宗属/type/action源hash保留。

数值未改：100独立性、有效赞助−1/月、原外资公式、30年、成功120月、失败60月及既有−15合法性modifier；原45日回复、6月冷却不变。移除的90日与2日等待是用户已批准设计纠正。

后续仅针对本冻结做测试；任何测试要求修改时应建立新修复轮次及新freeze。必测场景沿repair4计划第7节，外加JE invalid先于weekly的旧pending保护国迁移、finish清当前投资人后的保护通知、零点与30年同日互斥。

本轮技能维护复核：无新版本/接口事实；未修改永久技能。

修改文件：

- common/journal_entries/nesnd_egypt_independence.txt
- common/on_actions/nesnd_canon_diplomacy.txt
- common/script_values/nesnd_egypt_independence.txt
- common/scripted_buttons/nesnd_egypt_independence.txt
- common/scripted_effects/nesnd_canon_diplomacy.txt
- common/scripted_effects/nesnd_egypt_independence.txt
- common/scripted_triggers/nesnd_canon_diplomacy.txt
- common/scripted_triggers/nesnd_egypt_independence.txt
- events/nesnd_canon_diplomacy.txt
- events/nesnd_egypt_independence.txt
- localization/english/replace/zzzzzzzzzzzz_nesnd_batch_c_l_english.yml
- localization/simp_chinese/replace/zzzzzzzzzzzz_nesnd_batch_c_l_simp_chinese.yml
