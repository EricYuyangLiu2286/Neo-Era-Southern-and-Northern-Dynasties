"""Independent AST-subset tests. NOT a Jomini engine; unknown AST raises.
Native migration is a synchronous fixture callback. Does not prove engine timing.
"""
from pathlib import Path
import sys,json,copy,hashlib,math,operator
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
M=Path.cwd(); R=Path(__file__).parent
paths=['common/scripted_effects/nesnd_diaspora.txt','common/scripted_triggers/nesnd_diaspora.txt','common/scripted_progress_bars/nesnd_diaspora.txt','common/journal_entries/nesnd_diaspora.txt','common/scripted_effects/nesnd_american_restoration.txt','common/scripted_triggers/nesnd_south_settlement.txt']
E=parse((M/paths[0]).read_text('utf-8-sig'))
class VM:
 def __init__(self, tree=E): self.e=tree; self.g={};self.l={};self.b={'nesnd_diaspora_batch_bar':0,'nesnd_diaspora_total_bar':0};self.countries=[];self.chosen=0;self.route_valid=False;self.effective=None;self.jes=0
 def obj(self,s,c):
  if s=='this':return c
  if s.startswith('global_var:'):return self.g[s[11:]]
  raise AssertionError('unknown scope '+s)
 def v(self,s,c):
  if s=='total_size':return c['size']
  for prefix,d in [('local_var:',self.l),('global_var:',self.g),('var:',c.get('vars',{}))]:
   if s.startswith(prefix):
    tail=s[len(prefix):]
    if '.' in tail:
     head,tail=tail.split('.',1); return self.v(tail,d[head])
    return d[tail] # MISSING MUST ERROR
  return float(s)
 def value(self,n,c):
  if n.children is None:return self.v(n.value,c)
  z=0
  for a in n.children:
   if a.key=='value':z=self.value(a,c)
   elif a.key in ('add','subtract','multiply','divide','max','min'):
    q=self.value(a,c); z={'add':lambda:z+q,'subtract':lambda:z-q,'multiply':lambda:z*q,'divide':lambda:z/q,'max':lambda:min(z,q),'min':lambda:max(z,q)}[a.key]()
   elif a.key=='floor':z=math.floor(z)
   elif a.key=='every_scope_state':
    for st in c['states']: z+=self.value(a,st)
   elif a.key=='every_scope_pop':
    for pop in c['pops']:
     if self.cond(a.get('limit'),pop):z+=self.value(type(a)(None,children=[x for x in a.children if x.key!='limit']),pop)
   else:raise AssertionError('unknown value AST '+str(a.key))
  return z
 def cond(self,n,c):
  z=[]
  for a in n.children or []:
   if a.key=='has_variable':z.append(a.value in c['vars'])
   elif a.key=='has_global_variable':z.append(a.value in self.g)
   elif a.key=='NOT':z.append(not self.cond(a,c))
   elif a.key=='nesnd_diaspora_native_pop':z.append(c.get('native',False) and c.get('size',0)>=1)
   elif a.key=='nesnd_diaspora_route_valid':z.append(self.route_valid)
   elif a.key=='exists':z.append(a.value[11:] in self.g and self.g[a.value[11:]] is not None)
   elif a.key.startswith(('var:','local_var:','global_var:')) or a.key=='total_size':z.append({'=':operator.eq,'>':operator.gt,'<=':operator.le,'>=':operator.ge}[a.op](self.v(a.key,c),self.v(a.value,c)))
   elif a.key.startswith('scripted_bar_progress('):z.append(self.b[a.key.split('(')[1][:-1]]>=self.v(a.value,c))
   else:raise AssertionError('unknown condition AST '+str(a.key))
  return all(z)
 def run(self,n,c=None):
  if c is None:c={'vars':{}}
  branch=False
  for a in n.children or []:
   k=a.key
   if k=='limit':continue
   if k in ('if','else_if','else'):
    take= (k=='if' or not branch) and (k=='else' or self.cond(a.get('limit'),c))
    if k=='if':branch=False
    if take:self.run(a,c);branch=True
   elif k in ('set_variable','set_global_variable','set_local_variable','change_variable','change_global_variable','change_local_variable','remove_variable','remove_global_variable'):
    d=self.g if 'global' in k else self.l if 'local' in k else c['vars']
    name=a.value if a.value else a.scalar('name')
    if k.startswith('remove'):d.pop(name,None)
    elif k.startswith('set'): d[name]=True if a.value else (c if a.scalar('value')=='this' else self.value(a.get('value'),c))
    else:
     assert name in d,'change missing variable '+name
     for field,sign in [('add',1),('subtract',-1)]:
      if a.get(field):d[name]+=sign*self.value(a.get(field),c)
   elif k=='set_bar_progress':self.b[a.scalar('name')]=self.value(a.get('value'),c)
   elif k.startswith('global_var:'):self.run(a,self.obj(k,c))
   elif k=='every_scope_pop':
    for pop in list(c['pops']):
     if self.cond(a.get('limit'),pop):self.run(a,pop)
   elif k=='nesnd_diaspora_count_departure':
    clone=copy.deepcopy(self.e.get(k));name=a.scalar('COUNT')
    for q in clone.walk():
     if q.value=='$COUNT$':q.value=name
    self.run(clone,c)
   elif k=='nesnd_diaspora_choose_route':self.chosen+=1 # selector separate fixture
   elif k=='add_contextless_journal_entry':self.jes+=1
   elif k in ('move_pop','move_partial_pop'):
    dest=self.obj(a.value if k=='move_pop' else a.scalar('state'),c)
    amount=c['size'] if k=='move_pop' else self.value(a.get('population'),c)
    actual=min(c['size'],amount) if self.effective is None else min(c['size'],self.effective)
    c['size']-=actual;dest['received']=dest.get('received',0)+actual
   elif self.e.get(k):self.run(self.e.get(k),c)
   else:raise AssertionError('unknown effect AST '+str(k))
 def transfer(self,size,due,effective=None):
  origin={'vars':{'nesnd_diaspora_due':due}}
  p={'size':size,'native':True};st={'pops':[p]};dest={}
  self.g.update(nesnd_diaspora_pop=p,nesnd_diaspora_origin=origin,nesnd_diaspora_departure=st,nesnd_diaspora_destination=dest,nesnd_diaspora_remaining=due)
  self.effective=effective;self.run(self.e.get('nesnd_diaspora_move'))
  return due-origin['vars']['nesnd_diaspora_due'],dest.get('received',0)
rows=[]
def check(name,fn):
 try:fn();rows.append({'test':name,'pass':True})
 except Exception as ex:rows.append({'test':name,'pass':False,'detail':repr(ex)})
def same(a,b):assert a==b,(a,b)
for size,due,eff,expected in [(1000,15,None,15),(15,1000,None,15),(100,100,None,100),(100,15,0,0),(100,15,7,7),(1,1,None,1)]:
 check(f'move size={size} due={due} effective={eff}',lambda s=size,d=due,e=eff,x=expected:same(VM().transfer(s,d,e),(x,x)))
def concurrent():
 v=VM();a={'vars':{},'states':[{'pops':[{'native':True,'size':101},{'native':False,'size':10000}]}]};b={'vars':{},'states':[{'pops':[{'native':True,'size':42}]}]}
 v.run(E.get('nesnd_diaspora_register'),a);v.run(E.get('nesnd_diaspora_register'),b);v.run(E.get('nesnd_diaspora_register'),a)
 same((v.g['nesnd_diaspora_total'],v.g['nesnd_diaspora_remaining'],v.jes),(71,71,1))
check('actual register AST: 50% floor, two nations, duplicate rejection, one JE',concurrent)
def week(valid,bar,expected_choose,expect_move):
 v=VM();v.g.update(nesnd_diaspora_open=True,nesnd_diaspora_total=100,nesnd_diaspora_remaining=100);v.route_valid=valid;v.b['nesnd_diaspora_batch_bar']=bar
 if expect_move:
  origin={'vars':{'nesnd_diaspora_due':100}};p={'size':100,'native':True};v.g.update(nesnd_diaspora_origin=origin,nesnd_diaspora_pop=p,nesnd_diaspora_departure={'pops':[p]},nesnd_diaspora_destination={})
 v.run(E.get('nesnd_diaspora_week'));same(v.chosen,expected_choose);same(v.g['nesnd_diaspora_remaining'],0 if expect_move else 100)
for valid,bar,choose,moved in [(False,100,1,False),(False,0,1,False),(True,99,0,False),(True,100,0,True),(True,108,0,True)]:
 check(f'weekly route valid={valid} threshold={bar}',lambda v=valid,b=bar,c=choose,m=moved:week(v,b,c,m))
def mutation():
 mutant=copy.deepcopy(E);q=mutant.get('nesnd_diaspora_move').get('set_local_variable').get('value').get('max');q.key='min'
 # The native last batch cap mutation must be rejected by real AST evaluation.
 try:same(VM(mutant).transfer(1000,15),(15,15))
 except AssertionError:return
 raise AssertionError('test failed to catch uncapped last batch')
check('negative control: max->min mutation caught',mutation)
# Final-output native counter is observed, never replaced by requested amount.
def zero_snapshot():
 v=VM();c={'vars':{},'states':[{'pops':[{'native':False,'size':100000}]}]};v.run(E.get('nesnd_diaspora_register'),c)
 same((v.g,v.jes),({},0));assert 'nesnd_diaspora_due' not in c['vars']
check('zero eligible population does not create global journal/counters',zero_snapshot)

# Route predicate tests execute actual comparison/guard AST; native eligibility
# subtriggers are fixtures, with ownership/state/war relations fully evaluated.
T=parse((M/paths[1]).read_text('utf-8-sig'))
def route_eval(n,c,g):
 def term(a,c):
  k=a.key
  if k=='exists':return a.value[11:] in g and g[a.value[11:]] is not None
  if k=='always':return a.value=='yes'
  if k=='NOT':return not route_eval(a,c,g)
  if k.startswith('global_var:'):return route_eval(a,g[k[11:]],g)
  if k in ('nesnd_diaspora_can_depart','nesnd_diaspora_receiver','nesnd_diaspora_native_pop','nesnd_diaspora_american_state'):return c[k]
  if k in ('owner','state','this'):
   return (c if k=='this' else c[k]) is g[a.value[11:]]
  if k=='has_war_with':return g[a.value[11:]]['id'] in c['wars']
  raise AssertionError('unknown route AST '+str(k))
 out=[];branch=False
 for a in n.children or []:
  if a.key=='limit':continue
  if a.key=='trigger_if':
   branch=route_eval(a.get('limit'),c,g);out.append(route_eval(a,c,g) if branch else True)
  elif a.key=='trigger_else':out.append(route_eval(a,c,g) if not branch else True)
  else:out.append(term(a,c))
 return all(out)
def route_case(change=None):
 o={'id':'o','nesnd_diaspora_can_depart':True};h={'id':'h','nesnd_diaspora_receiver':True,'wars':set()}
 st={};dest={'nesnd_diaspora_american_state':True,'owner':h};p={'nesnd_diaspora_native_pop':True,'owner':o,'state':st}
 g=dict(zip(['nesnd_diaspora_origin','nesnd_diaspora_host','nesnd_diaspora_departure','nesnd_diaspora_destination','nesnd_diaspora_pop'],[o,h,st,dest,p]))
 if change:change(g)
 return route_eval(T.get('nesnd_diaspora_route_valid'),{},g)
check('actual route predicate: valid route',lambda:same(route_case(),True))
for missing in ['origin','host','departure','destination','pop']:
 check('missing route '+missing,lambda k=missing:same(route_case(lambda g:g.pop('nesnd_diaspora_'+k)),False))
for field in ['owner','state']:
 check('Pop invalidated '+field,lambda f=field:same(route_case(lambda g:g['nesnd_diaspora_pop'].__setitem__(f,{})),False))
check('destination changes owner',lambda:same(route_case(lambda g:g['nesnd_diaspora_destination'].__setitem__('owner',{})),False))
check('host wars with origin',lambda:same(route_case(lambda g:g['nesnd_diaspora_host']['wars'].add('o')),False))
check('origin debt/native shortage fixture',lambda:same(route_case(lambda g:g['nesnd_diaspora_origin'].__setitem__('nesnd_diaspora_can_depart',False)),False))

out={'scope':'STATIC source AST subset, migration and route selection modeled; NO ENGINE RUN','files':{p:hashlib.sha256((M/p).read_bytes()).hexdigest() for p in paths},'cases':rows}
(R/'independent-accounting-tests.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(rows,ensure_ascii=False,indent=2));assert all(r['pass'] for r in rows)
