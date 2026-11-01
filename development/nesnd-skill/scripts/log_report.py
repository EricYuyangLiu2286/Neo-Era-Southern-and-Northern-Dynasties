"""Group actual engine logs, preserving multiline context and raw provenance."""
import argparse,re,json,hashlib
from pathlib import Path
from collections import Counter
from catalog import MOD,GAME,WORK

STAMP=re.compile(r'^\[(\d\d:\d\d:\d\d)\]')
def report(folder):
    groups={};records=[]
    def add(lines,p,start):
        if not lines:return
        raw='\n'.join(lines);normalized=re.sub(r'^\[\d\d:\d\d:\d\d\]', '',raw)
        key=hashlib.sha256(normalized.encode()).hexdigest();m=STAMP.match(lines[0]);time=m[1] if m else None
        paths=re.findall(r'(?:file:\s*|File:\s*)([^\n]+?)(?:\s+line[: ]|\s+Line[: ]|$)',raw,re.M)
        # Path attribution is provisional: dependencies can override shared paths.
        origin='unknown'
        if any((MOD/q.strip()).exists() for q in paths):origin='mod-or-overridden-vanilla'
        elif 'EACR' in raw or 'EAC_' in raw:origin='EACR-related'
        elif any((GAME/q.strip()).exists() for q in paths):origin='vanilla-or-dependency'
        if key not in groups:groups[key]={'fingerprint':key,'count':0,'origin_hint':origin,'sample':raw,'occurrences':[]}
        g=groups[key];g['count']+=1;g['occurrences'].append({'file':str(p),'line':start,'time':time})
    files=sorted(Path(folder).glob('error*.log'))
    for p in files:
        lines=[];start=1
        for i,line in enumerate(p.read_text('utf-8-sig',errors='replace').splitlines(),1):
            if STAMP.match(line):add(lines,p,start);lines=[];start=i
            lines.append(line)
        add(lines,p,start)
    return {'log_files':[str(p) for p in files],'records':sum(g['count'] for g in groups.values()),'unique_groups':len(groups),'groups':sorted(groups.values(),key=lambda g:-g['count']),'note':'Origin hints are not verdicts. Compare actual enabled files, a vanilla/dependency baseline, and behavior in game.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--baseline',type=Path);a=ap.parse_args();r=report(a.folder)
    if a.baseline:
        b=json.loads(a.baseline.read_text('utf-8-sig'));old={g['fingerprint'] for g in b['groups']};new={g['fingerprint'] for g in r['groups']};r['new_groups']=sorted(new-old);r['absent_from_current']=sorted(old-new)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2),'utf-8');print(json.dumps({k:v for k,v in r.items() if k!='groups'},ensure_ascii=False))
