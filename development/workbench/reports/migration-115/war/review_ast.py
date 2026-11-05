"""Read-only, ordered source AST regression. Native operations are explicit fixtures.
Run: python review_ast.py. Does not launch Victoria 3; never an engine pass.
"""
from pathlib import Path
from types import SimpleNamespace as O
import sys,json,operator,hashlib
from functools import lru_cache
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
LIVE=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
OLD=W/'backups/pre-change-migration115-20261105T135256Z/mod'
OUT=Path(__file__).parent
P='nesnd_restoration_'
def obj(name,**a):return O(name=name,v={},lists={},a=a)
def body(n):return O(children=[x for x in n.children or [] if x.key not in ('limit','count')])
@lru_cache(None)
def database(base):
 db={}
 for folder in ('scripted_triggers','scripted_effects','script_values'):
  for file in (base/'common'/folder).glob('*.txt'):
   for n in parse(file.read_text(encoding='utf-8-sig')).children:db[n.key]=n
 return db
class Runtime:
 def __init__(self,base):
  self.base=base;self.db=database(base);self.saved={};self.globals={};self.plays=[];self.log=[]
 def scope(self,k,o,root,prev):
  if k is None:return None
  if '.' in k:
   first,rest=k.split('.',1);q=self.scope(first,o,root,prev)
   return self.scope(rest,q,root,o) if q is not None else None
  if k=='root':return root
  if k=='prev':return prev
  if k=='this':return o
  if k.startswith('scope:'):return self.saved.get(k[6:])
  if k.startswith('var:'):return o.v.get(k[4:]) if o else None
  if k.startswith('c:'):return self.countries.get(k[2:])
  if k in ('initiator','target','owner'):return o.a.get(k)
  if k=='nesnd_restoration_province_count':return sum(len(s.a['provinces']) for s in o.a['states'])
  try:return float(k)
  except (ValueError,TypeError):return None
 def pred(self,n,o,root,prev=None,mode='all'):
  chain=None;answers=[]
  for x in n.children or []:
   k,v=x.key,x.value
   if k=='trigger_if':
    chain=self.pred(x.get('limit'),o,root,prev)
    if chain:answers.append(self.pred(body(x),o,root,prev))
    continue
   if k in ('trigger_else','trigger_else_if'):
    assert chain is not None
    if not chain:
     chain=k=='trigger_else' or self.pred(x.get('limit'),o,root,prev)
     if chain:answers.append(self.pred(body(x),o,root,prev))
    continue
   chain=None
   if k in ('text','count'):continue
   if k=='always':a=v=='yes'
   elif k=='has_variable':a=v in o.v
   elif k=='has_variable_list':a=bool(o.lists.get(v))
   elif k=='has_global_variable':a=v in self.globals
   elif k=='exists':a=self.scope(v,o,root,prev) is not None
   elif k=='nesnd_regional_native_actor':a=o.a.get('regional',False)
   elif k=='has_journal_entry':a=v in o.a.get('journals',[])
   elif k=='is_country_alive':a=bool(o.a.get('states'))==(v=='yes')
   elif k=='is_diplomatic_play_type':a=o.a['type']==v
   elif k=='has_war_with':a=False
   elif k=='play_participant_has_war_goal_of_type_against':a=(o.name,x.scalar('type'),self.scope(x.scalar('target'),o,root,prev).name) in prev.a.get('goals',[])
   elif k=='any_scope_state':a=any(self.pred(x,s,root,o) for s in o.a.get('states',[]))
   elif k=='any_diplomatic_play':a=any(self.pred(x,p,root,o) for p in self.plays)
   elif k=='any_in_list':
    qs=o.lists.get(x.scalar('variable'),[]);tests=O(children=[z for z in x.children if z.key not in ('variable','count')]);hits=[self.pred(tests,q,root,o) for q in qs]
    a=all(hits) if x.scalar('count')=='all' else any(hits)
   elif k in ('AND','OR','NOT','NOR','custom_tooltip'):
    if k in ('AND','custom_tooltip'):a=self.pred(x,o,root,prev)
    elif k=='NOT':a=not self.pred(x,o,root,prev)
    else:
     a=self.pred(x,o,root,prev,mode='any')
     if k=='NOR':a=not a
   elif k in self.db:a=self.pred(self.db[k],o,root,prev)==(v!='no')
   elif x.children is not None:
    q=self.scope(k,o,root,prev)
    if q is None:
     if x.op=='?=':a=False
     else:raise AssertionError(('unbound scope',k))
    else:a=self.pred(x,q,root,o)
   else:
    left=self.scope(k,o,root,prev);right=self.scope(v,o,root,prev)
    if left is None or right is None:
     if x.op=='?=':a=False
     else:raise AssertionError(('missing value',k,v))
    else:a={'=':operator.eq,'?=':operator.eq,'>=':operator.ge,'>':operator.gt,'<':operator.lt,'<=':operator.le}[x.op](left,right)
   answers.append(a)
  return all(answers) if mode=='all' else any(answers)
 def call(self,k,o):self.run(self.db[k],o,o)
 def run(self,n,o,root,prev=None):
  chain=None
  for x in n.children or []:
   k,v=x.key,x.value
   if k=='if':
    chain=self.pred(x.get('limit'),o,root,prev)
    if chain:self.run(body(x),o,root,prev)
    continue
   if k in ('else','else_if'):
    assert chain is not None
    if not chain:
     chain=k=='else' or self.pred(x.get('limit'),o,root,prev)
     if chain:self.run(body(x),o,root,prev)
    continue
   chain=None
   if k=='set_variable':o.v[v or x.scalar('name')]=True if not x.get('value') else self.scope(x.scalar('value'),o,root,prev)
   elif k=='change_variable':o.v[x.scalar('name')]+=self.scope(x.scalar('add'),o,root,prev)
   elif k=='remove_variable':o.v.pop(v,None)
   elif k=='set_global_variable':self.globals[v or x.scalar('name')]=True
   elif k=='save_scope_as':self.saved[v]=o
   elif k=='clear_saved_scope':self.saved.pop(v,None)
   elif k=='clear_variable_list':o.lists[v]=[]
   elif k=='add_to_variable_list':o.lists.setdefault(x.scalar('name'),[]).append(self.scope(x.scalar('target'),o,root,prev))
   elif k=='annex':
    q=self.scope(v,o,root,prev)
    for s in q.a['states']:
     s.a['owner']=o
     for p in s.a['provinces']:p.a['owner']=o
    o.a['states']+=q.a['states'];q.a['states']=[];self.log.append((k,o.name,q.name))
   elif k=='add_journal_entry':o.a.setdefault('journals',[]).append(x.scalar('type'));self.log.append((k,o.name))
   elif k in ('every_scope_state','every_province','every_country'):
    qs=list(self.countries.values()) if k=='every_country' else o.a['states' if k=='every_scope_state' else 'provinces']
    for q in qs:
     if x.get('limit') is None or self.pred(x.get('limit'),q,root,o):self.run(body(x),q,root,o)
   elif k=='create_diplomatic_play':self.log.append((k,o.name)) # explicit native adapter: creation unsuccessful
   elif k=='add_war_goal':
    holder=self.scope(x.scalar('holder'),o,root,prev);target=self.scope(x.scalar('target_country'),o,root,prev)
    o.a.setdefault('goals',[]).append((holder.name,x.scalar('type'),target.name));self.log.append((k,holder.name,target.name))
   elif k=='random_diplomatic_play':
    for q in self.plays:
     if self.pred(x.get('limit'),q,root,o):self.run(body(x),q,root,o);break
   elif k in ('nesnd_restoration_popup','nesnd_restoration_publish_notice','nesnd_restoration_mark_resolved','nesnd_restoration_exile_people','nesnd_diaspora_register','add_modifier'):
    self.log.append((k,o.name)) # outside reviewed war control flow; effects not certified
   elif k in self.db:self.run(self.db[k],o,root,prev)
   else:
    q=self.scope(k,o,root,prev)
    if q is None:raise AssertionError(('unsupported effect',k))
    self.run(x,q,root,o)
 def fixture(self):
  h=obj('MEX',states=[],journals=[]);r=obj('NAH',states=[],journals=[]);z=obj('FRA',states=[],journals=[])
  self.countries={c.name:c for c in (h,r,z)}
  for c,role,opp in ((h,'war_host',r),(r,'rebel',h)):
   c.v.update({P+role:True,P+'opponent':opp,P+'epoch':1})
   s=obj(c.name+'state',owner=c,provinces=[]);p=obj(c.name+'province',owner=c);s.a['provinces']=[p];c.a['states']=[s]
  return h,r,z
def execute(base,case):
 r=Runtime(base);h,n,z=r.fixture();p=obj('oldplay',type='dp_nesnd_native_restoration',initiator=h,target=n);r.saved.update(target_country=n,diplomatic_play=p)
 if case.startswith('manual_'):
  if 'regional' in case:h.a['regional']=n.a['regional']=True
  winner,loser=(h,n) if 'host' in case else (n,h)
  if P+'record_enemy_land' in r.db:r.call(P+'record_enemy_land',winner)
  r.saved['loser']=loser;r.run(parse('annex = scope:loser'),winner,winner)
  r.call(P+'war_watch',winner);return P+'settlement_done' in winner.v,r.log
 if case=='after_lobby_records_both':
  source=base/'common/on_actions/nesnd_american_restoration.txt';db={x.key:x for x in parse(source.read_text(encoding='utf-8-sig')).children}
  hook=db.get('nesnd_restore_war_borders_on_load')
  if hook:r.run(hook.get('effect'),h,h)
  return bool(h.lists.get(P+'enemy_land')) and bool(n.lists.get(P+'enemy_land')),r.log
 if case=='third_party':
  if P+'record_enemy_land' in r.db:r.call(P+'record_enemy_land',h)
  r.saved['loser']=n;r.run(parse('annex = scope:loser'),z,z);r.call(P+'war_watch',h)
  return P+'external_end' in h.v and P+'settlement_done' not in h.v,r.log
 if case=='callback_after_external_terminal':h.v[P+'external_end']=True;h.v[P+'war_terminal']=4;h.v[P+'play']=p
 if case=='callback_other_play':h.v[P+'play']=obj('currentplay',type=p.a['type'],initiator=h,target=n)
 if case=='callback_wrong_pair':r.saved['target_country']=z
 if case=='callback_missing_play':r.saved.pop('diplomatic_play')
 if case=='callback_epoch_mismatch':n.v[P+'epoch']=2
 if case.startswith('callback'):
  r.call(P+'settlement',h);return bool(n.a['states']),r.log # expected rejected: target retains land
 if case=='legacy_peace_reopens':
  h.v[P+'war_terminal']=2;h.v[P+'peace_shown']=True;h.v[P+'war_dispatched']=True;r.call(P+'war_watch',h)
  return P+'war_terminal' not in h.v and len([x for x in r.log if x[0]=='create_diplomatic_play'])==1,r.log
 if case=='terminal_no_reopen':
  h.v[P+'war_terminal']=4;h.v[P+'external_end']=True;r.call(P+'war_watch',h);return not r.log,r.log
 if case=='vanished_no_proof':
  h.v.pop(P+'opponent');r.call(P+'war_watch',h);return P+'external_end' in h.v and P+'settlement_done' not in h.v,r.log
 if case=='false_receipt_is_present':
  h.v[P+'external_end']=False;r.call(P+'war_watch',h);return not r.log,r.log
 if case=='upgrade_missing_goal_no_duplicate':
  p.a['goals']=[(h.name,'wg_nesnd_restoration_settlement',n.name)];r.plays=[p]
  r.call(P+'dispatch',h);h.v.pop(P+'retry_wait',None);h.v.pop(P+'war_dispatched',None);r.call(P+'dispatch',h)
  return len(p.a['goals'])==2 and len(set(p.a['goals']))==2,r.log
 if case=='duplicate_no_reward':
  h.v[P+'play']=p;r.call(P+'settlement',h);before=len(r.log);r.call(P+'settlement',h);return not n.a['states'] and len(r.log)==before,r.log
 raise AssertionError(case)
def main():
 cases=['manual_host_no_dispatched','manual_rebel_no_dispatched','manual_regional_host_no_dispatched','manual_regional_rebel_no_dispatched','after_lobby_records_both','third_party','vanished_no_proof','legacy_peace_reopens','terminal_no_reopen','false_receipt_is_present','upgrade_missing_goal_no_duplicate','callback_after_external_terminal','callback_other_play','callback_wrong_pair','callback_epoch_mismatch','callback_missing_play','duplicate_no_reward']
 results=[]
 for case in cases:
  row={'case':case}
  for label,base in [('old',OLD),('live',LIVE)]:
   try:ok,detail=execute(base,case);row[label]={'pass':ok,'detail':detail}
   except Exception as e:row[label]={'pass':False,'harness_error':repr(e)}
  results.append(row)
 files=['common/diplomatic_plays/nesnd_american_restoration.txt','common/war_goal_types/nesnd_native_americas.txt','common/scripted_triggers/nesnd_american_restoration.txt','common/scripted_effects/nesnd_american_restoration.txt']
 report={'boundary':'STATIC AST control flow only. Native annex/creation adapters; no engine execution. Unsupported nodes fail.', 'sources':{p:hashlib.sha256((LIVE/p).read_bytes()).hexdigest() for p in files},'results':results}
 (OUT/'review-ast-results.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
 print(json.dumps(results,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
