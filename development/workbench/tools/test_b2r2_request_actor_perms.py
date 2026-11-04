from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
event=defs['nesnd_small_states.20'][1];rows=[]
try:
 for kind in [6,7,8,9]:
  for mutation in ['missing_sender','missing_partner','missing_serial','sender_dead','partner_dead','lost_IG','legitimacy49','revolution','missing_market_snapshot']:
   a,s,f,old=request_fixture(kind)
   if mutation.startswith('missing_') and mutation!='missing_market_snapshot':saved.pop({'missing_sender':'canon_sender','missing_partner':'canon_partner','missing_serial':'canon_serial'}[mutation])
   elif mutation=='sender_dead':a.alive=False
   elif mutation=='partner_dead':f.alive=False
   elif mutation=='lost_IG':a.igs['ig_landowners'].in_government=False
   elif mutation=='legitimacy49':a.government_legitimacy=49
   elif mutation=='revolution':a.has_revolution=True
   else:a.variables.pop('nesnd_small_request_market')
   assert x['triggers'](child(event,'cancellation_trigger').children,[f]),(kind,mutation)
   before=copy.copy(a.variables);ops.clear();eff('nesnd_small_accept_request',f);assert a.variables==before and not ops
   rows.append({'kind':kind,'case':mutation,'cancel':True,'accept_no_write':True})
  if kind in [6,8,9]:
   a,s,f,old=request_fixture(kind)
   if kind==6:a.can_increase=False
   elif kind==8:f.can_pact=False
   else:engine['can_create_treaty']=False
   assert x['triggers'](child(event,'cancellation_trigger').children,[f]);ops.clear();eff('nesnd_small_accept_request',f);assert not ops;rows.append({'kind':kind,'permission_loss':'cancel/no native action'})
 report={'status':'PASS_MISSING_ACTOR_CURRENT_AUTHORITY_AND_NATIVE_PERMISSION_CANCELLATION','cases':rows,'boundary':'Actual source event/reply/accept AST; explicit alive/IG/legitimacy/native permission facts. No engine validation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-request-actor-permission-matrix.json',report);print(json.dumps({'status':report['status'],'cases':len(rows),'error':report.get('error'),'traceback':report.get('traceback')},ensure_ascii=False,indent=2))
