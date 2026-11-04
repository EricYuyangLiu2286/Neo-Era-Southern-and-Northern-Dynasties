"""Fail-fast safety check against frozen ordered Jomini AST; never executes the game.

The preview fixture deliberately does not execute save_scope_as/set_variable or
other mutations. This is the documented missing-preview-object boundary, not a
claim to implement Clausewitz. All primitive country facts are explicit inputs;
unknown syntax raises Unsupported rather than being accepted.
"""
from canon_routes_context import *
import traceback
config=json.loads((R/'batch-c-validation-current.json').read_text('utf-8'))
RUN=Path(config['run']);SNAP=Path(config['snapshot'])
report={'phase':'TEST_ONLY','scope':'C-owned frozen scripts','snapshot':str(SNAP),'checks':[],
        'semantic_boundary':'ordered source AST only; injected primitive facts; preview writes/saves do not execute; unknown nodes fail closed',
        'expected_unimplemented_dependency':config['expected_unimplemented_dependency'],'engine_run':False,
        'tiger':'NOT_RUN','mcp':'NOT_RUN','later_matrix':'NOT_RUN'}
class Unsupported(Exception):pass
class MissingObject(Exception):
 def __init__(self,target,path,line,chain):
  self.target,self.path,self.line,self.chain=target,path,line,chain
  super().__init__(f'Missing preview target {target} at {path}:{line}')
class Country:
 def __init__(self,tag,variables=None,alive=True,overlord=None,subject_type=None,can_have_subjects=True):
  self.tag=tag;self.variables=variables or {};self.alive=alive;self.overlord=overlord
  self.subject_type=subject_type;self.can_have_subjects=can_have_subjects;self.modifiers=set();self.wars=set()
 def __repr__(self):return self.tag
world={'EGY':Country('EGY'),'FRA':Country('FRA')}
world['EGY'].variables={'nesnd_egypt_investor':world['FRA'],'nesnd_egypt_independence':0,'nesnd_egypt_sponsor_mode':1,'nesnd_egypt_started':True}
saved={};defs={};texts={};owners={};chain=[];trace=[]
def clean(v):return v.strip('"') if isinstance(v,str) else v
def child(n,key):return next((x for x in n.children or [] if x.key==key),None)
def body(n):return [x for x in n.children or [] if x.key!='limit']
def resolve(token,stack):
 token=clean(token)
 if token=='this':return stack[-1]
 if token=='root':return stack[0]
 if token=='prev':return stack[-2] if len(stack)>1 else None
 if token.startswith('c:'):return world.get(token[2:])
 if token.startswith('var:'):return stack[-1].variables.get(token[4:])
 if token.startswith('scope:'):return saved.get(token[6:])
 raise Unsupported('unimplemented resolver '+str(token))
def is_subject_of(actor,target):
 while actor.overlord is not None:
  actor=actor.overlord
  if actor is target:return True
 return False
def scalar(n,stack):
 k=n.key;v=clean(n.value);cur=stack[-1]
 if k in defs and defs[k][0]=='trigger':return triggers(defs[k][1].children,stack)
 if k in ['AND','OR','NOT','NOR']:
  values=trigger_values(n.children or [],stack)
  if k=='AND':return all(values)
  if k=='OR':return any(values)
  if k=='NOT':return not all(values)
  return not any(values)
 if k in ['hidden_trigger','custom_tooltip']:
  return triggers([x for x in n.children or [] if x.key!='text'],stack)
 if k=='always':return v=='yes'
 if k=='exists':return resolve(v,stack) is not None
 if k=='has_variable':return v in cur.variables
 if k=='has_modifier':return v in cur.modifiers
 if k=='is_country_alive':return cur.alive==(v=='yes')
 if k=='is_subject':return (cur.overlord is not None)==(v=='yes')
 if k=='can_have_subjects':return cur.can_have_subjects==(v=='yes')
 if k=='is_subject_type':return cur.subject_type==v
 if k=='is_direct_subject_of':return cur.overlord is resolve(v,stack)
 if k=='is_subject_of':
  target=resolve(v,stack)
  if target is None:raise Unsupported('null is_subject_of target '+v)
  return is_subject_of(cur,target)
 if k=='has_war_with':
  target=resolve(v,stack)
  if target is None:raise Unsupported('null has_war_with target '+v)
  return target.tag in cur.wars
 if k=='this':return cur is resolve(v,stack)
 if k.startswith(('c:','var:','scope:')):
  target=resolve(k,stack)
  if n.children is not None:
   if target is None:raise Unsupported('unguarded trigger scope '+k)
   return triggers(n.children,stack+[target])
  right=resolve(v,stack)
  if n.op in ['=','?=']:return target is not None and target is right
  if n.op=='!=':return target is not right
  raise Unsupported('scope comparison '+n.op)
 raise Unsupported('trigger '+str(k))
def trigger_values(nodes,stack):
 results=[];i=0
 while i<len(nodes):
  n=nodes[i]
  if n.key=='trigger_if':
   branches=[n];i+=1
   while i<len(nodes) and nodes[i].key in ['trigger_else_if','trigger_else']:
    branches.append(nodes[i]);i+=1
   selected=None
   for branch in branches:
    lim=child(branch,'limit')
    if branch.key=='trigger_else' or triggers(lim.children if lim else [],stack):selected=branch;break
   results.append(True if selected is None else triggers(body(selected),stack))
  else:
   results.append(scalar(n,stack));i+=1
 return results

def triggers(nodes,stack):return all(trigger_values(nodes or [],stack))
def effects(nodes,stack,path):
 i=0
 while i<len(nodes):
  n=nodes[i];k=n.key;v=clean(n.value)
  if k=='if':
   branches=[n];i+=1
   while i<len(nodes) and nodes[i].key in ['else_if','else']:
    branches.append(nodes[i]);i+=1
   for branch in branches:
    lim=child(branch,'limit')
    if branch.key=='else' or triggers(lim.children if lim else [],stack):
     effects(body(branch),stack,path);break
   continue
  i+=1
  if k in defs and defs[k][0]=='effect':
   _,node,definition_path=defs[k];chain.append(k)
   effects(node.children or [],stack,definition_path);chain.pop();continue
  if k in ['hidden_effect','show_as_tooltip']:
   effects(n.children or [],stack,path);continue
  if k.startswith(('c:','var:','scope:')):
   target=resolve(k,stack)
   if target is None:
    if n.op=='?=':continue
    raise Unsupported('unguarded effect scope '+k)
   effects(n.children or [],stack+[target],path);continue
  if k=='create_diplomatic_pact':
   target_node=child(n,'country');target_key=clean(target_node.value)
   target=resolve(target_key,stack)
   line=texts[path].count('\n',0,target_node.start)+1
   trace.append({'effect':k,'actor':stack[-1].tag,'target':target_key,'target_exists':target is not None,'path':path,'line':line})
   if target is None:raise MissingObject(target_key,path,line,list(chain))
   continue
  if k in ['set_variable','change_variable','remove_variable','save_scope_as','clear_saved_scope','add_modifier','remove_modifier','trigger_event','custom_tooltip']:
   trace.append({'preview_no_mutation':k,'value':v})
   continue
  raise Unsupported('effect '+str(k))

try:
 parsed=0
 for rel,expected in config['owned_files'].items():
  p=SNAP/rel
  if sha(p)!=expected:raise RuntimeError('snapshot content mismatch '+rel)
  if p.suffix=='.txt':
   text=read(p);tree=parse(text);parsed+=1;texts[rel]=text
   kind='trigger' if rel.startswith('common/scripted_triggers/') else ('effect' if rel.startswith('common/scripted_effects/') else None)
   if kind:
    for n in tree.children or []:
     if n.key is not None:defs[n.key]=(kind,n,rel)
 report['checks'].append({'name':'owned_sha_and_ordered_parse','status':'PASS','parsed_txt':parsed,'owned_file_count':len(config['owned_files'])})
 # This is the first adversarial behavior safety case. No source reimplementation.
 key='nesnd_egypt_settle_dependence';_,node,path=defs[key];chain.append(key)
 report['fixture']={'mode':'preview with no save/write execution','root':'EGY','EGY':'alive, independent, independence=0, selected living FRA, no finish/pending/grace flags','FRA':'alive, independent, can_have_subjects=yes','saved_scopes':[],'expected':'No effect may dereference a saved target that preview has not established'}
 effects(node.children or [],[world['EGY']],path)
 report['checks'].append({'name':'egypt_zero_live_sponsor_preview','status':'PASS'})
except MissingObject as exc:
 report['status']='FAIL_STOPPED'
 report['checks'].append({'name':'egypt_zero_live_sponsor_preview','status':'FAIL','target':exc.target,'path':exc.path,'line':exc.line,'source_function_chain':exc.chain,'reason':'save_scope_as is not an execution guarantee during preview; pact target is read without an exists branch'})
 report['first_material_failure']=report['checks'][-1]
 report['trace']=trace
except Unsupported as exc:
 report['status']='NOT_RUN_UNSUPPORTED_NODE';report['unsupported']=str(exc);report['trace']=trace
except Exception as exc:
 report['status']='FAIL_SETUP_OR_PARSE';report['error']=repr(exc);report['traceback']=traceback.format_exc()
else:report['status']='PREVIEW_CASE_PASS'
report['later_matrix']='NOT_RUN: stop at first material failure' if report['status']=='FAIL_STOPPED' else report['later_matrix']
dump(RUN/'first-stage-results.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if report['status'].startswith('FAIL') else 0)
