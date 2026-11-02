from qin_persia_context import *
import subprocess,zipfile
from datetime import datetime,timezone

repo=W/'projects/nesnd-repository';commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()
mf=man(M);assert mf==man(C)
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
remote=subprocess.check_output(['git','ls-remote','origin','refs/heads/main'],cwd=repo).decode().split()[0]
assert remote==commit
paths=sorted(mf)
request=''.join(f'{commit}:{p}\n' for p in paths).encode()
data=subprocess.run(['git','cat-file','--batch'],input=request,capture_output=True,cwd=repo,check=True).stdout
offset=0
for path in paths:
    end=data.index(b'\n',offset);header=data[offset:end].split()
    assert len(header)==3 and header[1]==b'blob',(path,header)
    size=int(header[2]);blob=data[end+1:end+1+size]
    assert hashlib.sha256(blob).hexdigest()==mf[path],path
    offset=end+size+2
assert offset==len(data)
package=json.loads(read(R/'package.json'))
assert sha(Path(package['path']))==package['sha256']
with zipfile.ZipFile(package['path']) as z:
    for path in z.namelist():assert hashlib.sha256(z.read(path)).hexdigest()==mf[path]
backup=W/'backups/checkpoint-qin-persia-main-final-20261102T045833Z/mod'
assert man(backup)==mf
result={'status':'DELIVERED','source_commit':commit,'remote_main_at_source_publish':remote,
 'main_files_verified_against_git_blobs':len(paths),'candidate_equal_main':True,'checkpoint_equal_main':True,
 'checkpoint':str(backup),'package':package['path'],'package_sha256':package['sha256'],
 'checks':5344,'arithmetic_cases':720,'MCP_queries':8,'Tiger_added':0,
 'engine_verified':False,'game_launched':False,'tools_shipped_in_game_package':False,
 'whitespace_check':'Native CRLF accepted with cr-at-eol; retained .diff evidence excluded from whitespace lint only.',
 'verified_utc':datetime.now(timezone.utc).isoformat()}
dump(R/'git-delivery.json',result)
target=repo/'development/workbench/reports'/R.name/'git-delivery.json'
shutil.copy2(R/'git-delivery.json',target)
manifest=repo/'development/snapshot-manifest.json';d=json.loads(read(manifest))
rel='workbench/reports/'+R.name+'/git-delivery.json'
d['files']=[x for x in d['files'] if x['path']!=rel]+[{'path':rel,'source':str(R/'git-delivery.json'),'sha256':sha(R/'git-delivery.json'),'bytes':(R/'git-delivery.json').stat().st_size}]
d['files'].sort(key=lambda x:x['path']);dump(manifest,d)
print(json.dumps(result,ensure_ascii=False))
