from qin_stage_context import *
import copy,itertools,subprocess,collections

def run(root):
 triggers={n.key:n for p in (root/'common/scripted_triggers').glob('nesnd_qe1*.txt') for n in parse(read(p)).children}
 unlock=parse(read(root/'common/scripted_effects/nesnd_qin_persia_lifecycle.txt')).get('nesnd_qe1_unlock_later_journals')
 def cond(n,e):
  k,v=n.key,n.value
  if k in triggers:return block(triggers[k].children,e)==(v=='yes')
  if k in ['AND','limit','hidden_trigger']:return block(n.children,e)
  if k=='OR':return any(cond(x,e) for x in n.children)
  if k in ['NOT','NOR']:return not any(cond(x,e) for x in n.children)
  if k=='has_variable':return v in e['vars']
  if k=='has_journal_entry':return v in e['jes']
  if k=='exists':return v=='c:QE1' and e['alive']
  if k=='c:QE1':return e['alive'] and e['tag']=='QE1'
  if k=='is_country_alive':return e['alive']==(v=='yes')
  if k=='has_law_or_variant':return v.split(':')[-1] in e['laws']
  if k=='country_or_subject_owns_entire_state_region':return v in e['owned']
  if k=='num_states':return {'>=':e['states']>=int(v),'<':e['states']<int(v)}[n.op]
  if k=='always':return v=='yes'
  raise AssertionError(('unsupported predicate',k,v))
 def block(nodes,e):
  branch=False;handled=False;results=[]
  for n in nodes:
   if n.key=='trigger_if':
    branch=True;handled=block(n.get('limit').children,e)
    if handled:results.append(block([x for x in n.children if x.key!='limit'],e))
   elif n.key=='trigger_else':
    if not handled:results.append(block(n.children,e))
   else:results.append(cond(n,e))
  return all(results)
 def effects(nodes,e):
  for n in nodes:
   if n.key=='if':
    if block(n.get('limit').children,e):effects([x for x in n.children if x.key!='limit'],e)
   elif n.key=='set_variable':e['vars'].add(n.value)
   else:raise AssertionError(('unsupported unlock effect',n.key))
 def environment():return {'tag':'QE1','alive':True,'states':36,'vars':set(),'jes':set(),'laws':{'law_monarchy','law_autocracy'},'owned':set()}
 def entry(kind,e):
  n=parse(read(root/f'common/journal_entries/nesnd_qe1_{kind}.txt')).get(f'nesnd_qe1_{kind}_journal')
  return block(n.get('possible').children,e)
 rows=[]
 for name,update,expected in [
  ('new start',{},(False,False)),
  ('short agenda ended',{'vars':{'nesnd_qe1_agenda_done'}},(True,True)),
  ('early Hexi recovery',{'owned':{'STATE_HEXI'}},(False,True)),
  ('old active court',{'jes':{'nesnd_qe1_court_journal'}},(True,False)),
  ('old active recovery',{'jes':{'nesnd_qe1_recovery_journal'}},(False,True)),
  ('completed recovery',{'vars':{'nesnd_qe1_agenda_done','nesnd_qe1_recovery_done'}},(True,False)),
  ('archived court',{'vars':{'nesnd_qe1_agenda_done','nesnd_qe1_court_archived'}},(False,True)),
  ('democratic exit',{'vars':{'nesnd_qe1_agenda_done'},'laws':{'law_universal_suffrage'}},(False,True)),
  ('council exit',{'vars':{'nesnd_qe1_agenda_done'},'laws':{'law_council_republic'}},(False,True)),
  ('small surviving Qin',{'vars':{'nesnd_qe1_agenda_done'},'states':3},(False,True))]:
  e=environment();e.update(update)
  if unlock:effects(unlock.children,e)
  result=(entry('court',e),entry('recovery',e));rows.append({'name':name,'expected':expected,'observed':result,'pass':result==expected})
  if unlock:
   old=copy.deepcopy(e);effects(unlock.children,e);rows.append({'name':name+' unlock idempotent','pass':e==old})
 if unlock:
  e=environment();e['owned']={'STATE_GANSU'};effects(unlock.children,e);e['owned']=set();effects(unlock.children,e)
  rows.append({'name':'opened recovery survives loss of foothold','pass':entry('recovery',e)})
  e=environment();effects(unlock.children,e)
  rows.append({'name':'waiting does not archive or complete','pass':not {'nesnd_qe1_court_archived','nesnd_qe1_recovery_done'}&e['vars']})
  for kind in ['court','recovery']:
   n=parse(read(root/f'common/journal_entries/nesnd_qe1_{kind}.txt')).get(f'nesnd_qe1_{kind}_journal')
   rows.append({'name':kind+' no positive self-JE entry dependency','pass':not any(x.key=='has_journal_entry' for x in n.get('possible').walk())})
 return rows

before=run(B);after=run(C)
assert any(not x['pass'] for x in before)
assert all(x['pass'] for x in after)
base,cur=man(B),man(C);changed=[r for r,h in cur.items() if base.get(r)!=h]
assert len(changed)==5 and all('qe1' in r or 'qin_persia_lifecycle' in r for r in changed)
assert man(M)==base
for rel in changed:parse(read(C/rel))
docfiles=['common/decisions/japan_shinto.txt','common/journal_entries/07_japanese_religion.txt','events/meiji_restoration.txt']
dump(R/'qin-stage-checks.json',{'status':'STATIC_PASS','before':before,'after':after,'changed_scripts':changed,'native_sources':[{'file':str(G/p),'sha256':sha(G/p)} for p in docfiles],'engine_verified':False})
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'reports/integrity-recheck-20261102/global-final/tiger-load-order.conf'),'--json',str(C)]
p=subprocess.run(cmd,capture_output=True);(R/'qin-stage-tiger.json').write_bytes(p.stdout);(R/'qin-stage-tiger.stderr.txt').write_bytes(p.stderr)
a=json.loads(p.stdout);old=json.loads(read(W/'reports/integrity-recheck-20261102/global-final/tiger_raw.json'))
def key(x):return x['severity'],x['key'],x['message'],tuple((n.get('from'),n.get('path'),n.get('line')) for n in x['locations'])
oldc=collections.Counter(map(key,old));added=[]
for x in a:
 if oldc[key(x)]:oldc[key(x)]-=1
 else:added.append(x)
dump(R/'qin-stage-tiger-delta.json',{'counts':dict(collections.Counter(x['severity'] for x in a)),'added':added,'engine_verified':False})
assert not added,added
print(json.dumps({'source_condition_checks':len(after),'before_failed':[x['name'] for x in before if not x['pass']],'Tiger_added':len(added),'game_launched':False}))
