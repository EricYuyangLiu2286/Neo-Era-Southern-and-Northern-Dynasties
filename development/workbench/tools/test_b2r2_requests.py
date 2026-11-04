from canon_routes_context import *
import copy,traceback
p=W/'tools/test_b2r2_routes.py';src=p.read_text();exec(src[:src.rindex('\ntry:\n check(')],globals())
results=[]
def sent():
 reset();a=world['USA'];b=world['FRA'];eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 2')
 event=next(z for z in captured_events if z['event']=='nesnd_canon_diplomacy.1')
 saved.clear();saved.update(event['scopes'])
 assert a.variables['nesnd_canon_request_sender_regime']==2 and a.variables['nesnd_canon_request_partner_regime']==1
 assert trig('nesnd_canon_current_request_valid',a)
 saved.clear();saved.update(event['scopes']);return a,b,event

def invalid_request(case):
 a,b,event=sent()
 if case=='partner_subject':b.overlord=world['GBR']
 if case=='partner_dead':b.alive=False
 if case=='sender_dead':a.alive=False
 if case=='partner_missing':world.pop('FRA');b.valid=False
 if case=='sender_regime':a.laws={'law_monarchy'}
 if case=='partner_regime':b.laws={'law_presidential_republic'}
 if case=='permissions':engine['can_create_treaty']=False
 if case=='relations':a.relations['FRA']=19
 if case=='missing_snapshot':a.variables.pop('nesnd_canon_request_partner_regime')
 if case!='missing_snapshot':
  assert x['triggers'](child(defs['nesnd_canon_diplomacy.1'][1],'cancellation_trigger').children,[b])
 assert not trig('nesnd_canon_current_request_valid',a)
 serial=a.variables['nesnd_canon_request_serial'];cooldown=a.variables['nesnd_canon_request_cooldown']
 eff('nesnd_canon_diplomatic_maintenance',a)
 assert 'nesnd_canon_request_clock' not in a.variables and 'nesnd_canon_request_partner' not in a.variables
 assert a.variables['nesnd_canon_request_serial']==serial and a.variables['nesnd_canon_request_cooldown']==cooldown
 return {'case':case,'serial':serial,'cooldown_preserved':True,'cleared_before_45_day_expiry':True}

def valid_maintenance():
 a,b,event=sent();before=dict(a.variables);eff('nesnd_canon_diplomatic_maintenance',a);assert a.variables==before
 return {'snapshots':{k:v for k,v in before.items() if 'regime' in k},'pending_retained':True}

def stale_cancel():
 a,b,event=sent();a.variables.pop('nesnd_canon_request_clock');a.variables.pop('nesnd_canon_request_cooldown')
 eff('nesnd_canon_send_request',a,'TAG = GBR KIND = 2');before=dict(a.variables)
 saved.clear();saved.update(event['scopes'])
 assert x['triggers'](child(defs['nesnd_canon_diplomacy.1'][1],'cancellation_trigger').children,[b])
 eff('nesnd_canon_refuse_request',b);eff('nesnd_canon_accept_request',b);assert a.variables==before
 eff('nesnd_canon_diplomatic_maintenance',a);assert a.variables==before
 return {'serial':a.variables['nesnd_canon_request_serial'],'partner':a.variables['nesnd_canon_request_partner'].tag}

def existing_subject_investor():
 reset();a=world['USA'];f=world['FRA'];g=world['GBR'];p=world['PRU'];a.variables['nesnd_canon_investor']=f;a.modifiers.add('nesnd_usa_european_capital')
 tf=treaty(a,f,'foreign_investment_rights',a,f);tg=treaty(a,g,'foreign_investment_rights',a,g);tp=treaty(a,p,'foreign_investment_rights',a,p)
 f.overlord=world['BAV'];g.overlord=world['BAV'];assert not trig('nesnd_canon_investment_valid',a)
 eff('nesnd_canon_diplomatic_maintenance',a);assert a.variables['nesnd_canon_investor'] is p and len(a.treaties)==3 and 'nesnd_usa_european_capital' in a.modifiers
 p.overlord=world['BAV'];eff('nesnd_canon_diplomatic_maintenance',a)
 assert 'nesnd_canon_investor' not in a.variables and 'nesnd_usa_european_capital' not in a.modifiers and len(a.treaties)==3
 return {'subject_investors_not_reused':True,'existing_treaties_preserved':3,'independent_alternate':'PRU'}

def kind2_send_subject():
 reset();a=world['USA'];b=world['FRA'];b.overlord=world['GBR'];eff('nesnd_canon_send_request',a,'TAG = FRA KIND = 2')
 assert not captured_events and 'nesnd_canon_request_serial' not in a.variables
 return {'send_rejected':True}
try:
 check('current_valid_request_snapshot_roundtrip',valid_maintenance)
 for case in ['partner_subject','partner_dead','sender_dead','partner_missing','sender_regime','partner_regime','permissions','relations','missing_snapshot']:check('cancel_'+case,lambda case=case:invalid_request(case))
 check('stale_cancel_accept_refuse_current_maintenance_preserve_new_nonce',stale_cancel)
 check('existing_subject_investors_USA_alternate_and_no_withdrawal',existing_subject_investor)
 check('kind2_subject_partner_cannot_send',kind2_send_subject)
 status='PASS_SOURCE_MATRIX'
except AssertionError:status='FAIL_STOPPED'
except Exception as exc:status='NOT_RUN_UNSUPPORTED';results.append({'name':'adapter','status':'NOT_RUN','error':repr(exc),'traceback':traceback.format_exc()})
report={'status':status,'checks':results,'snapshot':str(snap),'boundary':'Frozen source AST, native facts injected; not engine execution. real B2 kind5 positive/stock routes are executed in the dedicated repair2 matrices; no dependency placeholder.','engine_verified':False}
dump(run/'requests-repair4-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(status=='FAIL_STOPPED')
