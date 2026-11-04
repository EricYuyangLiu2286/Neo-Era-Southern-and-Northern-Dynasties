from sweep_context import *
rows=[]
for p in C.rglob('*.txt'):
 old=B/p.relative_to(C)
 if old.exists() and sha(p)==sha(old):continue
 s=read(p);t='\n'.join(x.rstrip() for x in s.splitlines())+'\n'
 if s!=t:
  assert shape(parse(s))==shape(parse(t))
  before=sha(p);write(p,t);rows.append({'path':p.relative_to(C).as_posix(),'before':before,'after':sha(p),'token_unchanged':True})
dump(R/'format-only.json',rows)
print('Whitespace-only:',len(rows))
