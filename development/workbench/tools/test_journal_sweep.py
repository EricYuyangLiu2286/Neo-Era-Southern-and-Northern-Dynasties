from sweep_context import *
root=Path(sys.argv[1]) if len(sys.argv)>1 else C
checks=[]
def ck(name,fn):
 try:assert fn();checks.append({'name':name,'pass':True})
 except Exception as e:checks.append({'name':name,'pass':False,'detail':str(e)})
def tree(rel):return parse(read(root/rel))
ck('crisis_desc_has_no_country_value_evaluation',lambda:tree('common/scripted_buttons/nesnd_crisis_buttons.txt').get('nesnd_federal_compact_button').get('desc').value is not None)
ck('qin_reward_has_two_explicit_victory_branches',lambda:not tree('common/scripted_effects/nesnd_qe1_agendas.txt').get('nesnd_qe1_settle_agenda').get('if').get('else'))
for kind in ['court','military','representative']:
 ck('japan_'+kind+'_always_has_effect_preview',lambda kind=kind:tree('common/scripted_buttons/nesnd_jp_politics.txt').get('nesnd_jp_inspect_'+kind).get('effect').get('show_as_tooltip') is not None)
ck('india_identity_not_expanded',lambda:tree('common/scripted_triggers/nesnd_india_diplomacy.txt').get('nesnd_india_diplomacy_live').get('hidden_trigger') is not None)
phase='baseline' if root==B else 'candidate';dump(R/('regression-'+phase+'.json'),{'checks':checks,'pass':all(x['pass'] for x in checks),'source_files':man(root),'engine_verified':False})
print(phase,'PASS',sum(x['pass'] for x in checks),'FAIL',sum(not x['pass'] for x in checks))
sys.exit(not all(x['pass'] for x in checks))
