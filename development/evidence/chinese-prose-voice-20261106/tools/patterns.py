"""Count candidate words/constructions across the three corpora.
python3 -I patterns.py corpora.json repo out.json
Counts are over prose entries (>=12 CJK chars after stripping codes).
"""
import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mine import clean, is_prose, chars
from fields import index, classify

# (label, regex). Sentence-scope patterns use [^。！？\n]* so they stay in one sentence.
S = r'[^。！？；\\]{0,40}'
PATTERNS = [
    ('生计', r'生计'),
    ('好处后补代价：可以/能……，但/却/不过……', r'(可以|可|能够|能)' + S + r'，(但|却|不过|只是|然而)'),
    ('须决定/判断/衡量/考虑（收尾抛给玩家）', r'(须|应当|要)(先)?(决定|判断|衡量|考虑|权衡|选择)'),
    ('……，又……（双问并列：须决定X，又愿意Y）', r'(决定|判断|衡量)' + S + r'，又'),
    ('也有人/有人主张（各方并陈）', r'也有人|有人(主张|认为|希望)'),
    ('政府（泛称主语）', r'政府'),
    ('朝廷（泛称主语）', r'朝廷'),
    ('两国/双方（对称叙述）', r'两国|双方'),
    ('谁……谁/由谁（设问罗列）', r'由谁|听谁|归谁'),
    ('……的余地/回旋余地', r'余地'),
    ('利益', r'利益'),
    ('然而……(并)不能/无法', r'然而' + S + r'(并不能|不能|无法|难以)'),
    ('不是……而是', r'不是' + S + r'而是'),
    ('既……也/又', r'既' + S + r'(也|又)'),
    ('在……之间', r'在' + S + r'之间'),
    ('此项/此事/本次（开发口吻指代）', r'此项|本次|本项'),
    ('相关', r'相关'),
    ('推进', r'推进'),
    ('能否……（将）决定/关系着', r'能否' + S + r'(将决定|决定|关系|取决)'),
    ('关系着/关系到', r'关系(着|到)'),
    ('也须/仍须/还须/须先', r'(也|仍|还|亦)须|须先'),
    ('……，同时……（并举）', r'，同时'),
    ('无论……还是/都', r'无论' + S + r'(还是|都|均)'),
    ('如今', r'如今'),
    ('已经……（完成体）', r'已经'),
    ('终于', r'终于'),
    ('也（补述代价）：“……，也……”', r'，(?:[^，。]{0,8})也(?:须|要|得|将|会|不)'),
    ('却（转折）', r'却'),
    ('仍（仍在/仍然/仍须）', r'仍'),
    ('秩序', r'秩序'),
    ('往来', r'往来'),
    ('安排', r'安排'),
    ('承担', r'承担'),
    ('地方（泛称）', r'地方(?!官|志|自治)'),
    ('争取', r'争取'),
    ('共同', r'共同'),
    ('希望', r'希望'),
    ('等候/等待……决定/答复', r'(等候|等待)' + S + r'(决定|答复|裁断)'),
    ('须就此/须作出决定', r'须就此|须(作出|做出)(决定|选择|答复)|作出决定'),
    ('人们', r'人们'),
    ('将怎样/如何……（悬问收尾）', r'(将怎样|将如何|会怎样|怎样生活)'),
    ('从此', r'从此'),
    ('经营', r'经营'),
    ('付出代价/代价', r'代价'),
    ('稳住/稳定', r'稳住|稳定'),
    ('依据/裁断', r'依据|裁断'),
    ('确保', r'确保'),
    ('维持', r'维持'),
    ('（使）……有了……', r'有了'),
    ('取决于', r'取决于'),
    ('事务', r'事务'),
    ('处置/处理', r'处置|处理'),
    ('若……则/便', r'若' + S + r'(则|便)'),
    ('并非', r'并非'),
    ('只能/只得', r'只能|只得'),
    ('不再', r'不再'),
    ('真正', r'真正'),
    ('各自', r'各自'),
]


def load(path):
    d = json.load(open(path, encoding='utf-8'))
    author = [(k, v) for k, vs in d['author'].items() for v in vs if is_prose(v)]
    vanilla = [(k, v) for k, v in d['vanilla'].items() if is_prose(v)]
    agent = [(r['key'], r['value']) for r in d['current']
             if r['status'] in ('agent_new', 'agent_changed') and is_prose(r['value'])]
    return d, author, vanilla, agent


def count(entries, rx):
    occ = 0
    keys = []
    for k, v in entries:
        n = len(re.findall(rx, clean(v)))
        if n:
            occ += n
            keys.append(k)
    return occ, keys


if __name__ == '__main__':
    d, author, vanilla, agent = load(sys.argv[1])
    repo, out = sys.argv[2], sys.argv[3]
    ix = index(repo)
    ca, cv, cg = (chars([v for _, v in x]) for x in (author, vanilla, agent))
    res = []
    for label, rx in PATTERNS:
        g, gk = count(agent, rx)
        a, ak = count(author, rx)
        v, _ = count(vanilla, rx)
        rg, ra, rv = g / cg * 1e4, a / ca * 1e4, v / cv * 1e4
        res.append({'label': label, 'regex': rx, 'agent': g, 'agent_keys': len(gk), 'author': a,
                    'vanilla': v, 'agent_per10k': round(rg, 2), 'author_per10k': round(ra, 2),
                    'vanilla_per10k': round(rv, 2),
                    'ratio_vs_author': round(rg / max(ra, 0.01), 1),
                    'ratio_vs_vanilla': round(rg / max(rv, 0.01), 1),
                    'agent_examples': gk[:8], 'author_examples': ak[:5]})
    res.sort(key=lambda r: -(min(r['ratio_vs_author'], r['ratio_vs_vanilla']) * (r['agent'] ** 0.5)))
    json.dump({'chars': {'author': ca, 'vanilla': cv, 'agent': cg},
               'entries': {'author': len(author), 'vanilla': len(vanilla), 'agent': len(agent)},
               'patterns': res}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('chars', ca, cv, cg)
    for r in res:
        print(f"{r['label'][:22]:<24}\t代理{r['agent']}({r['agent_per10k']})/{r['agent_keys']}键\t作者{r['author']}({r['author_per10k']})\t原版{r['vanilla']}({r['vanilla_per10k']})")
