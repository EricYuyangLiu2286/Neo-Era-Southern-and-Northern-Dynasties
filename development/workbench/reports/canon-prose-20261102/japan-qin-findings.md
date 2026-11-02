# 日本、西秦—波斯与周边审校：发现与边界

审阅776个唯一键（含7个新增分支），提出266项建议。逐项对照见writing-comparison-japan-qin.md；机器可读建议、原值、来源、SHA分别见同目录japan-qin-*.json。

本报告只读实际游戏源码和作者资料。报告产物不改变E/C/主MOD；源码版本1.13.11/build24799966。无游戏运行，无“零BUG”认证。

|编号|问题|处理|
|---|---|---|
|JP01|Effective legacy text promises direct imperial rule, while C implements Emperor nominally retained and regent conducting government.|C-only proposals; do not silently certify E old behavior as repaired.|
|JP02|C completion requires independence and seven Honshu regions, but result says Honshu, Kyushu and Shikoku are united. E still has the old nine-region requirement.|C-only result rewrite. E nine-island prose retained until corresponding code changes.|
|JP03|Canneries technology and operating cannery PM are completion conditions, but the active JE can appear before them.|Describe canning as prospective industry, not guaranteed present operation.|
|JP04|Kinds1/2/3/4/5/7 all show generic agreement; request kind is erased after trigger_event. Kind6 annex intentionally skips reply.|Save kind scope before cleanup; six proposed descs. No new union success popup referring to dead partner.|
|QE01|Court remains eligible under presidential republic/custom proportional voting; imperial ruler narration and preserve throne/abolish throne are not universal entry facts.|Keep imperial-house faction/history; use government-neutral action and historical tense where needed.|
|QE02|Description treats literacy as eligibility requirement; custom law sets wealth threshold10 and literacy voting weight50.|Separate property franchise from literacy vote weight; do not claim literal district seat allocation.|
|QE03|Economic winner affects Armed Forces and Petite Bourgeoisie, not Landowners; economy push penalizes Armed Forces and Rural Folk.|Name the actual affected constituencies; preserve existing mechanical labels.|
|PER01|Original nesnd_per_aid_live checks route/future only; missing, hostile or invalid-overlord Qin can still appear as sending aid.|Root explicitly plans exists/alive QE1, no has_war_with QE1, if subject direct QE1; event cancellation when aid_live false. Existing received six-month help persists. Not verified here after root mutation.|
|PER02|Aid-route completion may fail to create/retain Qin tributary relationship, but outcome text was generic and did not distinguish this.|Root to branch on actual current subject_of QE1. Progress must still complete if Qin disappears; no deadlock added.|
|PER03|India targets include Delhi/Agra outside Indus basin; diplomatic notes are addressed to states, not geographical regions.|Wider northwestern India label; name governments as recipients, without inventing historical title.|
|TEN01|Abolition activates Slavery Banned, not merely debt-contract separation. Existing logging staffing requirement applies whenever a logging camp exists, including first commission.|Describe slavery generally; require any existing logging camp staffed before expansion. No code changes.|
|MAP01|Four waterworks descriptions explain post-split allocation and retained design; English repeats Chinese.|Describe irrigation/infrastructure benefits; preserve actual numbers and state locations.|
|LANG01|All79 English Philippines values are Chinese fallback. Map/state labels also contain fallback, not intentional English proper-name practice.|All79 proposals completed, preserving 8000/3000 and8700/3700 routes,12months,20ships, bilateral consent and political-allegiance independence of B.|

未判为缺陷的例子：秦身份衰退确实把所选本国州约半数西域汉羌同步改为目标文化与宗教（identity effect第35–40行）；原句半数分母正确，予以保留。日本国际盟约、军府、幕府和各府指当地政权时合法；没有机械改成礼法或各省。日本政治分支的代议/军府/君主条件已分别核读；当前正文不再无条件硬写丰臣家/先前战胜。

所有KEEP为本轮来源与文意判断，不能保证任意未来存档、游戏更新或未读外围脚本的行为。根任务应用requires_branch后仍须核对新的有效覆盖键、延迟scope和本次源码指纹。