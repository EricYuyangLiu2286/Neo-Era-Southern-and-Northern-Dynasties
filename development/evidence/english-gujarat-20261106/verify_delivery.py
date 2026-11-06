"""Final source checks. No simulation of unobserved engine behaviour."""
from pathlib import Path
import hashlib, json, re, runpy, contextlib, io, sys
sys.path.insert(0,'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import read, parse
R=Path(__file__).parent; W=R.parents[1]
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
B=W/'backups/pre-change-english-gujarat-20261106T212037Z/mod'
names=['nesnd_civic_characters','nesnd_small_states','nesnd_phi_finance','nesnd_native_americas']
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def loc(p,lang):
    raw=p.read_bytes(); assert raw.startswith(b'\xef\xbb\xbf'),p
    lines=raw.decode('utf-8-sig').splitlines(); assert lines[0]=='l_'+lang+':'
    result={}
    for i,line in enumerate(lines[1:],2):
        if not line.strip() or line.lstrip().startswith('#'): continue
        match=re.fullmatch(r'\s+([\w.\-]+):(?:\d+)?\s+"((?:[^"\\]|\\.)*)"\s*',line)
        assert match,(p,i)
        k,v=match.groups(); assert k not in result,(p,k)
        result[k]=v
    return result
out={'validation':'STATIC_PASS','engine':'NOT_RUN','files':[]}
for name in names:
    rel=f'localization/english/replace/{name}_l_english.yml'
    oldrel=rel if (B/rel).exists() else rel.replace('/replace/','/')
    en=loc(M/rel,'english'); old=loc(B/oldrel,'english')
    zhrel=f'localization/simp_chinese/replace/{name}_l_simp_chinese.yml'
    zh=loc(M/zhrel,'simp_chinese')
    oldzhrel=zhrel if (B/zhrel).exists() else zhrel.replace('/replace/','/')
    assert (M/zhrel).read_bytes()==(B/oldzhrel).read_bytes(),zhrel
    assert list(en)==list(old)==list(zh),name
    for k,v in en.items():
        assert not re.search(r'[\u3400-\u9fff]',v),(name,k)
        for pat in [r'\[[^\]]+\]',r'\$[^$]+\$',r'#(?:v|p|n|!|bold|tooltippable|tooltip:[^ ]+)']:
            # Preserve English callable tokens; Concept display arguments are
            # localized prose and therefore can differ from the Chinese ones.
            assert sorted(re.findall(pat,v))==sorted(re.findall(pat,old[k])),(name,k,pat)
        def nums(s):
            s=re.sub(r'\[[^\]]+\]|\$[^$]+\$','',s)
            s=re.sub(r'(\d+(?:\.\d+)?)万',lambda m:str(int(float(m[1])*10000)),s)
            return [n.replace(',','') for n in re.findall(r'\d+(?:[,.]\d+)*',s)]
        # Preserve published English numeric literals. Chinese uses mixed
        # written and Arabic numbers (e.g. 2 vs "two"), checked editorially.
        assert sorted(nums(v))==sorted(nums(old[k])),(name,k,'numbers',nums(v),nums(old[k]))
    out['files'].append({'file':rel,'keys':len(en),'rewritten':sum(en[k]!=old[k] for k in en),'sha256':sha(M/rel)})
# The independent history audit was read by root before execution. It checks
# actual ordered records and all non-Gujarat states, not a fabricated fixture.
with contextlib.redirect_stdout(io.StringIO()): runpy.run_path(str(R/'sol-history-audit.py'))
history=json.loads((R/'sol-history-audit.json').read_text('utf-8'))
out['history']={k:v for k,v in history.items() if k!='effective_startup_refs'}
for language in ['english','simp_chinese']:
    rel=f'localization/{language}/replace/ce_country_flavor_l_{language}.yml'
    new=loc(M/rel,language); old=loc(B/rel,language)
    assert new.pop('nesnd_french_gujarat_squadron')==('Gujarat Squadron' if language=='english' else '古吉拉特分舰队')
    assert new==old
    assert sum('nesnd_french_gujarat_squadron:' in p.read_text('utf-8-sig') for p in (M/'localization'/language).rglob('*.yml'))==1
fleet=read(M/'common/history/military_formations/nesnd_french_gujarat_fleet.txt')[1].get('MILITARY_FORMATIONS').get('c:FRA').get('create_military_formation')
assert fleet.scalar('name')=='nesnd_french_gujarat_squadron'
assert set(n.key for n in fleet.children)=={'type','hq_region','name','ship'}
assert [(s.scalar('type'),s.scalar('count')) for s in fleet.all('ship')]==[('ship_type:ship_type_ship_of_the_line','2'),('ship_type:ship_type_frigate','4')]
for rel in ['common/history/states/00_states.txt','common/history/pops/10_india.txt','common/history/buildings/10_india.txt']:
    read(M/rel)
# Retain the unrelated author edit to the Chinese India text.
india=M/'localization/simp_chinese/replace/nesnd_india_l_simp_chinese.yml'
assert india.read_bytes()==(B/india.relative_to(M)).read_bytes()
out['author_india_sha256']=sha(india)
changed=[]
for p in M.rglob('*'):
    if not p.is_file(): continue
    q=B/p.relative_to(M)
    if not q.exists() or sha(p)!=sha(q): changed.append(str(p.relative_to(M)).replace('\\','/'))
out['changed_from_backup']=sorted(changed)
(R/'final-checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'validation':out['validation'],'entries':sum(x['keys'] for x in out['files']),'rewritten':sum(x['rewritten'] for x in out['files']),'history':out['history'],'changed_count':len(changed)},ensure_ascii=False))
