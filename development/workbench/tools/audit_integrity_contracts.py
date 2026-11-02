from integrity_context import *
import argparse,re
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=C);p.add_argument('--label',default='after');a=p.parse_args();root=a.root
rows=[]
def check(n,b):rows.append({'name':n,'pass':bool(b)})
def tree(rel):return parse(read(root/rel))
def has(n,k,v=None):return any(x.key==k and (v is None or x.value==v) for x in n.walk())
f=tree('common/scripted_effects/nesnd_qe1_fracture.txt')
for tag in ['AFG','KAL','PER','TIB','KAS','MGL','TUV']:
 n=f.get('nesnd_qe1_release_'+tag.lower());born=next(x.get('on_created') for x in n.walk() if x.key=='create_country')
 check(tag+' newborn connected to bounded frontier setup',has(born,'nesnd_qe1_register_new_frontier','yes'))
for name in ['nesnd_qe1_check_civil_conflict']+['nesnd_qe1_release_'+x for x in ['xin','uzb','buk','khi','trc','kyr','tji','kaz','afg','kal','per','tib','kas','mgl','tuv','other_provinces']]:
 n=f.get(name);seeds=[x for x in n.walk() if x.key in ['random_scope_state','ordered_scope_state'] and has(x,'save_scope_as')]
 check(name+' only populated state seeds',bool(seeds) and all(has(x.get('limit'),'state_population','0') for x in seeds))
dp=tree('common/diplomatic_plays/nesnd_qe1_conflicts.txt')
check('frontier initiator humiliation, not mirror annex',dp.get('dp_nesnd_qe1_frontier').scalar('war_goal')=='humiliation' and dp.get('dp_nesnd_qe1_frontier').scalar('mirror_war_goal')!='yes')
check('civil contest still mirrored annex',dp.get('dp_nesnd_qe1_civil').scalar('war_goal')=='annex_country' and dp.get('dp_nesnd_qe1_civil').scalar('mirror_war_goal')=='yes')
war=f.get('nesnd_qe1_start_frontier_war')
check('late joiners receive guarded Qin annex countergoal',has(war,'add_war_goal') and has(war,'war_participant_has_war_goal_of_type_against') and has(war,'play_participant_has_war_goal_of_type_against'))
check('global fallback uses saved actor not global root',not any(x.value=='root' for x in war.walk()))
identity=tree('common/scripted_effects/nesnd_qe1_identity.txt').get('nesnd_qe1_convert_selected_cohort')
check('orphan cohort cleared before new half conversion',identity.children[0].key=='nesnd_qe1_clear_orphan_cohort')
loops=[x for x in identity.children if x.key=='every_scope_pop']
check('same half then whole religion then whole culture',len(loops)==3 and loops[0].get('change_pop_culture').scalar('value')=='0.5' and loops[1].get('change_pop_religion').scalar('value')=='1' and loops[2].get('change_pop_culture').scalar('value')=='1')
check('conversion contains no population deletion/count change',not any(x.key in ['kill_pop','remove_pop','change_pop_size','create_pop'] for x in identity.walk()))
fra=tree('events/ce_fra_unrest_events.txt').get('fra_unrest.10')
check('one complete French cancellation predicate',len(fra.all('cancellation_trigger'))==1 and has(fra.get('cancellation_trigger'),'has_journal_entry','je_ce_unstable_imperium') and has(fra.get('cancellation_trigger'),'is_character_alive','no'))
for rel in ['common/scripted_effects/ce_french_empire_journal_effects.txt','common/scripted_effects/ce_japan_gov_effects.txt']:
 check('character IG target routing '+rel,not any(x.key=='set_interest_group' and (x.value or '').startswith('ig:') for x in tree(rel).walk()))
ai=tree('common/scripted_triggers/00_ai_triggers.txt')
check('AI law matches law object',not any(x.key=='imposed_law' and x.value=='scope:law.type' for x in ai.walk()))
check('AI Donghak uses global law types, not JE-only saved scopes',not any((x.value or '').startswith('scope:donghak_desired_law_') for x in ai.walk()))
tech=f.get('nesnd_qe1_prepare_frontier_army')
check('frontier tech explicit, army only new with no existing force',has(tech,'add_technology_researched','line_infantry') and has(tech,'add_technology_researched','artillery') and has(tech,'army_size','0'))
check('frontier population-scaled rather than unconditional8',all(has(tech,'total_population',str(n)) for n in [50000,100000,200000,400000]))
trigger=tree('common/scripted_triggers/nesnd_cne_programs.txt')
check('reported CNE triggers each defined exactly once',all(len(trigger.all(k))==1 for k in ['nesnd_cne_urban_welfare_technology','nesnd_cne_urban_welfare_law']))
failed=[r['name'] for r in rows if not r['pass']]
dump(R/f'contracts-{a.label}.json',{'status':'FAIL' if failed else 'PASS','checks':rows,'failed':failed,'engine_verified':False})
print(json.dumps({'checks':len(rows),'failed':failed},ensure_ascii=False));raise SystemExit(bool(failed))
