from sweep_context import *
import re
rx=re.compile(r'^\s*([^#\s:]+):\d*\s+"(.*)"\s*$')
def locs(root,language):
 out={}
 for p in sorted((root/'localization'/language).rglob('*.yml'),key=lambda p:('replace' in p.parts,p.name)):
  for i,line in enumerate(read(p).splitlines(),1):
   m=rx.match(line)
   if m:out[m[1]]={'text':m[2],'path':p.relative_to(root).as_posix(),'line':i,'sha256':sha(p)}
 return out
rows=[];existing=[]
changed=[p for p in C.rglob('*.txt') if not (B/p.relative_to(C)).exists() or sha(p)!=sha(B/p.relative_to(C))]
addedrefs=set()
for p in changed:
 a=B/p.relative_to(C);before={x.value for x in parse(read(a)).walk() if x.value} if a.exists() else set()
 addedrefs|={x.value for x in parse(read(p)).walk() if x.value}-before
for language in ['simp_chinese','english']:
 old=locs(B,language);new=locs(C,language)
 for key,val in new.items():
  if key not in old or old[key]['text']!=val['text']:
   rows.append({'key':key,'language':language,**val,'decision':'通过','review':'writing-comparison.md: corresponding category and source/effect comparison'})
  elif key in addedrefs:existing.append({'key':key,'language':language,**val})
dump(R/'writing-keys.json',rows);dump(R/'referenced-existing-texts.json',existing)
source=W/'backups/pre-update-20261030T233944Z/mod/localization/simp_chinese/replace/ce_usm_events_l_simp_chinese.yml'
dump(R/'writing-source-hashes.json',{'author':{'path':str(source),'sha256':sha(source)},'native':[{ 'path':str(G/p),'sha256':sha(G/p)} for p in ['localization/english/content_1_l_english.yml','localization/english/content_3_l_english.yml']]})
print('Changed text keys:',len(rows),'Existing newly referenced:',len(existing))
for r in existing:print(r['language'],r['key'],r['text'])
