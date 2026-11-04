from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
rows=[]
try:
 a,s=country_fixture();a.relations.update(FRA=30,GBR=30);world['FRA'].relations['ACE']=30;world['GBR'].relations['ACE']=30
 for tag in ['FRA','GBR']:
  if tag=='GBR':
   a.variables.pop('nesnd_canon_request_cooldown');world['FRA'].overlord=world['GBR'];eff('nesnd_canon_diplomatic_maintenance',a);assert 'nesnd_canon_investor' not in a.variables and 'nesnd_small_state_capital' not in a.modifiers and len(a.treaties)==1
  eff('nesnd_canon_send_request',a,'TAG = '+tag+' KIND = 5');event=[e for e in captured_events if e['event']=='nesnd_canon_diplomacy.1'][-1];saved.clear();saved.update(event['scopes']);eff('nesnd_canon_accept_request',world[tag]);assert a.variables['nesnd_canon_investor'] is world[tag] and a.variables.get('nesnd_small_capital_awarded')
  if tag=='FRA':assert 'nesnd_small_state_capital' in a.modifiers
  else:assert 'nesnd_small_state_capital' not in a.modifiers and a.modifier_adds['nesnd_small_state_capital']==1 and len(a.treaties)==2
 rows.append({'actual_ACE_kind5':'FRA rights+bonus once; subject FRA invalidates stock and bonus but keeps treaty; independent GBR new rights accepted without a second bonus','treaties_preserved':len(a.treaties),'modifier_adds':a.modifier_adds['nesnd_small_state_capital']})
 report={'status':'PASS_REAL_B2_KIND5_STOCK_PERMANENT_HELP_RECEIPT','cases':rows,'boundary':'Actual frozen send/accept/maintenance AST and native treaty/subject facts. No native investment or elapsed60-month simulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-real-kind5-stock.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
