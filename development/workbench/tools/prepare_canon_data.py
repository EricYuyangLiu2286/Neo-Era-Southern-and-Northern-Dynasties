"""Bounded data transformations, not gameplay generation: resolved cultures, six native law guards,
seven existing resettlement event gates, and population sizes with fixed region totals.
Run once against the named candidate; manifests retain every changed source/value."""
from canon_routes_context import *
from collections import defaultdict
import numpy as np
from scipy.optimize import linprog

def resolved(folder):
 out={}
 for root in [G,C]:
  for p in sorted((root/folder).glob('*.txt')):
   for n in parse(read(p)).children:
    if not n.children:continue
    k=n.key.removeprefix('REPLACE:').removeprefix('REPLACE_OR_CREATE:')
    out[k]=(n,p)
 return out
cult=resolved('common/cultures');traits=resolved('common/discrimination_traits')
def category(k):
 n,p=cult[k];herit=n.scalar('heritage');group=traits[herit][0].scalar('trait_group') if herit in traits else None
 if k=='manchu' or herit=='heritage_mongolian':return 'manchu_mongol'
 if herit=='heritage_han':return 'han'
 if group=='heritage_group_indigenous_american':return 'native'
 if group=='heritage_group_european':return 'european'
 return 'other'
cats={k:category(k) for k in cult}
dump(R/'culture-categories.json',{k:{'group':v,'source':str(cult[k][1]),'source_sha256':sha(cult[k][1])} for k,v in cats.items()})
lines=['# Generated from resolved GAME+MOD cultures; only applied to HUS while its registration law is active.']
for mode,values in [('hierarchy',{'han':85,'manchu_mongol':55,'native':35,'european':15}),('manchu',{'han':85,'manchu_mongol':80,'native':35,'european':15}),('native',{'han':85,'manchu_mongol':55,'native':80,'european':15})]:
 lines.append('nesnd_hus_acceptance_'+mode+' = {')
 for k in sorted(cats):
  if cats[k] in values:lines.append(f'    country_{k}_cultural_acceptance_add = {values[cats[k]]}')
 lines.append('}')
write(C/'common/static_modifiers/nesnd_hus_culture_tiers.txt','\n'.join(lines)+'\n')

# Preserve every native law field; add one conditional guard to normal enactment and imposition.
src=G/'common/laws/00_citizenship.txt';s=read(src);patches=[]
for n in parse(s).children:
 if not n.key.startswith('law_'):continue
 assert n.get('can_enact') is None
 pos=s.index('{',n.start)+1;patches.append((pos,pos,'\n    can_enact = { nesnd_hus_citizenship_unlocked = yes }'))
 impose=n.get('can_impose')
 if impose:
  pos=s.index('{',impose.start)+1;patches.append((pos,pos,'\n        nesnd_hus_citizenship_unlocked = yes'))
 patches.append((n.start,n.start+len(n.key),'REPLACE:'+n.key))
for a,b,t in sorted(patches,reverse=True):s=s[:a]+t+s[b:]
write(C/'common/laws/zzzz_nesnd_hus_citizenship_lock.txt',s)

# Native events have no verified REPLACE loader; preserve the same-path source and disable all seven removal-chain events.
src=G/'events/native_resettlement.txt';s=read(src);patches=[]
for n in parse(s).children:
 if not n.key.startswith('native_resettlement.'):continue
 tr=n.get('trigger')
 if tr:
  pos=s.index('{',tr.start)+1;patches.append((pos,pos,'\n        always = no # Replaced by the authored khanate/refugee route.'))
 else:
  pos=s.index('{',n.start)+1;patches.append((pos,pos,'\n    trigger = { always = no }'))
for a,b,t in sorted(patches,reverse=True):s=s[:a]+t+s[b:]
write(C/'events/native_resettlement.txt',s)

records=[];texts={}
effective_pops={p.name:p for p in (G/'common/history/pops').glob('*.txt')}
effective_pops.update({p.name:p for p in (C/'common/history/pops').glob('*.txt')})
for src in sorted(effective_pops.values()):
 p=C/'common/history/pops'/src.name
 s=read(src);texts[p]=s
 for pops in parse(s).all('POPS'):
  for region in pops.children:
   for country in region.children or []:
    if not country.key or not country.key.startswith('region_state:'):continue
    tag=country.key.split(':')[1]
    if tag not in ['HUS','MEX','NPU','SPU']:continue
    items=[]
    for n in country.all('create_pop'):
     c=n.scalar('culture');z=n.get('size');assert c in cats and z is not None,(p,region.key,c)
     items.append({'node':n,'size_node':z,'culture':c,'group':'M' if cats[c]=='manchu_mongol' else 'N' if cats[c]=='native' else 'O','size':int(z.value)})
    records.append({'path':p,'region':region.key,'country':tag,'items':items,'total':sum(x['size'] for x in items)})

def allocate(total,weights):
 assert total>=len(weights)
 weights=np.array(weights,dtype=float);w=weights/weights.sum();raw=w*(total-len(weights));out=np.floor(raw).astype(int)+1
 for i in sorted(range(len(weights)),key=lambda i:(-(raw[i]-(out[i]-1)),i))[:int(total-out.sum())]:out[i]+=1
 assert int(out.sum())==total
 return list(map(int,out))

audit=[];value_edits=defaultdict(list)
for tags,m_share,n_share in [(['HUS'],.30,.20),(['MEX'],None,.55),(['NPU','SPU'],None,.70)]:
 rs=[r for r in records if r['country'] in tags];N=len(rs);assert N>0,tags;total=sum(r['total'] for r in rs)
 m0=np.array([sum(x['size'] for x in r['items'] if x['group']=='M') for r in rs]);n0=np.array([sum(x['size'] for x in r['items'] if x['group']=='N') for r in rs])
 mt=round(total*m_share) if m_share is not None else int(m0.sum());nt=round(total*n_share)
 assert mt>=m0.sum() and nt>=n0.sum()
 mi=m0*mt/m0.sum() if m0.sum() else m0;ni=n0*nt/n0.sum()
 # M,N and four L1 slack variables per region; region totals and old geography remain fixed.
 costs=np.tile([0.,0.,1.,1.,1.,1.],N);eq=[];rhs=[];ub=[];urb=[];bounds=[]
 for i,r in enumerate(rs):
  a=np.zeros(6*N);a[6*i]=1;a[6*i+2]=-1;a[6*i+3]=1;eq.append(a);rhs.append(mi[i])
  a=np.zeros(6*N);a[6*i+1]=1;a[6*i+4]=-1;a[6*i+5]=1;eq.append(a);rhs.append(ni[i])
  a=np.zeros(6*N);a[6*i:6*i+2]=1;ub.append(a);urb.append(r['total']-sum(x['group']=='O' for x in r['items']))
  bounds.extend([(int(m0[i]),None) if m0[i]>0 else (0,0),(int(n0[i]),None) if n0[i]>0 else (0,0),(0,None),(0,None),(0,None),(0,None)])
 for j,target in [(0,mt),(1,nt)]:a=np.zeros(6*N);a[j::6]=1;eq.append(a);rhs.append(target)
 solution=linprog(costs,A_ub=np.array(ub),b_ub=np.array(urb),A_eq=np.array(eq),b_eq=np.array(rhs),bounds=bounds,method='highs')
 assert solution.success,solution.message
 raw=solution.x.reshape(N,6)[:,:2];counts=np.floor(raw+1e-7).astype(int)
 for j,target in [(0,mt),(1,nt)]:
  remain=target-int(counts[:,j].sum())
  for i in sorted(range(N),key=lambda i:(-(raw[i,j]-counts[i,j]),i)):
   if remain and (m0[i] if j==0 else n0[i])>0 and counts[i].sum()<urb[i]:counts[i,j]+=1;remain-=1
  assert remain==0
 for i,r in enumerate(rs):
  targets={'M':int(counts[i,0]),'N':int(counts[i,1]),'O':r['total']-int(counts[i].sum())};before={g:sum(x['size'] for x in r['items'] if x['group']==g) for g in targets}
  for group,t in targets.items():
   xs=[x for x in r['items'] if x['group']==group]
   if not xs:assert t==0;continue
   for x,size in zip(xs,allocate(t,[x['size'] for x in xs])):
    n=x['size_node'];value_edits[r['path']].append((n.vstart,n.vend,str(size)))
  audit.append({'country':r['country'],'region':r['region'],'total_before':r['total'],'total_after':sum(targets.values()),'before':before,'after':targets})
 print(tags,'total',total,'M',mt,'N',nt)
for p,patches in value_edits.items():
 s=texts[p]
 for a,b,t in sorted(patches,reverse=True):s=s[:a]+t+s[b:]
 write(p,s)
dump(R/'population-rebalance.json',{'method':'Within existing region-country pop groups; L1 nearest proportional growth, integer apportionment, no new or deleted pop records; regional total fixed','targets':{'HUS':{'M':.30,'N':.20},'MEX':{'N':.55},'NPU_SPU':{'N':.70}},'regions':audit,'files':{str(p.relative_to(C)):sha(p) for p in value_edits}})
print('Data changes complete; population owner-regions:',len(audit))
