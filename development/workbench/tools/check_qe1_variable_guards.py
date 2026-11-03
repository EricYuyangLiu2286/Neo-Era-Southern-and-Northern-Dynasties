"""Source guard regression for the exact variable reads in the captured engine trace.

This checks ordered source branches, not a substitute Jomini runtime.
"""
from qin_persia_context import W,M,read,parse,dump,sha
from pathlib import Path
import re,sys
root=Path(sys.argv[1]) if len(sys.argv)>1 else M
label=sys.argv[2] if len(sys.argv)>2 else 'current'
rel='common/script_values/nesnd_qe1_identity.txt'
source=read(root/rel);tree=parse(source)
findings=[];seen=[]
def required(limit):
    if limit is None:return set()
    out={n.value for n in limit.all('has_variable')}
    for n in limit.all('AND'):out|=required(n)
    return out
def walk(n,known,path):
    # Do not treat a sibling existence condition as short-circuit protection.
    for word in [n.key or '',n.value or '']:
        for name in re.findall(r'(?<![\w.:])var:(nesnd_qe1_\w+)',word):
            seen.append({'path':path,'variable':name})
            if name not in known:findings.append({'path':path,'variable':name,'line':source[:n.start].count('\n')+1})
    if n.key in ('if','else_if','trigger_if','trigger_else_if'):
        limit=n.get('limit')
        if limit:walk(limit,known,path+'.limit')
        inner=known|required(limit)
        for c in n.children or []:
            if c is not limit:walk(c,inner,path+'.'+str(c.key))
    else:
        for c in n.children or []:walk(c,known,path+'.'+str(c.key))
for n in tree.children:walk(n,set(),n.key)
status='STATIC_PASS' if not findings else 'FAIL'
report={'status':status,'root':str(root),'source':rel,'sha256':sha(root/rel),'reads_checked':len(seen),'unguarded_reads':findings,'engine_execution':False}
dump(W/'reports/qe1-variable-20261103'/('guards-'+label+'.json'),report)
print(status,len(seen),'variable reads;',len(findings),'unguarded:',findings)
if findings:raise SystemExit(1)
