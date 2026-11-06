# 任务47附表：作者改稿后又被代理改动的 34 个键

来源：作者改稿取自 `development/workbench/reports/canon-prose-20261102/author-revision-original.txt`（11-02 作者改稿）和提交 `be56496`（作者本机改稿）。“当时理由”取自 `canon-prose-20261102/*-proposals.json` 等审查记录。“改动提交”是作者文本被替换的那次提交。

**2026-11-06 作者同意全部建议，已按建议处理。** 第三组冲突句的具体改动见任务47 `## Result（34 键）`。

## 一、按钮已改成别的玩法，作者旧文描述的是旧玩法（8 键）

地权革命的四个按钮后来改了效果。作者旧文写的是清丈、清理军籍田产、可恢复的暂停；现在按钮分别是官营工坊拨款、转业救济、地权争讼复核、提请元老院永久收束改革。恢复旧文会让按钮说的和做的不一致。

**建议：保留现稿。若想恢复旧玩法本身，那是玩法改动，需另开任务。**

### `nesnd_land_survey`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：保留：已逐项核对叙事主语、制度、两种语言及触发/效果；无需为统一句式改写。
- 作者稿：
  > 重勘田界
- 现稿：
  > 拨款官营工坊

### `nesnd_land_survey_desc`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Actual cost comes from treasury, not an implemented stream of profits from land confiscation.
- 作者稿：
  > 地权革命必须越过宗祠与军营的围墙。各省另派清丈官，将庄田的四至、佃户的契约与历年的赋额一并查明，使被吞并的产业重新进入国家的簿籍。
- 现稿：
  > 由户部拨助工坊与实业学堂，使离开田庄的乡民学会新业，参与产业的增长。

### `nesnd_land_military`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：保留：已逐项核对叙事主语、制度、两种语言及触发/效果；无需为统一句式改写。
- 作者稿：
  > 清理军籍田产
- 现稿：
  > 增拨转业救济

### `nesnd_land_military_desc`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Concrete fiscal actor, existing institutions and affected population.
- 作者稿：
  > 开国将士曾随牧仲棠打破旧日的宗族与藩镇，如今他们的军籍又庇护着新的庄园。朝廷须将军功、俸饷与土地所有权分别核定。
- 现稿：
  > 由户部向已有救济机关增拨款项，接济离开田庄、尚未找到生业的农户，使失去收入的人仍能维持日用。

### `nesnd_land_review`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：保留：已逐项核对叙事主语、制度、两种语言及触发/效果；无需为统一句式改写。
- 作者稿：
  > 复核申诉
- 现稿：
  > 复核地权争讼

### `nesnd_land_review_desc`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Use competent ministries and provincial heads; retain the original promise of secure land rights.
- 作者稿：
  > 改革所要解放的农民，应当能够向新政府申明自己的权利。受理地方申诉，复核争议田契，并追究借清丈夺产的官吏。
- 现稿：
  > 由刑部会同户部复核地权争讼，责令省督查明地方官员执行新法的情形。已经取得田产的农户，应当能够依法保有他们的生活。

### `nesnd_land_suspend`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Button opens an irrevocable ending proposal; a resumable pause belongs only to the three individual programmes.
- 作者稿：
  > 暂停清丈
- 现稿：
  > 议止地权革命

### `nesnd_land_suspend_desc`
- 文件：`localization/simp_chinese/replace/nesnd_cne_land_reform_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Name the competent legislative body and preserve the fact that clicking opens a decision.
- 作者稿：
  > 命各省停办未结案件，承认已经完成的登记，将余下争议留待中央与地方重新议处。
- 现稿：
  > 将各省停办改革之请交元老院议定，呈请颁诏收束清丈与改制。

## 二、目前玩家看不到或只作兜底的键（4 键）

`nesnd_crisis.11` 现为隐藏事件，11.a/11.d 不显示；`nesnd_federal_compact_button` 只是兼容键，实际按钮是 `nesnd_south_offer_accord`；`nesnd_crisis.30.d` 只在缺少地方 scope 时兜底，正常显示的是 `nesnd_crisis.30.local`（也是代理据作者稿写的地方版）。

**建议：恢复作者原文，不影响玩法。**

### `nesnd_crisis.11.a`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：统一本轮设定与名称，保持原有数值和功能。
- 作者稿：
  > 公布案情，因循查办。
- 现稿：
  > 公布案情，循线查办。

### `nesnd_crisis.11.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：保留作者刑部/大理寺/锦衣卫办案争议，修复碎句；当前不可见。
- 作者稿：
  > 首辅护卫在核验随行人员时，查获了一封伪造的换防手令。携带密信的人员及其同伙很快被锦衣卫和大理寺抓捕，按照身份和参与事情分别收押。首辅本人被当即送往安全地点，在案犯落网后才得以返回住处。 ／ 对案犯的调查一发不可收拾。触及承办军需、海运的一些关键岗位的官员。而这些嫌疑人又同各省名绅大户乃至圈禁的旧藩邦君往来密切。这些人似乎掌握着刑部、大理寺在首辅要求下秘密核查的一些走私案的关键信息。然而，大理寺和锦衣卫对于下一步的行动产生了分歧。由大理寺审办，对刑事官员们公开案情，被内阁认为是可以从明面上开始大规模的内部调查，方便行事。锦衣卫方面则坚持应该封锁消息、秘密调查，不能打草惊蛇，以麻痹逆贼、防止事态扩大。
- 现稿：
  > 首辅护卫查获了一封伪造的换防手令。携信者与同伙很快被锦衣卫、大理寺捕获，分别收押。陈东阳先被送往安全之地，待案犯落网才返回住处。 ／ 调查随后牵出经办军需、海运的官员，以及同他们往来的各省名绅与旧封君。大理寺主张公开案情，借此追究藏在官场中的关系。锦衣卫则坚持封锁消息，以免惊动尚未落网的人。内阁须决定如何继续查办，也须承担事情扩大后的政治后果。

### `nesnd_federal_compact_button`
- 文件：`localization/simp_chinese/replace/nesnd_south_politics_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：作者旧按钮名保留为兼容键；真实按钮引用south_offer。
- 作者稿：
  > 重订邦国契约
- 现稿：
  > 重订国家礼法

### `nesnd_crisis.30.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：Guarded fallback for an already queued event without the newly saved locality scope. The normal branch is nesnd_crisis.30.local.
- 作者稿：
  > 在某一些地区，[ROOT.GetCountry.GetName]的清丈官带着新法下乡勘定后，军功庄园却仍在按旧例征租。已经缴清赎价的农户被他们的“老爷”告知所耕之田属于军籍，不许抵触租税。一些替农民代写申诉的塾师也因包庇隐产而遭拘押。 ／ 各县呈来的契约与军营的册籍彼此抵牾。县府、省府要求接手复核，清丈官则请朝廷派兵收缴隐匿的文书。迁延日久，原本期待分田的农民聚集到他们的县城，等待这个许诺解放他们的新政府作出答复。
- 现稿：
  > 地方呈来一桩清丈争讼：清丈官带着新法下乡勘定后，当地几处军功庄园却仍在按旧例征租。已经缴清赎价的农户被他们的“老爷”告知，所耕之田属于军籍，不许抵触租税。一些替农民代写申诉的塾师也因包庇隐产而遭拘押。 ／ 涉事各县呈来的契约与军营的册籍彼此抵牾。省督要求接手复核，清丈官则请朝廷派兵收缴隐匿的文书。迁延日久，原本期待分田的农民聚集到县城，等待这个许诺解放他们的新政府作出答复。

## 三、作者正文被代理“精修”，并按设定改了部分事实（13 键）

这组是作者的叙事正文和按钮说明，代理保留了大意，但改写了句子，并按设定或脚本改了若干事实（理由见每键“当时理由”）。这些正是去平衡腔要改回作者声音的对象。

**建议：恢复作者原文，只改与现行脚本或设定冲突的那几句（逐键列在“当时理由”里）；冲突句由我改写后给你过目。**

### `ce_cne_land_reform_reason`
- 文件：`localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：Keep the mature Chinese original byte-for-byte; replace Chinese fallback in the effective English layer with a faithful translation, without the older English’s invented extra theory.
- 作者稿：
  > 这一运动发源自1810年的西秦大革命。被本时代人视为农业发达而宗族根深蒂固的东方诸国内萌发的一种近代经济上的变革运动。其特点大致可以是用赎买或强制剥夺的手段，将超额聚敛的土地从其旧时代的所有者手中剥夺，平均到部分农民手中。以此打破古代宗族对农村人口的束缚和垄断。中华帝国统治集团在掌权过程中一度中止这一变革。但在1820年的牧仲棠南征前后，为了经济振兴、解放生产和发动底层农民、士兵，牧仲棠及其亲信重新开启了这一运动。
- 现稿：
  > 这一运动发源自1810年的西秦大革命。被本时代人视为农业发达而宗族根深蒂固的东方诸国内萌发的一种近代经济上的变革运动。其特点大致可以是用赎买或强制剥夺的手段，将超额聚敛的土地从其旧时代的所有者手中剥夺，平均到部分农民手中。以此打破古代宗族对农村人口的束缚和垄断。中华帝国统治集团在掌权过程中一度中止这一变革。但在1820年的牧仲棠南征前后，为了经济振兴、解放生产和发动底层农民、士兵，牧仲棠及其亲信重新开启了这一运动。 ／ 要巩固地权革命的成果，政府可以推行土地商品化、国家城市化与营产改制。

### `nesnd_federal_compact`
- 文件：`localization/simp_chinese/replace/nesnd_south_politics_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：此修正是明廷内部权力约束，不是国际宗盟。
- 作者稿：
  > 重订联邦契约
- 现稿：
  > 礼法定制

### `nesnd_federal_compact_button_desc`
- 文件：`localization/simp_chinese/replace/nesnd_south_politics_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：采用作者拥明主张；内阁六部、一院制礼议院；把即时效果写为遣使争取支持。
- 作者稿：
  > 在新政完全实现已不可阻挡的今天，局势已经逐渐脱离了杭州南府的掌控——这是好的！由此，我们需要重新平衡杭州的势力与西府各省。就像过去的“大礼议”改变了北明中期的国家格局，我们应当在各省代表共同支持的如今，从速召开额外的大礼议会（南明国家议会）和内阁会议。重新议定任官、赋额、军费、省制。以北朝、西夷、东洲施行的宪法/礼法制度为参照，重整政治。或可使朱姓天子终于挣脱桎梏，主持南朝国政。
- 现稿：
  > 新政已使南朝无法退回旧日的藩镇格局，杭州南府也不能再独断国政。各省学政将在礼议院议定任官、赋额、军费与省制，内阁及六部则须依新定礼法施政。我们应先遣使争取西府各省与海外诸邦的支持，使朱姓天子摆脱南府的挟持，依礼法主持国政。

### `nesnd_crisis.10.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：作者稿精修；绝对多数/永久消灭所有地方权力无机制依据，改为支持新法和权力边界。
- 作者稿：
  > 随着各省学政（南明国会议员）在大礼议上以绝对多数表明了对新法的支持。以中央政府为核心的任官、田赋与军费改革终于统合为广泛承认的系列条陈，写入南明的国家“礼法”。依照新法，明廷，或者说现政权的明廷，终于结束了自西历15世纪初塞王之乱以来的地方割据的状态。 ／ 当然，在行政上的统一于陈东阳重设行省布政司时就完成了。但那时的政策并未命令废止“封君”制度，也没有确定中央政府和地方的权力边界。只是南、西两府面临北朝南下的危机空前团结，以至于无人对南京（实际是杭州）统一执行军政事权、任免官员、捕杀不从的力量发出异议。即使有，也早在两府大兵的铁蹄铁铳下碾为尘埃——如今，这一切的努力终于刻入石头，万世难改。
- 现稿：
  > 各省学政在礼议院支持新法，任官、田赋与军费条陈由此写入南明的国家礼法。明廷保全了朱氏统绪，中央与各省的权责也有了共同认可的依据。 ／ 陈东阳重设行省布政司时，南朝已能够统一调度军政，却没有一并解决旧封君的名位与地方权力。南、西两府面临北朝南下，曾以共同的军队压服不从。如今，因战事而暂且搁置的争执终于有了法定的处置办法。

### `nesnd_crisis.31.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：Keep author’s national military-fiscal breakdown, clarify governors’ relationship to armies, remove country-as-ordering-person and advisory council executive sovereignty.
- 作者稿：
  > 各地行营开始截留本应解往中央的税款。军官以供饷为名接管关卡、仓廪与地方官署，清丈官只能在驻军准许的地方办案。欠饷的营伍纷纷向主将索要田产，原有的营兵集团由此取得了更广的地方权力。 ／ [ROOT.GetCountry.GetName]发出的调防命令接连退回。朝廷须重新承认各营与地方议局的既得权力，才能维持各省对中央的归顺；继续失去军饷与官员的控制，各地便将自行建立政府。
- 现稿：
  > 各地行营开始截留本应解往户部的税款。军官以供饷为名接管关卡、仓廪与地方官署，省督或被迫迁就驻军，或依靠自己的亲军与之争夺财源。清丈官只能在驻军准许的地方办案。欠饷的营伍纷纷向主将索要田产，原有的营兵集团由此取得了更广的地方权力。 ／ 兵部奉[ROOT.GetCountry.GetRuler.GetFullNameWithTitle]之命发出的调防令接连退回。元老院中的勋旧要求承认各营与省督已经掌握的兵财之权，以换取各省继续奉朝廷正朔。咨议局送来的地方陈情也已无从逐案办理。朝廷若不能作出让步，失去约束的营兵便可能拥立自己的政府。

### `nesnd_crisis.32.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Preserve author’s military-household ownership, reduced rent, freedom to migrate and state-land compromise as proposed policy. The event appears before the choice, and acceptance permanently ends this campaign.
- 作者稿：
  > 各省请求暂缓地权改革的文书已经汇集到朝廷，但这些不过是迫使朝廷公卿乃至天子难堪的妥协文字。[ROOT.GetCountry.GetName]的统治者们却不得不向现实的困难妥协，徐图后进。根据妥协后的政策，所谓“新契”所确认的土地将照旧归属军户，只是需要军户们承诺对佃农进行一定的减租，并不得阻止佃农离开本地务工。尚未处置的庄田、军田与宗族产业将交由地方官署继续保管，成为所谓“国家公田”，并由官府招募租佃。 ／ 虽然是朝廷的屈辱，但利用这样一份诏书，[ROOT.GetCountry.GetName]朝廷使各省从清丈、申诉、聚众闹事的循环中暂时脱身。依靠旧有地权组织起来的地方势力也将重新参与税赋的征解和乡里的治理。
- 现稿：
  > 各省请求停止地权改革的文书已经汇集到朝廷。元老院中的勋旧提出一份妥协草案，拟请[ROOT.GetCountry.GetRuler.GetFullNameWithTitle]颁诏收束这场运动。所谓“新契”确认的土地仍归军户，但须由军户承诺减轻佃租，并准许佃农离乡务工。尚未处置的庄田、军田与宗族产业，则交由省督督办，暂列为“国家公田”，由官府招佃。 ／ 这份草案使力主改革的公卿难堪，也将使依靠旧有地权组织起来的地方势力重新参与征税与乡里治理。户部与兵部都希望借此平息各省争端，将有限的财赋与人力收回常政。若予批准，地权革命便将在这些妥协中结束。余下的理想，只能留待后人。

### `nesnd_crisis.33.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：Preserve the author’s arrests, refusal to surrender officers, and compensation demand; join them to actual persistent hardship and make the imminent NSX secession intelligible without declaring it before choice.
- 作者稿：
  > 清丈引起的搜捕，将山西的退伍军人、地方士人与失地农户聚到了一处。共和派借乡校与旧日军中关系传递文书，要求各县推举代表，审问侵夺田产的军官。 ／ 然而，随着多处驻军大营拒绝交出祸首。被煽动选出的代表转而要求撤换清丈主官，重新审查田产，并赔补遭到侵夺的农户。
- 现稿：
  > 山西的退伍军人、地方士人与失地农户，因清丈后的生活困顿和对脱离户籍者的搜捕而聚到了一处。共和派借乡校与旧日军中关系传递文书，要求各县推举代表，追究侵夺田产的军官。 ／ 几处驻军大营拒绝交出涉案军官，省督派去查问的官员也被挡在营外。各县代表因而要求撤换清丈主官，重审田产并赔补受害农户。共和派已开始联络愿意倒戈的营伍，准备在请愿无门时举兵。刑部将案情呈至朝廷，请求裁定是撤官重审，还是以抗命聚众治罪。

### `nesnd_crisis.20.d`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 当时理由：保留北朝敌视吴的阵营语气；原稿无条件说土改继续，事件实际可在土改后触发，改条件性。
- 作者稿：
  > 倭吴叛明称制的消息传来，江北大臣纷纷弹冠相庆。更有人提起牧家天子当年御辇南下的盛举。毕竟伪吴郑狗与西府各省决裂互斗中无暇北顾。南征统一或可一举成功。 ／ 有心人的策动下，边将请拨军饷，并派员联络湖广的“有识之士”。然而，我朝却不是什么太平兴国之世界。国内正在推进的地权改革仍在继续。如果在改革期间卷入南朝的混战，未来是福是祸仍未可知也。
- 现稿：
  > 倭吴叛明称制的消息传来，江北大臣纷纷弹冠相庆。更有人提起牧家天子当年御辇南下的盛举。伪吴与西府诸省决裂互斗，若无暇北顾，南征统一或可一举成功。 ／ 边将已经请求拨饷，并派人联络湖广的“有识之士”。然而，我朝也远非太平兴国之世。国内政务仍须军队与财力维持，地权改革若尚未完成，更难兼顾南征。此时卷入南朝的混战，究竟能为帝国赢得什么？

### `nesnd_huguang_preparations_reason`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：保留作者对西府政治根基和郑氏排挤的叙述；学政不作学籍/教育机关；朱斑博统一为朱班博。
- 作者稿：
  > 朱班博整顿湖广时，曾修复襄阳工事，召集青年军官任教，又用军工铁件向川蜀换取粮食。伤兵与退伍军人分入后勤、屯垦卫所，留在襄阳的共和派协助总督府改造岳麓书院。二十年间，总督府的军队、田赋、学政渐成一体。加上朝廷中有陈东阳为奥援。时人多以襄阳兵为“新西府”的魁首。更是南明联邦建国不可或缺的柱石。 ／ 然而，曾经极力支持朱斑博的郑家屡屡在朝廷中指责襄阳方面拖欠税款、瞒报户籍。又外放石元辅、林汉涵等亲湖广派的南兵高层和许多亲近湖广的共和派官员。一系列迹象表明我们必须做好最坏准备。重新核定屯田兵农丁口，接续上游的粮运，在书院中造势拉拢士子。以备不时之需。
- 现稿：
  > 朱班博整顿湖广时曾修复襄阳工事，召集青年军官任教，又用军工铁件向川蜀换取粮食。伤兵与退伍军人分入后勤、屯垦卫所，留在襄阳的共和派协助总督府改造岳麓书院。二十年间，总督府掌握的军队、田赋与书院渐成一体，朝中又有陈东阳为奥援。时人多以襄阳兵为“新西府”的魁首，南明联邦也不能缺少这根柱石。 ／ 然而，曾经极力支持朱班博的郑家如今屡屡指责襄阳拖欠税款、瞒报户籍。石元辅、林汉涵等亲近湖广的南兵高层相继外调，朝中与我们交好的共和派官员也受到排挤。我们必须做好最坏的准备：重新核定屯田兵农丁口，接续上游粮运，并争取书院中即将步入政坛的监生。

### `nesnd_hna_academy_button_desc`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：按最新用户设定重写政治教育因果；不把书院降格为粮饷培训；考试只叙述制度，不冒称按钮有考试机制。
- 作者稿：
  > 襄阳的岳麓书院是湖广派官员、仪政士子的精神中心。但是它建立时起就奉行着忠于南朝的“爱国”教育。在南府频频发难的危急时刻，我们必须整顿人员，让岳麓教员们在我们的指挥下逐渐将把持朝政的倭吴丑类和朱明皇室区分开。以团结我内部思想以备不测。
- 现稿：
  > 襄阳的岳麓书院是湖广官员与议政士子的精神中心。院中监生一面读书，一面习议国事，日后须通过礼议院的考试，才能进入南朝政坛。书院自创办以来便以忠于南朝训育诸生，如今南府步步相逼，我们须让教员讲明：把持朝政的郑吴与朱明皇室并非一体。今日在讲席间争取到的士子，或许就是来日同我们共进退的学政。

### `nesnd_hna_supply_button_desc`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：保留作者政治口吻与真实省际协定；此处约不是宪法，不能机械改为礼法。
- 作者稿：
  > 在不久前抗击牧贼的战争中，湖广的工坊与川蜀的粮船曾共同供养襄阳军民。我们应当按照需求重新组织两省军工与粮运。重新启用战时的沿江转运库。以备奸臣发难。
- 现稿：
  > 抗击牧贼时，湖广的工坊与川蜀的粮船曾共同供养襄阳军民。如今南府与西府的裂痕日深，我们应当重新联络川中旧交，依两省所需组织军工与粮运，启用战时的沿江转运库。奸臣若要发难，襄阳总得有粮有械。

### `nesnd_hna_veterans_button_desc`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：保留作者退伍组织与社会改革主题；删除冗余断句。
- 作者稿：
  > 朱班博时代起，楚兵待遇优厚就远超南朝友军。其中更包括学自北朝的退伍年限和老兵集会。意图以此驱使受训听话的退伍士兵带领垦丁充实乡里，最终快速革新、改善久困于战火的湖广社会民生。时至今日，形成规模的“集会”老兵既熟悉营伍，也熟悉乡里。除了能在战时听令动员民众之外，我们也可以借助集会的力量对民众进行经济、生活上的动员准备。
- 现稿：
  > 朱班博治楚时，楚兵待遇已远优于南朝友军。他又仿照北朝规定退伍年限、组织老兵集会，使受过训练的退伍士兵带领垦丁充实乡里，改善久困于战火的湖广民生。如今各地集会已有根基，老兵既熟悉营伍，也熟悉乡里。召集他们筹办粮食、救济与后勤，战时动员便可有所依凭。

### `nesnd_protect_chen_button_desc`
- 文件：`localization/simp_chinese/replace/nesnd_chen_security_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：把用户保护改革领袖的动机接到真正后覆盖警卫按钮；保留真实有期限/风险，不恢复旧永久保护。
- 作者稿：
  > 陈东阳主持的改制触及各地士族、北明旧封君、明军军官的田产和爵位。不时有反诗、威胁信被我明锦衣卫截获。虽然陈东阳本人无所畏惧，但我们不能再托大。鉴于东关先生（陈东阳）对新法的独特意义，为了保障内阁继续推动改革的能力和朝廷的集权努力，我们应当选拔可靠的内卫高手组建保卫陈东阳大人的专属部队。
- 现稿：
  > 陈东阳主持的改制触及士族、旧封君与军官的田产和爵位。东关先生本人虽无所畏惧，朝廷却不能轻视这些敌意。安排专任护卫，并决定是否令他暂留官署、清查内应，以保全继续推动新政的力量。 ／ 警卫任期#v 六个月#!。未设专卫时，本案死亡、负伤、脱险的概率为#v 40／25／35#!。详细经费与续办办法见警卫议案。

## 四、选项和名称的小改（6 键）

多数是为了让文字对得上实际效果：30.c 实际是镇压；32.a 实际是永久收束而非暂缓；20.c 襄樊是大营不是“诸府”。

**建议：效果相关的三条（30.c、32.a、20.c）保留现稿；其余三条（30.b、`nesnd_hna_veterans`、`nesnd_protect_chen_button`）可恢复作者原文。**

### `nesnd_crisis.30.b`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：The Consultative Council can present petitions, not take over executive authority. Distinguish the local compromise from the central appeals review in A.
- 作者稿：
  > 责成地方议局办理。
- 现稿：
  > 责成省督议处，酌从地方之请。

### `nesnd_crisis.30.c`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：The actual option is repression, with radicals and higher disorder; merely declaring that the law binds garrisons hides the choice.
- 作者稿：
  > 令各营交册，依新法处置。
- 现稿：
  > 令各营交册，抗命聚众者依法惩办。

### `nesnd_crisis.32.a`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：The original “暂缓” promises a reversible pause; actual acceptance closes the whole reform permanently.
- 作者稿：
  > 依此颁诏，暂缓余案。
- 现稿：
  > 准此颁诏，收束地权革命。

### `nesnd_crisis.20.c`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：未能定位
- 当时理由：襄樊是据点/大营，不造“襄樊诸府”。
- 作者稿：
  > 联络襄樊诸府，准备南下。
- 现稿：
  > 联络襄樊大营，准备南下。

### `nesnd_hna_veterans`
- 文件：`localization/simp_chinese/replace/nesnd_crisis_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：统一本轮设定与名称，保持原有数值和功能。
- 作者稿：
  > 退伍安置章程
- 现稿：
  > 老兵集会

### `nesnd_protect_chen_button`
- 文件：`localization/simp_chinese/replace/nesnd_chen_security_l_simp_chinese.yml`；作者稿来源：11-02作者改稿；改动提交：1cb7b0c 2026-11-02 Correct constitutional canon and bilingual narrative context
- 当时理由：统一本轮设定与名称，保持原有数值和功能。
- 作者稿：
  > 保护首辅与审议程序
- 现稿：
  > 首辅警卫案

## 五、埃及（3 键）

两条按钮说明是作者在本机改的，代理后来在末尾补了一句“十二个月内不能更改这项安排”，与任务44按作者指示加的 12 个月锁定一致。日志正文是作者改了一个字（学堂→学校）之后，被代理整段重写。

**建议：两条按钮说明保留现稿（补的是真实限制）；日志正文恢复作者原文。**

### `nesnd_egypt_choose_cost`
- 文件：`localization/simp_chinese/replace/nesnd_egypt_l_simp_chinese.yml`；作者稿来源：be56496 作者本机改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 作者稿：
  > 有效投资承诺每月消耗1独立性。
- 现稿：
  > 有效投资承诺每月消耗1独立性。十二个月内不能更改这项安排。

### `nesnd_egypt_none_effect`
- 文件：`localization/simp_chinese/replace/nesnd_egypt_l_simp_chinese.yml`；作者稿来源：be56496 作者本机改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 作者稿：
  > 撤回投资承诺并失去赞助利益，但既有外资所有权仍会影响独立性。
- 现稿：
  > 撤回投资承诺并失去赞助利益，但既有外资所有权仍会影响独立性。十二个月内不能更改这项安排。

### `nesnd_egypt_investment_accounts_reason`
- 文件：`localization/simp_chinese/replace/nesnd_egypt_l_simp_chinese.yml`；作者稿来源：be56496 作者本机改稿；改动提交：90f15ac 2026-11-04 Consolidate localization, clarify Qin conditions and fix runtime error loops
- 作者稿：
  > 购入机器容易，留下能够制造、修理和使用机器的人却要付出更多心力。大学要教出本国的技术人才，工具工场要供给生产所需的器械，新的工业也要招得到真正的工人。 ／ 朝廷希望这些事业能成为埃及自己的立国之本。无论资本来自何处，学校有人讲授、工场有人劳作，才算把纸上的许诺变成了国力。
- 现稿：
  > 埃及需要能够制造、修理和使用机器的人。大学培养的技术人才要有工场可去，工具厂生产的器械也要有工人使用。政府希望外国投资能带起本国的产业，使学校与工场不再长久依赖外来的教师和技师。
