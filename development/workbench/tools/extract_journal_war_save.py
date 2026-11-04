from journal_war_context import *
import importlib.util,re
p=W/'reports/observer-finish-20261103/fra_hus_extract.py'
spec=importlib.util.spec_from_file_location('save_slices',p);h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
path=R/'runtime/autosave-text.v3';s=read(path)
hs=list(re.finditer(r'^([a-z_]+)=\{',s,re.M))
sections={m[1]:s[m.start():hs[i+1].start() if i+1<len(hs) else len(s)] for i,m in enumerate(hs)}
def recs(text):
    for m in re.finditer(r'^\t\t(\d+)=\{\n(.*?)^\t\t\}',text,re.M|re.S):
        yield m[1],re.sub(r'^\t\t','',m[2],flags=re.M)
def vals(text):
    body=h.block(text,'variables')
    if not body:return {}
    n=parse('variables={\n'+body+'\n}').get('variables');out={}
    data=n.get('data')
    if data:
        for item in data.children:
            flag=item.scalar('flag');value=item.get('data')
            if flag and value:out[flag]={'type':value.scalar('type'),'identity':value.scalar('identity')}
    return out
targets={'USM','HNA','SIH','GNG','MUG','HUS','CNE','JAP'}
cr=list(recs(sections['country_manager']));names={i:h.scalar(v,'definition') for i,v in cr}
countries={};ids={}
for i,v in cr:
    tag=names[i]
    if tag not in targets or h.scalar(v,'is_main_tag')!='yes':continue
    ids[i]=tag
    countries[tag]={'id':i,'dead':h.scalar(v,'dead'),'ruler':h.scalar(v,'ruler'),'capital':h.scalar(v,'capital'),'states':h.array(v,'states'),
        'variables':vals(v),'modifiers':h.modifiers(v)}
jm=sections['journal_entry_manager'];dead=h.block(jm,'dead',depth=1)
# A database record may retain active=yes after manager.death; retain both facts.
death={a:b for a,b in re.findall(r'object=(\d+)\s+death_date=([^\s}]+)',dead)}
journals=[]
for i,v in recs(jm):
    cid=h.scalar(v,'country');typ=h.scalar(v,'type','')
    if cid in ids and any(x in typ for x in ['india','eastern','civilwar','restoration','abolish','suppress_rebellion','ming_after']):
        journals.append({'id':i,'tag':ids[cid],'type':typ,'active':h.scalar(v,'active'),'death_date':death.get(i),'raw':v})
states=[]
for i,v in recs(sections['states']):
    if h.scalar(v,'country') in ids:
        states.append({'id':i,'tag':ids[h.scalar(v,'country')],'region':h.scalar(v,'region'),'controller':h.scalar(v,'controller'),'raw_fields':h.simple(v)})
plays=[]
for key in ['diplomatic_play_manager','war_manager']:
    if key in sections:
        for i,v in recs(sections[key]):
            if any(re.search(r'\b(?:initiator|target|country|actor|war_leader)='+cid+r'\b',v) for cid in ids):plays.append({'section':key,'id':i,'raw':v})
globals_={k:v for k,v in sections.items() if 'global_variable' in k or k=='variables'}
dump(R/'save-state.json',{'source':str(path),'source_sha256':sha(path),'game_date':re.search(r'game_date=(\S+)',s)[1],'sections':list(sections),'countries':countries,'journals':journals,'states':states,'plays':plays,'globals':globals_,'decoder':'rakaly0.8.22 strict unknown-key error; local copied save only'})
print('Date',re.search(r'game_date=(\S+)',s)[1],'countries',[(k,v['id'],v['dead']) for k,v in countries.items()])
for x in journals:print(x['tag'],x['type'],'active',x['active'],'death',x['death_date'])
for tag in ['MUG','HNA','SIH','GNG','USM']:
    if tag in countries:print(tag,'relevant vars', {k:v for k,v in countries[tag]['variables'].items() if any(a in k for a in ['india_priority','india_schools','india_industry','ming_court','surrender','south_defeat','status_quo','south_settled','opposition'])})
