# 完成条件对读

作者原始样本：pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_cne_events_l_simp_chinese.yml，cne_landreform_failure_tracker_100：“进度到达#bold 100#!时，腐化日志自动完成”。保留直接说明指标与阈值的句法，正文不重复机制。

原显示为country_var_greater_or_equal has no localization。改为“‘近西帝国的前途’进度达到100”；实际本地化引用已有进度名，数字与原完成谓词同为100。英文Progress towards … has reached 100；与中文同义，无新增剧情、开发说明或完成后果。中英文编辑检查通过；真实UI待用户验证。

仅此自定义变量条件使用一条custom_tooltip，保留原has_variable分支及比较，不改用镜像bar决定结算。棉田、纺织厂、铁路仍由三个原生条件分别呈现，没有添加建筑custom_tooltip，也没有把全国总量换成单座建筑或添加90%雇佣的新门槛。
