from qin_persia_context import W,M,S,read,sha,man,dump
import json,shutil,subprocess,datetime,zipfile
R=W/'reports/qe1-variable-20261103';C=W/'exports/qe1-variable-20261103-a'
B=W/'backups/pre-change-qe1-variable-guards-20261103T002508Z/mod'
F=W/'backups/candidate-qe1-variable-guards-20261103T002907Z/mod'
repo=W/'projects/nesnd-repository';parent='c1463da95111e3ec2369c174c86f37803adbbdce'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==parent
assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
before,after=man(B),man(C)
assert man(M)==before and man(F)==after
for rel,digest in before.items():assert sha(repo/rel)==digest,('Main/Git mismatch',rel)
v=json.loads(read(R/'validation.json'));assert v['status']=='STATIC_PASS'
for rel,digest in v['source_files'].items():assert after[rel]==digest
assert json.loads(read(R/'mcp.json'))['status']=='PASS'
assert not json.loads(read(R/'tiger-delta.json'))['added']
assert not before.keys()-after.keys()
changes=[p for p in sorted(after) if before.get(p)!=after[p]]
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(a,b)
for rel in changes:cp(C/rel,M/rel);cp(C/rel,repo/rel)
assert man(M)==after
dump(R/'main-merge.json',{'parent':parent,'candidate':str(C),'main':str(M),'prechange':str(B),'candidate_backup':str(F),'changes':[{'file':p,'before':before.get(p),'after':after[p]} for p in changes],'deletions':[],'conflicts':[],'main_equals_candidate':True,'engine_verified':False})
dump(R/'delivery-manifest.json',{'files':after,'engine_verified':False})
package=W/'exports/nesnd-qe1-variable-fix-20261103.zip';files=[]
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(after):
        if rel.split('/')[0] not in {'.metadata','common','events','gfx','gui','localization','map_data'}:continue
        if (M/rel).suffix.lower() in {'.md','.py','.log','.bak'}:continue
        assert 'qa-overlay' not in rel
        z.write(M/rel,rel);files.append(rel)
dump(R/'package.json',{'path':str(package),'sha256':sha(package),'files':files,'qa_tools_included':False})
e=json.loads(read(R/'runtime-save-evidence.json'));assert sha(__import__('pathlib').Path(e['save']))==e['sha256']
support={}
for p in R.iterdir():
    if p.is_file() and p.suffix in {'.md','.json','.txt'} and not p.name.startswith('skill-'):
        support['workbench/'+p.relative_to(W).as_posix()]=p
for name in ['capture_qe1_var_error.py','check_qe1_variable_guards.py','read_qe1_runtime_state.py','fix_qe1_variable_guards.py','validate_qe1_variable_fix.py','probe_qe1_variable_fix.py','record_qe1_variable_fix.py','deliver_qe1_variable_fix.py']:
    p=W/'tools'/name;support['workbench/'+p.relative_to(W).as_posix()]=p
for name in ['syntax-and-routing.md','active-work.md']:
    p=S/'references'/name;support['nesnd-skill/'+p.relative_to(S).as_posix()]=p
mp=repo/'development/snapshot-manifest.json';manifest=json.loads(read(mp));rows={x['path']:x for x in manifest['files']}
for rel,p in support.items():
    cp(p,repo/'development'/rel);rows[rel]={'path':rel,'source':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
manifest.update(files=[rows[k] for k in sorted(rows)],updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),refresh_scope='QE1 inactive journal variable guards; original save and runtime snapshot retained; no game operation.')
dump(mp,manifest)
print('Main delivered:',len(changes),'files;',len(after),'total;',len(files),'package files; save unchanged.')
