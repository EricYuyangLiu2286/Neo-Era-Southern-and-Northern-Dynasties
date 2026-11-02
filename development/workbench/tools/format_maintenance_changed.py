from maintenance_20261102_context import *
def shape(n):return n.key,n.op,n.value,tuple(shape(x) for x in n.children or [])
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
 return '\n'.join(out)+'\n'
paths={x['locations'][0][1].replace('\\','/') for x in json.loads(read(R/'tiger-delta.json'))['added'] if x['key']=='brace-placement'}
out=[]
for rel in sorted(paths):
 p=C/rel;s=read(p);new=indent(s);assert shape(parse(s))==shape(parse(new));write(p,new);out.append({'file':rel,'AST_unchanged':True})
dump(R/'final-format-proof.json',out);print('Indentation normalized without AST changes:',len(out))
