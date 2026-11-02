from qin_persia_context import *
def indent(text):
 depth=0;out=[]
 for line in text.splitlines():
  st=line.strip()
  if not st:out.append('');continue
  code='';quoted=False;escaped=False
  for ch in st:
   if escaped:escaped=False;continue
   if ch=='\\' and quoted:escaped=True;continue
   if ch=='"':quoted=not quoted;continue
   if not quoted:
    if ch=='#':break
    code+=ch
  leading=len(code)-len(code.lstrip('}'));out.append('\t'*max(0,depth-leading)+st);depth+=code.count('{')-code.count('}')
 assert depth==0
 return '\n'.join(out).rstrip()+'\n'
base,cur=man(B),man(C);proof=[]
for rel,h in cur.items():
 if rel.endswith('.txt') and base.get(rel)!=h:
  p=C/rel;s=read(p);out=indent(s);assert shape(parse(s))==shape(parse(out));write(p,out);proof.append({'file':rel,'AST_unchanged':True})
dump(R/'final-format-proof.json',proof);print('Ordered AST preserved across',len(proof),'formatted scripts.')
