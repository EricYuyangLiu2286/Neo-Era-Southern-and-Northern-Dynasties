# 自给经济、资格与转型：本机1.13.11

用于人口、农业、产业、土地改革和福利设计。2026-10-31核对本机代码；遇到相应源码指纹变化重验。具体国家试案与数据放WORK/plans/two-empires/02、03，不把试案数字当通用平衡规则。

## 文件链

- `map_data/state_regions/*.txt`：`arable_land`、`subsistence_building`、农业/种植园可建类型。国家实际可用容量还受分州占比等影响，须读取游戏。
- `common/buildings/12_subsistence.txt` 与 `common/building_groups/00_building_groups.txt`：不可手建/扩建的自给建筑，自动放置、仅雇失业者；商业农业/种植园用地，矿业/林业不一概占耕地。
- `common/production_methods/12_subsistence.txt`：普通自给基础5000 peasants/级、稻田10000；家庭作坊另有少量市场衣物/家具/酒。法律PM还会改变农民职业构成与自给产出。
- `common/pop_types/peasants.txt`：自给收入、消费倍率0.05、非失业职业；`laborers.txt`：可直接招聘且支持失业。不要把“自给农多”直接写成“失业多”。
- `common/pop_types/machinists.txt`、`engineers.txt`等：资格的脚本公式；识字、财富、旧职业和农奴制的影响按实际职业查。工程师某注释与公式系数不同，代码为准。`portrait_age`是肖像，不是招聘年龄限制；未见直接按个体年龄筛工人的当前脚本，不推断隐藏人口年龄系统。
- `common/history/pops`决定群体；`common/history/population`调用财富/识字effect。`common/scripted_effects/00_starting_pop_{wealth,literacy}.txt`明确初始化后还会计算，所以参数值不等于实际首日财富/识字。文件名不是生效国家，必须核对内部`c:TAG`。
- `common/laws/02_welfare.txt`与`common/institutions/00_institutions.txt`：真实救济支付、最低工资、家属收入、劳动人口比例和粮食保障效果；救济需国库与行政承受，不是凭空订单。`buy_packages`/`pop_needs`和实际商品账验证新增收入转成何种需求。

## 判断方法

严格区分三种数量：地图定义的可耕地总容量；历史/存档中商业农业占用的土地；引擎在剩余用地放置的自给建筑及其实际就业。`history/pops`是人口群体，`history/buildings`是初始建筑，都不是`arable_land`的来源。增删人口或修复建筑不能称为“恢复自给农土地”。称“恢复”必须指出被还原的文件、旧值和来源指纹；原版与作者设计不同仅是比较线索，参照原版重新分配应标为设计试案。2026-10-31山西335→375且河南500→460的试案并非恢复作者值，最新参考候选未采用，详见WORK/plans/two-empires/evidence/arable-provenance.md。

新增农场先算旧自给岗位损失、新PM的分职业岗位、资质人口和工资预期；再看投入和销路。新增工厂不一定高资质，但提高PM会改变岗位比例。建筑存在不等于有工作、满员不等于盈利，商品便宜也不能救无收入家庭。失业或低收入仍需按[可恢复性与两极案例](economic-agency-and-crises.md)分类：可被正常投资/转岗/外交改善的压力可以保留，不先假定需要增加耕地或删掉全部低薪产业。

可增加新州可耕地，不要求从别州抵扣；纯地图拆分的守恒检查不限制后续有依据的平衡调整。区分两种现场：自给建筑满员且仍有失业者，增加合理土地可试验承接；自给岗位未满，则先检查实际招聘失败原因，不以加地替代诊断。粮食保障差但已有工作的家庭还需查工资、税负、物价与收入来源。

用户提出高薪岗位会影响低薪岗位的求职意愿，必须纳入当地行业组合核验，但不能把“存在更高薪职位”直接当成所有失业的充分原因。本机`00_defines.txt`的`MIN_RAISE_TO_HIRE=0.10`说明在职换工所需加薪；它不直接证明失业者的保留工资公式。另查`BUILDING_DEFAULT_MIN_EARNINGS_TO_HIRE_EMPLOYEES`、`BUILDING_PROFIT_TARGET_TO_HIRE_EMPLOYEES`、`BUILDING_FAILED_HIRE_COOLDOWN_WEEKS_WITHOUT_WAGE_RAISE`，结合招聘悬停、工资报价、职业资质/接纳、实际员工变化及家庭收入，区分建筑不招、工资不合适、资质不足和岗位已满。指标单位须核对，不能将建筑周工资率直接当个人年薪。

农业国与工业国均可保有自给经济。高级PM节约劳动力在紧缺经济可能有益，在劳动力过剩且无替代就业时可能压低家庭收入；同一技术不能对所有国家写固定收益。政治改革、教育、迁移和福利提供不同过渡路径，须按法规资格和国库能力实际实现。

基线与修改后比较：职业劳动力、无workplace代理与UI失业、识字/资格、工资、food_security、财富/SoL、价格和财政。首日缓存可能未结算，至少走周/月；人口加权wealth不冒充UI SoL。适用的验证闭包见system-design-and-plans。
