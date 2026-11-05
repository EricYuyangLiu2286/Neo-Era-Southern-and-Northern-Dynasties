# 1.15.0 首局脚本错误复核

六份 error*.log 的封存副本在 script-review-first-snapshot，原始 SHA 在 script-fixes-verification.json。日志最后写入 2026-11-05 17:06:43，归因仅及这六份轮换保留窗口。版本 1.15.0 / Steam build 26453692，catalog CURRENT。此委派沿用既有审查代理，配置的模型 ID、推理强度未公开。

3,202 条 Jomini Script system error 中，3,189 条属于本次已修MOD 代码。下列六个主 MOD 文件的修改前预像在 script-fixes-baseline，最终 SHA 在验证 JSON。实际出处、引擎文档及原版调用链在 script-fixes-sources.md。

| 记录数 | 原因与修改 |
|---:|---|
| 1,553 | HUS 人口阶级在引擎初始化时比较 `this = cu:manchu`，右侧全局文化对象报错。以原版江户 `has_pop_culture` 的数据库键确认满洲 Pop，蒙古、汉及原住民/欧洲归属仍按原 heritage 和组。12 个阶级、总 hierarchy 与唯一的满洲迁徙调用共用同样的 Pop 谓词。全局 Manchu 的汉 heritage 和人物/文化 scope 调用均保留。 |
| 1,323 | 西秦士兵比例采用 `target = pop_type:soldiers value > 0.03`，保持超过 3% 的负担和原值。 |
| 313 | 小国土地议题采用 `target = pop_type:peasants value > 0.25`，保持超过四分之一的原资格。两项职业查询与 1.15 当次导出的 triggers.log 和本体 urbanization JE 一致。 |

从主 MOD 目录运行 `python ../../nesnd-workbench/reports/runtime-115-first/verify_script_fixes.py`。同一测试器对六个修前文件捕获三处原错，对现文件解析成功。通过实际调用节点核有效库中的 335 种文化、15 项职业及迁徙过滤，共 5,025 项文化/职业组合。核对全体满洲/蒙古组4、汉组13、美洲原住民35、欧洲99、其余184。验证只覆盖外部有序语法及判定子集，引擎初始化与实局日志次数等候以后运行观察。

余下13条脚本错误分别来自俄语考纳斯5个动态地名、秘玻已有参与者2次、原版法国政治 AI 谓词被州事件调用2次、原版政治游说2次、观察者无持有人时执行匈牙利转国1次、卡洛斯战争开局1次。法国两段在MOD有效同路径文件和1.15本体中一致，调用文件为本体 state_event。卡洛斯原版历史假设 PHI 仍是西班牙属国，而 MOD 开局已撤除该宗属，已交主任务处理历史文件。动态地名已交本地化。19 条单独的重复 JE 提示按既有作者保留重复入口决定归档。孤儿/未读变量的全局警告未直接作为新玩法故障（含明确停用的兼容壳）。对没有脚本位置的一条线程访问断言，现有记录不足以归因到脚本。其余 UI、旧存档元数据、图形及地图错误由对应分工处理。

本代理未启动游戏，未写 Git。原始日志记录的是修改前运行。