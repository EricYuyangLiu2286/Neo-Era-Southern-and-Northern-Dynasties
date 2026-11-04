from sweep_context import *
from test_commission_gate_behavior import Evaluator,Obj
from copy import deepcopy
import re
rows=[]
def ck(name,f):
 try:assert f();rows.append({'name':name,'pass':True})
 except Exception as e:rows.append({'name':name,'pass':False,'detail':repr(e)})
class E(Evaluator):
 def expr(self,n,o,root,prev):
  if n.key and n.key.startswith('var:'):
   assert n.key[4:] in o.a['vars'];return self.cmp(o.a['variable_values'][n.key[4:]],n.op,float(n.value))
  return super().expr(n,o,root,prev)
for balance in [-50,-49,-5,0,5,49,50]:
 for waiting in [False,True]:
  def case(balance=balance,waiting=waiting):
   o=Obj('country','QE1',vars={'nesnd_qe1_balance','nesnd_qe1_econ_edge','nesnd_qe1_army_edge'},variable_values={'nesnd_qe1_balance':balance})
   if waiting:o.a['vars']|={'nesnd_qe1_econ_wait','nesnd_qe1_army_wait'}
   ev=E(C,{'countries':{'QE1':o}})
   econ=ev.test('nesnd_qe1_economic_victory','QE1');army=ev.test('nesnd_qe1_military_victory','QE1')
   return econ==(balance==-50 and not waiting) and army==(balance==50 and not waiting) and not(econ and army)
  ck(f'qin_{balance}_waiting{waiting}',case)
for kind in ['court','military','representative']:
 def case(kind=kind):
  a=parse(read(B/'common/scripted_buttons/nesnd_jp_politics.txt')).get('nesnd_jp_inspect_'+kind)
  b=parse(read(C/'common/scripted_buttons/nesnd_jp_politics.txt')).get(a.key)
  return shape(a.get('ai_chance'))==shape(b.get('ai_chance')) and shape(a.get('effect').get('if'))==shape(b.get('effect').get('hidden_effect').get('if'))
 ck('same_japan_execution_and_ai_'+kind,case)
for row in json.loads(read(R/'bulk-changes.json'))['pins']:
 def case(row=row):
  a=parse(read(B/row['file'])).get(row['key']);b=parse(read(C/row['file'])).get(row['key'])
  assert b.scalar('should_be_pinned_by_default_uninvolved_or_context')=='yes'
  b.children=[x for x in b.children if x.key!='should_be_pinned_by_default_uninvolved_or_context'];return shape(a)==shape(b)
 ck('pin_only_'+row['key'],case)
def native():
 a=parse(read(G/'events/agitators_events/agitators_law_events.txt'));b=parse(read(C/'events/agitators_events/agitators_law_events.txt'))
 assert [x.key for x in a.children]==[x.key for x in b.children]
 return all(shape(x)==shape(y) for x,y in zip(a.children,b.children) if x.key!='agitators_law_events.3')
ck('all_other_native_events_unchanged',native)
def no_dynamic():
 return not any(n.get('desc') and n.get('desc').children for p in (C/'common/scripted_buttons').glob('*.txt') for n in parse(read(p)).children if n.key and n.key.startswith('nesnd_'))
ck('all_mod_dynamic_button_desc_country_calls_removed',no_dynamic)
def india():
 a=parse(read(B/'common/scripted_triggers/nesnd_india_diplomacy.txt'));b=parse(read(C/'common/scripted_triggers/nesnd_india_diplomacy.txt'))
 for k in ['nesnd_india_reply_valid','nesnd_india_reply_can_accept']:assert shape(a.get(k))==shape(b.get(k))
 return True
ck('india_delayed_request_guards_preserved',india)
ck('external_story_default_pin_enabled',lambda:parse(read(C/'common/journal_entries/nesnd_external_journal.txt')).get('nesnd_external_policy').scalar('should_be_pinned_by_default_uninvolved_or_context')=='yes')
bm,cm=man(B),man(C)
ck('all_history_population_map_and_graphics_preserved',lambda:all(cm[p]==h for p,h in bm.items() if p.startswith(('common/history/','map_data/','gfx/','common/country_definitions/','common/cultures/'))))
for p in C.rglob('*.txt'):
 if p.relative_to(C).as_posix().startswith(('common/','events/')):parse(read(p))
def sig(x):return x['severity'],x['key'],x['message'],tuple((z.get('path'),(z.get('line') or '').strip()) for z in x['locations'])
old={sig(x) for x in json.loads(read(R/'tiger-baseline.json'))};added=[x for x in json.loads(read(R/'tiger-candidate.json')) if sig(x) not in old]
dump(R/'tiger-added.json',added)
ck('tiger_no_added_diagnostic',lambda:not added)
dump(R/'boundary-checks.json',{'checks':rows,'pass':all(x['pass'] for x in rows),'engine_verified':False,'source_files':cm})
print('PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows))
for row in rows:
 if not row['pass']:print(row)
for x in added:print(x['key'],x['message'],x['locations'][:1])
sys.exit(not all(x['pass'] for x in rows))
