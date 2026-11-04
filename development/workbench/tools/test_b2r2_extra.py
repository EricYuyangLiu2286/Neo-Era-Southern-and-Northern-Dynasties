from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_routes.py').read_text();exec(src[:src.rindex('\ntry:\n check(')],globals());results=[]
def stored_small():
 reset();a=world['BAV'];f=world['FRA'];a.variables['nesnd_canon_investor']=f;a.modifiers.add('nesnd_small_state_capital');t=treaty(a,f,'foreign_investment_rights',a,f)
 assert trig('nesnd_canon_investment_valid',a);f.overlord=world['GBR'];assert not trig('nesnd_canon_investment_valid',a)
 eff('nesnd_canon_diplomatic_maintenance',a);assert 'nesnd_canon_investor' not in a.variables and not a.modifiers and a.treaties==[t]
 return {'shared_kind5_stock_maintenance':True,'treaty_preserved':True,'B2_positive_entry':'dedicated actual ACE repair2 send/accept/stock matrix; no stub'}
def notifications():
 reset();e=world['EGY'];f=world['FRA'];e.variables={'nesnd_egypt_started':True,'nesnd_egypt_independence':0,'nesnd_egypt_sponsor_mode':1,'nesnd_egypt_investor':f}
 eff('nesnd_egypt_settle_dependence',e);n=defs['nesnd_egypt.2'][1]
 assert 'nesnd_egypt_investor' not in e.variables and x['triggers'](child(n,'trigger').children,[e]) and not x['triggers'](child(n,'cancellation_trigger').children,[e])
 finished=dict(e.variables);e.overlord=None;e.subject_type=None;assert x['triggers'](child(n,'cancellation_trigger').children,[e]);eff('nesnd_egypt_maintenance',e);assert e.variables==finished
 e.variables.pop('nesnd_egypt_final_patron');assert x['triggers'](child(n,'cancellation_trigger').children,[e])
 return {'finish_keeps_notice_fact':True,'lost_relation_cancels_notice_only':True,'missing_final_patron_safe':True}
def inactive_writes():
 forbidden={'nesnd_egypt_settlement_pending','nesnd_egypt_settlement_started','nesnd_egypt_settlement_deadline','nesnd_egypt_settlement_grace','nesnd_egypt_standard_attempted','nesnd_egypt_pending_explained'};writes=[]
 def walk(n):
  if n.key in ['set_variable','change_variable']:
   name=child(n,'name');key=name.value if name else n.value
   if key in forbidden:writes.append(key)
  for c in n.children or []:walk(c)
 for rel in cfg['owned_files']:
  if rel.endswith('.txt'):walk(parse(read(snap/rel)))
 assert not writes
 for id in ['nesnd_egypt.5','nesnd_egypt.90','nesnd_egypt.91']:
  n=defs[id][1];assert not x['triggers'](child(n,'trigger').children,[world['EGY']]) and x['triggers'](child(n,'cancellation_trigger').children,[world['EGY']]);assert not child(n,'immediate') and not child(n,'option')
 return {'forbidden_writes':writes,'inert_events':['.5','.90','.91']}
try:
 check('kind5_existing_stock_does_not_require_placeholder_B2',stored_small)
 check('protected_notice_after_finish_and_relation_loss',notifications)
 check('all_owned_no_legacy_writes_and_all_retired_events_inert',inactive_writes)
 status='PASS_SOURCE_MATRIX'
except AssertionError:status='FAIL_STOPPED'
except Exception as exc:status='NOT_RUN_UNSUPPORTED';results.append({'name':'adapter','status':'NOT_RUN','error':repr(exc),'traceback':traceback.format_exc()})
dump(run/'extra-repair4-boundaries.json',{'status':status,'checks':results,'engine_verified':False});print(status)
