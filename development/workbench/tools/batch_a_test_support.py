"""Frozen A source matrix and actual-AST first-choice/preview interpreter.

Only tests/reports are written. Stop at the first material source failure.
Native APIs are explicit fixture boundaries; this is never an engine pass.
"""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
from datetime import date
import json, hashlib, sys, re, traceback

W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
R=W/'reports/canon-route-execution-20261104'
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse, effective_files, basekey, unquote
from test_commission_gate_behavior import Evaluator as Base, Obj
META=json.loads((R/'batch-a-test-snapshot.json').read_text(encoding='utf-8'));T=Path(META['snapshot'])

def read(p):return p.read_text(encoding='utf-8-sig')
def tree(rel):return parse(read(T/rel))
def defs(folder,roots=(G,T)):
    out={}
    for p in sorted(effective_files(roots,folder),key=lambda p:p.name.lower()):
        for n in parse(read(p)).children:
            if n.key:out[basekey(n.key)]=n
    return out
def shape(n):
    return None if n is None else (n.key,n.op,n.prefix,n.value,None if n.children is None else tuple(shape(x) for x in n.children))
def require(condition,detail):
    if not condition:raise AssertionError(detail)

TR=defs('common/scripted_triggers',(T,));EFF=defs('common/scripted_effects',(T,));LAWS=defs('common/laws')
CULT=defs('common/cultures');TRAITS=defs('common/discrimination_traits')
CULTURES={}
for k,n in CULT.items():
    traits={n.scalar('heritage'),n.scalar('language')}-{None}
    for field in ['traditions','traits']:
        if n.get(field):traits.update(n.get(field).values())
    groups={TRAITS[t].scalar('trait_group') for t in traits if t in TRAITS}-{None}
    CULTURES[k]=Obj('culture',k,traits=traits,groups=groups)

class E(Base):
    def __init__(self,w):self.w=w;self.db=TR;self.values={};self.reads=[]
    def scope(self,k,o,root,prev):
        if k.startswith('cu:'):return CULTURES.get(k[3:])
        if k.startswith('global_var:'):return self.w['globals'].get(k[11:])
        if k=='culture':return o.a.get('culture')
        return super().scope(k,o,root,prev)
    def expr(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='has_discrimination_trait':return v in o.a['traits']
        if k=='has_discrimination_trait_group':return v in o.a['groups']
        if k=='has_social_hierarchy':return o.a.get('hierarchy')==v
        if k=='has_global_variable':return v in self.w['globals']
        return super().expr(n,o,root,prev)

def country(tag,active=False):
    return Obj('country',tag,vars={'nesnd_hus_hierarchy_active'} if active else set(),variable_values={},laws=set(),hierarchy='default_social_hierarchy',is_country_alive=True)
def world():
    o=country('HUS',True);return {'countries':{'HUS':o},'regions':{},'saved':{},'globals':{},'expiries':{},'events':[]},o

class ChoiceTrace:
    """Execute the real helper AST; preview resolves effect arguments but suppresses mutation.

    This mode is the project's known precondition: writes in hidden_effect are
    not assumed to have happened before later tooltip expressions are read.
    No assumption about engine country creation/law activation is needed here.
    """
    def __init__(self,w,apply=True):self.w=w;self.apply=apply;self.pred=E(w);self.trace=[]
    def value(self,t,o,root,prev):
        try:return float(t)
        except (TypeError,ValueError):pass
        if t=='yes':return True
        if t=='no':return False
        value=self.pred.scope(t,o,root,prev)
        if value is None:raise AssertionError(('unguarded_effect_argument',t,o.name,'execute' if self.apply else 'preview'))
        self.trace.append(('read',t,repr(value)))
        return value
    def call(self,key,o,args=None):
        ast=deepcopy(EFF[key])
        for n in ast.walk():
            if n.value:
                for k,v in (args or {}).items():n.value=n.value.replace('$'+k+'$',v)
        self.block(ast,o,o)
    def block(self,n,o,root,prev=None):
        chain=None
        for x in n.children or []:
            if x.key=='if':
                chain=self.pred.block(x.get('limit'),o,root,prev)
                if chain:self.block(SimpleNamespace(children=[a for a in x.children if a.key!='limit']),o,root,prev)
            elif x.key in ('else','else_if'):
                require(chain is not None,'orphan effect else')
                if not chain:
                    selected=x.key=='else' or self.pred.block(x.get('limit'),o,root,prev)
                    if selected:self.block(SimpleNamespace(children=[a for a in x.children if a.key!='limit']),o,root,prev)
                    chain=selected
            else:
                chain=None;self.effect(x,o,root,prev)
    def effect(self,n,o,root,prev):
        k,v=n.key,n.value
        if k in EFF:
            ast=deepcopy(EFF[k]);args={q.key:q.value for q in n.children or []}
            for q in ast.walk():
                if q.value:
                    for name,arg in args.items():q.value=q.value.replace('$'+name+'$',arg)
            self.block(ast,o,root,prev);return
        if k in ('hidden_effect',):self.block(n,o,root,prev);return
        if k in ('custom_tooltip','show_as_tooltip'):return
        if k in ('set_variable','set_global_variable'):
            name=v or n.scalar('name');source=n.scalar('value');value=True if source is None else self.value(source,o,root,prev)
            self.trace.append((k,name,repr(value)))
            if self.apply:
                if k=='set_global_variable':self.w['globals'][name]=value
                else:o.a['vars'].add(name);o.a['variable_values'][name]=value
                duration={q.key:q.value for q in n.children or [] if q.key in ('days','months','years')}
                if duration:self.w['expiries'][('global' if k=='set_global_variable' else o.name,name)]=duration
            return
        if k=='change_global_variable':
            name=n.scalar('name');delta=self.value(n.scalar('add'),o,root,prev)
            # Preview need not resolve the previous LHS; the later explicit RHS read remains observable.
            if self.apply:
                require(name in self.w['globals'],('uninitialized numeric global',name));self.w['globals'][name]+=delta
            self.trace.append((k,name,delta));return
        if k=='save_scope_value_as':
            value=self.value(n.scalar('value'),o,root,prev)
            if self.apply:self.w['saved'][n.scalar('name')]=value
            return
        if k=='trigger_event':
            if self.apply:self.w['events'].append({q.key:q.value for q in n.children or []})
            return
        raise AssertionError(('unsupported_choice_AST',k))

