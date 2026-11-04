"""Root repairs after independently reproducing review findings; no gameplay tuning."""
from pathlib import Path
import json,re,sys,hashlib,shutil
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench');C=W/'exports/maintenance-current';R=W/'reports/branch-naming-cleanup-20261104'
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
def read(p):return p.read_text(encoding='utf-8-sig')
def write(p,s):p.write_bytes(b'\xef\xbb\xbf'+s.replace('\r\n','\n').replace('\n','\r\n').encode())
shutil.copy2(R/'candidate-freeze.json',R/'candidate-freeze-initial.json')
p=C/'common/dynamic_country_names/ce_dynamic_country_names.txt';s=read(p);nodes=[n for n in parse(s).children if n.key in ('REPLACE:HNA','REPLACE:SIH')]
assert len(nodes)==2
for n in sorted(nodes,key=lambda n:n.start,reverse=True):s=s[:n.start]+s[n.end:]
write(p,s)
edits={}
def pair(key,zh,en):edits[('simp_chinese',key)]=zh;edits[('english',key)]=en
pair('nesnd_egypt.4.d','大学培养的技术人才开始进入工场，工具厂和新兴产业也有了稳定的劳动力。埃及正在形成自己的生产与教育力量，今后的建设将有更多本国技师与工人参与。',"Graduates are entering the workshops, and toolmakers and new industries have established a steady workforce. Egypt is developing its own capacity to teach and manufacture, with more local engineers and workers able to take part in its development.")
pair('nesnd_american_restoration.6.t','复统之争暂告一段落','The Restoration Dispute Subsides')
pair('nesnd_american_restoration.6.d','复统之争已经暂告一段落。政府未能以这场对抗实现统一，必须依据眼前的疆界与各地势力，重新安排今后的方略。',"The restoration dispute has subsided. The government has not achieved unification through this confrontation. It must reconsider its course in light of the present borders and the forces that now hold power.")
english={
'HUB_NAME_STATE_WESTERN_HUBEI_city':'Jingzhou','HUB_NAME_STATE_DZUNGARIA_city':'Wusun','HUB_NAME_STATE_DZUNGARIA_farm':'Eastern Dzungaria Farms','HUB_NAME_STATE_DZUNGARIA_wood':'Zhundong Forests','HUB_NAME_STATE_CALIFORNIA_mine':'Beiyuan Mines','HUB_NAME_STATE_CALIFORNIA_wood':'Dayuan River Forests',
'STATE_GUANGXI':'Guinan','STATE_SOUTHERN_MANCHURIA':'Jilin','STATE_NORTHERN_MANCHURIA':'Heilongjiang','STATE_SHANXI':'Jinzhong','STATE_XIAN':'Guanzhong','STATE_CHONGQING':'Chuandong','STATE_JIANGXI':'Ganbei','STATE_WESTERN_HUBEI':'Jingzhou',
'nesnd_land_status_petition':"#bold Local petitions have arrived.#! Continue the survey or hear appeals to reduce Local Disorder.\\n#tooltippable #tooltip:[ROOT.GetCountry.GetTooltipTag],nesnd_land_rules Reform conditions#!#!",
'nesnd_land_survey_requirements':'The Land Rights Revolution is underway; [concept_bureaucracy] is positive; no separate survey grant is currently in effect.',
'nesnd_land_review_requirements':'The Land Rights Revolution is underway; Local Disorder is at least #v 15#!; no land appeals office is currently in effect.',
'nesnd_land_military_requirements':'The Land Rights Revolution is underway; [concept_bureaucracy] is positive; Local Disorder is below #v 50#!; military estates have not yet been inspected.',
'nesnd_cne_landreform_completion_tracker_ge_100':'Reform progress is at least #v 100#!.',
'nesnd_cne_landreform_failure_tracker_lt_70':'Local Disorder is below #v 70#!.',
'nesnd_cne_landreform_failure_tracker_ge_90':'Local Disorder is at least #v 90#!.',
'nesnd_usm_conflicts_within_tracker_ge_100':'Succession Pressure is at least #v 100#!.',
'nesnd_nesnd_hna_preparation_ge_90':'Huguang military preparations are at least #v 90#!.'}
edits.update({('english',k):v for k,v in english.items()})
rx=re.compile(r'^(\s*)([^\s:#]+)\s*:\s*\d*\s*"((?:\\.|[^"\\])*)"\s*(?:#.*)?$')
changes=[]
for p in (C/'localization').rglob('*.yml'):
    lang=p.relative_to(C/'localization').parts[0];s=read(p);lines=s.splitlines();dirty=False
    for i,line in enumerate(lines):
        m=rx.match(line)
        if m and (lang,m[2]) in edits:
            value=edits[(lang,m[2])];changes.append({'lang':lang,'key':m[2],'old':m[3],'new':value,'file':p.relative_to(C).as_posix()});lines[i]=f' {m[2]}:0 "{value}"';dirty=True
    if dirty:write(p,'\n'.join(lines)+'\n')
assert len(changes)==len(edits)
approved=json.loads(read(R/'root-approved-localization.json'));found={(x['lang'],x['key']):x for x in approved}
for x in changes:
    k=(x['lang'],x['key'])
    if k in found:found[k].update(new=x['new'],root_verdict='ROOT_REWRITTEN_AFTER_INDEPENDENT_REVIEW')
    else:approved.append({**x,'root_verdict':'ROOT_REWRITTEN_AFTER_SOURCE_REVIEW','status':'ROOT_EDITORIAL_APPROVED_PENDING_SOURCE_VALIDATION'})
(R/'root-approved-localization.json').write_text(json.dumps(approved,ensure_ascii=False,indent=2),encoding='utf-8')
values=json.loads(read(R/'final-localization-values.json'))
for x in changes:values[x['lang']][x['key']]=x['new']
(R/'final-localization-values.json').write_text(json.dumps(values,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'root-repair1.json').write_text(json.dumps({'dynamic_names_removed_superseded_directives':['REPLACE:HNA','REPLACE:SIH'],'authoritative_definition_file':'common/dynamic_country_names/00_dynamic_country_names.txt','text_changes':changes,'review':'Root read actual source at Egypt occupancy .75 and restoration terminal 2/3/4; rewrote shared event without promising a war or two surviving governments.'},ensure_ascii=False,indent=2),encoding='utf-8')
manifest={p.relative_to(C).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in C.rglob('*') if p.is_file()}
(R/'candidate-freeze.json').write_text(json.dumps({'root':str(C),'files':manifest,'status':'EDIT_FROZEN_READY_FOR_TEST','revision':'root-repair1'},indent=2),encoding='utf-8')
print({'text_values_repaired':len(changes),'frozen_files':len(manifest)})
