"""Checks actual generated source and teardown closures; never executes the game."""
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts');from pdx import parse
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/cne-confidence-20261101';C=Path(sys.argv[1]);label=sys.argv[2];rows=[];cache={};regions=json.loads((R/'initial-inventory.json').read_text('utf-8'))['regions']
def node(rel,*keys):
 if rel not in cache:cache[rel]=parse((C/rel).read_text('utf-8-sig')) if (C/rel).exists() else None
 n=cache[rel]
 for k in keys:n=n.get(k) if n else None
 return n
def has(n,k,v):return bool(n and any(x.key==k and x.value==v for x in n.walk()))
def test(k,v):rows.append({'name':k,'pass':bool(v)})
ef='common/scripted_effects/nesnd_cne_programs.txt';tr='common/scripted_triggers/nesnd_cne_programs.txt';btn='common/scripted_buttons/nesnd_cne_programs.txt';je='common/journal_entries/nesnd_cne_programs.txt';mods='common/static_modifiers/nesnd_cne_programs.txt';sv='common/script_values/nesnd_cne_programs.txt';parent='common/journal_entries/ce_cne_land_draft.txt';cr='common/scripted_effects/nesnd_crisis_effects.txt'
test('exactly three child journals',len(node(je).children if node(je) else [])==3)
test('parent JE existence gates every child programme',has(node(tr,'nesnd_cne_programs_live'),'has_journal_entry','ce_cne_land_reform'))
for kind in ['land','urban','camps']:
 n=node(je,'nesnd_cne_'+kind+'_journal')
 test(kind+' uses parent-dependent possible and invalid',has(n.get('possible') if n else None,'nesnd_cne_programs_live','yes') and has(n.get('invalid') if n else None,'nesnd_cne_programs_live','yes'))
 test(kind+' has explicit teardown',bool(n and n.get('on_invalid')))
for state in regions:
 key='nesnd_cne_camp_'+state[6:].lower();flag=key+'_active';start=node(ef,key+'_start');stop=node(ef,key+'_stop')
 test(state+' literal state scope is guarded',has(node(tr,key+'_ready','trigger_if','limit'),'exists','s:'+state+'.region_state:CNE'))
 test(state+' start flag and country penalty',has(start,'set_variable',flag) and has(start,'name',key+'_opposition'))
 test(state+' character penalty distinct from country penalty',has(start,'name',key+'_officers') and has(node(mods,key+'_officers'),'character_loyalty_add','-1'))
 test(state+' army approval -1',has(node(mods,key+'_opposition'),'interest_group_ig_armed_forces_approval_add','-1'))
 test(state+' state benefit triad',all(has(start,'name','nesnd_cne_camp_'+x) for x in ['agriculture','mining','administration']))
 test(state+' exact country/character/state teardown',all(has(stop,'remove_modifier',x) for x in [key+'_opposition',key+'_officers','nesnd_cne_camp_agriculture','nesnd_cne_camp_mining','nesnd_cne_camp_administration']) and has(stop,'remove_variable',flag))
 test(state+' included in terminal cleanup',has(node(ef,'nesnd_cne_stop_all_programs'),key+'_stop','yes'))
 test(state+' contribution counts active flag once',sum(1 for x in node(ef,'nesnd_cne_refresh_camp_count').walk() if x.key=='has_variable' and x.value==flag)==1 if node(ef,'nesnd_cne_refresh_camp_count') else False)
 test(state+' start/stop mutually exclusive',has(node(btn,key+'_start_button','visible','NOT'),'has_variable',flag) and has(node(btn,key+'_stop_button','visible'),'has_variable',flag))
 test(state+' start and stop buttons in estate journal',all(has(node(je,'nesnd_cne_camps_journal'),'scripted_button',key+'_'+x+'_button') for x in ['start','stop']))
test('exactly 22 initial regions, not future conquests',len(regions)==22 and sum(1 for x in node(tr,'nesnd_cne_initial_reform_state').walk() if x.key=='state_region')==22 if node(tr,'nesnd_cne_initial_reform_state') else False)
test('per-estate monthly contribution .05',has(node(sv,'nesnd_cne_program_monthly_progress'),'multiply','0.05'))
test('land and urban monthly rates',has(node(sv,'nesnd_cne_program_monthly_progress'),'add','0.25') and has(node(sv,'nesnd_cne_program_monthly_progress'),'add','0.35'))
test('old passive +2/+0.5 progress removed',not any(x.key=='change_variable' and x.scalar('name')=='cne_landreform_completion_tracker' and x.scalar('add') in {'2','0.5'} for x in node(cr,'nesnd_land_monthly').walk()))
test('new progress linked to actual programmes',has(node(cr,'nesnd_land_monthly'),'add','nesnd_cne_land_monthly_delta'))
test('existing progress not reinitialised',not has(node(ef,'nesnd_cne_programs_init'),'name','cne_landreform_completion_tracker'))
test('all parent exits clear programmes',has(node(cr,'nesnd_land_cleanup'),'nesnd_cne_programs_cleanup','yes') and all((has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_programs_cleanup','yes') or (has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_end_failed_reform','yes') and has(node('common/scripted_effects/nesnd_cne_confidence.txt','nesnd_cne_end_failed_reform'),'nesnd_cne_programs_cleanup','yes'))) for k in ['on_fail','on_invalid']))
test('cloned countries use local cleanup',has(node(cr,'nesnd_land_cleanup'),'nesnd_cne_cleanup_inherited_programs','yes') and not has(node(ef,'nesnd_cne_cleanup_inherited_programs'),'nesnd_cne_stop_all_programs','yes'))
test('new successful coup blocks completion as well as failing parent',all(has(node(parent,'ce_cne_land_reform',k),'nesnd_cne_reform_failed','yes') for k in ['complete','fail']) and has(node(cr,'nesnd_land_success'),'nesnd_cne_reform_failed','yes'))
test('actual country coup result and baseline used',has(node(tr,'nesnd_cne_coup_has_succeeded'),'has_modifier','modifier_government_recently_couped') and has(node(tr,'nesnd_cne_coup_has_succeeded'),'has_variable','nesnd_cne_old_coup_baseline'))
test('AI hysteresis and restart delay',all(has(node(ef,'nesnd_cne_programs_maintenance'),k,v) for k,v in [('var:cne_landreform_failure_tracker','65'),('var:cne_landreform_failure_tracker','45'),('months','6')]))
test('AI bounded projects and population priority',has(node(ef,'nesnd_cne_programs_maintenance'),'nesnd_cne_active_camp_count','3') and has(node(ef,'nesnd_cne_programs_maintenance'),'order_by','state_population'))
test('landowners and peasants bear land reform cost',has(node(mods,'nesnd_cne_land_commercialization'),'interest_group_ig_landowners_approval_add','-2') and has(node(mods,'nesnd_cne_land_commercialization'),'interest_group_ig_rural_folk_approval_add','-1'))
test('industrialists attracted, not paid approval, by land reform',has(node(mods,'nesnd_cne_land_commercialization'),'interest_group_ig_industrialists_pop_attraction_mult','0.15') and not any(x.key=='interest_group_ig_industrialists_approval_add' for x in node(mods,'nesnd_cne_land_commercialization').walk()) if node(mods,'nesnd_cne_land_commercialization') else False)
test('urban industry and welfare conditions visible',has(node(tr,'nesnd_cne_urban_foundation'),'count','5') and has(node(tr,'nesnd_cne_urban_foundation'),'institution','institution_social_security'))
for i,action in [(1,'invest'),(2,'relieve')]:
 p=node('common/scripted_effects/nesnd_cne_reform.txt','nesnd_reform_'+action);e=node('events/nesnd_cne_funding.txt','nesnd_cne_funding.'+str(i))
 test(action+' proposal does not spend',not any(x.key=='add_treasury' for x in p.walk()))
 test(action+' scoped target in event placement',has(e,'placement','scope:nesnd_cne_funding_state'))
 test(action+' cancellation and guarded spending',has(e.get('cancellation_trigger') if e else None,('nesnd_cne_funding_target_valid' if i==1 else 'nesnd_cne_relief_target_valid'),'yes') and any(x.key=='add_treasury' for x in e.walk()) if e else False)
test('proposal target has owner and existence validation',has(node(tr,'nesnd_cne_funding_target_valid','trigger_if','limit'),'exists','scope:nesnd_cne_funding_state') and has(node(tr,'nesnd_cne_funding_target_valid'),'owner','root'))
for lang in ['simp_chinese','english']:
 p=C/f'localization/{lang}/replace/zzzzzz_nesnd_cne_programs_l_{lang}.yml';s=p.read_text('utf-8-sig') if p.exists() else ''
 test(lang+' named buttons and target-localised funding',all('$'+r+'$' in s for r in regions) and "SCOPE.sState('nesnd_cne_funding_state').GetName" in s and p.read_bytes().startswith(b'\xef\xbb\xbf') if p.exists() else False)
test('preview numeric read has branch guard',has(node(tr,'nesnd_cne_program_can_start','trigger_if','limit'),'has_variable','cne_landreform_failure_tracker') and has(node(tr,'nesnd_cne_program_can_start','trigger_else'),'always','no'))
test('camp count preview uses safe accessor',has(node(ef,'nesnd_cne_refresh_camp_count'),'nesnd_cne_active_camp_count','0') and has(node(sv,'nesnd_cne_active_camp_count'),'has_variable','nesnd_cne_camps_active'))
test('monthly officers are a bounded registry',not any(x.key=='every_country' for x in node(ef,'nesnd_cne_programs_maintenance').walk()) if node(ef,'nesnd_cne_programs_maintenance') else False)
test('officer registry registered and cleared',has(node(ef,'nesnd_cne_register_officer'),'name','nesnd_cne_reform_officers') and has(node(ef,'nesnd_cne_programs_cleanup'),'clear_variable_list','nesnd_cne_reform_officers'))
test('structural prerequisites rechecked while active',all(has(node(ef,'nesnd_cne_programs_maintenance'),'nesnd_cne_'+x+'_foundation','yes') for x in ['land','urban']))
test('relief saved target still must be starving',has(node(tr,'nesnd_cne_relief_target_valid'),'is_in_mild_starvation','yes'))
test('funding duration is one native month and lock lasts two',all(has(node('events/nesnd_cne_funding.txt','nesnd_cne_funding.'+str(i)),'duration','1') for i in [1,2]) and all(has(node('common/scripted_effects/nesnd_cne_reform.txt','nesnd_reform_'+a),'months','2') for a in ['invest','relieve']))
out={'validation':'STATIC_PASS' if all(x['pass'] for x in rows) else 'STATIC_FAIL','game_launched':False,'source':str(C),'checks':rows};(R/(label+'.json')).write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(out['validation'],sum(x['pass'] for x in rows),'/',len(rows));print('\n'.join(x['name'] for x in rows if not x['pass']) if label!='red' else 'Full negative check list saved to red.json')
if label!='red':assert all(x['pass'] for x in rows)
