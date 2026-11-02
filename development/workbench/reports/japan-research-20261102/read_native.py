import json,sys
from pathlib import Path
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts'); import pdx
G=Path(r'D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
def show(p,ids=None,fields=None):
 t,r=pdx.read(G/p)
 for n in r.children:
  if n.children is None or (ids and n.key not in ids):continue
  print('\n',p,':',t.count('\n',0,n.start)+1,n.key)
  if fields:
   for c in n.children:
    if c.key in fields:print(t[c.start:c.end])
  else:print(t[n.start:n.end])
if __name__=='__main__':
 show(sys.argv[1],sys.argv[2].split(',') if len(sys.argv)>2 and sys.argv[2]!='-' else None,sys.argv[3].split(',') if len(sys.argv)>3 else None)
