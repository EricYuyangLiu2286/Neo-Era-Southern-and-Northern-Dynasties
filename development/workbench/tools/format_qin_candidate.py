from qin_persia_build_support import *
p=C/'common/scripted_effects/nesnd_qe1_fracture.txt';s=read(p).replace('create_country = { tag = QRC origin = root','save_scope_as = nesnd_qe1_prewar_country\n create_country = { tag = QRC origin = root').replace('limit = { root = { var:nesnd_qe1_balance <= -35 } }','limit = { scope:nesnd_qe1_prewar_country = { var:nesnd_qe1_balance <= -35 } }');write(p,s)
p=C/'common/scripted_progress_bars/nesnd_qe1_agendas.txt';write(p,read(p).replace('default_green = yes','double_sided_gold = yes'))
p=C/'common/scripted_progress_bars/nesnd_qe1_identity.txt';write(p,read(p).replace('default_green = no','default_bad = yes'))
loc('nesnd_qe1_identity.1.d',"[SCOPE.sStateRegion('nesnd_qe1_declining_region').GetName]的村社与军屯正在重述自己的来历。旧时的族名、经文与乡里关系重新成为人们彼此信任的凭据。当地约半数西域汉羌如今重新以[SCOPE.sCulture('nesnd_qe1_return_culture').GetName]自称，信奉[SCOPE.sReligion('nesnd_qe1_return_religion').GetName]。")
flush_loc()
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
base=man(B);current=man(C);proof=[]
for rel,h in current.items():
 if rel.endswith('.txt') and base.get(rel)!=h:
  p=C/rel;s=read(p);formatted=indent(s);assert shape(parse(s))==shape(parse(formatted));write(p,formatted);proof.append({'file':rel,'AST_unchanged':True})
dump(R/'format-proof.json',proof);print('Formatted',len(proof),'changed script files with identical ordered AST.')
