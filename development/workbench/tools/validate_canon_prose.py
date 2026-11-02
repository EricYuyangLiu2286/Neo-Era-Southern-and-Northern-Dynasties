from canon_prose_context import *
from collections import Counter

def shape(n):
    return (n.key,n.value,n.op,n.prefix,tuple(shape(x) for x in n.children or []))

u,e=man(U),man(E)
changed=[p for p in sorted(u.keys()|e.keys()) if u.get(p)!=e.get(p)]
checks=[]
def check(name,passed,detail=None):
    checks.append({'name':name,'passed':bool(passed),'detail':detail})
check('No deletions',not(u.keys()-e.keys()))
check('Game data unchanged',all(not p.startswith(('map_data/','common/history/','common/cultures/','common/country_definitions/','gfx/')) for p in changed))
parsed=[]
for rel in changed:
    p=E/rel
    if p.suffix=='.txt' and rel.startswith(('common/','events/')):
        parse(read(p));parsed.append(rel)
check('Changed scripts parse preserving ordered repeated fields',True,parsed)
localization=[]
for rel in changed:
    if rel.startswith('localization/'):
        p=E/rel;raw=p.read_bytes();s=read(p)
        check('UTF8 BOM '+rel,raw.startswith(b'\xef\xbb\xbf'))
        lang=rel.split('/')[1]
        check('Language header '+rel,s.splitlines()[0]=='l_'+lang+':')
        failures=[(i,line) for i,line in enumerate(s.splitlines(),1) if line.strip() and not line.lstrip().startswith('#') and i>1 and not LOC.match(line)]
        check('Localization syntax '+rel,not failures,failures)
        localization.append(rel)

# Event choices are gameplay, not editorial material. The locality must not alter outcomes.
for key in ['nesnd_crisis.30','nesnd_crisis.31','nesnd_crisis.32','nesnd_crisis.33']:
    b=parse(read(U/'events/nesnd_crisis_events.txt')).get(key)
    a=parse(read(E/'events/nesnd_crisis_events.txt')).get(key)
    check(key+' options unchanged',[shape(n) for n in a.all('option')]==[shape(n) for n in b.all('option')])
n=parse(read(E/'events/nesnd_crisis_events.txt')).get('nesnd_crisis.30')
check('Locality recorded at event creation',n.get('immediate').get('ordered_scope_state').scalar('save_scope_as')=='nesnd_land_petition_state')
first=n.get('desc').get('first_valid')
check('Absent locality has safe fallback',first.scalar('desc')=='nesnd_crisis.30.d' and first.get('triggered_desc').get('trigger').scalar('exists')=='scope:nesnd_land_petition_state')

# Foreign aid may no longer be sent by a dead country or an enemy. Verify source guards and reward preservation.
t=parse(read(E/'common/scripted_triggers/nesnd_per_campaign.txt')).get('nesnd_per_aid_live')
check('Aid source guarded before relation lookup',t.get('trigger_if').get('limit').scalar('exists')=='c:QE1' and t.get('trigger_else').scalar('always')=='no')
for i in (1,2,3):
    b=parse(read(U/'events/nesnd_per_campaign.txt')).get(f'nesnd_per.{i}')
    a=parse(read(E/'events/nesnd_per_campaign.txt')).get(f'nesnd_per.{i}')
    check(f'PER {i} reward unchanged',shape(a.get('immediate'))==shape(b.get('immediate')))
    check(f'PER {i} delayed cancellation',a.get('cancellation_trigger').get('NOT').scalar('nesnd_per_aid_live')=='yes')

application=[]
for file in ['cne-applied.json','usm-applied.json','japan-qin-applied.json','root-applied.json']:
    if (R/file).exists():
        data=json.loads(read(R/file));application+=data.get(str(E),[])
keys={r['key'] for r in application}
zh,en=loc_index(E,'simp_chinese'),loc_index(E,'english')
errors=[]
for k in sorted(keys):
    if k not in zh or k not in en:errors.append([k,'missing language']);continue
    # All duplicate definitions modified in place must agree.
    for lang,db in [('zh',zh),('en',en)]:
        if len({row[2] for row in db[k]})>1:errors.append([k,lang,'unequal override layers'])
    z,y=zh[k][-1][2],en[k][-1][2]
    if re.search('[\u3400-\u9fff]',y):errors.append([k,'CJK in English',y])
    tokens=lambda v:Counter(re.findall(r'\[[^\]]+\]|\$[^$]+\$',v))
    if tokens(z)!=tokens(y):errors.append([k,'dynamic token difference',dict(tokens(z)),dict(tokens(y))])
check('Changed bilingual keys and all override layers',not errors,errors)

dump(R/'external-validation.json',{'status':'PASS' if all(x['passed'] for x in checks) else 'FAIL','checks':checks,'changed_files':changed,'parsed_scripts':parsed,'localization_files':localization,'edited_keys':len(keys),'engine_verified':False,'game_launched':False})
print(json.dumps({'checks':len(checks),'failed':[x['name'] for x in checks if not x['passed']],'edited_keys':len(keys),'changed_files':len(changed)}))
if not all(x['passed'] for x in checks):raise SystemExit(1)
