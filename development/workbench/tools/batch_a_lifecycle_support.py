"""Strict ordered-AST lifecycle runner with explicitly injected native operations.

It executes source control flow. Native law application and callback scheduling,
calendar expiry, tag changes, and population/military operations are fixtures,
not claims about the real engine. Unsupported nodes fail loudly.
"""
from batch_a_test_support import *
import calendar
from datetime import timedelta

ON=tree('common/on_actions/nesnd_hus_registration.txt')
EVENTS=tree('events/nesnd_hus_registration.txt')
LAW_TYPES={key:Obj('law_type',key) for key in LAWS}

def bindvar(o,k,v=True):o.a['vars'].add(k);o.a['variable_values'][k]=v
def readvar(o,k):return o.a['variable_values'].get(k)
def lawful_country(w,tag='HUS',citizenship='law_cultural_exclusion',**attrs):
    o=country(tag)
    o.a.update(states=[],cultures=[],primary=[],active_laws={},is_revolutionary=False)
    o.a.update(attrs);w['countries'][tag]=o;w['objects'].append(o)
    for key in (citizenship,'law_presidential_republic'):
        group=LAWS[key].scalar('group');o.a['active_laws'][group]=Obj('law',key,owner=o,type=LAW_TYPES[key]);o.a['laws'].add(key)
    return o
def life_world(tag='HUS',citizenship='law_cultural_exclusion'):
    w={'countries':{},'regions':{},'saved':{},'globals':{},'objects':[],'timers':[],'events':[],'day':date(1836,1,15),'native_trace':[]}
    return w,lawful_country(w,tag,citizenship)

class LE(E):
    def scope(self,k,o,root,prev):
        if k is None:return None
        if '.' in k:
            first,rest=k.split('.',1);target=self.scope(first,o,root,prev)
            return self.scope(rest,target,root,o) if target is not None else None
        if k.startswith('law_type:'):return LAW_TYPES.get(k[9:])
        if k.startswith('active_law:'):return o.a.get('active_laws',{}).get(k[11:]) if o else None
        if k.startswith('var:'):return o.a.get('variable_values',{}).get(k[4:]) if o else None
        if k in ('type','capital','civil_war_origin_country'):return o.a.get(k) if o else None
        return super().scope(k,o,root,prev)
    def number(self,t,o,root,prev):
        try:return float(t)
        except (TypeError,ValueError):pass
        value=self.scope(t,o,root,prev)
        if isinstance(value,(int,float)):return value
        raise AssertionError(('missing_numeric_value',t,o))
    def expr(self,n,o,root,prev):
        k,v=n.key,n.value
        if k=='is_revolutionary':return o.a.get(k,False)==(v=='yes')
        if k in ('has_law','has_law_or_variant'):
            target=self.scope(v,o,root,prev);require(target is not None,('missing_law_argument',v,o))
            return target.name in o.a['laws']
        if k in ('var:nesnd_hus_registration_epoch',) or k.startswith(('var:','global_var:','scope:')) and n.children is None:
            a=self.scope(k,o,root,prev)
            if a is None:
                if n.op=='?=':return False
                raise AssertionError(('unguarded_value',k,o))
            try:b=float(v)
            except (TypeError,ValueError):
                b=self.scope(v,o,root,prev)
                if b is None and n.op!='?=':raise AssertionError(('unguarded_RHS',v,o))
            return self.cmp(a,n.op,b)
        if k=='country_has_primary_culture':return self.scope(v,o,root,prev) in o.a['primary']
        if k=='any_primary_culture':return any([self.block(n,q,root,o) for q in o.a['primary']])
        if k in ('nesnd_native_americas_unified',):
            # Territory/unification is the precondition owned by the next batch; explicit boundary fixture.
            return o.a.get(k,False)==(v=='yes')
        return super().expr(n,o,root,prev)

class Life(ChoiceTrace):
    def __init__(self,w,callback_timing='after',fail_activate=None):
        super().__init__(w,True);self.pred=LE(w);self.callback_timing=callback_timing;self.fail_activate=fail_activate;self.depth=0
    def value(self,t,o,root,prev):
        try:return float(t)
        except (TypeError,ValueError):pass
        if t in ('yes','no'):return t=='yes'
        value=self.pred.scope(t,o,root,prev)
        require(value is not None,('unguarded_effect_value',t,o))
        return value
    def block(self,n,o,root,prev=None):
        self.depth+=1
        require(self.depth<100,('recursive_callback',o))
        try:return super().block(n,o,root,prev)
        finally:self.depth-=1
    def due(self,n):
        d=self.w['day']
        months=int(n.scalar('months','0'))+12*int(n.scalar('years','0'))
        if months:
            y,m=divmod(d.year*12+d.month-1+months,12);m+=1;d=date(y,m,min(d.day,calendar.monthrange(y,m)[1]))
        return d+timedelta(days=int(n.scalar('days','0')))
    def timer(self,obj,name,n):
        self.w['timers']=[x for x in self.w['timers'] if not (x['obj'] is obj and x['name']==name)]
        if any(n.get(k) for k in ('days','months','years')):self.w['timers'].append({'obj':obj,'name':name,'due':self.due(n)})
    def advance(self,day):
        self.w['day']=day
        for entry in self.w['timers'][:]:
            if entry['due']<=day:
                if entry['obj'] is None:self.w['globals'].pop(entry['name'],None)
                else:entry['obj'].a['vars'].discard(entry['name']);entry['obj'].a['variable_values'].pop(entry['name'],None)
                self.w['timers'].remove(entry)
    def on(self,key,obj,target=None):
        old=self.w['saved'].get('target')
        if target is not None:self.w['saved']['target']=target
        ast=ON.get(key)
        require(ast is not None,('missing_on_action',key))
        try:
            if ast.get('trigger') is None or self.pred.block(ast.get('trigger'),obj,obj):self.block(ast.get('effect'),obj,obj)
        finally:
            if target is not None:
                if old is None:self.w['saved'].pop('target',None)
                else:self.w['saved']['target']=old
    def event(self,entry):
        o=entry['obj'];old=self.w['saved'];self.w['saved']=dict(entry['saved'])
        try:
            ast=EVENTS.get(entry['id'])
            if ast.get('trigger') is None or self.pred.block(ast.get('trigger'),o,o):self.block(ast.get('immediate'),o,o)
        finally:self.w['saved']=old
    def effect(self,n,o,root,prev):
        k,v=n.key,n.value
        if k in ('set_variable','set_global_variable'):
            name=v or n.scalar('name');value=True if n.scalar('value') is None else self.value(n.scalar('value'),o,root,prev)
            if k=='set_global_variable':self.w['globals'][name]=value;self.timer(None,name,n)
            else:bindvar(o,name,value);self.timer(o,name,n)
            self.trace.append((k,o.name,name,repr(value)));return
        if k in ('remove_variable','remove_global_variable'):
            target=None if k=='remove_global_variable' else o
            if target is None:self.w['globals'].pop(v,None)
            else:target.a['vars'].discard(v);target.a['variable_values'].pop(v,None)
            self.w['timers']=[x for x in self.w['timers'] if not (x['obj'] is target and x['name']==v)]
            return
        if k in ('change_variable','change_global_variable'):
            values=self.w['globals'] if k=='change_global_variable' else o.a['variable_values'];name=n.scalar('name')
            require(name in values,('change_missing_variable',name));values[name]+=self.value(n.scalar('add'),o,root,prev);return
        if k in ('save_scope_as','save_temporary_scope_as'):self.w['saved'][v]=o;return
        if k=='clear_saved_scope':self.w['saved'].pop(v,None);return
        if k=='save_scope_value_as':self.w['saved'][n.scalar('name')]=self.value(n.scalar('value'),o,root,prev);return
        if k=='trigger_event':
            self.w['events'].append({'id':n.scalar('id'),'due':self.due(n),'obj':o,'saved':dict(self.w['saved'])});return
        if k=='set_social_hierarchy':o.a['hierarchy']=v;self.w['native_trace'].append((k,o.name,v));return
        if k=='recalculate_pop_ig_support':self.w['native_trace'].append((k,o.name));return
        if k=='activate_law':
            wanted=self.pred.scope(v,o,root,prev);require(wanted is not None and wanted.kind=='law_type',('activation_type',v,wanted))
            if wanted.name==self.fail_activate:self.w['native_trace'].append(('activation_injected_failure',o.name,wanted.name));return
            definition=LAWS[wanted.name];group=definition.scalar('group');old=o.a['active_laws'].get(group)
            law=Obj('law',wanted.name,owner=o,type=wanted)
            if self.callback_timing=='before':self.on('nesnd_hus_hierarchy_law_activated',law)
            if old:
                on_deactivate=LAWS[old.name].get('on_deactivate')
                # Only module law hooks are interpreted. Native ordinary-law mechanics are fixture boundaries.
                if old.name.startswith('law_nesnd_hus_') and on_deactivate:self.block(on_deactivate,o,root,prev)
                o.a['laws'].discard(old.name)
            o.a['active_laws'][group]=law;o.a['laws'].add(wanted.name)
            if wanted.name.startswith('law_nesnd_hus_') and definition.get('on_activate'):self.block(definition.get('on_activate'),o,root,prev)
            if self.callback_timing=='after':self.on('nesnd_hus_hierarchy_law_activated',law)
            self.w['native_trace'].append((k,o.name,wanted.name));return
        if k=='deactivate_law':
            wanted=self.pred.scope(v,o,root,prev);require(wanted is not None,('deactivate_type',v))
            group=LAWS[wanted.name].scalar('group');current=o.a['active_laws'].get(group)
            if current and current.name==wanted.name:
                hook=LAWS[wanted.name].get('on_deactivate')
                if hook:self.block(hook,o,root,prev)
                o.a['active_laws'].pop(group,None);o.a['laws'].discard(wanted.name)
            return
        if k=='remove_modifier':
            require(v in o.a.get('modifiers',set()),('remove_absent_modifier',v));o.a['modifiers'].remove(v);return
        if k in ('every_primary_culture','every_scope_culture'):
            items=o.a['primary'][:] if k=='every_primary_culture' else o.a['cultures'][:]
            for item in items:
                if n.get('limit') is None or self.pred.block(n.get('limit'),item,root,o):self.block(SimpleNamespace(children=[q for q in n.children if q.key!='limit']),item,root,o)
            return
        if k in ('add_primary_culture','remove_primary_culture'):
            target=self.pred.scope(v,o,root,prev);require(target is not None,('primary_culture_scope',v))
            if k=='add_primary_culture' and target not in o.a['primary']:o.a['primary'].append(target)
            if k=='remove_primary_culture' and target in o.a['primary']:o.a['primary'].remove(target)
            require(bool(o.a['primary']),('removed_last_primary',o));return
        if k=='change_tag':
            old=o.name;self.w['countries'].pop(old,None);o.name=v;self.w['countries'][v]=o
            self.on('nesnd_hus_hierarchy_country_formed',o);return
        if k in ('custom_tooltip','show_as_tooltip'):return
        if k in EFF or k=='hidden_effect':return super().effect(n,o,root,prev)
        target=self.pred.scope(k,o,root,prev)
        if n.children is not None and (target is not None or n.op=='?='):
            if target is not None:self.block(n,target,root,o)
            return
        raise AssertionError(('unsupported_lifecycle_AST',k,v,o))

def active_law(o,group):
    law=o.a['active_laws'].get(group);return law.name if law else None
def initialized(w,o,**kwargs):
    runner=Life(w,**kwargs);runner.call('nesnd_hus_initialize_hierarchy',o);return runner
def choose(r,o,route=1):r.call('nesnd_hus_choose_registration',o,{'CHOICE':str(route)})
def fake_revolution(r,o,tag='REV'):
    rebel=lawful_country(r.w,tag)
    rebel.a['is_revolutionary']=True;rebel.a['civil_war_origin_country']=o
    r.on('nesnd_hus_hierarchy_revolution_start',o,rebel)
    return rebel
def win_revolution(r,o,rebel,formed_first=True):
    o.a['is_country_alive']=False;r.w['countries'].pop('HUS',None)
    if not formed_first:r.on('nesnd_hus_hierarchy_civil_war_won',rebel)
    r.w['countries'].pop(rebel.name,None);rebel.name='HUS';rebel.a['is_revolutionary']=False;r.w['countries']['HUS']=rebel
    r.on('nesnd_hus_hierarchy_country_formed',rebel)
    if formed_first:r.on('nesnd_hus_hierarchy_civil_war_won',rebel)
    return rebel
