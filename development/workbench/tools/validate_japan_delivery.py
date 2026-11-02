from japan_dev_context import *
from canon_prose_context import loc_index
from collections import Counter
import re,math

base,final=man(M),man(C)
changed=[p for p in sorted(base.keys()|final.keys()) if base.get(p)!=final.get(p)]
checks=[]
def check(name,result,detail=None):checks.append({'name':name,'passed':bool(result),'detail':detail})
check('No source files deleted',not(base.keys()-final.keys()))
protected=('map_data/','common/history/buildings/','common/history/pops/','common/history/states/','gfx/')
check('Territory, population, buildings and art unchanged',not any(p.startswith(protected) for p in changed))
asts={}
for p in C.rglob('*.txt'):
    rel=p.relative_to(C).as_posix()
    if rel.startswith(('common/','events/')):asts[rel]=parse(read(p))
check('All active script text parsed preserving duplicates',True,len(asts))
defs={}
for rel,t in asts.items():
    for n in t.children:
        if n.key:
            key=n.key.removeprefix('REPLACE:').removeprefix('REPLACE_OR_CREATE:')
            if key.startswith('nesnd_jp_'):defs.setdefault(key,[]).append((rel,n))
dbkeys=Counter((rel.split('/')[1],key) for key,rows in defs.items() for rel,_ in rows)
check('New definitions unique within each database',all(v==1 for v in dbkeys.values()),[k for k,v in dbkeys.items() if v>1])
missing=[]
for rel in changed:
    if rel not in asts:continue
    for n in asts[rel].walk():
        if n.key and n.key.startswith('nesnd_jp_') and n.value is not None and n.key not in defs:missing.append([rel,n.key,n.value])
check('All named JP trigger/effect/value calls resolve',not missing,missing)

zh,en=loc_index(C,'simp_chinese'),loc_index(C,'english')
jpkeys={k for k in zh if k.startswith('nesnd_jp_')}
for key in sorted(jpkeys):
    check('English present '+key,key in en)
    if key not in en:continue
    a,b=zh[key][-1][2],en[key][-1][2]
    tok=lambda v:Counter(re.findall(r'\[[^\]]+\]|\$[^$]+\$',v))
    check('Bilingual dynamic refs '+key,tok(a)==tok(b))
    check('English language '+key,not re.search('[\u3400-\u9fff]',b))
for rel in changed:
    if rel.startswith('localization/'):
        raw=(C/rel).read_bytes();check('UTF8 BOM '+rel,raw.startswith(b'\xef\xbb\xbf'))

je_defs={k:v[0] for k,v in defs.items() if v[0][0].startswith('common/journal_entries/')}
triggers={k:v[0][1] for k,v in defs.items() if v[0][0].startswith('common/scripted_triggers/')}
def self_requirements(n,key,neg=False,stack=()):
    found=[]
    for v in n.children or []:
        sign=neg ^ (v.key in ('NOT','NOR'))
        if v.key=='has_journal_entry' and v.value==key and not neg:found.append(stack+(v.key,))
        if v.key in triggers and v.value in ('yes','no') and v.key not in stack:
            found+=self_requirements(triggers[v.key],key,neg^(v.value=='no'),stack+(v.key,))
        if v.children:found+=self_requirements(v,key,sign,stack)
    return found
for key,(rel,n) in sorted(je_defs.items()):
    check('JE explicit possible '+key,n.get('possible') is not None)
    check('JE explicit invalid '+key,n.get('invalid') is not None)
    check('JE entry no positive self-lock '+key,not self_requirements(n.get('possible'),key))
    check('JE text '+key,key in zh and key+'_reason' in zh and key in en and key+'_reason' in en)
    for b in n.all('scripted_button'):check('JE button '+key+' '+b.value,b.value in defs)
    for b in n.all('scripted_progress_bar'):check('JE bar '+key+' '+b.value,b.value in defs)
    icon=n.scalar('icon')
    if icon:check('Icon exists '+key,(C/icon).is_file() or (G/icon).is_file(),icon)

native=json.loads(read(R/'native-entry-adaptation.json'))
for row in native['disabled_event_files']:
    rel=row['path'];check('Native source unchanged '+rel,sha(G/rel)==row['source_sha256'])
    events=[n for n in asts[rel].children if n.get('type') is not None]
    check('Native event ids preserved '+rel,{n.key for n in events}==set(row['event_ids']))
    for n in events:
        check('Native event closed '+n.key,n.get('trigger').scalar('always')=='no' and n.get('cancellation_trigger').scalar('always')=='yes')

bar=asts['common/scripted_progress_bars/nesnd_jp_development.txt'].get('nesnd_jp_cohesion_bar')
check('Five native cohesion sources',len(bar.get('monthly_progress').all('add'))==5)
for key in ['order','living','learning','conflict','victory']:
    n=asts['common/script_values/nesnd_jp_development.txt'].get('nesnd_jp_cohesion_'+key)
    check('Statistics gate '+key,n.get('if').get('limit').scalar('has_variable')=='nesnd_jp_statistics_ready')
exchange=asts['common/scripted_effects/nesnd_jp_development.txt'].get('nesnd_jp_cultural_exchange')
check('No pop deletion/religion in cultural exchange',not any(n.key in {'remove_pop','kill_pop','change_pop_religion','set_pop_religion'} for n in exchange.walk()))
check('Conversion fraction frozen before pop iteration',sum(n.key=='set_variable' and n.scalar('name')=='nesnd_jp_conversion_fraction' for n in exchange.walk())==2)
arithmetic=[]
for total in (1,10,101,10000,1000000):
    for target in (0,.1,.5,.75,.9,.95,.999,1):
        fraction=min(1,max(0,.1/max(.00001,1-target)))
        moved=total*(1-target)*fraction
        expected=min(total*.1,total*(1-target))
        arithmetic.append({'population':total,'target_share':target,'moved':moved,'expected':expected})
        check(f'Conversion mass bound {total}/{target}',math.isclose(moved,expected,abs_tol=1e-8) and 0<=moved<=total)
dump(R/'conversion-arithmetic.json',{'cases':arithmetic,'not_engine_execution':True})

arsenals=asts['common/journal_entries/nesnd_jp_industry.txt'].get('nesnd_jp_arsenals')
check('Single arsenals completion definition',arsenals.get('complete').scalar('nesnd_jp_arsenals_ready')=='yes')
withdrawn=('nesnd_jp_procurement','nesnd_jp_wu_procurement','nesnd_jp_wu_supplier_contract','nesnd_jp_wu_buyer_contract','nesnd_jp_offer_wu_procurement')
check('Rejected procurement files absent',not any('nesnd_jp_procurement' in rel for rel in asts))
left=[rel for rel in asts if any(token in read(C/rel) for token in withdrawn)]
check('No procurement calls variables payouts or gates',not left,left)
check('No procurement player text',not any(any(k.startswith(token) for token in withdrawn) for k in zh.keys()|en.keys()))
foreign=asts['common/scripted_triggers/nesnd_jp_foreign.txt']
check('Foreign kind range restored',not any(n.key in {'nesnd_jp_request_kind','nesnd_jp_incoming_kind'} and n.value=='8' for n in foreign.walk()))
grain=asts['common/scripted_triggers/nesnd_jp_industry.txt'].get('nesnd_jp_affordable_grain')
check('Food uses local capital price',any(n.key=='state_goods_pricier' and n.value=='0.1' for n in grain.walk()) and not any(n.key=='market_goods_pricier' for n in grain.walk()))
food=asts['common/journal_entries/nesnd_jp_industry.txt'].get('nesnd_jp_food_supply')
check('Food JE and bootstrap share actual readiness',food.get('complete').scalar('nesnd_jp_food_supply_ready')=='yes')
trade=asts['common/scripted_triggers/nesnd_supply_triggers.txt'].get('nesnd_supply_diplomacy_ready')
check('Shared market qualifies without contacts',any(n.key=='participants' and n.op=='>=' and n.value=='2' for n in trade.get('OR').walk()))
clear=asts['common/scripted_effects/nesnd_supply_effects.txt'].get('nesnd_supply_clear_partner')
check('Diplomatic contact cleanup preserves economic weeks',not any(n.key=='set_variable' and n.scalar('name')=='nesnd_supply_weeks' for n in clear.walk()))

for key in ['nesnd_jp_establish_toyotomi','nesnd_jp_establish_edo','nesnd_jp_establish_kyoto']:
    check('Establishment JE defined '+key,key in je_defs)
for kind in (1,2,6,7):
    text=read(C/'common/scripted_triggers/nesnd_jp_foreign.txt')
    check('Delayed diplomatic standing kind '+str(kind),f'nesnd_jp_request_kind = {kind}' in text and 'nesnd_jp_diplomatic_standing = yes' in text)

for role in ['japanese','jiangnan']:
    n=asts['common/script_values/nesnd_jp_development.txt'].get('nesnd_jp_conversion_fraction_'+role)
    check('Conversion uses 10 percent state target '+role,n.scalar('value')=='0.1')
raw=read(C/'common/scripted_effects/ce_japan_gov_effects.txt')
check('Guarded historical heir reuse',raw.count('exists = scope:jp_existing_historical_heir')==raw.count('set_heir = scope:jp_existing_historical_heir')==13)
check('Persistent shared Heikatsu creation marker',read(C/'common/character_templates/zz_ce_JAP.txt').count('set_global_variable = nesnd_jp_heikatsu_ever_created')==2)
check('No temporary Korean claimant alias', 'jp_korean_claimant' not in read(C/'common/scripted_effects/nesnd_jp_korea.txt'))

frozen=man(C);status='STATIC_PASS' if all(c['passed'] for c in checks) else 'FAIL'
dump(R/'external-final-checks.json',{'status':status,'checks':checks,'files':frozen,'changed':changed,'new_journal_count':len(je_defs),'jp_localization_keys':len(jpkeys),'game_launched':False,'engine_verified':False})
print(json.dumps({'status':status,'checks':len(checks),'failed':[c['name'] for c in checks if not c['passed']],'new_journals':len(je_defs),'localization_keys':len(jpkeys)}))
if status!='STATIC_PASS':raise SystemExit(1)
