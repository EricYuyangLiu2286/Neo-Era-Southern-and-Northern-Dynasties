"""Exact design arithmetic, never a Victoria 3 execution or peace forecast."""
from pathlib import Path
from itertools import product
from math import sqrt
import json
import numpy as np
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
R=W/'reports/south-allegiance-plan-20261101'
rows=json.loads((R/'membership-inventory.json').read_text('utf-8'))['rows']
bytag={x['tag']:x for x in rows}
core={x['tag'] for x in rows if x['sinosphere_primary_cultures'] and x['capital_in_project_china_list']}
assert core=={'SIH','HNA','GNG'}
regional={'BUR','SIA','DAI'};japan={'JAP'};overseas=set(bytag)-core-regional-japan
def weights(groups,quotas,raw):
 out={}
 for g,ts in groups.items():
  total=sum(raw(t) for t in ts)
  for t in ts:out[t]=quotas[g]*raw(t)/total
 assert abs(sum(out.values())-100)<1e-9
 return out
def raw(t):
 if t in core:return 2 if t=='GNG' else 3
 if t=='JAP':return 1
 v=max(.25,min(3,sqrt(bytag[t]['population']/1e6)))
 return min(3,v*1.25) if t in overseas and bytag[t]['sinosphere_primary_cultures'] else v
old=weights({'core':core,'japan':japan,'overseas':regional|overseas},{'core':50,'japan':20,'overseas':30},lambda t:3 if t in {'SIH','HNA','PHI','DEI','YN1'} else 2 if t in {'GNG','BUR','SIA','DAI','TRA','MYS'} else 1)
new=weights({'core':core,'japan':japan,'regional':regional,'overseas':overseas},{'core':60,'japan':15,'regional':15,'overseas':10},raw)
results=[]
for attitude_factor,phase,missing,rm in product([1,.1875],['initial','rejected'],['W','I'],[.1,.2,.4]):
 aq=30*attitude_factor/(30*attitude_factor+70)
 ac=20*attitude_factor/(20*attitude_factor+80)
 profiles={
  'SIH':{'M':.9,'W':.05,'P':.05*aq,'I':.05*(1-aq)},
  'HNA':{'M':.9+.05*(1-ac),'W':.05,'P':.05*ac},
  'GNG':{'M':.95,'W':.05},
  'JAP':{'M':.5,'N':.2,'I':.3} if phase=='rejected' else {'M':.8,'N':.1,missing:.1},
  'PHI':{'M':.5,'N':.4,'I':.1},'YN1':{'M':.3,'N':.4,'I':.3},
 }
 for t in regional:profiles[t]={'M':rm,'W':.1,'N':.9-rm}
 for t in overseas-{'PHI','YN1'}:profiles[t]={'W':1}
 assert set(profiles)==set(bytag)
 assert all(abs(sum(p.values())-1)<1e-9 for p in profiles.values())
 variable=sorted(t for t,p in profiles.items() if len(p)>1)
 fixed=set(profiles)-set(variable)
 combinations=list(product(*(profiles[t].items() for t in variable)))
 states=np.array([[v[0] for v in c] for c in combinations]);pr=np.prod([[v[1] for v in c] for c in combinations],axis=1)
 assert abs(float(pr.sum())-1)<1e-9
 no_secession=~np.any((states=='I')|(states=='P'),axis=1)
 core_w=np.all(states[:,[variable.index(t) for t in sorted(core)]]=='W',axis=1)
 japan_w=states[:,variable.index('JAP')]=='W'
 for mode,ww in [('old',old),('B',new),('C',new)]:
  ws=np.array([ww[t] for t in variable]);mshare=(states=='M')@ws
  wshare=(states=='W')@ws+sum(ww[t] for t in fixed)
  for env in ['snapshot','best']:
   f,d,mil=(20,12.4,12.7) if env=='snapshot' else (20,20,20)
   if mode=='old':ms=f+d+20+.4*mshare;wscore=f+d+mil+.4*wshare;threshold=85;accord=75;lead=20
   else:ms=(f+d)*.5+10+.7*mshare;wscore=(f+d+mil)*.5+.7*wshare;threshold=88 if mode=='B' else 90;accord=85 if mode=='B' else 90;lead=25
   gate=(ms>=threshold-1e-9)&(ms-wscore>=lead-1e-9)&(mshare>=accord-1e-9)
   wg=(wscore>=threshold-1e-9)&(wscore-ms>=lead-1e-9)&(wshare>=(80 if mode=='old' else accord)-1e-9)&core_w&japan_w
   p=float(pr[gate].sum())
   results.append(dict(mode=mode,environment=env,attitude_factor=attitude_factor,JAP_phase=phase,JAP_missing_10_sensitivity=missing,regional_M_sensitivity=rm,M_mean=float(pr@ms),W_mean=float(pr@wscore),M_max=float(ms.max()),M_gate_upper_bound=p,M_gate_without_secession_upper_bound=float(pr[gate&no_secession].sum()),two_independent_draws_upper_bound=1-(1-p)**2,W_gate_including_core_and_Japan_consent_upper_bound=float(pr[wg].sum()),QE1_accept_given_request=aq,CNE_accept_given_request=ac))
report={'validation':'ARITHMETIC_ONLY / ENGINE_NOT_RUN','supersedes':'calibration.json (old SIH/HNA fixed-M assumption, preserved)','assumptions':['All aligned members sign: an optimistic bound, not event acceptance or peace probability.','12-month hold, laws, actual diplomatic changes, pressure and pre-existing human choices are NOT simulated.','BUR/SIA/DAI Ming 10/20/40%, Wu 10%, remainder neutral are unapproved sensitivity inputs.','JAP initial missing 10% tested as Wu or independence; accepted-claim profile is unspecified.','Patron acceptance uses normalized AI option weights; P denotes accepted foreign protection, not Ming/Wu support.','Attitude factors 1 and .1875 are proposed neutral / mutually friendly scenarios, not read from a game save.','New groups: mainland Sino-primary core 60, Japan 15, regional kingdoms 15, residual overseas 10. Size proxies are initial population, not dynamic game forecasts.','Two-draw result assumes independent whole-profile draws, then stopping envoys; human choices, fixed completed missions and surviving 12 months may make actual behavior different.'],'weights':{t:dict(old=old[t],proposed=new[t]) for t in sorted(bytag)},'results':results}
(R/'calibration-v2.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
for r in results:
 if r['attitude_factor']==1 and r['regional_M_sensitivity']==.2 and r['JAP_missing_10_sensitivity']=='W':
  print(json.dumps({k:round(v,7) if isinstance(v,float) else v for k,v in r.items()},ensure_ascii=False))
