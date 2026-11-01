"""Repair real supply-button preview failures without changing valid contract outcomes."""
from pathlib import Path
import sys,copy,json,hashlib,difflib
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
P=W/'exports/resumed-integrated-20261101-a';C=W/'exports/release-logfix-20261101-a';R=W/'reports/logfix-release-20261101'
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import Node,parse,emit,replace_spans
def N(s):return parse(s).children[0]
def render(n):
    n=copy.deepcopy(n)
    for x in n.walk():
        if x.key and any(c in x.key for c in '() '):x.key=json.dumps(x.key,ensure_ascii=False)
    return emit(n)
def gbody(children,limit,effect=False):
    k='if' if effect else 'trigger_if'
    out=[Node(k,children=[Node('limit',children=parse(limit).children)]+children)]
    if not effect:out.append(N('trigger_else = { always = no }'))
    return out
def guarded(n,limit,effect=False):return gbody([n],limit,effect)
changes={}
def edit(rel,fn):
    old=(P/rel).read_text('utf-8-sig');t=parse(old);fn(t)
    original=parse(old);edits=[]
    for a,b in zip(original.children,t.children):
        if emit(a)!=emit(b):edits.append((a.start,a.end,render(b)))
    result=replace_spans(old,edits);parse(result)
    (C/rel).write_text(result,encoding='utf-8-sig')
    changes[rel]={'blocks':[t.children[i].key for i,(a,b) in enumerate(zip(original.children,t.children)) if emit(a)!=emit(b)],'before':hashlib.sha256((P/rel).read_bytes()).hexdigest(),'after':hashlib.sha256((C/rel).read_bytes()).hexdigest()}
    return ''.join(difflib.unified_diff(old.splitlines(True),result.splitlines(True),fromfile=rel+' before',tofile=rel+' after'))
def triggers(t):
    a=t.get('nesnd_supply_partner_valid')
    a.children=gbody(a.children,'exists = var:nesnd_supply_partner exists = var:nesnd_supply_sponsor exists = var:nesnd_supply_partner_sponsor')
    a=t.get('nesnd_supply_request_valid')
    a.children=gbody(gbody(a.children,'scope:nesnd_supply_requester ?= { exists = var:nesnd_supply_pending_sponsor exists = var:nesnd_supply_sponsor exists = var:nesnd_supply_pending }'),'exists = scope:nesnd_supply_requester')
    a=t.get('nesnd_supply_trade_request_valid')
    a.children=gbody(gbody(a.children,'scope:nesnd_supply_requester ?= { exists = var:nesnd_supply_trade_pending exists = var:nesnd_supply_partner }'),'exists = scope:nesnd_supply_requester')
    for n in t.walk():
        if n.children is not None and n.key in ('scope:nesnd_supply_requester','var:nesnd_supply_partner'):n.op='?='
def effects(t):
    a=t.get('nesnd_supply_clear_legacy');a.children=[guarded(n,'has_modifier = '+n.value,True)[0] if n.key=='remove_modifier' else n for n in a.children]
    a=t.get('nesnd_supply_save_pending_sponsor');a.children=gbody(a.children,'exists = var:nesnd_supply_pending',True)
    for n in list(a.walk()):
        if n.key=='var:nesnd_supply_pending' and n.children is not None:n.op='?='
    a=t.get('nesnd_supply_refresh')
    # These comparisons can run while a JE/button is previewed, before initialization.
    for n in list(a.walk()):
        if n.key=='limit' and 'var:nesnd_supply_sponsor' in emit(n):
            n.children=gbody(n.children,'exists = var:nesnd_supply_sponsor')
            n.children[-1].children[0].value='yes'
        elif n.key=='limit' and 'var:nesnd_supply_market' in emit(n):
            n.children=gbody(n.children,'exists = var:nesnd_supply_market')
            n.children[-1].children[0].value='yes'
    # Preview uses existing score/week values, never assumes a preceding assignment ran.
    a=t.get('nesnd_supply_update_display')
    for n in a.walk():
        if n.value=='scope:nesnd_supply_display.var:nesnd_supply_score':n.value='scope:nesnd_supply_display.nesnd_supply_score_value'
        if n.value=='scope:nesnd_supply_display.var:nesnd_supply_weeks':n.value='scope:nesnd_supply_display.nesnd_supply_weeks_value'
    # save_scope_as is not executed in a tooltip; scope must be checked after it.
    a.children=[a.children[0]]+gbody(a.children[1:],'exists = scope:nesnd_supply_display',True)
def buttons(t):
    for a in t.children:
        if a.key.startswith('nesnd_supply_invite_'):
            country='c:'+a.key.rsplit('_',1)[1].upper()
            a.get('possible').children=gbody(a.get('possible').children,'exists = '+country)
            a.get('effect').children=gbody(a.get('effect').children,'exists = '+country,True)
        for n in a.walk():
            if n.key=='var:nesnd_supply_weeks':n.key='nesnd_supply_weeks_value'
    a=t.get('nesnd_supply_trade')
    a.get('possible').children=gbody(a.get('possible').children,'exists = var:nesnd_supply_partner')
    a.get('effect').children=gbody(a.get('effect').children,'exists = var:nesnd_supply_partner',True)
    for n in a.walk():
        if n.key=='var:nesnd_supply_partner' and n.children is not None:n.op='?='
def events(t):
    for a in t.children:
        if a.key not in ('nesnd_supply.1','nesnd_supply.2'):continue
        for opt in a.all('option'):
            ai=opt.get('ai_chance')
            if ai:
                for mod in ai.all('modifier'):
                    tr=mod.get('trigger')
                    if tr and 'scope:nesnd_supply_requester' in emit(tr):tr.children=gbody(tr.children,'exists = scope:nesnd_supply_requester')
            for n in opt.walk():
                if n.key=='scope:nesnd_supply_requester' and n.children is not None:n.op='?='
                if n.key in ('var:nesnd_supply_pending','var:nesnd_supply_trade_pending') and n.children is None:n.op='?='
            # Treaty checks evaluate alongside the validity predicate; guard their own operands.
            def rewrite(n):
                if n.children is None:return
                out=[]
                for x in n.children:
                    if x.key=='can_create_treaty':out+=guarded(x,'exists = scope:nesnd_supply_requester')
                    elif x.key=='create_treaty':out+=guarded(x,'exists = scope:nesnd_supply_requester',True)
                    else:rewrite(x);out.append(x)
                n.children=out
            rewrite(opt)
diff=''
for rel,fn in [('common/scripted_triggers/nesnd_supply_triggers.txt',triggers),('common/scripted_effects/nesnd_supply_effects.txt',effects),('common/scripted_buttons/nesnd_supply_buttons.txt',buttons),('events/nesnd_supply_events.txt',events)]:diff+=edit(rel,fn)
values='''# Read-only display/completion operands; do not initialize gameplay in a preview.
nesnd_supply_score_value = {
 value = 0
 if = { limit = { has_variable = nesnd_supply_score } value = var:nesnd_supply_score }
}
nesnd_supply_weeks_value = {
 value = 0
 if = { limit = { has_variable = nesnd_supply_weeks } value = var:nesnd_supply_weeks }
}
'''
(C/'common/script_values/nesnd_supply_preview_values.txt').write_text(values,encoding='utf-8-sig');parse(values)
(R/'supply-fix.diff').write_text(diff,encoding='utf-8')
(R/'supply-fix.json').write_text(json.dumps({'changes':changes,'new_readonly_values':['nesnd_supply_score_value','nesnd_supply_weeks_value'],'native_failure':'WORK/research/20261101/supply-preview-reload/native-failure-a','design_changes':False,'source_patterns':['GAME/common/scripted_triggers/00_strike_triggers.txt:2','GAME/common/scripted_effects/00_expedition_effects.txt:908','WORK/tools/build_politics_preview_e2.py']},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'changed':changes,'new_values':2},ensure_ascii=False))
