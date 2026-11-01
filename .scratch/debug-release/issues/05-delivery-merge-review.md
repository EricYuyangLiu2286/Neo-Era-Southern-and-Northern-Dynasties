# 准备交付与主 MOD 合并清单

Record: implementation
Category: enhancement
Status: ready-for-human
Execution: open
Assignee: none
Blocked by: 02, 04
Validation: NOT_RUN
Evidence: pending
Approval: pending

## Scope

完成用户批准的第4阶段：整理精确候选、验证范围、未覆盖项、文件差异和独立备份，提交主 MOD 合并清单；取得用户对具体清单的批准后才合入。

## Acceptance

- 对比当前主 MOD 和冻结候选，保留 AGENTS、docs/agents、任务索引及用户后续编辑。
- 所有旧版与新候选的来源、提交/标签或 manifest 可追溯；第三方依赖和原版基线保持只读。
- 已验机制有精确证据，新修复未测部分明确列出；未通过完整门槛不标 accepted。
- GitHub 已核远端保存结果；主 MOD 合入审批与源码保存分别记录。
- 合入前、候选、真实成功后的独立备份按 [备份规范](<C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/references/backup-release.md>)执行。

## Result

尚未提交本轮可合并清单。

## Comments

用户当前授权推进至可审查交付；此任务的 Approval: pending 仅约束最终主 MOD 合入，不重复阻断已授权开发与验证。
