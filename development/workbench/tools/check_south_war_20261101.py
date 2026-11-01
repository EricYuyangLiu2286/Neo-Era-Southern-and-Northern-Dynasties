"""Real-source regression checks. Does not simulate or run Victoria 3."""
from pathlib import Path
import sys,json
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
R=W/'reports/south-war-collapse-20261101';R.mkdir(exist_ok=True)
root=Path(sys.argv[1]);label=sys.argv[2];checks=[]
def get(rel,*keys):
 f=root/rel;n=parse(f.read_text('utf-8-sig')) if f.exists() else None
 for k in keys:n=n.get(k) if n else None
 return n
def has(n,k,v):return bool(n and any(x.key==k and x.value==v for x in n.walk()))
def check(n,ok):checks.append({'name':n,'pass':bool(ok)})
ev='events/usm_civilwar_events.txt';tr='common/scripted_triggers/nesnd_war_collapse.txt';ef='common/scripted_effects/nesnd_war_collapse.txt';je='common/journal_entries/nesnd_war_collapse.txt';oa='common/on_actions/nesnd_war_collapse.txt'
check('capital surrender event is enabled',has(get(ev,'usm_civilwar.5','trigger'),'nesnd_south_capital_defeat','yes'))
check('old monthly caller still present',has(get('common/on_actions/ce_code_on_actions.txt','ce_monthly_pulse_country','events'),None,'usm_civilwar.5'))
check('single-capital rule excludes Japan',has(get(tr,'nesnd_south_capital_defeat','trigger_if','NOT'),'c:JAP','this'))
check('capital OR 80 percent rather than AND',bool(get(tr,'nesnd_south_capital_defeat','trigger_if','OR','AND','OR','capital')) and has(get(tr,'nesnd_south_capital_defeat','trigger_if','OR'),'enemy_occupation','0.8'))
check('real war required for ordinary annexation',has(get(tr,'nesnd_south_capital_defeat'),'has_war_with','c:USM'))
check('pending surrender prevents duplicate popup',has(get(ev,'usm_civilwar.5','trigger'),'has_variable','nesnd_capital_surrender_pending'))
check('surrender effect rechecks current eligibility',has(get(ev,'usm_civilwar.5','after','if','limit'),'nesnd_south_capital_defeat','yes'))
check('no forced player transfer in restored surrender',not has(get(ev,'usm_civilwar.5'),'play_as','c:USM'))
check('Japan uses BOTH Kyoto and Kanto',all(get(tr,'nesnd_japan_two_centres_lost','s:'+s) for s in ['STATE_KYOTO','STATE_KANTO']))
check('two-centre occupation checks hostile controllers',all(has(get(tr,'nesnd_japan_two_centres_lost','s:'+s),'has_war_with','c:JAP') for s in ['STATE_KYOTO','STATE_KANTO']))
check('collapse requires Wu war or confirmed defeat',has(get(tr,'nesnd_japan_collapse_ready'),'has_war_with','c:JAP') and has(get(tr,'nesnd_japan_collapse_ready'),'has_variable','nesnd_japan_defeat_confirmed'))
check('collapse once guard',has(get(tr,'nesnd_japan_collapse_ready'),'has_global_variable','nesnd_japan_collapse_committed'))
check('collapse registers before annex and requests recovery',all(has(get(ef,'nesnd_japan_commit_war_collapse'),k,v) for k,v in [('nesnd_japan_register_annex_target','yes'),('annex_as_civil_war','c:JAP'),('nesnd_japan_recovery_request','yes')]))
check('single global journal context',has(get(je,'nesnd_japan_war_collapse'),'group','je_group_global_international_situations'))
check('journal activates once',has(get(je,'nesnd_japan_war_collapse','possible'),'has_global_variable','nesnd_japan_collapse_journal_started'))
check('journal executes collapse once globally, not per viewer',has(get(je,'nesnd_japan_war_collapse','on_weekly_pulse'),'nesnd_check_war_collapses','yes') and not get(je,'nesnd_japan_war_collapse','on_complete_all_involved'))
check('shared journal visible to Japan and enemy countries',has(get(tr,'nesnd_japan_collapse_viewer'),'c:JAP','this') and has(get(tr,'nesnd_japan_collapse_viewer'),'has_war_with','c:JAP'))
check('battle and empty-battle callbacks wired',all(get(oa,k) for k in ['on_battle_ended','on_empty_battle_won']))
check('defeat callback binds enforcing USM and exact JAP target',all(has(get(oa,'nesnd_record_wu_defeat','effect'),k,v) for k,v in [('scope:target','c:JAP'),('set_variable','nesnd_japan_defeat_confirmed')]))
check('enemy capitulation without a targeted wargoal is handled',has(get(oa,'on_enemy_capitulated_notification'),'on_actions',None) or has(get(oa,'on_enemy_capitulated_notification'),None,'nesnd_record_wu_defeat'))
check('ordinary defeated backer cannot survive solely through absent wargoals',has(get(tr,'nesnd_south_capital_defeat'),'has_variable','nesnd_south_defeat_confirmed') and has(get(oa,'nesnd_record_wu_defeat'),'set_variable','nesnd_south_defeat_confirmed'))
check('Japanese losing-side settlement branch restored',has(get('common/journal_entries/ce_usm_the_last_days_of_ming.txt','ce_usm_cw_japanese_interest','on_complete'),'nesnd_japan_defeat_confirmed','yes') or has(get('common/journal_entries/ce_usm_the_last_days_of_ming.txt','ce_usm_cw_japanese_interest','on_complete'),'set_variable','nesnd_japan_defeat_confirmed'))
check('military goods cost minus 20%',has(get('common/static_modifiers/nesnd_xiangyang.txt','nesnd_xiangyang_camp'),'country_military_goods_cost_mult','-0.20'))
check('camp defense plus 20%',has(get('common/static_modifiers/nesnd_xiangyang.txt','nesnd_xiangyang_camp'),'unit_defense_mult','0.20'))
check('camp tied to HNA-owned Xiangyang journal',has(get(je,'nesnd_xiangyang_camp_journal','possible'),'c:HNA','this') and has(get(je,'nesnd_xiangyang_camp_journal','modifiers_while_active'),None,'nesnd_xiangyang_camp'))
n=get('common/history/military_formations/CE_military_formations_asia.txt','MILITARY_FORMATIONS','c:HNA','create_military_formation')
check('HNA 25 battalions',bool(n) and sum(int(x.scalar('count')) for x in n.all('combat_unit'))==25)
check('Gansu inherits untouched vanilla lake and terrain files',not (root/'map_data/default.map').exists() and not (root/'map_data/province_terrains.txt').exists())
check('noncapital renamed Xiyi', 'STATE_JETISY:0 "西益"' in (root/'localization/simp_chinese/replace/map/ce_states_l_simp_chinese.yml').read_text('utf-8-sig'))
for k in ['ce_usm_suppress_rebellion','ce_usm_restoration_of_ming','ce_usm_acheive_revolution']:
 check(k+' defers status quo while defeat resolution is pending',has(get('common/journal_entries/ce_usm_the_last_days_of_ming.txt',k,'fail'),'nesnd_south_defeat_resolution_pending','yes'))
check('global status-quo event also rechecks pending resolutions',has(get(ev,'usm_civilwar.9','trigger'),'nesnd_south_defeat_resolution_pending','yes'))
out={'source':str(root),'validation':'STATIC_PASS' if all(x['pass'] for x in checks) else 'STATIC_FAIL','game_launched':False,'checks':checks};(R/(label+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(out['validation'],sum(x['pass'] for x in checks),'/',len(checks));print('\n'.join(x['name'] for x in checks if not x['pass']))
if label!='red':assert all(x['pass'] for x in checks)
