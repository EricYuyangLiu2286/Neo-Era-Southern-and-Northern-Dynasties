from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_all_button_previews.py').read_text();exec(src[:src.index('rows=[]')],globals())
rows=[]
try:
 # All9 inherited India buttons are evaluated in actual B2 south identity modes, including active bridges.
 buttons=parse(read(snap/'common/scripted_buttons/nesnd_india_diplomacy.txt')).children
 for kind in [6,9]:
  x['effects']=effect_sequence2;a,s,f,scopes=request_fixture(kind)
  for k in list(a.variables):
   if k.startswith('nesnd_canon_request_') or k.startswith('nesnd_small_request_'):a.variables.pop(k)
  x['effects']=dry
  for button in buttons:
   saved.clear();before=copy.copy(a.variables);vis=x['triggers'](child(button,'visible').children,[a]);poss=x['triggers'](child(button,'possible').children,[a]);dry(child(button,'effect').children,[a],'common/scripted_buttons/nesnd_india_diplomacy.txt');assert a.variables==before
   rows.append({'kind_fixture':kind,'button':button.key,'visible':vis,'possible':poss,'preview_safe':True})
 # The six actual JE immediate entries must be safe before any effect writes, with all own JEs active.
 x['effects']=effect_sequence2;a,s,f,scopes=request_fixture(9);a.variables['nesnd_small_lineage']=True
 journals=[n for n in parse(read(snap/'common/journal_entries/nesnd_small_states.txt')).children if child(n,'immediate')]
 a.journals={n.key for n in journals};x['effects']=dry
 for je in journals:
  saved.clear();before=copy.copy(a.variables);dry(child(je,'immediate').children,[a],'common/journal_entries/nesnd_small_states.txt');assert a.variables==before;rows.append({'JE':je.key,'immediate_preview_safe':True})
 # Real expired political event and valid selected episode; no effect write is used to satisfy later reads.
 for clock in [True,False]:
  x['effects']=effect_sequence2;a,s,f,scopes=request_fixture(9);a.laws={'law_oligarchy'};a.techs={'democracy'};a.movements=[Entity('movement','liberal',movement_type='movement_liberal',owner=a,supporters=[])];a.variables.update(nesnd_small_episode_active=True,nesnd_small_episode_serial=1,nesnd_small_episode_issue=3,nesnd_small_episode_regime=val('nesnd_canon_regime',a));
  if clock:a.variables['nesnd_small_episode_clock']=True
  saved.clear();saved.update(small_episode_serial=1,small_episode_regime=val('nesnd_canon_regime',a));x['effects']=dry
  for opt in [z for z in defs['nesnd_small_states.10'][1].children if z.key=='option']:
   before=copy.copy(a.variables);tr=child(opt,'trigger');available=x['triggers'](tr.children if tr else [],[a]);dry([z for z in opt.children if z.key not in ['name','trigger','ai_chance','default_option']], [a],defs['nesnd_small_states.10'][2]);assert a.variables==before;rows.append({'event_option':child(opt,'name').value,'clock':clock,'available':available,'preview_safe':True})
 report={'status':'PASS_INHERITED_BUTTON_JE_AND_POLITICAL_EVENT_PREVIEWS','cases':rows,'boundary':'Actual frozen ordered AST with effect save/writes skipped, actual saved request/episode facts provided. No render/game claim.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-extra-previews.json',report);print(json.dumps({'status':report['status'],'completed':len(rows),'error':report.get('error'),'traceback':report.get('traceback')},ensure_ascii=False,indent=2))
