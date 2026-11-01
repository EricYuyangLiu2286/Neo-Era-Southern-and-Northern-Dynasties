"""Read-only orchestration of existing NESND validators and real MCP evidence.

This is NOT a Clausewitz interpreter. It never launches or drives Victoria 3,
changes a candidate, refreshes the fixed population baseline, or invents engine
success from Python checks. Each invocation has an immutable output directory.
"""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import argparse,contextlib,hashlib,io,json,subprocess,sys,time,traceback

W=Path('D:/Users/Eric Liu/Documents/Paradox Interactive/Victoria 3/nesnd-workbench')
SK=Path('C:/Users/Eric Liu/.codex/skills/nesnd-victoria3/scripts')
G=Path('D:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
EAC=Path('D:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3704408897')
E=W/'plans/two-empires/evidence'
sys.path[:0]=[str(W/'tools'),str(SK),str(W/'editor')]
from model import tree_manifest
from catalog import version
from classify_tiger_reviews import match_review

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def digest_manifest(m):return hashlib.sha256(json.dumps(m,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
def norm_tiger(x):
    d={k:v for k,v in x.items() if k!='locations'}
    d['locations']=[{k:v for k,v in n.items() if k not in ['fullpath','linenr','column','length','line']} for n in (x.get('locations') or [])]
    return json.dumps(d,sort_keys=True,ensure_ascii=False)
def tiger_lines(d):return ' '.join(x.get('line') or '' for x in (d.get('locations') or []))
def tiger_origin(d):return '+'.join(sorted({x.get('from') or 'unknown' for x in (d.get('locations') or [])})) or 'unknown'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',type=Path,required=True)
    p.add_argument('--baseline',type=Path)
    p.add_argument('--out',type=Path)
    p.add_argument('--dependency',type=Path,action='append')
    p.add_argument('--language',action='append',help='Required localization language; repeat to require another. Default simp_chinese; English is not silently made a new delivery requirement.')
    p.add_argument('--review-register',type=Path,default=W/'validation/review-register.json')
    p.add_argument('--toolchain-manifest',type=Path,default=W/'validation/toolchain-frozen-current.json')
    p.add_argument('--engine-collector',type=Path)
    p.add_argument('--runtime-run',type=Path)
    p.add_argument('--no-mcp',action='store_true')
    a=p.parse_args();candidate=a.candidate.resolve();baseline=a.baseline.resolve() if a.baseline else None
    if not candidate.is_dir() or not (candidate/'.metadata/metadata.json').is_file():raise ValueError('Choose an actual candidate MOD root')
    if baseline and not baseline.is_dir():raise ValueError('Baseline absent')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out=(a.out or W/'validation/runs'/f'{stamp}-{candidate.name}').resolve()
    if not out.is_relative_to(W.resolve()) or out.exists():raise ValueError('Choose a new output directory inside WORK')
    out.mkdir(parents=True)
    dependencies=a.dependency if a.dependency is not None else [EAC]
    languages=a.language or ['simp_chinese']
    tool_paths={Path(__file__),SK/'audit.py',SK/'pdx.py',SK/'catalog.py'}
    tool_paths.update(W/'tools'/x for x in ['population_envelope_audit.py','dependency_graph.py','audit_global_naval_exits.py','map_transport_preflight.py','validate_content_closure.py','validate_production_links.py','classify_history_findings.py','mcp_candidate_probe.py','classify_batch_probe_evidence.py','classify_tiger_reviews.py'])
    initial_tools={str(x):sha(x) for x in sorted(tool_paths) if x.exists()}
    manifests={str(candidate):tree_manifest(candidate)}
    if baseline:manifests[str(baseline)]=tree_manifest(baseline)
    register=json.loads(a.review_register.read_text('utf-8-sig')) if a.review_register.exists() else {}
    started=datetime.now(timezone.utc).isoformat();checks=[];state={}
    footprint={'schema':1,'started_utc':started,'candidate':str(candidate),'candidate_manifest':manifests[str(candidate)],
               'candidate_fingerprint':digest_manifest(manifests[str(candidate)]),'baseline':str(baseline) if baseline else None,
               'game':version(),'dependencies':[str(x) for x in dependencies],'required_languages':languages,
               'runner':{'path':str(Path(__file__)),'sha256':sha(Path(__file__))},
               'used_tool_sha256_at_start':initial_tools,
               'review_register':{'path':str(a.review_register),'sha256':sha(a.review_register)} if a.review_register.exists() else None,
               'toolchain_manifest':{'path':str(a.toolchain_manifest),'sha256':sha(a.toolchain_manifest)} if a.toolchain_manifest.exists() else None,
               'runtime_run':{'path':str(a.runtime_run),'sha256':sha(a.runtime_run)} if a.runtime_run and a.runtime_run.exists() else None,
               'scope':'Global static source checks + actual read-only MCP + separately bound engine evidence; no game simulation or UI actions'}
    write(out/'fingerprint.json',footprint)
    def step(name,lane,boundary,fn,required=True):
        begin=time.monotonic();capture=io.StringIO()
        print(json.dumps({'check':name,'state':'RUNNING'},ensure_ascii=False),flush=True)
        try:
            with contextlib.redirect_stdout(capture):r=fn()
            status=r.pop('_status','PASS');assert status in ['PASS','FAIL','NOT_RUN']
            execution='COMPLETED'
        except (ImportError,FileNotFoundError) as exc:
            r={'reason':str(exc),'traceback':traceback.format_exc()};status='NOT_RUN';execution='UNAVAILABLE'
        except Exception as exc:
            r={'reason':repr(exc),'traceback':traceback.format_exc()};status='FAIL';execution='ERROR'
        file=out/(name+'.json');write(file,r)
        if capture.getvalue():(out/(name+'.stdout.txt')).write_text(capture.getvalue(),encoding='utf8')
        row={'id':name,'lane':lane,'status':status,'execution':execution,'required':required,
             'engine_verified':bool(r.get('engine_verified',False)) if lane=='ENGINE_EVIDENCE' else False,
             'seconds':round(time.monotonic()-begin,3),'report':str(file),'report_sha256':sha(file),'boundary':boundary}
        checks.append(row);write(out/'progress.json',{'fingerprint':footprint['candidate_fingerprint'],'checks':checks})
        print(json.dumps({k:row[k] for k in ['id','status','execution','seconds']},ensure_ascii=False),flush=True)
        return r

    def frozen_toolchain():
        if not a.toolchain_manifest.exists():return {'_status':'NOT_RUN','engine_verified':False,'reason':'No explicitly frozen toolchain manifest'}
        frozen=json.loads(a.toolchain_manifest.read_text('utf-8-sig'));drift=[]
        for file,expected in frozen['sha256'].items():
            if not Path(file).is_file() or sha(file)!=expected:drift.append(file)
        return {'_status':'FAIL' if drift else 'PASS','engine_verified':False,'manifest':str(a.toolchain_manifest),
                'manifest_sha256':sha(a.toolchain_manifest),'changed_or_missing_tools':drift,'tool_count':len(frozen['sha256'])}
    step('frozen_toolchain','PROVENANCE','Freeze the validator code and executables before the integrated run; tool drift is not silently accepted.',frozen_toolchain)

    def source_version():
        q=subprocess.run([sys.executable,str(SK/'catalog.py'),'status'],capture_output=True,text=True,encoding='utf8',timeout=180)
        (out/'catalog.stderr.txt').write_text(q.stderr,encoding='utf8')
        r=json.loads(q.stdout.strip().splitlines()[-1]);r['_status']='PASS' if q.returncode==0 and r.get('status')=='CURRENT' else 'FAIL'
        return r
    step('source_version','STATIC','Actual installed build and maintained source index; stale index is not silently refreshed.',source_version)

    def source_graph():
        from audit import audit
        r=audit(candidate);base=audit(W/'research/20261031/naval-reference-vanilla-empty-overlay');r['engine_verified']=False
        signature=lambda x:json.dumps({k:v for k,v in x.items() if k!='file'},sort_keys=True,ensure_ascii=False)
        vanilla_issues=Counter(signature(x) for x in base['issues'])
        classified=[]
        for finding in r['issues']:
            inherited=vanilla_issues[signature(finding)]>0
            classified.append({'classification':'IDENTICAL_CURRENT_GAME_FINDING' if inherited else 'CANDIDATE_SPECIFIC_REVIEW','finding':finding})
        r['current_game_summary']=base['summary'];r['current_game_issues']=base['issues']
        r['classified_findings']=classified;r['classification_counts']=dict(Counter(x['classification'] for x in classified))
        from classify_history_findings import classify
        reviewed=classify(candidate,r['issues']);r['native_evidence_classification']=reviewed
        state['history_design']=reviewed
        r['_status']='FAIL' if reviewed['unreviewed_hard'] else ('NOT_RUN' if reviewed['unreviewed_semantics'] else 'PASS')
        r['classification']='All findings retained; identical-current-game does not auto-waive. Explicit ownership overlap and duplicate investors require source/native intent review, never automatic deletion or level summing.'
        return r
    step('history_production_parser','STATIC','Existing ordered parser, territory/history links, building→PM group→PM and ownership; not runtime employment.',source_graph)

    def history_design():
        r=state.get('history_design')
        if r is None:return {'_status':'NOT_RUN','reason':'History evidence stage unavailable','engine_verified':False}
        return {'_status':'NOT_RUN' if r['unreviewed_semantics'] else 'PASS','engine_verified':False,
                'nonblocking_author_notes':r['author_design_notes'],'review_counts':r['counts'],
                'boundary':'Confirmed author ordered outcomes are retained and nonblocking. Source drift needs renewed semantic review; only a specific lore/user territorial contradiction could justify redesign.'}
    step('history_intent_review','SOURCE_REVIEW','Keep exact-source/native ordered ownership evidence distinct from nonblocking author-design notes; never change borders just to make a checker green.',history_design)

    def production():
        from validate_production_links import audit
        r=audit(candidate);r['_status']='FAIL' if r['hard_errors'] else 'PASS';return r
    step('global_production_resources','STATIC','Global building→PM group→PM and region resource/trait references, including definitions not chosen by opening history.',production)

    def population():
        from population_envelope_audit import audit
        meta=candidate/'EDITOR-REVIEW.json';reasons=json.loads(meta.read_text('utf-8-sig')).get('population_reasons',{}) if meta.exists() else {}
        r=audit(candidate,reasons)
        bad=r['unresolved_mapping'] or r['missing_change_reasons'] or any(x['status']!='within_envelope' for x in r['rows'])
        r['_status']='FAIL' if bad else 'PASS';return r
    step('fixed_population_envelope','STATIC','Pinned original MOD + frozen inherited vanilla; aggregate new regions to original geography, exact inclusive ±25%.',population)

    def impact():
        from dependency_graph import build
        folder=out/'impact';build(candidate,folder)
        r=json.loads((folder/'dependency-graph.json').read_text('utf8'))
        return {'_status':'FAIL' if r['parse_failures'] else 'PASS','engine_verified':False,
                'graph':str(folder/'dependency-graph.json'),'sha256':sha(folder/'dependency-graph.json'),
                'nodes':len(r['nodes']),'edges':len(r['edges']),'parse_failures':r['parse_failures'],
                'limitations':r['limitations']}
    step('dependency_impact_graph','STATIC','Typed lexical routes and source lines; not trigger satisfiability or proof that every story branch executes.',impact)

    def content():
        from validate_content_closure import audit
        r=audit(candidate,dependencies=dependencies,languages=languages)
        r['_status']='FAIL' if r.get('hard_errors') else 'PASS';r['engine_verified']=False
        return r
    step('content_localization_resources','STATIC','Literal event/JE/button/bar/modifier/localization/media links; dynamic scope/display stays unexecuted.',content)

    def geography():
        from audit_global_naval_exits import audit
        vanilla=W/'research/20261031/naval-reference-vanilla-empty-overlay'
        cur=audit(candidate);base=audit(vanilla);write(out/'naval_geometry_full.json',cur);write(out/'naval_geometry_vanilla.json',base)
        state['geometry']=cur
        hard=[];review=[];known=[];registered={x['region']:x for x in register.get('geometry_exceptions',[])}
        fields=register.get('geometry_signature_fields',[])
        for row in cur['rows']:
            if not row['issues']:continue
            if any(i in row['issues'] for i in ['missing_exit_id','duplicate_exit_id','exit_is_not_sea','port_outside_declared_region','exit_without_port']):hard.append(row)
            signature=hashlib.sha256(json.dumps({k:row.get(k) for k in fields},sort_keys=True,separators=(',',':')).encode()).hexdigest()
            rr=registered.get(row['region']);ev=rr.get('evidence',{}) if rr else {}
            if rr and signature==rr['signature_sha256'] and Path(ev.get('path','')).is_file() and sha(ev['path'])==ev.get('sha256'):
                known.append({'region':row['region'],'issues':row['issues'],'evidence':ev,'scope':'Reviewed static exception only'})
            else:review.append({'region':row['region'],'issues':row['issues'],'reason':'No unchanged reviewed geometry signature'})
        duplicates=bool(cur['duplicate_keys'] or cur['duplicate_ids'] or any(cur['table_duplicate_keys'].values()))
        return {'_status':'FAIL' if hard or review or duplicates or cur['counts']['recommended_changes'] else 'PASS',
                'engine_verified':False,'counts':cur['counts'],'hard_errors':hard,'unreviewed_findings':review,'reviewed_exceptions':known,
                'duplicate_ids':cur['duplicate_ids'],'duplicate_keys':cur['duplicate_keys'],'network_duplicate_keys':cur['table_duplicate_keys'],
                'source_sha256':cur['sources'],'full_report':str(out/'naval_geometry_full.json')}
    step('global_naval_geometry','STATIC','All effective ports/exits; actual pixel edges and direct routes; reviewed native exceptions are explicit, never world navigation proof.',geography)

    def transport():
        from map_transport_preflight import check
        vanilla=W/'research/20261031/naval-reference-vanilla-empty-overlay'
        if 'geometry' not in state:raise ValueError('Naval geometry stage unavailable; cannot choose complete port set')
        base_geo=json.loads((out/'naval_geometry_vanilla.json').read_text('utf8'))
        cur=check(candidate,[r['region'] for r in state['geometry']['rows'] if r['port']]);base=check(vanilla,[r['region'] for r in base_geo['rows'] if r['port']])
        write(out/'transport_full.json',cur);write(out/'transport_vanilla.json',base)
        added=sorted(set(cur['errors'])-set(base['errors']))
        return {'_status':'FAIL' if added else 'PASS','engine_verified':False,
                'global_reference_errors':cur['global_naval_references']['errors'],
                'candidate_errors':len(cur['errors']),'vanilla_errors':len(base['errors']),'added_errors':added,
                'inherited_errors':sorted(set(cur['errors'])&set(base['errors'])),
                'warning':'PASS means no added transport errors against current vanilla; inherited errors remain in the report and are not declared harmless.',
                'full_report':str(out/'transport_full.json'),'full_report_sha256':sha(out/'transport_full.json')}
    step('global_transport_regression','STATIC','Global ID/type gate and all-port network structure compared with current vanilla; no fleet or war-path execution.',transport)

    def tiger():
        exe=W/'tools/tiger-1.19.0/vic3-tiger.exe'
        # Official bundled vic3-tiger.conf documents repeated load_mod blocks.
        # Resolve co-enabled assets in-place. No third-party file is copied.
        for dependency in dependencies:
            if not dependency.is_dir():raise FileNotFoundError('Declared Tiger dependency absent: '+str(dependency))
        config_lines=['languages = {']
        for language in languages:
            if not language.replace('_','').isalnum():raise ValueError('Invalid localization language')
            config_lines.append('    check = "'+language+'"')
        config_lines+=['}','filter = { show_vanilla = no show_loaded_mods = yes }']
        for index,dependency in enumerate(dependencies):
            path=dependency.resolve().as_posix()
            if '"' in path or '\n' in path:raise ValueError('Invalid config path')
            config_lines.append('load_mod = { label = "DEP'+str(index)+'" mod = "'+path+'" }')
        config=out/'tiger-load-order.conf';config.write_text('\n'.join(config_lines)+'\n',encoding='utf8')
        commands=[]
        def run(mod,name):
            cmd=[str(exe),'--game',str(G.parent),'--config',str(config),'--json',str(mod)]
            q=subprocess.run(cmd,capture_output=True,timeout=180);commands.append({'command':cmd,'returncode':q.returncode,'stderr':q.stderr.decode('utf-8-sig',errors='replace')})
            (out/(name+'.json')).write_bytes(q.stdout);(out/(name+'.stderr.txt')).write_bytes(q.stderr)
            data=json.loads(q.stdout.decode('utf-8-sig'));return data
        cur=run(candidate,'tiger_raw');base=run(baseline,'tiger_baseline_raw') if baseline else []
        cc=Counter(map(norm_tiger,cur));bc=Counter(map(norm_tiger,base))
        added=[json.loads(k) for k,n in (cc-bc).items() for _ in range(n)] if baseline else None
        classified=[];unknown_errors=[];unknown_warnings=[];reviewed_unresolved=[];review_hashes={}
        native_other=(G/'common/character_roles/02_unique_roles.txt').read_text('utf-8-sig')
        crew_evidence=E/'phi-A-expiry-May9-c5-224458.json'
        observed_crew=False
        if crew_evidence.exists():
            cr=json.loads(crew_evidence.read_text('utf8'));observed_crew=cr['snapshots'][0]['countries']['PHI']['variables'].get('nesnd_phi_needed_crew',{}).get('value',0)>0
        for d in cur:
            message=d.get('message') or '';lines=tiger_lines(d);classification='UNREVIEWED'
            proof=None
            exact_review=match_review(d,candidate,register,review_hashes)
            if exact_review:
                classification=exact_review['classification'];proof=exact_review['evidence']
            elif d.get('key')=='choice' and 'type = other' in lines and 'type = other' in native_other:
                classification='CURRENT_SOURCE_ENUM_TOOL_GAP';proof={'path':str(G/'common/character_roles/02_unique_roles.txt'),'sha256':sha(G/'common/character_roles/02_unique_roles.txt')}
            elif d.get('key')=='unknown-field' and 'total_crew_needed' in message and observed_crew:
                classification='OBSERVED_NATIVE_GETTER_TOOL_GAP';proof={'path':str(crew_evidence),'sha256':sha(crew_evidence),'boundary':'Only this getter was observed; not every unknown token is waived'}
            elif d.get('key')=='brace-placement':classification='FORMATTING_REVIEW'
            elif d.get('severity')=='tips':classification='TOOL_TIP'
            row={'classification':classification,'evidence':proof,'diagnostic':d}
            if exact_review:
                row.update(exact_review)
                if exact_review['requires_resolution']:reviewed_unresolved.append(row)
            classified.append(row)
            if classification=='UNREVIEWED':
                if d.get('severity')=='error':unknown_errors.append(row)
                else:unknown_warnings.append(row)
        write(out/'tiger_classified.json',classified)
        return {'_status':'FAIL' if unknown_errors or unknown_warnings or reviewed_unresolved else 'PASS','engine_verified':False,
                'counts_by_severity':dict(Counter(x.get('severity') for x in cur)),
                'classification_counts':dict(Counter(x['classification'] for x in classified)),
                'counts_by_origin':dict(Counter(tiger_origin(d) for d in cur)),
                'unreviewed_counts_by_origin_and_severity':dict(Counter(tiger_origin(row['diagnostic'])+':'+(row['diagnostic'].get('severity') or 'unknown') for row in classified if row['classification']=='UNREVIEWED')),
                'unreviewed_errors':unknown_errors,'unreviewed_warning_count':len(unknown_warnings),
                'reviewed_unresolved_count':len(reviewed_unresolved),
                'reviewed_unresolved_counts':dict(Counter(row['classification'] for row in reviewed_unresolved)),
                'reviewed_unresolved_errors':[row for row in reviewed_unresolved if row['diagnostic'].get('severity')=='error'],
                'baseline':str(baseline) if baseline else None,'new_vs_baseline':added,
                'regression_status':'NOT_RUN' if not baseline else ('PASS' if not added else 'FAIL'),
                'tool_sha256':sha(exe),'raw_report':str(out/'tiger_raw.json'),
                'configuration':{'path':str(config),'sha256':sha(config),'contents':config.read_text('utf8'),
                    'official_sample':str(W/'tools/tiger-1.19.0/vic3-tiger.conf'),'official_sample_sha256':sha(W/'tools/tiger-1.19.0/vic3-tiger.conf')},
                'actual_commands':commands,'dependencies':[{'label':'DEP'+str(i),'path':str(d),'metadata_sha256':sha(d/'.metadata/metadata.json') if (d/'.metadata/metadata.json').exists() else None} for i,d in enumerate(dependencies)],
                'boundary':'Known source/version gaps are evidenced narrowly; unchanged or unreviewed diagnostics are not automatically safe.'}
    step('tiger_classification','STATIC','Actual Tiger execution; exact baseline delta and explicit known gaps; unreviewed errors/warnings remain visible and fail triage.',tiger)

    def manual():
        rows=[]
        for r in register.get('manual_checks',[]):
            same=all((candidate/x['relative']).is_file() and sha(candidate/x['relative'])==x['sha256'] for x in r['source_witnesses'])
            evidence=r.get('evidence',{});available=Path(evidence.get('path','')).is_file() and sha(evidence['path'])==evidence.get('sha256')
            rows.append({**r,'witnesses_unchanged':same,'evidence_exists':available,
                         'current_status':r['status'] if same and available else 'NOT_RUN',
                         'meaning':r['reason'] if same and available else 'Witness changed or evidence absent; explicit review required, not auto-cleared'})
        status='FAIL' if any(r['current_status']=='FAIL' for r in rows) else ('NOT_RUN' if not rows or any(r['current_status']=='NOT_RUN' for r in rows) else 'PASS')
        return {'_status':status,'engine_verified':False,'checks':rows,'boundary':'Manual semantic defects are source-fingerprinted review findings; no Python gameplay simulation.'}
    step('known_semantic_review','SOURCE_REVIEW','Known settlement/leader/character-route defects remain blockers until their changed source is explicitly reviewed.',manual)

    def mcp():
        if a.no_mcp:return {'_status':'NOT_RUN','reason':'Explicit --no-mcp; no protocol query performed','engine_verified':False}
        python=W/'tools/mcp-venv/Scripts/python.exe';dest=out/'mcp_actual_protocol.json'
        q=subprocess.run([str(python),'-X','utf8',str(W/'tools/mcp_candidate_probe.py'),'--candidate',str(candidate),'--out',str(dest)],capture_output=True,text=True,encoding='utf8',timeout=75)
        (out/'mcp.stderr.txt').write_text(q.stderr,encoding='utf8');r=json.loads(dest.read_text('utf8'))
        return {'_status':r['status'],'engine_verified':False,'protocol_report':str(dest),'sha256':sha(dest),
                'candidate_unchanged':r.get('candidate_unchanged'),'observed_hawaii_exit':r.get('observed_hawaii_naval_exit'),
                'reason':r.get('reason'),'boundary':r['boundary']}
    step('mcp_actual_query','MCP','Real stdio initialize/list_tools/source query; explicitly not native game execution.',mcp)

    def engine_probe():
        if not a.engine_collector:return {'_status':'NOT_RUN','engine_verified':False,'reason':'No actual bound engine collector supplied; this runner never starts the game'}
        from classify_batch_probe_evidence import classify
        r=classify(candidate,a.engine_collector);r['_status']=r['status'];return r
    step('native_batch_probe_evidence','ENGINE_EVIDENCE','Only complete same-candidate/run/log/probe-bound actual predicates can pass; stale historical PASS is rejected.',engine_probe)

    def runtime_binding():
        if not a.runtime_run:return {'_status':'NOT_RUN','engine_verified':False,'reason':'No actual run manifest supplied'}
        run=json.loads(a.runtime_run.read_text('utf-8-sig'));match=run.get('source_sha256')==manifests[str(candidate)]
        return {'_status':'PASS' if match else 'NOT_RUN','engine_verified':False,'run':str(a.runtime_run),'sha256':sha(a.runtime_run),
                'candidate_exact_manifest_match':match,'profile':run.get('profile'),
                'boundary':'This proves which candidate the supplied run froze, not which actions executed or passed.'}
    step('runtime_candidate_binding','PROVENANCE','Actual run manifest binding only; not a gameplay acceptance.',runtime_binding,required=False)

    def untouched():
        checks_={path:tree_manifest(Path(path))==m for path,m in manifests.items()}
        return {'_status':'PASS' if all(checks_.values()) else 'FAIL','engine_verified':False,'input_manifests_unchanged':checks_}
    step('input_integrity_after','PROVENANCE','All read-only input candidate/baseline files retain their full SHA manifest.',untouched)
    def tools_untouched():
        now={str(x):sha(x) for x in sorted(tool_paths) if x.exists()}
        changed={k:{'before':initial_tools.get(k),'after':now.get(k)} for k in set(initial_tools)|set(now) if initial_tools.get(k)!=now.get(k)}
        return {'_status':'FAIL' if changed else 'PASS','engine_verified':False,'changed_tools':changed,'sha256_after':now}
    tool_final=step('tool_integrity_after','PROVENANCE','A validator changed mid-run invalidates this suite; do not retrospectively assign a newer tool SHA to older results.',tools_untouched)
    footprint['used_tool_sha256_after']=tool_final.get('sha256_after',{});write(out/'fingerprint.json',footprint)
    fail=[r['id'] for r in checks if r['required'] and r['status']=='FAIL'];notrun=[r['id'] for r in checks if r['required'] and r['status']=='NOT_RUN']
    report={'schema':1,'started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),'candidate':str(candidate),
            'candidate_fingerprint':footprint['candidate_fingerprint'],'game':footprint['game'],'pipeline_completed':True,
            'overall_status':'FAIL' if fail else ('NOT_RUN' if notrun else 'PASS'),
            'failing_checks':fail,'not_run_required_checks':notrun,'checks':checks,
            'all_gameplay_validated':False,'publication_approved':False,
            'rule':'PASS is limited to each check boundary. A completed pipeline, MCP read success, or zero new Tiger reports never certifies all game branches/world economy/naval travel.'}
    write(out/'summary.json',report)
    lines=['# NESND 全局验证报告','',f'候选：`{candidate}`',f'指纹：`{footprint["candidate_fingerprint"]}`',
           f'游戏：{footprint["game"]["version"]} / {footprint["game"]["build"]}',
           f'本地编排已完成；总体状态 **{report["overall_status"]}**。未宣称全游戏已验收。','',
           '|检查|层次|状态|实际执行|用时秒|证据|','|---|---|---|---|---:|---|']
    for r in checks:lines.append(f'|{r["id"]}|{r["lane"]}|{r["status"]}|{r["execution"]}|{r["seconds"]}|[{Path(r["report"]).name}]({Path(r["report"]).name})|')
    lines+=['','## 尚需处理','',f'FAIL：{", ".join(fail) or "无"}',f'NOT_RUN：{", ".join(notrun) or "无"}',
            '', '未知/继承告警不因基线相同自动豁免；已知源码反证与视觉例外各有证据。静态范围、真实MCP协议和原生运行证据分别保存。',
            '下一阶段先修报告中的源码/闭包错误，重跑本入口；之后才在精确冻结候选上实际进入国家、走时并执行所需分支，再收集绑定原生探针。',
            '运行时scope、预览求值、AI、就业/价格、战争胜负、舰队到达及所有故事组合均不能由本检查器模拟认证。']
    (out/'report.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print(json.dumps({'summary':str(out/'summary.json'),'report':str(out/'report.md'),'overall_status':report['overall_status'],'failed':fail,'not_run':notrun},ensure_ascii=False),flush=True)
    return 1 if fail else 2 if notrun else 0

if __name__=='__main__':raise SystemExit(main())
