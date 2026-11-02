from pathlib import Path
import json, hashlib, sys
sys.stdout.reconfigure(encoding='utf-8')
b=Path('D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)')
out=Path(__file__).parent
files={
 'H01':('localisation/replace/DMF_bookmark_l_english.yml',[(34,34)]),
 'H02':('history/countries/MUG - Mughliyah.txt',[(1,61)]),
 'H03':('history/countries/TZ1 - TianZhuColonies.txt',[(1,15),(106,117)]),
 'H04':('history/countries/DMF - Dahelianbang.txt',[(123,158),(168,190),(199,220)]),
 'H05':('history/units/MUG_1936_land.txt',[(1,74)]),
 'H06':('history/units/TZ1_1936_land.txt',[(1,56)]),
 'H07':('history/units/TZ1_1936_naval_mtg.txt',[(1,11)]),
 'H08':('localisation/replace/DMF_focus_l_english.yml',[(63,71),(163,168)]),
 'H09':('common/national_focus/Dawu.txt',[(863,884),(2072,2094)]),
 'H10':('localisation/replace/CPC_focus_l_english.yml',[(585,586),(659,660)]),
 'H11':('localisation/replace/KMT_focus_l_english.yml',[(22,23)]),
 'H12':('localisation/replace/CEM_countries_l_english.yml',[(15,18),(67,85),(335,353)]),
 'H13':('localisation/replace/0CE_parties_l_english.yml',[(154,160),(194,199)]),
 'H14':('common/characters/MUG.txt',[(1,16)]),
 'H15':('common/characters/TZ1.txt',[(1,16)]),
 'H16':('localisation/replace/CEM_characters_l_english.yml',[(1,3),(28,28)]),
 'H17':('common/country_tags/CEM_countries.txt',[(13,13),(24,24)]),
 'H18':('common/national_focus/CF1.txt',[(1878,1898)]),
 'H19':('localisation/replace/0CE_focus_l_english.yml',[(1870,1870),(1891,1898),(1917,1922),(1956,1965)]),
}
rows=[]; texts=[]
for k,(name,ranges) in files.items():
 p=b/name; lines=p.read_text(encoding='utf-8-sig').splitlines(); sha=hashlib.sha256(p.read_bytes()).hexdigest()
 rs=[{'line':i,'text':lines[i-1]} for a,z in ranges for i in range(a,min(z,len(lines))+1)]
 rows.append({'id':k,'path':str(p),'sha256':sha,'ranges':ranges,'records':rs})
 texts.extend([f'[{k}] {p}',f'SHA256 {sha}']+[f"L{x['line']}: {x['text']}" for x in rs]+[''])
(out/'hoi4-canon-original-reread.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
(out/'hoi4-canon-excerpts.txt').write_text('\n'.join(texts),encoding='utf-8')
print('Sources',len(rows))
