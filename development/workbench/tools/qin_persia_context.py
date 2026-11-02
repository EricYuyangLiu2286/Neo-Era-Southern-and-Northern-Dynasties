from pathlib import Path
import sys,json,hashlib,shutil
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
B=W/'backups/pre-change-qin-persia-campaign-20261102T022528Z/mod';C=W/'exports/qin-persia-campaign-20261102-a';R=W/'reports/qin-persia-20261102';G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3');D=W/'references/engine-docs-1.13.11-20261031'
sys.path.insert(0,str(S/'scripts'));from pdx import parse
def read(p):return p.read_text('utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def man(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
def write(p,s):
 old=p.read_bytes() if p.exists() else b'\xef\xbb\xbf';s=s.replace('\r\n','\n');s=s.replace('\n','\r\n') if b'\r\n' in old else s
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((b'\xef\xbb\xbf' if old.startswith(b'\xef\xbb\xbf') else b'')+s.encode())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
def put(rel,s):write(C/rel,s.strip()+'\n')
def shape(n):return n.key,n.op,n.value,tuple(shape(a) for a in n.children or [])
if __name__=='__main__':
 assert not C.exists();assert man(M)==man(B);shutil.copytree(M,C);R.mkdir(parents=True,exist_ok=True)
 dump(R/'baseline.json',{'parent':'c0e11fe','backup':str(B),'files':man(B),'game_launched':False})
 print('Independent candidate created; main untouched.')
