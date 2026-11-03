from qin_persia_context import W,M,read,sha,dump
import re,shutil,collections
R=W/'reports/qe1-variable-20261103'
source=W/'runtime/profiles/20261102T234900Z'
R.mkdir(exist_ok=True)
counts=collections.Counter();rows=[]
for name in ['error.1.log','error.log','debug.log','game.log']:
    p=source/'logs'/name
    if not p.exists():continue
    dest=R/'original-logs'/name
    if not dest.exists():dest.parent.mkdir(exist_ok=True);shutil.copy2(p,dest)
    if not name.startswith('error'):continue
    s=read(dest)
    for match in re.finditer(r'Error: (.*?)\n\s*Script location: ([^\r\n]+)',s):
        counts[(match[1],match[2])]+=1
    rows.append({'source':str(p),'copy':str(dest),'sha256':sha(dest),'bytes':dest.stat().st_size})
report={'logs':rows,'unique_errors':[{'error':a,'location':b,'count':c} for (a,b),c in counts.most_common()],'total_script_errors':sum(counts.values())}
dump(R/'error-inventory.json',report)
print('Captured script errors:',sum(counts.values()),'unique pairs:',len(counts))
for (a,b),c in counts.most_common(18):print(c,b,a)
print('Snapshot/main identity file equal:',sha(M/'common/script_values/nesnd_qe1_identity.txt')==sha(W/'exports/runtime-20261102T234900Z/mod/common/script_values/nesnd_qe1_identity.txt'))
