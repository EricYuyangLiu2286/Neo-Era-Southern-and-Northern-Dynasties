from pathlib import Path
import sys,re,itertools,codecs
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
from operator import eq,gt,le
root=Path.cwd()
game=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
report=Path('../../nesnd-workbench/reports/diaspora-39')
def script(rel):
    return parse((root/rel).read_text('utf-8-sig'))
je=script('common/journal_entries/nesnd_diaspora.txt').get('nesnd_diaspora')
bars=script('common/scripted_progress_bars/nesnd_diaspora.txt')
rates=script('common/script_values/nesnd_diaspora_laws.txt')
mods=script('common/static_modifiers/nesnd_diaspora.txt')
events=script('events/nesnd_diaspora.txt')
assert je.get('is_shown_when_inactive').scalar('always')==je.get('possible').scalar('always')=='no'
assert je.get('on_weekly_pulse').get('effect').get('scope:journal_entry').scalar('nesnd_diaspora_week')=='yes'
assert je.get('on_complete').get('hidden_effect').scalar('nesnd_diaspora_finish')=='yes'
assert not je.get('on_complete_all_involved')
batch=bars.get('nesnd_diaspora_batch_bar')
assert [n.value for n in je.all('scripted_progress_bar')]==[n.key for n in bars.children]
assert [n.scalar('is_inverted') for n in bars.children]==['yes']*2
drift=batch.get('weekly_progress').get('if')
assert drift.get('limit').scalar('nesnd_diaspora_route_valid')=='yes'
assert drift.get('add').scalar('value')=='1'
lawrows=drift.get('global_var:nesnd_diaspora_origin').all('add')
known={x.group(1) for d in [game/'common/laws',root/'common/laws'] for p in d.glob('*.txt') for x in re.finditer(r'(?m)^(?:REPLACE:)?(law_\w+)\s*=',p.read_text('utf-8-sig'))}
def rate(row,law):
    r=rates.get(row.scalar('value'))
    for cond in r.children:
        if cond.key=='value': continue
        laws={n.value.split(':')[1] for n in cond.get('limit').walk() if n.key=='has_law'}
        assert laws<=known
        if law in laws: return int(cond.scalar('value'))
    return int(r.scalar('value'))
assert len(lawrows)==2
assert 1+rate(lawrows[0],'law_ethnostate')+rate(lawrows[1],'law_autocracy')==8
assert 1+rate(lawrows[0],'law_multicultural')+rate(lawrows[1],'law_universal_suffrage')==1
assert 1+rate(lawrows[0],'law_racial_segregation')+rate(lawrows[1],'law_wealth_voting')==4
def cond(n,vals):
    k=n.key
    if k in ('text','desc'): return True
    if k=='always': return n.value=='yes'
    if k in ('has_variable','has_global_variable'): return n.value in vals
    if k and k.startswith('global_var:'): return {'>':gt,'<=':le,'=':eq}[n.op](vals[k.split(':')[1]],int(n.value))
    kids=n.children or []
    if k=='NOT': return not all(cond(c,vals) for c in kids)
    if k=='trigger_if': return all(cond(c,vals) for c in kids if c.key!='limit')
    if n.get('trigger_if'):
        branch=n.get('trigger_if')
        return cond(branch,vals) if cond(branch.get('limit'),vals) else cond(n.get('trigger_else'),vals)
    return all(cond(c,vals) for c in kids)
for total,remain,expected in [(None,None,False),(100,None,False),(0,0,False),(100,1,False),(100,0,True)]:
    d={k:v for k,v in [('nesnd_diaspora_total',total),('nesnd_diaspora_remaining',remain)] if v is not None}
    assert cond(je.get('complete'),d)==expected
for name,warkey in [('nesnd_american_restoration','nesnd_native_restoration_war'),('nesnd_regional_native_restoration','nesnd_regional_native_war')]:
    w=script(f'common/journal_entries/{name}.txt').get(warkey)
    for tag,flags,exp in [('pending',{},(False,False)),('no_play',{'nesnd_restoration_war_terminal':4},(False,True)),('peace',{'nesnd_restoration_war_terminal':2},(False,True)),('successful government',{'nesnd_restoration_war_terminal':1,'nesnd_restoration_settlement_done':1,'nesnd_restoration_war_host':1},(True,False)),('successful uprising',{'nesnd_restoration_war_terminal':1,'nesnd_restoration_settlement_done':1,'nesnd_restoration_rebel':1,'nesnd_restoration_victory':1},(True,False))]:
        assert (cond(w.get('complete'),flags),cond(w.get('fail'),flags))==exp,tag
def loc(lang):
    f=Path(f'localization/{lang}/replace/nesnd_diaspora_l_{lang}.yml'); raw=f.read_bytes()
    assert raw.startswith(codecs.BOM_UTF8)
    lines=raw.decode('utf-8-sig').splitlines();assert lines.pop(0)==f'l_{lang}:'
    pairs=[re.fullmatch(r' (\S+):0 "(.*)"',s).groups() for s in lines]
    keys=dict(pairs);assert len(keys)==len(lines)
    for k,v in pairs:
        assert v.count('[')==v.count(']')
        assert set(re.findall(r'\$(.*?)\$',v))<=set(keys)
        assert 'country var' not in v.lower()
    return keys
en,zh=loc('english'),loc('simp_chinese')
assert en.keys()==zh.keys()
need={'nesnd_diaspora','nesnd_diaspora_reason'}|{n.key for n in mods.children}
for tree in [je,bars,events]:
    need.update(n.value for n in tree.walk() if n.key in ('name','desc','text','title','custom_tooltip') and n.value)
assert need<=set(en),need-set(en)
for event in [events.get('nesnd_diaspora.1'),events.get('nesnd_diaspora.2')]:
    assert event.scalar('type')=='country_event' and event.get('option').scalar('default_option')=='yes'
assert all(m.children and len(m.children)==1 and m.children[0].value=='0.05' for m in mods.children)
print(f'UI: ordered parse; activation, pulse, finish and both bar references; law mappings checked against native/mod definitions; drift 1/4/8, missing-ledger and completion cases, ten WAR lifecycle cases, {len(en)} matching bilingual keys, BOM, loc links, 2 no-choice events and 2 country modifiers passed.')
