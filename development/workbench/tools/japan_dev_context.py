from qin_persia_context import W, M, G, S, D, read, write, sha, man, dump, parse
from pathlib import Path
import json, shutil, subprocess, sys
B = W/'backups/pre-change-japan-development-20261102T172647Z/mod'
C = W/'exports/japan-development-20261102-a'
R = W/'reports/japan-development-20261102'
PARENT = 'c4bbc194ddafcb2bb62f2bb89746c95f0b7b7f49'
def put(rel, body):
    write(C/rel, body.strip()+'\n')
def nodes(rel):
    return parse(read(C/rel))
def replace_top(rel, key, text):
    p=C/rel; s=read(p)
    import re
    match=re.search(r'(?m)^'+re.escape(key)+r'\s*=\s*\{',s)
    assert match,(rel,key)
    start=match.start(); depth=0; quoted=False; escaped=False; comment=False
    for i in range(s.index('{',match.start()),len(s)):
        c=s[i]
        if comment:
            if c=='\n':comment=False
            continue
        if quoted:
            if escaped:escaped=False
            elif c=='\\':escaped=True
            elif c=='"':quoted=False
            continue
        if c=='#':comment=True
        elif c=='"':quoted=True
        elif c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:
                write(p,s[:start]+text.strip()+s[i+1:]);return
    raise AssertionError('unclosed '+key)
if __name__=='__main__':
    assert not C.exists()
    before=man(B); assert before==man(M)
    repo=W/'projects/nesnd-repository'
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo).decode().strip()==PARENT
    assert not subprocess.check_output(['git','status','--porcelain'],cwd=repo).strip()
    shutil.copytree(M,C);R.mkdir(parents=True,exist_ok=True)
    dump(R/'baseline.json',{'commit':PARENT,'backup':str(B),'candidate':str(C),'main_files':before,'game_launched':False})
    print('Independent Japan implementation candidate created; main unchanged.')
