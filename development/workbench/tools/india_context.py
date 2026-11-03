from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
import json,re,shutil
C=W/'exports/india-development-20261103-a';R=W/'reports/india-development-20261103';B=W/'backups/checkpoint-feedback-restoration-delivered-20261103T032233Z/mod'
def put(rel,text):write(C/rel,text.strip()+'\n')
def loc(rows):
 for i,lang in enumerate(['simp_chinese','english']):
  p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzzz_nesnd_india_l_{lang}.yml';s=read(p) if p.exists() else 'l_'+lang+':\n'
  for k,v in rows.items():
   assert not re.search(r'(?m)^\s*'+re.escape(k)+':',s),k
   t=v[i].replace('"','\\"').replace('\n','\\n');s+=f' {k}:0 "{t}"\n'
  write(p,s)
def append(rel,text):write(C/rel,read(C/rel)+'\n'+text.strip()+'\n')
def replace_node(rel,key,text):
 p=C/rel;s=read(p);n=parse(s).get(key);assert n,(rel,key);write(p,s[:n.start]+text.strip()+s[n.end:])
if __name__=='__main__':
 assert not C.exists();assert man(M)==man(B);shutil.copytree(M,C);dump(R/'implementation-baseline.json',{'commit':'a1f2be277000bb228b7e96b9b28621711dc045d4','main':man(M),'source':str(B),'game_launched':False});print('India isolated candidate created')
