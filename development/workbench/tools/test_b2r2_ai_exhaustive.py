from canon_routes_context import *
import itertools,copy,traceback,time
src=(W/'tools/b2r2_b2_minimal_source_cases.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
old_scalar=scalar
def scalar(n,stack):
 k=subst(n.key);cur=stack[-1]
 if k=='in_default':return cur.in_default==(subst(n.value)=='yes')
 if k=='economic_dependence':
  target=resolve(child(n,'target').value,stack);test=child(n,'value')
  if target is None:raise Unsupported('missing dependence target')
  return cmp[test.op](cur.dependence[target.tag],x['number'](test.value,stack))
 return old_scalar(n,stack)
x['scalar']=scalar;x['ns']['scalar']=scalar
original=Path(json.loads((R/'batch-b2-repair1-freeze.json').read_text())['parent_freeze'])
oldnode=next(n for n in parse(read(original/'common/script_values/nesnd_small_diplomacy.txt')).children if n.key=='nesnd_small_reply_acceptance')
event=defs['nesnd_small_states.20'][1];opt=next(n for n in event.children if n.key=='option' and child(n,'name').value=='nesnd_canon_diplomacy.1.a');chance=child(opt,'ai_chance')
refuse=next(n for n in event.children if n.key=='option' and child(n,'name').value=='nesnd_canon_diplomacy.1.b')
a,land=fixture();f=world['FRA'];b=world['BAV'];a.overlord=f;a.dependence={'FRA':1};f.army_size=100;f.gdp=100;f.in_default=False;b.army_size=1000;b.in_default=False;b.has_revolution=False
support=treaty(a,b,'support_independence',source=b,target=a)
newraw=defs['nesnd_small_reply_acceptance_raw'];rawpoints=set();scores=set();count=0;fail=[];start=time.monotonic()
for kind,relation,default,war,has_support,dependence,army,gdp in itertools.product([5,6,7,8,9],[49,50],[False,True],[False,True],[False,True],[.7999,.8,1.2,1.2001],[.3999,.4,.5999,.6],[.3999,.4]):
 saved.clear();saved.update(canon_sender=a,canon_partner=f,canon_kind=kind);f.relations['ACE']=relation;f.in_default=default;f.wars={'GBR'} if war else set();a.treaties=[support] if has_support else [];a.dependence['FRA']=dependence;a.army_size=army*100;a.gdp=gdp*100
 old=calculate(oldnode.children,[f]);raw=val('nesnd_small_reply_acceptance_raw',f);clamped=val('nesnd_small_reply_acceptance',f)
 weight=float(child(chance,'base').value)
 for m in chance.children:
  if m.key=='modifier' and x['triggers'](child(m,'trigger').children,[f]):weight+=float(child(m,'add').value)
 count+=1;rawpoints.add(raw);scores.add(weight)
 if not(old==clamped==weight):
  fail.append({'drivers':[kind,relation,default,war,has_support,dependence,army,gdp],'original_score':old,'raw':raw,'new_clamped':clamped,'new_event_weight':weight});break
missing=[]
for mask in range(1,8):
 saved.clear();saved.update(canon_sender=a,canon_partner=f,canon_kind=6)
 for i,k in enumerate(['canon_sender','canon_partner','canon_kind']):
  if mask&(1<<i):saved.pop(k)
 old=calculate(oldnode.children,[f]);new=val('nesnd_small_reply_acceptance',f);weight=float(child(chance,'base').value)
 for m in chance.children:
  if m.key=='modifier' and x['triggers'](child(m,'trigger').children,[f]):weight+=float(child(m,'add').value)
 missing.append({'mask':mask,'old':old,'new':new,'event':weight});assert old==new==weight==0
result={'status':'FAIL_STOPPED' if fail else 'PASS_EXHAUSTIVE_SOURCE_AST_EQUIVALENCE','cases':count,'driver_product':'kinds5..9 × relations49/50 × default/war4 × actual support treaty present/absent × dependence .7999/.8/1.2/1.2001 × army .3999/.4/.5999/.6 × GDP .3999/.4','raw_points':sorted(rawpoints),'event_weights':sorted(scores),'missing_object_cases':missing,'refuse_weight_literal':child(child(refuse,'ai_chance'),'base').value,'failures':fail,'seconds':time.monotonic()-start,'boundary':'Original score ordered AST versus repair raw/clamped AST and literal event modifiers; native primitive facts are injected. No rewritten score model; actual support helper and actual ratios executed. No engine AI simulation.'}
dump(run/'b2r2-ai-exhaustive.json',result);print(json.dumps(result,ensure_ascii=False,indent=2))
