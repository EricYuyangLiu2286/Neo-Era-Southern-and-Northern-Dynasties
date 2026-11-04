"""Narrow B-r3 display regression. Real ordered AST and actual MCP, no engine/UI run."""
from canon_routes_context import *
from test_commission_gate_behavior import Evaluator, Obj
import asyncio, re

META=json.loads(read(R/'batch-b-test-snapshot.json')); T=Path(META['snapshot'])
OLD=W/'validation/runs/canon-b-unity-20261104-r2/mod'
REL='common/journal_entries/nesnd_ottoman_unity.txt'
KEYS={'nesnd_ottoman_direct_states_27':27,'nesnd_ottoman_direct_states_36':36}

def node_at(root):
    return parse(read(root/REL)).get('nesnd_ottoman_unity')

def logical_shape(n):
    """Remove only actual tooltip display metadata, preserving ordered predicates."""
    children=[]
    for q in n.children or []:
        if q.key=='custom_tooltip':
            assert q.scalar('text') in KEYS
            children.extend(logical_shape(x) for x in q.children if x.key!='text')
        else:children.append(logical_shape(q))
    return (n.key,n.op,n.value,children if n.children is not None else None)

def bare_visible_counts(n,inside_custom=False):
    out=[]
    if n.key in ['hidden_trigger','limit']:return out
    inside_custom=inside_custom or n.key=='custom_tooltip'
    if n.key=='num_states' and not inside_custom:out.append((n.op,n.value))
    for q in n.children or []:out.extend(bare_visible_counts(q,inside_custom))
    return out

def loc(path):
    return dict(re.findall(r'^\s*([\w.]+):\d*\s*"(.*)"\s*$',read(path),re.M))

def ast_checks():
    before=man(T);old=node_at(OLD);new=node_at(T)
    assert logical_shape(old)==logical_shape(new), 'Non-display JE logic changed'
    assert bare_visible_counts(old.get('possible'))==[('>=','27'),('>=','36')]
    assert not bare_visible_counts(new.get('possible'))
    tips=[x for x in new.get('possible').walk() if x.key=='custom_tooltip']
    assert len(tips)==2
    for x in tips:
        assert [q.key for q in x.children]==['text','num_states'], 'Tooltip hides more than one count predicate'
        key=x.scalar('text');pred=x.get('num_states')
        assert key in KEYS and pred.op=='>=' and int(pred.value)==KEYS[key]
    # Regression guard binds to the actual native localization gap, not spelling alone.
    mappings=[]
    for source in (G,T):
        for p in (source/'common/trigger_localization').glob('*.txt'):
            mappings.extend(n.key for n in parse(read(p)).children)
    assert 'num_states' not in mappings and 'num_states_greater_or_equal' not in mappings
    cases=0
    for opened in [False,True]:
        for n in range(51):
            o=Obj('country','TUR',states=[None]*n,is_country_alive=True,vars={'nesnd_ottoman_unity_opened'} if opened else set())
            w={'countries':{'TUR':o},'regions':{}};ev=Evaluator(T,w)
            actual=ev.block(new.get('possible'),o,o)
            assert actual==ev.block(old.get('possible'),o,o)==(n>=(27 if opened else 36))
            cases+=1
    for who,alive in [('TUR',False),('FRA',True)]:
        o=Obj('country',who,states=[None]*40,is_country_alive=alive,vars=set())
        t=o if who=='TUR' else Obj('country','TUR',states=[],is_country_alive=True,vars=set())
        ev=Evaluator(T,{'countries':{'TUR':t,who:o},'regions':{}})
        assert not ev.block(new.get('possible'),o,o)
        assert ev.block(new.get('possible'),o,o)==ev.block(old.get('possible'),o,o)
        cases+=1
    texts={}
    for language in ['simp_chinese','english']:
        rel=f'localization/{language}/replace/zzzzzzzzzzzzzzzzzzzz_nesnd_unity_policies_l_{language}.yml'
        assert (T/rel).read_bytes().startswith(b'\xef\xbb\xbf')
        prior=loc(OLD/rel);current=loc(T/rel)
        assert {k:v for k,v in current.items() if k not in KEYS}==prior
        assert current.keys()-prior.keys()==KEYS.keys()
        # Resolve all candidate localization files in lexical load order; late override cannot hide repair.
        effective={}
        for folder in [T/f'localization/{language}',T/f'localization/{language}/replace']:
            for p in sorted(folder.glob('*.yml')):effective.update(loc(p))
        for k,n in KEYS.items():
            assert effective[k]==current[k]
            assert re.findall(r'\d+',current[k])==[str(n)]
            assert len(current[k])<70
        texts[language]={k:current[k] for k in KEYS}
    assert man(T)==before
    result={'status':'PASS','revision':META['revision'],'snapshot':str(T),'source_sha256':sha(T/REL),
            'logical_ordered_AST_unchanged':True,'actual_gate_scenarios':cases,'minimal_tooltips':2,
            'old_visible_num_states_negative_control_rejected':True,'native_mapping_absent':True,
            'bilingual_effective_text':texts,'snapshot_unchanged':True,'engine_verified':False}
    dump(R/'batch-b-statecount-ui-ast.json',result)
    print('B-r3 UI AST PASS:',cases,'actual predicates,2 minimal labels,4 effective localized strings; original gap detected')

async def mcp_checks():
    from mcp import ClientSession,StdioServerParameters
    from mcp.client.stdio import stdio_client
    before=man(T);rows=[]
    async with stdio_client(StdioServerParameters(command=str(W/'tools/mcp-venv/Scripts/paradox-script-mcp.exe'),cwd=str(W/'tools'))) as (r,w):
        async with ClientSession(r,w) as session:
            await session.initialize()
            init=await session.call_tool('init_game',{'game_directory':str(T),'game_type':'vic3'})
            assert not init.isError
            for branch,count in [('trigger_if',27),('trigger_else',36)]:
                args={'file_path':REL,'symbol':'nesnd_ottoman_unity','key_path':f'possible.{branch}.custom_tooltip'}
                response=await session.call_tool('get_structure',args)
                body='\n'.join(x.text for x in response.content if getattr(x,'type',None)=='text')
                ok=not response.isError and all(s in body for s in [f'nesnd_ottoman_direct_states_{count}','num_states','>=',str(count)])
                rows.append({'query':args,'response':body,'source_sha256':sha(T/REL),'pass':ok})
                if not ok:
                    dump(R/'batch-b-statecount-ui-mcp.json',{'status':'FAIL_STOP','queries':rows,'snapshot':str(T),'engine_verified':False})
                    raise AssertionError((args,body))
    assert man(T)==before
    dump(R/'batch-b-statecount-ui-mcp.json',{'status':'PASS','revision':META['revision'],'queries':rows,'snapshot':str(T),'snapshot_unchanged':True,'engine_verified':False})
    print('B-r3 UI MCP PASS:2 actual query responses contain the label and original comparison')

if __name__=='__main__':
    if sys.argv[1]=='ast':ast_checks()
    elif sys.argv[1]=='mcp':asyncio.run(mcp_checks())
