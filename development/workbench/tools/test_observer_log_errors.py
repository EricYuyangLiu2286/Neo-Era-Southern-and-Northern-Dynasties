"""Source regressions tied to captured engine failures; no engine simulation claim."""
from observer_logfix_context import *
from pathlib import Path
from copy import deepcopy
import operator,re
rootdir=Path(sys.argv[1]) if len(sys.argv)>1 else C
rows=[]
def check(name,fn):
    try: fn();rows.append({'name':name,'pass':True})
    except (AssertionError,ValueError,KeyError) as e:rows.append({'name':name,'pass':False,'detail':str(e)})
def require(value,message='condition failed'):
    assert value,message

# Only the actual character-filter AST subset is evaluated. Unknown nodes fail.
# Missing scope reads raise, including reads after a false AND sibling.
def resolve(key,obj,world):
    if key=='root':return world['country']
    if key=='owner':return obj.get('owner') if obj else None
    if key in ('market','mg:artillery'):return obj.get(key) if obj else None
    if key.startswith('scope:'):return world.get(key)
    if key.startswith('var:'):return obj.get(key) if obj else None
    raise AssertionError('unsupported scope '+key)
def block(node,obj,world):
    assert obj is not None,'invalid character/object scope'
    vals=[];branch=False
    for n in node.children or []:
        if n.key=='trigger_if':
            branch=block(n.get('limit'),obj,world)
            vals.append(block_body(n,obj,world) if branch else True)
        elif n.key=='trigger_else':
            if not branch:vals.append(block(n,obj,world))
        else:vals.append(expr(n,obj,world))
    return all(vals)
def block_body(n,obj,world):
    q=deepcopy(n);q.children=[x for x in q.children if x.key!='limit'];return block(q,obj,world)
def expr(n,obj,w):
    k,v=n.key,n.value
    if k=='always':return v=='yes'
    if k=='exists':return resolve(v,obj,w) is not None
    if k in ('is_character_alive','is_ruler_of_own_country','nesnd_ming_authorized_dynast'):
        return obj.get(k,False)==(v=='yes')
    if k=='market_goods_sell_orders':return {'>':operator.gt}[n.op](obj[k],float(v))
    if k in ('AND','hidden_trigger'):return block(n,obj,w)
    if k=='owner':
        a,b=resolve(k,obj,w),resolve(v,obj,w)
        assert a is not None and b is not None,'invalid owner comparison'
        return a is b
    if k.startswith(('var:','scope:')) or k in ('market','mg:artillery'):return block(n,resolve(k,obj,w),w)
    raise AssertionError('unsupported filter node '+str(k))

def retained_limit():
    n=parse(read(rootdir/'common/scripted_effects/nesnd_ming_royal_refuge.txt')).get('nesnd_ming_mark_retained_royals')
    return n.get('if').all('if')[0].get('limit')
def royal_case(case):
    country={};other={};char={'owner':country,'is_character_alive':True,'nesnd_ming_authorized_dynast':True,'is_ruler_of_own_country':False}
    obj={'var:nesnd_ming_claimant_ref':char};w={'country':country,'scope:nesnd_ming_royal_origin':country}
    want=False
    if case=='retained':want=True
    elif case=='no_character':obj.clear()
    elif case=='exile_or_void':char.pop('owner')
    elif case=='foreign_owner':char['owner']=other
    elif case=='dead':char['is_character_alive']=False
    elif case=='ruler':char['is_ruler_of_own_country']=True
    elif case=='not_authorized':char['nesnd_ming_authorized_dynast']=False
    require(block(retained_limit(),obj,w)==want,case)
for case in ['retained','no_character','exile_or_void','foreign_owner','dead','ruler','not_authorized']:
    check('royal_filter_'+case,lambda c=case:royal_case(c))

def event_order():
    for p in (rootdir/'events').rglob('*.txt'):
        for n in parse(read(p)).children:
            cancel=n.get('cancellation_trigger')
            if cancel:
                typ=n.get('type');require(typ is not None and typ.start<cancel.start,str(p)+':'+str(n.key))
check('event_type_before_cancellation',event_order)
def relations():
    for p in (rootdir/'events').rglob('*.txt'):
        require('relations:scope:' not in read(p),str(p))
    for f,key,count in [('events/nesnd_india_diplomacy.txt','relations(scope:india_sender)',1),('events/nesnd_jp_foreign.txt','relations(scope:jp_sender)',2)]:
        require(sum(x.key==key for x in parse(read(rootdir/f)).walk())==count,f)
check('native_saved_scope_relations',relations)
def general_ideology():
    n=parse(read(rootdir/'common/scripted_effects/nesnd_qe1_fracture.txt')).get('nesnd_qe1_setup_civil_challenger').get('create_character')
    key=n.scalar('ideology');ideology=parse(read(G/'common/ideologies/01_character_ideologies.txt')).get(key)
    require(ideology is not None and ideology.scalar('character_ideology')=='yes',key)
check('general_uses_character_ideology',general_ideology)
def disabled_global():
    n=parse(read(rootdir/'common/journal_entries/zzzz_nesnd_india_native.txt')).get('REPLACE:je_uneasy_raj')
    require(n.get('should_be_involved') is not None,'missing explicit involvement')
    for k,want in [('should_be_involved','no'),('should_show_when_not_involved','no'),('possible','no'),('is_shown_when_inactive','no'),('invalid','yes')]:
        require(n.get(k).scalar('always')==want,k)
check('disabled_global_has_empty_involvement',disabled_global)

railrel='gfx/map/spline_network/military_route_graphics/02_railroad_vehicles.txt'
railpath=rootdir/railrel if (rootdir/railrel).exists() else G/railrel
def rail_case(tag,orders,want):
    node=parse(read(railpath)).get('military_train_01').get('tags').get(tag).get('trigger')
    obj={} if orders is None else {'market':{'mg:artillery':{'market_goods_sell_orders':orders}}}
    require(block(node,obj,{})==want,(tag,orders))
for tag,threshold in [('artillery',5),('more_artillery',20)]:
    for orders in [None,0,5,6,20,21]:
        check('rail_'+tag+'_'+str(orders),lambda t=tag,o=orders,n=threshold:rail_case(t,o,o is not None and o>n))

def same_mechanics():
    # Unmodified JE/refresh routes and all localization/history/map data stay byte-identical.
    for rel,h in man(B).items():
        if rel.startswith(('localization/','map_data/','common/history/','common/scripted_progress_bars/','common/scripted_buttons/')) or rel in ['common/scripted_effects/nesnd_india_core.txt','common/scripted_effects/nesnd_qin_persia_lifecycle.txt','common/scripted_effects/nesnd_cne_confidence.txt']:
            require(sha(rootdir/rel)==h,rel)
check('data_buttons_and_duplicate_JE_routes_unchanged',same_mechanics)

phase='baseline' if rootdir==B else 'candidate'
dump(R/('regression-'+phase+'.json'),{'status':'PASS' if all(x['pass'] for x in rows) else 'FAIL','checks':rows,'source_files':man(rootdir),'engine_verified':False,'scope':'Real source AST and native databases; fixture character links; no live engine replay'})
print(phase,'PASS',sum(x['pass'] for x in rows),'FAIL',sum(not x['pass'] for x in rows))
for x in rows:
    if not x['pass']:print(x['name'],x['detail'])
sys.exit(0 if all(x['pass'] for x in rows) else 1)
