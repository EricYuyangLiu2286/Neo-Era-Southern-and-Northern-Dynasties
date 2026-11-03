from india_context import *
from pdx import LEX
import re

def shape(n):return n.key,n.value,n.op,n.prefix,tuple(shape(x) for x in n.children or [])
def braces(line):
    return [m.group() for m in LEX.finditer(line) if m.group() in ('{','}')]
base=man(M);cand=man(C);changed=[]
for rel in sorted(cand):
    if not rel.endswith('.txt') or not rel.startswith(('common/','events/')) or base.get(rel)==cand[rel]:continue
    p=C/rel;s=read(p);before=shape(parse(s));depth=0;out=[]
    for line in s.splitlines():
        raw=line.strip()
        if not raw:out.append('');continue
        if re.fullmatch(r'(?:}\s*)+',raw):
            for _ in braces(raw):
                depth-=1;assert depth>=0,(rel,line)
                out.append('    '*depth+'}')
            continue
        leading=len(re.match(r'^(?:}\s*)*',raw).group().replace(' ',''))
        # The prefix only contains literal closing braces and whitespace.
        leading=raw[:len(re.match(r'^(?:}\s*)*',raw).group())].count('}')
        out.append('    '*max(0,depth-leading)+raw)
        bs=braces(raw);depth+=bs.count('{')-bs.count('}')
    assert depth==0,rel
    final='\n'.join(out)+'\n';assert before==shape(parse(final)),rel
    if final!=s:write(p,final);changed.append({'file':rel,'before':cand[rel],'after':sha(p)})
dump(R/'india-formatting-semantic-equivalence.json',{'files':changed,'all_ast_identical':True,'game_launched':False})
print('Indented',len(changed),'changed scripts; all ordered ASTs identical.')
