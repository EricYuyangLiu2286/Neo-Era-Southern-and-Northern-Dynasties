from canon_routes_context import *
import traceback,copy
src=(W/'tools/test_b2r2_display_preview_red.py').read_text();exec(src[:src.index('# A real active economy JE')],globals())
bar_results=[]
def normal(nodes,stack,path):
 i=0
 while i<len(nodes or []):
  n=nodes[i];i+=1;k=subst(n.key);cur=stack[-1]
  if k=='if':
   chosen,i=x['selected_branches'](nodes,i-1,stack,'if')
   if chosen:normal(body(chosen),stack,path)
  elif k=='save_scope_as':saved[substituted if False else subst(n.value)]=cur
  elif k=='clear_saved_scope':saved.pop(subst(n.value),None)
  elif k.startswith('je:'):
   key=k[3:];assert key in stack[0].journals;normal(n.children,stack+[Entity('journal',key,owner=stack[0])],path)
  elif k=='set_bar_progress':bar_results.append({'journal':cur.tag,'bar':child(n,'name').value,'value':x['number'](child(n,'value').value,stack)})
  else:raise Unsupported('normal sync '+k)
rows=[]
for key,value in [('economy',7),('governance',4),('regional_economy',10),('regional_governance',1),('order',23)]:
 for populated in [False,True]:
  a,s=country_fixture();a.variables['nesnd_small_lineage']=True;a.journals={'nesnd_small_'+key+'_journal'}
  if populated:a.variables['nesnd_small_'+key+'_months']=value
  saved.clear();reads.clear();before=copy.copy(a.variables);x['effects']=dry;eff('nesnd_small_sync_bars',a);assert not reads and a.variables==before and not saved
  x['effects']=normal;bar_results.clear();eff('nesnd_small_sync_bars',a);assert len(bar_results)==1 and bar_results[0]['value']==(value if populated else 0) and not saved
  rows.append({'path':key,'counter_present':populated,'preview_no_saved_read':True,'actual_sync':copy.deepcopy(bar_results)})
# No JE and no variables produces no bar call.
a,s=country_fixture();saved.clear();bar_results.clear();eff('nesnd_small_sync_bars',a);assert not bar_results and not saved
report={'status':'PASS_FIVE_BAR_PREVIEW_AND_EXECUTION','cases':rows,'no_journal_no_write':True,'boundary':'Actual repair2 helper AST. Preview skips all saves/writes; ordinary source execution reads real injected JE and country counter facts. No game UI rendering/timing claim.'}
dump(run/'b2r2-display-five-bar-matrix.json',report);print(json.dumps({'status':report['status'],'cases':len(rows)},ensure_ascii=False))
