from qin_persia_context import *
LOCFILE=R/'localization-draft.json'
LOC=json.loads(read(LOCFILE)) if LOCFILE.exists() else {}
def loc(k,zh,en=None):LOC[k]=[zh,en or zh];return k
def flush_loc():
 dump(LOCFILE,LOC)
 for idx,lang in enumerate(['simp_chinese','english']):
  put(f'localization/{lang}/replace/zzzzzzz_nesnd_qin_persia_l_{lang}.yml','l_'+lang+':\n'+'\n'.join(' '+k+':0 "'+v[idx].replace('"',"'").replace('\n','\\n')+'"' for k,v in LOC.items()))
def append_history(rel,effect):
 p=C/rel;s=read(p);country=parse(s).children[0].children[0];assert effect not in s;s=s[:country.end-1]+'\n '+effect+' = yes\n'+s[country.end-1:];write(p,s)
def bar(key,name,lo,hi,start,parts=None,green=True):
 loc(key+'_desc',f"[JournalEntry.GetCurrentBarValue(ScriptedProgressBar.Self)|1] / {hi}")
 return f'''{key} = {{ name = {name} desc = {key}_desc min_value = {lo} max_value = {hi} start_value = {start} default_green = {'yes' if green else 'no'}
 '''+(('monthly_progress = {\n'+'\n'.join(f'add = {{ desc = {label} value = {sv} }}' for label,sv in parts)+'\n}') if parts else '')+'\n}\n'
def je(key,trigger,body,reason,extra='',inactive=None):
 loc(key,body);loc(key+'_reason',reason)
 return f'''{key} = {{
 icon = "gfx/interface/icons/invention_icons/egalitarianism.dds"
 group = je_group_historical_content
 can_revolution_inherit = yes
 is_shown_when_inactive = {{ {inactive or trigger} }}
 possible = {{ {trigger} }}
 should_be_pinned_by_default_uninvolved_or_context = yes
 weight = 1000
 {extra}
}}\n'''
def button(key,name,desc,visible,possible,effect,ai='value = 0'):
 loc(key,name);loc(key+'_desc',desc)
 return f'''{key} = {{ name = {key} desc = {key}_desc visible = {{ {visible} }} possible = {{ {possible} }} ai_chance = {{ {ai} }} effect = {{ if = {{ limit = {{ {visible} {possible} }} {effect} }} }} }}\n'''
def event(key,title,desc,options,trigger='',immediate='',placement='root'):
 loc(key+'.t',title);loc(key+'.d',desc)
 return f'''{key} = {{ type = country_event placement = {placement} duration = 3 title = {key}.t desc = {key}.d
 event_image = {{ video = "unspecific_signed_contract" }}
 '''+(f'trigger = {{ {trigger} }}\n' if trigger else '')+(f'immediate = {{ {immediate} }}\n' if immediate else '')+options+'\n}\n'
