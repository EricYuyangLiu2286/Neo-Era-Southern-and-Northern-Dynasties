from pathlib import Path
import json,hashlib,shutil,subprocess,collections,sys
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');R=W/'reports/canon-route-execution-20261104';G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
META=json.loads((R/'batch-a-test-snapshot.json').read_text(encoding='utf-8'));SOURCE_T=Path(META['snapshot'])
T=SOURCE_T.parent/'tiger-context-mod'
B=SOURCE_T.parent/'tiger-baseline-context-mod'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
shutil.copytree(SOURCE_T,T)
extra=[]
for locale in ('simp_chinese','english'):
    rel=f'localization/{locale}/replace/ce_countries_l_{locale}.yml'
    p=W/'exports/canon-route-execution-20261104-a'/rel
    dest=T/rel;dest.parent.mkdir(parents=True,exist_ok=True);data=p.read_bytes();dest.write_bytes(data)
    extra.append({'path':rel,'source':p.as_posix(),'sha256':hashlib.sha256(data).hexdigest(),'role':'unchanged country-name localization dependency, present in both current and baseline'})
owned=json.loads((R/'batch-a-before.json').read_text(encoding='utf-8'));by_path={x['path']:x for x in owned}
B.mkdir(exist_ok=False)
for p in sorted(T.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(T).as_posix()
    if rel in by_path:
        if not by_path[rel]['existed']:continue
        source=R/'batch-a-before'/rel
    else:source=p
    dest=B/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
conf=R/'batch-a-tiger.conf'
conf.write_text('languages = { check = "simp_chinese" }\nfilter = { show_vanilla = no show_loaded_mods = no }\n',encoding='utf-8')
binary=W/'tools/tiger-1.19.0/vic3-tiger.exe'
report={'scope':'A-owned files with frozen prerequisites; same dependency context with A restored to pre-edit state as baseline','source_snapshot':str(SOURCE_T),'snapshot':str(T),'baseline':str(B),'extra_dependencies':extra,'binary_sha256':sha(binary),'config_sha256':sha(conf),'runs':[],'game_launched':False,'whole_C_checked':False}
before={p.relative_to(T).as_posix():sha(p) for p in T.rglob('*') if p.is_file()}
for label,root in [('current',T),('baseline',B)]:
    cmd=[str(binary),'--game',str(G.parent),'--config',str(conf),'--json',str(root)]
    print('Tiger A '+label+' started',flush=True)
    with (R/f'batch-a-tiger-{label}.json').open('wb') as out,(R/f'batch-a-tiger-{label}.stderr.txt').open('wb') as err:
        run=subprocess.run(cmd,stdout=out,stderr=err)
    report['runs'].append({'label':label,'command':cmd,'returncode':run.returncode})
    print('Tiger A '+label+' returned '+str(run.returncode),flush=True)
current=json.loads((R/'batch-a-tiger-current.json').read_text(encoding='utf-8-sig'))
baseline=json.loads((R/'batch-a-tiger-baseline.json').read_text(encoding='utf-8-sig'))
def sig(d):
    return (d['severity'],d['key'],d['message'],tuple((x.get('from'),x.get('path','').replace('\\','/'),(x.get('line') or '').strip()) for x in d['locations']))
old=collections.Counter(sig(x) for x in baseline);added=[]
for x in current:
    key=sig(x)
    if old[key]:old[key]-=1
    else:added.append(x)
def touches_owned(d):return any(x.get('from')=='MOD' and x.get('path','').replace('\\','/') in by_path for x in d['locations'])
report.update(current_count=len(current),baseline_count=len(baseline),new_total=len(added),new_owned=[x for x in added if touches_owned(x)],new_dependency=[x for x in added if not touches_owned(x)],counts=dict(collections.Counter((x['severity']+':'+x['key']) for x in added)),classification='PENDING_SOURCE_CLASSIFICATION')
after={p.relative_to(T).as_posix():sha(p) for p in T.rglob('*') if p.is_file()};report['snapshot_unchanged']=before==after
(R/'batch-a-tiger-delta.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'current':len(current),'baseline':len(baseline),'new_owned':len(report['new_owned']),'new_dependency':len(report['new_dependency']),'counts':report['counts'],'snapshot_unchanged':report['snapshot_unchanged']},ensure_ascii=False),flush=True)
