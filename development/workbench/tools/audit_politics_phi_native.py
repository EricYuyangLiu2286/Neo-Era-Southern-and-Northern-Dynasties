"""Read actual native saves for PHI contracts, ship identities, B values and Chen.
No game simulation, source mutation or UI. Optional prior report enables ID deltas.
"""
from pathlib import Path
import argparse,collections,hashlib,json,re,sys
sys.path.insert(0,r'C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
from pdx import parse
from save_market_network import sections,records,scalar
W=Path(r'D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
def nested(body,key):
 m=re.search(r'^\t'+re.escape(key)+r'=\{\n(.*?)^\t\}',body,re.M|re.S)
 return parse(m[0]).children[0] if m else None
def variables(n):
 out={}
 if not n or not n.get('data'):return out
 for item in n.get('data').children:
  key=item.scalar('flag');d=item.get('data')
  if key and d:
   typ=d.scalar('type');v=int(d.scalar('identity','0'));signed=v-(1<<64) if v>=1<<63 else v
   out[key]={'type':typ,'raw_identity':str(v),'value':signed/100000 if typ=='value' else (bool(v) if typ=='boolean' else v),'tick':item.scalar('tick')}
 return out
def dead_ids(section):
 d=nested(section,'dead');objs=d.get('dead_objects') if d else None
 return {n.scalar('object'):n.scalar('death_date') for n in objs.children} if objs else {}
def node(body):return parse('record={\n'+body+'}').children[0]
def audit(source):
 s0=source.stat();raw=source.read_bytes();s1=source.stat()
 assert (s0.st_size,s0.st_mtime_ns)==(s1.st_size,s1.st_mtime_ns) and len(raw)==s0.st_size,'Save is being written; retry only after stable'
 assert raw.startswith(b'SAV0100'),'Unverified save format'
 text=raw.decode('utf-8-sig');sec=sections(text);cb=records(sec['country_manager']);tags={i:scalar(b,'definition') for i,b in cb.items()};countries={}
 for i,b in cb.items():
  if scalar(b,'dead','no')=='yes':continue
  tag=tags[i];v=variables(nested(b,'variables'))
  relevant={k:x for k,x in v.items() if k.startswith(('nesnd_phi','nesnd_south','nesnd_ready','nesnd_chen','nesnd_assassination','nesnd_board','nesnd_ming','nesnd_accession','nesnd_compact','usm_conflicts','tag_WUU'))}
  if relevant or tag in ['USM','PHI','HNA','SIH']:
   countries[tag]={'id':i,'market':scalar(b,'market'),'capital':scalar(b,'capital'),'variables':relevant}
 globalvars=variables(parse(sec['variables']).get('variables'))
 fleets={i:{'country':scalar(b,'country'),'tag':tags.get(scalar(b,'country')),'type':scalar(b,'type'),'dead':scalar(b,'dead','no'),'supply_hub':scalar(b,'supply_hub'),'raw_record':b} for i,b in records(sec['military_formation_manager']).items()}
 templates=parse(sec['ship_templates_manager']).get('ship_templates_manager');versions={n.key:n.get('info') for n in templates.get('versions').get('database').children if n.children is not None}
 shipdead=dead_ids(sec['ship_manager']);ships={};allships={};counts=collections.Counter()
 for i,b in records(sec['ship_manager']).items():
  n=node(b);fl=fleets.get(n.scalar('fleet'),{});v=versions.get(n.scalar('version'));crew=n.get('crew');owner=fl.get('tag')
  row={'id':i,'owner_from_actual_fleet':owner,'fleet_id':n.scalar('fleet'),'version':n.scalar('version'),'type':v.scalar('type') if v else None,'hit_points':n.scalar('hit_points'),'crew':sum(int(x.scalar('crew','0')) for x in crew.children) if crew else 0,'crew_entries':[{'state_id':x.scalar('state'),'crew':x.scalar('crew'),'index':x.scalar('index')} for x in crew.children] if crew else [],'dead_date':shipdead.get(i),'raw_dead':n.scalar('dead')}
  if not row['dead_date'] and row['raw_dead']!='yes':counts[owner]+=1
  allships[i]=row
  if owner in ['USM','PHI'] or i in shipdead:ships[i]=row
 articles={}
 for i,b in records(sec['treaty_article_manager']).items():
  n=node(b);a={'id':i,'article':n.scalar('article'),'treaty_id':n.scalar('treaty'),'source_country_id':n.scalar('source_country'),'target_country_id':n.scalar('target_country'),'source_tag':tags.get(n.scalar('source_country')),'target_tag':tags.get(n.scalar('target_country')),'raw_record':b}
  articles.setdefault(a['treaty_id'],[]).append(a)
 treaties={};tdead=dead_ids(sec['treaty_manager'])
 for i,b in records(sec['treaty_manager']).items():
  first=tags.get(scalar(b,'first_country'));second=tags.get(scalar(b,'second_country'))
  if 'PHI' not in [first,second]:continue
  treaties[i]={'id':i,'first_tag':first,'second_tag':second,'entered_into_force_on':scalar(b,'entered_into_force_on'),'binding_period':scalar(b,'binding_period'),'is_draft_field':scalar(b,'is_draft'),'dead_date':tdead.get(i),'articles':articles.get(i,[]),'raw_record':b}
 characters={};cdead=dead_ids(sec['character_manager'])
 for i,b in records(sec['character_manager']).items():
  template=scalar(b,'template');v=variables(nested(b,'variables'))
  if template not in ['USM_chen_dongyang','USM_hao_tingjiang','USM_zheng_Ju'] and not str(template).startswith('USM_zhu_') and not any(k.startswith('nesnd_ming') for k in v):continue
  n=node(b);characters[i]={'id':i,'template':template,'owner_country_id':n.scalar('country'),'owner_tag':tags.get(n.scalar('country')),'first_name':n.scalar('first_name'),'last_name':n.scalar('last_name'),'traits':n.get('traits').values() if n.get('traits') else [],'roles':n.get('character_roles').values() if n.get('character_roles') else [],'dead_date':cdead.get(i),'death_date_field':n.scalar('death_date'),'variables':v}
 je=[]
 for i,b in records(sec['journal_entry_manager']).items():
  typ=scalar(b,'type')
  if typ not in ['nesnd_south_succession_board','nesnd_phi_service_recovery','ce_usm_conflicts_within']:continue
  n=node(b);bars=n.get('progress_bars');members=n.get('involved_countries')
  je.append({'id':i,'type':typ,'active':n.scalar('active'),'country_id':n.scalar('country'),'date_added':n.scalar('date_added'),'members':[tags.get(x,x) for x in members.values()] if members else [],'bars':{x.scalar('type'):x.scalar('value') for x in bars.children} if bars else {}})
 return {'source':str(source),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'stable_read':True,'date':re.search(r'^date=(\S+)',text,re.M)[1],'seed':re.search(r'^seed=(\d+)',text,re.M)[1],'evidence_kind':'actual native save extraction; not general gameplay correctness','countries':countries,'global_variables':{k:v for k,v in globalvars.items() if k.startswith(('nesnd_south','nesnd_board','usm_civilwar'))},'global_alive_ship_counts':dict(counts),'all_ship_records':allships,'USM_PHI_ship_records':ships,'PHI_treaties':treaties,'Chen_Hao_Ming_characters':characters,'journal_entries':je}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--save',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--before',type=Path);a=p.parse_args();report=audit(a.save)
 if a.before:
  old=json.loads(a.before.read_text('utf-8'));changes=[]
  oldships=old.get('all_ship_records',old['USM_PHI_ship_records'])
  for i,b in oldships.items():
   n=report['all_ship_records'].get(i)
   if n and n['owner_from_actual_fleet']!=b['owner_from_actual_fleet']:changes.append({'id':i,'before':b,'after':n})
  report['delta']={'before_report':str(a.before),'before_save_sha256':old['sha256'],'ownership_changes':changes,'PHI_to_USM':[x['id'] for x in changes if x['before']['owner_from_actual_fleet']=='PHI' and x['after']['owner_from_actual_fleet']=='USM'],'prior_ship_IDs_missing':sorted(set(oldships)-set(report['all_ship_records'])),'new_ship_IDs':sorted(set(report['all_ship_records'])-set(oldships)),'new_PHI_treaty_ids':sorted(set(report['PHI_treaties'])-set(old['PHI_treaties'])),'global_ship_counts_before':old['global_alive_ship_counts'],'global_ship_counts_after':report['global_alive_ship_counts']}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps({'out':str(a.out),'date':report['date'],'sha256':report['sha256'],'PHI_treaty_ids':list(report['PHI_treaties']),'PHI_ship_count':report['global_alive_ship_counts'].get('PHI',0),'USM_ship_count':report['global_alive_ship_counts'].get('USM',0),'delta':{k:v for k,v in report.get('delta',{}).items() if k not in ['ownership_changes','global_ship_counts_before','global_ship_counts_after']}},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
