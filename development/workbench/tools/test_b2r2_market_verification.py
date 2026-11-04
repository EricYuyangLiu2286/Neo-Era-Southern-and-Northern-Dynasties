from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
flags=['nesnd_small_market_verifying','nesnd_small_market_verification','nesnd_small_verification_partner','nesnd_small_verification_regime','nesnd_small_verification_partner_regime','nesnd_small_verification_overlord','nesnd_small_verification_serial']
def pending():
 a,s,f,scopes=request_fixture(8);native['market']='pending';eff('nesnd_small_accept_request',f);assert a.variables.get('nesnd_small_market_verifying') and 'nesnd_canon_request_clock' not in a.variables;return a,s,f,scopes
rows=[]
try:
 for mutation in ['wait','market_now_own','expired_still_foreign','expired_now_own','pact_removed_now_own','sender_regime','partner_regime','partner_dead','overlord_changed','war']:
  a,s,f,scopes=pending();before_notices=len(x['notifications'])
  if mutation in ['market_now_own','expired_now_own','pact_removed_now_own']:a.market=Entity('market','own-market',owner=a)
  if mutation.startswith('expired'):a.variables.pop('nesnd_small_market_verification')
  elif mutation=='pact_removed_now_own':a.pact_facts=[];f.pact_facts=[]
  elif mutation=='sender_regime':a.laws={'law_presidential_republic'}
  elif mutation=='partner_regime':f.laws={'law_presidential_republic'}
  elif mutation=='partner_dead':f.alive=False
  elif mutation=='overlord_changed':a.overlord=world['GBR'];a.subject_type='subject_type_puppet'
  elif mutation=='war':a.wars={'FRA'};f.wars={'ACE'}
  owner=a.market.owner;eff('nesnd_small_market_verify',a);assert a.market.owner is owner
  if mutation=='wait':assert a.variables.get('nesnd_small_market_verifying') and len(x['notifications'])==before_notices;notice='pending'
  else:
   assert not any(k in a.variables for k in flags);notice=x['notifications'][-1][1];assert notice==('nesnd_canon_diplomacy.2' if mutation=='market_now_own' else 'nesnd_canon_diplomacy.3')
  rows.append({'mutation':mutation,'notice':notice,'native_market_preserved':True,'all7_verification_fields_clean_if_terminal':mutation!='wait'})
 # Same serial daily callback remains harmless if snapshot state changed; helper will fail once and never roll back market.
 a,s,f,old=pending();old_saved=copy.copy(saved);a.variables.pop('nesnd_small_market_verification');eff('nesnd_small_market_verify',a);a.variables.pop('nesnd_canon_request_cooldown');saved.clear();saved['small_receiver']=f;eff('nesnd_small_send_request',a,'KIND = 8');new_event=[e for e in captured_events if e['event']=='nesnd_small_states.20'][-1];saved.clear();saved.update(new_event['scopes']);eff('nesnd_small_accept_request',f);assert a.variables['nesnd_small_verification_serial']==2
 before=copy.copy(a.variables);saved.clear();saved.update(old_saved);assert not trig('nesnd_small_market_event_valid',a);x['effects'](child(defs['nesnd_small_states.22'][1],'immediate').children,[a],defs['nesnd_small_states.22'][2]);assert a.variables==before
 rows.append({'old_daily_serial':'cannot clear actual reissued verification serial2'})
 report={'status':'PASS_30DAY_VERIFICATION_REAL_MARKET_OWNER_MATRIX','cases':rows,'boundary':'Actual frozen request/accept/verify/daily immediate AST. Market ownership, pact and clock facts are explicitly injected, not derived. No engine market tick or exact30-day event ordering claim.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-market-verification-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
