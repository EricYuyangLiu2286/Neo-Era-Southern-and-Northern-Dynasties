# Issue tracker: Local Markdown

本项目的任务与规格使用 `.scratch/` 下的 Markdown 文件。

## 文件约定

- 每项功能一个目录：`.scratch/<feature-slug>/`。
- 规格：`.scratch/<feature-slug>/spec.md`。
- 实施任务：`.scratch/<feature-slug>/issues/<NN>-<slug>.md`，
  从 `01` 编号，每个任务单独一个文件。
- 普通任务的分诊状态写在文件顶部附近的 `Status:` 行，
  名称见 `triage-labels.md`。
- 讨论记录追加到文件末尾的 `## Comments` 下。

## 技能操作

技能要求“发布到任务跟踪器”时，按上述约定创建文件。
技能要求“获取相关任务”时，读取用户指定的文件；
仅给出编号时，先在对应功能目录定位。

## Wayfinding

`wayfinder` 使用以下布局和执行状态：

- 总图：`.scratch/<effort>/map.md`，
  包含 Notes、Decisions-so-far、Fog。
- 子任务：`.scratch/<effort>/issues/NN-<slug>.md`，
  正文写待解决的问题。
- `Type:` 为 `research`、`prototype`、`grilling` 或 `task`。
- `Blocked by: NN, NN` 记录依赖；
  所列任务全部为 `resolved` 后解除阻塞。
- 从未完成、未领取且无阻塞的任务中，按编号选择最前一项。
- 开始工作前写入 `Status: claimed`。
- 完成后在 `## Answer` 下追加答案，写入 `Status: resolved`，
  并向总图的 Decisions-so-far 追加结论摘要与任务链接。
