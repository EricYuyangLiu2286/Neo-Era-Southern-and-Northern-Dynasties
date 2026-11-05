from pathlib import Path
from dataclasses import dataclass, field
from operator import eq,lt,gt
import sys, re, copy, codecs
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
P=Path.cwd()
def db(f): return parse((P/f).read_text('utf-8-sig'))
tr=db('common/scripted_triggers/nesnd_jp_development.txt')
fx=db('common/scripted_effects/nesnd_jp_development.txt')
je=db('common/journal_entries/nesnd_jp_cohesion.txt').get('nesnd_jp_cohesion')
cl=db('common/customizable_localization/nesnd_jp_cohesion.txt').get('nesnd_jp_culture_preview')
realm=db('common/scripted_effects/nesnd_jp_foreign.txt').get('nesnd_jp_new_realm')
@dataclass(eq=False)
class Obj:
    key:str
    attrs:dict=field(default_factory=dict)
    var:dict=field(default_factory=dict)
    def __repr__(self): return self.key
class Case:
    def __init__(self,mode=1,target='han',j=False):
        self.cs={name:Obj(name) for name in ('japanese','han','ce_wuu','test')}
        self.c=Obj('Japan'); self.s=Obj('Kyoto'); self.p=Obj('People'); self.je=True;self.j=j
        self.culture=self.cs['japanese' if target!='japanese' else 'ce_wuu']
        self.tag=Obj('JIM' if j else 'JAP');self.c.attrs.update(country_definition=self.tag,nesnd_jp_cohesion_value=20 if mode==1 else 80)
        self.c.var.update(nesnd_jp_statistics_ready=True,nesnd_jp_next_mode=mode,nesnd_jp_next_realm=self.tag,nesnd_jp_next_state=self.s,nesnd_jp_next_target=self.cs[target],nesnd_jp_next_source_culture=self.culture,nesnd_jp_next_pop=self.p)
        if j:self.c.var['nesnd_jp_jiangnan_policy']=True
        self.s.attrs.update(owner=self.c,state_population=100,pops=[self.p]);self.p.attrs.update(state=self.s,culture=self.culture)
        self.c.attrs['primary']=[self.culture]
    def val(self,txt,o,prev):
        if txt=='prev': return prev
        if txt.startswith('prev.'): return self.val(txt[5:],prev,None)
        if txt.startswith('var:'): return o.var.get(txt[4:])
        if txt.startswith('cu:'): return self.cs[txt[3:]]
        if txt in o.attrs: return o.attrs[txt]
        if txt in ['yes','no']: return txt=='yes'
        return float(txt)
    def block(self,n,o,prev):
        result=True;matched=False
        for c in n.children:
            k=c.key
            if k=='limit':continue
            if k=='trigger_if': matched=False
            if k in ['trigger_if','trigger_else_if','trigger_else']:
                if not matched and (k=='trigger_else' or self.block(c.get('limit'),o,prev)):
                    matched=True;result&=self.block(c,o,prev)
            else: result&=self.check(c,o,prev)
            if not result:return False
        return result
    def check(self,n,o,prev):
        k,v=n.key,n.value
        if k=='OR': return any(self.check(x,o,prev) for x in n.children)
        if k=='AND': return self.block(n,o,prev)
        if k=='NOT': return not self.block(n,o,prev)
        if k=='always':return v=='yes'
        if k=='nesnd_jp_cohesion_live':return self.je
        if k=='nesnd_jp_jiangnan_policy': return self.j and 'nesnd_jp_jiangnan_policy' in self.c.var
        if k=='nesnd_jp_drift_toward_japanese':return self.block(tr.get(k),o,prev)
        if k=='country_has_primary_culture':return self.val(v,o,prev) in o.attrs['primary']
        if k=='has_variable':return v in o.var
        if k=='exists':return self.val(v,o,prev) is not None
        if k=='any_scope_pop':return any(self.block(n,p,o) for p in o.attrs['pops'])
        if k=='is_primary_culture_of':return o in self.val(v,o,prev).attrs['primary']
        val=self.val(k,o,prev)
        if n.children is not None:
            assert val is not None, ('dereference',k)
            return self.block(n,val,o)
        return {'=':eq,'<':lt,'>':gt}[n.op](val,self.val(v,o,prev))
    def valid(self): return self.block(tr.get('nesnd_jp_culture_plan_valid'),self.c,None)
count=0
for mode,target,jiang in [(1,'han',False),(1,'ce_wuu',False),(1,'japanese',True),(2,'ce_wuu',True),(2,'japanese',False)]:
    c=Case(mode,target,jiang);assert c.valid();count+=1
    for attr in ['nesnd_jp_next_mode','nesnd_jp_next_realm','nesnd_jp_next_state','nesnd_jp_next_target','nesnd_jp_statistics_ready']+(['nesnd_jp_next_source_culture','nesnd_jp_next_pop'] if mode==1 else []):
        c=Case(mode,target,jiang);del c.c.var[attr];assert not c.valid(),attr;count+=1
    for mut in [('owner',lambda c:c.s.attrs.update(owner=Obj('other'))),('je',lambda c:setattr(c,'je',False)),('tag',lambda c:c.c.attrs.update(country_definition=Obj('new'))),('limit',lambda c:c.c.attrs.update(nesnd_jp_cohesion_value=25 if mode==1 else 75)),('empty',lambda c:c.s.attrs.update(state_population=0))]:
        c=Case(mode,target,jiang);mut[1](c);assert not c.valid(),mut[0];count+=1
    c=Case(mode,target,jiang);c.j=not jiang
    if jiang:c.c.var.pop('nesnd_jp_jiangnan_policy')
    else:c.c.var['nesnd_jp_jiangnan_policy']=True
    assert not c.valid();count+=1
    if mode==1:
        for fn in [lambda c:c.p.attrs.update(state=Obj('another_state')),lambda c:c.p.attrs.update(culture=c.cs['test']),lambda c:c.c.attrs.update(primary=[])]:
            c=Case(mode,target,jiang);fn(c);assert not c.valid();count+=1
    else:
        c=Case(mode,target,jiang);c.p.attrs.update(culture=c.cs[target]);assert not c.valid();count+=1
sett=fx.get('nesnd_jp_settle_culture_plan')
assert sett.get('if').get('limit').scalar('nesnd_jp_culture_plan_valid')=='yes'
assert not any((x.key or '').startswith('random') for x in sett.walk())
assert {x.scalar('value') for x in sett.walk() if x.key=='change_pop_culture'}=={'0.25','state.var:nesnd_jp_conversion_fraction'}
assert {x.scalar('value') for x in sett.walk() if x.key=='set_variable'}=={'nesnd_jp_conversion_fraction_japanese','nesnd_jp_conversion_fraction_jiangnan'}
plan=fx.get('nesnd_jp_prepare_culture_plan')
assert plan.get('if').get('limit').get('NOT').scalar('has_variable')=='nesnd_jp_next_mode'
assert [x.key for x in next(x for x in plan.walk() if x.key=='random_list').children]==['50','50']
high=fx.get('nesnd_jp_select_exchange'); assert [x.key for x in next(x for x in high.walk() if x.key=='random_list').children]==['70','30']
monthly=[x.key for x in fx.get('nesnd_jp_cohesion_monthly').get('if').children]
assert monthly.index('clamp_variable')<monthly.index('nesnd_jp_settle_culture_plan')<monthly.index('nesnd_jp_reset_culture_plan')<monthly.index('nesnd_jp_prepare_culture_plan')
assert realm.scalar('nesnd_jp_reset_culture_plan')==je.get('on_invalid').scalar('nesnd_jp_reset_culture_plan')=='yes'
for key in ('nesnd_jp_prepare_culture_plan','nesnd_jp_reset_culture_plan'):assert je.get('immediate').scalar(key)=='yes'
assert fx.get('nesnd_jp_bootstrap').get('if').scalar('nesnd_jp_prepare_culture_plan')=='yes'
variables={x.scalar('name') for key in ('nesnd_jp_prepare_culture_plan','nesnd_jp_select_drift','nesnd_jp_select_exchange') for x in fx.get(key).walk() if x.key=='set_variable'}
assert variables=={x.value for x in fx.get('nesnd_jp_reset_culture_plan').walk() if x.key=='remove_variable'}
assert cl.get('text').get('trigger').scalar('nesnd_jp_culture_plan_valid')=='yes'
for lang in ('english','simp_chinese'):
    data=Path(f'localization/{lang}/replace/nesnd_japan_l_{lang}.yml').read_bytes()
    assert data.startswith(codecs.BOM_UTF8)
    s=data.decode('utf-8-sig'); assert s.count("Country.GetCustom('nesnd_jp_culture_preview')")==5
    for name in ('nesnd_jp_culture_preview_state','nesnd_jp_culture_preview_none'):
        line=re.search(r'^ '+name+r':0 "([^"]+)"',s,re.M)[1]
        assert ("Var('nesnd_jp_next_state')" in line)==name.endswith('state')
print(f'Japanese preview: {count} AST-driven plan-validity cases passed; monthly order, no settlement rerolls, persisted quiet draw, original fractions and weights, 6 fields cleared, creation/migration/retirement and bilingual status references checked.')
