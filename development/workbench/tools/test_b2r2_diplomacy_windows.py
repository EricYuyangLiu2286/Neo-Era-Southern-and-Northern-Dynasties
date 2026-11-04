from canon_routes_context import *
import copy,traceback
src=(W/'tools/test_b2r2_diplomacy_matrix.py').read_text();exec(src[:src.index("\nif __name__=='__main__':")],globals())
event=defs['nesnd_small_states.20'][1];cancel=child(event,'cancellation_trigger')
def cancelled(f):return x['triggers'](cancel.children,[f])
rows=[]
try:
 for kind in [6,7,8,9]:
  for mutation in ['clock_expired','sender_regime','partner_regime','market_changed','overlord_changed','relations_drop','war','imperial_line']:
   a,s,f,scopes=request_fixture(kind)
   if mutation=='clock_expired':a.variables.pop('nesnd_canon_request_clock')
   elif mutation=='sender_regime':a.laws={'law_presidential_republic'}
   elif mutation=='partner_regime':f.laws={'law_presidential_republic'}
   elif mutation=='market_changed':a.market=Entity('market','different-market',owner=world['GBR'])
   elif mutation=='overlord_changed':a.overlord=world['GBR'];a.subject_type='subject_type_puppet'
   elif mutation=='relations_drop':a.relations['FRA']={6:-1,7:-21,8:-1,9:19}[kind]
   elif mutation=='war':a.wars={'FRA'};f.wars={'ACE'}
   else:a.variables['nesnd_india_imperial_line']=True
   assert cancelled(f),(kind,mutation,'window remains live')
   before=copy.copy(a.variables);ops.clear();eff('nesnd_small_accept_request',f);assert a.variables==before and not ops,(kind,mutation,'stale accept wrote')
   # Refusal intentionally closes any still-identical reply even if current eligibility was lost; it must never execute native action.
   eff('nesnd_small_refuse_request',f);assert not ops
   rows.append({'kind':kind,'mutation':mutation,'cancel':True,'accept_no_action':True})
  # Reissue through actual send after explicit native expiry of clock/cooldown; old nonce cannot touch new state.
  a,s,f,old=request_fixture(kind);a.variables.pop('nesnd_canon_request_clock');a.variables.pop('nesnd_canon_request_cooldown');saved.clear();saved['small_receiver']=f;eff('nesnd_small_send_request',a,'KIND = '+str(kind));assert a.variables['nesnd_canon_request_serial']==2
  before=copy.copy(a.variables);saved.clear();saved.update(old);assert cancelled(f);eff('nesnd_small_accept_request',f);eff('nesnd_small_refuse_request',f);assert a.variables==before and 'nesnd_canon_request_clock' in a.variables
  rows.append({'kind':kind,'old_nonce_after_actual_reissue':'no accept/refuse mutation; serial2 clock preserved'})
  # Ordinary refusal closes current request and preserves cooldown.
  a,s,f,scopes=request_fixture(kind);eff('nesnd_small_refuse_request',f);assert 'nesnd_canon_request_clock' not in a.variables and 'nesnd_canon_request_cooldown' in a.variables
  rows.append({'kind':kind,'valid_refusal':'closed; cooldown retained'})
 report={'status':'PASS_REQUEST_WINDOW_CANCELLATION_NONCE_MATRIX','cases':rows,'boundary':'Actual fixed send/event cancellation/accept/refuse AST. Clock/cooldown expiration, changed native relations/war/regime/market/overlord facts explicitly injected; no elapsed engine timing simulation.'}
except Exception as e:report={'status':'FAIL_OR_ADAPTER_UNRESOLVED','rows':rows,'error':repr(e),'traceback':traceback.format_exc()}
dump(run/'b2r2-request-window-matrix.json',report);print(json.dumps(report,ensure_ascii=False,indent=2))
