from journal_war_context import *
import difflib
bm=man(B);before=man(C)
changed=[p for p,h in before.items() if bm.get(p)!=h]
for rel in changed:
    p=C/rel
    if p.suffix=='.txt':
        old=read(p);new='\n'.join(line.rstrip() for line in old.splitlines())+'\n'
        assert shape(parse(old))==shape(parse(new));write(p,new)
after=man(C);changed={p:h for p,h in after.items() if bm.get(p)!=h}
assert not bm.keys()-after.keys()
data_prefix=['common/history/','common/country_definitions/','common/cultures/','common/religions/','map_data/','gfx/']
protected=[p for p in bm if any(p.startswith(pre) for pre in data_prefix)]
assert all(after[p]==bm[p] for p in protected)
dump(R/'data-preservation.json',{'status':'PASS','files':len(protected),'no_history_map_population_or_graphics_changes':True})
dump(R/'patch-files.json',changed)
diff=''
for rel in changed:
    old=read(B/rel) if (B/rel).exists() else ''
    diff+=''.join(difflib.unified_diff(old.splitlines(True),read(C/rel).splitlines(True),fromfile='baseline/'+rel,tofile='candidate/'+rel))
(R/'gameplay.diff').write_text(diff,'utf-8')
print('Frozen changed files:',len(changed),'total:',len(after),'preserved data files:',len(protected))
for rel in changed:print(rel)
