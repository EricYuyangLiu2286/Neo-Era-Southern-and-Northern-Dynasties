"""Format edited definition spans only; AST equivalence and quoted lexemes retained."""
import re
def shape(n): return (n.key,n.op,n.value,n.prefix,tuple(shape(x) for x in n.children or []))
def comments(s,level): return ''.join('\t'*level+x.group().strip()+'\n' for x in re.finditer(r'#[^\n]*',s))
def render(n,s,level=0):
 pad='\t'*level
 if n.children is None:return pad+s[n.start:n.end].strip()+'\n'
 # These edited definitions contain ordinary blocks, not rgb/hsv prefixed literals.
 assert not n.prefix
 opening=n.vstart
 assert s[opening]=='{'
 result=pad+s[n.start:opening].strip()+' {\n'; pos=opening+1
 for child in n.children:
  result+=comments(s[pos:child.start],level+1)+render(child,s,level+1);pos=child.end
 return result+comments(s[pos:n.end-1],level+1)+pad+'}\n'
for p in C.rglob('*.txt'):
 rel=p.relative_to(C).as_posix(); old=(B/rel).read_text('utf-8-sig') if (B/rel).exists() else ''
 s=p.read_text('utf-8-sig')
 if s==old:continue
 before=parse(s); old_nodes={n.key:shape(n) for n in parse(old).children}; edits=[]
 for n in before.children:
  if shape(n)!=old_nodes.get(n.key):edits.append((n.start,n.end,render(n,s).rstrip('\n')))
 for start,end,value in sorted(edits,reverse=True):s=s[:start]+value+s[end:]
 assert shape(parse(s))==shape(before),rel
 write(rel,s)
 if not (B/rel).exists():p.write_bytes(b'\xef\xbb\xbf'+p.read_bytes().removeprefix(b'\xef\xbb\xbf'))
