"""Read-only, typed impact index for NESND. Not a scope checker or engine test.

Uses ordered PDX AST; comments are never counted as references. Edges retain
source lines and uncertainty. Dynamic localization is recorded, not executed.
"""
from pathlib import Path
import argparse, collections, hashlib, json, re, sys
sys.path.insert(0, r'C:\Users\Eric Liu\.codex\skills\nesnd-victoria3\scripts')
from pdx import read, basekey, unquote
from catalog import GAME

def build(mod, out):
    nodes = {}; edges = []; definitions = collections.defaultdict(list)
    docs = []; failures = []; hashes = {}
    def node(key, **data):
        nodes.setdefault(key, {'id': key, **data}); return key
    def edge(a,b,kind,path,line,certainty='parsed-reference',detail=''):
        edges.append(dict(source=a,target=b,kind=kind,path=path,line=line,certainty=certainty,detail=detail))
    # Index only candidate definitions. External refs resolve on demand below.
    for path in sorted(mod.rglob('*.txt')):
        rel=path.relative_to(mod).as_posix()
        if not rel.startswith(('common/','events/','map_data/')): continue
        data=path.read_bytes(); hashes[rel]=hashlib.sha256(data).hexdigest()
        fileid=node('file:'+rel,kind='script-file',path=str(path))
        try: text,doc=read(path)
        except Exception as exc: failures.append({'path':rel,'error':str(exc)});continue
        docs.append((rel,text,doc,fileid))
        if rel.startswith('common/history/'): continue
        for n in doc.children:
            if not n.key or n.children is None:continue
            symbol=basekey(n.key);line=text.count('\n',0,n.start)+1
            sid=node('def:'+rel+':'+str(line),kind='definition',symbol=symbol,path=str(path),line=line)
            definitions[symbol].append(sid);edge(fileid,sid,'defines',rel,line)
    # Localization is a separate display layer; keys with multiple languages are valid.
    locdefs=collections.defaultdict(list)
    for path in sorted(mod.glob('localization/**/*.yml')):
        rel=path.relative_to(mod).as_posix();hashes[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
        for i,line in enumerate(path.read_text('utf-8-sig').splitlines(),1):
            m=re.match(r'^\s*([\w.]+):\d*\s+"(.*)"\s*$',line)
            if not m:continue
            sid=node('loc:'+rel+':'+str(i),kind='localization',symbol=m[1],path=str(path),line=i)
            locdefs[m[1]].append(sid)
            for v in re.findall(r'\$([\w.]+)\$',m[2]):
                edge(sid,node('loc-key:'+v,kind='localization-key',symbol=v),'localization-expansion',rel,i)
            for v in re.findall(r'\[[^\]]+\]',m[2]):
                edge(sid,node('dynamic:'+v,kind='dynamic-localization',expression=v),'dynamic-display',rel,i,'requires-engine-scope')
    variables={'set_variable':'write-variable','change_variable':'write-variable','remove_variable':'remove-variable','has_variable':'read-variable',
               'set_global_variable':'write-global','remove_global_variable':'remove-global','has_global_variable':'read-global','change_global_variable':'write-global'}
    for rel,text,doc,fileid in docs:
        for top in doc.children:
            sid=next((v for v in definitions.get(basekey(top.key),[]) if nodes[v]['path']==str(mod/rel) and nodes[v]['line']==text.count('\n',0,top.start)+1),fileid)
            for n in top.walk():
                line=text.count('\n',0,n.start)+1
                key=n.key or '';value=unquote(n.value) if n.value is not None else ''
                if n is not top and key in definitions:
                    for dst in definitions[key]:edge(sid,dst,'script-symbol',rel,line,detail=key)
                if value in definitions:
                    for dst in definitions[value]:edge(sid,dst,'symbol-argument',rel,line,detail=key+'='+value)
                for tok in (key,value):
                    for prefix,identifier in re.findall(r'\b(c|s|region_state|var|global_var|je|law_type|ig|g):([A-Za-z_0-9]+)',tok):
                        kind={'c':'country','s':'state-region','region_state':'country','var':'variable','global_var':'global-variable','je':'journal','law_type':'law','ig':'interest-group','g':'goods'}[prefix]
                        edge(sid,node(kind+':'+identifier,kind=kind,symbol=identifier),'scope-or-value-reference',rel,line,'scope-not-validated',tok)
                if key in variables:
                    v=value or n.scalar('name','')
                    if v:
                        category='global-variable' if 'global' in key else 'variable'
                        edge(sid,node(category+':'+v,kind=category,symbol=v),variables[key],rel,line,'scope-not-validated')
                if value in locdefs:
                    for dst in locdefs[value]:edge(sid,dst,'display',rel,line)
                if re.search(r'\.(dds|png|asset|mesh|anim)$',value,re.I):
                    found=next((str(root/value) for root in (mod,GAME) if (root/value).exists()),None)
                    edge(sid,node('asset:'+value,kind='asset',path=found or value,exists_in_candidate_or_game=bool(found)),'asset-reference',rel,line,'resolved-path' if found else 'dependency-or-missing')
            if top.key:
                for suffix in ('','_reason','_status','_desc','_tooltip'):
                    for dst in locdefs.get(basekey(top.key)+suffix,[]):edge(sid,dst,'implicit-display-convention',rel,text.count('\n',0,top.start)+1,'engine-convention-needs-ui')
    # Resolve exact identifiers in GAME definitions for reading; no claim of runtime mount precedence.
    requested={n['symbol'] for n in nodes.values() if n['kind'] in {'state-region','journal','law','interest-group','goods'}}
    external={}
    for folder in ('map_data/state_regions','common/journal_entries','common/laws','common/interest_groups','common/goods'):
        for p in sorted((GAME/folder).glob('*.txt')):
            try:t,d=read(p)
            except Exception:continue
            for n in d.children:
                if basekey(n.key) in requested:external.setdefault(basekey(n.key),[]).append({'path':str(p),'line':t.count('\n',0,n.start)+1})
    # File/name mismatch is a review finding, never an automatic rewrite.
    identity=[]
    for rel,text,doc,_ in docs:
        if not rel.startswith('common/history/population/'):continue
        expected=re.match(r'([A-Z0-9]{3})(?:[ ._-]|$)',Path(rel).name,re.I)
        actual=[n.key[2:] for n in doc.walk() if n.key and re.fullmatch(r'c:[A-Z0-9]{3}',n.key)]
        if expected and expected[1].upper() not in actual:
            identity.append({'file':rel,'filename_tag':expected[1].upper(),'actual_country_scopes':actual,'status':'REVIEW—not inferred semantics'})
    incoming=collections.defaultdict(set);outgoing=collections.defaultdict(set)
    for e in edges:
        if e['kind']!='defines':incoming[e['target']].add(e['source']);outgoing[e['source']].add(e['target'])
    shared=sorted(({'node':k,'kind':nodes[k]['kind'],'symbol':nodes[k].get('symbol',k),'incoming_distinct_nodes':len(v)} for k,v in incoming.items()),key=lambda r:-r['incoming_distinct_nodes'])
    result={'candidate':str(mod),'limitations':['Typed lexical/AST impact graph; NOT an engine call graph.','Variable scope/lifetime and shadowing require manual review.','Same-named definitions can have load-order semantics; all candidates retained.','High degree prioritizes investigation, not automatic risk or correctness.','Runtime prices, qualifications, warfare and dynamically created scopes are not simulated.'],
            'sha256':hashes,'nodes':list(nodes.values()),'edges':edges,'external_definition_routes':external,'parse_failures':failures,'population_identity_review':identity,'shared_nodes':shared[:80]}
    out.mkdir(parents=True,exist_ok=True);(out/'dependency-graph.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),'utf-8')
    lines=['# 实际文件依赖索引','',f'候选：`{mod}`','', '这是带来源行号的影响索引，不是引擎执行证明。完整节点、边、指纹见 dependency-graph.json。','', '## 高连接节点（只用于安排审查）','', '|对象|类别|引用节点数|','|---|---|---|']
    for row in shared[:30]:lines.append(f"|{row['symbol']}|{row['kind']}|{row['incoming_distinct_nodes']}|")
    lines+=['','## 历史初始化归属待审','',json.dumps(identity,ensure_ascii=False,indent=2),'','## 解析失败','',json.dumps(failures,ensure_ascii=False,indent=2)]
    (out/'dependency-index.md').write_text('\n'.join(lines),'utf-8')
    print(json.dumps({'nodes':len(nodes),'edges':len(edges),'parse_failures':len(failures),'population_identity_review':identity,'output':str(out)},ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--mod',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();build(a.mod.resolve(),a.out.resolve())
