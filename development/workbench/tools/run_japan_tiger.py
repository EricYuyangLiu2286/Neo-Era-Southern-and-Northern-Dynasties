from japan_dev_context import *
phase=sys.argv[1]
assert phase in ('baseline','candidate')
target=B if phase=='baseline' else C
cmd=[str(W/'tools/tiger-1.19.0/vic3-tiger.exe'),'--game',str(G.parent),'--config',str(W/'validation/runs/release-logfix-20261101-a/tiger-load-order.conf'),'--json',str(target)]
with (R/f'tiger-{phase}.json').open('wb') as out,(R/f'tiger-{phase}.stderr.txt').open('wb') as err:
    p=subprocess.run(cmd,stdout=out,stderr=err)
dump(R/f'tiger-{phase}-run.json',{'command':cmd,'returncode':p.returncode,'source_files':man(target),'game_launched':False})
print('Tiger '+phase+' completed; exit '+str(p.returncode))
