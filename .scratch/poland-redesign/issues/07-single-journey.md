# 波兰朝圣者逐批迁移

部署版本 `914bcc27d778fa13936b4457b8bf3fb7`。开工 check 三方一致，旧版为 `7872679d`。

全局日志每周处理一批。有效路线满 100 后结算人口、归零，再从尚待离境的人口中选下一批。路线失效时重新选路。正文列一条路线，地图标出这条路线的起讫州，条面与悬停标题均使用「流亡者行程」。沿用旧第一条行程的变量和进度条标识。旧第二条路线在选择时没有扣除人口，更新后也没有结算入口。

六个运行文件位于源目录，分别为

- `common/journal_entries/nesnd_polish_exile.txt`
- `common/scripted_progress_bars/nesnd_polish_exile.txt`
- `common/scripted_effects/nesnd_polish_exile.txt`
- `common/scripted_triggers/nesnd_polish_exile.txt`
- `localization/simp_chinese/nesnd_polish_exile_l_simp_chinese.yml`
- `localization/english/nesnd_polish_exile_l_english.yml`

STATIC_PASS。Toolkit 六文件零诊断，本地化链接零发现。结构检查核对了每周调用次数、满条门槛、人口结算与进度清零的先后，以及下一批的出发条件。部署逐文件 SHA-256 一致。

未实机验证。重启游戏后读有活动行程的旧档，检查日志只显示一条路线和一根进度条。走满一次，观察待离境人数、抵达与死亡读数和下一批从零起步。