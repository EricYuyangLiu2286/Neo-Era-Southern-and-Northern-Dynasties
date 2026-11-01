"""Narrow source-span edits; never serialize the whole PDX tree or edit the game."""
from pathlib import Path
import sys, json, hashlib, shutil, difflib, textwrap
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
B=W/'backups/pre-change-button-guard-fix-20261101T093152Z/mod'
C=W/'exports/button-guards-20261101-a'; R=W/'reports/button-guards-20261101'
sys.path.insert(0,str(S/'scripts'))
from pdx import parse
def manifest(p): return {f.relative_to(p).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in p.rglob('*') if f.is_file()}
assert manifest(M)==manifest(B),'Main changed after backup'
assert not C.exists(); shutil.copytree(M,C); R.mkdir(parents=True,exist_ok=False)
shutil.copytree(S,R/'skill-before')
def read(rel): return (C/rel).read_text('utf-8-sig')
def write(rel,s):
 p=C/rel; old=p.read_bytes() if p.exists() else b''
 p.parent.mkdir(parents=True,exist_ok=True)
 p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.replace('\r\n','\n').replace('\n','\r\n' if b'\r\n' in old else '\n').encode('utf-8'))
def select(s,path):
 n=parse(s)
 for key in path: n=n.get(key); assert n is not None,path
 return n
def edit(rel,path,fn):
 s=read(rel); n=select(s,path); s=s[:n.start]+fn(s[n.start:n.end],n)+s[n.end:]; parse(s);write(rel,s)
def inner(block): return block[block.index('{')+1:block.rfind('}')].strip()
def guard(block,cond,kind='trigger'):
 key=block[:block.index('{')].strip(); body=textwrap.indent(inner(block),'        ')
 if kind=='trigger': return key+' {\n    trigger_if = {\n        limit = { '+cond+' }\n'+body+'\n    }\n    trigger_else = { always = no }\n}'
 return key+' {\n    if = {\n        limit = { '+cond+' }\n'+body+'\n    }\n}'
def wrap(rel,path,cond,kind='trigger'):edit(rel,path,lambda s,n:guard(s,cond,kind))
def replace(rel,key,s):edit(rel,[key],lambda old,n:textwrap.dedent(s).strip())

t='common/scripted_triggers/nesnd_external_triggers.txt'
wrap(t,['nesnd_external_target_valid'],'exists = var:nesnd_external_target')
for action in ('offer_money','offer_arms','request_money','request_arms'):
 wrap(t,['nesnd_external_can_'+action],'exists = var:nesnd_external_target')
wrap(t,['nesnd_external_any_legal_aid'],'exists = var:nesnd_external_target')
replace(t,'nesnd_external_request_valid','''
nesnd_external_request_valid = {
    trigger_if = {
        limit = { exists = scope:nesnd_external_requester }
        is_country_alive = yes
        NOT = { has_global_variable = nesnd_south_settled }
        scope:nesnd_external_requester = {
            trigger_if = {
                limit = { exists = var:nesnd_external_pending exists = var:nesnd_external_target }
                is_country_alive = yes is_at_war = no has_journal_entry = nesnd_external_policy
                NOT = { has_variable = nesnd_external_dismissed }
                NOT = { has_variable = nesnd_external_aid_committed }
                var:nesnd_external_pending = root
                var:nesnd_external_target = root
                nesnd_external_target_valid = yes
                nesnd_external_pending_politics_valid = yes
            }
            trigger_else = { always = no }
        }
    }
    trigger_else = { always = no }
}''')
replace(t,'nesnd_external_pending_politics_valid','''
nesnd_external_pending_politics_valid = {
    trigger_if = {
        limit = {
            exists = var:nesnd_external_target
            exists = var:nesnd_external_requester_sponsor
            exists = var:nesnd_external_receiver_sponsor
        }
        trigger_if = { limit = { is_subject = yes } overlord = var:nesnd_external_requester_sponsor }
        trigger_else = { this = var:nesnd_external_requester_sponsor }
        var:nesnd_external_target = {
            trigger_if = { limit = { is_subject = yes } overlord = prev.var:nesnd_external_receiver_sponsor }
            trigger_else = { this = prev.var:nesnd_external_receiver_sponsor }
        }
    }
    trigger_else = { always = no }
}''')
# Named-country branches must fail safely when that country disappears.
edit(t,['nesnd_external_any_partner_available'],lambda s,n:s.replace(
 'exists = c:FRA c:FRA = { is_country_alive = yes } NOT = { has_war_with = c:FRA }',
 'trigger_if = { limit = { exists = c:FRA } c:FRA = { is_country_alive = yes } NOT = { has_war_with = c:FRA } } trigger_else = { always = no }').replace(
 'exists = c:HUS c:HUS = { is_country_alive = yes } NOT = { has_war_with = c:HUS }',
 'trigger_if = { limit = { exists = c:HUS } c:HUS = { is_country_alive = yes } NOT = { has_war_with = c:HUS } } trigger_else = { always = no }').replace(
 'exists = c:USM c:USM = { is_country_alive = yes } NOT = { has_war_with = c:USM }',
 'trigger_if = { limit = { exists = c:USM } c:USM = { is_country_alive = yes } NOT = { has_war_with = c:USM } } trigger_else = { always = no }').replace(
 'exists = c:SIH c:SIH = { is_country_alive = yes } NOT = { has_war_with = c:SIH }',
 'trigger_if = { limit = { exists = c:SIH } c:SIH = { is_country_alive = yes } NOT = { has_war_with = c:SIH } } trigger_else = { always = no }'))
wrap('common/scripted_effects/nesnd_external_effects.txt',['nesnd_external_send_request'],'nesnd_external_target_valid = yes','effect')

b='common/scripted_buttons/nesnd_external_buttons.txt'
for suffix,tag in [('wu','USM'),('sih','SIH'),('hus','HUS'),('fra','FRA')]:
 key='nesnd_external_choose_'+suffix
 wrap(b,[key,'possible'],'exists = c:'+tag)
 condition=inner(read(b)[select(read(b),[key,'possible']).start:select(read(b),[key,'possible']).end])
 wrap(b,[key,'effect'],condition,'effect')
for action in ('offer_money','offer_arms','request_money','request_arms'):
 wrap(b,['nesnd_external_'+action,'effect'],'nesnd_external_can_'+action+' = yes','effect')
wrap(b,['nesnd_external_mysore','effect'],'exists = c:USM exists = s:STATE_MYSORE.region_state:USM','effect')
s=read(b).replace('var:nesnd_external_idle_weeks >=','nesnd_external_idle_weeks_value >=');write(b,s)
write('common/script_values/nesnd_external_preview_values.txt','''# Zero idle weeks means no AI abandonment before the first review.
nesnd_external_idle_weeks_value = {
    value = 0
    if = { limit = { has_variable = nesnd_external_idle_weeks } add = var:nesnd_external_idle_weeks }
}
''')

e='events/nesnd_external_events.txt'
for num in (2,3,5,6):
 key='nesnd_external.'+str(num)
 # Guard every option phase, rather than trusting visibility or delayed-event creation.
 wrap(e,[key,'option','trigger'],'nesnd_external_request_valid = yes')
 s=read(e); event=select(s,[key]); opt=event.get('option'); trig=opt.get('trigger'); condition=inner(s[trig.start:trig.end])
 keep={'name','trigger','ai_chance'}; effects=[n for n in opt.children if n.key not in keep]
 start,end=effects[0].start,effects[-1].end
 block='if = {\n    limit = { '+condition+' }\n'+textwrap.indent(s[start:end],'    ')+'\n}'
 s=s[:start]+block+s[end:];write(e,s)
 # ai_chance can be evaluated outside option.trigger; retain its original weights.
 s=read(e); ai=select(s,[key,'option','ai_chance']); patches=[]
 for n in ai.all('modifier'):
  trig=n.get('trigger'); patches.append((trig.start,trig.end,guard(s[trig.start:trig.end],'exists = scope:nesnd_external_requester')))
 for a,z,x in sorted(patches,reverse=True):s=s[:a]+x+s[z:]
 write(e,s)
 # Declining an already-cancelled request is an idempotent no-op.
 edit(e,[key],lambda s,n:s.replace('scope:nesnd_external_requester ?= { nesnd_external_clear_request = yes }','scope:nesnd_external_requester ?= { if = { limit = { exists = var:nesnd_external_pending } if = { limit = { var:nesnd_external_pending = root } nesnd_external_clear_request = yes } } }'))
 edit(e,[key],lambda s,n:s[:s.index('{')+1]+'\n cancellation_trigger = { NOT = { nesnd_external_request_valid = yes } }'+s[s.index('{')+1:])

# Scope writes do not establish preview scopes. Preserve the already-measured values.
for rel,key,scope,vars_ in [
 ('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_land_display','nesnd_land_display_country',['cne_landreform_completion_tracker','cne_landreform_failure_tracker']),
 ('common/scripted_effects/nesnd_presentation_effects.txt','nesnd_refresh_south_display','nesnd_south_display_country',[]),
 ('common/scripted_effects/nesnd_tenasserim.txt','nesnd_ten_display','nesnd_ten_display_country',['nesnd_ten_score','nesnd_ten_good_months']),
 ('common/scripted_effects/nesnd_phi_finance.txt','nesnd_phi_display','nesnd_phi_display_country',['nesnd_phi_score','nesnd_phi_good_months'])]:
 def protect_display(s,n):
  local=parse(s).children[0]; save=local.get('save_scope_as'); tail=s[save.end:s.rfind('}')].strip()
  if vars_:
   condition='scope:'+scope+' = { '+' '.join('has_variable = '+v for v in vars_)+' }'
   tail='if = { limit = { '+condition+' }\n'+textwrap.indent(tail,'    ')+'\n}'
  return s[:save.end]+'\n    if = { limit = { exists = scope:'+scope+' }\n'+textwrap.indent(tail,'        ')+'\n    }\n}'
 edit(rel,[key],protect_display)

t='common/scripted_triggers/nesnd_tenasserim.txt'
for key in ['nesnd_ten_healthy','nesnd_ten_can_build','nesnd_ten_can_train']:
 wrap(t,[key],'exists = s:STATE_TENASSERIM.region_state:DEI')
wrap(t,['nesnd_ten_can_compromise'],'exists = ig:ig_landowners')
wrap('common/scripted_triggers/nesnd_japan.txt',['nesnd_japan_can_send'],'exists = c:JAP')
edit('common/scripted_triggers/nesnd_japan.txt',['nesnd_japan_can_send','trigger_if'],lambda s,n:s.replace('limit = { exists = c:JAP }','limit = { exists = c:JAP }\n        c:JAP = { is_country_alive = yes }',1))
wrap('common/scripted_buttons/nesnd_japan.txt',['nesnd_japan_send_terms','effect'],'nesnd_japan_can_send = yes','effect')

# Match the same eligible IG set in possible and actual selection.
f='common/scripted_buttons/ce_french_empire_je_buttons.txt'
edit(f,['ce_french_republican_hit_unity','effect','random_interest_group','limit'],lambda s,n:s[:s.rfind('}')]+'    NOT = { has_modifier = ce_french_republican_unity }\n'+s[s.rfind('}'):])

# Reindent only changed definitions, retaining raw quoted tokens and comments.
exec((W/'tools/format_button_guard_spans_20261101.py').read_text('utf-8'))
base,final=manifest(B),manifest(C); changed=[p for p,h in final.items() if base.get(p)!=h]
assert not(set(base)-set(final))
diff=[]
for p in changed:
 parse((C/p).read_text('utf-8-sig'))
 diff+=list(difflib.unified_diff((B/p).read_text('utf-8-sig').splitlines(True) if (B/p).exists() else [],(C/p).read_text('utf-8-sig').splitlines(True),fromfile='before/'+p,tofile='after/'+p))
(R/'changes.diff').write_text(''.join(diff),encoding='utf-8')
(R/'source-changes.json').write_text(json.dumps({'base':str(B),'candidate':str(C),'changed':changed,'before':base,'after':final,'engine_executed':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'candidate':str(C),'changed_files':changed,'deletions':0},ensure_ascii=False))
