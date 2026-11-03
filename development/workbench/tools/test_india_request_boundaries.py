from test_commission_effect_boundaries import *
def reply_world(kind=1):
 w=world_from_history();sender=w['countries']['MUG'];partner=w['countries']['FRA']
 w['strategic']={'region_north_india':Obj('strategic_region','region_north_india'),'region_south_india':Obj('strategic_region','region_south_india')}
 for st in sender.a['states']:st.a['region']=w['strategic']['region_north_india']
 for c in [sender,partner]:c.a['laws']={'law_presidential_republic'};c.a['gold_reserves']=200000
 sender.a['vars'].update(['nesnd_india_request_clock','nesnd_india_request_serial','nesnd_india_request_kind','nesnd_india_request_quote','nesnd_india_request_partner'])
 sender.a['variable_values']={'nesnd_india_request_serial':7,'nesnd_india_request_kind':kind,'nesnd_india_request_quote':50000,'nesnd_india_request_partner':partner}
 sender.a['can_increase_autonomy']=True
 w['saved']={'india_sender':sender,'india_partner':partner,'india_serial':7,'india_sender_patron':partner,'india_partner_patron':partner,'india_sender_regime':4,'india_partner_regime':4}
 return w

def run():
 rows=[]
 def check(name,w,want,key='nesnd_india_reply_valid'):
  ev=Evaluator(C,w);got=ev.test(key,'FRA');assert got==want,(name,got,want);rows.append({'name':name,'pass':True,'expected':want})
 check('valid_aid_request',reply_world(),True)
 check('valid_aid_acceptance_funds',reply_world(),True,'nesnd_india_reply_can_accept')
 for name in ['india_sender','india_partner','india_serial','india_sender_patron','india_partner_patron','india_sender_regime','india_partner_regime']:
  w=reply_world();w['saved'].pop(name);check('missing_'+name,w,False)
 for kind in [4,7]:check('valid_subject_request_'+str(kind),reply_world(kind),True)
 w=reply_world();w['saved']['india_serial']=6;check('stale_serial',w,False)
 # The actual refusal effect must not erase a new pending request on stale reply.
 before=set(w['countries']['MUG'].a['vars']);trace=EffectTrace(w);trace.call('nesnd_india_refuse_request',w['countries']['FRA']);assert w['countries']['MUG'].a['vars']==before and not trace.trace
 rows.append({'name':'stale_refusal_does_not_clear_new_request','pass':True})
 w=reply_world();w['countries']['MUG'].a['vars'].remove('nesnd_india_request_clock');check('expired_clock',w,False)
 w=reply_world();w['countries']['MUG'].a['overlord']=None;check('sender_became_independent_before_reply',w,False)
 w=reply_world();w['countries']['FRA'].a['overlord']=w['countries']['USM'];check('recipient_changed_patron',w,False)
 w=reply_world();w['countries']['FRA'].a['laws']={'law_council_republic'};check('recipient_regime_changed',w,False)
 w=reply_world();w['countries']['MUG'].a['wars']={'FRA'};check('bilateral_war',w,False)
 w=reply_world();w['countries']['MUG'].a['variable_values']['nesnd_india_request_partner']=w['countries']['USM'];check('request_retargeted',w,False)
 w=reply_world();w['countries']['FRA'].a['gold_reserves']=49999;check('cannot_accept_below_quoted_funds',w,False,'nesnd_india_reply_can_accept')
 w=reply_world();w['countries']['FRA'].a['gold_reserves']=50000;check('can_accept_exact_quoted_funds',w,True,'nesnd_india_reply_can_accept')
 w=reply_world();w['countries']['MUG'].a['vars'].add('nesnd_india_aid_lock');check('aid_already_committed',w,False)
 w=reply_world();w['countries']['FRA'].a['is_country_alive']=False;check('recipient_dead',w,False)
 # Deliberately remove the actual serial condition from AST; stale-serial case must become wrongly valid.
 w=reply_world();w['saved']['india_serial']=6;ev=Evaluator(C,w);found=False
 for parent in ev.db['nesnd_india_reply_valid'].walk():
  if parent.children is not None:
   for x in list(parent.children):
    if x.key=='nesnd_india_request_serial':parent.children.remove(x);found=True
 assert found and ev.test('nesnd_india_reply_valid','FRA') is True
 dump(R/'request-boundaries.json',{'status':'PASS','cases':rows,'negative_control':'Removing actual serial comparison wrongly accepts stale request; detected','scope':'Actual guard/value AST, explicit static diplomatic snapshots; no engine event timing certification','engine_verified':False})
 print('PASS',len(rows),'request scenarios and serial mutation')
run()
