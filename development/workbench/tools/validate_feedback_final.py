from feedback_context import *
checks=[]
def ck(k,v):checks.append({'name':k,'pass':bool(v)})
def tree(rel):return parse(read(C/rel))
def node(rel,key):return tree(rel).get(key)
def has(n,key,val=None):return any(x.key==key and (val is None or x.value==val) for x in n.walk())
def frag(rel,key):s=read(C/rel);n=parse(s).get(key);return s[n.start:n.end]
a,b=man(C),man(B);changed={p:h for p,h in a.items() if b.get(p)!=h}
ck('No baseline files deleted',not b.keys()-a.keys())
ck('Population/map/building/history protected',not any(p.startswith(('map_data/','common/history/','gfx/')) for p in changed))
parsed=0
for folder in ['common','events']:
 for p in (C/folder).rglob('*.txt'):parse(read(p));parsed+=1
ck('All '+str(parsed)+' scripts parse',True)
locs={}
for lang in ['simp_chinese','english']:
 loc={}
 for p in sorted((G/'localization'/lang).rglob('*.yml'))+sorted((C/'localization'/lang).rglob('*.yml')):
  for k,v in re.findall(r'^\s*([\w.\-]+):\d*\s+"(.*)"',read(p),re.M):loc[k]=v
 locs[lang]=loc
 p=C/f'localization/{lang}/replace/zzzzzzzzzzzzz_nesnd_feedback_l_{lang}.yml'
 ck('Feedback UTF8 BOM '+lang,p.read_bytes().startswith(b'\xef\xbb\xbf'))
for rel in changed:
 if not rel.endswith('.txt') or not rel.startswith(('common/','events/')):continue
 for n in tree(rel).walk():
  if n.key=='custom_tooltip':
   k=n.value or n.scalar('text')
   if k:ck('Localized tooltip '+k,all(k in loc for loc in locs.values()))
buttons={};jes={};effects={};triggers={}
for folder,db in [('scripted_buttons',buttons),('journal_entries',jes),('scripted_effects',effects),('scripted_triggers',triggers)]:
 for p in (C/'common'/folder).glob('*.txt'):
  for n in parse(read(p)).children:db[n.key]=n
for rel in changed:
 if rel.startswith('common/journal_entries/'):
  for n in tree(rel).walk():
   if n.key=='scripted_button':ck('JE button resolves '+n.value,n.value in buttons)
future=jes['nesnd_per_future_journal'].get('complete').get('custom_tooltip')
ck('PER completion original guarded predicate',future is not None and has(future,'has_variable','nesnd_per_future_progress') and has(future,'var:nesnd_per_future_progress','100'))
econ=triggers['nesnd_per_economy_ready'].all('country_has_building_type_levels')
ck('PER canonical national buildings 10/10/5',[(n.scalar('target'),n.scalar('value')) for n in econ]==[('bt:building_cotton_plantation','10'),('bt:building_textile_mill','10'),('bt:building_railway','5')])
claims=tree('common/scripted_buttons/nesnd_per_border_claims.txt').children
ck('37 separate claim buttons',len(claims)==37)
for n in claims:
 regions=[x.key for x in n.walk() if x.key.startswith('s:STATE_')]
 ck(n.key+' fixed same region',len(regions)==3 and len(set(regions))==1)
 ck(n.key+' border check preview and execution',sum(x.key=='nesnd_per_border_claim_state' for x in n.walk())==3)
 ck(n.key+' deterministic segment',has(n,'ordered_scope_state') and not any(x.key.startswith('random_') for x in n.walk()))
 ck(n.key+' guarded cooldown',has(n.get('effect'),'has_variable','nesnd_per_claim_cooldown'))
 ck(n.key+' localized target',all(n.key in loc and n.key+'_effect_tt' in loc for loc in locs.values()))
ck('Country-to-specific-state adjacency',has(triggers['nesnd_per_border_claim_state'],'is_adjacent_to_state','prev'))
values=tree('common/script_values/nesnd_cne_confidence.txt')
for key,want in [('base','-25'),('land','-5'),('urban','-5'),('estates','-5'),('war','-25'),('radicals','-20')]:ck('Confidence halved '+key,any(x.value==want for x in values.get('nesnd_cne_conf_'+key).walk()))
for key in ['intelligentsia','petty_bourgeoisie','trade_unions','industrialists']:ck('Government recovery unchanged '+key,shape(values.get('nesnd_cne_conf_'+key))==shape(parse(read(B/'common/script_values/nesnd_cne_confidence.txt')).get('nesnd_cne_conf_'+key)))
respite=effects['nesnd_cne_take_respite'];ck('Pause permanent one-use and six month lock',has(respite,'set_variable','nesnd_cne_respite_used') and any(n.key=='set_variable' and n.scalar('name')=='nesnd_cne_respite_active' and n.scalar('months')=='6' for n in respite.walk()))
ck('Pause stops programs, adds100, preserves main lifecycle',has(respite,'nesnd_cne_stop_all_programs','yes') and has(respite,'add','100') and not has(respite,'nesnd_land_cleanup'))
for n in tree('common/scripted_buttons/nesnd_cne_programs.txt').children:
 if n.key.endswith('_start_button'):ck(n.key+' pause gate',has(n.get('possible'),'has_variable','nesnd_cne_respite_active'))
 if n.key.endswith('_stop_button'):ck(n.key+' hidden bookkeeping',n.get('possible').get('hidden_trigger') is not None and n.get('effect').get('custom_tooltip') is not None)
ck('Respite actual guard once',has(triggers['nesnd_cne_respite_ready'],'has_variable','nesnd_cne_respite_used'))
ck('Bankruptcy -250',any(n.key=='change_variable' and n.scalar('name')=='nesnd_cne_confidence' and n.scalar('add')=='-250' for n in tree('common/scripted_effects/nesnd_cne_confidence.txt').walk()))
rep=jes['nesnd_cne_republic_journal'];ck('Republic failure only after actual war',has(rep.get('fail'),'has_variable','nesnd_cne_republic_war_seen'))
s=read(C/'common/scripted_effects/nesnd_cne_republic.txt');ck('Correct general ideology','ideology_republican_leader' in s and not re.search(r'ideology\s*=\s*ideology_republican\s',s));ck('Revolt is never reset','remove_variable = nesnd_cne_republic_rose' not in s)
for n in tree('common/scripted_progress_bars/nesnd_qe1_court.txt').children:ck(n.key+' real weekly breakdown',n.get('weekly_progress') is not None)
ck('Pure court preview no variable writes',not any(n.key in ['set_variable','change_variable','set_global_variable'] for n in tree('common/script_values/nesnd_qe1_court.txt').walk()))
s=frag('common/scripted_effects/nesnd_crisis_effects.txt','nesnd_open_southern_war');ck('War countdown after all backers',s.rfind('add_escalation = 90')>max(s.rfind('add_initiator_backers'),s.rfind('add_target_backers'),s.rfind('nesnd_join_opposition_play')))
ck('Nested helper uses prev','add_target_backers = { prev }' in frag('common/scripted_effects/nesnd_crisis_effects.txt','nesnd_join_opposition_play'))
s=read(C/'common/on_actions/nesnd_war_collapse.txt');ck('USM existence before comparison',s.find('exists = c:USM')<s.find('scope:enemy_country ?= c:USM'))
for k in ['nesnd_ming_find_ning_dynast','nesnd_ming_find_huai_dynast']:
 n=effects[k]
 for t in ['random_scope_character','random_character','random_character_in_exile_pool','random_character_in_void']:ck(k+' searches '+t,has(n,t))
for k in ['nesnd_ming_generate_ning_dynast','nesnd_ming_generate_huai_dynast']:
 n=effects[k];ck(k+' creation lock',has(n,'has_variable','nesnd_ming_generation_in_progress') and has(n,'has_global_variable','nesnd_ming_generation_cooldown'));ck(k+' no historical template cloning',not has(n,'template'))
factory=effects['nesnd_ming_create_dynast'].get('create_character');ck('New royal actual nonhistorical age21',factory.scalar('historical')=='no' and factory.scalar('age')=='21')
birth=effects['nesnd_ming_name_new_dynastic_heir'];ck('Birth only parent identity, no global scan',not has(birth,'nesnd_ming_refresh_royal_identity') and has(birth,'nesnd_ming_identify_lineage'))
gng=effects['nesnd_postwar_gng_restore_ming'];ck('Huai local branch restrictions',sum(n.key=='has_variable' and n.value=='nesnd_ming_huai_line' for n in gng.walk())>=3)
ck('Existing old royals not recreated',not any(n.key=='template' and (n.value or '').startswith('USM_zhu_') for n in tree('common/scripted_effects/nesnd_ming_generation.txt').walk()))
ck('Main user Japanese edit untouched',sha(M/'localization/simp_chinese/replace/zzzzzz_nesnd_jp_development_l_simp_chinese.yml')!=b['localization/simp_chinese/replace/zzzzzz_nesnd_jp_development_l_simp_chinese.yml'] and 'localization/simp_chinese/replace/zzzzzz_nesnd_jp_development_l_simp_chinese.yml' not in changed)
ck('Tiger no new diagnostics',not json.loads(read(R/'tiger-final-diff.json'))['added'])
ck('MCP real source queries pass',json.loads(read(R/'mcp.json'))['status']=='PASS')
status='STATIC_PASS' if all(x['pass'] for x in checks) else 'FAIL';dump(R/'final-validation.json',{'status':status,'checks':checks,'changed':changed,'engine_verified':False});print(status,len(checks));print([x['name'] for x in checks if not x['pass']])
