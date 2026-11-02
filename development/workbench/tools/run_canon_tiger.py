from canon_prose_context import *
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(E)]
before=man(E)
with (R/'tiger-candidate.json').open('wb') as out,(R/'tiger-candidate.stderr.txt').open('wb') as err:
    p=subprocess.run(cmd,stdout=out,stderr=err)
dump(R/'tiger-run.json',{'command':cmd,'returncode':p.returncode,'source_files':before,'unchanged':before==man(E),'game_launched':False})
print('Tiger completed; classify diagnostics separately. Exit',p.returncode)
