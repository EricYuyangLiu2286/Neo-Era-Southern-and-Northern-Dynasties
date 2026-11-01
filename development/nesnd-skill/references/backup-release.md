# 备份与回溯

WORK/backups 保存完整 MOD 副本和逐文件 SHA-256 manifest；不以 MOD 内 .bak 作为唯一恢复，不覆盖旧备份。

实质修改前保存 pre-change；可交付但未跑完验收保存 candidate；每次真实验收成功的输出保存 accepted，附游戏/依赖版本、加载组合、MOD 指纹、分支矩阵、原日志与必要测试存档。中断保存 checkpoint，标明失败/缺证。上一个版本备份不能代替本次成功版本备份。

`python -X utf8 <skill>/scripts/backup.py --label <短标识> --status pre-change|candidate|checkpoint|accepted [--evidence <证据JSON>]`。accepted 必须有 engine_verified=true、当前 mod_sha256 及实际运行记录路径，不能手填虚假证明。

独立候选用 `--source WORK/exports/<候选>`，省略时仍备份主 MOD。工具只接受主 MOD 或 exports 内具有 `descriptor.mod` / `.metadata/metadata.json` 的实际 MOD 根目录，复制后逐文件核对哈希。20261031 的南明年度 checkpoint 已用此入口实际保存；局部经济实测通过、全 MOD 尚有缺证时仍标 checkpoint，并在 evidence 列明通过范围。

恢复前比较当前目录与目标 manifest，备份当前状态，再复制目标到新运行目录复现；不直接覆盖用户后续编辑。版本比较同时看原版基线、依赖与运行条件。

临时加载配置逐次备份，仅在退出时配置仍等于本次临时值时还原，防止覆盖用户修改。异常退出下次首先检查。不同时启动多个游戏争用日志/存档；测试另存独立名字。
