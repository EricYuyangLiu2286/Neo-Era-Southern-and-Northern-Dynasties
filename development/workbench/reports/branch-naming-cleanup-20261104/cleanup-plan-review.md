# 清理规划修订：按用户最新明确删除授权

**本版取代先前“保留旧候选/失败现场/快照”的建议。** 用户现已明确只保留少量关键版本，并允许删除旧候选、失败现场、snapshots和旧运行保存。子代理仅规划；最终清单与执行由主代理决定。实际配置：`gpt-6-astra / high`。

## 确定保留

- 唯一主MOD与 `projects/nesnd-repository` 的main；私有远端历史；`original-20261030`标签。
- 约3个本地源码备份：现有 `backups/pre-update-20261030T233944Z`（119.99 MiB）；主代理新建的pre-cleanup主MOD备份；命名规范化/部署完成后新建的current-final备份。后两项精确路径由主代理冻结，不用模糊latest规则。
- `baselines/vanilla-1.13.11-24799966`（150.17 MiB）。人口检查器在 `tools/population_envelope_audit.py:24–25` 直接依赖该基线与上述原版备份精确路径，因此保留它们不额外增加第四个源码备份。
- 维护中的tools/editor、未完成设计文本/项目JSON、轻量交接和报告结论；不把大型原始decoded save/旧源树混入“轻量报告”。
- 若主代理选择保留关键引擎样本，仅留1866.1.15观察者终档一份（203.52 MiB），移至 `evidence/key-engine-terminal/` 后核SHA；不为它保留整套profile。终档已存在的备份不可再重复留两份。

## 精确允许清理的范围

| 相对WORK目标 | 现有体量 | 操作 |
|---|---:|---|
| `exports` | 26.373 GiB | delete_each_existing_child_keep_parent |
| `backups` | 36.539 GiB | delete_children_except_three_explicit_keep_roots |
| `runtime/profiles` | 36.416 GiB | delete_inactive_old_profile_children |
| `validation/snapshots` | 3.368 GiB | delete_all_old_child_trees_keep_parent |
| `validation/runs` | 0.823 GiB | delete_old_large_outputs_after_compact_report_selection |
| `projects` | 2.088 GiB | delete_explicit_transient_directories_only |

`exports`可清全部旧子目录和旧发行ZIP，但若主代理已新建本次重命名候选，应先排除它直到部署完成。`backups`只按3项绝对白名单保留，其余旧备份可删，不再要求逐个找相同副本。`runtime/profiles`先重新查询游戏和编辑器进程；只保护确有运行占用的profile，其余旧存档、日志、shadercache均在本次授权删除范围内。用户正常USERDATA存档目录不属于目标。

projects待删目录逐项：

- `projects/editor-export-staging-052e897b4ec74323b674ad1182fdd904`
- `projects/editor-export-staging-12d58345b26449be88730081b0bd3348`
- `projects/editor-export-staging-5b92545de83042af9c733ca7e83f670b`
- `projects/editor-export-staging-cf7e6f5c1f82401a8477dd239fa022b0`
- `projects/editor-fixtures-20261031T144950Z`
- `projects/editor-fixtures-20261031T152435Z`
- `projects/editor-fixtures-20261031T152701Z`
- `projects/editor-load-185a1daa6af846e998aa7e7c2b513fb2`
- `projects/editor-load-1da2c53eacf74883b713a5ecb6488084`
- `projects/editor-load-1f3a70562dc042b1ba61b4e983fe3da9`
- `projects/editor-load-2d11d8475d824a2ba167359a42b757dc`
- `projects/editor-load-328b17f4e13143c089c2a66c8e39058d`
- `projects/editor-load-43fdebaed4ef4a07b0b2cbbccaabe3f2`
- `projects/editor-load-7b5de0b32d854d58a4a8935faac1040c`
- `projects/editor-load-80daa0c6de3b448e95500516246647cb`
- `projects/editor-load-c4d0e627ef79480ab2d462475f84a2e7`
- `projects/phi-expiry-probe-static-20261031`
- `projects/phi-permission-static-20261031-b`

validation保留父目录及简要结论/工具入口；旧snapshots与runs中的大型原始输出不再作为必须存留的复现证据。新清理过程生成的报告/快照不误归入旧目录删除。

## Git分支引用

本地分支只保留main；原始版通过现有 `original-20261030` 标签与远端保存。可先记录每个旧ref的SHA、核实时远端、生成并验证bundle，再删除18个旧本地branch引用。未合入candidate/unselected仍保存在远端和bundle，删除本地活动引用不等于删除提交内容。其`-d`可能因非祖先拒绝；在上述保障和最新授权下可由主代理明确使用`-D`，不应错误合并历史分支来绕过判断。

潜在风险仅在：忘记保存只有本地存在的ref/未提交变化、bundle没有验证、删除正在checkout的worktree分支、后续误删远端或原始标签。此次观察repo干净、stash为空、仅一个main worktree；执行前重查。Git保存的是已提交历史，不宣称每个即将丢弃的非Git失败目录都已上传。

## 编辑器旧引用退役

编辑器 `app.py:12` 默认从主MOD打开，无需保留旧exports才可继续使用。旧project JSON保留设计动作与原source_manifest，另写一份短退役说明：这些旧source路径已按作者清理要求删除，旧工程不是当前可直接恢复的工程；新工作从主MOD打开后重新应用经过审查的动作。不要把旧JSON的source直接改成主MOD、伪造manifest一致或把旧文件盲目覆盖当前MOD。

建议退役说明仅记录：清理日期、旧路径范围、历史Git ref/SHA映射、当前M/repo位置、3份备份清单，以及旧报告路径失效是主动清理结果。原报告仍描述当时证据，不全局替换成当前路径。

## 执行安全边界

每个删除目标先解析为绝对路径并证明位于本表明确WORK子树；查目标、父链和内层reparse point，发现链接跳出范围则单独处理而不跟随。先冻结3份备份白名单和本次运行排除项，再原生PowerShell LiteralPath执行。不得以字符串前缀代替路径包含关系，不跨shell传递删除列表；主MOD、repo、原始资料、本体与工坊绝不在删除清单中。

全部体量来自本次初始盘点，逻辑字节不等于保证释放的磁盘空间。子代理没有删除、移动或归档任何旧内容；仅更新本报告与JSON。
