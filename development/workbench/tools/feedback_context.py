from qin_persia_context import W,M,G,S,D,read,write,sha,man,dump,parse,shape
import json,re,shutil
C=W/'exports/persia-journal-ui-20261103-a';R=W/'reports/persia-journal-ui-20261103'
B=W/'backups/pre-change-persia-journal-ui-20261103T005805Z/mod'
def replace_node(rel,key,body):
    p=C/rel;s=read(p);n=parse(s).get(key);assert n,(rel,key)
    write(p,s[:n.start]+body.strip()+s[n.end:])
def append_texts(texts):
    for i,lang in enumerate(['simp_chinese','english']):
        p=C/'localization'/lang/'replace'/f'zzzzzzzzzzzzz_nesnd_feedback_l_{lang}.yml'
        s=read(p) if p.exists() else 'l_'+lang+':\n'
        for key,pair in texts.items():
            assert not re.search(r'(?m)^\s*'+re.escape(key)+':',s),key
            value=pair[i].replace('"','\\"').replace('\n','\\n')
            s+=f' {key}:0 "{value}"\n'
        write(p,s)
def wrap_button(rel,key,tooltip,native=''):
    p=C/rel;s=read(p);b=parse(s).get(key);e=b.get('effect');body=s[e.vstart+1:e.vend-1]
    new='effect = {\n'
    if tooltip:new+='\t\tcustom_tooltip = '+tooltip+'\n'
    if native:new+='\t\tshow_as_tooltip = { '+native+' }\n'
    new+='\t\thidden_effect = {'+body+'}\n\t}'
    replacement=parse(new).get('effect').get('hidden_effect')
    assert [shape(n) for n in replacement.children]==[shape(n) for n in e.children],key
    write(p,s[:e.start]+new+s[e.end:])
    return {'button':key,'file':rel,'tooltip':tooltip,'native_preview':native,'runtime_effect_ast_preserved':True}
