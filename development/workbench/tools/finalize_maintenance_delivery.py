from maintenance_20261102_context import *
import zipfile
repo=W/'projects/nesnd-repository'
assert man(M)==man(C)
def shape(n):return n.key,n.op,n.value,tuple(shape(a) for a in n.children or [])
proof=[]
for rel in ['common/history/treaties/ce_historical_treaties.txt','common/journal_entries/ce_usm_the_last_days_of_ming.txt']:
 p=C/rel;s=read(p);new='\n'.join('' if not line.strip() else line for line in s.splitlines())+'\n'
 assert sha(M/rel)==sha(repo/rel)==sha(C/rel)
 assert shape(parse(s))==shape(parse(new))
 old=sha(p);write(p,new);shutil.copy2(p,M/rel);shutil.copy2(p,repo/rel);proof.append({'file':rel,'before':old,'after':sha(p),'AST_unchanged':True})
dump(R/'whitespace-preservation.json',proof)
data=json.loads(read(R/'main-merge.json'));shutil.copy2(R/'main-merge.json',R/'main-merge-before-whitespace.json')
for row in data['changed']:row['after']=sha(M/row['file'])
data['postmerge_whitespace_only']=proof;dump(R/'main-merge.json',data)
previous=json.loads(read(R/'package.json'));archive=W/'releases/nesnd-20261102-ui-poland-tributary-final.zip';assert not archive.exists();files=man(M)
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
 for rel in sorted(files):
  if rel in previous['excluded']:continue
  z.write(M/rel,rel)
with zipfile.ZipFile(archive) as z:
 for rel in z.namelist():assert z.read(rel)==(M/rel).read_bytes()
dump(R/'package.json',{'path':str(archive),'sha256':sha(archive),'excluded':previous['excluded'],'QA_included':False,'previous_archive_preserved':previous['path']})
assert man(M)==man(C)
mf=repo/'development/snapshot-manifest.json';records=json.loads(read(mf));index={x['path']:x for x in records['files']}
sources={f'workbench/reports/{R.name}/{name}':R/name for name in ['main-merge.json','package.json','whitespace-preservation.json']}
sources['workbench/tools/finalize_maintenance_delivery.py']=W/'tools/finalize_maintenance_delivery.py'
for rel,p in sources.items():
 target=repo/'development'/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target);index[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
records['files']=[index[k] for k in sorted(index)];dump(mf,records)
print('Final archive verified; whitespace-only AST proof saved; all614 main files equal candidate.')
