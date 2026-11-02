from pathlib import Path
import sys,json,hashlib,shutil
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
B=W/'backups/pre-change-qin-planning-docs-20261102T004019Z/mod';C=W/'exports/ui-poland-tributary-20261102-a';R=W/'reports/ui-poland-tributary-20261102';G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game');S=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3')
sys.path.insert(0,str(S/'scripts'));from pdx import parse
def read(p):return p.read_text('utf-8-sig')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def man(root):return {p.relative_to(root).as_posix():sha(p) for p in root.rglob('*') if p.is_file()}
def write(p,s):
 old=p.read_bytes() if p.exists() else b'\xef\xbb\xbf';bom=old.startswith(b'\xef\xbb\xbf');s=s.replace('\r\n','\n')
 if b'\r\n' in old:s=s.replace('\n','\r\n')
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((b'\xef\xbb\xbf' if bom else b'')+s.encode())
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def replace_def(rel,key,body):
 p=C/rel;s=read(p);n=parse(s).get(key);assert n,key;write(p,s[:n.start]+body.strip()+s[n.end:])
if __name__=='__main__':
 assert man(M)==man(B);assert not C.exists();shutil.copytree(M,C);R.mkdir(parents=True,exist_ok=True)
 dump(R/'baseline.json',{'parent':'044de73e0e0fb516a4b8f36384d0d815a86802f7','backup':str(B),'files':man(B),'game_launched':False})
