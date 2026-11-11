本次任务：按已确认的设计，实现登莱共和国（TAG `SHA`）的原生发展路线。设计、数值、作者的全部决定都已写成文件，**不要重新设计**。
类型：新内容（脚本 + 中英文本地化）
游戏：Victoria 3 1.15.0。本次不启动游戏，由我自己实机测试。

## 先读（按顺序）

主 MOD：`D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties`

1. `AGENTS.md`，以及它指向的技能 `nesnd-victoria3`（必读 `references/content-design.md`、`syntax-and-routing.md`、`journal-text-contract.md`、`numeric-scale-contract.md`、`verification.md`）。写玩家文字前读技能 `nesnd-player-writing`。
2. `.scratch/denglai-route/map.md`：我的全部决定和设定（Decisions-so-far 一节）。**与其他文件冲突时以它为准。**
3. `.scratch/denglai-route/spec-v3.md`：内容树。9 个日志、2 个决议、2 家特许公司、东燕新 TAG。
4. `.scratch/denglai-route/numbers-v1.md`：数值。全部是源码估算。
5. `.scratch/denglai-route/spec-fable.md` 第 1 节：现有机制调查和周边四方的边界节点（附出处）。
6. `.scratch/denglai-route/issues/01-far-north-pops.md`：已经做完的远北人口与祖地改动，不要重做。

`spec.md`、`spec-v2.md`、`questions.md` 是旧稿，不用读。

## 硬规则

- 只有主 MOD、技能目录、工作台 `nesnd-workbench` 可写。游戏本体、创意工坊、素材目录只读。
- 动手前用技能的 `scripts/backup.py --status pre-change --label <名字>` 备份。
- 不改其他国家已有的日志、事件、变量。允许动到别国的地方只有 `spec-v3.md` 第 6 节列出的那些，超出的先列出来问我。
- 名称、文化、国名一律以 **MOD 的本地化**为准，不要按原版理解。例：`han` 在本 MOD 是“华北”，`manchu` 是女真人，KRA 显示为克拉科夫。
- 设定不要编。`map.md` 里 C1–C3 是建国脉络；我明确允许你拟的只有：最初的逃亡者、东燕君主（徐氏远支）、公司与事件的具体名称。
- 新内容前缀 `nesnd_sha_`。逻辑写在用它的日志、按钮、事件里；两处以上复用才提取 scripted trigger/effect。
- 所有日志排除原版军阀事件生成的 SHA（`has_variable = warlord_state`），并设 `can_revolution_inherit = no`、`transferable = no`。

## 我对做法的要求（这几条之前反复纠正过）

- **写之前先读现成的写法**：进度条分批迁徙读 `nesnd_diaspora`（日志、effects、progress bars）；镇压起义的战争读 `nesnd_cne_republic`；锁法律读 `common/laws/nesnd_hus_citizenship_lock_overrides.txt`；殖民网络读原版 `00_scramble_for_africa.txt`；分离运动读原版 `02_cultural_movement.txt` 和 `52_nationalism_actions.txt`；公司读原版俄美公司和 `ce_companies_china.txt`。
- **一次性的选择用决议**（迁都两个决议）；**向别国提的请求用自定义外交行动**，不要一律按钮加事件。
- **登莱很弱**：凡是要动武的环节，先煽动，看到对方处于原生的乱局才解锁下一步。不能让 AI 送死。
- **失败要留余地**：请求被拒只进冷却；日志超时也推进；后面的门槛读真实领土。不做无限分支。
- 我已经定过的事不要再问。真被卡住时，问题要具体，带选项和你的默认。

## 工作顺序

分批做，每批都能独立进游戏测试。**每批交付后停下等我实测**，除非我说连着做。

1. 根日志「雪国共和」：开局事件选路线、身份修正、政体锁、每年随机事件、最后一段的华夏要求；两个迁都决议。
2. 「远北的阴谋」「黄金与同盟」；北海公司。
3. 东燕 TAG（国家定义、旗帜、本地化、君主）；「复燕」，含北朝的战争目标、「东燕之乱」修正、北朝打赢后恢复整编的 on_action。
4. 「渡海」「齐鲁之约」。
5. 「海外落脚点」「垦殖」；登莱远洋公司。
6. 「君主主义阴谋」。

开始第 1 批之前，先用一条消息告诉我：你读完后发现的设计与引擎冲突之处（给最小改法，不推翻树），以及第 1 批要新建和修改的文件清单。然后直接开工，不用等我回复，除非有冲突需要我定。

## 每批的交付

- 脚本，以及 `localization/simp_chinese/replace/` 和 `localization/english/replace/` 两种语言、相同的键。
- 游戏外检查：技能的 `scripts/pdx.py` 解析、`scripts/audit.py`；内容树工具（`D:\Users\Eric Liu\OneDrive\Documents\Modings\V3-content-tree`，先 `python run.py index`，再对新节点跑 `near`）核对入口、结局、变量有写有读。
- 任务记录 `.scratch/denglai-route/issues/NN-*.md`（格式见 `docs/agents/issue-tracker.md`，一页以内），并按规则更新 `docs/agents/STATUS.md`。
- 交付说明写四件事：改了哪些文件；跑了哪些检查；哪些行为没有实机验证；遗留问题。另附“怎么复测”：新开局用登莱，要看什么、预期是什么。

## 已知要实机才能确定的事

列在 `spec-v3.md` 第 7 节和 `numbers-v1.md` 第 9 节。遇到时按最简单的写法实现，在交付说明里标出，不要为每种可能各搭一层保护。静态检查通过不等于游戏内验证，分开写。
