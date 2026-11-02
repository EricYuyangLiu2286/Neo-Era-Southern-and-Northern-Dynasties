from pathlib import Path
import re, json, hashlib
W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
M=W.parent/'mod/Neo-Era Southern and Northern Dynasties'
C=W/'exports/japan-development-20261102-a'
B=W/'backups/pre-update-20261030T233944Z/mod'
R=W/'reports/canon-prose-20261102'
rx=re.compile(r'^\s*([^#\s][^:]*):\s*\d*\s*"(.*)"\s*$')
def loc(root,lang):
 out={}; defs=[]
 for p in sorted((root/'localization'/lang/'replace').rglob('*.yml'),key=lambda x:x.name):
  for n,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
   m=rx.match(line)
   if m:
    d={'key':m[1],'text':m[2],'file':str(p.relative_to(root)).replace('\\','/'),'line':n}
    defs.append(d);out[m[1]]=d
 return out,defs
allloc={}
for label,path in [('main',M),('candidate',C),('baseline',B)]:
 allloc[label]={}
 for lang in ['simp_chinese','english']:
  allloc[label][lang]=loc(path,lang)
keys=set()
for d in allloc['candidate']['simp_chinese'][1]:
 if 'cne_' in Path(d['file']).name or re.match(r'(nesnd_land_|nesnd_reform_|nesnd_crisis\.(20|30|31|32|33)\.|NSX$|NSX_ADJ$|NHB$|NHB_ADJ$|NSD$|NSD_ADJ$|nesnd_army_audit$|nesnd_secession_disorder$)',d['key']): keys.add(d['key'])
rows=[]
for k in sorted(keys):
 row={'key':k}
 for lang in ['simp_chinese','english']:
  a=allloc['candidate'][lang][0].get(k);b=allloc['baseline'][lang][0].get(k);m=allloc['main'][lang][0].get(k)
  row[lang]={'candidate':a,'main':m,'baseline':b,'origin':'baseline_unchanged' if a and b and a['text']==b['text'] else ('changed_since_baseline' if b else 'added_since_baseline'),'layers':[d for d in allloc['candidate'][lang][1] if d['key']==k]}
 rows.append(row)
(R/'cne-inventory-data.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print('keys',len(rows))
for lang in ['simp_chinese','english']:
 print(lang,{v:sum(r[lang]['origin']==v for r in rows) for v in ['baseline_unchanged','changed_since_baseline','added_since_baseline']})
 print('main-candidate effective diffs',[(r['key'],r[lang]['candidate']['file'] if r[lang]['candidate'] else None) for r in rows if r[lang]['candidate'] and r[lang]['main'] and r[lang]['candidate']['text']!=r[lang]['main']['text']])
