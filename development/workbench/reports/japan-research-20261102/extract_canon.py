from pathlib import Path
import hashlib, json, re, zipfile, posixpath
from xml.etree import ElementTree as ET
from PIL import Image

OUT = Path(__file__).parent
CANON = Path('D:/Users/Eric Liu/OneDrive/文档/文案-EMP2286/Modings/北明战国世')
MODINGS = CANON.parent
HOI = Path('D:/Users/Eric Liu/OneDrive/Documents/Modings/CelestialDynastyOfMan(Old Abandoned Project)')
PAT = re.compile('日本|九州|丰臣|德川|毛利|李汉涵|林汉涵|朝鲜|幕府|东洲|华美')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
manifest = []
def register(p):
    d={'path':str(p), 'sha256':sha(p),'bytes':p.stat().st_size}
    manifest.append(d)
    return d
ppt=CANON/'北明ppet.pptx'
register(ppt)
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(ppt) as z:
    allslides=[]
    for name in sorted((n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)),key=lambda n:int(re.search(r'(\d+)\.xml',n).group(1))):
        n=int(re.search(r'(\d+)\.xml',name).group(1))
        ps=[''.join(p.itertext()) for p in []]
        ps=[''.join(t.text or '' for t in p.findall('.//a:t',ns)) for p in ET.fromstring(z.read(name)).findall('.//a:p',ns)]
        allslides.append({'slide':n,'part':name,'paragraphs':[{'p':i+1,'text':s} for i,s in enumerate(ps)]})
    (OUT/'ppt-original-reread.json').write_text(json.dumps(allslides,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=[]
    for s in allslides:
        if any(PAT.search(p['text']) for p in s['paragraphs']):
            lines.extend([f"[slide {s['slide']} p{p['p']}] {p['text']}" for p in s['paragraphs'] if p['text']])
    (OUT/'ppt-relevant-full-slides.txt').write_text('\n'.join(lines),encoding='utf-8')
docs=[]
for fname in ['北明人物列传.docx','朱班博传（上）.docx','朱班博传（中）.docx','海军人物.docx','时间线 - 副本.docx']:
    p=CANON/fname
    info=register(p)
    cache=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench/research/20261031')/(p.stem+'.json')
    info['cache_sha_matches']=json.loads(cache.read_text(encoding='utf-8'))['sha256']==info['sha256']
    with zipfile.ZipFile(p) as z:
        wn={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        ps=[''.join(t.text or '' for t in x.findall('.//w:t',wn)) for x in ET.fromstring(z.read('word/document.xml')).findall('.//w:p',wn)]
        matches=[{'paragraph':i+1,'text':t} for i,t in enumerate(ps) if PAT.search(t)]
        docs.append({'source':str(p),'sha256':info['sha256'],'matches':matches})
(OUT/'docx-original-reread.json').write_text(json.dumps(docs,ensure_ascii=False,indent=2),encoding='utf-8')
for fname in ['伟大和平和战后局势（1950）.png','1835年的南明联邦.png','1936年.png','1936 of Another.png','第五次、第六次中原大战时的亚洲.png']:
    p=MODINGS/fname
    d=register(p)
    with Image.open(p) as im: d['dimensions']=im.size
with Image.open(MODINGS/'1835年的南明联邦.png') as im:
    im.crop((3700,2500,5600,3550)).save(OUT/'1835-japan-korea-crop.png')
    im.crop((3640,3500,4100,4250)).save(OUT/'1835-map-note-crop.png')
with Image.open(MODINGS/'伟大和平和战后局势（1950）.png') as im:
    im.crop((5650,750,6200,1120)).save(OUT/'1950-japan-korea-crop.png')
    im.crop((60,180,1150,680)).save(OUT/'1950-legend-east-crop.png')
    im.crop((60,1600,1400,2360)).save(OUT/'1950-legend-west-crop.png')
for rel in ['common/country_tags/CEM_countries.txt','common/national_focus/Dawu.txt','history/countries/DMF - Dahelianbang.txt','history/countries/JAP - Japan.txt','history/states/282-Japan.txt','history/states/533-Akita.txt','history/states/536-Hokkaido.txt','history/states/877-jianghu.txt','history/states/881-Huanghaidao.txt','localisation/replace/DMF_bookmark_l_english.yml','localisation/replace/DMF_focus_l_english.yml','localisation/replace/DMF_ideas_l_english.yml','localisation/replace/CEM_countries_l_english.yml','localisation/replace/CEM_state_names_l_english.yml']:
    register(HOI/rel)
(OUT/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(manifest,ensure_ascii=False,indent=2))
