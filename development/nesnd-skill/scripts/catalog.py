"""Versioned, read-only source inventory; writes only to the workbench."""
from pathlib import Path
import argparse, hashlib, json, re, shutil
from datetime import datetime, timezone
GAME = Path(r'D:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game')
MOD = Path(r'D:\Users\Eric Liu\Documents\Paradox Interactive\Victoria 3\mod\Neo-Era Southern and Northern Dynasties')
WORK = MOD.parent.parent / 'nesnd-workbench'
WORKSHOP = Path(r'D:\Program Files (x86)\Steam\steamapps\workshop\content\529340')
ROOTS = {'game': GAME, 'mod': MOD, **{x:WORKSHOP/x for x in ['3704408897','3385002128','3278156786','3464386853']}}
INDEX = WORK/'reports/source-catalog.json'
EXTS = {'.txt','.gui','.md','.json','.yml','.asset'}
FOLDERS = ['common','events','map_data','gui','data_binding','localization','gfx/portraits','tools/scripted_tests','.metadata']

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def version():
    v = json.loads((GAME.parent/'launcher/launcher-settings.json').read_text('utf-8-sig'))
    steam = (GAME.parents[2]/'appmanifest_529340.acf').read_text('utf-8-sig')
    match = re.search(r'"buildid"\s+"(\d+)"', steam)
    return {'version':v['rawVersion'], 'build':match[1] if match else 'unknown'}
def inventory(root):
    records = {}
    for folder in FOLDERS:
        for p in (root/folder).rglob('*'):
            if p.is_file() and p.suffix.lower() in EXTS:
                rel = p.relative_to(root).as_posix()
                if any(x.startswith('_backup') for x in p.parts): continue
                records[rel] = {'sha256':digest(p),'bytes':p.stat().st_size}
    return records
def refresh():
    now = {'generated_utc':datetime.now(timezone.utc).isoformat(), **version(), 'roots':{}}
    for label, root in ROOTS.items():
        files = inventory(root)
        symbols = []
        for rel, record in files.items():
            if Path(rel).suffix not in {'.txt','.gui','.md'}: continue
            try: text=(root/rel).read_text('utf-8-sig')
            except UnicodeError: continue
            for line_no, line in enumerate(text.splitlines(),1):
                # Index only; not a validity checker. Nested keys retained as routes.
                m=re.match(r'^([\w@:.\-]+)\s*(?:\?=|=)\s*(.*)',line)
                if m:
                    symbols.append({'symbol':m[1],'file':rel,'line':line_no,'kind':rel.split('/')[1] if '/' in rel else '', 'sha256':record['sha256']})
        now['roots'][label]={'path':str(root),'files':files,'symbols':symbols}
    INDEX.parent.mkdir(parents=True,exist_ok=True)
    changes={}
    if INDEX.exists():
        old=json.loads(INDEX.read_text('utf-8'))
        shutil.copy2(INDEX, INDEX.with_name('source-catalog.previous.json'))
        for label, current in now['roots'].items():
            prior=old.get('roots',{}).get(label,{}).get('files',{})
            changes[label]={'added':sorted(set(current['files'])-set(prior)), 'removed':sorted(set(prior)-set(current['files'])), 'changed':[p for p in current['files'] if p in prior and current['files'][p]['sha256']!=prior[p]['sha256']]}
    INDEX.write_text(json.dumps(now,ensure_ascii=False,indent=2),'utf-8')
    (INDEX.parent/'source-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2),'utf-8')
    print(json.dumps({'index':str(INDEX), **version(),'files':{k:len(v['files']) for k,v in now['roots'].items()},'changes':{k:{a:len(b) for a,b in v.items()} for k,v in changes.items()}},ensure_ascii=False))
def status():
    current=version()
    if not INDEX.exists(): print(json.dumps({**current,'status':'NO_INDEX: run refresh'})); return
    old=json.loads(INDEX.read_text('utf-8'))
    current_files=inventory(GAME)
    previous=old['roots']['game']['files']
    changed=[p for p in set(previous)|set(current_files) if previous.get(p,{}).get('sha256')!=current_files.get(p,{}).get('sha256')]
    print(json.dumps({**current,'indexed_version':old['version'],'status':'STALE' if changed or current['version']!=old['version'] else 'CURRENT','changed_count':len(changed),'changed':changed[:50]},ensure_ascii=False))
def snapshot():
    v=version()
    dest=WORK/'baselines'/f"vanilla-{v['version']}-{v['build']}"
    if dest.exists(): raise SystemExit(f'Baseline already exists; not overwritten: {dest}')
    files=inventory(GAME)
    for rel in files:
        target=dest/'game'/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(GAME/rel,target)
    (dest/'manifest.json').write_text(json.dumps({**v,'files':files},ensure_ascii=False,indent=2),'utf-8')
    print(str(dest))
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['status','refresh','snapshot','find']);p.add_argument('query',nargs='?',default=''); a=p.parse_args()
    if a.command=='find':
        data=json.loads(INDEX.read_text('utf-8')); matches=[]
        for label,root in data['roots'].items():
            for s in root['symbols']:
                if a.query.lower() in (s['symbol']+' '+s['file']).lower(): matches.append({'root':label, **s})
        print(json.dumps(matches[:150],ensure_ascii=False,indent=2)); print(f'{len(matches)} total matches')
    else: globals()[a.command]()
