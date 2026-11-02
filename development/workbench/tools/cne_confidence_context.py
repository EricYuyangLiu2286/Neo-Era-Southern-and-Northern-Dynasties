from pathlib import Path
import sys,json,hashlib,shutil
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
B=W/'backups/pre-change-cne-confidence-20261101T235300Z/mod'
C=W/'exports/cne-confidence-20261101-a'
R=W/'reports/cne-confidence-20261101'
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
sys.path.insert(0,str(S/'scripts'))
from pdx import parse
def read(p):return p.read_text('utf-8-sig')
def write(p,s):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'\xef\xbb\xbf'+s.encode('utf-8'))
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
def replace_def(rel,key,body):
 p=C/rel;s=read(p);n=parse(s).get(key);assert n,key;write(p,s[:n.start]+body.strip()+s[n.end:])
if __name__=='__main__':
 R.mkdir(parents=True,exist_ok=True)
 assert manifest(M)==manifest(B)
 assert not C.exists();shutil.copytree(M,C)
 dump(R/'baseline.json',{'parent_commit':'bbe7ebe0fec2067da13022a74aef49ed4dcc4be6','backup':str(B),'candidate':str(C),'files':manifest(B),'game_launched':False})
