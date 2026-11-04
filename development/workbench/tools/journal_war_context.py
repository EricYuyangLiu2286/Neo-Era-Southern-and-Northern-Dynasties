from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
from pathlib import Path
import json,shutil,sys,subprocess
B=W/'backups/pre-change-journal-war-feedback-20261103T222744Z/mod'
C=W/'exports/journal-war-feedback-20261103-a'
R=W/'reports/journal-war-feedback-20261103'
PARENT='c4626514277991a415283897af47769e12495138'
if __name__=='__main__':
    assert man(M)==man(B)
    if C.exists():assert man(C)==man(B),'Existing candidate has changes; review before reuse'
    else:shutil.copytree(M,C)
    if not (R/'baseline.json').exists():dump(R/'baseline.json',{'parent':PARENT,'backup':str(B),'files':man(B),'engine_verified':False})
    else:assert json.loads(read(R/'baseline.json'))['files']==man(B)
    captured=[]
    for rel in ['logs/error.log','save games/autosave.v3','save games/大吴_1850_09_03.v3']:
        src=W.parent/rel;dst=R/'runtime'/rel
        if src.exists():
            h=sha(src);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
            assert sha(src)==sha(dst)==h,('Source changed during capture',rel)
            captured.append({'path':str(src),'capture':str(dst),'sha256':h,'bytes':dst.stat().st_size})
    dump(R/'runtime-capture.json',captured)
    print('Candidate created; stable runtime captures:',len(captured))
