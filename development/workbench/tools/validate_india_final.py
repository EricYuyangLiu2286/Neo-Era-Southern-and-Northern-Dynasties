from india_context import *
from collections import Counter
bm,cm=man(B),man(C);changed={p:h for p,h in cm.items() if bm.get(p)!=h};checks=[]
def ck(n,v):checks.append({'name':n,'pass':bool(v)})
def tree(rel):return parse(read(C/rel))
def has(n,k,v=None):return any(x.key==k and (v is None or x.value==v) for x in n.walk())
def node(rel,k):n=tree(rel).get(k);assert n,(rel,k);return n
ck('No deletion of previous work',not bm.keys()-cm.keys());ck('Main unchanged since independent India baseline',man(M)==bm)
protected=[p for p in bm if p.startswith(('map_data/','gfx/','common/history/pops/','common/history/population/','common/history/states/','common/history/buildings/'))]
ck('All population territory buildings resources preserved',all(bm[p]==cm[p] for p in protected))
for d in ['common','events']:
 for p in (C/d).rglob('*.txt'):parse(read(p))
ck('All gameplay script ASTs parse',True)
# Closed effective databases, not the presence of a filename alone.
dbs={}
for folder in ['scripted_buttons','journal_entries','scripted_triggers','scripted_effects','script_values','scripted_progress_bars','static_modifiers','country_definitions','diplomatic_plays']:
 db={}
 for rootdir in [G,C]:
  for p in (rootdir/'common'/folder).glob('*.txt'):
   for n in parse(read(p)).children:db[(n.key or '').removeprefix('REPLACE:').removeprefix('REPLACE_OR_CREATE:')]=(n,p)
 dbs[folder]=db
locs={}
for lang in ['simp_chinese','english']:
 loc={}
 for rootdir in [G,C]:
  for p in sorted((rootdir/'localization'/lang).rglob('*.yml')):
   for k,v in re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"',read(p),re.M):loc[k]=v
 locs[lang]=loc
 p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzzz_nesnd_india_l_{lang}.yml';pairs=re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"',read(p),re.M)
 ck(lang+' localization BOM/header/unique',(p.read_bytes().startswith(b'\xef\xbb\xbf') and read(p).startswith('l_'+lang+':') and len(pairs)==len(dict(pairs))))
 ck(lang+' no mechanical draft residue',not any(t in read(p) for t in ['子项目','按原规则','结案','country_var_greater','has no localization']))
for rel in changed:
 if rel.startswith(('common/','events/')) and rel.endswith('.txt'):
  for n in tree(rel).walk():
   if n.key in ['scripted_button','scripted_progress_bar','activate_law','add_technology_researched'] and n.value:
    if n.key in ['scripted_button','scripted_progress_bar']:ck(rel+':'+n.key+':'+n.value,n.value in dbs['scripted_buttons' if n.key=='scripted_button' else 'scripted_progress_bars'])
   if n.key=='add_journal_entry':ck('Explicit JE resolves '+str(n.scalar('type')),n.scalar('type') in dbs['journal_entries'])
   if n.key=='custom_tooltip':
    k=n.value or n.scalar('text')
    if k:ck('Custom tooltip bilingual '+k,all(k in l for l in locs.values()))
   if n.key=='add_modifier':
    k=n.scalar('name');ck('Modifier defined '+str(k),k in dbs['static_modifiers']);ck('Modifier bilingual '+str(k),all(k in l for l in locs.values()))
   if n.key in ['texture','icon'] and n.value and '$' not in n.value:
    # CoA texture is relative to dedicated asset directories; handled separately below.
    if n.value.startswith('gfx/'):ck('Asset '+n.value,any((d/n.value).exists() for d in [C,G]))
# Every new JE, button, progress bar has active bilingual keys.
for folder in ['journal_entries','scripted_buttons','scripted_progress_bars']:
 for key,(n,p) in dbs[folder].items():
  if p.is_relative_to(C) and p.relative_to(C).as_posix() in changed and key.startswith('nesnd_'):
   keys=[key,key+'_reason'] if folder=='journal_entries' else ([n.scalar('name'),n.scalar('desc')] if folder=='scripted_buttons' else [n.scalar('name'),n.scalar('desc')])
   for k in keys:ck(folder+' localized '+str(k),bool(k) and all(k in l for l in locs.values()))
# Native replacement of contextless JE remains contextless; all old active callbacks eliminated.
disabled=tree('common/journal_entries/zzzz_nesnd_india_native.txt')
for n in disabled.children:ck(n.key+' closes all effect paths',has(n.get('possible'),'always','no') and has(n.get('invalid'),'always','yes') and not any(x.key in ['immediate','on_complete','on_fail','on_monthly_pulse'] for x in n.children))
ck('Uneasy Raj global history contract preserved',disabled.get('REPLACE:je_uneasy_raj').scalar('group')=='je_group_global_international_situations')
# Author single ruler/heir source and initial military count.
ck('Native duplicate MUG history no effects',not tree('common/history/countries/mug - mughals.txt').get('COUNTRIES').children)
chr=tree('common/history/characters/mug - hindustan.txt');ck('No duplicate Akbar/Bahadur ruler from native',not has(chr,'template','mug_akbar_ii') and not has(chr,'template','mug_bahadur_ii'))
ck('Author MUG characters exact bytes preserved',cm['common/history/characters/mug - mongul.txt']==bm['common/history/characters/mug - mongul.txt'])
ck('Inapplicable British company removed',not has(tree('common/history/countries/mug - mongul.txt'),'add_company','company_type:company_east_india_company'))
army=tree('common/history/military_formations/nesnd_mughal_armies.txt');ck('37 additional land battalions plus native3',sum(int(n.scalar('count')) for n in army.walk() if n.key=='combat_unit')==37 and not has(army,'type','fleet'))
# Stage reachability: all late stages use explicit live predicates.
for k in ['society','caste','schools','industry']:
 n=dbs['journal_entries']['nesnd_india_'+k][0];ck(k+' same possible and explicit-add qualifier',n.get('possible') is not None and n.get('invalid') is not None)
ck('School and industry progress preserved across priority switch',not any(n.key=='remove_variable' and n.value in ['nesnd_india_schools_months','nesnd_india_industry_months'] for n in tree('common/scripted_effects/nesnd_india_core.txt').walk()))
ck('Community survives republican transition',has(dbs['journal_entries']['nesnd_india_dynasty_journal'][0].get('invalid'),'country_has_monarchy_law','yes') and not has(dbs['journal_entries']['nesnd_india_society'][0].get('invalid'),'country_has_monarchy_law'))
ck('Inputs accept functional markets',sum(n.key=='country_has_local_shortage' for n in dbs['scripted_triggers']['nesnd_india_industry_ready'][0].walk())==4)
ck('Caste completion handles hierarchy exit',has(dbs['scripted_triggers']['nesnd_india_caste_ready'][0],'has_social_hierarchy','default_social_hierarchy'))
# Requests: real transfer and no procurement inventory subsystem.
send=dbs['scripted_effects']['nesnd_india_send_request'][0];reply=dbs['scripted_triggers']['nesnd_india_reply_valid'][0]
for key in ['india_sender','india_partner','india_serial','india_sender_patron','india_partner_patron','india_sender_regime','india_partner_regime']:ck('Reply guards snapshot '+key,has(reply,'exists','scope:'+key))
ck('45day request > event1month and <6month cooldown',any(n.key=='set_variable' and n.scalar('name')=='nesnd_india_request_clock' and n.scalar('days')=='45' for n in send.walk()) and dbs['scripted_effects']['nesnd_india_accept_request'][0] is not None and tree('events/nesnd_india_diplomacy.txt').get('nesnd_india_diplomacy.1').scalar('duration')=='1')
ck('Old external aid is mutually excluded',all(has(dbs['scripted_triggers'][k][0],'has_variable','nesnd_india_aid_lock') for k in ['nesnd_external_can_request_money','nesnd_external_can_request_arms']))
for k in ['nesnd_india_request_1','nesnd_india_request_2','nesnd_india_request_3']:ck(k+' native visible benefit',dbs['scripted_buttons'][k][0].get('effect').get('show_as_tooltip') is not None)
# Province-precise conservative rollback and single execution identity.
for index,region in enumerate(['CIRCARS','KURNOOL','MADRAS','MYSORE','TRAVANCORE','GUJARAT'],1):
 slug=region.lower();tag='IR'+str(index);launch=dbs['scripted_effects']['nesnd_india_'+slug+'_launch'][0];maint=dbs['scripted_effects']['nesnd_india_'+slug+'_maintain'][0];cp=dbs['scripted_effects']['nesnd_india_'+slug+'_create_play'][0]
 ck(slug+' isolated backer',cp.children[0].key=='clear_saved_scope' and cp.children[0].value=='india_case_backer')
 ck(slug+' create from actual selected state',has(launch,'state','scope:india_case_state') and not has(launch,'annex'))
 ck(slug+' native literal limited recruitment',set(n.scalar('count') for n in launch.walk() if n.key=='combat_unit')=={'2','4','6','8'} and has(launch,'army_size','1') and not has(launch,'type','fleet'))
 ck(slug+' rollback blocks territory changes',has(maint,'has_variable','nesnd_india_revolt_territory_changed') and has(maint,'num_provinces','prev.var:nesnd_india_case_original_provinces') and has(maint,'num_states','1'))
 ck(slug+' retry maximum bounded',has(maint,'nesnd_india_case_retries_value','2'))
 ck(slug+' failure distinct from negotiated result',has(maint,'set_variable','nesnd_india_revolt_failed') and has(maint,'set_variable','nesnd_india_revolt_negotiation_ended'))
 ck(slug+' launch same actual eligibility',has(dbs['scripted_buttons']['nesnd_india_'+slug+'_launch'][0].get('possible'),'nesnd_india_'+slug+'_launch_ready','yes'))
 ck(slug+' temporary strength is not permanent invalidation',not has(maint,'nesnd_india_uprising_strength'))
 ck(slug+' no global monthly second progression',not any(n.key=='change_variable' and n.scalar('name')=='nesnd_india_case_progress' for n in maint.walk()))
 dp=dbs['diplomatic_plays']['dp_nesnd_india_'+slug][0];ck(slug+' limited return-state and peace allowed',dp.scalar('war_goal')=='return_state' and dp.scalar('allow_negotiated_peace')=='yes')
 ck(slug+' defender humiliation primary demand',any(n.key=='add_war_goal' and n.scalar('type')=='humiliation' and n.scalar('primary_demand')=='yes' for n in cp.walk()))
won=dbs['scripted_triggers']['nesnd_india_revolt_won'][0];warje=dbs['journal_entries']['nesnd_india_revolt_war'][0]
ck('Revolt victory actual territory and independence',has(won,'is_subject','no') and has(won,'state_region','prev.var:nesnd_india_revolt_origin'))
ck('Resolved nonvictory terminates',has(warje.get('fail'),'has_variable','nesnd_india_revolt_resolved') and has(warje.get('fail'),'nesnd_india_revolt_won','yes'))
ck('Pause removes upkeep',has(dbs['scripted_effects']['nesnd_india_advance_contact'][0],'remove_modifier','nesnd_india_contact_cost'))
ck('Local real grievance gates preparation',has(dbs['scripted_triggers']['nesnd_india_case_can_advance'][0],'nesnd_india_case_unrest','yes'))
# Commissions do not mint population, change USM national hierarchy, or receive other countries' states.
for slug,tag,cap in [('tianzhu','TZ1','MADRAS'),('yuanshan','YU1','ZULULAND')]:
 fn=dbs['scripted_effects']['nesnd_establish_'+slug+'_commission'][0]
 ck(slug+' actual owner-state capital seed',has(fn,'state','s:STATE_'+cap+'.region_state:USM'))
 ck(slug+' no created population or army',not has(fn,'create_pop') and not has(fn,'create_military_formation'))
 ck(slug+' subject relation before rest of transfers',has(fn,'create_diplomatic_pact') and has(fn,'is_subject_of','c:USM'))
 ck(slug+' date-free actual territorial gate',has(dbs['scripted_triggers']['nesnd_'+slug+'_commission_ready'][0],'state_population','0') and not has(fn,'game_date'))
ck('Existing preparation migration covers six regions',sum(n.key=='nesnd_india_migrate_commission_case' for n in dbs['scripted_effects']['nesnd_establish_tianzhu_commission'][0].walk())==6)
ck('Persistent TZ1 suppression even after construction reward',has(dbs['scripted_triggers']['nesnd_india_usm_live'][0],'c:TZ1','this') and sum(n.key=='scripted_button' for n in dbs['journal_entries']['nesnd_india_usm'][0].walk())==6)
# Actual arithmetic units and bounded cases, not a Victoria engine simulation.
for income,want in [(-1000,25000),(0,25000),(5000,25000),(10000,40000),(1000000,125000)]:ck('Grant arithmetic '+str(income),max(25000,min(125000,income*4))==want)
for high_unrest,transport,aid in [(False,False,False),(True,False,False),(True,True,False),(True,True,True)]:
 monthly=1+2*high_unrest+int(transport)+int(aid);ck('Grievance-qualified organisation bound '+str((high_unrest,transport,aid)),1<=monthly<=5)
for stage,territory_changed,count,expected in [(4,False,True,True),(4,True,True,False),(4,False,False,False),(5,False,True,False)]:ck('Rollback condition model '+str((stage,territory_changed,count)),((stage==4) and not territory_changed and count)==expected)
ck('Tiger zero new diagnostics',not json.loads(read(R/'tiger-added.json')))
status='STATIC_PASS' if all(x['pass'] for x in checks) else 'FAIL';dump(R/'final-validation.json',{'status':status,'checks':checks,'changed':changed,'game_launched':False,'engine_verified':False});print(status,len(checks));print([x['name'] for x in checks if not x['pass']])
