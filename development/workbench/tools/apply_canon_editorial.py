from canon_prose_context import *

usm=json.loads(read(R/'usm-proposals.json'))
jp=json.loads(read(R/'japan-qin-proposals.json'))
cne=json.loads(read(R/'cne-proposals.json'))
assert not (usm.keys()&cne.keys()),sorted(usm.keys()&cne.keys())
assert not (usm.keys()&jp.keys()),sorted(usm.keys()&jp.keys())
for root in (E,C):
    for change in json.loads(read(R/'usm-code-changes.json')):
        p=root/change['file'];s=read(p)
        assert s.count(change['find'])==change['count'],change
        write(p,s.replace(change['find'],change['replace']))

# A reply is historical information: snapshot its kind before request cleanup.
replace_once(C,'common/scripted_effects/nesnd_jp_foreign.txt',
    'trigger_event = { id = nesnd_jp_foreign.2 popup = yes }',
    'save_scope_value_as = { name = jp_reply_kind value = nesnd_jp_request_kind }\n                trigger_event = { id = nesnd_jp_foreign.2 popup = yes }')
descs='''desc = {
        first_valid = {
'''
for kind in (1,2,3,4,5,7):
    descs+='''            triggered_desc = {
                trigger = {
                    trigger_if = {
                        limit = { exists = scope:jp_reply_kind }
                        scope:jp_reply_kind = KIND
                    }
                    trigger_else = { always = no }
                }
                desc = nesnd_jp_foreign.2.dKIND
            }
'''.replace('KIND',str(kind))
descs+='''            desc = nesnd_jp_foreign.2.d
        }
    }'''
replace_once(C,'events/nesnd_jp_foreign.txt','desc = nesnd_jp_foreign.2.d',descs)

for label,proposals in [('usm',usm),('japan-qin',jp)]:
    rows={}
    for root in (E,C):
        selected={k:v for k,v in proposals.items() if root==C or not v.get('apply_to','E_and_C').startswith('C_only')}
        rows[str(root)]=apply_proposals(root,selected)
    dump(R/(label+'-applied.json'),rows)
    print(label,len(proposals),[(Path(k).name,len(v)) for k,v in rows.items()])

for root in (E,C):
    for rel in ['common/scripted_buttons/nesnd_south_accords.txt','common/scripted_buttons/nesnd_crisis_buttons.txt','events/nesnd_south_accords.txt']:
        parse(read(root/rel))
parse(read(C/'events/nesnd_jp_foreign.txt'))
print('Editorial proposals and display branches applied; main unchanged.')
