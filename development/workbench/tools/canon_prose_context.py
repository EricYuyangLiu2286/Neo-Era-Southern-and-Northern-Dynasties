from japan_dev_context import *
import re
E = W/'exports/canon-prose-20261102-a'
R = W/'reports/canon-prose-20261102'
U = W/'backups/pre-canon-prose-20261102T213403Z/mod'
J0 = W/'backups/pre-canon-prose-20261102T213403Z/japan-candidate'
LOC = re.compile(r'^(\s*)([\w.\-]+)(:\d*\s*)"(.*)"(\s*(?:#.*)?)$')

def replace_definition(root, rel, key, body):
    p=root/rel;s=read(p);ns=[n for n in parse(s).children if n.key==key]
    assert len(ns)==1,(rel,key,len(ns))
    n=ns[0];write(p,s[:n.start]+body.strip()+s[n.end:])

def replace_once(root, rel, old, new):
    p=root/rel;s=read(p);assert s.count(old)==1,(rel,old,s.count(old));write(p,s.replace(old,new))

def loc_index(root,lang):
    rows={}
    for p in sorted((root/'localization'/lang).rglob('*.yml')):
        for ln,line in enumerate(read(p).splitlines(),1):
            m=LOC.match(line)
            if m:rows.setdefault(m[2],[]).append((p,ln,m[4]))
    return rows

def apply_proposals(root, proposals, extra_name='zzzzzzzzzzzz_nesnd_canon'):
    edits=[]
    for lang,field in [('simp_chinese','zh'),('english','en')]:
        seen=set()
        for p in sorted((root/'localization'/lang).rglob('*.yml')):
            s=read(p);lines=s.splitlines(True);out=[]
            for line in lines:
                ending='\n' if line.endswith('\n') else ''
                m=LOC.match(line.rstrip('\r\n'))
                if m and m[2] in proposals:
                    k=m[2];v=proposals[k][field]
                    assert '\n' not in v and '\r' not in v,(k,'actual newline')
                    # Victoria localization accepts interior quotes; preserve native style.
                    assert v.count('[')==v.count(']'),(k,'brackets')
                    seen.add(k)
                    if v!=m[4]:
                        edits.append({'file':str(p.relative_to(root)),'key':k,'before':m[4],'after':v})
                        line=m[1]+k+m[3]+'"'+v+'"'+m[5]+ending
                out.append(line)
            if ''.join(out)!=s:write(p,''.join(out))
        missing=proposals.keys()-seen
        if missing:
            p=root/f'localization/{lang}/replace/{extra_name}_l_{lang}.yml'
            s=read(p) if p.exists() else 'l_'+lang+':\n'
            for k in sorted(missing):
                s+=' '+k+':0 "'+proposals[k][field]+'"\n'
                edits.append({'file':str(p.relative_to(root)),'key':k,'before':None,'after':proposals[k][field]})
            write(p,s)
    return edits
